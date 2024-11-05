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

def hide_all_frames():
    for frame in content_frames:
        frame.pack_forget()
    buy_knife_frame.pack_forget() 

def show_home_window():
    hide_all_frames()  # ซ่อนทุกฟังก์ชัน
    home_frame.pack(fill="both", expand=True)

def show_add_knife_window():
    hide_all_frames()  # ซ่อนทุกฟังก์ชัน
    add_knife_frame.pack(fill="both", expand=True)

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
            button_frame.pack(pady=10)  # แสดงปุ่มแถวบนสุดเมื่อเข้าสู่ระบบสำเร็จ
            show_home_window(logged_in=True)  # แสดงหน้าหลัก
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันสำหรับสมัครสมาชิก
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()  # รับค่าจากช่องยืนยันรหัสผ่าน

    if username and password and confirm_password:
        if password == confirm_password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Register Success", "สมัครสมาชิกสำเร็จแล้ว! กรุณาล็อกอินเพื่อใช้งาน")
                show_login_window()  # กลับไปหน้าล็อกอิน
            except sqlite3.IntegrityError:
                messagebox.showerror("Register Failed", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
        else:
            messagebox.showerror("Password Mismatch", "รหัสผ่านไม่ตรงกัน กรุณาลองใหม่")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันออกจากระบบ
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    logout_button.pack_forget()  # ซ่อนปุ่มออกจากระบบ
    button_frame.pack_forget()  # ซ่อนปุ่มแถวบนสุด
    show_login_window()  # กลับไปหน้าล็อกอิน

# ฟังก์ชันแสดงหน้าล็อกอิน
def show_login_window():
    button_frame.pack_forget()  # ซ่อนปุ่มแถวบนสุดเมื่ออยู่ในหน้าล็อกอิน
    for frame in content_frames:
        frame.pack_forget()
   # welcome_label = ttk.Label(login_frame, text="ยินดีต้อนรับสู่ร้านตะดอบจอบเสียม", font=("Arial", 16))
    #welcome_label.pack(pady=0)  # เพิ่มข้อความต้อนรับในหน้าล็อกอิน
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
    #store_name_label = ttk.Label(home_frame, text="ร้านตะดอบจอบเสียม", font=("Arial", 20))
    #store_name_label.pack(pady=20)  # เพิ่มชื่อร้านตรงกลางหน้าหลัก
    home_frame.pack(fill="both", expand=True)


# ฟังก์ชันออกจากโปรแกรม
def exit_program():
    conn.close()
    root.quit()

# ฟังก์ชันแสดงหน้าต่างซื้อมีด
def buy_knife_window():
    hide_all_frames()  # ซ่อนฟังก์ชันซื้อมีดเมื่อกดปุ่มอื่น
    buy_knife_frame.pack(fill="both", expand=True)  # แสดงฟังก์ชันซื้อมีด
    refresh_knife_list(buy_knife_tree)  # รีเฟรชรายการมีด

# ฟังก์ชันสำหรับการซื้อมีด
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

# ฟังก์ชันรีเฟรชรายการมีดใน Treeview สำหรับการซื้อมีด
def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price FROM knives")
    knives = c.fetchall()
    for name, stock, price in knives:
        treeview.insert("", "end", values=(name, stock, price))

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Knife Shop Management")
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


# สร้าง Frame สำหรับหน้าเนื้อหาต่าง ๆ
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
home_frame = ttk.Frame(root)
add_knife_frame = ttk.Frame(root)
remove_knife_frame = ttk.Frame(root)
knife_list_frame = ttk.Frame(root)
checkout_frame = ttk.Frame(root)

content_frames = [login_frame, register_frame, home_frame, add_knife_frame, remove_knife_frame, knife_list_frame, checkout_frame]

# สร้างแถบปุ่มด้านบน
button_frame = ttk.Frame(root)
button_frame.pack_forget()  # เริ่มต้นซ่อนแถบปุ่ม

home_button = ttk.Button(button_frame, text="หน้าหลัก", command=show_home_window)
home_button.pack(side="left")

add_knife_button = ttk.Button(button_frame, text="เพิ่มมีด", command=add_knife_window)
add_knife_button.pack(side="left")

remove_knife_button = ttk.Button(button_frame, text="แก้ไข", command=remove_knife_window)
remove_knife_button.pack(side="left")

knives_button = ttk.Button(button_frame, text="รายการมีด", command=show_knives_window)
knives_button.pack(side="left")

buy_knife_button = ttk.Button(button_frame, text="ซื้อมีด", command=buy_knife_window)
buy_knife_button.pack(side="left")

checkout_button = ttk.Button(button_frame, text="ชำระเงิน", command=checkout_window)
checkout_button.pack(side="left")

logout_button = ttk.Button(button_frame, text="ออกจากระบบ", command=logout)
logout_button.pack(side="left")

welcome_label = ttk.Label(login_frame, text="ยินดีต้อนรับสู่ร้านตะดอบจอบเสียม", font=("Arial", 16))
welcome_label.pack(pady=(20, 10), anchor="n")  # ใช้ anchor="n" เพื่อจัดให้อยู่ด้านบนสุด

login_title_label = ttk.Label(login_frame, text="Login", font=("Arial", 16))
login_title_label.pack(pady=5)

# ฟอร์มเข้าสู่ระบบ
username_label = ttk.Label(login_frame, text="Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(login_frame)
username_entry.pack(pady=10)

password_label = ttk.Label(login_frame, text="Password:")
password_label.pack(pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=10)

  # สร้างเฟรมแยกสำหรับจัดเรียงปุ่ม Register และ Login ให้อยู่ในแถวเดียวกัน
button_row_frame = ttk.Frame(login_frame)
button_row_frame.pack(pady=10)
    
register_button = ttk.Button(button_row_frame, text="Register", command=show_register_window)
register_button.pack(side="left", padx=5)  # ปุ่ม Register อยู่ทางซ้าย

login_button = ttk.Button(button_row_frame, text="Login", command=login)
login_button.pack(side="left", padx=5)  # ปุ่ม Login อยู่ทางขวา

#login_button = ttk.Button(login_frame, text="Login", command=login)
#login_button.pack(pady=10)

#register_button = ttk.Button(login_frame, text="Register", command=show_register_window)
#register_button.pack(pady=10)
welcome_label = ttk.Label(register_frame, text="ยินดีต้อนรับสู่ร้านตะดอบจอบเสียม", font=("Arial", 16))
welcome_label.pack(pady=(20, 10), anchor="n")  # ใช้ anchor="n" เพื่อจัดให้อยู่ด้านบนสุด

Register_title_label = ttk.Label(register_frame, text="Register", font=("Arial", 16))
Register_title_label.pack(pady=5)

# ฟอร์มสมัครสมาชิก
reg_username_label = ttk.Label(register_frame, text="Username:")
reg_username_label.pack(pady=10)
reg_username_entry = ttk.Entry(register_frame)
reg_username_entry.pack(pady=10)

reg_password_label = ttk.Label(register_frame, text="Password:")
reg_password_label.pack(pady=10)
reg_password_entry = ttk.Entry(register_frame, show="*")
reg_password_entry.pack(pady=10)

# เพิ่มช่องกรอก Confirm Password
reg_confirm_password_label = ttk.Label(register_frame, text="Confirm Password:")
reg_confirm_password_label.pack(pady=10)
reg_confirm_password_entry = ttk.Entry(register_frame, show="*")
reg_confirm_password_entry.pack(pady=10)


# สร้างเฟรมแยกสำหรับจัดเรียงปุ่ม Back to Login และ Register ให้อยู่ในแถวเดียวกัน
button_row_frame = ttk.Frame(register_frame)
button_row_frame.pack(pady=10)

    # จัดปุ่มให้อยู่ในเฟรมเดียวกันเหมือนหน้าเข้าสู่ระบบ
login_redirect_button = ttk.Button(button_row_frame, text="Back to Login", command=show_login_window)
login_redirect_button.pack(side="left", padx=10)

reg_button = ttk.Button(button_row_frame, text="Register", command=register)
reg_button.pack(side="left", padx=10)

buy_knife_frame = ttk.Frame(root)

# ตารางมีดสำหรับการซื้อ
buy_knife_tree = ttk.Treeview(buy_knife_frame, columns=("Name", "Stock", "Price"), show="headings")
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

# ฟอร์มลบ/ปรับจำนวนมีด
remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
remove_knife_tree.heading("Name", text="ชื่อมีด")
remove_knife_tree.heading("Stock", text="จำนวนในสต็อก")
remove_knife_tree.heading("Price", text="ราคา")
remove_knife_tree.heading("Total Price", text="ราคารวม")
remove_knife_tree.pack(pady=10)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
remove_knife_tree.column("Name", anchor='center')
remove_knife_tree.column("Stock", anchor='center')
remove_knife_tree.column("Price", anchor='center')

increase_stock_buttonn = ttk.Frame(remove_knife_frame)
increase_stock_buttonn.pack(side = "bottom",pady=10)

increase_stock_button = ttk.Button(remove_knife_frame, text="เพิ่มจำนวน", command=increase_stock)
increase_stock_button.pack( side = "bottom",padx=10)

decrease_stock_button = ttk.Button(remove_knife_frame, text="ลดจำนวน", command=decrease_stock)
decrease_stock_button.pack( side = "bottom",padx=10)

delete_knife_button = ttk.Button(remove_knife_frame, text="ลบมีด", command=delete_knife)
delete_knife_button.pack( side = "bottom",padx=10)

button_frame.pack(side="bottom", fill="x")

# ตารางมีด
knife_tree = ttk.Treeview(knife_list_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
knife_tree.heading("Name", text="ชื่อมีด")
knife_tree.heading("Stock", text="จำนวนในสต็อก")
knife_tree.heading("Price", text="ราคา")
knife_tree.heading("Total Price", text="ราคารวม")
knife_tree.pack(pady=10)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
knife_tree.column("Name", anchor='center')
knife_tree.column("Stock", anchor='center')
knife_tree.column("Price", anchor='center')
knife_tree.column("Total Price", anchor='center')

# หน้าชำระเงิน
checkout_tree = ttk.Treeview(checkout_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
checkout_tree.heading("Name", text="ชื่อมีด")
checkout_tree.heading("Stock", text="จำนวนในสต็อก")
checkout_tree.heading("Price", text="ราคา")
checkout_tree.heading("Total Price", text="ราคารวม")
checkout_tree.pack(pady=10)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
checkout_tree.column("Name", anchor='center')
checkout_tree.column("Stock", anchor='center')
checkout_tree.column("Price", anchor='center')
checkout_tree.column("Total Price", anchor='center')

total_price_label = ttk.Label(checkout_frame, text="ราคารวมทั้งหมด: 0 บาท")
total_price_label.pack(pady=10)

confirm_payment_button = ttk.Button(checkout_frame, text="ยืนยันชำระเงิน", command=confirm_payment)
confirm_payment_button.pack(pady=10)

# เริ่มต้นโปรแกรมที่หน้าล็อกอิน
show_login_window()

root.mainloop()
