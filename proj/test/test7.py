import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Create SQLite database and table for knife inventory
conn = sqlite3.connect('knife_shop.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS knives (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER
    )
''')

# Function to fetch knife data from the database
def fetch_knives():
    c.execute("SELECT name, price, stock FROM knives")
    return c.fetchall()

# Function to refresh the knife display after changes (add/remove stock)
def refresh_display():
    for widget in knife_frame.winfo_children():
        widget.destroy()
    create_knife_checkboxes()

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

# Function to show cart details
def show_cart():
    cart_items = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if cart_items:
        cart_details = "\n".join(cart_items)
        messagebox.showinfo("Cart", f"Items in your cart:\n{cart_details}")
    else:
        messagebox.showinfo("Cart", "Your cart is empty.")

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
        refresh_display()
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to purchase.")

knife_name_entry = {}
knife_price_entry = {}
knife_stock_entry = {}
# Function to add a new knife to the database
def add_knife():
    name = knife_name_entry.get()
    price = int(knife_price_entry.get())
    stock = int(knife_stock_entry.get())

    if name and price > 0 and stock > 0:
        c.execute("INSERT INTO knives (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        refresh_display()
        knife_name_entry.delete(0, tk.END)
        knife_price_entry.delete(0, tk.END)
        knife_stock_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"{name} has been added to the shop!")
    else:
        messagebox.showwarning("Invalid input", "Please enter valid data for the knife.")

# Function to remove a knife from the database
def remove_knife():
    selected_knives = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if selected_knives:
        for knife in selected_knives:
            c.execute("DELETE FROM knives WHERE name = ?", (knife,))
            conn.commit()
        messagebox.showinfo("Success", f"{', '.join(selected_knives)} has been removed from the shop!")
        refresh_display()
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to remove.")

# Function to reduce stock for a selected knife
def reduce_stock():
    selected_knives = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if selected_knives:
        for knife in selected_knives:
            stock_var = knife_stock_vars[knife]
            reduce_amount = int(stock_reduce_entry.get())  # Get the amount to reduce from entry
            if stock_var.get() - reduce_amount >= 0:
                stock_var.set(stock_var.get() - reduce_amount)
                c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock_var.get(), knife))
                conn.commit()
                messagebox.showinfo("Success", f"Reduced {reduce_amount} from {knife}'s stock!")
            else:
                messagebox.showwarning("Invalid stock", f"Not enough stock to reduce {reduce_amount} from {knife}.")
        refresh_display()
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to reduce stock.")

# Function to add stock for a selected knife
def add_stock():
    selected_knives = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if selected_knives:
        for knife in selected_knives:
            stock_var = knife_stock_vars[knife]
            add_amount = int(stock_add_entry.get())  # Get the amount to add from entry
            stock_var.set(stock_var.get() + add_amount)
            c.execute("UPDATE knives SET stock = ? WHERE name = ?", (stock_var.get(), knife))
            conn.commit()
            messagebox.showinfo("Success", f"Added {add_amount} to {knife}'s stock!")
        refresh_display()
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to add stock.")

# Toggle the visibility of the reduce stock menu
def toggle_reduce_stock_menu():
    if stock_reduce_menu.winfo_ismapped():
        stock_reduce_menu.pack_forget()
    else:
        stock_reduce_menu.pack(pady=5)

# Toggle the visibility of the add stock menu
def toggle_add_stock_menu():
    if stock_add_menu.winfo_ismapped():
        stock_add_menu.pack_forget()
    else:
        stock_add_menu.pack(pady=5)

def toggle_add_knife_menu():
    if knife_add_menu.winfo_ismapped():
        stock_add_menu.pack_forget()
    else:
        stock_add_menu.pack(pady=5)

# Create main window
root = tk.Tk()
root.title("Enhanced Cute Knife Shop with Stock Management")
root.geometry("500x600")
root.configure(bg='#F0F8FF')

# Create style for ttk widgets to make them cute
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background='#FFD700')
style.configure("TLabel", font=("Helvetica", 12), background='#F0F8FF')

# Create a cute label for the shop name
shop_label = ttk.Label(root, text="Welcome to the Enhanced Cute Knife Shop!", font=("Helvetica", 16, "bold"), background='#F0F8FF')
shop_label.pack(pady=10)

# Create a frame for knife checkboxes
knife_frame = tk.Frame(root, bg='#F0F8FF')
knife_frame.pack(pady=10)

# Store knife variables for prices and stocks
knife_vars = {}
knife_prices = {}
knife_stock_vars = {}

# Function to create knife checkboxes
def create_knife_checkboxes():
    knives = fetch_knives()
    for knife in knives:
        knife_name, price, stock = knife
        knife_prices[knife_name] = price

        var = tk.IntVar()
        stock_var = tk.IntVar(value=stock)
        knife_vars[knife_name] = var
        knife_stock_vars[knife_name] = stock_var

        chk = tk.Checkbutton(knife_frame, text=f"{knife_name} - ${price} (Stock: {stock_var.get()})", 
                             variable=var, command=update_price, bg='#F0F8FF', font=("Helvetica", 12))
        chk.pack(anchor='w')

# Create knife checkboxes initially
create_knife_checkboxes()

# Display total price
total_label = ttk.Label(root, text="Total: $0")
total_label.pack(pady=10)

# Purchase button
purchase_button = ttk.Button(root, text="Purchase", command=purchase)
purchase_button.pack(pady=5)

# Show cart button
cart_button = ttk.Button(root, text="Show Cart", command=show_cart)
cart_button.pack(pady=5)

# Remove knife button
remove_button = ttk.Button(root, text="Remove Knife", command=remove_knife)
remove_button.pack(pady=5)

# Toggle reduce stock menu button
reduce_stock_button = ttk.Button(root, text="Reduce Stock", command=toggle_reduce_stock_menu)
reduce_stock_button.pack(pady=5)

#add_k
add_knife_button = ttk.Button(root, text="Add Knife", command=toggle_reduce_stock_menu)
reduce_stock_button.pack(pady=5)

# Reduce stock menu (initially hidden)
stock_reduce_menu = tk.Frame(root, bg='#F0F8FF')
ttk.Label(stock_reduce_menu, text="Reduce Stock Amount:", background='#F0F8FF').pack(pady=5)
stock_reduce_entry = ttk.Entry(stock_reduce_menu, width=20)
stock_reduce_entry.pack(pady=5)
confirm_reduce_button = ttk.Button(stock_reduce_menu, text="Confirm Reduce", command=reduce_stock)
confirm_reduce_button.pack(pady=5)

# Toggle add stock menu button
add_stock_button = ttk.Button(root, text="Add Stock", command=toggle_add_stock_menu)
add_stock_button.pack(pady=5)

# Add stock menu (initially hidden)
stock_add_menu = tk.Frame(root, bg='#F0F8FF')
ttk.Label(stock_add_menu, text="Add Stock Amount:", background='#F0F8FF').pack(pady=5)
stock_add_entry = ttk.Entry(stock_add_menu, width=20)
stock_add_entry.pack(pady=5)
confirm_add_button = ttk.Button(stock_add_menu, text="Confirm Add", command=add_stock)
confirm_add_button.pack(pady=5)

#ADD
add_stock_button = ttk.Button(root, text="Add knife", command=toggle_add_stock_menu)
add_stock_button.pack(pady=5)
# Run the application
root.mainloop()