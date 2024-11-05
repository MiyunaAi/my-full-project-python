import tkinter as tk
from tkinter import ttk, messagebox
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

# ฟังก์ชันรีเฟรชรายการมีดใน Treeview
def refresh_knife_list(treeview):
    treeview.delete(*treeview.get_children())
    c.execute("SELECT name, stock FROM knives")
    knives = c.fetchall()
    for name, stock in knives:
        treeview.insert("", "end", values=(name, stock))

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
    if name and stock > 0:
        c.execute("INSERT INTO knives (name, stock) VALUES (?, ?)", (name, stock))
        conn.commit()
        messagebox.showinfo("Success", f"เพิ่มมีด {name} เรียบร้อยแล้ว!")
        knife_name_entry.delete(0, tk.END)
        knife_stock_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid input", "กรุณากรอกข้อมูลให้ถูกต้อง")

def add_knife_window():
    for frame in content_frames:
        frame.pack_forget()

    add_knife_frame.pack(fill="both", expand=True)

# ฟังก์ชันแสดงและลบมีด
def remove_knife_window():
    for frame in content_frames:
        frame.pack_forget()

    remove_knife_frame.pack(fill="both", expand=True)
    refresh_knife_list(remove_knife_tree)

# ฟังก์ชันลบจำนวนมีด
def reduce_stock():
    selected_item = remove_knife_tree.selection()
    if not selected_item:
        messagebox.showwarning("Error", "กรุณาเลือกมีดที่ต้องการลดจำนวน")
        return

    name = remove_knife_tree.item(selected_item, "values")[0]
    reduce_amount = int(reduce_stock_entry.get())

    # ตรวจสอบจำนวนที่มี
    c.execute("SELECT stock FROM knives WHERE name = ?", (name,))
    result = c.fetchone()
    if result and result[0] >= reduce_amount:
        c.execute("UPDATE knives SET stock = stock - ? WHERE name = ?", (reduce_amount, name))
        conn.commit()
        refresh_knife_list(remove_knife_tree)
        messagebox.showinfo("Success", f"ลดจำนวน {reduce_amount} ของมีด {name} เรียบร้อยแล้ว!")
    else:
        messagebox.showwarning("Error", "จำนวนไม่เพียงพอหรือไม่มีมีดนี้")

# ฟังก์ชันลบมีดทั้งหมด
def delete_knife():
    selected_item = remove_knife_tree.selection()
    if not selected_item:
        messagebox.showwarning("Error", "กรุณาเลือกมีดที่ต้องการลบ")
        return
    name = remove_knife_tree.item(selected_item, "values")[0]
    c.execute("DELETE FROM knives WHERE name = ?", (name,))
    conn.commit()
    refresh_knife_list(remove_knife_tree)
    messagebox.showinfo("Success", f"ลบมีด {name} เรียบร้อยแล้ว!")

# ฟังก์ชันเปิดหน้าต่างให้เลือกลบจำนวนหรือชนิดมีด
def confirm_delete():
    confirmation_window = tk.Toplevel(root)
    confirmation_window.title("เลือกการลบ")

    ttk.Label(confirmation_window, text="คุณต้องการลบจำนวนหรือชนิดมีดทั้งหมด?").pack(pady=10)

    delete_type_button = ttk.Button(confirmation_window, text="ลบชนิดมีด", command=lambda: [delete_knife(), confirmation_window.destroy()])
    delete_type_button.pack(pady=5)

    reduce_stock_frame = tk.Frame(confirmation_window)
    ttk.Label(reduce_stock_frame, text="ลดจำนวน").pack(side="left", padx=5)
    global reduce_stock_entry
    reduce_stock_entry = ttk.Entry(reduce_stock_frame, width=5)
    reduce_stock_entry.pack(side="left", padx=5)
    reduce_stock_frame.pack(pady=5)

    reduce_button = ttk.Button(confirmation_window, text="ลดจำนวนมีด", command=lambda: [reduce_stock(), confirmation_window.destroy()])
    reduce_button.pack(pady=5)

# GUI หลัก
root = tk.Tk()
root.title("ร้านขายมีด")
root.geometry("600x400")

# ตั้งค่าธีม
style = ttk.Style(root)
style.theme_use("clam")

# Frame หลักสำหรับแต่ละเนื้อหา
content_frames = []

# สร้างปุ่มหลักแถวบนสุด
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

show_knives_button = ttk.Button(button_frame, text="แสดงมีดที่มีอยู่", command=show_knives_window)
show_knives_button.pack(side="left", padx=10)

add_knife_button = ttk.Button(button_frame, text="เพิ่มมีด", command=add_knife_window)
add_knife_button.pack(side="left", padx=10)

remove_knife_button = ttk.Button(button_frame, text="ลบมีด", command=remove_knife_window)
remove_knife_button.pack(side="left", padx=10)

# ส่วนแสดงมีดที่มีอยู่
knife_list_frame = tk.Frame(root)
content_frames.append(knife_list_frame)

columns = ('Name', 'Stock')
knife_tree = ttk.Treeview(knife_list_frame, columns=columns, show="headings", height=5)  # ลดขนาดตารางด้วย height
knife_tree.heading('Name', text="ชื่อมีด")
knife_tree.heading('Stock', text="จำนวนคงเหลือ")
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

confirm_add_button = ttk.Button(add_knife_frame, text="ยืนยันการเพิ่ม", command=add_knife)
confirm_add_button.pack(pady=10)

# ส่วนลบมีด
remove_knife_frame = tk.Frame(root)
content_frames.append(remove_knife_frame)

remove_knife_tree = ttk.Treeview(remove_knife_frame, columns=columns, show="headings", height=5)  # ลดขนาดตารางด้วย height
remove_knife_tree.heading('Name', text="ชื่อมีด")
remove_knife_tree.heading('Stock', text="จำนวนคงเหลือ")
remove_knife_tree.pack(fill="both", expand=True)

# Scrollbar สำหรับตารางการลบ
remove_scrollbar = ttk.Scrollbar(remove_knife_frame, orient="vertical", command=remove_knife_tree.yview)
remove_knife_tree.configure(yscroll=remove_scrollbar.set)
remove_scrollbar.pack(side="right", fill="y")

delete_button = ttk.Button(remove_knife_frame, text="ยืนยันการลบ", command=confirm_delete)
delete_button.pack(pady=10)

# เริ่มต้นด้วยการแสดงตารางมีด
show_knives_window()

root.mainloop()

# ปิดการเชื่อมต่อกับฐานข้อมูล
conn.close()
