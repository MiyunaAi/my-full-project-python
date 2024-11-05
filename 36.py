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

    # ขนาดหน้าจอ
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    # แบ่งครึ่งหน้าจอเป็นสองเฟรม
    left_frame = tk.Frame(root, width=window_width//2, height=window_height)
    right_frame = tk.Frame(root, width=window_width//2, height=window_height)

    left_frame.pack(side="left", fill="both", expand=True)
    right_frame.pack(side="right", fill="both", expand=True)

    # โหลดและปรับขนาดภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\xenos\Pictures\twn6\myn-2.jpg")  # แทนที่ด้วย path ของรูป
    background_image = background_image.resize((window_width//2, window_height), Image.LANCZOS)
    
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Canvas เพื่อใส่รูปภาพในเฟรมซ้าย
    canvas = tk.Canvas(left_frame, width=window_width//2, height=window_height)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)
    canvas.image = background_photo  # เก็บ reference เพื่อไม่ให้รูปหาย
    canvas.pack(fill="both", expand=True)

    # สร้างฟิลด์ล็อกอินในเฟรมขวา
    username_label = tk.Label(right_frame, text="Username", font=("Arial", 16))
    username_label.pack(pady=20)
    username_entry = tk.Entry(right_frame, textvariable=username_var, font=("Arial", 14))
    username_entry.pack(pady=10)

    password_label = tk.Label(right_frame, text="Password", font=("Arial", 16))
    password_label.pack(pady=20)
    password_entry = tk.Entry(right_frame, show="*", textvariable=password_var, font=("Arial", 14))
    password_entry.pack(pady=10)

    login_button = tk.Button(right_frame, text="Login", command=login, font=("Arial", 14))
    login_button.pack(pady=40)

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Login Window")
root.geometry("800x600")  # ขนาดหน้าต่าง

# สร้างตัวแปรเพื่อเก็บข้อมูลจากฟิลด์
username_var = tk.StringVar()
password_var = tk.StringVar()

content_frames = []

show_login_window()

root.mainloop()
