import pygame
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
import os
#import pymysql
from tkinter import PhotoImage

import subprocess

import MySQLdb
from dotenv import load_dotenv
load_dotenv()

# Assuming you've already loaded environment variables for your database connection using `dotenv`
# You can also hardcode the values here but using environment variables is safer

import subprocess

def signup_page():
    login_window.destroy()
    subprocess.run(['python', 'signuppage.py'])


def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror('Login Error', 'Blanks are not allowed')
        return

    db = None

    # Connect to the database
    try:
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

        # Query the database to get the password for the given username
        cur.execute("SELECT password FROM registration WHERE username = %s", (username,))
        result = cur.fetchone()

        # If the username exists and the password matches
        if result and result[0] == password:
            cur.execute("SELECT id FROM registration WHERE username = %s", (username,))
            user_id = cur.fetchone()[0]
            login_window.destroy()
            run_geomap(user_id)
        else:
            messagebox.showerror('Login Error', 'Incorrect Username and Password')

    except Exception as e:
        messagebox.showerror('Error', 'Database error: ' + str(e))
    finally:
        if db:
            db.close()




def run_geomap(user_id):
    # os.system("python geomap.py")
    # subprocess.run(['python', 'geomap.py'])

    # Pass the user id to geomap.py
    subprocess.run(['python', 'choice.py', str(user_id)])


login_window = Tk()
login_window.geometry('1000x750')
#login_window.configure(bg='brown2')

bgImage = ImageTk.PhotoImage(file ='login_img/myimage_1000.jpg')

# bgLabel =Label(login_window, image=bgImage)
# bgLabel.grid()

canvas = Canvas(login_window, width=1000, height=750)
canvas.pack()

canvas.create_image(0, 0, anchor="nw", image=bgImage)

global username_entry
global password_entry
global confirmpassword_entry


# Create text directly on the canvas
canvas.create_text(500, 70, text='WORLD WANDERER', fill='black', font=('Franklin Gothic Demi', 60))
canvas.create_text(680, 130, text='ADVENTURE AWAITS THOSE WHO DARE TO EXPLORE THE UNKNOWN', fill='black', font=('Franklin Gothic Demi', 12))

usernamelabel = Label(login_window, text ='Username : ', font=('Franklin Gothic Demi',20),  fg='black')
usernamelabel.place(x =50 , y =250)

passwordlabel = Label(login_window, text ='Password : ', font=('Franklin Gothic Demi',20), fg='black')
passwordlabel.place(x =50 , y =350)


username_entry = Entry(login_window , font =('Franklin Gothic Demi',20),bg ='floralwhite', fg='black')
username_entry.place(x =200 , y =250)

password_entry = Entry(login_window , font =('Franklin Gothic Demi',20),bg ='floralwhite', fg='black',show='.')
password_entry.place(x =195 , y =350)


EmbarkOnJourneyButton = Button(login_window, text='Embark On The Journey!', bg='floralwhite',font =('Franklin Gothic Demi',12),bd=10 , command = login)
EmbarkOnJourneyButton.place(x=110,y =650)

Signupbutton = Button(login_window, text='No Account? Signup here!', bg='floralwhite',font =('Franklin Gothic Demi',12),bd=10,command= signup_page )
Signupbutton.place(x=110,y =550)




login_window.mainloop()