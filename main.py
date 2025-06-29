print("=== Customer Budget Tracker ===")

full_name = input("Enter your full name: ")
balance = float(input("Enter your current balance: "))
expense = float(input("Enter your expense amount: "))
loan_balance = float(input("Enter your active loan balance: "))

balance_after_expense = balance - expense


if balance_after_expense >= 0:
    print("\n=== Summary ===")
    print("Name:", full_name)
    print("Original Balance: $", balance)
    print("Expense: $", expense)
    print("Remaining Balance: $", balance_after_expense)
    print("Loan Balance: $", loan_balance)
    print("You did not use your loan.")
else:
    amount_from_loan = -balance_after_expense

    if amount_from_loan <= loan_balance:
        loan_balance = loan_balance - amount_from_loan
        print("\n=== Summary ===")
        print("Name:", full_name)
        print("Original Balance: $", balance)
        print("Expense: $", expense)
        print("Remaining Balance: $0.0 (all used)")
        print("Loan used: $", amount_from_loan)
        print("Loan Balance Left: $", loan_balance)
        print(" You spent from your loan.")
    else:
        print("\n You do not have enough balance or loan to cover this expense.")

