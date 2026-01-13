import os
import csv
from datetime import datetime

def convert_info_to_dict(label, amount, category, description, entry_type):
    """Converts the input information to a dictionary."""
    return {
        "Label": str(label),
        "Amount": float(amount),
        "Category": category,
        "Description": description,
        "Type": entry_type
    }

def load_from_csv(filename="data.csv"):
    """Loads all entries from a CSV file as a list of dicts."""
    entries = []
    if not os.path.exists(filename):
        return entries
    
    try:
        with open(filename, "r", encoding="utf-8", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure Amount is treated as a float
                row["Amount"] = float(row["Amount"])
                entries.append(row)
    except Exception as e:
        print(f"Error loading data: {e}")
    
    return entries
def save_to_csv(amount, category, description, entry_type, filename="data.csv"):
    """Saves the data to a CSV file with an auto-incrementing Label."""
    entries = load_from_csv(filename)
    # Calculate next Label ID
    if not entries:
        counter = 1
    else:
        # Get the label of the last entry and add 1
        counter = int(entries[-1].get("Label", 0)) + 1

    data = convert_info_to_dict(counter, amount, category, description, entry_type)
    header = ["Label", "Amount", "Category", "Description", "Type"]
    
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    with open(filename, "a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    print(f"Saved entry with Label {counter}")

def delete_data(target_label, filename="data.csv"):
    """Deletes a specific data dict based on its Label."""
    entries = load_from_csv(filename)
    
    initial_count = len(entries)
    # Filter out the row with the target label
    new_rows = [row for row in entries if str(row.get("Label")) != str(target_label)]
    
    if len(new_rows) == initial_count:
        print(f"Label {target_label} not found.")
        return

    header = ["Label", "Amount", "Category", "Description", "Type"]
    with open(filename, "w", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(new_rows)
    
    print(f"Successfully deleted Label {target_label}")

def append_summary_report(data, filename="summary_report.txt"):
    """Appends a summary report to a text file."""
    with open(filename, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Summary report ({timestamp})\n")
        file.write("=================\n")
        file.write(f"Total amount: {data.get('Amount', 0)}\n")
        file.write(f"Category: {data.get('Category', '')}\n")
        file.write(f"Description: {data.get('Description', '')}\n")
        file.write(f"Type: {data.get('Type', '')}\n")
        file.write("=================\n")