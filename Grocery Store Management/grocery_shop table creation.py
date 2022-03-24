import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='1001001',database='grocery_shop')
if conn.is_connected():
    print('successfully connected')

c=conn.cursor()
c.execute('create table if not exists customer_details(phone_no int(13),cust_name varchar(25),cost float(10))')
print('table created')

c.execute('create table if not exists product_details(product_name varchar(25),product_cost float(10))')
print('table created')

c.execute('create table if not exists worker_details(worker_name varchar(25),worker_work varchar(10),worker_age int(3), worker_salary float(10),phone_no int(13))')
print('table created')
