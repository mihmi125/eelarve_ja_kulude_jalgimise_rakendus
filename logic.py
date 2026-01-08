
def income(number):
    try:
        return float(number)
    except ValueError:
        print(f"Warning: your entered income is not a valid income.")
        return None


def expenses(number):
    try:
        return float(number)
    except ValueError:
        print(f"Warning: your entered expenses is not a valid expense.")
        return None

def calculate(incomeval, expensesval):
    my_income = income(incomeval)
    my_expenses = expenses(expensesval)

    if my_income is not None and my_expenses is not None:
        Amount = my_income - my_expenses
        print(round(Amount, 2))
    else:
        None
        
mas = calculate(1o, 5)