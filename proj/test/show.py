import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect(r'C:\Users\xenos\Documents\datab\knife_shop.db')
c = conn.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')


c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER
    )
''')


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


# เก็บผู้ใช้ที่ล็อกอินจ้า
current_user = None

# คำนวณราคารวมของมีดในกะต้า
def calculate_total_price():
    c.execute("SELECT SUM(price * stock) FROM knives")
    total_price = c.fetchone()[0]
    return total_price if total_price else 0

# รีเฟรช Treeview
def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price FROM knives")
    knives = c.fetchall()
    for name, stock, price in knives:
        total_price_per_type = price * stock
        treeview.insert("", "end", values=(name, stock, price, total_price_per_type))


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
        c.execute("DELETE FROM knives")  
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
            show_home_window(logged_in=True)  # แสดงหน้าหลัก
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# สมัคร
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_password_entry.get()  # รับค่า

    if username and password and confirm_password:
        if password == confirm_password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Register Success", "สมัครสมาชิกสำเร็จแล้ว! กรุณาล็อกอินเพื่อใช้งาน")
                show_login_window()  # กลับ
            except sqlite3.IntegrityError:
                messagebox.showerror("Register Failed", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
        else:
            messagebox.showerror("Password Mismatch", "รหัสผ่านไม่ตรงกัน กรุณาลองใหม่")
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ออก
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "ออกจากระบบเรียบร้อยแล้ว")
    logout_button.pack_forget()  
    button_frame.pack_forget()  
    show_login_window()  

# ล๊อกอินระบบ
def show_login_window():
    button_frame.pack_forget()  # ซ่อนปุ่มแถวบน
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


# ออกด
def exit_program():
    conn.close()
    root.quit()

# เมน
root = tk.Tk()
root.title("Knife Shop Management")
root.geometry("800x600")

# ตีม
style = ttk.Style(root)

try:
    root.tk.call("source", r"C:\Users\xenos\Documents\pp\proj\test\Azure\azure.tcl")
    style.theme_use("azure-light")
except tk.TclError:

    pass


# สร้าเฟม
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
home_frame = ttk.Frame(root)
add_knife_frame = ttk.Frame(root)
remove_knife_frame = ttk.Frame(root)
knife_list_frame = ttk.Frame(root)
checkout_frame = ttk.Frame(root)

content_frames = [login_frame, register_frame, home_frame, add_knife_frame, remove_knife_frame, knife_list_frame, checkout_frame]

# สร้างแถบไอ้สส
button_frame = ttk.Frame(root)
button_frame.pack_forget()  # ซ่อนๆ

home_button = ttk.Button(button_frame, text="หน้าหลัก", command=show_home_window)
home_button.pack(side="left")

add_knife_button = ttk.Button(button_frame, text="เพิ่มมีด", command=add_knife_window)
add_knife_button.pack(side="left")

remove_knife_button = ttk.Button(button_frame, text="แก้ไข", command=remove_knife_window)
remove_knife_button.pack(side="left")

knives_button = ttk.Button(button_frame, text="รายการมีด", command=show_knives_window)
knives_button.pack(side="left")

checkout_button = ttk.Button(button_frame, text="ชำระเงิน", command=checkout_window)
checkout_button.pack(side="left")

logout_button = ttk.Button(button_frame, text="ออกจากระบบ", command=logout)
logout_button.pack(side="left")

welcome_label = ttk.Label(login_frame, text="ยินดีต้อนรับสู่ร้านตะดอบจอบเสียม", font=("Arial", 16))
welcome_label.pack(pady=(20, 10), anchor="n")  # ใช้ anchor="n" เพื่อจัดให้อยู่ด้านบนสุด

login_title_label = ttk.Label(login_frame, text="Login", font=("Arial", 16))
login_title_label.pack(pady=5)


username_label = ttk.Label(login_frame, text="Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(login_frame)
username_entry.pack(pady=10)

password_label = ttk.Label(login_frame, text="Password:")
password_label.pack(pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=10)


button_row_frame = ttk.Frame(login_frame)
button_row_frame.pack(pady=10)
    
register_button = ttk.Button(button_row_frame, text="Register", command=show_register_window)
register_button.pack(side="left", padx=5)  # ปุ่ม Register อยู่ทางซ้าย

login_button = ttk.Button(button_row_frame, text="Login", command=login)
login_button.pack(side="left", padx=5)  # ปุ่ม Login อยู่ทางขวา


welcome_label = ttk.Label(register_frame, text="ยินดีต้อนรับสู่ร้านตะดอบจอบเสียม", font=("Arial", 16))
welcome_label.pack(pady=(20, 10), anchor="n")  # ใช้ anchor="n" เพื่อจัดให้อยู่ด้านบนสุด

Register_title_label = ttk.Label(register_frame, text="Register", font=("Arial", 16))
Register_title_label.pack(pady=5)


reg_username_label = ttk.Label(register_frame, text="Username:")
reg_username_label.pack(pady=10)
reg_username_entry = ttk.Entry(register_frame)
reg_username_entry.pack(pady=10)

reg_password_label = ttk.Label(register_frame, text="Password:")
reg_password_label.pack(pady=10)
reg_password_entry = ttk.Entry(register_frame, show="*")
reg_password_entry.pack(pady=10)


reg_confirm_password_label = ttk.Label(register_frame, text="Confirm Password:")
reg_confirm_password_label.pack(pady=10)
reg_confirm_password_entry = ttk.Entry(register_frame, show="*")
reg_confirm_password_entry.pack(pady=10)



button_row_frame = ttk.Frame(register_frame)
button_row_frame.pack(pady=10)


login_redirect_button = ttk.Button(button_row_frame, text="Back to Login", command=show_login_window)
login_redirect_button.pack(side="left", padx=10)

reg_button = ttk.Button(button_row_frame, text="Register", command=register)
reg_button.pack(side="left", padx=10)


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


remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
remove_knife_tree.heading("Name", text="ชื่อมีด")
remove_knife_tree.heading("Stock", text="จำนวนในสต็อก")
remove_knife_tree.heading("Price", text="ราคา")
remove_knife_tree.heading("Total Price", text="ราคารวม")
remove_knife_tree.pack(pady=10)


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


knife_tree = ttk.Treeview(knife_list_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
knife_tree.heading("Name", text="ชื่อมีด")
knife_tree.heading("Stock", text="จำนวนในสต็อก")
knife_tree.heading("Price", text="ราคา")
knife_tree.heading("Total Price", text="ราคารวม")
knife_tree.pack(pady=10)


knife_tree.column("Name", anchor='center')
knife_tree.column("Stock", anchor='center')
knife_tree.column("Price", anchor='center')
knife_tree.column("Total Price", anchor='center')


checkout_tree = ttk.Treeview(checkout_frame, columns=("Name", "Stock", "Price", "Total Price"), show="headings")
checkout_tree.heading("Name", text="ชื่อมีด")
checkout_tree.heading("Stock", text="จำนวนในสต็อก")
checkout_tree.heading("Price", text="ราคา")
checkout_tree.heading("Total Price", text="ราคารวม")
checkout_tree.pack(pady=10)


checkout_tree.column("Name", anchor='center')
checkout_tree.column("Stock", anchor='center')
checkout_tree.column("Price", anchor='center')
checkout_tree.column("Total Price", anchor='center')

total_price_label = ttk.Label(checkout_frame, text="ราคารวมทั้งหมด: 0 บาท")
total_price_label.pack(pady=10)

confirm_payment_button = ttk.Button(checkout_frame, text="ยืนยันชำระเงิน", command=confirm_payment)
confirm_payment_button.pack(pady=10)


show_login_window()

root.mainloop()
