
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import datetime

# Database Connection
con = sqlite3.connect('restaurant.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS restaurant (
    OrderID TEXT PRIMARY KEY,
    CustomerName TEXT,
    Mobile TEXT,
    FoodName TEXT,
    Quantity TEXT,
    Price TEXT,
    Total TEXT,
    Tax TEXT,
    GrandTotal TEXT,
    Date TEXT
)''')
con.commit()

root = tk.Tk()
root.title("RESTAURANT MANAGEMENT SYSTEM")
root.geometry("1400x820")
root.config(bg="#A9CCE3")

# Title
title_frame = tk.Frame(root, bd=5, relief=tk.RIDGE, bg="#D6EAF8")
title_frame.pack(fill=tk.X, padx=5, pady=5)
tk.Label(title_frame, text="RESTAURANT MANAGEMENT SYSTEM", font=("Arial", 26, "bold"),
         bg="#D6EAF8", fg="#154360").pack(pady=10)

# Main Frame
main_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#A9CCE3")
main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

left_frame = tk.LabelFrame(main_frame, text="Customer Details", font=("Arial", 12, "bold"), bg="#A9CCE3", bd=3)
left_frame.place(x=10, y=10, width=750, height=460)

right_frame = tk.LabelFrame(main_frame, text="Menu & Bill", font=("Arial", 12, "bold"), bg="#A9CCE3", bd=3)
right_frame.place(x=770, y=10, width=600, height=460)

# Variables
OrderID = tk.StringVar()
CustomerName = tk.StringVar()
Mobile = tk.StringVar()
FoodName = tk.StringVar()
Quantity = tk.StringVar()
Price = tk.StringVar()
Total = tk.StringVar()
Tax = tk.StringVar()
GrandTotal = tk.StringVar()
DateVar = tk.StringVar()
DateVar.set(datetime.now().strftime("%d/%m/%Y"))
OrderID.set(str(random.randint(1000, 9999)))

# Menu with Price
menu_items = {
    "Veg Biryani": 180, "Chicken Biryani": 250, "Paneer Butter Masala": 200,
    "Chicken Curry": 220, "Veg Fried Rice": 150, "Chicken Fried Rice": 190,
    "Masala Dosa": 80, "Idli Sambar": 60, "Vada Pav": 30,
    "Pizza Margherita": 299, "Veg Burger": 99, "French Fries": 70,
    "Cold Drink": 40, "Ice Cream": 50, "Gulab Jamun": 60, "Tea/Coffee": 30
}

# Left Fields
def add_field(text, var, row, col):
    tk.Label(left_frame, text=text, font=("Arial", 11, "bold"), bg="#A9CCE3").grid(row=row, column=col, sticky="w", padx=10, pady=12)
    tk.Entry(left_frame, textvariable=var, font=("Arial", 11), width=28, bd=2).grid(row=row, column=col+1, padx=10)

add_field("Order ID:", OrderID, 0, 0)
add_field("Customer Name:", CustomerName, 1, 0)
add_field("Mobile No:", Mobile, 2, 0)
add_field("Food Name:", FoodName, 3, 0)
add_field("Quantity:", Quantity, 4, 0)
add_field("Price Rs:", Price, 0, 2)
add_field("Total Rs:", Total, 1, 2)
add_field("Tax (5%) Rs:", Tax, 2, 2)
add_field("Grand Total Rs:", GrandTotal, 3, 2)
add_field("Date:", DateVar, 4, 2)

# Right Side - Menu List
tk.Label(right_frame, text="Select Food Item", bg="#A9CCE3", font=("Arial", 10, "bold")).place(x=10, y=10)
menu_list = tk.Listbox(right_frame, font=("Arial", 11), height=15, width=25)
menu_list.place(x=10, y=35, width=200, height=300)
for item in menu_items:
    menu_list.insert(tk.END, item)

tk.Label(right_frame, text="Bill Receipt", bg="#A9CCE3", font=("Arial", 10, "bold")).place(x=230, y=10)
txt_bill = tk.Text(right_frame, font=("Courier", 10), width=42, height=20, bd=2)
txt_bill.place(x=230, y=35, width=350, height=300)

def select_menu(event):
    selected = menu_list.get(menu_list.curselection())
    FoodName.set(selected)
    Price.set(str(menu_items[selected]))
    Quantity.set("1")
    calculate()

menu_list.bind("<<ListboxSelect>>", select_menu)

# Functions
def calculate():
    try:
        if Quantity.get() == "" or Price.get() == "":
            return
        q = int(Quantity.get())
        p = float(Price.get())
        t = q * p
        tax = t * 0.05
        grand = t + tax
        Total.set(f"{t:.2f}")
        Tax.set(f"{tax:.2f}")
        GrandTotal.set(f"{grand:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Enter valid Quantity and Price\n{e}")

def generate_bill():
    txt_bill.delete("1.0", tk.END)
    txt_bill.insert(tk.END, f"\tWelcome to Food Court\n")
    txt_bill.insert(tk.END, f"----------------------------------------\n")
    txt_bill.insert(tk.END, f"Order ID: {OrderID.get()}\n")
    txt_bill.insert(tk.END, f"Customer: {CustomerName.get()}\n")
    txt_bill.insert(tk.END, f"Mobile: {Mobile.get()}\n")
    txt_bill.insert(tk.END, f"Date: {DateVar.get()}\n")
    txt_bill.insert(tk.END, f"----------------------------------------\n")
    txt_bill.insert(tk.END, f"Food: {FoodName.get()}\n")
    txt_bill.insert(tk.END, f"Qty: {Quantity.get()} Price: {Price.get()}\n")
    txt_bill.insert(tk.END, f"Total: Rs {Total.get()}\n")
    txt_bill.insert(tk.END, f"Tax: Rs {Tax.get()}\n")
    txt_bill.insert(tk.END, f"Grand Total: Rs {GrandTotal.get()}\n")
    txt_bill.insert(tk.END, f"----------------------------------------\n")
    txt_bill.insert(tk.END, f"\tThank You Visit Again\n")

def add_data():
    if CustomerName.get() == "" or Mobile.get() == "" or FoodName.get() == "":
        messagebox.showerror("Error", "Fill Customer Name, Mobile, Food Name")
        return
    try:
        cur.execute("INSERT INTO restaurant VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (OrderID.get(), CustomerName.get(), Mobile.get(), FoodName.get(),
                     Quantity.get(), Price.get(), Total.get(), Tax.get(), GrandTotal.get(), DateVar.get()))
        con.commit()
        show_data()
        generate_bill()
        messagebox.showinfo("Success", "Order Added Successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Order ID already exists. Click RESET")

def show_data():
    for row in tree.get_children():
        tree.delete(row)
    for row in cur.execute("SELECT * FROM restaurant"):
        tree.insert("", tk.END, values=row)

def update_data():
    sel = tree.focus()
    if not sel:
        messagebox.showerror("Error", "Select row from table first")
        return
    cur.execute("UPDATE restaurant SET CustomerName=?, Mobile=?, FoodName=?, Quantity=?, Price=?, Total=?, Tax=?, GrandTotal=?, Date=? WHERE OrderID=?",
                (CustomerName.get(), Mobile.get(), FoodName.get(), Quantity.get(), Price.get(), Total.get(), Tax.get(), GrandTotal.get(), DateVar.get(), OrderID.get()))
    con.commit()
    show_data()
    messagebox.showinfo("Updated", "Record Updated")

def delete_data():
    sel = tree.focus()
    if not sel:
        messagebox.showerror("Error", "Select row from table")
        return
    oid = tree.item(sel)['values'][0]
    cur.execute("DELETE FROM restaurant WHERE OrderID=?", (oid,))
    con.commit()
    show_data()
    messagebox.showinfo("Deleted", "Record Deleted")

def reset_data():
    OrderID.set(str(random.randint(1000, 9999)))
    CustomerName.set(""); Mobile.set(""); FoodName.set(""); Quantity.set("")
    Price.set(""); Total.set(""); Tax.set(""); GrandTotal.set("")
    DateVar.set(datetime.now().strftime("%d/%m/%Y"))
    txt_bill.delete("1.0", tk.END)

def on_select_table(event):
    sel = tree.focus()
    if not sel: return
    vals = tree.item(sel)['values']
    OrderID.set(vals[0]); CustomerName.set(vals[1]); Mobile.set(vals[2]); FoodName.set(vals[3])
    Quantity.set(vals[4]); Price.set(vals[5]); Total.set(vals[6]); Tax.set(vals[7]); GrandTotal.set(vals[8]); DateVar.set(vals[9])
    generate_bill()

# Buttons on left
btn_cal = tk.Frame(left_frame, bg="#A9CCE3")
btn_cal.grid(row=5, column=0, columnspan=4, pady=15)
tk.Button(btn_cal, text="CALCULATE", bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=15, command=calculate).pack(side=tk.LEFT, padx=10)
tk.Button(btn_cal, text="GENERATE BILL", bg="#8E44AD", fg="white", font=("Arial", 10, "bold"), width=15, command=generate_bill).pack(side=tk.LEFT, padx=10)
tk.Button(btn_cal, text="NEW ID", bg="#2E86C1", fg="white", font=("Arial", 10, "bold"), width=10, command=lambda: OrderID.set(str(random.randint(1000,9999)))).pack(side=tk.LEFT, padx=10)

# Bottom Table
table_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
table_frame.pack(fill=tk.X, padx=5, pady=2)
cols = ("OrderID","CustomerName","Mobile","FoodName","Quantity","Price","Total","Tax","GrandTotal","Date")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=7)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=120, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_select_table)

# Bottom Buttons - SAME TYPE AS YOUR LIBRARY PHOTO
btn_frame = tk.Frame(root, bg="#2E5090", bd=4, relief=tk.RIDGE)
btn_frame.pack(fill=tk.X, padx=5, pady=5)

tk.Button(btn_frame, text="ADD DATA", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=add_data).grid(row=0, column=0, padx=12, pady=10)
tk.Button(btn_frame, text="SHOW DATA", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=show_data).grid(row=0, column=1, padx=12, pady=10)
tk.Button(btn_frame, text="UPDATE", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=update_data).grid(row=0, column=2, padx=12, pady=10)
tk.Button(btn_frame, text="DELETE", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=delete_data).grid(row=0, column=3, padx=12, pady=10)
tk.Button(btn_frame, text="RESET", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=reset_data).grid(row=0, column=4, padx=12, pady=10)
tk.Button(btn_frame, text="EXIT", bg="#C0392B", fg="white", font=("Arial", 11, "bold"), width=16, bd=3, command=root.quit).grid(row=0, column=5, padx=12, pady=10)

show_data()
root.mainloop()