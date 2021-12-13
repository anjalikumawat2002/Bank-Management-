from tkinter import *
root = Tk()
root.title("LogIn Page")

lbl1 = Label(root, text="From")
lbl2 = Label(root, text="To")
lbl3 = Label(root, text="Amount")

t1 = Entry(root)
t2 = Entry(root)
t3 = Entry(root)

btn1=Button(root, text="Transfer")
btn2=Button(root, text="Cancel")
btn3=Button(root, text="Close")

lbl1.place(x=100, y=50)
t1.place(x=200, y=50)
lbl2.place(x=100, y=100)
t2.place(x=200, y=100)
lbl3.place(x=100,y=150)
t3.place(x=200,y=150)

btn1.place(x=100, y=200)
btn2.place(x=160,y=200)
btn3.place(x=220,y=200)

root.mainloop()