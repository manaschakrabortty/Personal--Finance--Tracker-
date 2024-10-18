"""HERE I ACAN WRITE ALL OF THE FUNCTIONS RELATED TO GETTING 
INFORMATION FROM THE USER..
"""        

from datetime import datetime
date_format ="%d-%m-%Y"
CATAGORIES = {"I": "Income","E": "Expense"}




def get_date(promt,allow_default = False):
    date_str = input(promt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format.please enter the date in dd--mm-yy format")
        return get_date(promt,allow_default)
    

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount<=0:
            raise ValueError("Amount must be a non_neagtive non-zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter the category ('I' for Income 'E' for Expense): ").upper()
    if category in CATAGORIES:
        return CATAGORIES[category]
    
    print("Invalid category. please enter 'I' for Income or 'E' for Expences. ")
    return get_category

def get_discription():
    return input("Enter a description (optional): ")