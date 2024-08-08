# Account Number : 10 ------------ Password : trial
from tkinter import *
from tkinter import messagebox
import sqlite3

ARIAL = ("arial", 10, "bold")


class Bank:
    def __init__(self, root):
        self.conn = sqlite3.connect("atm_databse.db", timeout=100)
        self.login = False
        self.root = root
        self.header = Label(self.root, text="B~K BANK", bg="dark blue", fg="white", font=("arial", 20, "bold"))
        self.header.pack(fill=X)
        self.frame = Frame(self.root, bg="white", width=600, height=400)
        # Login Page Form Components

        self.userlabel = Label(self.frame, text="Account Number", bg="pink", font=ARIAL)
        self.uentry = Entry(self.frame, width=30, bg="light green")
        self.plabel = Label(self.frame, text="Password", bg="pink", font=ARIAL)
        self.pentry = Entry(self.frame, show="*", bg="light green")
        self.button = Button(self.frame, text="LOGIN", bg="yellow", font=ARIAL, command=self.verify)
        self.q = Button(self.frame, text="Quit", bg="pink", font=ARIAL, command=self.root.destroy)
        self.frame.config(bg="cyan")
        self.userlabel.place(x=145, y=100, width=120, height=20)
        self.uentry.place(x=153, y=130, width=200, height=20)
        self.plabel.place(x=145, y=160, width=120, height=20)
        self.pentry.place(x=153, y=190, width=200, height=20)
        self.button.place(x=155, y=230, width=120, height=20)
        self.q.place(x=480, y=360, width=120, height=20)
        self.frame.pack()

    def database_fetch(self):
        # Fetching Account data from database
        self.acc_list = []
        self.temp = self.conn.execute("select name,pass,acc_no,acc_type,bal from atm where acc_no = ? ", (self.ac,))
        for i in self.temp:
            self.acc_list.append("Name = {}".format(i[0]))
            self.acc_list.append("Account no = {}".format(i[2]))
            self.acc_list.append("Account type = {}".format(i[3]))
            self.ac = i[2]
            self.acc_list.append("Balance = {}".format(i[4]))

    def verify(self):
        # verifying of authorised user
        ac = False
        self.temp = self.conn.execute("select name,pass,acc_no,acc_type,bal from atm where acc_no = ? ",
                                      (int(self.uentry.get()),))
        for i in self.temp:
            self.ac = i[2]
            if i[2] == self.uentry.get():
                ac = True
            elif i[1] == self.pentry.get():
                ac = True
                m = "{} Login SucessFull".format(i[0])
                self.database_fetch()
                messagebox._show("Login Info", m)
                self.frame.destroy()
                self.MainMenu()
            else:
                ac = True
                m = " Login UnSucessFull ! Wrong Password"
                messagebox._show("Login Info!", m)
        if not ac:
            m = " Wrong Acoount Number !"
            messagebox._show("Login Info!", m)

    def MainMenu(self):
        # Main App Appears after logined !
        self.frame = Frame(self.root, bg="white", width=800, height=400)
        root.geometry("800x400")
        self.frame.config(bg="cyan")
        self.detail = Button(self.frame, text="Account Details", bg="blue", font=ARIAL, command=self.account_detail)
        self.enquiry = Button(self.frame, text="Balance Enquiry", bg="pink", font=ARIAL, command=self.Balance)
        self.deposit = Button(self.frame, text="Deposit Money", bg="pink", font=ARIAL, command=self.deposit_money)
        self.withdrawl = Button(self.frame, text="Withdrawl Money", bg="pink", font=ARIAL, command=self.withdrawl_money)
        self.q = Button(self.frame, text="Quit", bg="yellow", font=ARIAL, command=self.root.destroy)
        self.detail.place(x=50, y=50, width=200, height=50)
        self.enquiry.place(x=50, y=200, width=200, height=50)
        self.deposit.place(x=500, y=50, width=200, height=50)
        self.withdrawl.place(x=500, y=200, width=200, height=50)
        self.q.place(x=340, y=340, width=120, height=20)
        self.frame.pack()

    def account_detail(self):
        self.database_fetch()
        text = self.acc_list[0] + "\n" + self.acc_list[1] + "\n" + self.acc_list[2]
        self.label = Label(self.frame, text=text, font=ARIAL)
        self.label.place(x=200, y=100, width=300, height=100)

    def Balance(self):
        self.database_fetch()
        self.label = Label(self.frame, text=self.acc_list[3], font=ARIAL)
        self.label.place(x=200, y=100, width=300, height=100)

    def deposit_money(self):
        self.money_box = Entry(self.frame, width=20)
        self.submitButton = Button(self.frame, text="Submit", bg="lightyellow", font=ARIAL)
        self.money_box.place(x=200, y=100, width=200, height=20)
        self.submitButton.place(x=445, y=100, width=55, height=20)
        self.submitButton.bind("<Button-1>", self.deposit_trans)

    def deposit_trans(self, flag):
        self.label = Label(self.frame, text="Transaction Completed !", font=ARIAL)
        self.label.place(x=200, y=100, width=300, height=100)
        self.conn.execute("update atm set bal = bal + ? where acc_no = ?", (self.money_box.get(), self.ac))
        self.conn.commit()

    def withdrawl_money(self):
        self.money_box = Entry(self.frame, width=20)
        self.submitButton = Button(self.frame, text="Submit", bg="lightyellow", font=ARIAL)
        self.money_box.place(x=200, y=100, width=200, height=20)
        self.submitButton.place(x=445, y=100, width=55, height=20)
        self.submitButton.bind("<Button-1>", self.withdrawl_trans)

    def withdrawl_trans(self, flag):
        self.label = Label(self.frame, text="Money Withdrawl !", font=ARIAL)
        self.label.place(x=200, y=100, width=300, height=100)
        self.conn.execute("update atm set bal = bal - ? where acc_no = ?", (self.money_box.get(), self.ac))
        self.conn.commit()


root = Tk()
root.title("Sign In")
root.geometry("600x420")
root.config(bg="cyan")
obj = Bank(root)
root.mainloop()

