import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import qrcode
import sqlite3
import io

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ร้านขายของ")
root.geometry("800x600")

# สร้างฐานข้อมูลสินค้า
conn = sqlite3.connect('shop.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                image BLOB)''')
conn.commit()

# ฟังก์ชันสำหรับโหลดภาพสินค้า
def load_image(image_path):
    img = Image.open(image_path)
    img = img.resize((100, 100))
    return ImageTk.PhotoImage(img)

# เพิ่มสินค้าเพื่อการทดสอบ
def add_product(name, price, image_path):
    with open(image_path, 'rb') as file:
        image_data = file.read()
    c.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", (name, price, image_data))
    conn.commit()

# เริ่มต้นรายการสินค้าในฐานข้อมูล (เฉพาะการทดสอบ)
# add_product("Product 1", 100.0, "product1.png")
# add_product("Product 2", 150.0, "product2.png")

# ฟังก์ชันค้นหาและแสดงสินค้า
cart = {}
def show_products(search_term=""):
    for widget in main_frame.winfo_children():
        widget.destroy()

    c.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
    products = c.fetchall()
    
    for product in products:
        frame = ttk.Frame(main_frame)
        frame.pack(pady=10)

        name, price, image_data = product[1], product[2], product[3]
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)

        label = tk.Label(frame, image=img)
        label.image = img
        label.pack()

        tk.Label(frame, text=name).pack()
        tk.Label(frame, text=f"฿{price:.2f}").pack()

        quantity = tk.IntVar(value=1)
        tk.Spinbox(frame, from_=1, to=10, textvariable=quantity, width=5).pack()
        
        tk.Button(frame, text="เพิ่มลงตะกร้า", command=lambda p=product, q=quantity: add_to_cart(p, q)).pack()

# เพิ่มสินค้าไปยังตะกร้า
def add_to_cart(product, quantity):
    product_id, name, price = product[0], product[1], product[2]
    cart[product_id] = {"name": name, "price": price, "quantity": quantity.get()}
    messagebox.showinfo("ตะกร้าสินค้า", f"เพิ่ม {name} ลงในตะกร้าเรียบร้อยแล้ว")

# แสดงตะกร้าสินค้า
def show_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("ตะกร้าสินค้า")
    
    total = 0
    for item in cart.values():
        tk.Label(cart_window, text=f"{item['name']} - ฿{item['price']} x {item['quantity']}").pack()
        total += item['price'] * item['quantity']
        
    tk.Label(cart_window, text=f"ยอดรวมทั้งหมด: ฿{total:.2f}").pack()
    tk.Button(cart_window, text="ชำระเงิน", command=lambda: generate_qr_code(total)).pack()

# สร้าง QR Code PromptPay สำหรับชำระเงิน
def generate_qr_code(amount):
    promptpay_id = "0812345678"  # ใส่หมายเลข PromptPay ของร้านค้า
    payload = f"00020101021129370016A0000006770101110213{promptpay_id}5802TH53037645802TH5406{amount:.2f}6304"
    qr = qrcode.make(payload)
    
    # แสดง QR Code ใน pop-up
    qr_window = tk.Toplevel(root)
    qr_window.title("ชำระเงิน")
    qr_img = ImageTk.PhotoImage(qr)
    tk.Label(qr_window, image=qr_img).pack()
    tk.Label(qr_window, text=f"จำนวนเงิน: ฿{amount:.2f}").pack()
    qr_window.mainloop()

# ส่วนแสดงผล
search_bar = tk.Entry(root)
search_bar.pack(pady=5)
search_bar.bind("<Return>", lambda event: show_products(search_bar.get()))

tk.Button(root, text="ดูตะกร้าสินค้า", command=show_cart).pack(pady=5)

main_frame = tk.Frame(root)
main_frame.pack()

show_products()  # เรียกดูสินค้าทั้งหมด

root.mainloop()
