
import getpass
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from tkinter import messagebox
import os.path
import socket
from tkinter import filedialog
import os
from plyer import notification
import winsound
import ctypes
import os
import sqlite3
import wikipedia

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)
master = Tk()
master.title("H-PING")
master.geometry('350x200')

def center(toplevel):
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2.5 - size[0]/3
    y = screen_height/2.5 - size[1]/3
    toplevel.geometry("+%d+%d" % (x, y))

def handle_server(ip, s):
    master.withdraw()
    server_username = s.recv(4141)
    server_username = server_username.decode('ascii')

    top = Toplevel()
    top.title('H-PING')
    top.geometry("400x500")
    top.attributes('-topmost', 1)
    top.attributes('-topmost', 0)
    center(top)
    top.resizable(width=FALSE, height=FALSE)
    inputentry = Text(top, bd=0, bg="white", width="29", height="5", font=("Arial", 12))
    inputentry.configure(highlightbackground='lightgrey', highlightthickness=1)
    inputentry.bind('<Return>', (lambda event: send()))
    img = ImageTk.PhotoImage(Image.open("user4.png"))
    panel = Label(top, image=img)
    prompt = server_username
    user_lb = Label(top, text=prompt, width=len(prompt), font=(12,))
    prompt = ip
    ip_lb = Label(top, text=prompt, width=len(prompt), font=("Arial", 8))
    SendButton = Button(top, font=30, text="Send", width="12", height=5, bd=0, command=(lambda: send()))
    send_img = PhotoImage(file="e2.png")  # make sure to add "/" not "\"
    SendButton.config(image=send_img)
    up = Button(top, text="Attach", font=30, width="18", height=3, bd=0, command=(lambda: FileTransfer()))
    upbt_img = PhotoImage(file="at3.png")  # make sure to add "/" not "\"
    up.config(image=upbt_img)
    up1 = Button(top, text="money transfer ", font=30, width="18", height=3, bd=0,command=(lambda:stk()))
    abt_img = PhotoImage(file="money transfer.png")
    up1.config(image=abt_img)
    ggt = Button(top, text="google ", font=30, width="18", height=3, bd=0,command=(lambda:google()))
    sept_img=PhotoImage(file="google.png")
    ggt.config(image=sept_img)

    outputtext = Text(top, bd=0, bg="white", height="8", width="50", font=("Arial", 12))
    outputtext.configure(highlightbackground='lightgrey', highlightthickness=1)
    scrollbar = Scrollbar(top, command=outputtext.yview)
    outputtext['yscrollcommand'] = scrollbar.set
    def send():
        varContent = inputentry.get("1.0", END)
        varContent = varContent.strip()
        if varContent and (not varContent.isspace()):
            message = varContent.encode("ascii")
            s.send(message)
            message = "\n" + varContent + "\n\n"
            outputtext.tag_config('user_message', justify='right',wrap='word')
            outputtext.insert(tk.END, message, 'user_message')
            outputtext.see(tk.END)
            inputentry.delete('1.0', END)

    def recv():
        while True:
            reply = s.recv(4141)
            reply = reply.decode('ascii')

            chek = 'START_TRANSFER_FILE_NAME#3@41$*='
            if chek in reply:
                # print(reply)
                file_name = reply.split("=", 1)[1]
                scc = socket.socket()
                port = 6767
                scc.connect((ip, port))
                received_path = os.path.expanduser('~\\Downloads\\')
                with open(received_path + file_name, 'wb') as f:
                    while True:

                        data = scc.recv(1024)

                        f.write(data)

                        if not data:
                            break

                fmessage = "\n" + file_name + "\n\n"
                outputtext.tag_config('r', background="lightsteelblue", foreground="royalblue")
                outputtext.insert(tk.END, fmessage, 'r')
                f.close()
                scc.close()
                popup2 = Toplevel()
                popup2.title('File Received')
                popup2.geometry('250x100')
                popup2.attributes('-topmost', 1)
                popup2.attributes('-topmost', 0)
                prompt = file_name+" received"
                label1 = Label(popup2, text=prompt, width=len(prompt), font=("Arial", 10))
                label1.place(x=45, y=32, height=39, width=200)
                imgn = ImageTk.PhotoImage(Image.open("tick.png"))
                paneln = Label(popup2, image=imgn)
                paneln.place(x=14, y=30, height=39, width=30)
                def close_after_2s():
                    popup2.destroy()
                popup2.after(4000, close_after_2s)

            else:
                reply = "\n" + reply + "\n\n"
                outputtext.tag_config('reply', background="lightsteelblue", foreground="black", wrap='word')
                outputtext.insert(tk.END, reply, 'reply')
                outputtext.see(tk.END)

                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                winsound.PlaySound("notif.wav", winsound.SND_ALIAS)

                if 'normal' != top.state():
                    popup3 = Toplevel()
                    popup3.title('Notification')
                    popup3.geometry('250x100')
                    popup3.attributes('-topmost', 1)
                    popup3.attributes('-topmost', 0)
                    prompt ="Message received from\n " + server_username + ""
                    label3 = Label(popup3, text=prompt, width=len(prompt), font=("Arial", 10))
                    label3.place(x=45, y=32, height=39, width=200)
                    imgn = ImageTk.PhotoImage(Image.open("tick.png"))
                    paneln3 = Label(popup3, image=imgn)
                    paneln3.place(x=14, y=30, height=39, width=30)
                    def close_after_2s():
                        popup3.destroy()
                    popup3.after(4000, close_after_2s)

                    notification.notify(
                        title='New message received',
                        message="Message received from \n" + server_username + "",
                        app_name='H-PING',
                        timeout=20,
                        app_icon='3.ico')


    def FileTransfer():
            File_path = filedialog.askopenfilename(title='Choose file to send')

            if File_path:
                File_name = os.path.basename(File_path)
                trnsfr_st = 'START_TRANSFER_FILE_NAME#3@41$*=' + File_name
                message = trnsfr_st.encode("ascii")
                s.send(message)
                port = 7676
                ss = socket.socket()
                host = "0.0.0.0"
                ss.bind((host, port))
                ss.listen(5)
                conns, addr = ss.accept()
                while True:
                    b = os.path.getsize(File_path)
                    f = open(File_path, 'rb')
                    l = f.read(b)

                    while (l):
                        conns.send(l)

                        l = f.read(b)
                    f.close()
                    break
                conns.close()
                ss.close()
                # messagebox.showinfo("Success", File_name + " Sent")
                popup4 = Toplevel()
                popup4.title('Success')
                popup4.geometry('250x100')
                popup4.attributes('-topmost', 1)
                popup4.attributes('-topmost', 0)
                prompt = File_name + " Sent"
                label4 = Label(popup4, text=prompt, width=len(prompt), font=("Arial", 10))
                label4.place(x=45, y=32, height=39, width=200)
                img4 = ImageTk.PhotoImage(Image.open("ms1.png"))
                panel4 = Label(popup4, image=img4)
                panel4.place(x=14, y=30, height=39, width=30)
                def close_after_2s():
                    popup4.destroy()

                popup4.after(4000, close_after_2s)
                ftmessage = "\n" + File_name + "\n\n"
                outputtext.tag_config('u', justify='right', foreground="royalblue")
                outputtext.insert(tk.END, ftmessage, 'u')
    def google():
        def get_me():
            entry_value = entry.get()
            answer.delete(1.0, END)
            try:
                answer_value = wikipedia.summary(entry_value)
                answer.insert(INSERT, answer_value)
            except:
                answer.insert(INSERT, "please check you input or internet connection")

        root = Tk()

        topframe = Frame(root)
        entry = Entry(topframe)
        entry.pack()
        button = Button(topframe, text="search", command=get_me)
        button.pack()
        topframe.pack(side=TOP)

        bottomframe = Frame(root)
        scroll = Scrollbar(bottomframe)
        scroll.pack(side=RIGHT, fill=Y)
        answer = Text(bottomframe, width=70, height=20, yscrollcommand=scroll.set, wrap=WORD, bg="aqua")
        scroll.config(command=answer.yview)
        answer.pack()
        bottomframe.pack()

        root.mainloop()

    def stk():
        # Account Number : 10 ------------ Password : trial

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
                self.temp = self.conn.execute("select name,pass,acc_no,acc_type,bal from atm where acc_no = ? ",
                                              (self.ac,))
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
                self.detail = Button(self.frame, text="Account Details", bg="blue", font=ARIAL,
                                     command=self.account_detail)
                self.enquiry = Button(self.frame, text="Balance Enquiry", bg="pink", font=ARIAL, command=self.Balance)
                self.deposit = Button(self.frame, text="Deposit Money", bg="pink", font=ARIAL,
                                      command=self.deposit_money)
                self.withdrawl = Button(self.frame, text="Withdrawl Money", bg="pink", font=ARIAL,
                                        command=self.withdrawl_money)
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

        root = Toplevel()
        root.title("Sign In")
        root.geometry("600x420")
        root.config(bg="cyan")
        obj = Bank(root)


    scrollbar.place(x=376, y=40, height=352)
    outputtext.place(x=6, y=40, height=352, width=370)
    inputentry.place(x=6, y=401, height=90, width=265)
    panel.place(x=6, y=1, height=39, width=39)
    SendButton.place(x=285, y=418, height=60, width=62)
    up.place(x=360, y=3, height=32, width=32)
    up1.place(x=320, y=3,height=32,width=32)
    ggt.place(x=280, y=3, height=32, width=32)
    user_lb.place(x=45, y=4, height=18)
    ip_lb.place(x=50, y=26, height=10)
    def onclosing(arg,s):

            s.close()
            top.destroy()
            sys.exit()
    top.protocol("WM_DELETE_WINDOW", lambda arg=(top): onclosing(arg, s))
    while True:
        t2=Thread(target=recv())
        t2.start()

def chat_window(userInput):
  try:

    e1.configure(text=userInput.get())
    ip = userInput.get()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 4141
    s.connect((ip, port))
    user_name = getpass.getuser()
    user_name = user_name.encode("ascii")
    s.send(user_name)
    t = Thread(target=handle_server, args=(ip, s))
    t.start()

  except Exception as e:
    messagebox.showerror("Error", "Please activate H PINGER in target system first or check IP")
    master.destroy()

def connect(userInput):
        t1 = Thread(target=chat_window(userInput))
        t1.start()
userInput = StringVar()
ll = Label(master, text="IP Address:",  font=("Arial", 10))
ll.config(height=2, width=15)
ll.place(x=15, y=65, height=18)
e1 = Entry(master, textvariable=userInput,width=20, font=("Arial", 12))
e1.bind('<Return>', (lambda event: connect(userInput)))
e1.place(x=120, y=60, height=25)
imgu = ImageTk.PhotoImage(Image.open("user3.png"))
panelu = Label(master, image = imgu)
panelu.place(x=6, y=6, height=35)
slabel1 = Label(text=getpass.getuser(),font=("Arial", 10))
slabel1.place(x=48, y=18, height=14)
ss = Button(text='connect', anchor='center', font=30, width=18, height=3, bd=0, command=(lambda: connect(userInput)))
act_img = PhotoImage(file='e1.png')
ss.config(image=act_img)
ss.place(x=200, y=110, height=68, width=68)

master.mainloop()