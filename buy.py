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
from tkinter import simpledialog

from time import strftime

class Buy:

    def __init__(self,root,email):
        #---------------- New Window-------------
        self.root=root
        self.email =email
        self.email = 'madhumithasareesjkpm@gmail.com'
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("TexCO")
        # ---------------------------------------
        self.label1 = Label(self.root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/inventory.png")
        self.label1.configure(image=self.img)

        self.message = Label(self.root)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(
            font="-family {Poppins} -size 10",
            foreground="#000000",
            background="#ffffff",
            text="ADMIN",
            anchor="w"
        )

        self.clock = Label(self.root)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(
            font="-family {Poppins Light} -size 12",
            foreground="#000000",
            background="#ffffff",
            text="HH-MM-SS"
        )

        self.entry1 = Entry(self.root)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        self.button1 = Button(self.root)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 10",
            borderwidth="0",
            text="Search",
            command=self.search_product
        )

        self.button2 = Button(self.root)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 10",
            borderwidth="0",
            text="Logout",
            command=self.logout
        )

        self.button6 = Button(self.root)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 10",
            borderwidth="0",
            text="EXIT",
            command=self.Exit
        )
        self.button7 = Button(self.root)
        self.button7.place( width=100, height=40,x=1100,y=80)
        self.button7.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 10",
            borderwidth="0",
            text="Refresh",
            command=self.refresh
        )
        self.order_button = Button(self.root)
        self.order_button.place(relx=0.130, rely=0.350, width=100, height=40)
        self.order_button.configure(
            relief="flat",
            overrelief="flat",
            activebackground="#325096",
            cursor="hand2",
            foreground="#ffffff",
            background="#325096",
            font="-family {Poppins SemiBold} -size 10",
            borderwidth="0",
            text="Make Order",
            command=self.make_order
        )
        
        self.scrollbarx = Scrollbar(self.root, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.root, orient=VERTICAL)
        self.tree = ttk.Treeview(self.root)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Product ID",
                "Product Name",
                "Quantity",
                "Price",
                "Category",
                "MOQ",
                "Vendor Name"
                
            )
        )

        self.tree.heading("Product ID", text="Product ID", anchor=W)
        self.tree.heading("Product Name", text="Product Name", anchor=W)
        self.tree.heading("Price", text="Price", anchor=W)
        self.tree.heading("Category", text="Category", anchor=W)
        self.tree.heading("Quantity", text="Quantity", anchor=W)
        self.tree.heading("MOQ", text="MOQ", anchor=W)
        self.tree.heading("Vendor Name", text="Vendor Name", anchor=W)
        

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=100)
        self.tree.column("#2", stretch=NO, minwidth=0, width=100)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=100)
        self.tree.column("#5", stretch=NO, minwidth=0, width=100)
        
        self.show()
        self.update_time()

    def show(self):
        con=sqlite3.connect(database=r'TexCO.db')
        cur=con.cursor()

        try:
            cur.execute("select * from products")
            rows=cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
               self.tree.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root) 
    
    
    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False
    
    def make_order(self):
        try:
            con = sqlite3.connect(database=r'TexCO.db')
            cur = con.cursor()
            for item in self.sel:
                values = self.tree.item(item)['values']
                product_id = values[0]
                product_name = values[1]
                price = values[3]
                category = values[4]
                moq = values[5]
                vendor_name = values[6]
                cur.execute("SELECT quantity FROM products WHERE pid = ?", (product_id,))
                available_quantity = cur.fetchone()[0]
                
                quantity = simpledialog.askinteger("Enter Quantity", f"Enter quantity for {product_name}:", parent=self.root)
                if quantity is None:
                    continue  
                if quantity > available_quantity:
                    messagebox.showerror("Error", f"Quantity entered exceeds available quantity for {product_name}. Available quantity: {available_quantity}", parent=self.root)
                    continue
                
                order_data = (product_id, product_name, quantity, price, category, moq, vendor_name)
                cid = cur.execute("SELECT cid FROM Register WHERE email = ?", (self.email,)).fetchone()[0]

                cur.execute('''INSERT INTO orders 
                    (product_id, product_name, quantity, price, category, moq, vendor_name, customer_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', order_data + (cid,))

                con.commit()
                con.close()
                messagebox.showinfo("Success", "Order placed successfully!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)  


    def testchar(self, val):
            if val.isalpha():
                return True
            elif val == "":
                return True
            return False
        
    sel = []
    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def refresh(self):
        self.show()
    
    
    def search_product(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=self.root)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", f"Product ID: {self.entry1.get()} found.", parent=self.root)
                    break
            else:
                messagebox.showerror("Oops!!", f"Product ID: {self.entry1.get()} not found.", parent=self.root)

    def update_time(self):
        string = strftime("%I:%M:%S")
        self.clock.config(text=f'{str(string)}')
        self.clock.after(1, self.update_time)

    def Exit(self):
        sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=self.root)
        if sure == True:
            self.root.destroy()

    def logout(self):
        sure = messagebox.askyesno("Exit","Are you sure you want to logout?", parent=self.root)
        if sure == True:
            self.root.destroy()
            os.system("python login1.py")



if __name__=="__main__":
    root=Tk()
    obj=Buy(root,email)
    root.mainloop() 