import os

# Impordime kõik funktsioonid failidest logic.py ja file_read.py
# Nüüd saab kasutada funktsioone otse, ilma eesliiteta (nt calculate() vs logic.calculate())
from logic import *
from file_read import *

# ==========================================
# SISENDI VALIDEERIMINE (3 funktsiooni)
# ==========================================
def validate_symbol_input():
    """Kontrollib, mis juhtub, kui sisestada sümbol numbri asemel ('%')"""
    # Kasutame calculate() otse
    assert calculate('%', 100) == "Invalid"

def validate_negative_input():
    """Kontrollib, et negatiivsed arvud annaksid vea"""
    assert calculate(-50, 10) == "Invalid"

def validate_correct_input():
    """Kontrollib, kas korrektsete arvudega arvutamine töötab (100 - 30 = 70.0)"""
    assert calculate(100, 30) == 70.0

# ==========================================
# SUMMA ARVUTAMINE (3 funktsiooni)
# ==========================================
def sum_mixed_inputs():
    """Kontrollib tulude ja kulude kogusummat"""
    data = [
        {"Amount": 100, "Type": "Income"}, 
        {"Amount": 40, "Type": "Expense"}
    ]
    # Kasutame calculate_total_recursive() otse
    assert calculate_total_recursive(data) == 60.0

def sum_expenses_only():
    """Kontrollib summat, kui on ainult kulud (tulemus peab olema negatiivne)"""
    data = [
        {"Amount": 20, "Type": "Expense"}, 
        {"Amount": 10, "Type": "Expense"}
    ]
    assert calculate_total_recursive(data) == -30.0

def sum_empty_list():
    """Kontrollib tühja nimekirja summat (peab olema 0)"""
    assert calculate_total_recursive([]) == 0 

# ==========================================
# SUMMA ARVUTAMINE KATEGOORIA PÕHISELT (3 funktsiooni)
# ==========================================
# Testandmed kategooriate kontrollimiseks
test_data = [
    {"Category": "Food", "Amount": 15, "Type": "Expense"},
    {"Category": "Work", "Amount": 500, "Type": "Income"},
    {"Category": "Food", "Amount": 5, "Type": "Expense"}
]

def sum_category_food_expense():
    """Kontrollib kategooria 'Food' summat (kulud)"""
    # filter_out_category() on nüüd otse kättesaadav
    filtered_data = filter_out_category(test_data, "Food")
    assert calculate_total_recursive(filtered_data) == -20.0

def sum_category_work_income():
    """Kontrollib kategooria 'Work' summat (tulud)"""
    filtered_data = filter_out_category(test_data, "Work")
    assert calculate_total_recursive(filtered_data) == 500.0

def sum_category_unknown():
    """Kontrollib olematu kategooria summat (peab olema 0)"""
    filtered_data = filter_out_category(test_data, "Sport")
    assert calculate_total_recursive(filtered_data) == 0

# ==========================================
# SISSETULEKU JA VÄLJAMINEKU FUNKTSIOONID (3 funktsiooni)
# ==========================================
def income_valid_number():
    """Kontrollib, kas income() funktsioon töötab numbriga"""
    assert income(100) == 100.0

def expenses_valid_number():
    """Kontrollib, kas expenses() funktsioon töötab numbriga"""
    assert expenses(50) == 50.0

def income_invalid_input():
    """Kontrollib, et income() tagastab hoiatuse sobimatu sisendi puhul"""
    result = income("abc")
    assert isinstance(result, str)
    assert "Warning" in result

# ==========================================
# STRINGI TEISENDAMINE DICTIONARYKS (3 funktsiooni)
# ==========================================
def convert_info_to_dict_valid():
    """Kontrollib convert_info_to_dict() õiget muundamist"""
    result = convert_info_to_dict(1, 100.5, "Food", "Lunch", "Expense")
    assert result["Label"] == "1"
    assert result["Amount"] == 100.5
    assert result["Category"] == "Food"
    assert result["Description"] == "Lunch"
    assert result["Type"] == "Expense"

def convert_info_to_dict_with_string_amount():
    """Kontrollib convert_info_to_dict() stringi summaga"""
    result = convert_info_to_dict(2, "50.75", "Transport", "Taxi", "Expense")
    assert result["Amount"] == 50.75

def convert_info_to_dict_label_as_string():
    """Kontrollib, et Label on alati string"""
    result = convert_info_to_dict(999, 100, "Muu", "Test", "Income")
    assert isinstance(result["Label"], str)
    assert result["Label"] == "999"

# ==========================================
# FILTER KATEGOORIA JÄRGI (3 funktsiooni)
# ==========================================
def filter_single_category():
    """Kontrollib, et filter tagastab ainult valitud kategooria"""
    data = [
        {"Category": "Food", "Amount": 20, "Type": "Expense"},
        {"Category": "Transport", "Amount": 10, "Type": "Expense"}
    ]
    result = filter_out_category(data, "Food")
    assert len(result) == 1
    assert result[0]["Category"] == "Food"

def filter_multiple_same_category():
    """Kontrollib, et filter tagastab kõik sama kategooria read"""
    data = [
        {"Category": "Food", "Amount": 10, "Type": "Expense"},
        {"Category": "Transport", "Amount": 15, "Type": "Expense"},
        {"Category": "Food", "Amount": 5, "Type": "Expense"}
    ]
    result = filter_out_category(data, "Food")
    assert len(result) == 2

def filter_nonexistent_category():
    """Kontrollib, et filtreerimine tagastab tühja nimekirja olematu kategooria jaoks"""
    data = [
        {"Category": "Food", "Amount": 20, "Type": "Expense"}
    ]
    result = filter_out_category(data, "NonExistent")
    assert len(result) == 0

# ==========================================
# KOMPLEKSSED ARVUTUSED (3 funktsiooni)
# ==========================================
def mixed_income_expense_recursive():
    """Kontrollib keerulisemat segast summat"""
    data = [
        {"Amount": 1000, "Type": "Income"},
        {"Amount": 300, "Type": "Expense"},
        {"Amount": 200, "Type": "Income"},
        {"Amount": 150, "Type": "Expense"}
    ]
    assert calculate_total_recursive(data) == 750.0

def all_income_recursive():
    """Kontrollib summat, kui on ainult tulud"""
    data = [
        {"Amount": 100, "Type": "Income"},
        {"Amount": 200, "Type": "Income"}
    ]
    assert calculate_total_recursive(data) == 300.0

def calculate_zero_amounts():
    """Kontrollib arvutamist nullsummadega"""
    data = [
        {"Amount": 0, "Type": "Income"},
        {"Amount": 0, "Type": "Expense"}
    ]
    assert calculate_total_recursive(data) == 0.0

# ==========================================
# KÕIGI TESTIDE KÄIVITAMINE
# ==========================================
if __name__ == "__main__":
    try:
        print("Testide käivitamine...\n")

        # 1. Sisendi valideerimine
        validate_symbol_input()
        validate_negative_input()
        validate_correct_input()
        print(">>> Sisendi valideerimine: KORRAS (OK)")

        # 2. Summa arvutamine
        sum_mixed_inputs()
        sum_expenses_only()
        sum_empty_list()
        print(">>> Summa arvutamine: KORRAS (OK)")

        # 3. Summa kategooria põhiselt
        sum_category_food_expense()
        sum_category_work_income()
        sum_category_unknown()
        print(">>> Summa arvutamine kategooria põhiselt: KORRAS (OK)")

        # 4. Sissetulekud ja kulud
        income_valid_number()
        expenses_valid_number()
        income_invalid_input()
        print(">>> Sissetulekud ja kulud: KORRAS (OK)")

        # 5. Stringi teisendamine dictionaryks
        convert_info_to_dict_valid()
        convert_info_to_dict_with_string_amount()
        convert_info_to_dict_label_as_string()
        print(">>> Stringi teisendamine dictionaryks: KORRAS (OK)")

        # 6. Filter kategooria järgi
        filter_single_category()
        filter_multiple_same_category()
        filter_nonexistent_category()
        print(">>> Filter kategooria järgi: KORRAS (OK)")

        # 7. Komplekssed arvutused
        mixed_income_expense_recursive()
        all_income_recursive()
        calculate_zero_amounts()
        print(">>> Komplekssed arvutused: KORRAS (OK)")

        print("\n=== KÕIK TESTID LÄBISID EDUKALT ===")

    except AssertionError as e:
        print(f"\n!!! VIGA TESTIS !!!")
        import traceback
        traceback.print_exc()