import mysql.connector as sql
cn=sql.connect(user="root", password="admin", host="localhost", database="management")
cr=cn.cursor(buffered=True)
try:
    cr.execute("Create table contacts(name varchar(30), number double, id varchar(30), password varchar(40));")
except:
    pass
while(1):
    print("Enter 1 to add new details")
    print("Enter 2 to quit")
    a=int(input())
    if a==1:
        name=input("Enter name: ")
        number=int(input("Enter number: "))
        id=input("Enter id: ")
        passw=input("Enter password: ")
        query="Insert into contacts values(%s,%s,%s,%s)"
        cr.execute(query,(name,number,id,passw))
        cn.commit()
    if a==2:
        break
