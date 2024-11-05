import tkinter as tk
from tkinter import messagebox, ttk
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

# ฟังก์ชันเพิ่มมีด
def add_knife():
    name = knife_name_entry.get()
    price = int(knife_price_entry.get())
    stock = int(knife_stock_entry.get())
    if name and price > 0 and stock > 0:
        c.execute("INSERT INTO knives (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        messagebox.showinfo("Success", f"เพิ่มมีด {name} เรียบร้อยแล้ว!")
        knife_name_entry.delete(0, tk.END)
        knife_price_entry.delete(0, tk.END)
        knife_stock_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ถูกต้อง")

# ฟังก์ชันลบจำนวนมีด
def reduce_stock():
    name = knife_name_entry.get()
    reduce_amount = int(stock_reduce_entry.get())
    c.execute("SELECT stock FROM knives WHERE name = ?", (name,))
    result = c.fetchone()
    if result and result[0] >= reduce_amount:
        c.execute("UPDATE knives SET stock = stock - ? WHERE name = ?", (reduce_amount, name))
        conn.commit()
        messagebox.showinfo("Success", f"ลดจำนวน {reduce_amount} ของมีด {name} เรียบร้อยแล้ว!")
    else:
        messagebox.showwarning("Error", "จำนวนไม่เพียงพอหรือมีดไม่มีในคลัง")

# ฟังก์ชันลบมีด
def remove_knife():
    name = knife_name_entry.get()
    c.execute("DELETE FROM knives WHERE name = ?", (name,))
    conn.commit()
    messagebox.showinfo("Success", f"ลบมีด {name} เรียบร้อยแล้ว!")

# ฟังก์ชันแสดงมีดทั้งหมด
def show_knives():
    c.execute("SELECT name, stock FROM knives")
    knives = c.fetchall()
    knife_list = "\n".join([f"{name}: {stock} ชิ้น" for name, stock in knives])
    messagebox.showinfo("Knife Inventory", knife_list if knife_list else "ไม่มีมีดในคลัง")

# ฟังก์ชันซื้อมีด
def purchase_knife():
    name = knife_name_entry.get()
    quantity = int(purchase_quantity_entry.get())
    c.execute("SELECT stock, price FROM knives WHERE name = ?", (name,))
    result = c.fetchone()
    if result and result[0] >= quantity:
        total_price = result[1] * quantity
        c.execute("UPDATE knives SET stock = stock - ? WHERE name = ?", (quantity, name))
        conn.commit()
        messagebox.showinfo("Purchase", f"ซื้อ {quantity} ชิ้นของมีด {name} ในราคา ${total_price}")
    else:
        messagebox.showwarning("Error", "จำนวนไม่เพียงพอหรือไม่มีมีดนี้")

# ฟังก์ชันซ่อนหรือแสดงส่วนต่าง ๆ
def toggle_section(section_frame, toggle_button):
    if section_frame.winfo_viewable():
        section_frame.pack_forget()
        toggle_button.config(text=f"แสดง {toggle_button.text}")
    else:
        section_frame.pack(pady=10)
        toggle_button.config(text=f"ซ่อน {toggle_button.text}")

# GUI หลัก
root = tk.Tk()
root.title("ร้านขายมีด")
root.geometry("500x500")
root.config(bg="skyblue")

# สร้างส่วนต่าง ๆ เป็น Frame
# ส่วนเพิ่มมีด
add_frame = tk.Frame(root)
ttk.Label(add_frame, text="ชื่อมีด").pack(pady=5)
knife_name_entry = ttk.Entry(add_frame)
knife_name_entry.pack(pady=5)
ttk.Label(add_frame, text="ราคา").pack(pady=5)
knife_price_entry = ttk.Entry(add_frame)
knife_price_entry.pack(pady=5)
ttk.Label(add_frame, text="จำนวน").pack(pady=5)
knife_stock_entry = ttk.Entry(add_frame)
knife_stock_entry.pack(pady=5)
add_button = ttk.Button(add_frame, text="เพิ่มมีด", command=add_knife)
add_button.pack(pady=10)

# ส่วนลดจำนวนสินค้า
reduce_frame = tk.Frame(root)
ttk.Label(reduce_frame, text="ลดจำนวนสินค้า").pack(pady=5)
stock_reduce_entry = ttk.Entry(reduce_frame)
stock_reduce_entry.pack(pady=5)
reduce_button = ttk.Button(reduce_frame, text="ลดจำนวนมีด", command=reduce_stock)
reduce_button.pack(pady=10)

# ส่วนลบมีด
remove_frame = tk.Frame(root)
remove_button = ttk.Button(remove_frame, text="ลบมีด", command=remove_knife)
remove_button.pack(pady=10)

# ส่วนแสดงมีดทั้งหมด
show_frame = tk.Frame(root)
show_button = ttk.Button(show_frame, text="แสดงมีดทั้งหมด", command=show_knives)
show_button.pack(pady=10)

# ส่วนการซื้อมีด
purchase_frame = tk.Frame(root)
ttk.Label(purchase_frame, text="จำนวนที่ต้องการซื้อ").pack(pady=5)
purchase_quantity_entry = ttk.Entry(purchase_frame)
purchase_quantity_entry.pack(pady=5)
purchase_button = ttk.Button(purchase_frame, text="ซื้อมีด", command=purchase_knife)
purchase_button.pack(pady=10)

# ปุ่มเพื่อซ่อนและแสดงแต่ละฟังก์ชัน
toggle_add_button = ttk.Button(root, text="แสดง เพิ่มมีด", command=lambda: toggle_section(add_frame, toggle_add_button))
toggle_add_button.pack(side=tk.TOP, padx=5)
toggle_add_button.config(bg="red", fg="white")  # เปลี่ยนสีปุ่มเป็นแดง

toggle_reduce_button = ttk.Button(root, text="แสดง ลดจำนวนมีด", command=lambda: toggle_section(reduce_frame, toggle_reduce_button))
toggle_reduce_button.pack(side=tk.TOP, padx=5)
toggle_reduce_button.config(bg="red", fg="white")  # เปลี่ยนสีปุ่มเป็นแดง

toggle_remove_button = ttk.Button(root, text="แสดง ลบมีด", command=lambda: toggle_section(remove_frame, toggle_remove_button))
toggle_remove_button.pack(side=tk.TOP, padx=5)
toggle_remove_button.config(bg="red", fg="white")  # เปลี่ยนสีปุ่มเป็นแดง

toggle_show_button = ttk.Button(root, text="แสดง มีดทั้งหมด", command=lambda: toggle_section(show_frame, toggle_show_button))
toggle_show_button.pack(side=tk.TOP, padx=5)
toggle_show_button.config(bg="red", fg="white")  # เปลี่ยนสีปุ่มเป็นแดง

toggle_purchase_button = ttk.Button(root, text="แสดง ซื้อมีด", command=lambda: toggle_section(purchase_frame, toggle_purchase_button))
toggle_purchase_button.pack(side=tk.TOP, padx=5)
toggle_purchase_button.config(bg="red", fg="white")  # เปลี่ยนสีปุ่มเป็นแดง

# เริ่มต้นโปรแกรม
root.mainloop()

# ปิดการเชื่อมต่อกับฐานข้อมูล
conn.close()
