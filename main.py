import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_discription
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS=columns=["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE,index=False)


    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry ={
            "date": date,
            "amount":amount,
            "category":category,
            "description":description
        }
        with open(cls.CSV_FILE,"a",newline="")as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry add successfully")


    @classmethod # GIVE ALL THE TRANSACTIONS WITHIN A DATE RANGE
    def get_transactions(cls, start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        #CONVERT ALL OF THE DATES INSIDE  OF THE DATE COLUMN TO A DATETIME OBJECT
        # USE THEM TO FILTER BY DIFFERENT TRANSACTIONS
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)
        
        mask = (df["date"]>= start_date) & (df["date"] <= end_date)  #MASK-"SOMETHING THAT WE CAN APPLY TO THE DIFFERENT ROWS INSIDE OF A DATAFRAME TO SEE IF WE SHOULD SELECT OR NOT"
        filter_df= df.loc[mask] # RETURNS A NEW FILTERED DATAFRAME

        if filter_df.empty:
            print("N0 Transation found in the given date range")
            return None
        else:
            print(f"Transation from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filter_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
        
            total_income = filter_df[filter_df["category"] == "Income"] ["amount"].sum()
            total_expense = filter_df[filter_df["category"] == "Expense"] ["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Saving: ₹{(total_income - total_expense):.2f}")
            return filter_df



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",allow_default=True)
    amount = get_amount()
    category =get_category()
    description = get_discription()
    CSV.add_entry(date, amount, category, description )

#plot sction

def plot_transaction(df):  #DATAFRAME IS GOING TO CONTAIN ALL OF THE TRANSACTION THAT WE WANT TO PLOT
    df.set_index("date", inplace = True)   # THE INDEX  IS WAY IN WHICH WE LOCATE AND MANIPULATE DIFFERENT ROWS
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    # all of the rows of the income/ D = "daily frequency"
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
# CREATE A  PLOT USING  MATAPLOTLIB
    plt.figure(figsize=(10, 5))           #SETTING UP THE SCREEN/CANVAS
    plt.plot(income_df.index, income_df["amount"], label= "Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label= "Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transation")
        print("\n2. View transation and summary within a date range")
        print("\n3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice =="1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if df is not None and input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1,2 or 3.")


if __name__ == "__main__":
    main()

# CSV.get_transactions("01-01-2023","30-07-2024")
# add()
# CSV.initialize_csv()
# CSV.add_entry("20-07-2024",124.65,"Income","salary")


