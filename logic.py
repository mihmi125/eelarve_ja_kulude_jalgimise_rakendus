def income(number):
    """Attempts to convert a given input into a float for income processing."""
    try:
        return float(number)
    except ValueError:
        return "Warning: The entered income is not valid."


def expenses(number):
    """Attempts to convert a given input into a float for expense processing."""
    try:
        return float(number)
    except ValueError:
        return "Warning: The entered expenses value is not valid."

def calculate(income_val, expenses_val):
    """Calculates the net balance. Returns Invalid for bad inputs."""
    my_income = income(income_val)
    my_expenses = expenses(expenses_val)

    #Check types FIRST (Must be floats to avoid crash)
    if isinstance(my_income, float) and isinstance(my_expenses, float):
        
        #Check if inputs are negative
        if my_income < 0 or my_expenses < 0:
            return "Invalid"

        #Calculate
        amount = my_income - my_expenses
        return round(amount, 2)
    else:
        # Returns Invalid if types were not floats
        return "Invalid"

def calculate_total_recursive(entries):
    """
    Calculates the total net balance from a list of dictionaries using recursion.
    Treats 'expense' types as negative values.
    """
    # Base Case: If the list is empty, return 0
    if not entries:
        return 0
    
    # Process the first item in the current list
    current = entries[0]
    val = float(current["Amount"])
    
    # If the entry is an expense, subtract it from the total
    if current["Type"].lower() == "expense":
        val = -val
        
    # Recursive Step: Add the current value to the result of the rest of the list
    return val + calculate_total_recursive(entries[1:])