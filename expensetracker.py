import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date

# create database and table if not present
def setup_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


# function to add expense
def add_expense():
    amt = amount_entry.get()
    cat = category_box.get()
    desc = desc_entry.get()
    dt = date_entry.get()

    # basic validation
    if amt == "" or cat == "" or dt == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        float(amt)
    except ValueError:
        messagebox.showerror("Error", "Amount should be numeric")
        return

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses(amount, category, date, description) VALUES(?,?,?,?)",
        (amt, cat, dt, desc)
    )

    conn.commit()
    conn.close()

    # clear fields after insert
    amount_entry.delete(0, END)
    category_box.set("")
    desc_entry.delete(0, END)
    date_entry.delete(0, END)
    date_entry.insert(0, str(date.today()))

    load_data()
    messagebox.showinfo("Success", "Expense added successfully")


# load data into table
def load_data():
    table.delete(*table.get_children())

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()
    conn.close()

    for i, row in enumerate(rows, start=1):
        table.insert("", END, values=(i, row[1], row[2], row[3], row[4]))


# delete all records
def clear_all():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all data?"):
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()
        load_data()


# delete selected record
def delete_selected():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a record first")
        return

    if not messagebox.askyesno("Confirm", "Delete selected expense?"):
        return

    sr_no = table.item(selected)["values"][0]

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM expenses")
    ids = cur.fetchall()

    if sr_no <= len(ids):
        cur.execute("DELETE FROM expenses WHERE id=?", (ids[sr_no - 1][0],))
        conn.commit()

    conn.close()
    load_data()


# ---------------- GUI PART ----------------
root = Tk()
root.title("Expense Tracker")
root.geometry("650x500")
root.configure(bg="lightblue")

Label(root, text="Amount:", bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky=W)
amount_entry = Entry(root)
amount_entry.grid(row=0, column=1)

Label(root, text="Category:", bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky=W)
category_box = ttk.Combobox(root, values=["Food", "Travel", "Shopping", "Bills", "Other"])
category_box.grid(row=1, column=1)

Label(root, text="Date:", bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky=W)
date_entry = Entry(root)
date_entry.grid(row=2, column=1)
date_entry.insert(0, str(date.today()))

Label(root, text="Description:", bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky=W)
desc_entry = Entry(root)
desc_entry.grid(row=3, column=1)

Button(root, text="Add Expense", bg="green", fg="white", command=add_expense).grid(row=4, column=0, pady=10)
Button(root, text="Clear All", bg="red", fg="white", command=clear_all).grid(row=4, column=1)
Button(root, text="Delete Selected", bg="orange", command=delete_selected).grid(row=4, column=2)

cols = ("S.No", "Amount", "Category", "Date", "Description")
table = ttk.Treeview(root, columns=cols, show="headings")

for c in cols:
    table.heading(c, text=c)
    table.column(c, width=120)

table.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

setup_db()
load_data()
root.mainloop()