from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import socket
import requests
import json
import bs4


con=None
try :
        con=connect("test.db")  #connect to dbms
        cursor=con.cursor()
        sql="create table student (rno int primary key, name text, marks int)"
        cursor.execute(sql)        #python --> sqlite --> parsing & execution
        print("table created")
except Exception as e:
        print(e)
finally :
        if con is not None :
                con.close()   #clode connection
               
 

#insert student

def f1():
		adst.deiconify()
		root.withdraw()
def f5():
        con=None
        try:
                con=connect("test.db")
                rno=int(entrno.get())
                if rno<0:
                        raise Exception ("Invalid Roll No.")
                name=(entname.get())
                if len(name)<2 :
                        raise Exception ("The name should contain at least 2 letters")
                if name.isalpha()==False:
                        raise Exception("Name should contain letters only!")
                marks=int(entmarks.get())
                if marks<0 or marks>100:
                        raise Exception("Invalid range of marks.")
                args=(rno, name, marks)
                cursor=con.cursor()
                sql="insert into student values ('%d','%s','%d')"
                cursor.execute(sql%args)
                showinfo("Success", "Record Added")
                con.commit()

        except ValueError :
                showerror("Failure","Check if the info is entered properly!")
        except Exception as e:
                showerror("Failure", "Insert issue - " + str(e))
                con.rollback()
        finally:
                if con is not None :
                        con.close()
                
def f2():
		root.deiconify()
		adst.withdraw()


#View Student

def f3():
        stdata.delete(1.0, END)
        visit.deiconify()
        root.withdraw()
        con = None
        try:
                con = connect("test.db")
                cursor = con.cursor()
                sql = "select * from student"
                cursor.execute(sql)
                data = cursor.fetchall()
                info = " "
                for d in data:
                        info ="RollNo : " + str(d[0]) + "\t\t" +"Name : " + str(d[1]) + "\t\t" + "Marks : " + str(d[2]) + "\n"
                        stdata.insert(INSERT, info)
        except Exception as e:
                showerror("Failure", "Select issue: " + str(e))
                con.rollback()
        finally:
                if con is not None:
                        con.close()
                  
def f4():
		root.deiconify()
		visit.withdraw()


#Delete Student

def f7() :
        dlt.deiconify()
        root.withdraw()
def f6():
        
        con=None
        try:
                con=connect("test.db")
                cursor=con.cursor()
                drno=int(entdrno.get())
                if drno<0:
                        raise Exception ("Invalid Roll No.")
                arg=(drno)
                sql="delete from student where rno ='%d' "
                cursor.execute(sql%arg)
                if cursor.rowcount >= 1:
                        showinfo("Success", "Record Deleted")
                        con.commit()
                else :
                        showerror(drno, "doesnt exist")
        except ValueError :
                showerror("Failure","Please enter the details. Value cannot be empty.")
        except Exception as e:
                showerror("Issue"+str(e))
                con.rollback()
        finally :
                if con is not None :
                        con.close()
                       
def f8():
        root.deiconify()
        dlt.withdraw()
                        
		   						
#Update Student

def f9() :
        upd.deiconify()
        root.withdraw()
        


def f10():
        con = None
        try:
                con = connect("test.db")
                cursor = con.cursor()
                urno = int(enturno.get())
                if urno<0:
                        raise Exception ("Invalid Roll No.")
                uname = entuname.get()
                if uname.isalpha()==False :
                        raise Exception ("Name should contain letters only")
                umarks = int(entumarks.get())
                if umarks<0 or umarks>100 :
                        raise Exception("Invalid range of marks.")
                sql = """Update student set name = ?, marks = ? where rno = ? """
                args = (uname, umarks, urno)
                cursor.execute(sql, args)
                con.commit()
                data = cursor.fetchone()
                if cursor.rowcount >= 1:
                        showinfo("Success ", "Record updated")
                else:
                        showinfo("Error", "Roll Number does not exist")
        except ValueError :
                showerror("Failure","Please enter the details. Value cannot be empty.")
        except Exception as e:
                showerror("Failure", "Update issue: " + str(e))
                con.rollback()
        finally:
                if con is not None:
                        con.close()

                        
def f11():
        root.deiconify()
        upd.withdraw()
        
#Chart

def f12():
        con = connect('test.db', isolation_level=None, detect_types=PARSE_COLNAMES)
        data1 = pd.read_sql_query("SELECT * FROM student", con)
        data1.to_csv('student_info.csv', index=False)

        data2 = pd.read_csv("student_info.csv")

        trno = data2['rno'].tolist()
        tname = data2['name'].tolist()
        tmarks = data2['marks'].tolist()

        x = np.arange(len(trno))
        c =  {'xkcd:sky blue', 'c', 'xkcd:hot pink', 'xkcd:greenish yellow', 'xkcd:dark aqua'}
        plt.bar(x, tmarks, width = 0.8, color = c, align = 'center', label = 'Marks')
        plt.xticks(x, tname)
        plt.ylabel("Marks")
        plt.title("Class Performance")
        plt.show()
        
#Location and Temp
def f13() :
        try:
                socket.create_connection(("www.google.com",80))
                res = requests.get("https://ipinfo.io/")
                data = res.json()
                city = data['city']
                a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
                a2 = "&q=" + city
                a3 = "&appid=c6e315d09197cec231495138183954bd"
                api_address =  a1 + a2  + a3
                res = requests.get(api_address)
                data = res.json()
                main = data['main']
                temp1 = main['temp']
                s = ("Location : " + city + "   Temperature : " + str(temp1))
                return (s)
        except OSError as e:
                showerror("Failure", "Issue: " + str(e))
                       

#QOTD
try:
    res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
    print(res)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    quote=soup.find('img',{"class":"p-qotd"})
    mesg=quote['alt']
            
        
except OSError as e:
    print("check network",e)


#######################################################################################
root=Tk()
root.title("STUDENT MANAGEMENT SYSTEM")
root.geometry("800x550+550+350")
root.configure(background='pink')

btnAdd=Button(root, text="Add", font=("Candara", 18, "bold"), width=10, command=f1)
btnVisit=Button(root, text="View", font=("Candara", 18, "bold"), width=10, command=f3)
btnDlt=Button(root, text="Delete",font=("Candara", 18, "bold"), width=10, command=f7)
btnUpd=Button(root, text="Update",font=("Candara", 18, "bold"), width=10, command=f9)
btnCh=Button(root, text="Chart", font=("Candara", 18, "bold"), width=10, command=f12)

loc=LabelFrame(root,text= "Location Detail", font=("SignPainter", 27, "italic"), width=50, bg = 'pink', relief = 'solid', pady=5)
lblloc=Label(loc, text=f13(), font=("SignPainter", 25, "italic"), width=50, bg = 'pink')
QOTD=LabelFrame(root, text= "Quote of the Day", font=("SignPainter", 25), width=50, bg = 'pink', relief = 'solid', pady=5 )
lblQOTD=Label(QOTD, text=mesg, font=("SignPainter", 27), width=50, wraplength = 750, bg = 'pink' )

btnAdd.pack(pady=15)
btnVisit.pack(pady=15)
btnDlt.pack(pady=15)
btnUpd.pack(pady=15)
btnCh.pack(pady=15)
loc.pack(pady=15)
lblloc.pack()
QOTD.pack(padx=15, pady=15)
lblQOTD.pack()

#Add Student Window 

adst=Toplevel(root)
adst.title("ADD STUDENT INFORMATION")
adst.geometry("500x400+400+200")
adst.configure(background='peachpuff')
adst.withdraw()

lblrno=Label(adst, text="Enter Roll Number", font=("Apple Chancery", 18, "bold"), bg = 'peachpuff')
entrno=Entry(adst,bd=5, font=("arial", 18, "bold"))
lblname=Label(adst, text="Enter Name", font=("Apple Chancery", 18, "bold"), bg = 'peachpuff')
entname=Entry(adst,bd=5, font=("arial", 18, "bold"))
lblmarks=Label(adst, text="Enter Marks", font=("Apple Chancery", 18, "bold"), bg = 'peachpuff')
entmarks=Entry(adst,bd=5, font=("arial", 18, "bold"))
btnsave=Button(adst, text="Save", font=("arial", 18, "bold"), command=f5)
btnback=Button(adst, text="Back", font=("arial", 18, "bold"), command=f2)

lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnsave.pack(pady=10)
btnback.pack(pady=10)

#View window
	
visit=Toplevel(root)
visit.title("VIEW STUDENT INFORMATION")
visit.geometry("450x420+400+320")
visit.configure(background='light green')
visit.withdraw()

stdata=ScrolledText(visit, width=50, height=20, bg='light green', font=("corbel", 14))
btnvback=Button(visit, text="Back", font=("arial", 18, "bold") , width=10, command=f4)

stdata.pack(pady=10)
btnvback.pack(pady=10)

#Delete Window

dlt=Toplevel(root)
dlt.title("DELETE STUDENT INFORMATION")
dlt.geometry("500x400+400+200")
dlt.configure(background='lavender')
dlt.withdraw()

lbldrno=Label(dlt, text="Enter Roll Number", font=("Apple Chancery", 18, "bold"), bg = 'lavender')
entdrno=Entry(dlt,bd=5, font=("arial", 18, "bold"))
btndsave=Button(dlt, text="Save", font=("arial", 18, "bold"), width=10, command=f6)
btndback=Button(dlt, text="Back", font=("arial", 18, "bold"), width=10, command=f8)

lbldrno.pack(pady=5)
entdrno.pack(pady=5)
btndsave.pack(pady=10)
btndback.pack(pady=10)


#Update Window

upd=Toplevel(root)
upd.title("UPDATE STUDENT INFORMATION")
upd.geometry("500x400+400+200")
upd.configure(background='lightcyan')
upd.withdraw()

lblurno=Label(upd, text="Enter Roll Number", font=("Apple Chancery", 18, "bold"), bg = 'lightcyan')
lbluname=Label(upd, text="Enter Name", font=("Apple Chancery", 18, "bold"), bg = 'lightcyan')
lblumarks=Label(upd, text="Enter Marks", font=("Apple Chancery", 18, "bold"), bg = 'lightcyan')
enturno=Entry(upd,bd=5, font=("arial", 18, "bold"))
entuname=Entry(upd,bd=5, font=("arial", 18, "bold"))
entumarks=Entry(upd,bd=5, font=("arial", 18, "bold"))
btnusave=Button(upd, text="Save", font=("arial", 18, "bold"), width=10, command=f10)
btnuback=Button(upd, text="Back", font=("arial", 18, "bold"), width=10, command=f11)

lblurno.pack(pady=5)
enturno.pack(pady=5)
lbluname.pack(pady=5)
entuname.pack(pady=5)
lblumarks.pack(pady=5)
entumarks.pack(pady=5)
btnusave.pack(pady=10)
btnuback.pack(pady=10)



root.mainloop()
