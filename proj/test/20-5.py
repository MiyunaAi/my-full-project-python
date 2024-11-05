import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import os

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
        stock INTEGER,
        image_path TEXT
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

def hide_all_frames():
    for frame in content_frames:
        frame.pack_forget()
    buy_knife_frame.pack_forget() 

def show_home_window():
    hide_all_frames()
    home_frame.pack(fill="both", expand=True)

def show_add_knife_window():
    hide_all_frames()
    add_knife_frame.pack(fill="both", expand=True)

def calculate_total_price():
    c.execute("SELECT SUM(price * stock) FROM knives")
    total_price = c.fetchone()[0]
    return total_price if total_price else 0

def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price, image_path FROM knives")
    knives = c.fetchall()
    for name, stock, price, image_path in knives:
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((50, 50), Image.ANTIALIAS)  # Resize image
            photo = ImageTk.PhotoImage(img)
            treeview.insert("", "end", values=(name, stock, price, photo))
            treeview.image = photo  # Keep a reference to avoid garbage collection

def add_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    add_knife_frame.pack(fill="both", expand=True)

def add_knife():
    name = knife_name_entry.get()
    stock = knife_stock_entry.get()
    price = knife_price_entry.get()
    if name and stock.isdigit() and price.isdigit():
        stock = int(stock)
        price = int(price)
        if stock > 0 and price > 0:
            image_path = image_file_path  # Use the global image path
            c.execute("INSERT INTO knives (name, stock, price, image_path) VALUES (?, ?, ?, ?)", (name, stock, price, image_path))
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

def remove_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    remove_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(remove_knife_tree)

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

def delete_knife():
    selected_item = remove_knife_tree.selection()
    if selected_item:
        name = remove_knife_tree.item(selected_item)['values'][0]
        c.execute("DELETE FROM knives WHERE name = ?", (name,))
        conn.commit()
        refresh_knife_list(remove_knife_tree)
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการลบ")

def show_knives_window():
    for frame in content_frames:
        frame.pack_forget()
    knife_list_frame.pack(fill="both", expand=True)
    refresh_knife_list(knife_tree)

def checkout_window():
    for frame in content_frames:
        frame.pack_forget()
    checkout_frame.pack(fill="both", expand=True)
    refresh_knife_list(checkout_tree)
    total_price_label.config(text=f"ราคารวมทั้งหมด: {calculate_total_price()} บาท")

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

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {username}!")
            global current_user
            current_user = username
            button_frame.pack(pady=10)
            show_home_window(logged_in=True)
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()

    if username and password and confirm_password:
        if password == confirm_password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Register Success", "สมัครสมาชิกสำเร็จแล้ว! กรุณาล็อกอินเพื่อใช้งาน")
                show_login_window()
            except sqlite3.IntegrityError:
                messagebox.showerror("Register Failed", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
        else:
            messagebox.showerror("Password Mismatch", "รหัสผ่านไม่ตรงกัน กรุณาลองใหม่")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    logout_button.pack_forget()
    button_frame.pack_forget()
    show_login_window()

def show_login_window():
    button_frame.pack_forget()
    for frame in content_frames:
        frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def show_register_window():
    for frame in content_frames:
        frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

def show_home_window(logged_in=False):
    for frame in content_frames:
        frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

def exit_program():
    conn.close()
    root.quit()

def buy_knife_window():
    hide_all_frames()
    buy_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(buy_knife_tree)

def purchase_knife():
    selected_item = buy_knife_tree.selection()
    if selected_item:
        name = buy_knife_tree.item(selected_item)['values'][0]
        quantity = quantity_entry.get()
        if quantity.isdigit() and int(quantity) > 0:
            quantity = int(quantity)
            c.execute("SELECT stock, price FROM knives WHERE name = ?", (name,))
            result = c.fetchone()
            if result:
                stock, price = result
                if quantity <= stock:
                    total_price = quantity * price
                    c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock - quantity, name))
                    c.execute("INSERT INTO purchase_history (username, knife_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                              (current_user, name, quantity, total_price))
                    conn.commit()
                    messagebox.showinfo("Success", f"ซื้อ {quantity} {name} สำเร็จ! ราคารวม {total_price} บาท")
                    refresh_knife_list(buy_knife_tree)
                else:
                    messagebox.showwarning("Warning", "จำนวนมีดในสต็อกไม่เพียงพอ")
            else:
                messagebox.showwarning("Warning", "ไม่พบมีดในฐานข้อมูล")
        else:
            messagebox.showwarning("Invalid input", "กรุณากรอกจำนวนที่ถูกต้อง")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการซื้อ")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Knife Shop Management")
root.geometry("800x600")

# ตั้งค่าธีม
style = ttk.Style(root)

# สร้าง Frame สำหรับหน้าเนื้อหาต่าง ๆ
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
home_frame = ttk.Frame(root)
add_knife_frame = ttk.Frame(root)
remove_knife_frame = ttk.Frame(root)
buy_knife_frame = ttk.Frame(root)

content_frames = [login_frame, register_frame, home_frame, add_knife_frame, remove_knife_frame, buy_knife_frame]

# สร้าง Label สำหรับแสดงภาพ
image_file_path = ""  # ตัวแปร global สำหรับที่อยู่ภาพ
image_label = ttk.Label(add_knife_frame)
image_label.pack(pady=10)

# ปุ่มอัพโหลดภาพ
upload_image_button = ttk.Button(add_knife_frame, text="อัพโหลดภาพมีด", command=lambda: upload_image(image_label))
upload_image_button.pack(pady=10)

# ฟอร์มเพิ่มมีด
knife_name_label = ttk.Label(add_knife_frame, text="ชื่อมีด:")
knife_name_label.pack(pady=10)
knife_name_entry = ttk.Entry(add_knife_frame)
knife_name_entry.pack(pady=10)

knife_stock_label = ttk.Label(add_knife_frame, text="จำนวนมีดในสต็อก:")
knife_stock_label.pack(pady=10)
knife_stock_entry = ttk.Entry(add_knife_frame)
knife_stock_entry.pack(pady=10)

knife_price_label = ttk.Label(add_knife_frame, text="ราคามีด:")
knife_price_label.pack(pady=10)
knife_price_entry = ttk.Entry(add_knife_frame)
knife_price_entry.pack(pady=10)

add_knife_submit_button = ttk.Button(add_knife_frame, text="เพิ่มมีด", command=add_knife)
add_knife_submit_button.pack(pady=10)

# ตารางสำหรับการซื้อมีด
buy_knife_tree = ttk.Treeview(buy_knife_frame, columns=("Name", "Stock", "Price", "Image Path"), show="headings")
buy_knife_tree.heading("Name", text="ชื่อมีด")
buy_knife_tree.heading("Stock", text="จำนวนในสต็อก")
buy_knife_tree.heading("Price", text="ราคา")
buy_knife_tree.pack(pady=10)

# ช่องกรอกจำนวนที่ต้องการซื้อ
quantity_label = ttk.Label(buy_knife_frame, text="จำนวนที่ต้องการซื้อ:")
quantity_label.pack(pady=5)
quantity_entry = ttk.Entry(buy_knife_frame)
quantity_entry.pack(pady=5)

# ปุ่มซื้อ
buy_button = ttk.Button(buy_knife_frame, text="ซื้อ", command=purchase_knife)
buy_button.pack(pady=10)

# ปุ่มย้อนกลับ
back_button = ttk.Button(buy_knife_frame, text="กลับ", command=show_home_window)
back_button.pack(pady=10)

# เริ่มต้นแสดงหน้าล็อกอิน
show_login_window()
root.mainloop()

# ปิดการเชื่อมต่อฐานข้อมูลเมื่อปิดโปรแกรม
conn.close()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import os

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
        stock INTEGER,
        image_path TEXT
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
image_file_path = ""  # ตัวแปรสำหรับเก็บที่อยู่ภาพ

def hide_all_frames():
    for frame in content_frames:
        frame.pack_forget()
    buy_knife_frame.pack_forget() 

def show_home_window():
    hide_all_frames()
    home_frame.pack(fill="both", expand=True)

def calculate_total_price():
    c.execute("SELECT SUM(price * stock) FROM knives")
    total_price = c.fetchone()[0]
    return total_price if total_price else 0

def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price, image_path FROM knives")
    knives = c.fetchall()
    for name, stock, price, image_path in knives:
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((50, 50), Image.ANTIALIAS)  # Resize image
            photo = ImageTk.PhotoImage(img)
            treeview.insert("", "end", values=(name, stock, price, photo))
            treeview.image = photo  # Keep a reference to avoid garbage collection

def add_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    add_knife_frame.pack(fill="both", expand=True)

def add_knife():
    name = knife_name_entry.get()
    stock = knife_stock_entry.get()
    price = knife_price_entry.get()
    if name and stock.isdigit() and price.isdigit():
        stock = int(stock)
        price = int(price)
        if stock > 0 and price > 0:
            image_path = image_file_path  # Use the global image path
            c.execute("INSERT INTO knives (name, stock, price, image_path) VALUES (?, ?, ?, ?)", (name, stock, price, image_path))
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

def remove_knife_window():
    for frame in content_frames:
        frame.pack_forget()
    remove_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(remove_knife_tree)

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

def delete_knife():
    selected_item = remove_knife_tree.selection()
    if selected_item:
        name = remove_knife_tree.item(selected_item)['values'][0]
        c.execute("DELETE FROM knives WHERE name = ?", (name,))
        conn.commit()
        refresh_knife_list(remove_knife_tree)
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกมีดที่ต้องการลบ")

def show_knives_window():
    for frame in content_frames:
        frame.pack_forget()
    knife_list_frame.pack(fill="both", expand=True)
    refresh_knife_list(knife_tree)

def checkout_window():
    for frame in content_frames:
        frame.pack_forget()
    checkout_frame.pack(fill="both", expand=True)
    refresh_knife_list(checkout_tree)
    total_price_label.config(text=f"ราคารวมทั้งหมด: {calculate_total_price()} บาท")

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

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {username}!")
            global current_user
            current_user = username
            button_frame.pack(pady=10)
            show_home_window()
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()

    if username and password and confirm_password:
        if password == confirm_password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Register Success", "สมัครสมาชิกสำเร็จแล้ว! กรุณาล็อกอินเพื่อใช้งาน")
                show_login_window()
            except sqlite3.IntegrityError:
                messagebox.showerror("Register Failed", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
        else:
            messagebox.showerror("Password Mismatch", "รหัสผ่านไม่ตรงกัน กรุณาลองใหม่")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    logout_button.pack_forget()
    button_frame.pack_forget()
    show_login_window()

def show_login_window():
    button_frame.pack_forget()
    for frame in content_frames:
        frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def show_register_window():
    for frame in content_frames:
        frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

def upload_image(label):
    global image_file_path  # ใช้ตัวแปร global
    image_file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if image_file_path:
        img = Image.open(image_file_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img  # เก็บการอ้างอิงเพื่อลดการถูกเก็บกวาดโดย garbage collector

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Knife Shop Management")
root.geometry("800x600")

# ตั้งค่าธีม
style = ttk.Style(root)

# สร้าง Frame สำหรับหน้าเนื้อหาต่าง ๆ
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
home_frame = ttk.Frame(root)
add_knife_frame = ttk.Frame(root)
remove_knife_frame = ttk.Frame(root)
buy_knife_frame = ttk.Frame(root)

content_frames = [login_frame, register_frame, home_frame, add_knife_frame, remove_knife_frame, buy_knife_frame]

# สร้าง Label สำหรับแสดงภาพ
image_label = ttk.Label(add_knife_frame)
image_label.pack(pady=10)

# ปุ่มอัพโหลดภาพ
upload_image_button = ttk.Button(add_knife_frame, text="อัพโหลดภาพมีด", command=lambda: upload_image(image_label))
upload_image_button.pack(pady=10)

# ฟอร์มเพิ่มมีด
knife_name_label = ttk.Label(add_knife_frame, text="ชื่อมีด:")
knife_name_label.pack(pady=10)
knife_name_entry = ttk.Entry(add_knife_frame)
knife_name_entry.pack(pady=10)

knife_stock_label = ttk.Label(add_knife_frame, text="จำนวนมีดในสต็อก:")
knife_stock_label.pack(pady=10)
knife_stock_entry = ttk.Entry(add_knife_frame)
knife_stock_entry.pack(pady=10)

knife_price_label = ttk.Label(add_knife_frame, text="ราคามีด:")
knife_price_label.pack(pady=10)
knife_price_entry = ttk.Entry(add_knife_frame)
knife_price_entry.pack(pady=10)

add_knife_submit_button = ttk.Button(add_knife_frame, text="เพิ่มมีด", command=add_knife)
add_knife_submit_button.pack(pady=10)

# ตารางสำหรับการซื้อมีด
buy_knife_tree = ttk.Treeview(buy_knife_frame, columns=("Name", "Stock", "Price", "Image Path"), show="headings")
buy_knife_tree.heading("Name", text="ชื่อมีด")
buy_knife_tree.heading("Stock", text="จำนวนในสต็อก")
buy_knife_tree.heading("Price", text="ราคา")
buy_knife_tree.pack(pady=10)

# ช่องกรอกจำนวนที่ต้องการซื้อ
quantity_label = ttk.Label(buy_knife_frame, text="จำนวนที่ต้องการซื้อ:")
quantity_label.pack(pady=5)
quantity_entry = ttk.Entry(buy_knife_frame)
quantity_entry.pack(pady=5)

# ปุ่มซื้อ
buy_button = ttk.Button(buy_knife_frame, text="ซื้อ", command=purchase_knife)
buy_button.pack(pady=10)

# ปุ่มย้อนกลับ
back_button = ttk.Button(buy_knife_frame, text="กลับ", command=show_home_window)
back_button.pack(pady=10)

# เริ่มต้นแสดงหน้าล็อกอิน
show_login_window()
root.mainloop()

# ปิดการเชื่อมต่อฐานข้อมูลเมื่อปิดโปรแกรม
conn.close()
