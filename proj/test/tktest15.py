import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# สร้างหรือเชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect(r'C:\Users\xenos\Documents\datab\knife_shop.db')
c = conn.cursor()

# สร้างตารางผู้ใช้ถ้ายังไม่มี
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# สร้างตารางมีดถ้ายังไม่มี
c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER
    )
''')

# สร้างตารางประวัติการซื้อถ้ายังไม่มี
c.execute('''
    CREATE TABLE IF NOT EXISTS purchase_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        knife_name TEXT,
        quantity INTEGER,
        total_price INTEGER,
        FOREIGN KEY (username) REFERENCES users(username)
    )
''')

# ตัวแปรเก็บผู้ใช้ที่ล็อกอินปัจจุบัน
current_user = None

# ฟังก์ชันคำนวณราคารวมของมีดในตะกร้า
def calculate_total_price():
    c.execute("SELECT SUM(price * stock) FROM knives")
    total_price = c.fetchone()[0]
    return total_price if total_price else 0

# ฟังก์ชันรีเฟรชรายการมีดใน Treeview
def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price FROM knives")
    knives = c.fetchall()
    for name, stock, price in knives:
        total_price_per_type = price * stock
        treeview.insert("", "end", values=(name, stock, price, total_price_per_type))

# ฟังก์ชันแสดงหน้าต่างเพิ่มมีดใหม่
def add_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    add_knife_frame.pack(fill="both", expand=True)

# ฟังก์ชันเพิ่มมีดใหม่
def add_knife():
    name = knife_name_entry.get()
    stock = knife_stock_entry.get()
    price = knife_price_entry.get()
    if name and stock.isdigit() and price.isdigit():
        stock = int(stock)
        price = int(price)
        if stock > 0 and price > 0:
            # เพิ่มข้อมูลมีดลงในฐานข้อมูล
            c.execute("INSERT INTO knives (name, stock, price) VALUES (?, ?, ?)", (name, stock, price))
            conn.commit()
            messagebox.showinfo("Success", f"เพิ่มมีด {name} เรียบร้อยแล้ว!")
            knife_name_entry.delete(0, tk.END)
            knife_stock_entry.delete(0, tk.END)
            knife_price_entry.delete(0, tk.END)
            refresh_knife_list(knife_tree)
        else:
            messagebox.showwarning("Invalid input", "จำนวนและราคาต้องมากกว่า 0")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ถูกต้อง")

# ฟังก์ชันลบจำนวนหรือชนิดมีด
def remove_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    remove_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(remove_knife_tree)

# ฟังก์ชันเพิ่มจำนวนมีด
def increase_stock():
    selected_item = remove_knife_tree.selection()
    if selected_item:
        name = remove_knife_tree.item(selected_item)['values'][0]
        c.execute("SELECT stock FROM knives WHERE name = ?", (name,))
        stock = c.fetchone()[0]
        c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock + 1, name))
        conn.commit()
        refresh_knife_list(remove_knife_tree)
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการเพิ่มจำนวน")

# ฟังก์ชันลดจำนวนมีด
def decrease_stock():
    selected_item = remove_knife_tree.selection()
    if selected_item:
        name = remove_knife_tree.item(selected_item)['values'][0]
        c.execute("SELECT stock FROM knives WHERE name = ?", (name,))
        stock = c.fetchone()[0]
        if stock > 1:
            c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock - 1, name))
            conn.commit()
            refresh_knife_list(remove_knife_tree)
        else:
            messagebox.showwarning("Warning", "จำนวนมีดต้องมากกว่าหรือเท่ากับ 1")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการลดจำนวน")

# ฟังก์ชันลบมีด
def delete_knife():
    selected_item = remove_knife_tree.selection()
    if selected_item:
        name = remove_knife_tree.item(selected_item)['values'][0]
        c.execute("DELETE FROM knives WHERE name = ?", (name,))
        conn.commit()
        refresh_knife_list(remove_knife_tree)
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการลบ")

# ฟังก์ชันแสดงตารางมีด
def show_knives_window():
    for frame in content_frames:
        frame.pack_forget()
    knife_list_frame.pack(fill="both", expand=True)
    refresh_knife_list(knife_tree)

# ฟังก์ชันชำระเงิน
def checkout_window():
    for frame in content_frames:
        frame.pack_forget()
    checkout_frame.pack(fill="both", expand=True)
    refresh_knife_list(checkout_tree)
    total_price_label.config(text=f"ราคารวมทั้งหมด: {calculate_total_price()} บาท")

# ฟังก์ชันยืนยันการชำระเงิน
def confirm_payment():
    global current_user
    if current_user:
        c.execute("SELECT name, stock, price FROM knives")
        knives = c.fetchall()
        for knife in knives:
            name, stock, price = knife
            total_price = stock * price
            c.execute("INSERT INTO purchase_history (username, knife_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                      (current_user, name, stock, total_price))
        conn.commit()
        messagebox.showinfo("Payment", "ชำระเงินเสร็จสิ้น!")
        c.execute("DELETE FROM knives")  # ลบสินค้าทั้งหมดหลังชำระเงิน
        conn.commit()
        refresh_knife_list(knife_tree)
        refresh_knife_list(checkout_tree)
        total_price_label.config(text="ราคารวมทั้งหมด: 0 บาท")
    else:
        messagebox.showwarning("Error", "กรุณาล็อกอินก่อนทำการชำระเงิน")

# ฟังก์ชันสำหรับเข้าสู่ระบบ
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {username}!")
            global current_user
            current_user = username  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบ
            show_home_window(logged_in=True)  # แสดงหน้าหลัก
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันสำหรับสมัครสมาชิก
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    if username and password:
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Register Success", "สมัครสมาชิกสำเร็จแล้ว! กรุณาล็อกอินเพื่อใช้งาน")
            show_login_window()  # กลับไปหน้าล็อกอิน
        except sqlite3.IntegrityError:
            messagebox.showerror("Register Failed", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันออกจากระบบ
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    logout_button.pack_forget()  # ซ่อนปุ่มออกจากระบบ
    button_frame.pack(pady=10)  # แสดงปุ่มแถวบนสุด
    show_login_window()  # กลับไปหน้าล็อกอิน

# ฟังก์ชันแสดงหน้าล็อกอิน
def show_login_window():
    for frame in content_frames:
        frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# ฟังก์ชันแสดงหน้าสมัครสมาชิก
def show_register_window():
    for frame in content_frames:
        frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

# ฟังก์ชันแสดงหน้าหลัก
def show_home_window(logged_in=False):
    for frame in content_frames:
        frame.pack_forget()
    home_frame.pack(fill="both", expand=True)
    if logged_in:
        button_frame.pack_forget()  # ซ่อนปุ่มแถวบนสุด
        logout_button.pack(side="right", padx=10)  # แสดงปุ่มออกจากระบบ

# GUI หลัก
root = tk.Tk()
root.title("ร้านขายมีด")
root.geometry("800x600")

# ตั้งค่าธีม
style = ttk.Style(root)
# ตรวจสอบว่าไฟล์ธีมมีอยู่จริงหรือไม่
try:
    root.tk.call("source", r"C:\Users\xenos\Documents\pp\proj\test\Azure\azure.tcl")
    style.theme_use("azure-light")
except tk.TclError:
    # ถ้าไม่มีไฟล์ธีม ให้ใช้ธีมเริ่มต้น
    pass

# Frame หลักสำหรับแต่ละเนื้อหา
content_frames = []

# สร้างปุ่มหลักแถวบนสุด
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

home_button = ttk.Button(button_frame, text="หน้าหลักร้านค้า", command=lambda: show_home_window(logged_in=False))
home_button.pack(side="left", padx=10)

show_knives_button = ttk.Button(button_frame, text="แสดงมีดที่มีอยู่", command=show_knives_window)
show_knives_button.pack(side="left", padx=10)

add_knife_button = ttk.Button(button_frame, text="เพิ่มมีด", command=add_knife_window)
add_knife_button.pack(side="left", padx=10)

remove_knife_button = ttk.Button(button_frame, text="แก้ไขมีด", command=remove_knife_window)
remove_knife_button.pack(side="left", padx=10)

checkout_button = ttk.Button(button_frame, text="ชำระเงิน", command=checkout_window)
checkout_button.pack(side="left", padx=10)

# ปุ่มออกจากระบบ (ซ่อนอยู่ในตอนแรก)
logout_button = ttk.Button(root, text="ออกจากระบบ", command=logout)

# หน้าหลักร้านค้า
home_frame = tk.Frame(root)
content_frames.append(home_frame)

home_label = ttk.Label(home_frame, text="ร้านมีดออนไลน์", font=("Arial", 24))
home_label.pack(pady=50)  # ปรับระยะห่าง

welcome_message = ttk.Label(home_frame, text="ยินดีต้อนรับสู่ร้านมีดออนไลน์ของเรา!", font=("Arial", 16))
welcome_message.pack(pady=10)

# หน้าล็อกอิน
login_frame = tk.Frame(root)
content_frames.append(login_frame)

ttk.Label(login_frame, text="เข้าสู่ระบบ", font=("Arial", 24)).pack(pady=10)
ttk.Label(login_frame, text="ชื่อผู้ใช้").pack(pady=5)
username_entry = ttk.Entry(login_frame)
username_entry.pack(pady=5)

ttk.Label(login_frame, text="รหัสผ่าน").pack(pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

login_button = ttk.Button(login_frame, text="เข้าสู่ระบบ", command=login)
login_button.pack(pady=10)

ttk.Button(login_frame, text="สมัครสมาชิก", command=show_register_window).pack(pady=5)

# หน้าสมัครสมาชิก
register_frame = tk.Frame(root)
content_frames.append(register_frame)

ttk.Label(register_frame, text="สมัครสมาชิก", font=("Arial", 24)).pack(pady=10)
ttk.Label(register_frame, text="ชื่อผู้ใช้").pack(pady=5)
reg_username_entry = ttk.Entry(register_frame)
reg_username_entry.pack(pady=5)

ttk.Label(register_frame, text="รหัสผ่าน").pack(pady=5)
reg_password_entry = ttk.Entry(register_frame, show="*")
reg_password_entry.pack(pady=5)

register_button = ttk.Button(register_frame, text="สมัครสมาชิก", command=register)
register_button.pack(pady=10)

ttk.Button(register_frame, text="กลับไปล็อกอิน", command=show_login_window).pack(pady=5)

# ส่วนแสดงมีดที่มีอยู่
knife_list_frame = tk.Frame(root)
content_frames.append(knife_list_frame)

columns = ('Name', 'Stock', 'Price', 'TotalPricePerType')
knife_tree = ttk.Treeview(knife_list_frame, columns=columns, show="headings", height=10)
knife_tree.heading('Name', text="ชื่อมีด")
knife_tree.heading('Stock', text="จำนวน")
knife_tree.heading('Price', text="ราคาต่อชิ้น")
knife_tree.heading('TotalPricePerType', text="ราคารวมต่อชนิด")
knife_tree.pack(fill="both", expand=True)

# Scrollbar สำหรับตารางมีด
scrollbar = ttk.Scrollbar(knife_list_frame, orient="vertical", command=knife_tree.yview)
knife_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ส่วนเพิ่มมีด
add_knife_frame = tk.Frame(root)
content_frames.append(add_knife_frame)

ttk.Label(add_knife_frame, text="ชื่อมีด").pack(pady=5)
knife_name_entry = ttk.Entry(add_knife_frame)
knife_name_entry.pack(pady=5)

ttk.Label(add_knife_frame, text="จำนวน").pack(pady=5)
knife_stock_entry = ttk.Entry(add_knife_frame)
knife_stock_entry.pack(pady=5)

ttk.Label(add_knife_frame, text="ราคาต่อชิ้น").pack(pady=5)
knife_price_entry = ttk.Entry(add_knife_frame)
knife_price_entry.pack(pady=5)

confirm_add_button = ttk.Button(add_knife_frame, text="ยืนยันการเพิ่ม", command=add_knife)
confirm_add_button.pack(pady=10)

# ส่วนแก้ไขมีด
remove_knife_frame = tk.Frame(root)
content_frames.append(remove_knife_frame)

remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=columns, show="headings", height=10)
remove_knife_tree.heading('Name', text="ชื่อมีด")
remove_knife_tree.heading('Stock', text="จำนวน")
remove_knife_tree.heading('Price', text="ราคาต่อชิ้น")
remove_knife_tree.heading('TotalPricePerType', text="ราคารวมต่อชนิด")
remove_knife_tree.pack(fill="both", expand=True)

# Scrollbar สำหรับตารางการลบ
remove_scrollbar = ttk.Scrollbar(remove_knife_frame, orient="vertical", command=remove_knife_tree.yview)
remove_knife_tree.configure(yscroll=remove_scrollbar.set)
remove_scrollbar.pack(side="right", fill="y")

# ปุ่มเพิ่มจำนวน
increase_button = ttk.Button(remove_knife_frame, text="เพิ่มจำนวน", command=increase_stock)
increase_button.pack(pady=5)

# ปุ่มลดจำนวน
decrease_button = ttk.Button(remove_knife_frame, text="ลดจำนวน", command=decrease_stock)
decrease_button.pack(pady=5)

# ปุ่มลบมีด
delete_button = ttk.Button(remove_knife_frame, text="ลบมีด", command=delete_knife)
delete_button.pack(pady=5)

# ส่วนการชำระเงิน
checkout_frame = tk.Frame(root)
content_frames.append(checkout_frame)

checkout_tree = ttk.Treeview(checkout_frame, columns=columns, show="headings", height=10)
checkout_tree.heading('Name', text="ชื่อมีด")
checkout_tree.heading('Stock', text="จำนวน")
checkout_tree.heading('Price', text="ราคาต่อชิ้น")
checkout_tree.heading('TotalPricePerType', text="ราคารวมต่อชนิด")
checkout_tree.pack(fill="both", expand=True)

# Scrollbar สำหรับตารางการชำระเงิน
checkout_scrollbar = ttk.Scrollbar(checkout_frame, orient="vertical", command=checkout_tree.yview)
checkout_tree.configure(yscroll=checkout_scrollbar.set)
checkout_scrollbar.pack(side="right", fill="y")

# ป้ายแสดงราคารวม
total_price_label = ttk.Label(checkout_frame, text=f"ราคารวมทั้งหมด: {calculate_total_price()} บาท")
total_price_label.pack(pady=10)

# ปุ่มยืนยันการชำระเงิน
confirm_payment_button = ttk.Button(checkout_frame, text="ยืนยันการชำระเงิน", command=confirm_payment)
confirm_payment_button.pack(pady=10)

# เริ่มต้นด้วยการแสดงหน้าล็อกอิน
show_login_window()

# เริ่ม GUI หลัก
root.mainloop()

# ปิดการเชื่อมต่อกับฐานข้อมูล
conn.close()
