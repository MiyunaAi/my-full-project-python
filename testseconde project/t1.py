import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import io

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ร้านขายของ")
root.geometry("800x600")

# สร้างฐานข้อมูลสินค้า
conn = sqlite3.connect(r'C:\Users\xenos\Documents\datab\hop.db')
c = conn.cursor()

# ลบตารางเดิมหากมีอยู่แล้วและสร้างตารางใหม่
c.execute("DROP TABLE IF EXISTS products")
c.execute('''CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                quantity INTEGER,
                image BLOB)''')
conn.commit()

# ฟังก์ชันเพิ่มสินค้าใหม่ในระบบ
def open_add_product_window():
    add_product_window = tk.Toplevel(root)
    add_product_window.title("เพิ่มสินค้า")
    add_product_window.geometry("400x300")

    # ชื่อสินค้า
    tk.Label(add_product_window, text="ชื่อสินค้า").pack()
    name_entry = tk.Entry(add_product_window)
    name_entry.pack()

    # ราคา
    tk.Label(add_product_window, text="ราคาสินค้า").pack()
    price_entry = tk.Entry(add_product_window)
    price_entry.pack()

    # จำนวน
    tk.Label(add_product_window, text="จำนวนสินค้า").pack()
    quantity_entry = tk.Entry(add_product_window)
    quantity_entry.pack()

    # รูปภาพ
    tk.Label(add_product_window, text="รูปสินค้า").pack()
    image_path = tk.StringVar()
    tk.Entry(add_product_window, textvariable=image_path, state='readonly').pack()
    tk.Button(add_product_window, text="เลือกรูปภาพ", command=lambda: select_image(image_path)).pack()

    # ปุ่มเพิ่มสินค้า
    tk.Button(add_product_window, text="เพิ่มสินค้า", command=lambda: add_product(name_entry.get(), price_entry.get(), quantity_entry.get(), image_path.get(), add_product_window)).pack()

# ฟังก์ชันสำหรับเลือกไฟล์รูปภาพ
def select_image(image_path_var):
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    image_path_var.set(path)

# ฟังก์ชันบันทึกสินค้าใหม่ในฐานข้อมูล
def add_product(name, price, quantity, image_path, window):
    if not name or not price or not quantity or not image_path:
        messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        return

    try:
        price = float(price)
        quantity = int(quantity)
        
        with open(image_path, 'rb') as file:
            image_data = file.read()
        
        c.execute("INSERT INTO products (name, price, quantity, image) VALUES (?, ?, ?, ?)", (name, price, quantity, image_data))
        conn.commit()
        
        messagebox.showinfo("สำเร็จ", f"เพิ่มสินค้า '{name}' เรียบร้อยแล้ว")
        window.destroy()  # ปิดหน้าต่างเพิ่มสินค้า
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกราคาสินค้าและจำนวนสินค้าเป็นตัวเลขที่ถูกต้อง")
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเพิ่มสินค้าได้: {e}")

# ส่วนแสดงผลในหน้าหลัก
tk.Button(root, text="เพิ่มสินค้าใหม่", command=open_add_product_window).pack(pady=5)
main_frame = tk.Frame(root)
main_frame.pack()

root.mainloop()
