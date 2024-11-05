import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Toplevel
import sqlite3
import qrcode
from PIL import Image, ImageTk
cart = {}
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


conn.commit()


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
    addk_image_frame.pack(side="left", fill="y")
    addk_image_frame.place(y = 0)

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
    remove_image_frame.pack(side="left", fill="y")
    remove_image_frame.place(y = 0)


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
    listknife_image_frame.pack(side="left", fill="y")
    listknife_image_frame.place(y = 0)

# ฟังก์ชันสำหรับเข้าสู่ระบบ
# ฟังก์ชันสำหรับเข้าสู่ระบบ
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
        if username == "miyuna" and password == "6304":
            messagebox.showinfo("Login Success", "ยินดีต้อนรับ Admin!")
            global current_user
            current_user = username  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบเป็นแอดมิน
            button_frame.pack(pady=10)  # แสดงปุ่มแถวบนสุดเมื่อเข้าสู่ระบบสำเร็จ
            
            # แสดงปุ่มเฉพาะสำหรับ Admin
            add_knife_button.pack(side="left")
            remove_knife_button.pack(side="left")
            knives_button.pack(side="left")

            cart_button.pack(side="left")  # เพิ่มปุ่มตะกร้า
            logout_button.pack(side="left")  # แสดงปุ่มออกจากระบบ
            
            show_home_window(logged_in=True)  # แสดงหน้าหลักสำหรับ Admin
        else:
            # ตรวจสอบการเข้าสู่ระบบของผู้ใช้ปกติ
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
            if user:
                messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {username}!")
                current_user = username  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบเป็นผู้ใช้ปกติ
                button_frame.pack(pady=10)  # แสดงปุ่มแถวบนสุดเมื่อเข้าสู่ระบบสำเร็จ

                # ซ่อนปุ่มสำหรับผู้ใช้ปกติ
                remove_knife_button.pack_forget()
                add_knife_button.pack_forget()
                knives_button.pack_forget()

                show_home_window(logged_in=True)  # แสดงหน้าหลักสำหรับผู้ใช้ปกติ
                logout_button.pack(side="left")  # แสดงปุ่มออกจากระบบเมื่อเข้าสู่ระบบสำเร็จ
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

def show_admin_buttons():
    # ซ่อนปุ่มแถบด้านบนทั้งหมดก่อน
    for widget in button_frame.winfo_children():
        widget.pack_forget()

    # แสดงเฉพาะปุ่มสำหรับแอดมิน
    home_button.pack(side="left")
    add_knife_button.pack(side="left")
    remove_knife_button.pack(side="left")
    knives_button.pack(side="left")
    logout_button.pack(side="left")
    button_frame.pack(pady=10)

def show_user_buttons():
    # ซ่อนปุ่มแถบด้านบนทั้งหมดก่อน
    for widget in button_frame.winfo_children():
        widget.pack_forget()

    # แสดงเฉพาะปุ่มสำหรับผู้ใช้ทั่วไป
    home_button.pack(side="left")
    knives_button.pack(side="left")
    sell_button.pack(side="left")
    cart_button.pack(side="left")
    logout_button.pack(side="left")

    button_frame.pack(pady=10)


# ฟังก์ชันแสดงหน้าล็อกอิน
def show_login_window():
    for frame in content_frames:
        frame.pack_forget()

    # สร้างเฟรมซ้ายและขวาสำหรับแบ่งครึ่งจอ
       # แสดงรูปภาพทางฝั่งซ้าย
    left_frame.pack(side="left", fill="both", expand=True)
    # แสดง UI ล็อกอินทางฝั่งขวา
    right_frame.pack(side="right", fill="both", expand=True)

    button_frame.pack_forget()
    username_entry.focus()
# ฟังก์ชันแสดงหน้าสมัครสมาชิก
def show_register_window():
    for frame in content_frames:
        frame.pack_forget()
    #register_frame.pack(fill="both", expand=True)
    leftt_frame.pack(side="left", fill="both", expand=True)

    rightt_frame.pack(side="right", fill="both", expand=True)

    # แสดงรูปภาพทางฝั่งซ้าย
    button_frame.pack_forget()
# ฟังก์ชันแสดงหน้าหลัก
def show_home_window(logged_in=False):
    for frame in content_frames:
        frame.pack_forget()
    
    home_frame.pack(fill="both", expand=True)

    # โหลดรูปภาพ
    image = Image.open(r"C:\Users\xenos\Pictures\gif\ff.png")  # ใส่พาธของรูปภาพที่ต้องการ
    image = image.resize((1600, 700), Image.LANCZOS)  # ปรับขนาดรูปภาพ
    bg_image = ImageTk.PhotoImage(image)

    # เพิ่ม Label สำหรับรูปภาพ
    image_label = tk.Label(home_frame, image=bg_image)
    image_label.image = bg_image  # จำเป็นต้องเก็บอ้างอิงเพื่อไม่ให้ถูกเก็บใน garbage collection
    image_label.pack(pady=20)  # เพิ่มระยะห่างด้านบน
    refresh_knife_list(sell_product_tree)
    # อาจเพิ่มข้อความอื่น ๆ ที่ต้องการแสดงในหน้าหลักได้ที่นี่

# ฟังก์ชันสำหรับแสดงหน้าขายสินค้า
def sell_product_window():
    for frame in content_frames:
        frame.pack_forget()
            # วางเฟรมซ้าย ขวา และตรงกลาง
    bgsell_image_frame.pack(side="left", fill="y")
    bgsell_image_frame.place(y = 0)
    left_image_frame.pack(side="left", fill="y")
    left_image_frame.place(y = 0)
    right_image_frame.pack(side="right", fill="y")
    right_image_frame.place(x =1130,y = 0)
    sell_product_frame.pack(fill="both", expand=True)
    
    refresh_knife_list(sell_product_tree)


# ฟังก์ชันซื้อสินค้า
def purchase_product():
    cart = {}
    selected_item = sell_product_tree.selection()
    if selected_item:
        name = sell_product_tree.item(selected_item)['values'][0]
        stock = int(sell_product_tree.item(selected_item)['values'][1])
        price = int(sell_product_tree.item(selected_item)['values'][2])
        
        quantity = quantity_entry.get()
        if quantity.isdigit():
            quantity = int(quantity)
            if 0 < quantity <= stock:
                total_price = quantity * price
                c.execute("UPDATE knives SET stock = stock - ? WHERE name = ?", (quantity, name))
                c.execute("INSERT INTO purchase_history (username, knife_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                          (current_user, name, quantity, total_price))
                conn.commit()
                messagebox.showinfo("Success", f"ซื้อสินค้า {name} จำนวน {quantity} ชิ้น เรียบร้อยแล้ว!")
                refresh_knife_list(sell_product_tree)  # รีเฟรชรายการสินค้า
            else:
                messagebox.showwarning("Invalid quantity", "หมดอิสัส")
        else:
            messagebox.showwarning("Invalid input", "กรุณากรอกจำนวนสินค้าเป็นตัวเลขที่ถูกต้อง")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกสินค้าที่ต้องการซื้อ")

# ฟังก์ชันรีเฟรชรายการสินค้าสำหรับขาย
def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock, price FROM knives")
    knives = c.fetchall()
    for name, stock, price in knives:
        treeview.insert("", "end", values=(name, stock, price))


def add_to_cart():
    selected_item = sell_product_tree.selection()
    if selected_item:
        name = sell_product_tree.item(selected_item)['values'][0]
        stock = int(sell_product_tree.item(selected_item)['values'][1])
        quantity = quantity_entry.get()

        if quantity.isdigit():
            quantity = int(quantity)
            if 0 < quantity <= stock:
                if name in cart:
                    cart[name] += quantity
                else:
                    cart[name] = quantity
                messagebox.showinfo("ตะกร้าสินค้า", f"เพิ่ม {name} จำนวน {quantity} ชิ้นลงในตะกร้าแล้ว!")
            else:
                messagebox.showwarning("Invalid quantity", "จำนวนสินค้าไม่เพียงพอ")
        else:
            messagebox.showwarning("Invalid input", "กรุณากรอกจำนวนสินค้าเป็นตัวเลขที่ถูกต้อง")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกสินค้าที่ต้องการเพิ่มลงตะกร้า")


def cart_window():
    for frame in content_frames:
        frame.pack_forget()
    cart_frame.pack(fill="both", expand=True)
    # แสดงรายการสินค้าในตะกร้า
    cart_tree.delete(*cart_tree.get_children())  # ลบข้อมูลเดิม
    total = 0

    for name, qty in cart.items():
        c.execute("SELECT price FROM knives WHERE name = ?", (name,))
        price = c.fetchone()[0]
        total_price = qty * price
        total += total_price
        cart_tree.insert("", "end", values=(name, qty, price, total_price))

    total_label.config(text=f"ราคารวม: {total} บาท")
    cart_image_frame.pack(side="left", fill="y")
    cart_image_frame.place(y = 0)


def refresh_cart_list(treeview):
    treeview.delete(*treeview.get_children())
    total = 0
    for name, quantity in cart.items():
        c.execute("SELECT price FROM knives WHERE name = ?", (name,))
        price = c.fetchone()[0]
        total_price = price * quantity
        total += total_price
        treeview.insert("", "end", values=(name, quantity, price, total_price))
    

def increase_cart_item():
    selected_item = cart_tree.selection()
    if selected_item:
        name = cart_tree.item(selected_item)['values'][0]
        cart[name] += 1
        refresh_cart_list(cart_tree)

def decrease_cart_item():
    selected_item = cart_tree.selection()
    if selected_item:
        name = cart_tree.item(selected_item)['values'][0]
        if cart[name] > 1:
            cart[name] -= 1
        else:
            del cart[name]
        refresh_cart_list(cart_tree)

from datetime import datetime

def save_transaction_history(username, total_amount):
    transaction_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        c.execute(
            "INSERT INTO transaction_history (username, total_amount, transaction_time) VALUES (?, ?, ?)",
            (username, total_amount, transaction_time)
        )
        conn.commit()  # บันทึกข้อมูลลงฐานข้อมูล
        messagebox.showinfo("สำเร็จ", "บันทึกประวัติการทำรายการเรียบร้อยแล้ว!")
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกข้อมูลได้: {e}")



def confirm_order():
    global current_user
    if not current_user:
        messagebox.showwarning("Error", "กรุณาล็อกอินก่อนทำการสั่งซื้อ")
        return

    if not cart:
        messagebox.showwarning("Error", "ไม่มีสินค้าในตะกร้า")
        return

    total_price = 0
    for name, qty in cart.items():
        c.execute("SELECT stock, price FROM knives WHERE name = ?", (name,))
        stock, price = c.fetchone()
        if qty > stock:
            messagebox.showerror("Error", f"สินค้า {name} มีจำนวนไม่เพียงพอ")
            return
        total_price += qty * price
        c.execute("UPDATE knives SET stock = stock - ? WHERE name = ?", (qty, name))

    for name, qty in cart.items():
        total_item_price = qty * price
        c.execute("INSERT INTO purchase_history (username, knife_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                  (current_user, name, qty, total_item_price))



    conn.commit()

    # แสดงข้อความยืนยันการสั่งซื้อ
    messagebox.showinfo("Order Confirmed", f"กรุณาชำระเงิน ผ่าน Qr code  ราคารวม {total_price} บาท")
    # แสดงป๊อปอัปบิลรายการ
    show_order_bill_popup(total_price)
    show_image_popup()

    cart.clear()  # ล้างตะกร้า 
    cart_window()  # อัปเดตรายการตะกร้าใหม่

def show_order_bill_popup(total_price):
    # สร้างหน้าต่างป๊อปอัปใหม่
    bill_window = tk.Toplevel(root)
    bill_window.title("บิลรายการสั่งซื้อ")
    bill_window.geometry("400x600")  # ปรับขนาดได้ตามต้องการ

    frame = tk.Frame(bill_window)
    frame.pack(side=tk.TOP, fill=tk.X)

    # โหลดรูปภาพพื้นหลังและแสดง
    background_image_path = r"C:\Users\xenos\Pictures\gif\slp.png"  # ระบุพาธของรูปพื้นหลัง
    bg_image = Image.open(background_image_path)
    bg_image = bg_image.resize((400, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # ใส่รูปพื้นหลังในหน้าต่างป๊อปอัป
    bg_label = tk.Label(bill_window, image=bg_photo)
    bg_label.image = bg_photo  # เก็บอ้างอิงไว้
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # แสดงบิลรายการสินค้าบนรูปพื้นหลัง
    bill_text = "รายการสั่งซื้อ\n"
    bill_text += "-" * 30 + "\n"
       # แสดงชื่อสินค้า จำนวน ราคาต่อชิ้น และราคารวมสำหรับแต่ละสินค้าใน cart
    for name, qty in cart.items():
        c.execute("SELECT price FROM knives WHERE name = ?", (name,))
        price = c.fetchone()[0]
        total_item_price = qty * price
        bill_text += f"{name} x {qty} ชิ้น - ราคา/ชิ้น: {price} บาท, รวม: {total_item_price} บาท\n"

    bill_text += "-" * 30 + "\n"
    bill_text += f"ราคารวมทั้งหมด: {total_price} บาท"

    # เพิ่มป้ายข้อความบิลรายการสั่งซื้อบนหน้าต่างป๊อปอัป
    bill_label = tk.Label(bill_window, text=bill_text, font=("Arial", 10), bg="white", fg="black", justify="center")
    bill_label.place(x=20, y=1)
    bill_label.pack(pady=(10, 0))

def show_image_popup():
    # สร้างหน้าต่าง Toplevel ใหม่
    image_window = Toplevel(root)
    image_window.title("ภาพสินค้า")

    # โหลดและแสดงภาพ
    img = Image.open(r'C:\Users\xenos\Pictures\gif\ppt.png')
    img = img.resize((400, 400), Image.LANCZOS)  # ปรับขนาดภาพตามต้องการ
    img_photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(image_window, image=img_photo)
    img_label.image = img_photo  # เก็บอ้างอิงเพื่อป้องกัน Garbage Collection
    img_label.pack()


# ฟังก์ชันออกจากโปรแกรม
def exit_program():
    conn.close()
    root.quit()

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Knife Shop Management")
root.geometry("1920x1080")
    # ขนาดของหน้าต่าง




# ตั้งค่าธีม
style = ttk.Style(root)
# ตรวจสอบว่าไฟล์ธีมมีอยู่จริงหรือไม่
try:
    root.tk.call("source", r"C:\Users\xenos\Documents\pp\proj\test\ggwp\theme2\Forest-ttk-theme-master\forest-light.tcl")
    style.theme_use("forest-light")
except tk.TclError:
    # ถ้าไม่มีไฟล์ธีม ให้ใช้ธีมเริ่มต้น
    pass

# สร้าง Frame สำหรับหน้าเนื้อหาต่าง ๆ
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
left_frame = tk.Frame(root, width=960, height=1080)
right_frame = tk.Frame(root, width=960, height=1080)
leftt_frame = tk.Frame(root, width=960, height=1080)
rightt_frame = tk.Frame(root, width=960, height=1080)
home_frame = ttk.Frame(root)
add_knife_frame = ttk.Frame(root)
addk_image_frame = ttk.Frame(add_knife_frame,width=200,height=500)
remove_knife_frame = ttk.Frame(root)
remove_image_frame = ttk.Frame(remove_knife_frame,width=200,height=500)
knife_list_frame = ttk.Frame(root)
listknife_image_frame = ttk.Frame(knife_list_frame,width=200,height=500)
checkout_frame = ttk.Frame(root)
sell_product_frame = ttk.Frame(root)
left_image_frame = tk.Frame(sell_product_frame, width=200, height=500)
right_image_frame = tk.Frame(sell_product_frame, width=200, height=500)
bgsell_image_frame = tk.Frame(sell_product_frame, width=200, height=500)
cart_frame = ttk.Frame(root)
cart_image_frame = ttk.Frame(cart_frame,width=200,height=500)
history_frame = ttk.Frame(root)
content_frames = [login_frame,left_frame,right_frame,leftt_frame,rightt_frame, register_frame, home_frame, add_knife_frame,addk_image_frame, remove_knife_frame,remove_image_frame, knife_list_frame,listknife_image_frame, checkout_frame,sell_product_frame,left_image_frame,right_image_frame,bgsell_image_frame,cart_frame,cart_image_frame,history_frame ]

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

sell_button = ttk.Button(button_frame, text="ขายมีด", command=sell_product_window)
sell_button.pack(side="left")

cart_button = ttk.Button(button_frame, text="ตะกร้า", command=cart_window)
cart_button.pack(side="left")

logout_button = ttk.Button(button_frame, text="ออกจากระบบ", command=logout)
logout_button.pack(side="left")



# ฟอร์มเข้าสู่ระบบ
image = Image.open(r"C:\Users\xenos\Pictures\gif\vvs.jpg")  # ใส่พาธของรูปภาพที่ต้องการ
image = image.resize((800, 600), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(image)

image_label = tk.Label(left_frame, image=bg_image)
image_label.image = bg_image
image_label.pack(fill="both", expand=True)


                                                                                                                    
welcome_label = ttk.Label(right_frame, text="", font=("Arial", 20))
welcome_label.pack(pady=100)

login_title_label = ttk.Label(right_frame, text="Login", font=("Arial", 50))
login_title_label.pack(pady=20,padx=200)

# ฟอร์มเข้าสู่ระบบ
username_label = ttk.Label(right_frame, text="Username",font=("Arial", 15))
username_label.pack(pady=10)
username_entry = ttk.Entry(right_frame,font=("Arial", 15))
username_entry.pack(pady=10)

password_label = ttk.Label(right_frame, text="Password",font=("Arial", 15))
password_label.pack(pady=10)
password_entry = ttk.Entry(right_frame, show="*",font=("Arial", 15))
password_entry.pack(pady=10)

  # สร้างเฟรมแยกสำหรับจัดเรียงปุ่ม Register และ Login ให้อยู่ในแถวเดียวกัน
button_row_frame = ttk.Frame(right_frame)
button_row_frame.pack(pady=10)
    
register_button = ttk.Button(button_row_frame, text="Register", command=show_register_window)
register_button.pack(side="left", padx=5)  # ปุ่ม Register อยู่ทางซ้าย

login_button = ttk.Button(button_row_frame, text="Login", command=login)
login_button.pack(side="left", padx=5)  # ปุ่ม Login อยู่ทางขวา

#reg
image_label = tk.Label(leftt_frame, image=bg_image)
image_label.image = bg_image
image_label.pack(fill="both", expand=True)

welcome_label = ttk.Label(rightt_frame, text="", font=("Arial", 20))
welcome_label.pack(pady=50)  # ใช้ anchor="n" เพื่อจัดให้อยู่ด้านบนสุด

Register_title_label = ttk.Label(rightt_frame, text="Register", font=("Arial", 50))
Register_title_label.pack(pady=20,padx=200)

# ฟอร์มสมัครสมาชิก
reg_username_label = ttk.Label(rightt_frame, text="Username:",font=("Arial", 20))
reg_username_label.pack(pady=10)
reg_username_entry = ttk.Entry(rightt_frame,font=("Arial", 20))
reg_username_entry.pack(pady=10)

reg_password_label = ttk.Label(rightt_frame, text="Password:",font=("Arial", 20))
reg_password_label.pack(pady=10)
reg_password_entry = ttk.Entry(rightt_frame, show="*",font=("Arial", 20))
reg_password_entry.pack(pady=10)

# เพิ่มช่องกรอก Confirm Password
reg_confirm_password_label = ttk.Label(rightt_frame, text="Confirm Password:",font=("Arial", 20))
reg_confirm_password_label.pack(pady=10)
reg_confirm_password_entry = ttk.Entry(rightt_frame, show="*",font=("Arial", 20))
reg_confirm_password_entry.pack(pady=10)


# สร้างเฟรมแยกสำหรับจัดเรียงปุ่ม Back to Login และ Register ให้อยู่ในแถวเดียวกัน
button_row_frame = ttk.Frame(rightt_frame)
button_row_frame.pack(pady=10)

    # จัดปุ่มให้อยู่ในเฟรมเดียวกันเหมือนหน้าเข้าสู่ระบบ
login_redirect_button = ttk.Button(button_row_frame, text="Back to Login", command=show_login_window)
login_redirect_button.pack(side="left", padx=10)

reg_button = ttk.Button(button_row_frame, text="Register", command=register)
reg_button.pack(side="left", padx=10)

# ฟอร์มเพิ่มมีด
knife_sp_label = ttk.Label(add_knife_frame, text="",font=("Arial", 20),background="#c2e1fb")
knife_sp_label.pack(pady=50)
knife_name_label = ttk.Label(add_knife_frame, text="ชื่อมีด",font=("Arial", 20),background="#c2e5fb")
knife_name_label.pack(pady=10)
knife_name_entry = ttk.Entry(add_knife_frame,font=("Arial", 20))
knife_name_entry.pack(pady=10)

knife_stock_label = ttk.Label(add_knife_frame, text="จำนวนมีดในสต็อก",font=("Arial", 20),background="#c2e9fb")
knife_stock_label.pack(pady=10)
knife_stock_entry = ttk.Entry(add_knife_frame,font=("Arial", 20))
knife_stock_entry.pack(pady=10)

knife_price_label = ttk.Label(add_knife_frame, text="ราคามีด",font=("Arial", 20),background="#c2effb")
knife_price_label.pack(pady=10)
knife_price_entry = ttk.Entry(add_knife_frame,font=("Arial", 20))
knife_price_entry.pack(pady=10)

add_knife_submit_button = ttk.Button(add_knife_frame, text="เพิ่มมีด", command=add_knife)
add_knife_submit_button.pack(pady=10)

addk_image_path =r"C:\Users\xenos\Pictures\gif\bgc.png"

addk_image = Image.open(r"C:\Users\xenos\Pictures\gif\bgc.png")
addk_image = addk_image.resize((1550, 800), Image.LANCZOS)
addk_photo = ImageTk.PhotoImage(addk_image)

addk_image_label = tk.Label(addk_image_frame, image=addk_photo)
addk_image_label.image = addk_photo
addk_image_label.pack(pady=0)

# ฟอร์มลบ/ปรับจำนวนมีด
remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=("Name", "Stock", "Price"), show="headings")
remove_knife_tree.heading("Name", text="ชื่อมีด")
remove_knife_tree.heading("Stock", text="จำนวนในสต็อก")
remove_knife_tree.heading("Price", text="ราคา")
remove_knife_tree.pack(pady=10)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
remove_knife_tree.column("Name", anchor='center')
remove_knife_tree.column("Stock", anchor='center')
remove_knife_tree.column("Price", anchor='center')

increase_stock_buttonn = ttk.Frame(remove_knife_frame)
increase_stock_buttonn.pack(side = "bottom",pady=200)

increase_stock_button = ttk.Button(remove_knife_frame, text="เพิ่มจำนวน", command=increase_stock)
increase_stock_button.pack( side = "bottom",padx=10)

decrease_stock_button = ttk.Button(remove_knife_frame, text="ลดจำนวน", command=decrease_stock)
decrease_stock_button.pack( side = "bottom",padx=10)

delete_knife_button = ttk.Button(remove_knife_frame, text="ลบมีด", command=delete_knife)
delete_knife_button.pack( side = "bottom",padx=10)
button_frame.pack(side="bottom", fill="x")

remove_image_path =r"C:\Users\xenos\Pictures\gif\bgs.png"

remove_image = Image.open(r"C:\Users\xenos\Pictures\gif\bgs.png")
remove_image = remove_image.resize((1550, 800), Image.LANCZOS)
remove_photo = ImageTk.PhotoImage(remove_image)

remove_image_label = tk.Label(remove_image_frame, image=remove_photo)
remove_image_label.image = remove_photo
remove_image_label.pack(pady=0)


# ตารางมีด
knife_tree = ttk.Treeview(knife_list_frame, columns=("Name", "Stock", "Price"), show="headings")
knife_tree.heading("Name", text="ชื่อมีด")
knife_tree.heading("Stock", text="จำนวนในสต็อก")
knife_tree.heading("Price", text="ราคา")
knife_tree.pack(pady=10)

listknife_image_path =r"C:\Users\xenos\Pictures\gif\bgs.png"

listknife_image = Image.open(r"C:\Users\xenos\Pictures\gif\bgs.png")
listknife_image = listknife_image.resize((1550, 800), Image.LANCZOS)
listknife_photo = ImageTk.PhotoImage(listknife_image)

listknife_image_label = tk.Label(listknife_image_frame, image=listknife_photo)
listknife_image_label.image = listknife_photo
listknife_image_label.pack(pady=0)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
knife_tree.column("Name", anchor='center')
knife_tree.column("Stock", anchor='center')
knife_tree.column("Price", anchor='center')




sell_product_tree = ttk.Treeview(sell_product_frame, columns=("Name", "Stock", "Price"), show="headings")
sell_product_tree.heading("Name", text="ชื่อมีด")
sell_product_tree.heading("Stock", text="จำนวนในสต็อก")
sell_product_tree.heading("Price", text="ราคา")
sell_product_tree.pack(pady=10)

# ปรับให้เนื้อหาทั้งหมดในตารางอยู่ตรงกลาง
sell_product_tree.column("Name", anchor='center')
sell_product_tree.column("Stock", anchor='center')
sell_product_tree.column("Price", anchor='center')

quantity_label = ttk.Label(sell_product_frame, text="จำนวนสินค้าที่ต้องการซื้อ",font=("Arial", 20),background="#c2ebfb")
quantity_label.pack(pady=10)
quantity_entry = ttk.Entry(sell_product_frame)
quantity_entry.pack(pady=10)


add_to_cart_button = ttk.Button(sell_product_frame, text="เพิ่มลงตะกร้า", command=add_to_cart)
add_to_cart_button.pack(pady=10)



# โหลดรูปภาพและจัดเก็บนอกฟังก์ชันเพื่อให้ใช้ได้ตลอด
left_image_path =r"C:\Users\xenos\Pictures\gif\lsell.png"  # ระบุพาธของรูปซ้าย
right_image_path =r"C:\Users\xenos\Pictures\gif\rsell.png"  # ระบุพาธของรูปขวา

left_image = Image.open(r"C:\Users\xenos\Pictures\gif\lsell.png")
left_image = left_image.resize((400, 800), Image.LANCZOS)
left_photo = ImageTk.PhotoImage(left_image)

right_image = Image.open(r"C:\Users\xenos\Pictures\gif\rsell.png")
right_image = right_image.resize((400, 800), Image.LANCZOS)
right_photo = ImageTk.PhotoImage(right_image)

    # แสดงรูปภาพในเฟรมซ้าย
left_image_label = tk.Label(left_image_frame, image=left_photo)
left_image_label.image = left_photo
left_image_label.pack(pady=0)

    # แสดงรูปภาพในเฟรมขวา
right_image_label = tk.Label(right_image_frame, image=right_photo)
right_image_label.image = right_photo
right_image_label.pack(pady=0)


bgsell_image_path =r"C:\Users\xenos\Pictures\gif\bgs.png"

bgsell_image = Image.open(r"C:\Users\xenos\Pictures\gif\bgs.png")
bgsell_image = bgsell_image.resize((1550, 800), Image.LANCZOS)
bgsell_photo = ImageTk.PhotoImage(bgsell_image)

bgsell_image_label = tk.Label(bgsell_image_frame, image=bgsell_photo)
bgsell_image_label.image = bgsell_photo
bgsell_image_label.pack(pady=0)



# สร้างฟอร์มแสดงรายการสินค้าในตะกร้า
cart_tree = ttk.Treeview(cart_frame, columns=("Name", "Quantity", "Price", "Total"), show="headings")
cart_tree.heading("Name", text="ชื่อสินค้า")
cart_tree.heading("Quantity", text="จำนวน")
cart_tree.heading("Price", text="ราคา/ชิ้น")
cart_tree.heading("Total", text="ราคารวม")
cart_tree.pack(pady=10)

cart_tree.column("Name", anchor='center')
cart_tree.column("Quantity", anchor='center')
cart_tree.column("Price", anchor='center')
cart_tree.column("Total", anchor='center')
# ป้ายแสดงราคารวม
total_label = ttk.Label(cart_frame, text="ราคารวม 0 บาท", font=("Arial", 20),background="#c2ebfb")
total_label.pack(pady=20)

increase_button = ttk.Button(cart_frame, text="เพิ่มจำนวน", command=increase_cart_item)
increase_button.pack(side="top", padx=20,pady=10)

decrease_button = ttk.Button(cart_frame, text="ลดจำนวน", command=decrease_cart_item)
decrease_button.pack(side="top", padx=10)

# ปุ่มยืนยันการชำระเงิน
confirm_button = ttk.Button(cart_frame, text="ยืนยันการสั่งซื้อ", command=confirm_order)
confirm_button.pack(pady=10)

cart_image_path =r"C:\Users\xenos\Pictures\gif\bgc.png"

cart_image = Image.open(r"C:\Users\xenos\Pictures\gif\bgc.png")
cart_image = cart_image.resize((1550, 800), Image.LANCZOS)
cart_photo = ImageTk.PhotoImage(cart_image)

cart_image_label = tk.Label(cart_image_frame, image=cart_photo)
cart_image_label.image = cart_photo
cart_image_label.pack(pady=0)

show_login_window()

root.mainloop()
