from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

# planetscale sql
from dotenv import load_dotenv
load_dotenv()

import os
import MySQLdb
import uuid
import subprocess
import pygame

# testing
ssl_cert_path = os.getenv("SSL_CERT")

if os.path.exists(ssl_cert_path):
    print(f"The file exists at: {ssl_cert_path}")
else:
    print(f"The file does NOT exist at: {ssl_cert_path}")
print(os.getenv("USERNAME"))
print(os.getenv("PASSWORD"))


def login_page():
    signup_window.destroy()
    subprocess.run(['python', 'userlogin.py'])



def connect_database():
    # Check if fields are empty
    if email_entry.get() == '' or username_entry.get() == '' or password_entry.get() == '' or confirmpassword_entry.get() == '':
        messagebox.showerror('Error', 'All Fields are Required')
        return

    # Check if password matches confirm password
    elif password_entry.get() != confirmpassword_entry.get():
        messagebox.showerror('Error', 'Password Mismatch')
        return

    # Connect to the database
    db = MySQLdb.connect(
        host=os.getenv("HOST"),
        user=os.getenv("DB_USERNAME"),
        passwd=os.getenv("PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        # ssl={
        #     # for mac
        #     "ca": "/etc/ssl/cert.pem"
        # }
        ssl={
            "ca": os.getenv("SSL_CERT")
        }

    )
    cur = db.cursor()

    try:
        # Insert the user data into the registration table
        query = 'INSERT INTO registration(id, username, email, password) VALUES (%s,%s,%s,%s)'
        unique_id = str(uuid.uuid4())
        cur.execute(query, (unique_id, username_entry.get(), email_entry.get(), password_entry.get()))
        db.commit()
        messagebox.showinfo('Successful', 'Successful Registration')
    except Exception as e:
        # Handle any database errors
        messagebox.showerror('Error', str(e))
    finally:
        db.close()

    login_page()


signup_window = Tk()
# signup_window.configure(bg='brown2')
signup_window.geometry('1000x750')
bgImage = ImageTk.PhotoImage(file='login_img/myimage_1000.jpg')

bgLabel = Label(signup_window, image=bgImage)
bgLabel.grid()

create_acclabel = Label(signup_window, text='CREATE AN ACCOUNT', fg='black', font=('Franklin Gothic Demi', 45))
create_acclabel.place(x=280, y=30)

emaillabel = Label(signup_window, text='Email : ', font=('Franklin Gothic Demi', 20), fg='black')
emaillabel.place(x=50, y=210)

usernamelabel = Label(signup_window, text='Username : ', font=('Franklin Gothic Demi', 20), fg='black')
usernamelabel.place(x=50, y=140)

passwordlabel = Label(signup_window, text='Password : ', font=('Franklin Gothic Demi', 20), fg='black')
passwordlabel.place(x=50, y=280)

confirmpasswordlabel = Label(signup_window, text='Confirm Password :', font=('Franklin Gothic Demi', 20), fg='black')
confirmpasswordlabel.place(x=50, y=350)

username_entry = Entry(signup_window, font=('Franklin Gothic Demi', 20), bg='floralwhite', fg='black')
username_entry.place(x=200, y=140)

email_entry = Entry(signup_window, font=('Franklin Gothic Demi', 20), bg='floralwhite', fg='black')
email_entry.place(x=150, y=210)

password_entry = Entry(signup_window, font=('Franklin Gothic Demi', 20), bg='floralwhite', fg='black', show='.')
password_entry.place(x=200, y=280)

confirmpassword_entry = Entry(signup_window, font=('Franklin Gothic Demi', 20), bg='floralwhite', fg='black', show='.')
confirmpassword_entry.place(x=290, y=350)

Signupbutton = Button(signup_window, text='Create Account', bg='floralwhite', font=('Franklin Gothic Demi', 20), bd=10,
                      command=connect_database)
Signupbutton.place(x=50, y=570)

alreadyhaveaccountlabel = Label(signup_window, text='Already have an account?  ', font=('Franklin Gothic Demi', '13'),
                                fg='black')
alreadyhaveaccountlabel.place(x=50, y=500)

loginbutton = Button(signup_window, text='LOGIN', bg='floralwhite', font=('Franklin Gothic Demi', 10),
                     command=login_page)
loginbutton.place(x=255, y=500)

signup_window.mainloop()
