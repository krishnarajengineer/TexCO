import email
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
import os
import re
import subprocess
import sqlite3
import email_pass
import smtplib
import time


def valid_email(email):
        if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
         return True
        return False

def valid_gst(gst_number):

    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    if re.match(pattern, gst_number):
        return True
    else:
        return False

class Registration:

    def __init__(self,root):
        #---------------- New Window-------------
        self.root=root
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("TexCO")
        # ---------------------------------------
        self.label1 = Label(self.root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/registration_page.png")
        self.label1.configure(image=self.img)
        # -----------------------------------------
        self.var_email=StringVar()
        self.var_cname=StringVar()
        self.var_category=StringVar()
        self.var_state=StringVar()
        self.var_gst=StringVar()
        self.var_mob=StringVar()
        self.var_address=StringVar()
        self.var_pincode=StringVar()

        
        # =====>COLUMN 1<========


        self.cname = Entry(self.root)
        self.cname.place(x=383.5, y=232, width=305, height=24)
        self.cname.configure(
            font=("Segoe UI", 12),
            relief="flat",
            textvariable=self.var_cname
        )
        self.cname.focus_set()
        self.email = Entry(self.root)
        self.email.place(x=383.5, y=300, width=305, height=24)
        self.email.configure(
            font=("Segoe UI", 12),
            relief="flat",         
            textvariable=self.var_email
        )

        cat = ["Manufacturer","Trader"]
        self.combo1 = ttk.Combobox(self.root,textvariable=self.var_category)
        self.combo1.place(x=383.5, y=373, width=305, height=24)
        self.combo1.configure(
            values=cat,
            font=("Segoe UI", 12),
        )
        self.state = Entry(self.root)
        self.state.place(x=383.5, y=436, width=305, height=24)
        self.state.configure(
            font=("Segoe UI", 12),
            relief="flat",
            textvariable=self.var_state
            
            
        )
        # ==================>COLUMN 2===============<========

        self.gst = Entry(self.root)
        self.gst.place(x=861, y=232, width=305, height=24)
        self.gst.configure(
            font=("Segoe UI", 12),
            relief="flat",textvariable=self.var_gst
        )

        self.mob = Entry(self.root)
        self.mob.place(x=861, y=300, width=305, height=24)
        self.mob.configure(
            font=("Segoe UI", 12),
            relief="flat",textvariable=self.var_mob
        )

        self.address = Entry(self.root)
        self.address.place(x=861, y=368, width=305, height=24)
        self.address.configure(
            font=("Segoe UI", 12),
            relief="flat",textvariable=self.var_address
        )
        self.pincode = Entry(self.root)
        self.pincode.place(x=861, y=436, width=305, height=24)
        self.pincode.configure(
            font=("Segoe UI", 12),
            relief="flat",textvariable=self.var_pincode
            
        )

        self.register = Button(self.root)
        self.register.place(x=614,y=555,width=138, height=48)
        self.register.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font=("Segoe UI", 18, "bold"),
            bd=0,
            text="Register",
            command=self.add
        )

#=======================FUNCTIONS=============
    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False
    
    
    def testchar(self, val):
            if val.isalpha():
                return True
            elif val == "":
                return True
            return False
    

    def add(self):
    # Connect to the SQLite database
        con = sqlite3.connect(database=r'TexCO.db')
        cur = con.cursor()

        # Here you would fetch data from your Entry fields and Combobox
        cname = self.var_cname.get()
        emailid = self.var_email.get()
        category = self.var_category.get()  # Fetch the selected category from the Combobox
        state = self.var_state.get()
        gst = self.var_gst.get()
        mob = self.var_mob.get()
        address = self.var_address.get()
        pincode = self.var_pincode.get()

        # Once you have retrieved the data, you can insert it into your database
        try:

            if cname.strip():
                if valid_email(emailid):
                    if category:
                        if state:
                            if valid_gst(gst):
                                if mob:
                                    if address:
                                        if pincode:
                                            cur.execute("INSERT INTO Register (company_name, email, category, state, GSTIN, mobile, address, pincode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                            (cname, emailid, category, state, gst, mob, address, pincode))
            
                                            # Commit the changes and close the connection
                                            con.commit()
                                            con.close()
                                            messagebox.showinfo("Success!!", "Registration Successfull", parent=self.root)
                                            
                                            # messagebox.showinfo("Success", "Registration Successful")
                                        else:
                                            messagebox.showerror("Oops!", "Please Pincode", parent=self.root)
                                    else:
                                        messagebox.showerror("Oops!", "Please enter address.", parent=self.root)
                                else:
                                    messagebox.showerror("Oops!", "Please mobile number", parent=self.root)
                            else:
                                messagebox.showerror("Oops!", "Invalid GST number.", parent=self.root)
                        else:
                            messagebox.showerror("Oops!", "Please enter state", parent=self.root)
                    else:
                        messagebox.showerror("Oops!", "Please enter category", parent=self.root)
                else:
                    messagebox.showerror("Oops!", "Invalid Email Id.", parent=self.root)
            else:
                messagebox.showerror("Oops!", "Please enter company name.", parent=self.root)

        except Exception as ex:
               messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


   


if __name__=="__main__":
    root=Tk()
    obj=Registration(root)
    root.mainloop() 