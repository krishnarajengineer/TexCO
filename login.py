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
from register import Registration
from dashboard import Dashboard
class Login:

    def __init__(self,root):
        
        #---------------- New Window-------------
        self.root=root
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("TexCO")
        # ---------------------------------------
        self.var_email=StringVar()
        self.var_password=StringVar()
        
        self.label1 = Label(self.root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/login_page.png")
        self.label1.configure(image=self.img)


        self.email = Entry(self.root)
        self.email.place(x=540, y=288, width=300, height=24)
        self.email.configure(
            font=("Segoe UI", 12),
            relief="flat",
            textvariable=self.var_email
        )
        self.email.focus_set()
        self.password = Entry(root)
        self.password.place(x=540, y=428, width=300, height=24)
        self.password.configure(
            font=("Segoe UI", 20),
            relief="flat",
            show="*",
            textvariable=self.var_password
        )
        self.login = Button(self.root)
        self.login.place(x=628,y=535,width=111, height=36)
        self.login.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font=("Segoe UI", 18, "bold"),
            bd=0,
            text="Login",
            command=self.validate_otp
        )
        self.sendotp = Button(self.root)
        self.sendotp.place(x=626,y=330,width=112, height=36)
        self.sendotp.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#ffffff",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font=("Segoe UI", 18, "bold"),
            bd=0,
            text="Send OTP",
            command=self.login_process
        )
        btn_register=Button(self.root,command=self.register,text="New User?Click Here",font=("Segoe UI",12,"bold"),bg="white",fg="#325096",cursor="hand2",activeforeground="#D2463E",bd=0,activebackground="white").place(x=506,y=496)
    
    
    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subj='TexCO Password OTP'
        msg=f'Dear Sir/Madam \n\n Your Login OTP is {str(self.otp)}.\n\n With Regards,\nTexCO '
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
        
    def login_process(self):
        con = sqlite3.connect(database=r'TexCO.db')
        cur = con.cursor()
        try:
            if not self.var_email.get():
                messagebox.showerror("Error", "Enter Email ID", parent=self.root)
            else:
                cur.execute("select email from Register where email=?",(self.var_email.get(),))
                email=cur.fetchone() 
                if email is not None and email[0]== self.var_email.get():
                    # # messagebox.showinfo("Success","Email Available")

                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,Try again",parent=self.root)   
                    else:
                        messagebox.showinfo("Success","OTP Sent to Email")
                        print(self.var_email.get())
                else:
                    messagebox.showerror("Error","Invalid EmailID",parent=self.root)
                        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def getemail(self):
        self.email=self.var_email.get().strip()
        return self.email
        
    def register(self):
        try:
            self.root.withdraw()
            self.new_win=Toplevel(self.root)
            self.new_obj=Registration(self.new_win)

        except subprocess.CalledProcessError as e:
            print("An error occurred while executing register.py:", e)
        except Exception as e:
            print("An exception occured:",e)



    def validate_otp(self): 
        if int(self.otp)==int(self.var_password.get()):
            messagebox.showinfo("Success","Login Successfull")
            dashboard = Dashboard(root, self.var_email.get().strip())
            

        else:
            messagebox.showerror("Error","Invalid OTP,Try Again",parent=self.root)



















if __name__=="__main__":
    root=Tk()
    obj=Login(root)
    root.mainloop() 