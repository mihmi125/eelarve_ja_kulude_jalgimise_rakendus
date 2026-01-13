from tkinter import *
from tkinter import ttk         # platvormi ühise stiili saamiseks
from tkinter import messagebox
from logic import *

frame = Tk()
frame.title("Eelarve ja kulude j6lgimise rakendus")
frame.geometry("900x400")


# Income/expense value box
label1 = ttk.Label(frame, text="Enter Income:")
label1.grid(row=0, column=0, pady=5)
txtbox1 = ttk.Entry(frame)
txtbox1.grid(row=0, column=1, pady=5)

# Checkboxes 
label2 = ttk.Label(frame, text="Enter Expenses:")
label2.grid(row=0, column=2, pady=5)
txtbox2 = ttk.Entry(frame)
txtbox2.grid(row=0, column=3, pady=5)

# Button 1
button1 = ttk.Button(frame, text="Calculate!!!")
button1.grid(row=3, column=0, pady=5)

# Drop Down Menu
options = ["Toit", "Transport", "Meelelahutus", "Muu"]

selected_option = StringVar()

dropdown = ttk.Combobox(frame, textvariable=selected_option, values=options)
dropdown.grid(row=2, column=1, pady=5) # Adjust coordinates to fit your GUI
dropdown.set("Select Category") # Set the default text

category = dropdown.get()
print(f"User selected: {category}")


# Sum box
sumboxlabel = ttk.Label(frame, text="Sum will be displayed here:")
sumboxlabel.grid(row=0, column=4, pady=5)

sumbox = ttk.Label(frame, text="")
sumbox.grid(row=1, column=4, pady=5)

def display_sum():
    # 1. Get strings from the entry boxes
    num1 = txtbox1.get()
    num2 = txtbox2.get()
    
    # 2. Use your logic.py calculate function
    result = calculate(num1, num2)
    
    # 3. Updates the sumbox label with the result
    if result == "Invalid":
        sumbox.config(text="Error: Invalid Input", foreground="red")
    else:
        sumbox.config(text=f"Total: {result}", foreground="black")

# Makes button work
button1.config(command=display_sum)


#Total sum + button
totalsum_button = ttk.Button(frame, text="Calculate Total Sum")
totalsum_button.grid(row=4, column=4, pady=5)

totalsum_label = ttk.Label(frame, text="Total Sum is Displayed here:")
totalsum_label.grid(row=4, column=5, pady=5)

def display_totalsum():
    # Uses saved logs to calculate
    result = calculate_total_recursive()
    totalsum_label.config(text=f"Total: {result}", foreground="black")


frame.mainloop()