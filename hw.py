from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import socket
import requests
import bs4
import matplotlib.pyplot as plt

def f1():
	adst.deiconify()
	root.withdraw()
def f2():
	root.deiconify()
	adst.withdraw()
def f3():
	root.deiconify()
	vst.withdraw()
def f4():
	con=None
	try:
		con=connect("sms2.db")
		rno=int(entrno.get())
		name1=entname.get()
		if len(name1)>=2:
			name=entname.get()
		else:
			showwarning("Warning","Enter Valid Name")
		mks=int(entmks.get())
		args=(rno,name,mks)
		cursor=con.cursor()
		sql="insert into student values('%d','%s','%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success","Record Added")
	except Exception as e:
		showerror("Failed","Issue: Record was Not Added")
		con.rollback()
	finally:
		if con is not None:
			con.close()
def f5():
	stdata.delete(1.0,END)
	vst.deiconify()
	root.withdraw()
	try:
		con = connect("sms2.db")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info + "rno: "+ str(d[0]) + "\t\t"+"name: " + str(d[1]) +"\t\t\t"+"marks: "+ str(d[2])+"\n"
		stdata.insert(INSERT,info)
	except Exception as e:
		showerror("Failed","Issue "+str(e))
	finally:
		if con is not None:
			con.close()
def f6():				#to go from delete to root
	root.deiconify()
	delst.withdraw()
def f7():				#from root to update 
	delst.deiconify()
	root.withdraw()
		
def f8():				#Deletion	
	con=None
	try:
		con=connect("sms2.db")
		rno=int(entdel.get())
		args=(rno)
		cursor=con.cursor()
		sql="delete from student where erno='%d'"
		cursor.execute(sql % args)
		if cursor.rowcount>=1:
			con.commit()
			showinfo("Deletion","Record Deleted")
		else:
			showerror("Failed","No Record Found")
	except Exception as e:
		showerror("Issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def f9():				#root to update
	updst.deiconify()
	root.withdraw()

def f10():				#update to root
	root.deiconify()
	updst.withdraw()

def f11():
	con=None
	try:
		con=connect("sms2.db")
		rno=int(ent_upd_rno.get())
		
		name1=ent_upd_name.get()
		if len(name1)>=2:
			name=ent_upd_name.get()
		else:
			showwarning("Warning","Enter Valid Name")
	
		marks=int(ent_upd_mks.get())
		args=(name,marks,rno)
		cursor=con.cursor()
		sql="update student SET ename='%s',emarks='%d' where erno='%d'"
		cursor.execute(sql % args)
		if cursor.rowcount>=1:
			con.commit()
			showinfo("Success","Record Updated")
		else:
			showerror("Failure","No Record Found")
	except Exception as e:
		showerror("Failed","Issue: Record was Not Updated")		
		con.rollback
	finally:
		if con is not None:
			con.close()

def f12():		# Chart-----------------------
	con=None
	list_name,list_marks=[],[]
	try:
		con= connect("sms2.db")
		cursor=con.cursor()
		sql="select * from student ORDER BY emarks DESC"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			list_name.append(d[1])
			list_marks.append(d[2])
		plt.bar(list_name[:5],list_marks[:5],color=['red', 'green', 'blue', 'red', 'green'])

		plt.title("Batch Information")
		plt.xlabel=("Name")
		plt.ylabel=("Marks")
		plt.grid()
		plt.show()

	except Exception as e:
		showerror("Select Issue",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()


def f13(a):		#Validate  Rollno-------------
	if a.isdigit():
		return True
	elif a is "":
		return True
	else:
		showwarning("Warning","Enter Digits Only")
		return False

def f14(a):		#Validate Mks--------------
	if a.isdigit() :
		if 0<=int(a)<=100:
			return True
		else:
			showwarning("Warning","Enter Valid Marks")
			return False
	elif a is "":
		return True
	else:
		showwarning("Warning","Enter Digits Only")
		return False


def f15(a):		#Validate Name-----------------
	if a.isalpha():
		return True
	elif a is "":
		return True

	else:
		showwarning("Warning","Enter Alphabets Only")
		return False
	

	
#root-----------------------------------------------
root=Tk()
root.title("S. M. S")
root.geometry("500x600+450+100")
root.configure(background='rosy brown')
root.resizable(0,0)

lbl=Label(root,text="STUDENT INFO SYSTEM",font=("times",25,"bold underline"))
lbl.pack(pady=10)
btnadd=Button(root,text="ADD",font=("times",18,"bold"),command=f1)
btnadd.place(x=230,y=100)
btnview=Button(root,text="VIEW",font=("times",18,"bold"),command=f5)
btnview.place(x=220,y=170)
btndel=Button(root,text="DELETE",font=("times",18,"bold"),command=f7)
btndel.place(x=220,y=240)
btnupd=Button(root,text="UPDATE",font=("times",18,"bold"),command=f9)
btnupd.place(x=220,y=310)
btncharts=Button(root,text="CHARTS",font=("times",18,"bold"),command=f12)
btncharts.place(x=220,y=380)



#LOCATION---------------------------------------------

socket.create_connection(("www.google.com",80))
res=requests.get("https://ipinfo.io")
data=res.json()
city_name=data['city']
	
lbl_location=Label(root,text="LOCATION: "+str(city_name),font=("times",18,"bold"))
lbl_location.place(x=10,y=460)
	

#Temperature----------------------------------------------

socket.create_connection( ("www.google.com", 80))
a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
a2 = "&q=" + "kalyan" 
a3 = "&appid=c6e315d09197cec231495138183954bd"
api_address =  a1 + a2  + a3 		
res = requests.get(api_address)
data=res.json()
temp2=data['main']['temp']
	
lbl_location=Label(root,text="TEMP: "+str(temp2)+"\u2103",font=("times",18,"bold"))
lbl_location.place(x=320,y=460)


#Quote of the day--------------------------------------

socket.create_connection(("www.google.com",80))
res=requests.get("https://www.brainyquote.com/quote_of_the_day")
soup=bs4.BeautifulSoup(res.text,'lxml')
data=soup.find('img',{"class":"p-qotd"})
qotd=data['alt']
'''
lbl_qotd=Label(root,text="
QOTD: "+str(qotd),font=("times",18,"bold"))
lbl_qotd.place(x=15,y=490)
'''
T =Text(root,height=3, width=38,font=('times',18,'bold'))
T.place(x=15,y=500)
T.insert(END, str(qotd))



# Add Student-------------------
adst=Toplevel(root)
adst.title("Add Student")
adst.geometry("500x550+450+100")
adst.withdraw()
adst.resizable(0,0)

lbleno=Label(adst,text="Enter Roll no",font=("times",18,"bold"))
lbleno.pack(pady=10)


validation_add_rno = adst.register(f13)
entrno=Entry(adst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_add_rno,'%P'))
entrno.pack(pady=10)



lblname=Label(adst,text="Enter Name",font=("times",18,"bold"))
lblname.pack(pady=10)

validation_add_name = adst.register(f15)
entname=Entry(adst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_add_name,'%P'))
entname.pack(pady=10)

lblmks=Label(adst,text="Enter Marks",font=("times",18,"bold"))
lblmks.pack(pady=10)



validation_add_mks = adst.register(f14)
entmks=Entry(adst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_add_mks,'%P'))
entmks.pack(pady=10)


btnsave=Button(adst,text="SAVE",font=("times",18,"bold"),command=f4)
btnsave.pack(pady=10)
btnback=Button(adst,text="BACK",font=("times",18,"bold"),command=f2)
btnback.pack(pady=10)


#View Student ---------------------------------

vst=Toplevel(root)
vst.title("View Student")
vst.geometry("620x550+550+100")
vst.withdraw()
vst.resizable(0,0)

stdata=ScrolledText(vst,width=60,height=15,font=("times",18,"bold"))
stdata.pack(pady=10)
btnback1=Button(vst,text="BACK",font=("times",18,"bold"),command=f3)
btnback1.pack(pady=10)


#Delete Student-----------------------

delst=Toplevel(root)
delst.title("Delete Student")
delst.geometry("500x400+400+200")
delst.withdraw()
delst.resizable(0,0)

lbldel=Label(delst,text="Enter Rollno",font=("times",18,"bold"))
lbldel.pack(pady=10)


validation_del_rno = delst.register(f13)
entdel=Entry(delst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_del_rno,'%P'))
entdel.pack(pady=20)

btndel=Button(delst,text="DELETE",font=("times",18,"bold"),command=f8)
btndel.pack(pady=10)
btndelback=Button(delst,text="BACK",font=("times",18,"bold"),command=f6)
btndelback.pack(pady=10)



#Updation------------------------------------
updst=Toplevel(root)
updst.title("UPDATION")
updst.geometry("500x550+400+200")
updst.withdraw()
updst.resizable(0,0)

lbl_upd_rno=Label(updst,text="Enter Roll no",font=("times",18,"bold"))
lbl_upd_rno.pack(pady=10)

validation_upd_rno = updst.register(f13)
ent_upd_rno=Entry(updst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_upd_rno,'%P'))
ent_upd_rno.pack(pady=10)

lbl_upd_name=Label(updst,text="Enter Name",font=("times",18,"bold"))
lbl_upd_name.pack(pady=10)

validation_upd_name = updst.register(f15)
ent_upd_name=Entry(updst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_upd_name,'%P'))
ent_upd_name.pack(pady=20)


lbl_upd_mks=Label(updst,text="Enter Marks",font=("times",18,"bold"))
lbl_upd_mks.pack(pady=10)

validation_upd_mks = updst.register(f14)
ent_upd_mks=Entry(updst,bd=5,width=20,font=("times",18,"bold"),validate="key",validatecommand=(validation_upd_mks,'%P'))
ent_upd_mks.pack(pady=20)


btnupd=Button(updst,text="UPDATE",font=("times",18,"bold"),command=f11)
btnupd.pack(pady=10)
btn_upd_back=Button(updst,text="BACK",font=("times",18,"bold"),command=f10)
btn_upd_back.pack(pady=10)



root.mainloop()