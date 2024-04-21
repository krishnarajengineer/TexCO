import email
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import os
import subprocess
import sqlite3
import email_pass
from tkinter import ttk
import smtplib
import time
from time import strftime

class Sell:

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
        self.img = PhotoImage(file="./images/sell.png")
        self.label1.configure(image=self.img)
        
        self.entry1 = Entry(self.root)
        self.entry1.place(x=127,y=200, width=996, height=30)
        self.entry1.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )
        self.entry3 = Entry(self.root)
        self.entry3.place(x=683,y=200, width=996, height=30)
        self.entry3.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        self.entry2 = Entry(self.root)
        self.entry2.place(x=127,y=346, width=996, height=30)
        self.entry2.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        self.entry4 = Entry(self.root)
        self.entry4.place(x=683,y=346, width=996, height=30)
        self.entry4.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        self.entry5 = Entry(self.root)
        self.entry5.place(x=457,y=500, width=996, height=30)
        self.entry5.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )
        
        self.button1 = Button(self.root)
        self.button1.place(relx=0.450, rely=0.750, width=96, height=34)
        self.button1.configure(
            relief="flat",
            overrelief="flat",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 14",
            borderwidth="0",
            text="SUBMIT",
            command=self.add_to_db
        )
    def clear(self):

        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')
        self.entry3.delete(0, 'end')
        self.entry4.delete(0, 'end')
        self.entry5.delete(0, 'end')    
        

    def add_to_db(self):
        pname = self.entry1.get()
        qty = self.entry2.get()
        price = self.entry3.get()
        cat = self.entry4.get()
        moq = self.entry5.get()

        if pname.strip() and qty.strip() and price.strip() and cat.strip() and moq.strip():
            try:
                conn = sqlite3.connect('TeXCO.db')
                c = conn.cursor()
                cid = c.execute("Select cid from Register where email=? ", (self.email,)).fetchone()[0]
                cname = c.execute("Select company_name from Register where email=? ", (self.email,)).fetchone()[0]
                c.execute("INSERT INTO products (product_name, quantity, price, category, moq,cid,cname) VALUES (?, ?, ?, ?, ?,?,?)",
                        (pname, qty, price, cat, moq,cid,cname))
                conn.commit()
                messagebox.showinfo("Success!!", "Product successfully listed in the buy page you can check your orders if any in the dashboard .", parent=self.root)
                self.root.destroy()
                conn.close()

            except Exception as e:
                print("An exception occured:",e)
        else:
            if not pname.strip():
                print("Product name field is empty.")
            elif not qty.strip():
                print("Quantity field is empty.")
            elif not price.strip():
                print("Price field is empty.")
            elif not cat.strip():
                print("Category field is empty.")
            elif not moq.strip():
                print("Minimum order quantity field is empty.")

           



if __name__=="__main__":
    root=Tk()
    obj=Sell(root,email)
    root.mainloop() 