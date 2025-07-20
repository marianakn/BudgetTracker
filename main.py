# === Customer Budget Tracker ===

# Function to make sure user enters numbers
def get_valid_number(prompt):
    while True:
        value = input(prompt)
        if value.replace('.', '', 1).isdigit():
            return float(value)
        print("Please enter numbers only (e.g. 100.50)")

# Function to clean and format a name properly
def format_name(raw):
    parts = raw.strip().split()
    formatted = [p.capitalize() for p in parts]
    return " ".join(formatted)

# Asks user for full name and format it
raw_name = input("Enter your full name: ")
full_name = format_name(raw_name)

# Get first and last name to create a transaction ID base
name_parts = full_name.split()
first_name = name_parts[0]
last_name = name_parts[-1]
transaction_base_id = f"{first_name}.{last_name}"

# Asks for balances
balance = get_valid_number("Enter your current balance: ")
loan = get_valid_number("Enter your active loan balance: ")

# Stores initial balances to use in summary later
initial_balance = balance
initial_loan = loan

# Lists to store data
transactions = []  # Each transaction is stored as a dictionary
expenses = []      # Just to track expense values if needed
balances = []      # Track balance after each expense
loans = []         # Track loan left after each expense

transaction_number = 1  # To generate transaction IDs

#Main expense loop
while True:
    # Asks user for expense amount
    expense = get_valid_number("Enter an expense amount: ")

    total_spent = sum(expenses) + expense
    balance_after = initial_balance - total_spent

    # Creates a transaction ID like: Maria.Smith-1
    transaction_id = f"{transaction_base_id}-{transaction_number}"

    if balance_after >= 0:
        # Still using own balance
        balances.append(balance_after)
        loans.append(loan)
        expenses.append(expense)
        transactions.append({
            "id": transaction_id,
            "amount": expense,
            "balance": balance_after,
            "loan": loan
        })
        print(f"Remaining balance: ${balance_after:.2f}")

    else:
        # Use loan if balance not enough
        needed_from_loan = -balance_after

        if needed_from_loan <= loan:
            loan -= needed_from_loan
            balances.append(0.00)
            loans.append(loan)
            expenses.append(expense)
            transactions.append({
                "id": transaction_id,
                "amount": expense,
                "balance": 0.00,
                "loan": loan
            })
            print(f"You are using your loan: ${needed_from_loan:.2f}")
        else:
            print("Not enough balance or loan to cover this expense.")
            break

    transaction_number += 1

    # Asks if they want to continue
    more = input("Do you have another expense? (yes/no): ").strip().lower()
    if more != "yes":
        break

# Print Final Summary
print("\n=== Expense Summary ===")
print("Customer Name:", full_name)
print(f"Original Balance: ${initial_balance:.2f}")
print(f"Original Loan: ${initial_loan:.2f}")
print(f"Total Expenses: ${sum(expenses):.2f}")
print(f"Number of Transactions: {len(transactions)}\n")

print("Transactions:")
for t in transactions:
    print(f"  - ID: {t['id']}, Amount: ${t['amount']:.2f}, "
          f"Balance Left: ${t['balance']:.2f}, Loan Left: ${t['loan']:.2f}")

# Final status
if balances and balances[-1] > 0:
    print("You didn’t use your loan.")
else:
    loan_used = initial_loan - loans[-1] if loans else 0
    print(f"You used ${loan_used:.2f} from your loan.")
