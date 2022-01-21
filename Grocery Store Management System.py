import pandas as pd
import mysql.connector as  sql
conn=sql.connect(host='localhost',user='root',password='09062003',database='grocery_shop',charset='utf8')
if conn.is_connected():
    print('         SUCCESSFULLY CONNECTED TO THE DATAFRAME')
c=conn.cursor()


def menu():
    
    print(' -----------------------------------------------------------------------------------------------------')
    print('#=#=#=#=#  LOGIN SUCCESSFUL  #=#=#=#=#')
    print(' -----------------------------------------------------------------------------------------------------')
    print('     1.Create Table Customer Details')
    print('     2.Create Table Product Details')
    print('     3.Create Table Worker Details')
    print('     4.Insert New Customer Details')
    print('     5.Insert New Product Details')
    print('     6.Insert New Worker Details')
    print('     7.See All Customer Details')
    print('     8.See All Product Details')
    print('     9.See All Worker Details')
    print('     10.See Selected Number of Customer Details from Top')
    print('     11.See Selected Number of Product Details from Top')
    print('     12.See Selected Number of Worker Details from Top')
    print('     13.See Selected Number of Customer Details from Bottom')
    print('     14.See Selected Number of Product Details from Bottom')
    print('     15.See Selected Number of Worker Details from Bottom')
    print('     16.EXIT')
    print('\n')

def CreateCust():
    c.execute('create table if not exists customer_details(phone_no int(13),cust_name varchar(25),cost float(10))')
    c.commit()
    print('Customer Table Created')
    
def CreateProd():
    c.execute('create table if not exists product_details(product_name varchar(25),product_cost float(10))')
    c.commit()
    print('Product Table Created')
    
def CreateWork():
    c.execute('create table if not exists worker_details(worker_name varchar(25),worker_work varchar(10),worker_age int(3), worker_salary float(10),phone_no int(13))')
    print('Worker Table Created')
    
def CustIn():
    cust_name=input('Enter Customer\'s Name=')
    phone_no=int(input('Enter Customer\'s Phone Number='))
    cost=float(input('Enter Customer\'s Cost='))
    sql_insert="insert into customer_details values("+str(phone_no)+","+str(cust_name)+"',"+str(cost)+")"
    c.execute(sql_insert)
    conn.commit()
    print('DATA ENTERED')

def ProdIn():
    product_name=input('Enter Product Name=')
    product_cost=float(input('Enter The Cost='))
    sql_insert="insert into product_details values("+str(product_name)+","+str(product_cost)+")"
    c.execute(sql_insert)
    conn.commit()
    print('DATA ENTERED')

def WorkIn():
    worker_name=input('Enter Worker\'s Name=')
    worker_work=input('Enter Area Of Work=')
    worker_age=int(input('Enter Age='))
    worker_salary=float(input('Enter Salary='))
    phone_no =int(input('Enter Phone Number='))
    sql_insert="insert into worker_details values("+str(worker_name)+"'," +str(worker_work)+"',"+str(worker_age)+","+str(worker_salary)+","+str(phone_no)+ ")"
    c.execute(sql_insert)
    conn.commit()
    print('DATA ENTERED')

def CustSee():
    df=pd.read_sql("select * from customer_details",conn)
    
def ProdSee():
    df=pd.read_sql("select * from product_details",conn)

def WorkSee():
    df=pd.read_sql("select * from worker_details",conn)

def CustTop():
    df=pd.read_sql("select * from customer_details",conn)
    r=int(input("Enter the Number of Details you want to see from top"))
    print(df.head(r))

def ProdTop():
    df=pd.read_sql("select * from product_details",conn)
    r=int(input("Enter the Number of Details you want to see from top"))
    print(df.head(r))

def WorkTop():
    df=pd.read_sql("select * from worker_details",conn)
    r=int(input("Enter the Number of Details you want to see from top"))
    print(df.head(r))

def CustBottom():
    df=pd.read_sql("select * from customer_details",conn)
    r=int(input("Enter the Number of Details you want to see from bottom"))
    print(df.tail(r))

def ProdBottom():
    df=pd.read_sql("select * from product_details",conn)
    r=int(input("Enter the Number of Details you want to see from bottom"))
    print(df.tail(r))

def WorkBottom():
    df=pd.read_sql("select * from worker_details",conn)
    r=int(input("Enter the Number of Details you want to see from bottom"))
    print(df.tail(r))

def Stocks():
    print('******************************************')
    f=open('test.txt','r')
    data=f.read()
    print(data)
    f.close()
    print('******************************************')

def PieChart():
    import matplotlib.pyplot as plt
    items=('shoes','stationary','watch','house use','food items')
    avalibility=[156,200,103,206,196]
    colors=['red','yellowgreen','blue','gold','green']
    plt.pie(avalibility,labels=items,colors=colors)
    plt.title('Avalibility of Items in Shop')
    plt.show()

print(' -----------------------------------------------------------------------------------------------------')
print('#####  WELCOME TO GROCERY SHOP MANAGEMENT SYSTEM  #####')
print(' -----------------------------------------------------------------------------------------------------')
print('1.   LOGIN')
print('2.   EXIT')
choice=int(input('SELECT YOUR CHOICE :  '))
if choice==1:
    c=0 #variable to limit user attempts
    while True:  #loop to create login
        user_name=input('ENTER USERNAME =  ')
        password=input('ENTER PASSWORD =  ')
        c=+1
        if c==3:
            print('You have already reached maximum attempts')
            break
        else:
            if user_name=='vidit' and password=='1234':
                print('\n')
                menu()
                select=int(input('Enter the Corresponding Choice :   '))
                while select !=16:
                    print('\n')
                    if select==1:
                        CreateCust()
                    if select==2:
                        CreateProd()
                    if select==3:
                        CreateWork()
                    if select==4:
                        CustIn()
                    if select==5:
                        ProdIn()
                    if select==6:
                        WorkIn()
                    if select==7:
                        CustSee()
                    if select==8:
                        ProdSee()
                    if select==9:
                        WorkSee()
                    if select==10:
                        CustTop()
                    if select==11:
                        ProdTop()
                    if select==12:
                        WorkTop()
                    if select==13:
                        CustBottom()
                    if select==14:
                        ProdBottom()
                    if select==15:
                        WorkBottom()
                    if select==16 :
                        exit()
            else:
                print('Either the Username or the Password is wrong. Try Again ')                
if choice==2:
    exit()
            
