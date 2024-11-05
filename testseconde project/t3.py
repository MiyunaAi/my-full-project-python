import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import qrcode
import io

# สร้างฐานข้อมูลและตารางสินค้า
conn = sqlite3.connect(r'C:\Users\xenos\Documents\datab\tore.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        stock INTEGER,
        image BLOB
    )
''')
conn.commit()

cart = {}  # ตะกร้าสินค้าเก็บสินค้าและจำนวน

# ฟังก์ชันเพิ่มสินค้าในฐานข้อมูล
def add_product(name, price, stock, image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    c.execute("INSERT INTO products (name, price, stock, image) VALUES (?, ?, ?, ?)", (name, price, stock, image_data))
    conn.commit()
    refresh_home_page()

# ฟังก์ชันดึงข้อมูลสินค้าจากฐานข้อมูล
def get_products():
    c.execute("SELECT * FROM products ORDER BY id DESC")
    return c.fetchall()

# ฟังก์ชันเพิ่มสินค้าลงในตะกร้า
def add_to_cart(product_id, quantity):
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

# ฟังก์ชันแสดงหน้าหลัก
def show_home_page():
    clear_frame()
    products = get_products()

    for idx, product in enumerate(products):
        product_id, name, price, stock, image_data = product
        row, col = divmod(idx, 3)
        
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)

        frame = tk.Frame(content_frame)
        frame.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(frame, image=img_tk).pack()
        tk.Label(frame, text=f"{name}\n{price} บาท").pack()
        
        def add_product_to_cart(product_id=product_id):
            quantity = int(quantity_entry.get())
            add_to_cart(product_id, quantity)
            messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าลงในตะกร้าแล้ว")

        quantity_entry = tk.Entry(frame, width=5)
        quantity_entry.pack()
        tk.Button(frame, text="เพิ่มลงตะกร้า", command=add_product_to_cart).pack()

# ฟังก์ชันแสดงหน้าเพิ่มสินค้า
def show_add_product_page():
    clear_frame()

    tk.Label(content_frame, text="เพิ่มสินค้าใหม่").grid(row=0, column=0, columnspan=2)

    tk.Label(content_frame, text="ชื่อสินค้า").grid(row=1, column=0)
    name_entry = tk.Entry(content_frame)
    name_entry.grid(row=1, column=1)

    tk.Label(content_frame, text="ราคา").grid(row=2, column=0)
    price_entry = tk.Entry(content_frame)
    price_entry.grid(row=2, column=1)

    tk.Label(content_frame, text="จำนวนสินค้า").grid(row=3, column=0)
    stock_entry = tk.Entry(content_frame)
    stock_entry.grid(row=3, column=1)

    tk.Label(content_frame, text="รูปภาพ").grid(row=4, column=0)
    image_path = tk.StringVar()
    
    def upload_image():
        path = filedialog.askopenfilename()
        image_path.set(path)
        tk.Label(content_frame, text="อัปโหลดรูปภาพแล้ว").grid(row=4, column=1)

    tk.Button(content_frame, text="อัปโหลดรูปภาพ", command=upload_image).grid(row=5, column=0, columnspan=2)

    def save_product():
        name = name_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        add_product(name, price, stock, image_path.get())
        messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าเรียบร้อยแล้ว")
        show_home_page()

    tk.Button(content_frame, text="บันทึกสินค้า", command=save_product).grid(row=6, column=0, columnspan=2)

# ฟังก์ชันแสดงหน้าตะกร้าสินค้า
def show_cart():
    clear_frame()
    total = 0
    row = 0
    
    for product_id, quantity in cart.items():
        c.execute("SELECT name, price FROM products WHERE id = ?", (product_id,))
        name, price = c.fetchone()
        subtotal = price * quantity
        total += subtotal

        tk.Label(content_frame, text=f"{name} x {quantity} = {subtotal} บาท").grid(row=row, column=0)
        
        def update_quantity(new_quantity, product_id=product_id):
            cart[product_id] = new_quantity
            show_cart()
        
        tk.Entry(content_frame, text=str(quantity), width=5).grid(row=row, column=1)
        row += 1

    tk.Label(content_frame, text=f"รวมทั้งหมด: {total} บาท").grid(row=row, column=0)

    def show_qr_code():
        qr = qrcode.make(f"promptpay://qr?amt={total}")
        qr_window = tk.Toplevel()
        qr_window.title("QR Code ชำระเงิน")
        img = ImageTk.PhotoImage(qr)
        tk.Label(qr_window, image=img).pack()
        qr_window.mainloop()

    tk.Button(content_frame, text="ชำระเงิน", command=show_qr_code).grid(row=row+1, column=0)

# ฟังก์ชันล้างเนื้อหาในหน้า
def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# สร้างหน้าหลัก
root = tk.Tk()
root.title("ร้านค้าออนไลน์")

# สร้างเมนูด้านบน
menu_frame = tk.Frame(root)
menu_frame.pack()

tk.Button(menu_frame, text="หน้าหลัก", command=show_home_page).grid(row=0, column=0)
tk.Button(menu_frame, text="เพิ่มสินค้า", command=show_add_product_page).grid(row=0, column=1)
tk.Button(menu_frame, text="ตะกร้า", command=show_cart).grid(row=0, column=2)

# สร้างพื้นที่แสดงเนื้อหา
content_frame = tk.Frame(root)
content_frame.pack()

show_home_page()

root.mainloop()

# ปิดฐานข้อมูลเมื่อปิดโปรแกรม
conn.close()
