import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    username = username_var.get()
    password = password_var.get()
    # เช็คข้อมูลล็อกอิน (ที่นี่สามารถเปลี่ยนเป็นการตรวจสอบจริง)
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_login_window():
    # ซ่อนเฟรมอื่น ๆ ที่ไม่จำเป็น
    for frame in content_frames:
        frame.pack_forget()

    login_frame.pack(fill="both", expand=True)

    # ขนาดหน้าจอ
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    # โหลดและปรับขนาดภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\xenos\Pictures\twn6\myn-2.jpg")    # แทนที่ด้วย path ของรูป
    background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
    
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Canvas เพื่อใส่รูปภาพ
    canvas = tk.Canvas(login_frame, width=window_width, height=window_height)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)
    canvas.image = background_photo  # เก็บ reference เพื่อไม่ให้รูปหาย
    canvas.pack(fill="both", expand=True)

    # สร้างฟิลด์ล็อกอิน
    username_label = tk.Label(login_frame, text="Username", bg='white')
    username_label.place(x=100, y=100)
    username_entry = tk.Entry(login_frame, textvariable=username_var)
    username_entry.place(x=200, y=100)

    password_label = tk.Label(login_frame, text="Password", bg='white')
    password_label.place(x=100, y=150)
    password_entry = tk.Entry(login_frame, show="*", textvariable=password_var)
    password_entry.place(x=200, y=150)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.place(x=150, y=200)

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Login Window")
root.geometry("800x600")  # ขนาดหน้าต่าง

# สร้างตัวแปรเพื่อเก็บข้อมูลจากฟิลด์
username_var = tk.StringVar()
password_var = tk.StringVar()

content_frames = []
login_frame = tk.Frame(root)

content_frames.append(login_frame)

show_login_window()

root.mainloop()
