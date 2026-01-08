"""File saving module."""
from datetime import datetime

def convert_info_to_dict(amount, category, description, type):
    """Converts the input information to a dictionary."""
    data = {
        "Amount": amount,
        "Category": category,
        "Description": description,
        "Type": type
    }
    return data

def save_to_CSV(data, filename="data.csv"):
    """Saves the data  to a CSV file."""
    with open(filename, "w", encoding="utf-8") as file:
        for key, value in data.items():
            file.write(f"{key}; {value}\n")

def load_from_CSV(filename="data.csv"):
    """Loads the data from a CSV file."""
    data = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split("; ")
                if key == "Amount":
                    value = float(value)
                data[key] = value
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return data

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