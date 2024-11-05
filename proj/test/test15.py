import tkinter as tk
from tkinter import messagebox
import sqlite3

# สร้างหน้าต่างหลักของแอปพลิเคชัน
root = tk.Tk()
root.title("Knife Store")
root.geometry("400x400")

# เชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect('knife_store.db')
c = conn.cursor()

# สร้างตาราง users และ knives ในฐานข้อมูล (ถ้ายังไม่มี)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

# สร้างผู้ใช้ตัวอย่าง (กรณีที่ไม่มีผู้ใช้อยู่)
c.execute("SELECT * FROM users")
if c.fetchone() is None:
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user1', 'password1'))
    conn.commit()

# ตัวแปรเก็บชื่อผู้ใช้ที่เข้าสู่ระบบ
current_user = None

# ฟังก์ชันแสดงหน้าล็อกอิน
def show_login_window():
    login_frame.pack(pady=20)

# ฟังก์ชันแสดงหน้าหลัก
def show_home_window(logged_in=False):
    if logged_in:
        home_frame.pack(pady=20)
    else:
        login_frame.pack(pady=20)

# ฟังก์ชันเข้าสู่ระบบ
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()

        if user or (username == "Admin" and password == "6304"):  # ตรวจสอบการเข้าสู่ระบบของ Admin ด้วย
            global current_user
            current_user = username  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบ

            login_frame.pack_forget()  # ซ่อนหน้าล็อกอิน

            if username == "Admin" and password == "6304":
                messagebox.showinfo("Login Success", "ยินดีต้อนรับ Admin!")
                button_frame.pack(pady=10)  # แสดงปุ่มทั้งหมดสำหรับ Admin
            else:
                messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {username}!")
                # สำหรับ User ปกติให้แสดงเฉพาะปุ่มบางส่วน
                home_button.pack(side="left")
                knives_button.pack(side="left")
                checkout_button.pack(side="left")
                logout_button.pack(side="left")
                button_frame.pack(pady=10)  # แสดงปุ่มสำหรับผู้ใช้ปกติ

            show_home_window(logged_in=True)  # แสดงหน้าหลักหลังจากล็อกอิน
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันออกจากระบบ
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    
    # ซ่อนปุ่มทั้งหมด
    logout_button.pack_forget()
    button_frame.pack_forget()

    # ซ่อนปุ่มของ Admin (ปุ่มที่เกี่ยวกับการจัดการมีด)
    add_knife_button.pack_forget()
    remove_knife_button.pack_forget()

    # ซ่อนปุ่มของผู้ใช้ปกติ
    home_button.pack_forget()
    knives_button.pack_forget()
    checkout_button.pack_forget()

    show_login_window()  # กลับไปหน้าล็อกอิน

# ฟังก์ชันสำหรับเพิ่มมีด
def add_knife():
    add_knife_window = tk.Toplevel(root)
    add_knife_window.title("เพิ่มมีด")
    add_knife_window.geometry("300x200")

    tk.Label(add_knife_window, text="ชื่อมีด:").pack()
    knife_name_entry = tk.Entry(add_knife_window)
    knife_name_entry.pack()

    tk.Label(add_knife_window, text="ราคา:").pack()
    knife_price_entry = tk.Entry(add_knife_window)
    knife_price_entry.pack()

    def save_knife():
        knife_name = knife_name_entry.get()
        knife_price = knife_price_entry.get()

        if knife_name and knife_price:
            try:
                price = float(knife_price)
                c.execute("INSERT INTO knives (name, price) VALUES (?, ?)", (knife_name, price))
                conn.commit()
                messagebox.showinfo("Success", "เพิ่มมีดเรียบร้อยแล้ว!")
                add_knife_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "กรุณากรอกราคาเป็นตัวเลข")
        else:
            messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

    tk.Button(add_knife_window, text="บันทึก", command=save_knife).pack()

# สร้าง UI สำหรับหน้าล็อกอิน
login_frame = tk.Frame(root)
login_label = tk.Label(login_frame, text="เข้าสู่ระบบ")
login_label.pack()

username_label = tk.Label(login_frame, text="ชื่อผู้ใช้")
username_label.pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

password_label = tk.Label(login_frame, text="รหัสผ่าน")
password_label.pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_frame, text="เข้าสู่ระบบ", command=login)
login_button.pack()

# สร้าง UI สำหรับหน้าหลัก (ปุ่มต่างๆ)
button_frame = tk.Frame(root)

home_button = tk.Button(button_frame, text="หน้าหลัก", command=lambda: show_home_window(logged_in=True))
knives_button = tk.Button(button_frame, text="ซื้อมีด")
checkout_button = tk.Button(button_frame, text="ตะกร้า")
logout_button = tk.Button(button_frame, text="ออกจากระบบ", command=logout)

add_knife_button = tk.Button(button_frame, text="เพิ่มมีด", command=add_knife)
remove_knife_button = tk.Button(button_frame, text="ลบ/แก้ไขมีด")

# เริ่มต้นแสดงหน้าล็อกอิน
show_login_window()

# เริ่มต้น loop ของ Tkinter
root.mainloop()

# ปิดการเชื่อมต่อกับฐานข้อมูลเมื่อโปรแกรมสิ้นสุด
conn.close()
