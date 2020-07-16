# ALL THE IMPORTS

# IMPORT FOR GUI
import tkinter as tk
from tkinter import messagebox

# IMPORT FOR SENDING MAIL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# IMPORT FOR DISPLAYING DATE
import datetime as dt

#IMPORT FOR CONNECTION DATABASE
import sqlite3

# MAKING THE CONNECTION TO DATABASE
conn=sqlite3.connect('mail.sqlite')
cur=conn.cursor()
try:
    cur.execute('CREATE TABLE email (date TEXT, sender TEXT, subject TEXT, message TEXT)')
except:
    cur.execute('SELECT * FROM email')

# GLOBAL VARIABLES
date = dt.datetime.now()
format_date = f"{date:%a, %b %d %Y}"


# CREATING GUI USING TKINTER

root=tk.Tk()
root.geometry('500x640')
root.title('EMAIL SENDER')

# DISPLAYING HEADING
Label_0=tk.Label(root, text="YOUR MAIL ACCOUNT", width=20, fg="green", font=("bold",15), relief="solid")
Label_0.place(x=150,y=33)

# DISPLAYING DATE
w=tk.Label(root, text=format_date, fg="black", bg="white", width="14")
w.place(x=0,y=0)

# DISPLAYING TEXT-Your Email Account
Label_1=tk.Label(root, text="Your Email Account", width=20, font=("bold",10))
Label_1.place(x=40,y=110)

# DISPLAYING ENRTY BOX
emailE=tk.Entry(root, width=40)
emailE.place(x=200, y=110)

# DISPLAYING TEXT-Your Email Account
Label_2=tk.Label(root, text="Your Password", width=20, font=("bold",10))
Label_2.place(x=40,y=160)

# DISPLAYING ENRTY BOX
passwordE=tk.Entry(root, width=40,show="*")
passwordE.place(x=200, y=160)

# DISPLAYING  SECOND HEADING
compose=tk.Label(root, text="COMPOSE YOUR MAIL", width=20, fg="green", font=("bold",15), relief="solid")
compose.place(x=150,y=210)

# DISPLAYING TEXT-Send To Email
Label_3=tk.Label(root, text="Send To Email", width=20, font=("bold",10))
Label_3.place(x=40,y=260)

# DISPLAYING ENRTY BOX
senderE=tk.Entry(root, width=40)
senderE.place(x=200, y=260)

# DISPLAYING TEXTS-Subject
Label_4=tk.Label(root, text="Subject", width=20, font=("bold",10))
Label_4.place(x=40,y=310)

# DISPLAYING ENRTY BOX
subjectE=tk.Entry(root, width=40)
subjectE.place(x=200, y=310)

# DISPLAYING TEXT-Message
Label_5=tk.Label(root, text="Message", width=20, font=("bold",10))
Label_5.place(x=40,y=360)

# DISPLAYING MESSAGE BOX
msgbodyE=tk.Text(root, width=30, height=10)
msgbodyE.place(x=200, y=360)

# FUNCTION TO SEND MAIL
def sendemail():
    isubmit = tk.messagebox.askyesno("Confirm","Are you sure to submit?") # TO DISPLAY CONFIRM BOX
    if isubmit > 0:
        try:
            mymsg=MIMEMultipart()
            mymsg['From']=emailE.get()
            mymsg['To']=senderE.get()
            mymsg['Subject']=subjectE.get()

            mymsg.attach(MIMEText(msgbodyE.get(1.0,'end'), 'plain'))

            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(emailE.get(), passwordE.get())
            text=mymsg.as_string()
            server.sendmail(emailE.get(), senderE.get(), text)

            Label_6 = tk.Label(root, text="Done!", width=20, fg='green', font=("bold", 15))
            Label_6.place(x=140, y=550)

            cur.execute('''INSERT OR IGNORE INTO email (date, sender, subject, message)
                VALUES ( ?, ?, ?, ? )''', ( format_date, emailE.get(), subjectE.get(), msgbodyE.get(1.0,'end'), ) )
            conn.commit()

            server.quit()

        except:
            Label_6 = tk.Label(root, text="something went wrong!", width=20, fg='red', font=("bold", 15))
            Label_6.place(x=140, y=550)

# FUNCTION TO QUIT THE APP
def quit_mail():
    iExit = tk.messagebox.askyesno("Confirm","Are you sure to exit?") # TO DISPLAY CONFIRM BOX
    if iExit > 0:
        exit()


# DISPLAYING SEND BUTTON
tk.Button(root,text="Send", width=14, bg='green',fg="white", command=sendemail).place(x=100, y=590)

# DISPLAYING QUIT BUTTON
tk.Button(root,text="Quit", width=14, bg='brown',fg="white", command=quit_mail).place(x=250, y=590)

root.mainloop()
