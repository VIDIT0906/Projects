import requests
import json
from io import BytesIO
from datetime import datetime
import os
import random
import re
import time
from dotenv import load_dotenv

load_dotenv()

# ================== CONFIG ==================
username = os.environ.get("USER")
password = os.environ.get("PASS")
file_id = os.environ.get("FILE_ID")
filename = ""


# ================== UTIL ==================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def retry(func, retries=3, delay=2):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            log(f"[Retry {i+1}] {e}")
            if i == retries - 1:
                raise
            time.sleep(delay)


def generate_file_key(length=13):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "U" + ''.join(random.choice(chars) for _ in range(length))


# ================== CLIENT ==================
class NaukriClient:
    LOGIN_URL = "https://www.naukri.com/central-login-services/v1/login"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        log("Logging in...")
        resp = self.session.post(
            self.LOGIN_URL,
            headers={
                "accept": "application/json",
                "appid": "105",
                "clientid": "d3skt0p",
                "content-type": "application/json",
                "referer": "https://www.naukri.com/nlogin/login",
                "systemid": "jobseeker",
                "user-agent": "Mozilla/5.0",
            },
            json={
                "username": self.username,
                "password": self.password
            }
        )
        resp.raise_for_status()
        log("Login successful")

    def get_token(self):
        return self.session.cookies.get("nauk_at")

    def fetch_form_key(self):
        log("Fetching form_key from page state...")

        resp = self.session.get(
            "https://www.naukri.com/mnjuser/homepage",
            headers={
                "user-agent": "Mozilla/5.0",
                "accept": "text/html",
            }
        )

        resp.raise_for_status()

        # Extract JSON blob
        match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*});', resp.text)

        if not match:
            raise Exception("INITIAL_STATE not found")

        data = json.loads(match.group(1))

        # 🔍 Traverse safely
        def find_form_key(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "formKey":
                        return v
                    result = find_form_key(v)
                    if result:
                        return result
            elif isinstance(obj, list):
                for item in obj:
                    result = find_form_key(item)
                    if result:
                        return result
            return None

        form_key = find_form_key(data)

        if not form_key:
            raise Exception("form_key not found in state")

        log(f"form_key: {form_key}")
        return form_key

    def fetch_profile_id(self):
        log("Fetching profile ID...")
        resp = self.session.get(
            "https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v0/users/self/dashboard",
            headers={
                "accept": "application/json",
                "appid": "105",
                "clientid": "d3skt0p",
                "systemid": "fileupload",
                "origin": "https://www.naukri.com",
                "referer": "https://www.naukri.com/",
                "user-agent": "Mozilla/5.0",
            },
        )
        resp.raise_for_status()
        data = resp.json()

        pid = data.get("dashBoard", {}).get("profileId") or data.get("profileId")
        if not pid:
            raise Exception("Profile ID not found")

        log(f"Profile ID: {pid}")
        return pid


# ================== MAIN ==================
def update_resume():
    if not username or not password:
        return {"success": False, "error": "Missing credentials"}

    if not file_id:
        return {"success": False, "error": "Missing file_id"}

    client = NaukriClient(username, password)

    try:
        retry(client.login)
        token = client.get_token()

        if not token:
            return {"success": False, "error": "Token missing"}

        # form_key = retry(client.fetch_form_key)
        form_key = "null"   # or ""

        # ---- Download resume ----
        log("Downloading resume...")
        drive_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        res = retry(lambda: requests.get(drive_url))
        res.raise_for_status()

        if res.content[:4] != b'%PDF':
            return {"success": False, "error": "Invalid PDF"}

        if len(res.content) > 2 * 1024 * 1024:
            return {"success": False, "error": "File too large (>2MB)"}

        today = datetime.now()
        final_filename = filename or f"resume_{today.strftime('%d_%B_%Y').lower()}.pdf"
        FILE_KEY = generate_file_key()

        # ---- Upload ----
        log("Uploading resume...")

        def upload():
            return client.session.post(
                "https://filevalidation.naukri.com/file",
                headers={
                    "accept": "application/json",
                    "appid": "105",
                    "systemid": "fileupload",
                    "origin": "https://www.naukri.com",
                    "referer": "https://www.naukri.com/",
                    "user-agent": "Mozilla/5.0",
                },
                files={
                    "file": (final_filename, BytesIO(res.content), "application/pdf")
                },
                data={
                    "fileName": final_filename,
                    "uploadCallback": "true",
                    "fileKey": FILE_KEY,
                }
            )

        upload_resp = retry(upload)
        upload_resp.raise_for_status()

        try:
            upload_json = upload_resp.json()

            # Sometimes formKey comes back here
            form_key = upload_json.get("formKey", form_key)
            if FILE_KEY not in upload_json:
                FILE_KEY = next(iter(upload_json.keys()))
        except Exception:
            pass

        # ---- Profile Update ----
        profile_id = retry(client.fetch_profile_id)

        log("Updating profile...")

        payload = {
            "textCV": {
                "fileKey": FILE_KEY,
                "textCvContent": None
            }
        }

        def update():
            return client.session.put(
                f"https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v0/users/self/profiles/{profile_id}/advResume",
                headers={
                    "accept": "application/json",
                    "appid": "105",
                    "clientid": "d3skt0p",
                    "systemid": "Naukri",
                    "authorization": f"Bearer {token}",
                    "content-type": "application/json",
                    "origin": "https://www.naukri.com",
                    "referer": "https://www.naukri.com/mnjuser/profile",
                    "user-agent": "Mozilla/5.0",
                },
                data=json.dumps(payload)
            )

        resp = retry(update)
        resp.raise_for_status()

        log("Resume updated successfully ✅")

        return {
            "success": True,
            "file_key": FILE_KEY
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ================== HANDLER ==================
def handler(event=None, context=None):
    log("Cron job started")
    result = update_resume()
    log(f"Result: {result}")
    return result


# ================== RUN ==================
if __name__ == "__main__":
    print(handler())