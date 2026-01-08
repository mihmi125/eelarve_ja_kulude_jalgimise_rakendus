"""File saving module."""
from datetime import datetime

def convert_info_to_dict(label, amount, category, description, type):
    """Converts the input information to a dictionary."""
    data = {
        "Label": label,
        "Amount": amount,
        "Category": category,
        "Description": description,
        "Type": type
    }
    return data

def save_to_CSV(amount, category, description, type, filename="data.csv"):
    """Saves the data to a CSV file."""

    last_entry = load_from_CSV(filename)
    counter = int(last_entry.get("Label", 0)) + 1

    data = convert_info_to_dict(counter, amount, category, description, type)

    with open(filename, "a", encoding="utf-8") as file:
        for key, value in data.items():
            file.write(f"{key}; {value}\n")
    
    print(f"Saved data with Label: {counter}")

def load_from_CSV(filename="data.csv"):
    """Loads the data from a CSV file."""
    data = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if "; " in line:
                    key, value = line.strip().split("; ", 1)
                    if key == "Amount":
                        value = float(value)
                    data[key] = value
    except FileNotFoundError:
        pass 
    return data

def delete_data(target_label, filename="data.csv"):
    """Deletes a specific data dict based on its Label."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return

    with open(filename, "w", encoding="utf-8") as file:
        skip = False
        deleted = False
        
        for line in lines:
            if line.startswith("Label;"):
                parts = line.strip().split("; ")
                if len(parts) > 1 and str(parts[1]) == str(target_label):
                    skip = True
                    deleted = True
                else:
                    skip = False
            
            if not skip:
                file.write(line)

    if deleted:
        print(f"Successfully deleted Label {target_label}")
    else:
        print(f"Label {target_label} not found")

def save_summary_report(data, filename="summary_report.txt"):
    """Saves a summary report to a text file."""
    with open(filename, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Summary report ({timestamp})\n")
        file.write("=================\n")
        file.write(f"Total amount: {data.get('Amount', 0)}\n")
        file.write(f"Category: {data.get('Category', '')}\n")
        file.write(f"Description: {data.get('Description', '')}\n")
        file.write(f"Type: {data.get('Type', '')}\n")
        file.write("=================\n")


# --- Testing area ---
save_to_CSV(100, "Food", "Dinner", "Expense")
save_to_CSV(200, "Tech", "Mouse", "Expense")
delete_data(4)