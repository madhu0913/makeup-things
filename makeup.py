import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="makeupdb"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


def fetch_products():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM cosmetics")
        products = cursor.fetchall()
        conn.close()
        return products
    return []


def add_to_cart():
    selected_items = product_table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "No product selected!")
        return
   
    for item in selected_items:
        cart_table.insert("", tk.END, values=product_table.item(item, "values"))
    calculate_total()
    update_total_products()


def remove_from_cart():
    selected_items = cart_table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "No item selected!")
        return

    for item in selected_items:
        cart_table.delete(item)
    calculate_total()
    update_total_products()


def calculate_total():
    total = sum(float(cart_table.item(item, "values")[1][3:]) for item in cart_table.get_children())
    total_label.config(text=f"Total: Rs {total:.2f}")


def update_total_products():
    total_products = len(cart_table.get_children())
    total_products_label.config(text=f"Total Products: {total_products}")


def checkout():
    if not cart_table.get_children():
        messagebox.showinfo("Cart Empty", "Your cart is empty!")
        return

    messagebox.showinfo("Success", "Purchase Successful!")
    cart_table.delete(*cart_table.get_children())
    total_label.config(text="Total: Rs 0.00")
    update_total_products()


root = tk.Tk()
root.configure(bg="lightpink")
root.title("Makeup & Cosmetics Store")
root.geometry("600x500")


tk.Label(root, text="Available Makeup Products", font=("Arial", 14, "bold"), bg="lightpink").pack()
product_table = ttk.Treeview(root, columns=("Name", "Price"), show="headings")
product_table.heading("Name", text="Product Name")
product_table.heading("Price", text="Price")
product_table.pack()


sample_products = [
    ("Lipstick", 150),
    ("Foundation", 300),
    ("Eyeliner", 120),
    ("Mascara", 150),
    ("Blush", 199),
    ("Highlighter", 229),
    ("Compact Powder", 149),
    ("Concealer", 279),
    ("Makeup Remover", 109),
    ("Face Primer", 279)
]
for product in sample_products:
    product_table.insert("", tk.END, values=(product[0], f"Rs {product[1]:.2f}"))

tk.Button(root, text="Add to Cart", command=add_to_cart, bg="purple", fg="white").pack(pady=5)

tk.Button(root, text="View Menu", command=lambda: messagebox.showinfo("Menu", "Lipstick, Foundation, Eyeliner, Mascara, Blush, Highlighter, Compact Powder, Concealer, Makeup Remover, Face Primer"), bg="blue", fg="white").pack(pady=5)


tk.Label(root, text="Shopping Cart", font=("Arial", 14, "bold"), bg="lightpink").pack()
cart_table = ttk.Treeview(root, columns=("Name", "Price"), show="headings")
cart_table.heading("Name", text="Product Name")
cart_table.heading("Price", text="Price")
cart_table.pack()

tk.Button(root, text="Remove", command=remove_from_cart, bg="red", fg="white").pack(pady=5)


total_label = tk.Label(root, text="Total: Rs 0.00", font=("Arial", 14, "bold"), bg="lightpink")
total_label.pack()
total_products_label = tk.Label(root, text="Total Products: 0", font=("Arial", 14, "bold"), bg="lightpink")
total_products_label.pack()
tk.Button(root, text="Place Order", command=checkout, bg="orange", fg="white").pack(pady=5)


root.mainloop()


