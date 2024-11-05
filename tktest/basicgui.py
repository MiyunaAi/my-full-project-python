from tkinter import *

root = Tk()
root.title("My GUI")

#ใส่่ข้อความในหน้าจอ
myLable = Label(text="Kuay",fg="red",font=20,bg="black").pack()
myLable1 = Label(text="Kuay").pack()

#กำหนดขนาดหน้าจอและตำแหน่ง +แรกx+สองy
root.geometry("600x200+500+300")
root.mainloop() 
