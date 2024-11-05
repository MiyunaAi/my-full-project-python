import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Knife Shop")
root.geometry("400x400")

# Sample knife data
knives = {
    "Chef's Knife": 50,
    "Paring Knife": 20,
    "Bread Knife": 30,
    "Carving Knife": 40
}

# Function to update the total price
def update_price():
    total = 0
    for knife, var in knife_vars.items():
        if var.get() == 1:  # If the checkbox is selected
            total += knives[knife]
    total_label.config(text=f"Total: ${total}")

# Function to handle purchase
def purchase():
    selected_knives = [knife for knife, var in knife_vars.items() if var.get() == 1]
    if selected_knives:
        messagebox.showinfo("Purchase", f"You bought: {', '.join(selected_knives)}!")
    else:
        messagebox.showwarning("No selection", "Please select at least one knife to purchase.")

# Create labels and checkboxes
knife_vars = {}
for knife, price in knives.items():
    var = tk.IntVar()
    chk = tk.Checkbutton(root, text=f"{knife} - ${price}", variable=var, command=update_price)
    chk.pack(anchor='w')
    knife_vars[knife] = var

# Display total price
total_label = tk.Label(root, text="Total: $0")
total_label.pack()

# Purchase button
purchase_button = tk.Button(root, text="Purchase", command=purchase)
purchase_button.pack(pady=10)

# Run the application
root.mainloop()
