import tkinter as tk
from tkinter import ttk, messagebox
import os


FILE_NAME = "expenses.txt"


# LOAD EXPENSES


def load_expenses():
    expenses = []

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r", encoding="utf-8") as file:

            for line in file:

                data = line.strip().split(",")

                if len(data) == 2:

                    category = data[0]

                    try:
                        amount = float(data[1])

                        expenses.append({
                            "category": category,
                            "amount": amount
                        })

                    except ValueError:
                        pass

    return expenses


# SAVE EXPENSES


def save_expenses():

    with open(FILE_NAME, "w", encoding="utf-8") as file:

        for expense in expenses:

            file.write(
                f"{expense['category']},{expense['amount']}\n"
            )


# ADD EXPENSE


def add_expense():

    category = category_var.get().strip()
    amount_text = amount_entry.get().strip()

    # Check category
    if category == "":

        messagebox.showwarning(
            "Missing Category",
            "Please select a category."
        )

        return

    # Check amount
    if amount_text == "":

        messagebox.showwarning(
            "Missing Amount",
            "Please enter an amount."
        )

        return

    # Convert amount
    try:

        amount = float(amount_text)

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return

    # Amount cannot be negative
    if amount <= 0:

        messagebox.showwarning(
            "Invalid Amount",
            "Amount must be greater than 0."
        )

        return

    # Add to list
    expenses.append({
        "category": category,
        "amount": amount
    })

    # Save
    save_expenses()

    # Update screen
    refresh_expenses()

    # Clear amount box
    amount_entry.delete(0, tk.END)

    # Reset category
    category_var.set("Food")

    messagebox.showinfo(
        "Expense Added",
        f"₹{amount:,.2f} added to {category}."
    )


# DELETE SELECTED EXPENSE


def delete_expense():

    selected = expense_tree.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense first."
        )

        return

    item = selected[0]

    index = expense_tree.index(item)

    expense = expenses[index]

    confirm = messagebox.askyesno(
        "Delete Expense",
        f"Are you sure you want to delete?\n\n{expense['category']} ₹{expense['amount']:,.2f}"
    )

    if confirm:

        expenses.pop(index)

        save_expenses()

        refresh_expenses()


# CLEAR ALL DATA


def clear_all_data():

    if len(expenses) == 0:

        messagebox.showinfo(
            "No Data",
            "There is no expense data to delete."
        )

        return

    confirm = messagebox.askyesno(
        "Clear All Data",
        "⚠ WARNING\n\n"
        "This will delete ALL expense records.\n\n"
        "This action cannot be undone.\n\n"
        "Do you want to continue?"
    )

    if confirm:

        # Clear memory
        expenses.clear()

        # Clear file
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write("")

        # Update screen
        refresh_expenses()

        messagebox.showinfo(
            "Data Cleared",
            "All old expense data has been deleted."
        )


# REFRESH EXPENSE LIST


def refresh_expenses():

    # Remove old rows
    for item in expense_tree.get_children():

        expense_tree.delete(item)

    # Calculate total
    total = 0

    # Add rows
    for expense in expenses:

        expense_tree.insert(
            "",
            tk.END,
            values=(
                expense["category"],
                f"₹{expense['amount']:,.2f}"
            )
        )

        total += expense["amount"]

    # Update total
    total_label.config(
        text=f"₹{total:,.2f}"
    )

    # Update transaction count
    count_label.config(
        text=f"{len(expenses)} Transactions"
    )


# MAIN WINDOW


expenses = load_expenses()

root = tk.Tk()

root.title("Expense Tracker")

root.geometry("900x700")

root.minsize(800, 600)

root.configure(
    bg="#f3f4f6"
)


# STYLE


style = ttk.Style()

style.theme_use("clam")


style.configure(
    "Treeview",
    background="white",
    foreground="#111827",
    rowheight=42,
    fieldbackground="white",
    font=("Segoe UI", 11)
)


style.configure(
    "Treeview.Heading",
    background="#111827",
    foreground="white",
    font=("Segoe UI", 11, "bold"),
    padding=10
)


style.map(
    "Treeview",
    background=[
        ("selected", "#dbeafe")
    ],
    foreground=[
        ("selected", "#111827")
    ]
)


# HEADER

header = tk.Frame(
    root,
    bg="#111827",
    height=100
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title = tk.Label(
    header,
    text="💰 Expense Tracker",
    font=("Segoe UI", 26, "bold"),
    bg="#111827",
    fg="white"
)

title.pack(
    side="left",
    padx=35
)


subtitle = tk.Label(
    header,
    text="Manage your daily expenses",
    font=("Segoe UI", 11),
    bg="#111827",
    fg="#cbd5e1"
)

subtitle.pack(
    side="right",
    padx=35
)


# MAIN AREA

main_frame = tk.Frame(
    root,
    bg="#f3f4f6"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=25
)


# TOTAL CARD

summary_frame = tk.Frame(
    main_frame,
    bg="white",
    height=115
)

summary_frame.pack(
    fill="x",
    pady=(0, 20)
)

summary_frame.pack_propagate(False)


total_title = tk.Label(
    summary_frame,
    text="TOTAL SPENDING",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#6b7280"
)

total_title.pack(
    anchor="w",
    padx=30,
    pady=(20, 0)
)


total_label = tk.Label(
    summary_frame,
    text="₹0.00",
    font=("Segoe UI", 27, "bold"),
    bg="white",
    fg="#111827"
)

total_label.pack(
    anchor="w",
    padx=30
)


count_label = tk.Label(
    summary_frame,
    text="0 Transactions",
    font=("Segoe UI", 11),
    bg="white",
    fg="#6b7280"
)

count_label.place(
    relx=1,
    x=-30,
    rely=0.5,
    anchor="e"
)


# ADD EXPENSE CARD

form_frame = tk.Frame(
    main_frame,
    bg="white"
)

form_frame.pack(
    fill="x",
    pady=(0, 20)
)


form_title = tk.Label(
    form_frame,
    text="Add New Expense",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#111827"
)

form_title.grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="w",
    padx=25,
    pady=(20, 15)
)


# CATEGORY LABEL

category_label = tk.Label(
    form_frame,
    text="Category",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#374151"
)

category_label.grid(
    row=1,
    column=0,
    sticky="w",
    padx=(25, 10)
)


# CATEGORY

category_var = tk.StringVar()

category_combo = ttk.Combobox(
    form_frame,
    textvariable=category_var,
    values=[
        "Food",
        "Rent",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ],
    state="readonly",
    width=20,
    font=("Segoe UI", 11)
)

category_combo.grid(
    row=2,
    column=0,
    padx=(25, 15),
    pady=(5, 20)
)

category_combo.set("Food")


# AMOUNT LABEL

amount_label = tk.Label(
    form_frame,
    text="Amount",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#374151"
)

amount_label.grid(
    row=1,
    column=1,
    sticky="w",
    padx=10
)


# AMOUNT ENTRY

amount_entry = tk.Entry(
    form_frame,
    font=("Segoe UI", 12),
    width=22,
    relief="solid",
    bd=1
)

amount_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=(5, 20)
)


# ADD BUTTON

add_button = tk.Button(
    form_frame,
    text="＋ Add Expense",
    command=add_expense,
    font=("Segoe UI", 11, "bold"),
    bg="#111827",
    fg="white",
    activebackground="#374151",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=22,
    pady=10
)

add_button.grid(
    row=2,
    column=2,
    padx=20,
    pady=(5, 20)
)


# RECENT EXPENSES CARD

list_frame = tk.Frame(
    main_frame,
    bg="white",
    height=300
)

list_frame.pack(
    fill="x"
)

list_frame.pack_propagate(False)


list_title = tk.Label(
    list_frame,
    text="Recent Expenses",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#111827"
)

list_title.pack(
    anchor="w",
    padx=25,
    pady=(15, 8)
)


# TABLE CONTAINER

table_frame = tk.Frame(
    list_frame,
    bg="white",
    height=185
)

table_frame.pack(
    fill="x",
    padx=25
)

table_frame.pack_propagate(False)


# TREEVIEW

expense_tree = ttk.Treeview(
    table_frame,
    columns=("category", "amount"),
    show="headings",
    selectmode="browse"
)


expense_tree.heading(
    "category",
    text="CATEGORY"
)

expense_tree.heading(
    "amount",
    text="AMOUNT"
)


expense_tree.column(
    "category",
    width=400,
    anchor="w"
)

expense_tree.column(
    "amount",
    width=300,
    anchor="e"
)


expense_tree.pack(
    side="left",
    fill="both",
    expand=True
)


# SCROLLBAR

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=expense_tree.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


expense_tree.configure(
    yscrollcommand=scrollbar.set
)


# BUTTON AREA

button_frame = tk.Frame(
    list_frame,
    bg="white",
    height=55
)

button_frame.pack(
    fill="x",
    padx=25,
    pady=(10, 10)
)

button_frame.pack_propagate(False)


# DELETE SELECTED

delete_button = tk.Button(
    button_frame,
    text="🗑 Delete Selected",
    command=delete_expense,
    font=("Segoe UI", 10, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=8
)

delete_button.pack(
    side="left"
)


# CLEAR ALL DATA

clear_button = tk.Button(
    button_frame,
    text="🧹 Clear All Data",
    command=clear_all_data,
    font=("Segoe UI", 10, "bold"),
    bg="#7f1d1d",
    fg="white",
    activebackground="#991b1b",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=8
)

clear_button.pack(
    side="right"
)


# INITIAL DATA LOAD

refresh_expenses()


# START APPLICATION

root.mainloop()