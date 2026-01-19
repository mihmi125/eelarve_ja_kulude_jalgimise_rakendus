from tkinter import *           # Core Tkinter library
from tkinter import ttk         # For themed widgets with a modern look
from tkinter import messagebox  # For displaying message boxes
from logic import *             # Import functions from logic.py
from file_read import load_from_csv, save_to_csv, delete_data  # Import specific functions from file_read.py

# --- FUNCTION DEFINITIONS ---

# --- Refreshes the UI components ---
def refresh_ui():
    refresh_table()
    show_stats()

# --- Refreshes the table with current data ---
def refresh_table():
    # -Clear existing rows-
    for row in tree.get_children():
        tree.delete(row)
    
    # -Load entries from CSV-
    entries = load_from_csv()
    
    # -Insert entries into the treeview-
    for entry in entries:
        tree.insert("", "end", values=(
            entry["Label"],
            entry["Amount"],
            entry["Category"],
            entry["Description"],
            entry["Type"]
        ))

# --- Adds a new entry based on user input ---
def add_entry():
    amount = txtbox1.get()
    description = desc_entry.get()
    category = selected_option.get()
    entry_type = type_var.get()

    # -Validation check: Stop the process if the user entered non-numeric characters-
    if entry_type == "Income":
        value = calculate(amount, 0)
    else:
        value = calculate(0, amount)
    if value == "Invalid":
        messagebox.showwarning("Input Error", "Please enter a valid amount.")
        return
    
    # -Prepare data dictionary for the summary report generator-
    report = {
        "Amount": amount,
        "Category": category,
        "Description": description,
        "Type": entry_type
    }
    append_summary_report(report)

    # -Save the new data to the CSV file and update the interface-
    save_to_csv(amount, category, description, entry_type)
    refresh_ui()

    # -Reset input fields for the next transaction-
    txtbox1.delete(0, END)
    desc_entry.delete(0, END)

# --- Deletes the selected row from the table and data source ---
def delete_selected():
    selected_item = tree.selection() # -Returns ID of selected row-
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to delete.")
        return
    
    # -Retrieve the values of the selected row to identify the unique label/ID-
    item_values = tree.item(selected_item)["values"]
    target_label = item_values[0]  # -Assuming Label is the first column-

    # -Remove data from file and refresh the table to show changes-
    delete_data(target_label)
    refresh_ui()

# --- Shows the total balance calculated from all CSV entries ---
# -Updates the statbox label with the current balance-
def show_stats(*args):
    entries = load_from_csv()
    category_entries = filter_out_category(entries, selected_option.get())
    total_balance = calculate_total_recursive(entries)
    category_balance = calculate_total_recursive(category_entries)
    balanceboxlabel.config(text=f"Balance: {total_balance}€")
    selected_category_label.config(text=f"Selected Category: {category_balance}€")

# ---- MAIN GUI SETUP ----

frame = Tk()
frame.title("Eelarve ja kulude j6lgimise rakendus")
frame.geometry("900x600")                               # Sets window size

# --- Input Frame: Groups input widgets together ---
input_frame = ttk.LabelFrame(frame, text="Add New Transaction", padding=10)
input_frame.pack(pady=10, fill="x", padx=10)

# --- Income/expense value box ---
label1 = ttk.Label(input_frame, text="Enter Amount:")
label1.grid(row=0, column=0)
txtbox1 = ttk.Entry(input_frame)
txtbox1.grid(row=0, column=1, padx=5)

# --- Radiobuttons: Toggle between Income and Expense types --- 
type_var = StringVar(value="Income")  # Default type is "Income"; can be "Income" or "Expense"
Radiobutton(input_frame, text="Income", variable=type_var, value="Income").grid(row=0, column=4)
Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense").grid(row=0, column=5)

# --- Add button: Executes the entry logic ---
button1 = ttk.Button(input_frame, text="Add", command=add_entry)
button1.grid(row=0, column=7, padx=5)

# --- Description box ---
ttk.Label(input_frame, text="Description:").grid(row=0, column=2)
desc_entry = ttk.Entry(input_frame, width=20)
desc_entry.grid(row=0, column=3, padx=5)

# --- Drop Down Menu: Pre-defined categories for better data organization ---
options = ["Toit", "Transport", "Meelelahutus", "Muu"]

selected_option = StringVar()

dropdown = ttk.Combobox(input_frame, textvariable=selected_option, values=options, state="readonly", width=16)
dropdown.grid(row=0, column=6, padx=5)
dropdown.set("Select Category") # Sets the default text
dropdown.bind("<<ComboboxSelected>>", show_stats)

category = dropdown.get()
print(f"User selected: {category}")

# --- Data Table ---
tree_frame = ttk.Frame(frame, padding=10)
tree_frame.pack(fill="both", expand=True)
tree = ttk.Treeview(tree_frame, show="headings", columns=("ID", "Amount", "Category", "Description", "Type"))

# -Define Column Headings-
tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Type", text="Type")

# -Define Column Widths-
tree.column("ID", width=50)
tree.column("Amount", width=100)
tree.column("Category", width=100)
tree.column("Description", width=150)
tree.column("Type", width=100)

tree.pack(side=LEFT, fill="both", expand=True)

# --- Scrollbar for the data table ---
scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill="y")

# --- Delete button: Placed outside the table frame ---
delete_button = ttk.Button(frame, text="Delete Selected Row", command=delete_selected)
delete_button.pack(pady=5)

# --- Stats box: Large label to display current financial status ---
balanceboxlabel = ttk.Label(frame, text="Balance: 0€", font=("Arial", 12, "bold"), foreground="blue")
balanceboxlabel.pack(pady=19)
selected_category_label = ttk.Label(frame, text="Selected Category: 0€", font=("Arial", 12, "bold"), foreground="blue")
selected_category_label.pack(pady=19)

# --- Initial call to populate the table when the app starts ---
refresh_ui()
# --- Start the Tkinter event loop ---
frame.mainloop()