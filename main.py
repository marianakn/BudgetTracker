print("=== Customer Budget Tracker ===")

full_name = input("Enter your full name: ")

balance_input = input("Enter your current balance: ")
while not balance_input.isdigit():
    print("Please enter digits only.")
    balance_input = input("Enter your current balance: ")
balance = float(balance_input)

loan_input = input("Enter your active loan balance: ")
while not loan_input.isdigit():
    print("Please enter digits only.")
    loan_input = input("Enter your active loan balance: ")
loan_balance = float(loan_input)

total_expense = 0

while True:
    expense_input = input("Enter an expense amount: ")
    while not expense_input.isdigit():
        print("Please enter digits only.")
        expense_input = input("Enter an expense amount: ")
    expense = float(expense_input)

    total_expense += expense
    balance_after_expense = balance - total_expense

    if balance_after_expense >= 0:
        print(f"Remaining balance: ${balance_after_expense:.2f}")
    else:
        amount_from_loan = -balance_after_expense

        if amount_from_loan <= loan_balance:
            print(f"You're now using your loan: ${amount_from_loan:.2f}")
        else:
            print("\nYou do not have enough balance or loan left to cover this expense.")
            total_expense -= expense
            break


    more = input("Do you have another expense? (yes/no): ").strip().lower()
    if more != "yes":
        break


balance_after_expense = balance - total_expense

print("\n=== Summary ===")
print("Name:", full_name)
print(f"Original Balance: ${balance:.2f}")
print(f"Total Expenses: ${total_expense:.2f}")

if balance_after_expense >= 0:
    print(f"Remaining Balance: ${balance_after_expense:.2f}")
    print(f"Loan Balance: ${loan_balance:.2f}")
    print("You did not use your loan.")
else:
    amount_from_loan = -balance_after_expense
    loan_balance = loan_balance - amount_from_loan
    print("Remaining Balance: $0.00 (all used)")
    print(f"Loan Used: ${amount_from_loan:.2f}")
    print(f"Loan Balance Left: ${loan_balance:.2f}")
    print("You spent from your loan.")
