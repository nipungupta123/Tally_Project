from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image       #importing all modules needed for my program 
import pickle
import pymysql

master = Tk()              #main window
master.title("Tally Project")
icon_photo = PhotoImage(file = "logo.png")
master.iconphoto(True,icon_photo)       #to set a photo as an icon
master.configure(bg="blue")
master.geometry('450x350')              #change size and color

lsin_frame = LabelFrame(master,padx=10, pady=10,relief= SUNKEN) #frame for log/sign in buttons
lsin_frame.pack(padx=10,pady=10)
lsin_frame.configure(bg = "aquamarine")

logo_img=Image.open("logo.png")
logo_img=logo_img.resize((300, 250), Image.ANTIALIAS)
my_logo_img = ImageTk.PhotoImage(logo_img)
logo_label = Label(lsin_frame,image=my_logo_img)           #printing an image
logo_label.grid(row=0,column=0, columnspan=2)
str_criteria=""  #will be used in change_the_value function

def sign():
    global Id_entry             #globalling variables to use again in other functions
    global pass_entry
    global con_pass_entry
    global top1
    top1 = Toplevel()
    top1.title("Sign in")
    lbl1=Label(top1,text="CREATE YOUR USER ID :").grid(row=0,column=0)    #to show where to enter id
    lbl2=Label(top1,text="CREATE YOUR PASSWORD :").grid(row=1,column=0)
    lbl3=Label(top1,text="CONFIRM YOUR PASSWORD :").grid(row=3,column=0)
    lbl4=Label(top1,text="minimum 8 characters",fg="red").grid(row=2,column=0)
    Id_entry=Entry(top1)              #here user enter the values
    Id_entry.grid(row=0,column=1)
    pass_entry=Entry(top1,show="*")   #it shows what we enter as an asterisk
    pass_entry.grid(row=1,column=1)
    con_pass_entry=Entry(top1,show="*")
    con_pass_entry.grid(row=3,column=1)
    sign_submit_but=Button(top1,text="SUBMIT",bg="light blue",command=sign_submit).grid(row=4,column=0)
    #buttons can be given a command which performs a function

def sign_submit(): #binary file for password is already created
    Id=Id_entry.get()
    Pass=pass_entry.get()  #grt gives the value of what we enter
    con_pass=con_pass_entry.get()
    if (len(Id)<=0):
        messagebox.showwarning("Warning","Invalid ID")  #ID parameter that it can't be null
    elif(len(Pass)<8):
        messagebox.showwarning("Warning","Password should be of atleast 8 characters") #Password can't nbe less than 8 char
    elif(con_pass!=Pass):
        messagebox.showwarning("Warning","Invalid Password") #Pass has to be equal to confirm pass
    else:
        try:
            g=open("Password",'rb')
            f=open("Password",'ab')     #storing in binary file to maintain the secrecy
            found=0                     # a counter variable to check if id exists or not
            while True:
                data=pickle.load(g)
                d=data.keys()
                for i in d:
                    if(i==Id.upper()):
                        messagebox.showwarning("Warning","Sorry!This ID is already there") # messagebox shows a messagebox with warning,info etc.
                        found=1
                    
        except EOFError:
            g.close()
            if found!=1:
                z={Id.upper():Pass}  #storing ID,Password as dictionary
                pickle.dump(z,f)     # dumping values in binary file
                f.close()
                top1.destroy()
                try:
                    myCon = pymysql.connect( host='localhost', user='root', passwd='nipun')
                    cursor = myCon.cursor()     #connecting to database
                    cursor.execute("CREATE DATABASE "+Id)#creaating ID as daabase
                    cursor.execute("use "+Id) #creating table to store data of different accounts(user created) in mysql
                    cursor.execute("CREATE TABLE IF NOT EXISTS Accounts(ID integer PRIMARY KEY,Name varchar(20) NOT NULL,Address varchar(50),Opening_Balance float DEFAULT 0.00,Email_ID varchar(50) )")
                except Exception as e:
                    print("Exception :  {}".format(e))
                finally:
                    myCon.commit()
                    myCon.close()


def log():                  #logging in the program to access its features
    global user_id
    global user_pass
    global top2
    top2 = Toplevel()
    top2.title("Log in")
    lbl1=Label(top2,text="ENTER YOUR USER ID :").grid(row=0,column=0)
    lbl2=Label(top2,text="ENTER YOUR PASSWORD :").grid(row=1,column=0)
    user_id=Entry(top2)
    user_id.grid(row=0,column=1)
    user_pass=Entry(top2,show="*")
    user_pass.grid(row=1,column=1)
    log_submit_but=Button(top2,text="SUBMIT",bg="light blue",command=log_submit).grid(row=3,column=0)

def log_submit():
    global l1       #globalling l1 as used in many places
    l1=user_id.get()
    l2=user_pass.get()
    found=1              #again maintaining counter to check ID and Password
    try:
        g=open("Password",'rb')
        while True:
            data=pickle.load(g)
            d=data.keys()
            for i in d:
                if i==l1.upper():
                    if data[i]==l2:
                        found=0
                        break
    except EOFError:
        g.close()
    if found!=1:
        top2.destroy()
        lsin_frame.destroy()    #destroying frame to edit my main window
        tally()                   #the main structure function call
    else:
        forgot_pass_but=Button(top2,text="Forgot Password click here!",command=forgot_pass).grid(row=2,column=0)
        messagebox.showwarning("Warning","Sorry!This ID or Password is incorrect!")

def forgot_pass():
    top2.destroy()
    global p1
    global p2
    global top3
    top3=Toplevel()
    lbll=Label(top3,text="Type your ID :").grid(row=0,column=0)
    lbl=Label(top3,text="Type your new password :").grid(row=1,column=0)
    p1=Entry(top3)
    p1.grid(row=0,column=1)
    p2=Entry(top3)
    p2.grid(row=1,column=1)
    butttt=Button(top3,text="Enter",command=pass_enter)
    butttt.grid(row=2,column=0,columnspan=2)

def pass_enter():
    r=p1.get()
    new_pass=p2.get()
    try:
        found=1
        h=open("Password",'rb+')
        d=[]
        while True:
            d.append(pickle.load(h))
    except EOFError:
        for i in d:
            for j in i.keys():
                if j==r.upper():
                    if len(new_pass) >=8:
                        i[j]=new_pass
                        found=0
                    else:
                        found=2    
                    break
    if found==0:
        h.seek(0)
        for i in d:
            pickle.dump(i,h)
        h.close()
        messagebox.showinfo("Succesful","Your password is changed successfully")
        top3.destroy()
    elif found==2:
        messagebox.showwarning("Warning","Password should be of atleast 8 characters") #Password can't nbe less than 8 char
    else:
        h.close()
        top3.destroy()
        messagebox.showwarning("OOPS!!","ID does not exist")

def tally():
    master.configure(bg='darkcyan')
    master.geometry('850x500')
    master.title("Tally Project")        #changing parameters of the main window
    welcome_lbl=Label(master,text="WELCOME "+l1.upper()+" !!!",bg="lavender",fg="darkcyan",bd=4,relief=SUNKEN,pady=50)
    welcome_lbl.grid(row=0,column=0,columnspan=5,sticky=W+E) #length of label is from left to right 
    welcome_lbl.config(font=("algerian",50))
    create_acc_but=Button(master,text="CREATE ACCOUNT",padx=30,pady=10,command=create_account).grid(row=1,column=0,pady=100,padx=25)
    acc_info_but=Button(master,text="ACCOUNT INFO",padx=30,pady=10,command=account_info).grid(row=1,column=1,padx=25)
    acc_ent_but=Button(master,text="ACCOUNT ENTRIES",padx=30,pady=10,command=account_entries_fn).grid(row=1,column=2,padx=25)
    bal_sheet_but=Button(master,text="BALANCE SHEET",padx=30,pady=10,command=balance_sheet).grid(row=1,column=3,padx=25)
    exit_but=Button(master,text="EXIT",padx=30,pady=10,command=master.destroy).grid(row=2,column=1,padx=50,columnspan=2)
    bfeedback_but=Button(master,text="FEEDBACK",padx=30,pady=10,command=feedback).grid(row=2,column=0,padx=50,columnspan=2)
    help_but=Button(master,text="HELP",padx=30,pady=10,command=help_tally).grid(row=2,column=2,padx=50,columnspan=2)

def create_account():  #creating accounts with inputs like ID,Name,
    global create_ID   #Opening Balance etc. and store in table in sql
    global create_name
    global create_address
    global create_openingbal
    global create_email
    global top4
    top4=Toplevel()
    top4.title("Create Account")
    lbl1=Label(top4,text="*Enter ID(no.) :").grid(row=0,column=0,padx=10,pady=(10,0))
    lbl2=Label(top4,text="*Enter Name :").grid(row=1,column=0,padx=10)
    lbl3=Label(top4,text="*Enter Address :").grid(row=2,column=0,padx=10)
    lbl4=Label(top4,text="*Enter Opening Balance :").grid(row=3,column=0,padx=10)
    lbl5=Label(top4,text="*Enter Email ID :").grid(row=4,column=0,padx=10)
    create_ID=Entry(top4,width=60,fg="Blue")
    create_ID.grid(row=0,column=1,pady=(10,0))
    create_name=Entry(top4,width=60,fg="Blue")
    create_name.grid(row=1,column=1)
    create_address=Entry(top4,width=60,fg="Blue")
    create_address.grid(row=2,column=1)
    create_openingbal=Entry(top4,width=60,fg="Blue")
    create_openingbal.grid(row=3,column=1)
    create_email=Entry(top4,width=60,fg="Blue")
    create_email.grid(row=4,column=1)
    create_acc_submit_but=Button(top4,text="SUBMIT",command=create_acc_submit)
    create_acc_submit_but.grid(row=5,column=0,columnspan=2)

def create_acc_submit():
    found=0
    try:
        l=create_ID.get()
        m=create_name.get()
        n=create_address.get()
        o=create_openingbal.get()    #taking value from the entry fields
        p=create_email.get()
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun')
        cursor = myCon.cursor()
        cursor.execute("use "+l1)    #storing them in the table accounts
        cursor.execute("INSERT into Accounts values("+str(l)+",\""+m+"\",\""+n+"\","+str(o)+",\""+p+"\")")
        cursor.execute("CREATE TABLE id_"+str(l)+"_account(TID integer PRIMARY KEY,DOT date NOT NULL,Credit float DEFAULT 0.00,Debit float DEFAULT 0.00,MOT varchar(50) )")
        myCon.commit()    #creating table with account ID to store any entries of debit and credit
    except Warning as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()
        top4.destroy()

def account_info():
    global top5
    global acc_id
    top5=Toplevel()
    top5.title("Account Infrormation")
    search_acc_name=Label(top5,text="Enter the ID of the Account :").grid(row=0,column=0,pady=10)
    acc_id=Entry(top5,fg="Blue")
    acc_id.grid(row=0,column=1)  # taking value of the Id to display and change account info
    search_acc_but=Button(top5,text="Enter To Check",command=search_account)
    search_acc_but.grid(row=0,column=2,columnspan=2)


def search_account():
    global record_val
    acc_id_val_inp=acc_id.get()
    if acc_id_val_inp.isnumeric()== True:  #checking if the Id entered is a number and not any other char
        acc_id_val=acc_id_val_inp
    else:
        messagebox.showwarning("Warning","Sorry!It has to be a number!")
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor() #cheking if the Id exists or not
        check_record="SELECT EXISTS(SELECT * from Accounts WHERE ID="+str(acc_id_val)+")"
        cursor.execute(check_record)
        check_record_tupval=cursor.fetchone()
        check_record_numval=check_record_tupval[0]
        if check_record_numval==1: #if Id exists then display info of the account
            cursor.execute("SELECT * from Accounts where ID="+str(acc_id_val))
            record_val=cursor.fetchone()  #fetch the value from table accounts
            acc_id_name_1=Label(top5,text="Name : ").grid(row=1,column=0)  #its in the form of a tuple
            acc_id_name_2=Label(top5,text=str(record_val[1]),fg="Blue").grid(row=1,column=1,sticky=W)
            acc_id_name_change=Button(top5,text="Change Name",command= lambda: change_the_value("Name"))
            acc_id_name_change.grid(row=1,column=2,columnspan=2)
            acc_id_address_1=Label(top5,text="Address : ").grid(row=2,column=0)
            acc_id_addess_2=Label(top5,text=str(record_val[2]),fg="Blue").grid(row=2,column=1,sticky=W)
            acc_id_address_change=Button(top5,text="Change Address",command= lambda: change_the_value("Address"))
            acc_id_address_change.grid(row=2,column=2,columnspan=2)
            acc_id_opening_1=Label(top5,text="Opening Balance : ").grid(row=3,column=0)
            acc_id_opening_2=Label(top5,text=str(record_val[3]),fg="Blue").grid(row=3,column=1,sticky=W)
            acc_id_opening_change=Button(top5,text="Change Opening Balance",command= lambda: change_the_value("Opening_Balance"))
            acc_id_opening_change.grid(row=3,column=2,columnspan=2)
            acc_id_email_1=Label(top5,text="Email ID : ").grid(row=4,column=0)
            acc_id_email_2=Label(top5,text=str(record_val[4]),fg="Blue").grid(row=4,column=1,sticky=W)
            acc_id_email_change=Button(top5,text="Change Email ID",command= lambda: change_the_value("Email_ID"))
            acc_id_email_change.grid(row=4,column=2,columnspan=2)
            del_acc_but=Button(top5,text="Delete this account",command=delete_account)
            del_acc_but.grid(row=5,column=1,columnspan=2)
            close_top5=Button(top5,text="CLOSE",command=top5.destroy)
            close_top5.grid(row=5,column=0,pady=10)  #button to close the window
        else:
            messagebox.showwarning("Warning","Sorry!This ID dos not exist!")
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()



def change_the_value(str_criteria):
    global top6          #window where the new value for name,email,opening balance is entered
    global change_acc_entry
    top6=Toplevel()
    top6.title("Change Value of "+str_criteria)
    change_acc_val=Label(top6,text="Change "+str_criteria).grid(row=0,column=0)
    change_acc_entry=Entry(top6,width=60,fg="Blue")
    change_acc_entry.grid(row=0,column=1)
    comm_change_sub=Button(top6,text="Submit",command= lambda: submit_change_value(str_criteria))
    comm_change_sub.grid(row=1,column=0,columnspan=2)


def submit_change_value(str_criteria):
    change_acc_inp_val=change_acc_entry.get()
    if str_criteria=="Name":   #giving # crit_val a value acc to the str_criteria to change accordingly
        crit_val=1
    elif str_criteria=="Address":
        crit_val=2
    elif str_criteria=="Opening_Balance":
        crit_val=3
    elif str_criteria=="Email_ID":
        crit_val=4
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        change_val_query="UPDATE Accounts SET "+str_criteria+" = \""+change_acc_inp_val+"\" where "+str_criteria+" = \""+str(record_val[crit_val])+"\""
        cursor.execute(change_val_query)  #updating value in accounts according str_criteria
        myCon.commit()    #commiting the changes
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()
        top6.destroy()
        end_top5=Label(top5,text="Please close the window to review changes!!",fg="Red",font=("Algerian",16)).grid(row=5,column=0,columnspan=3)

def delete_account():
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        del_acc_id=acc_id.get()
        cursor.execute("DELETE from Accounts where ID = "+del_acc_id)
        cursor.execute("Drop Table id_"+str(del_acc_id)+"_account")
        myCon.commit()
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()
        top5.destroy()

def account_entries_fn():
    global top7
    global acc_find_entry
    top7=Toplevel()        #entering the values for credit and debit into one account ID
    top7.title("Account Entries")
    acc_find=Label(top7,text="Enter the ID of the Account :").grid(row=0,column=0)
    acc_find_entry=Entry(top7,fg="Blue")
    acc_find_entry.grid(row=0,column=1)
    acc_find_button=Button(top7,text="Enter to Search",command=find_account)
    acc_find_button.grid(row=0,column=2)

def find_account():
    global acc_find_val
    acc_find_val_inp=acc_find_entry.get()
    if acc_find_val_inp.isnumeric()== True:    #checking if the ID entered is a number or not
        acc_find_val=acc_find_val_inp
    else:
        messagebox.showwarning("Warning","Sorry!It has to be a number!")
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        find_record="SELECT EXISTS(SELECT * from Accounts WHERE ID="+str(acc_find_val)+")"
        cursor.execute(find_record)           #checking if the account exists
        find_record_tupval=cursor.fetchone()
        find_record_numval=find_record_tupval[0]
        if find_record_numval==1:     #if the account exists only then the next statements will pass
            credit_but=Button(top7,text="CREDIT",command=credit_but_fn,width=10)
            credit_but.grid(row=1,column=0,padx=10,pady=10,columnspan=2)     #giving option to credit or debit
            debit_but=Button(top7,text="DEBIT",command=debit_but_fn,width=10)
            debit_but.grid(row=1,column=1,pady=10,columnspan=2)
        else:
            messagebox.showwarning("Warning","Sorry!This ID dos not exist!")
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()

def credit_but_fn():     #enter the value in the credit field
    global create_TID
    global create_DOT
    global create_Credit
    global create_MOT
    credit_frame=LabelFrame(top7,padx=10,pady=10,relief= SUNKEN)
    credit_frame.grid(row=2,column=0,columnspan=3)
    lbl1=Label(credit_frame,text="Enter Transaction ID :").grid(row=0,column=0,padx=10,pady=(10,0))
    lbl2=Label(credit_frame,text="Enter Date of Transaction(yyyy-mm-dd) :").grid(row=1,column=0,padx=10)
    lbl3=Label(credit_frame,text="Enter Credit Amount :").grid(row=2,column=0,padx=10)
    lbl4=Label(credit_frame,text="Enter Any Note(related to the transaction) :").grid(row=3,column=0,padx=10)
    create_TID=Entry(credit_frame,width=60,fg="Blue")
    create_TID.grid(row=0,column=1,pady=(10,0))
    create_DOT=Entry(credit_frame,width=60,fg="Blue")
    create_DOT.grid(row=1,column=1)
    create_Credit=Entry(credit_frame,width=60,fg="Blue")
    create_Credit.grid(row=2,column=1)
    create_MOT=Entry(credit_frame,width=60,fg="Blue")
    create_MOT.grid(row=3,column=1)
    credit_submit_but=Button(credit_frame,text="Submit",command=credit_submit)
    credit_submit_but.grid(row=4,column=0,columnspan=2)

def credit_submit():
    l=create_TID.get()
    m=create_DOT.get()
    n=create_Credit.get()  #insert the values of credit into table specific to ID of the account
    o=create_MOT.get()
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        cursor.execute("INSERT into id_"+str(acc_find_val)+"_account values("+str(l)+",\""+str(m)+"\","+str(n)+",0,\""+str(o)+"\")")
        myCon.commit()
        lbl5=Label(top7,text="YOUR CHANGES HAVE BEEN REGISTERED!!",fg="Green",font=("Algerian",16)).grid(row=3,column=0,columnspan=3)
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()

def debit_but_fn():      #enter the value in the debit field
    global create_TID
    global create_DOT
    global create_Debit
    global create_MOT
    debit_frame=LabelFrame(top7,padx=10,pady=10,relief= SUNKEN)
    debit_frame.grid(row=2,column=0,columnspan=3)
    lbl1=Label(debit_frame,text="Enter Transaction ID :").grid(row=0,column=0,padx=10,pady=(10,0))
    lbl2=Label(debit_frame,text="Enter Date of Transaction(yyyy-mm-dd) :").grid(row=1,column=0,padx=10)
    lbl3=Label(debit_frame,text="Enter Debit Amount :").grid(row=2,column=0,padx=10)
    lbl4=Label(debit_frame,text="Enter Any Note(related to the transaction) :").grid(row=3,column=0,padx=10)
    create_TID=Entry(debit_frame,width=60,fg="Blue")
    create_TID.grid(row=0,column=1,pady=(10,0))
    create_DOT=Entry(debit_frame,width=60,fg="Blue")
    create_DOT.grid(row=1,column=1)
    create_Debit=Entry(debit_frame,width=60,fg="Blue")
    create_Debit.grid(row=2,column=1)
    create_MOT=Entry(debit_frame,width=60,fg="Blue")
    create_MOT.grid(row=3,column=1)
    debit_submit_but=Button(debit_frame,text="Submit",command=debit_submit)
    debit_submit_but.grid(row=4,column=0,columnspan=2)

def debit_submit():
    l=create_TID.get()
    m=create_DOT.get()
    n=create_Debit.get()    #insert the values of debit into table specific to ID of the account
    o=create_MOT.get()
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        cursor.execute("INSERT into id_"+str(acc_find_val)+"_account values("+str(l)+",\""+str(m)+"\", 0 ,"+str(n)+",\""+str(o)+"\")")
        lbl5=Label(top7,text="YOUR CHANGES HAVE BEEN REGISTERED!!",fg="Green",font=("Algerian",16)).grid(row=3,column=0,columnspan=3)
        myCon.commit()
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()

def balance_sheet():   #dispaying all the credit and debit records of a specific ID
    global top8
    global bal_find_entry
    top8=Toplevel()
    top8.title("Balance Sheet")
    bal_find=Label(top8,text="Enter the ID of the Account :").grid(row=0,column=0,columnspan=2)
    bal_find_entry=Entry(top8,fg="Blue")
    bal_find_entry.grid(row=0,column=2)
    bal_find_button=Button(top8,text="Enter to Search",command=bal_find_account)
    bal_find_button.grid(row=0,column=3,columnspan=2)

def bal_find_account():
    global bal_record_numval
    global row_count
    global bal_find_val
    global bals_closing_bal
    global bals_opening_bal
    bal_find_val_inp=bal_find_entry.get()
    if bal_find_val_inp.isnumeric()== True:  #check whether the input is number or not
        bal_find_val=bal_find_val_inp
    else:
        messagebox.showwarning("Warning","Sorry!It has to be a number!")
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()  #checking the existence of account
        bal_find_record="SELECT EXISTS(SELECT * from Accounts WHERE ID="+str(bal_find_val)+")"
        cursor.execute(bal_find_record)
        bal_record_tupval=cursor.fetchone()
        bal_record_numval=bal_record_tupval[0]
        if bal_record_numval==1:   #if the account exists only then the next statements will pass
            cursor.execute("SELECT * from Accounts where ID="+str(bal_find_val))
            bal_record_val=cursor.fetchone()
            bals_opening_bal=bal_record_val[3]
            cursor.execute("SELECT SUM(Credit) from id_"+str(bal_find_val)+"_account")
            sum_credit_record=cursor.fetchone()
            bals_credit_sum=sum_credit_record[0]
            cursor.execute("SELECT SUM(Debit) from id_"+str(bal_find_val)+"_account")
            sum_debit_record=cursor.fetchone()
            bals_debit_sum=sum_debit_record[0]
            cursor.execute("SELECT * from id_"+str(bal_find_val)+"_account ORDER BY TID")
            all_bal_val=cursor.fetchall()
            row_count=2
            if len(all_bal_val)!=0: #check whether ifthe tupls has any value or not
                bals_closing_bal=bals_opening_bal+bals_debit_sum-bals_credit_sum
                lbl1=Label(top8,text="Transaction ID").grid(row=1,column=0,pady=10)
                lbl2=Label(top8,text="Date OF Transaction").grid(row=1,column=1,padx=5,pady=10)
                lbl3=Label(top8,text="Credit").grid(row=1,column=2,pady=10)
                lbl4=Label(top8,text="Debit").grid(row=1,column=3,padx=5,pady=10)
                lbl5=Label(top8,text="Note").grid(row=1,column=4,pady=10)
                for row_bal_val in all_bal_val:    #it is the single tuple field inside the tuple
                    lbl6=Label(top8,text=str(row_bal_val[0]),fg="Blue").grid(row=row_count,column=0,pady=10)
                    lbl7=Label(top8,text=str(row_bal_val[1]),fg="Blue").grid(row=row_count,column=1,padx=5,pady=10)
                    lbl8=Label(top8,text=str(row_bal_val[2]),fg="Brown",font=('calibri',10,'bold')).grid(row=row_count,column=2,pady=10)
                    lbl9=Label(top8,text=str(row_bal_val[3]),fg="Darkolivegreen",font=('calibri',10,'bold')).grid(row=row_count,column=3,padx=5,pady=10)
                    lbl10=Label(top8,text=str(row_bal_val[4]),fg="Blue").grid(row=row_count,column=4,pady=10)
                    row_count+=1
                lbl11=Label(top8,text="OPENING BALANCE : "+str(bals_opening_bal),fg="Darkorange").grid(row=row_count,column=0,columnspan=2)
                lbl12=Label(top8,text="CLOSING BALANCE : "+str(bals_closing_bal),fg="Darkred").grid(row=row_count,column=2,columnspan=3)
                delete_bal_row_but=Button(top8,text="Delete any Row!!",font=("Algerian",12),fg="Blue",command=delete_bal_row)
                delete_bal_row_but.grid(row=(row_count+1),column=0,columnspan=2)
                send_user_but=Button(top8,text="Email Account Holder the Receipt",font=("Algerian",12),fg="Blue",command=send_user)
                send_user_but.grid(row=(row_count+1),column=2,columnspan=3)
            else:
                bals_closing_bal=bals_opening_bal
                lbl14=Label(top8,text="IT HAS NO RECORD!!",fg="Green").grid(row=row_count+2,column=0,columnspan=5)
                lbl11=Label(top8,text="OPENING BALANCE : "+str(bals_opening_bal),fg="Darkorange").grid(row=row_count,column=0,columnspan=2)
                lbl12=Label(top8,text="CLOSING BALANCE : "+str(bals_closing_bal),fg="Darkred").grid(row=row_count,column=2,columnspan=3)
                send_user_but=Button(top8,text="Email Account Holder the Receipt",font=("Algerian",12),fg="Blue",command=send_user)
                send_user_but.grid(row=(row_count+1),column=0,columnspan=5)
        else:
            messagebox.showwarning("Warning","Sorry!This ID dos not exist!")
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()

def delete_bal_row():  #delete any row
    global top9
    global row_tid_no
    top9=Toplevel()
    top9.title("Delete Any Row")
    lbl1=Label(top9,text="Enter the Transaction ID :").grid(row=0,column=0)
    row_tid_no=Entry(top9,fg="Blue")
    row_tid_no.grid(row=0,column=1)
    delete_row_sub_but=Button(top9,text="Submit",command=delete_row_sub)
    delete_row_sub_but.grid(row=1,column=0,columnspan=2)

def delete_row_sub():
    row_tid_val=row_tid_no.get()
    if row_tid_val.isnumeric()== True:  #check if the Transaction ID is number
        try:
            myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
            cursor = myCon.cursor()
            cursor.execute("Select * from id_"+str(bal_find_val)+"_account where TID = "+str(row_tid_val))
            del_row_val=cursor.fetchone()
            if del_row_val is not None: #to check if te row exists or not
                cursor.execute("DELETE from id_"+str(bal_find_val)+"_account where TID = "+str(row_tid_val))
                myCon.commit()
                lbl13=Label(top8,text="Please close the window to review changes!!",fg="Red",font=("Algerian",16)).grid(row=(row_count+2),column=0,columnspan=5)
                top9.destroy()
            else:
                messagebox.showwarning("Warning","Sorry!This Transaction ID does not exist!")
        except Exception as e:
            print("Exception :  {}".format(e))
        finally:
            myCon.close()
    else:
        messagebox.showwarning("Warning","Sorry!It has to be a number!")

def send_user():
    import os
    import smtplib          # imorting tp get values to my email
    from email.message import EmailMessage
    my_email_id=os.environ.get('MY_EMAIL_ID')     #storing my personal data else where to encrypt my data
    my_email_pass=os.environ.get('MY_EMAIL_PASSWORD')
    try:
        myCon = pymysql.connect( host='localhost', user='root', passwd='nipun',database=l1)
        cursor = myCon.cursor()
        cursor.execute("SELECT * from Accounts where ID="+str(bal_find_val))
        send_email_val=cursor.fetchone()
        user_acc_id=send_email_val[0]
        user_acc_name=send_email_val[1]
        user_acc_email=send_email_val[4]
    except Exception as e:
        print("Exception :  {}".format(e))
    finally:
        myCon.close()
        user_email_msg=EmailMessage()
        user_email_msg['Subject']='From the Accountant '+l1
        user_email_msg['To']=user_acc_email
        user_email_msg['From']=my_email_id
        user_email_msg.set_content("Account ID : "+str(user_acc_id)+"\n"+"Account Name : "+user_acc_name+"\n"+"Account Opening Balance : "+str(bals_opening_bal)+"\n"+"Account Closing Balance : "+str(bals_closing_bal))
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(my_email_id,my_email_pass)  #login to my id
            smtp.send_message(user_email_msg)
        messagebox.showinfo("Receipt","Your Receipt has been sent successfully!")

def help_tally():  #help people understand the functions
    top10=Toplevel()
    top10.title("HELP")
    help_str='''1. Create Account button allows you to create an account for which
                   you have to make credit and debit entries to.
                2. Acount Info gives you the information of the neccessary account
                   and allows you to make any changes.
                3. Account Entries allow you to enter the desired values to credit
                   from or debit into account.
                4. Balance sheet allows you to view entries made in the desired
                   acount and delete any rows.
                5. Feedback allows you to give your insightful opinion to change and
                   make the interface better.
                6. Exit allows you to quit the program'''
    lbl1=Label(top10,text=help_str,fg="Green",font=('Comic Sans MS',14)).grid(row=0,column=0,sticky=W)
    lbl2=Label(top10,text="NOTE: Click any button only once to make the program work efficiently!!",fg="Red",font=('Algerian',15)).grid(row=1,column=0)
    lbl3=Label(top10,text="THANK YOU!!",fg="Gold",font=('Algerian',16)).grid(row=2,column=0)

def feedback():
    global top11
    global rate_val
    global fdbck_entry
    top11=Toplevel()
    top11.title("FEEDBACK")
    exp_lbl=Label(top11,text="HOW IS YOUR EXPERIENCE?").pack(anchor=W)
    rate_list=[("BAD","Bad"),("GOOD","good"),("VERY GOOD","Very Good")] #don't have to call radio button again
    rate_val = StringVar()
    rate_val.set("")
    for rate,rate_inp in rate_list:
        Radiobutton(top11, text=rate, variable=rate_val, value=rate_inp, fg="Blue").pack(anchor=W)
    fdbck_entry=Entry(top11,fg="Blue",width=200)
    fdbck_entry.pack(pady=10)
    fdbck_entry.insert(0,"PLEASE GIVE YOUR VALUABLE SUGGESTION")
    fdbck_submit_but=Button(top11,text="SUBMIT",command=fdbck_submit)
    fdbck_submit_but.pack(padx=150,anchor=W)

def fdbck_submit():
    import os
    import smtplib          # imorting tp get values to my email
    from email.message import EmailMessage
    fdbck_msg_val=fdbck_entry.get()
    my_email_id=os.environ.get('MY_EMAIL_ID')     #storing my personal data else where to encrypt my data
    my_email_pass=os.environ.get('MY_EMAIL_PASSWORD')
    fdbck_msg=EmailMessage()
    fdbck_msg['Subject'] = "From the user "+l1    #content of the email
    fdbck_msg['From']=my_email_id
    fdbck_msg['To']=my_email_id
    fdbck_msg.set_content("Rating App got was : "+rate_val.get()+"\n"+"The Feedback was : "+fdbck_msg_val)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(my_email_id,my_email_pass)  #login to my id
        smtp.send_message(fdbck_msg)
    messagebox.showinfo("Successful","Thanks for providing us with your feedback!")
    top11.destroy()

log_in = Button(lsin_frame, text="LOG IN",padx=52,pady=10,bg = "light blue",command=log)
log_in.grid(row=1,column=0)  #log in button in main window

sign_in = Button(lsin_frame, text="SIGN IN",padx=52,pady=10,bg = "light blue",command=sign)
sign_in.grid(row=1,column=1) #sign in button in the main window



master.mainloop()   #so that loop runs infinitely and changes are read automatically
