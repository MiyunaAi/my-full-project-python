import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Create SQLite database and table for knife inventory
conn = sqlite3.connect(r'C:\Users\xenos\Documents\db\knife_shop.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER
    )
''')

# Sample knife data (add only if table is empty)
c.execute("SELECT COUNT(*) FROM knives")
if c.fetchone()[0] == 0:
    knife_data = [
        ("Chef's Knife", 50, 10),
        ("Paring Knife", 20, 15),
        ("Bread Knife", 30, 8),
        ("Carving Knife", 40, 5)
    ]
    c.executemany("INSERT INTO knives (name, price, stock) VALUES (?, ?, ?)", knife_data)
    conn.commit()

# Create main window
root = tk.Tk()
root.title("Cute Knife Shop")
root.geometry("400x400")
root.configure(bg='#F0F8FF')

# Create style for ttk widgets to make them cute
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background='#FFD700')
style.configure("TLabel", font=("Helvetica", 12), background='#F0F8FF')

# Fetch knife data from the database
c.execute("SELECT name, price, stock FROM knives")
knives = c.fetchall()

# Function to update the total price and handle stock
def update_price():
    total = 0
    for knife, var in knife_vars.items():
        if var.get() == 1:
            selected_stock = knife_stock_vars[knife]
            if selected_stock.get() > 0:
                total += knife_prices[knife]
            else:
                messagebox.showwarning("Out of stock", f"{knife} is out of stock!")
                var.set(0)
    total_label.config(text=f"Total: ${total}")

# Function to handle purchase
def purchase():
    selected_knives = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if selected_knives:
        for knife in selected_knives:
            stock_var = knife_stock_vars[knife]
            if stock_var.get() > 0:
                stock_var.set(stock_var.get() - 1)
                c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock_var.get(), knife))
                conn.commit()
            else:
                messagebox.showwarning("Out of stock", f"{knife} is out of stock!")
        messagebox.showinfo("Purchase", f"You bought: {', '.join(selected_knives)}!")
        update_price()
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to purchase.")

# Create a cute label for the shop name
shop_label = ttk.Label(root, text="Welcome to the Cute Knife Shop!", font=("Helvetica", 16, "bold"), background='#F0F8FF')
shop_label.pack(pady=10)

# Store knife variables for prices and stocks
knife_vars = {}
knife_prices = {}
knife_stock_vars = {}

# Create checkboxes and labels for each knife
for knife in knives:
    knife_name, price, stock = knife
    knife_prices[knife_name] = price
    
    var = tk.IntVar()
    stock_var = tk.IntVar(value=stock)
    knife_vars[knife_name] = var
    knife_stock_vars[knife_name] = stock_var
    
    chk = tk.Checkbutton(root, text=f"{knife_name} - ${price} (Stock: {stock_var.get()})", 
                         variable=var, command=update_price, bg='#F0F8FF', font=("Helvetica", 12))
    chk.pack(anchor='w')

# Display total price
total_label = ttk.Label(root, text="Total: $0")
total_label.pack(pady=10)

# Purchase button
purchase_button = ttk.Button(root, text="Purchase", command=purchase)
purchase_button.pack(pady=10)

# Run the application
root.mainloop()

# Close the SQLite connection
conn.close()
