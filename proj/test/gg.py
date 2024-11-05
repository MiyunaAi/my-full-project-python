import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # ไลบรารีสำหรับจัดการรูปภาพที่มีความซับซ้อนมากขึ้น เช่น .jpg, .png
import sqlite3

# สร้างหรือเชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect(r'C:\Users\xenos\Documents\datab\knife_shop.db')
c = conn.cursor()

# สร้างตารางมีดถ้ายังไม่มี
c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER
    )
''')

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

# ฟังก์ชันแสดงตารางมีด
def show_knives_window():
    for frame in content_frames:
        frame.pack_forget()

    knife_list_frame.pack(fill="both", expand=True)
    refresh_knife_list(knife_tree)

# ฟังก์ชันเพิ่มมีดใหม่
def add_knife():
    name = knife_name_entry.get()
    stock = int(knife_stock_entry.get())
    price = int(knife_price_entry.get())
    if name and stock > 0 and price > 0:
        # เพิ่มข้อมูลมีดลงในฐานข้อมูล
        c.execute("INSERT INTO knives (name, stock, price) VALUES (?, ?, ?)", (name, stock, price))
        conn.commit()
        messagebox.showinfo("Success", f"เพิ่มมีด {name} เรียบร้อยแล้ว!")
        
        # ล้างข้อมูลในฟิลด์
        knife_name_entry.delete(0, tk.END)
        knife_stock_entry.delete(0, tk.END)
        knife_price_entry.delete(0, tk.END)
        
        # อัปเดตตารางแสดงผล
        refresh_knife_list(knife_tree)
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ถูกต้อง")

def add_knife_window():
    for frame in content_frames:
        frame.pack_forget()

    add_knife_frame.pack(fill="both", expand=True)

# ฟังก์ชันลบจำนวนหรือชนิดมีด
def remove_knife_window():
    for frame in content_frames:
        frame.pack_forget()

    remove_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(remove_knife_tree)

def show_home_window():
    for frame in content_frames:
        frame.pack_forget()

    home_frame.pack(fill="both", expand=True)

# ฟังก์ชันชำระเงิน
def checkout_window():
    for frame in content_frames:
        frame.pack_forget()

    checkout_frame.pack(fill="both", expand=True)
    refresh_knife_list(checkout_tree)
    total_price_label.config(text=f"ราคารวมทั้งหมด: {calculate_total_price()} บาท")

# ฟังก์ชันยืนยันการชำระเงิน
def confirm_payment():
    messagebox.showinfo("Payment", "ชำระเงินเสร็จสิ้น!")
    c.execute("DELETE FROM knives")  # ลบสินค้าทั้งหมดหลังชำระเงิน
    conn.commit()
    refresh_knife_list(knife_tree)
    refresh_knife_list(checkout_tree)
    total_price_label.config(text="ราคารวมทั้งหมด: 0 บาท")

# GUI หลัก
root = tk.Tk()
root.title("ร้านขายมีด")
root.geometry("800x600")

# โหลดรูปภาพพื้นหลัง
bg_image = Image.open(r'C:\Users\xenos\Pictures\Screenshots\Screenshot (68).png')  # ปรับเส้นทางให้ถูกต้อง
bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)  # ปรับขนาดรูปภาพให้พอดีกับหน้าต่าง
bg_photo = ImageTk.PhotoImage(bg_image)

# ใช้ Canvas สำหรับพื้นหลัง
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack(fill="both", expand=True)

# วางรูปภาพลงใน Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ตั้งค่าธีม
style = ttk.Style(root)
root.tk.call("source", r"C:\Users\xenos\Documents\pp\proj\test\Azure\azure.tcl")  # ใช้ธีมที่ทันสมัย
style.theme_use("azure-light")

# Frame หลักสำหรับแต่ละเนื้อหา
content_frames = []

# สร้างปุ่มหลักแถวบนสุด
button_frame = tk.Frame(root)
canvas.create_window(10, 10, anchor="nw", window=button_frame)

home_button = ttk.Button(button_frame, text="หน้าหลักร้านค้า", command=show_home_window)
home_button.pack(side="left", padx=10)

show_knives_button = ttk.Button(button_frame, text="แสดงมีดที่มีอยู่", command=show_knives_window)
show_knives_button.pack(side="left", padx=10)

add_knife_button = ttk.Button(button_frame, text="เพิ่มมีด", command=add_knife_window)
add_knife_button.pack(side="left", padx=10)

remove_knife_button = ttk.Button(button_frame, text="แก้ไขมีด", command=remove_knife_window)
remove_knife_button.pack(side="left", padx=10)

checkout_button = ttk.Button(button_frame, text="ชำระเงิน", command=checkout_window)
checkout_button.pack(side="left", padx=10)

# หน้าหลักร้านค้า
home_frame = tk.Frame(root)
content_frames.append(home_frame)
canvas.create_window(400, 300, anchor="center", window=home_frame)

home_label = ttk.Label(home_frame, text="ร้านมีดออนไลน์เจ๊หลิน", font=("Arial", 24))
home_label.pack(pady=100)

# ส่วนแสดงมีดที่มีอยู่
knife_list_frame = tk.Frame(root)
content_frames.append(knife_list_frame)
canvas.create_window(400, 300, anchor="center", window=knife_list_frame)

columns = ('Name', 'Stock', 'Price', 'TotalPricePerType')
knife_tree = ttk.Treeview(knife_list_frame, columns=columns, show="headings", height=5)
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
canvas.create_window(400, 300, anchor="center", window=add_knife_frame)

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

# ส่วนลบมีด
remove_knife_frame = tk.Frame(root)
content_frames.append(remove_knife_frame)
canvas.create_window(400, 300, anchor="center", window=remove_knife_frame)

remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=columns, show="headings", height=5)
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
increase_button = ttk.Button(remove_knife_frame, text="เพิ่มจำนวน", command=lambda: messagebox.showinfo("Update", "เพิ่มจำนวนเสร็จสิ้น"))
increase_button.pack(side="left", padx=5)

# ปุ่มลบมีด
delete_button = ttk.Button(remove_knife_frame, text="ลบชนิดมีด", command=lambda: messagebox.showinfo("Delete", "ลบมีดเสร็จสิ้น"))
delete_button.pack(side="left", padx=5)

# ส่วนการชำระเงิน
checkout_frame = tk.Frame(root)
content_frames.append(checkout_frame)
canvas.create_window(400, 300, anchor="center", window=checkout_frame)

checkout_tree = ttk.Treeview(checkout_frame, columns=columns, show="headings", height=5)
checkout_tree.heading('Name', text="ชื่อมีด")
checkout_tree.heading('Stock', text="จำนวน")
checkout_tree.heading('Price', text="ราคาต่อชิ้น")
checkout_tree.heading('TotalPricePerType', text="ราคารวมต่อชนิด")
checkout_tree.pack(fill="both", expand=True)

total_price_label = ttk.Label(checkout_frame, text="ราคารวมทั้งหมด: 0 บาท")
total_price_label.pack(pady=20)

confirm_checkout_button = ttk.Button(checkout_frame, text="ยืนยันการชำระเงิน", command=confirm_payment)
confirm_checkout_button.pack(pady=10)

# เริ่มต้นด้วยการแสดงหน้าหลัก
show_home_window()

root.mainloop()

# ปิดการเชื่อมต่อกับฐานข้อมูล
conn.close()
