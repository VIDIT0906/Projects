#PLEASE CHANGE CONN AND CONN1 ACCORDING TO YOUR SYSTEM

import pandas as pd
import mysql.connector as  sql
conn1=sql.connect(host='localhost',user='root',password='09062003')
#if conn1.is_connected():
    #print('           SUCCESSFULLY CONNECTED TO THE DATAFRAME')
#else:
    #print('           CONNECTION TO DATAFRAME UNSUCCESSFUL')
c1=conn1.cursor()
c1.execute('CREATE DATABASE IF NOT EXISTS banking')
c1.close()
conn1.close()


conn=sql.connect(host='localhost',\
                 user='root',password='09062003',database='banking')
#if conn.is_connected():
    #print('           SUCCESSFULLY CONNECTED TO THE DATAFRAME')
#else:
    #print('           CONNECTION TO DATAFRAME UNSUCCESSFUL')
cursor=conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS customer\
(acno int(11) AUTO_INCREMENT Primary key, name char(30), \
address varchar(100), phone varchar(15), email varchar(80), \
aadhar_no varchar(20), acc_type varchar(20), status char(15), \
balance float(15,2))")
cursor.execute("CREATE TABLE IF NOT EXISTS transaction\
(tid int(11) AUTO_INCREMENT Primary key, \
dot date, amount int(10), type char(20), acno int(10))")
print("-"*120)
print('\n\n\n\t\tBACKEND REQUIREMENTS SATISFIED')
from datetime import date

def account_status(acno): #CHECK ACCOUNT STATUS
    sql ="select status,balance from customer where acno ='"+acno+"'"
    result = cursor.execute(sql)
    result = cursor.fetchone()
    
    return result


def deposit_amount():#DEPOSIT
    acno = input('Enter account No :')
    amount = input('Enter amount :')
    today = date.today()
    result = account_status(acno)
    if result [0]== 'active':
      sql1 ="update customer set balance = balance+"+amount + \
             ' where acno = '+acno+' and status="active";'
      sql2 = 'insert into transaction(amount,type,acno,dot) values(' \
             + amount +',"deposit",'+acno+',"'+str(today)+'");'
      cursor.execute(sql2)
      cursor.execute(sql1)
      conn.commit()
      print("\n\nAmount Deposited")

    else:
        print('\n\nClosed or Suspended Account....')
        
    wait= input('\n\n\n Press any key to continue....')

def withdraw_amount():#WITHDRAW
    acno = input('Enter account No :')
    amount = input('Enter amount :')
    today = date.today()
    result = account_status(acno)
    if result[0] == 'active' and int(result[1])>=int(amount):
      sql1 = "update customer set balance = balance-" + \
          amount + ' where acno = '+acno+' and status="active";'
      sql2 = 'insert into transaction(amount,type,acno,dot) values(' + \
          amount + ',"withdraw",'+acno+',"'+str(today)+'");'

      cursor.execute(sql2)
      cursor.execute(sql1)
      conn.commit()
      print('\n\nAmount Withdrawn')

    else:
        print('\n\nClosed or Suspended Account Or Insufficient amount')
        
    wait = input('\n\n\n Press any key to continue....')

def transaction_menu():#TRANSACTION MENU
    while True:
      print('\n')
      print(' Trasaction Menu')
      print("\n1.  Deposit Amount")
      print('\n2.  WithDraw Amount')
      print('\n3.  Back to Main Menu')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))
      if choice == 1:
        deposit_amount()
      if choice == 2:
        withdraw_amount()
      if choice == 3:
        break

def search_menu():#SEARCH MENU
    while True:
      print('\n')
      print(' Search Menu')
      print("\n1.  Account No")
      print('\n2.  Aadhar Card')
      print('\n3.  Phone No')
      print('\n4.  Email')
      print('\n5.  Names')
      print('\n6.  Back to Main Menu')
      print('\n')
      choice = int(input('Enter your choice ...: '))
   
      if choice == 1:
        field_name ='acno'
  
      if choice == 2:
        field_name ='aadhar_no'
   
      if choice == 3:
        field_name = 'phone'
      
      if choice == 4:
        field_name = 'email'

      if choice == 5:
        field_name = 'name'
      
      if choice == 6:
        break
      msg ='Enter '+field_name+': '
      value = input(msg)
      if field_name=='acno':
        sql = 'select * from customer where '+field_name + ' = '+value+';'
      else:
        sql = 'select * from customer where '+field_name +' like "%'+value+'%";'
      cursor.execute(sql)
      records = cursor.fetchall()
      n = len(records)
      print('\n')
      print('Search Result for ', field_name, ' ',value)
      print('-'*80)
      print("Acno\tName\tAddress\t\tPhoneNo\t\tEmail\t\t\tAadharNo\tAccType\tStatus\tBalance")
      for record in records:          
          print(record[0],'\t',record[1],'\t',record[2],'\t',record[3],'\t',\
                record[4],'\t',record[5],'\t',record[6],'\t',record[7],'\t',record[8])
      if(n <= 0):
        print(field_name, ' ', value, ' does not exist')
      wait = input('\n Press any key to continue....')
   
    wait=input('\n Press any key to continue....')
    
def daily_report():#REPORT ON DAILY BASIS
   today = date.today()
   cursor = conn.cursor()
   sql = 'select tid,dot,amount,type,acno from transaction t where dot="'+ str(today)+'";'
   cursor.execute(sql)
   records = cursor.fetchall()   
   print('Daily Report :',today)
   print('-'*120)
   print("TId\tDoT\t\tAmount\tType\tAcno")
   for record in records:
       print(record[0],'\t',record[1],'\t',record[2],'\t',record[3],'\t',record[4])
       
   print('-'*120)   
   wait = input('\n\n\n Press any key to continue....')
   
def monthly_report():#REPORT ON MONTHLY BASIS 
   today = date.today()
   sql = 'select tid,dot,amount,type,acno from transaction t where month(dot)="' + \
       str(today).split('-')[1]+'";'
   cursor.execute(sql)
   records = cursor.fetchall()   
   print('Monthly Report :', str(today).split(
       '-')[1], '-,', str(today).split('-')[0])
   print('-'*120)
   print("TId\tDoT\t\tAmount\tType\tAcno")
   for record in records:
       print(record[0],'\t',record[1],'\t',record[2],'\t',record[3],'\t',record[4])
       
   print('-'*120)
   wait = input('\n\n\n Press any key to continue....')

def account_details():##REPORT BASED ON ACNO
    acno = input('Enter account no :')
    sql ='select * from customer where acno ='+acno+';'
    cursor.execute(sql)
    result = cursor.fetchone()
    print('\n\n\n')
    print('Account Details')
    print('-'*120)
    print('Account No :',result[0])
    print('Customer Name :',result[1])
    print('Address :',result[2])
    print('Phone NO :',result[3])
    print('Email ID :',result[4])
    print('Aadhar No :',result[5])
    print('Account Type :',result[6])
    print('Account Status :',result[7])
    print('Current Balance :',result[8])
    print('-'*120)
    sql1 = 'select tid,dot,amount,type from transaction t where t.acno='+acno+';'
    cursor.execute(sql1)
    results = cursor.fetchall()
    print("Acno\tDoT\t\tAmount\tType")
    for result in results:
        print(result[0],'\t',result[1],'\t',result[2],'\t',result[3])

    wait=input('\n\n\nPress any key to continue.....')

def report_menu():#REPORT MENU
    while True:
      print(' Report Menu')
      print("\n1.    Daily Report")
      print('\n2.    Monthly Report')
      print('\n3.    Account Details')
      print('\n4.    Back to Main Menu')
      choice = int(input('Enter your choice ...: '))
      if choice == 1:
        daily_report()
      if choice == 2:
        monthly_report()
      if choice == 3:
        account_details()
      if choice == 4:
        break

def add_account():#ADD NEW ACCOUNT
    name = input('Enter Name :')
    addr = input('Enter address :')
    phone = input('Enter Phone no :')
    email = input('Enter Email :')
    aadhar = input('Enter Aadhar no :')
    actype = input('Account Type (saving/current ) :')
    balance = input('Enter opening balance :')
    sql='insert into customer(name,address,phone,email,aadhar_no,\
    acc_type,balance,status) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    val=(name,addr,phone,email,aadhar,actype,balance,"active")
    cursor.execute(sql,val)
    conn.commit()
    print('\nNew Customer Added Successfully')
    wait=input('\n\n\nPress any key to continue.....')       

def modify_account():#MODIFY EXISTING ACCOUNT
    acno = input('Enter customer Account No :')
    print('Modify screen ')
    print('\n    1.  Customer Name')
    print('\n    2.  Customer Address')
    print('\n    3.  Customer Phone No')
    print('\n    4.  Customer Email ID')
    choice = int(input('What do you want to change ? '))
    new_data  = input('Enter New value :')
    if choice == 1:
       field_name ="name"
    elif choice == 2:
       field_name = "address"
    elif choice == 3:
       field_name = "phone"
    elif choice == 4:
       field_name = "email"
    sql ='update customer set ' + field_name + '="'+ new_data +'" where acno='+acno+';' 
    cursor.execute(sql)
    conn.commit()
    print('Customer Information Modified....')
    wait=input('\n\n\nPress any key to continue.....')

def close_account():#CLOSE ACTIVE ACCOUNT
    acno = input('Enter customer Account No :')
    sql ='update customer set status="close" where acno ='+acno+';'
    cursor.execute(sql)
    conn.commit()
    print('Account Closed')
    wait=input('\n\n\nPress any key to continue.....')

def menu():#MAIN MENU
    print('-'*120)
    print('#'*15,'LOGIN SUCCESSFUL','#'*15)
    print('-'*120)
    print('\n')
    print(' Main Menu')
    print("\n    1.  Add Account")
    print('\n    2.  Modify Account')
    print('\n    3.  Close Account')
    print('\n    4.  Transaction Menu')
    print('\n    5.  Search Menu')
    print('\n    6.  Report Menu')
    print('\n    7.  Close application')
    print('\n\n')
    

#MAIN LOOPING
print('-'*120)
print('#'*15,'WELCOME TO BANK MANAGEMENT SYSTEM','#'*15)
print('-'*120)
print('\n')
print('1.   LOGIN')
print('2.   EXIT')
select=int(input('SELECT YOUR CHOICE :  '))
if select==1:
    c=0 #variable to limit user attempts
    while c<=3:  #loop to create login
        user_name=input('ENTER USERNAME :  ')
        password=input('ENTER PASSWORD :  ')        
        c+=1
        if c>3:
            print('You have already reached maximum attempts')
            break
        else:
            if user_name=='vidit' and password=='1234':
                print('\n')                
                
                while select ==1:
                    print('\n')
                    menu()
                    choice=int(input('Enter the Corresponding Choice :   '))
                    if choice == 1:
                        add_account()
                    if choice == 2:
                        modify_account()
                    if choice == 3:
                        close_account()
                    if choice ==4 :
                        transaction_menu()
                    if choice ==5 :
                        search_menu()
                    if choice == 6:
                        report_menu()
                    if choice ==7 :
                        exit()
            else:
                print('Either the Username or the Password is wrong. Try Again ')
                print("\n")
elif select==2:
    exit()


