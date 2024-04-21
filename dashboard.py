import email
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import os
import subprocess
import sqlite3
import email_pass
import smtplib
import time
from sell import Sell
from buy import Buy

class Dashboard:

    def __init__(self,root,email):
        #---------------- New Window-------------
        self.root=root
        self.email = email
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("TexCO")
        # ---------------------------------------
        self.label1 = Label(self.root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="images/dashboard.png")
        self.label1.configure(image=self.img)

        self.button1 = Button(self.root)
        self.button1.place(x=15,y=70, width=100, height=23)
        self.button1.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 12",
            borderwidth="0",
            text="Logout",
            command=self.logout
        )
        
        self.button2 = Button(self.root)
        self.button2.place(relx=0.14, rely=0.508, width=146, height=63)
        self.button2.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#333333",
            background="#ffffff",
            font="-family {Poppins SemiBold} -size 12",
            borderwidth="0",
            text="Buy",
            command=self.buy
        )

        self.button3 = Button(self.root)
        self.button3.place(relx=0.338, rely=0.508, width=146, height=63)
        self.button3.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#333333",
            background="#ffffff",
            font="-family {Poppins SemiBold} -size 12",
            borderwidth="0",
            text="Sell",
            command=self.sell
        )


        self.button4 = Button(self.root)
        self.button4.place(relx=0.536, rely=0.508, width=146, height=63)
        self.button4.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#333333",
            background="#ffffff",
            font="-family {Poppins SemiBold} -size 12",
            borderwidth="0",
            text="Market News"
        )
        self.button5 = Button(self.root)
        self.button5.place(relx=0.732, rely=0.508, width=146, height=63)
        self.button5.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#333333",
            background="#ffffff",
            font="-family {Poppins SemiBold} -size 12",
            borderwidth="0",
            text="Orders"
        )
        print(self.email)

    def sell(self):
        try:
            sell = Sell(self.root,self.email)
        except subprocess.CalledProcessError as e:
            print("An error occurred while executing sell.py:", e)
        except Exception as e:
            print("An exception occured:",e)
    def buy(self):
        try:
            buy = Buy(self.root,self.email)
        except subprocess.CalledProcessError as e:
            print("An error occurred while executing buy.py:", e)
        except Exception as e:
            print("An exception occured:",e)
    

    def logout(self):
        sure = messagebox.askyesno("Exit","Are you sure you want to logout?", parent=self.root)
        if sure == True:
            self.root.withdraw()
            self.root.quit()  
            os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = Dashboard(root,email)
    root.mainloop()