import random
import sqlite3
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

conn = sqlite3.connect('database.s3db')
cur = conn.cursor()

root = tk.Tk()
root.title("finance holding bank")
root.config(bg='#3F3351')
root.iconbitmap("images/bank_icon.ico")


def create_btn():
    global create_account_frame
    global home_frame
    global t2, t3, t4
    t2.delete(0, tk.END)
    t3.delete(0, tk.END)
    t4.delete(0, tk.END)
    create_account_frame.pack()
    home_frame.pack_forget()
    myAcc.create_account()


def cancel_btn():
    global create_account_frame
    global home_frame
    home_frame.pack()
    create_account_frame.pack_forget()


def save_btn():
    global create_account_frame
    global home_frame, t3, t4, t5
    if t3.get() == "" or t4.get() == "" or t5.get() == "":
        messagebox.showwarning("unfilled", "Please fill all entries")
        return

    myAcc.save_acc()
    messagebox.showinfo('saved', "your Account has been created")
    create_account_frame.pack_forget()
    home_frame.pack()


def close_btn():
    global create_account_frame, home_frame, login_frame, closed_frame, transfer_frame, deposit_frame, withdraw_frame
    create_account_frame.pack_forget()
    home_frame.pack_forget()
    login_frame.pack_forget()
    transfer_frame.pack_forget()
    deposit_frame.pack_forget()
    withdraw_frame.pack_forget()
    closed_frame.pack()


def login_btn():
    myAcc.log_in()


def go_to_transfer_frame():
    global login_frame, transfer_frame
    login_frame.pack_forget()
    transfer_frame.pack()


def transfer_cancel_btn():
    global login_frame, transfer_frame, deposit_frame, withdraw_frame
    transfer_frame.pack_forget()
    deposit_frame.pack_forget()
    withdraw_frame.pack_forget()
    login_frame.pack()


def transfer_btn():
    global login_frame, transfer_frame, balance_login_lbl
    myAcc.transfer_to()
    transfer_frame.pack_forget()
    login_frame.pack()
    balance_login_lbl = tk.Label(login_frame, text=f"balance: {myAcc.balance}", font=('calibri', 27), fg='white',
                                 bg='black').grid(row=2, column=4, columnspan=2)

    
    
def withdraw_btn():
    global login_frame, withdraw_frame
    global t1_withdraw, t2_withdraw, t3_withdraw, t4_withdraw, t5_withdraw
    t1_withdraw.delete(0, tk.END)
    t2_withdraw.delete(0, tk.END)
    t3_withdraw.delete(0, tk.END)
    t4_withdraw.delete(0, tk.END)
    t5_withdraw.delete(0, tk.END)
    login_frame.pack_forget()
    withdraw_frame.pack()


def deposit_btn():
    global login_frame, deposit_frame
    global t1_deposit, t2_deposit, t3_deposit, t4_deposit, t5_deposit
    t1_deposit.delete(0, tk.END)
    t2_deposit.delete(0, tk.END)
    t3_deposit.delete(0, tk.END)
    t4_deposit.delete(0, tk.END)
    t5_deposit.delete(0, tk.END)
    login_frame.pack_forget()
    deposit_frame.pack()

def show_btn_deposit():
    global t1_deposit, t2_deposit, t3_deposit, t4_deposit, t5_deposit
    global myAcc
    t1_deposit.delete(0, tk.END)
    t2_deposit.delete(0, tk.END)
    t3_deposit.delete(0, tk.END)
    t4_deposit.delete(0, tk.END)
    t5_deposit.delete(0, tk.END)
    t1_deposit.insert(0, myAcc.accNo)
    t3_deposit.insert(0, myAcc.name)
    t4_deposit.insert(0, myAcc.phone)
    messagebox.showinfo("guideline", "enter pin and Amount")


def show_btn_withdraw():
    global t1_withdraw, t2_withdraw, t3_withdraw, t4_withdraw, t5_withdraw
    global myAcc
    t1_withdraw.delete(0, tk.END)
    t2_withdraw.delete(0, tk.END)
    t3_withdraw.delete(0, tk.END)
    t4_withdraw.delete(0, tk.END)
    t5_withdraw.delete(0, tk.END)
    t1_withdraw.insert(0, myAcc.accNo)
    t3_withdraw.insert(0, myAcc.name)
    t4_withdraw.insert(0, myAcc.phone)
    messagebox.showinfo("guideline", "enter pin and Amount")


def delete_btn_login():
    global login_frame, home_frame, myAcc, e1, e2
    click = messagebox.askyesno("delete", "do you want to delete Your account")
    if click:
        cur.execute(f"DELETE FROM database WHERE Account = {myAcc.accNo}")
        conn.commit()
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        login_frame.pack_forget()
        home_frame.pack()
    else:
        return


def update_withdraw():
    global t2_withdraw, t5_withdraw, myAcc, balance_login_lbl, login_frame, withdraw_frame
    if t2_withdraw.get() == myAcc.pin:
        try:
            amount_withdraw = int(t5_withdraw.get())
            if amount_withdraw < myAcc.balance:
                click = messagebox.askyesno('withdraw', "do you want to withdraw?")
                if click:
                    myAcc.balance -= amount_withdraw
                    cur.execute(f"UPDATE database SET balance = {myAcc.balance} WHERE Account = {myAcc.accNo}")
                    conn.commit()
                    balance_login_lbl = tk.Label(login_frame, text=f"balance: {myAcc.balance}", font=('calibri', 27),
                                                 fg='white',
                                                 bg='black').grid(row=2, column=4, columnspan=2)
                    messagebox.showinfo('info', 'amount has been withdraw')
                    withdraw_frame.pack_forget()
                    login_frame.pack()
                else:
                    return
            else:
                messagebox.showwarning('warning', 'insufficient amount')
                return
        except:
            messagebox.showwarning('error', "please reenter amount")
            return
    else:
        messagebox.showwarning('warning', 'invalid pin')
        return


def update_deposit():
    global t2_deposit, t5_deposit, myAcc, balance_login_lbl, login_frame, deposit_frame
    if t2_deposit.get() == myAcc.pin:
        try:
            amount_deposit = int(t5_deposit.get())

            click = messagebox.askyesno('withdraw', "do you want to deposit?")
            if click:
                myAcc.balance += amount_deposit
                cur.execute(f"UPDATE database SET balance = {myAcc.balance} WHERE Account = {myAcc.accNo}")
                conn.commit()
                balance_login_lbl = tk.Label(login_frame, text=f"balance: {myAcc.balance}", font=('calibri', 27),
                                                 fg='white',
                                                 bg='black').grid(row=2, column=4, columnspan=2)
                messagebox.showinfo('info', 'amount has been deposit')
                deposit_frame.pack_forget()
                login_frame.pack()
            else:
                return

        except:
            messagebox.showwarning('error', "please reenter amount")
            return
    else:
        messagebox.showwarning('warning', 'invalid pin')
        return



def checksum(x):
    addition, digit, count = 0, 0, 1
    for i in x:
        if count % 2 != 0:
            if int(i) * 2 > 9:
                addition += int(i) * 2 - 9
            else:
                addition += int(i) * 2
        else:
            addition += int(i)

    for i in range(10):
        if (addition + i) % 10 == 0:
            digit = i
            break
    return digit


class Account:

    def __init__(self):
        self.accNo = ""
        self.pin = ""
        self.name = ""
        self.balance = 0
        self.phone = ""

    def create_account(self):
        accounts = list(cur.execute('SELECT Account FROM database'))
        print(accounts)
        global t1, t2
        while True:
            x = '400000' + str(random.randrange(0, 999999999)).zfill(9)
            last_digit = checksum(x)

            x += str(last_digit)

            pin = str(random.randrange(9999)).zfill(4)

            if (x,) not in accounts:
                self.accNo = x
                self.pin = pin
                break

        t1.insert(0, x)
        t2.insert(0, pin)

    def save_acc(self):
        global t3, t4, t5
        accounts = list(cur.execute('SELECT Account FROM database'))
        name = t3.get()  # this will be changed to display the it on gui
        phone = t5.get()  # this will be changed to display the it on gui
        balance = int(t4.get())
        self.name, self.phone, self.balance = name, phone, balance
        cur.execute(f"INSERT INTO database (id, Account, pin, name, balance, phone) VALUES(?, ?, ?, ?, ?, ?)"
                    , (len(accounts) + 1, self.accNo, self.pin, self.name, self.balance, self.phone))
        conn.commit()

    def log_in(self):
        global e1, e2, home_frame, login_frame
        all_accounts = list(cur.execute("SELECT Account, pin FROM database"))
        logged_in = False
        acc = e1.get()
        password = e2.get()

        for x, y in all_accounts:
            if acc == x and password == y:
                home_frame.pack_forget()
                login_frame.pack()
                card_detail = list(cur.execute(f'SELECT * FROM database WHERE Account = {acc}'))
                print(card_detail)
                id, self.accNo, self.pin, self.name, self.balance, self.phone = card_detail[0]
                logged_in = True
                break
        else:
            messagebox.showwarning(title="Error", message="Account No or pin is invalid")
            return

        if logged_in:
            global name_login_lbl, phone_login_lbl, balance_login_lbl

            name_login_lbl = tk.Label(login_frame, text=f"Name: {self.name}", font=('calibri', 27), fg='white',
                                      bg='black').grid(row=0, column=4, columnspan=2)

            phone_login_lbl = tk.Label(login_frame, text=f"mobile No: {self.phone}", font=('calibri', 27), fg='white',
                                       bg='black').grid(row=1, column=4, columnspan=2)

            balance_login_lbl = tk.Label(login_frame, text=f"balance: {self.balance}", font=('calibri', 27), fg='white',
                                         bg='black').grid(row=2, column=4, columnspan=2)

    def transfer_to(self):
        x = t_1.get()
        amount = int(t_3.get())
        pin = t_2.get()
        if (x,) in list(cur.execute(f"SELECT Account FROM database")) and pin == self.pin:
            other_account_balance = int(list(cur.execute(f"SELECT balance FROM database WHERE Account = {x}"))[0][0])
            if amount < self.balance:
                confirmation = messagebox.askyesno("transfer", "do you want to transfer")
                if not confirmation:
                    return
                else:
                    other_account_balance += amount
                    self.balance -= amount
                    cur.execute(f"UPDATE database SET balance = {other_account_balance} WHERE Account = {x}")
                    cur.execute(f"UPDATE database SET balance = {self.balance} WHERE Account = {self.accNo}")
                    conn.commit()
                    messagebox.showinfo("transferred", "amount transferred successfully!")
            else:
                messagebox.showwarning("error", "Insufficient balance")

        else:
            messagebox.showwarning("error", "Such account does not exist")




myAcc = Account()

print(list(cur.execute("SELECT * FROM database")))
# home frame
home_frame = tk.Frame(root)

bank_img = ImageTk.PhotoImage(Image.open("images/bank_home_page.jpeg"))
img_label = tk.Label(home_frame, image=bank_img).grid(row=0, column=0, columnspan=3)
account_label = tk.Label(home_frame, text="Acc No: ",  font=('Arial', 12)).grid(row=1, column=0)
pin_label = tk.Label(home_frame, text="PIN: ", font=('Arial', 12)).grid(row=2, column=0)
create_label = tk.Label(home_frame, text="Don't have a Account:", font=('Arial', 12)).grid(row=4, column=0, columnspan=2)

e1 = tk.Entry(home_frame)
e2 = tk.Entry(home_frame)
btn1_ = tk.Button(home_frame, text="Login", command=login_btn)
btn2_ = tk.Button(home_frame, text="create", command=create_btn)


e1.grid(row=1, column=1, pady=6, columnspan=2, sticky=tk.W+tk.E, padx=4)
e2.grid(row=2, column=1, pady=6, columnspan=2, sticky=tk.W+tk.E, padx=4)
btn1_.grid(row=3, column=2, pady=5, padx=4, sticky=tk.W+tk.E)

btn2_.grid(row=4, column=2, sticky=tk.W+tk.E, padx=4, pady=5)

home_frame.pack()


# create account
create_account_frame = tk.Frame(root)
lbl1 = tk.Label(create_account_frame, text="Account No")
lbl2 = tk.Label(create_account_frame, text="PIN")
lbl3 = tk.Label(create_account_frame, text="Name")
lbl4 = tk.Label(create_account_frame, text="Amount")
lbl5 = tk.Label(create_account_frame, text="Phone No")

t1 = tk.Entry(create_account_frame)
t2 = tk.Entry(create_account_frame)
t3 = tk.Entry(create_account_frame)
t4 = tk.Entry(create_account_frame)
t5 = tk.Entry(create_account_frame)

btn1 = tk.Button(create_account_frame, text="Save", command=save_btn)
btn2 = tk.Button(create_account_frame, text="Cancel", command=cancel_btn)
btn3 = tk.Button(create_account_frame, text="Close", command=close_btn)
lbl1.grid(row=0, column=0, padx=60, pady=10)
t1.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5)
lbl2.grid(row=1, column=0, padx=60, pady=10)
t2.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5)
lbl3.grid(row=2, column=0, padx=60, pady=10)
t3.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5)
lbl4.grid(row=3, column=0, padx=60, pady=10)
t4.grid(row=3, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5)
lbl5.grid(row=4, column=0, pady=10)
t5.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5)


btn1.grid(row=5, column=0, padx=5)
btn2.grid(row=5, column=1, padx=5)
btn3.grid(row=5, column=2, padx=5)

# login frame
login_frame = tk.Frame(root)

img = ImageTk.PhotoImage(Image.open("images/login_page.jpeg"))
label_img = tk.Label(login_frame, image=img).grid(row=0, column=0, rowspan=10, columnspan=10, sticky=tk.N+tk.S+tk.W+tk.E)


b1 = tk.Button(login_frame, text="Delete Account", font =
               ('calibri', 20, 'bold'),
            borderwidth ='4', activeforeground="#678983", activebackground="#B4FE98", width=20, pady=10, command=delete_btn_login)

b2 = tk.Button(login_frame, text="Withdraw", font=
                    ('calibri', 20, 'bold'),
                    borderwidth='4', activeforeground="#678983", activebackground="#B4FE98", width = 20, pady=10, command=withdraw_btn)

b3 = tk.Button(login_frame, text="Deposite", font =
               ('calibri', 20, 'bold'),
            borderwidth = '4', activeforeground="#678983", activebackground="#B4FE98", width = 20, pady=10, command=deposit_btn)

b4 = tk.Button(login_frame, text="Transfer", font =
               ('calibri', 20, 'bold'),
            borderwidth = '4', activeforeground="#678983", activebackground="#B4FE98", width = 20, pady=10, command=go_to_transfer_frame)
b5 = tk.Button(login_frame, text="Close", font =
               ('calibri', 20, 'bold'),
            borderwidth = '4', activeforeground="red", activebackground="pink", width = 20, pady=10,command=close_btn )

b1.grid(row=0, column=9, padx=100)
b2.grid(row=1, column=9, pady=10, padx=100)
b3.grid(row=2, column=9, pady=10, padx=100)
b4.grid(row=3, column=9, pady=10, padx=100)
b5.grid(row=4, column=5, pady=10, padx=100)


# transfer frame
transfer_frame = tk.Frame(root)

lb1 = tk.Label(transfer_frame, text="To Account No", font =
               ('calibri', 13, 'bold')).grid(row=0,column=0, pady = 2)
lb2 = tk.Label(transfer_frame, text="PIN", font =
               ('calibri', 13, 'bold')).grid(row=1,column=0,pady = 2)
lb3 = tk.Label(transfer_frame, text="Amount", font =
               ('calibri', 13, 'bold')).grid(row=2,column=0,pady = 2)

t_1 = tk.Entry(transfer_frame)
t_2 = tk.Entry(transfer_frame)
t_3 = tk.Entry(transfer_frame)

btn_1=tk.Button(transfer_frame, text="Transfer ", font =
               ('calibri', 11, 'bold'), width = 10, pady=5, borderwidth = '3', activeforeground="black", activebackground="light green",
                command=transfer_btn)
btn_2=tk.Button(transfer_frame, text=" Cancel ", font =
               ('calibri', 11, 'bold'), width=8, pady=5, borderwidth = '3', activeforeground="red", activebackground="pink",
                command=transfer_cancel_btn)
btn_3=tk.Button(transfer_frame, text=" Close ", font =
               ('calibri', 11, 'bold'), width=10, pady=5, borderwidth = '3', activeforeground="red", activebackground="#E7EAB5",
                command=close_btn)
t_1.grid(row=0,column=1,pady=10,columnspan=5)
t_2.grid(row=1,column=1,pady=10,columnspan=5)
t_3.grid(row=2,column=1,pady=10,columnspan=5)

btn_1.grid(row=8,column=0,padx=10)
btn_2.grid(row=8,column=1,padx=10)
btn_3.grid(row=8,column=2,padx=10)


# withdraw frame
withdraw_frame = tk.Frame(root)
lb1_withdraw = tk.Label(withdraw_frame, text="Account No", font =
               ('calibri', 13, 'bold')).grid(row=0,column=0, pady = 2)
lb2_withdraw = tk.Label(withdraw_frame, text="PIN", font =
               ('calibri', 13, 'bold')).grid(row=1,column=0,pady = 2)
lb3_withdraw = tk.Label(withdraw_frame, text="Name", font =
               ('calibri', 13, 'bold')).grid(row=2,column=0,pady = 2)
lb4_withdraw = tk.Label(withdraw_frame, text="Phone No", font =
               ('calibri', 13, 'bold')).grid(row=3,column=0,pady = 2)
lb5_withdraw = tk.Label(withdraw_frame, text="Amount", font =
               ('calibri', 13, 'bold')).grid(row=4,column=0,pady = 2)
t1_withdraw = tk.Entry(withdraw_frame)
t2_withdraw = tk.Entry(withdraw_frame)
t3_withdraw = tk.Entry(withdraw_frame)
t4_withdraw = tk.Entry(withdraw_frame)
t5_withdraw = tk.Entry(withdraw_frame)

btn1_withdraw=tk.Button(withdraw_frame, text="Update ", font =
               ('calibri', 11, 'bold'), width = 10, pady=5, borderwidth='3', activeforeground="black",
                        activebackground="light green", command=update_withdraw)
btn2_withdraw=tk.Button(withdraw_frame, text=" Cancel ", font =
               ('calibri', 11, 'bold'), width=8, pady=5, borderwidth = '3', activeforeground="red",
                        activebackground="pink", command=transfer_cancel_btn)
btn3_withdraw=tk.Button(withdraw_frame, text=" Close ", font =
               ('calibri', 11, 'bold'), width=10, pady=5, borderwidth = '3', activeforeground="red",
                        activebackground="#E7EAB5", command=close_btn)
btn4_withdraw=tk.Button(withdraw_frame, text=" Show ", font =
               ('calibri', 11, 'bold'), width=9, pady=5, borderwidth = '3', activeforeground="black",
                        activebackground="#E7EAB5", command=show_btn_withdraw)
t1_withdraw.grid(row=0,column=1,pady=10,columnspan=5)
t2_withdraw.grid(row=1,column=1,pady=10,columnspan=5)
t3_withdraw.grid(row=2,column=1,pady=10,columnspan=5)
t4_withdraw.grid(row=3,column=1,pady=10,columnspan=5)
t5_withdraw.grid(row=4,column=1,pady=10,columnspan=5)

btn1_withdraw.grid(row=8,column=0,padx=10)
btn2_withdraw.grid(row=8,column=1,padx=10)
btn3_withdraw.grid(row=8,column=2,padx=10)
btn4_withdraw.grid(row=0,column=5,padx=2,columnspan=5)


# deposit frame
deposit_frame = tk.Frame(root)

lb1_deposit = tk.Label(deposit_frame, text="Account No", font =
               ('calibri', 13, 'bold')).grid(row=0,column=0, pady = 2)
lb2_deposit = tk.Label(deposit_frame, text="PIN", font =
               ('calibri', 13, 'bold')).grid(row=1,column=0,pady = 2)
lb3_deposit = tk.Label(deposit_frame, text="Name", font =
               ('calibri', 13, 'bold')).grid(row=2,column=0,pady = 2)
lb4_deposit = tk.Label(deposit_frame, text="Phone No", font =
               ('calibri', 13, 'bold')).grid(row=3,column=0,pady = 2)
lb5_deposit = tk.Label(deposit_frame, text="Amount", font =
               ('calibri', 13, 'bold')).grid(row=4,column=0,pady = 2)
t1_deposit = tk.Entry(deposit_frame)
t2_deposit = tk.Entry(deposit_frame)
t3_deposit = tk.Entry(deposit_frame)
t4_deposit = tk.Entry(deposit_frame)
t5_deposit = tk.Entry(deposit_frame)

btn1_deposit=tk.Button(deposit_frame, text="Update ", font =
               ('calibri', 11, 'bold'), width = 10, pady=5, borderwidth = '3', activeforeground="black",
                       activebackground="light green", command=update_deposit)
btn2_deposit = tk.Button(deposit_frame, text=" Cancel ", font =
               ('calibri', 11, 'bold'), width=8, pady=5, borderwidth = '3', activeforeground="red",
                         activebackground="pink", command=transfer_cancel_btn)
btn3_deposit=tk.Button(deposit_frame, text=" Close ", font =
               ('calibri', 11, 'bold'), width=10, pady=5, borderwidth = '3', activeforeground="red",
                       activebackground="#E7EAB5", command=close_btn)
btn4_deposit=tk.Button(deposit_frame, text=" Show ", font =
               ('calibri', 11, 'bold'), width=9, pady=5, borderwidth='3', activeforeground="black",
                       activebackground="#E7EAB5", command=show_btn_deposit)
t1_deposit.grid(row=0, column=1, pady=10, columnspan=5)
t2_deposit.grid(row=1, column=1, pady=10, columnspan=5)
t3_deposit.grid(row=2, column=1, pady=10, columnspan=5)
t4_deposit.grid(row=3, column=1, pady=10, columnspan=5)
t5_deposit.grid(row=4, column=1, pady=10, columnspan=5)

btn1_deposit.grid(row=8, column=0, padx=10)
btn2_deposit.grid(row=8, column=1, padx=10)
btn3_deposit.grid(row=8, column=2, padx=10)
btn4_deposit.grid(row=0, column=5, padx=2, columnspan=5)



# closed frame
closed_frame = tk.Frame(root)
logo = ImageTk.PhotoImage(Image.open("images/close_image.jpeg"))
w = tk.Label(closed_frame,justify=tk.LEFT,
          compound = tk.LEFT,
          padx = 10,

             text="Thankyou \n For Joining Our Bank !!",font =
               ('Algerian', 25, 'bold'),
             image=logo).pack(side="right")

root.mainloop()
