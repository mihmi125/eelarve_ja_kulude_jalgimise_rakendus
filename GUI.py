from tkinter import *
from tkinter import ttk         # platvormi ühise stiili saamiseks
from tkinter import messagebox
from logic import *
from file_read import *

def refresh_ui():
    refresh_table()
    show_stats()

def refresh_table():
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    
    # Load entries from CSV
    entries = load_from_csv()
    
    # Insert entries into the treeview
    for entry in entries:
        tree.insert("", "end", values=(
            entry["Label"],
            entry["Amount"],
            entry["Category"],
            entry["Description"],
            entry["Type"]
        ))

def add_entry():
    amount = txtbox1.get()
    description = desc_entry.get()
    category = selected_option.get()
    entry_type = type_var.get()

    if entry_type == "income":
        value = calculate(amount, 0)
    else:
        value = calculate(0, amount)
    if value == "Invalid":
        messagebox.showwarning("Input Error", "Please enter a valid amount.")
        return

    report = {
        "Amount": amount,
        "Category": category,
        "Description": description,
        "Type": entry_type
    }
    append_summary_report(report)

    save_to_csv(amount, category, description, entry_type)
    refresh_ui()
    txtbox1.delete(0, END)
    desc_entry.delete(0, END)

def delete_selected():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to delete.")
        return
    
    item_values = tree.item(selected_item)["values"]
    target_label = item_values[0]  # Assuming Label is the first column

    delete_data(target_label)
    refresh_ui()

def show_stats():
    entries = load_from_csv()
    total_balance = calculate_total_recursive(entries)
    statboxlabel.config(text=f"Balance: {total_balance}€")


frame = Tk()
frame.title("Eelarve ja kulude j6lgimise rakendus")
frame.geometry("900x600")

input_frame = ttk.LabelFrame(frame, text="Add New Transaction", padding=10)
input_frame.pack(pady=10, fill="x", padx=10)

# Income/expense value box
label1 = ttk.Label(input_frame, text="Enter Income:")
label1.grid(row=0, column=0)
txtbox1 = ttk.Entry(input_frame)
txtbox1.grid(row=0, column=1, padx=5)

# Checkboxes 
type_var = StringVar(value="Income") # 1 for Income, 2 for Expense
Radiobutton(input_frame, text="Income", variable=type_var, value="Income").grid(row=0, column=4)
Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense").grid(row=0, column=5)

# Button 1
button1 = ttk.Button(input_frame, text="Add", command=add_entry)
button1.grid(row=0, column=7, padx=5)

# Description box
ttk.Label(input_frame, text="Description:").grid(row=0, column=2)
desc_entry = ttk.Entry(input_frame, width=20)
desc_entry.grid(row=0, column=3, padx=5)

# Drop Down Menu
options = ["Toit", "Transport", "Meelelahutus", "Muu"]

selected_option = StringVar()

dropdown = ttk.Combobox(input_frame, textvariable=selected_option, values=options, state="readonly", width=16)
dropdown.grid(row=0, column=6, padx=5) # Adjust coordinates to fit your GUI
dropdown.set("Select Category") # Set the default text

category = dropdown.get()
print(f"User selected: {category}")

# Tree
tree_frame = ttk.Frame(frame, padding=10)
tree_frame.pack(fill="both", expand=True)
tree = ttk.Treeview(tree_frame, show="headings", columns=("ID", "Amount", "Category", "Description", "Type"))
tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Type", text="Type")
tree.column("ID", width=50)
tree.column("Amount", width=100)
tree.column("Category", width=100)
tree.column("Description", width=150)
tree.column("Type", width=100)

tree.pack(side=LEFT, fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill="y")

#Delete button
delete_button = ttk.Button(frame, text="Delete Selected Row", command=delete_selected)
delete_button.pack(pady=5)

# Stats box
statboxlabel = ttk.Label(frame, text="Balance: 0€", font=("Arial", 12, "bold"), foreground="blue")
statboxlabel.pack(pady=19)

refresh_ui()
frame.mainloop()