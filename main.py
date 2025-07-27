# === Customer Budget Tracker ===

# Function to make sure user enters numbers

def get_valid_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter numbers only (e.g. 100.50)")

# Function to clean and format a name properly
def format_name(raw):
    parts = raw.strip().split()
    formatted = [p.capitalize() for p in parts]
    return " ".join(formatted)

# Get input method
manual_input = input("Do you want to input name, balance and loan manually? (yes/no): ").strip().lower()

if manual_input == "yes":
    raw_name = input("Enter your full name: ")
    full_name = format_name(raw_name)
    balance = get_valid_number("Enter your current balance: ")
    loan = get_valid_number("Enter your active loan balance: ")
else:
    file_path = input("Enter the file path for 'CustomerData': ").strip()
    try:
        with open(file_path, "r") as f:
            line = f.readline().strip()
            parts = line.split(",")
            if len(parts) != 4:
                print("Invalid file format. Expected: Name, Surname, Balance, Loan")
                exit()
            raw_name = f"{parts[0]} {parts[1]}"
            full_name = format_name(raw_name)
            balance = float(parts[2])
            loan = float(parts[3])
    except FileNotFoundError:
        print("File not found.")
        exit()
    except ValueError:
        print("Invalid data format in the file.")
        exit()

# Prepare name parts and transaction base ID
name_parts = full_name.split()
first_name = name_parts[0]
last_name = name_parts[-1]
transaction_base_id = f"{first_name}.{last_name}"

# Store initial balances
initial_balance = balance
initial_loan = loan

# Track current state
current_balance = balance
current_loan = loan

transactions = []
expenses = []
balances = []
loans = []
transaction_number = 1

# Expense loop
while True:
    expense = get_valid_number("Enter an expense amount: ")
    transaction_id = f"{transaction_base_id}-{transaction_number}"

    if expense <= current_balance:
        # Use current balance
        current_balance -= expense
        balances.append(current_balance)
        loans.append(current_loan)
        expenses.append(expense)
        transactions.append({
            "id": transaction_id,
            "amount": expense,
            "balance": current_balance,
            "loan": current_loan
        })
        print(f"Remaining balance: ${current_balance:.2f}")

    elif expense <= current_balance + current_loan:
        # Use remaining balance + loan
        needed_from_loan = expense - current_balance
        current_loan -= needed_from_loan
        current_balance = 0.0
        balances.append(current_balance)
        loans.append(current_loan)
        expenses.append(expense)
        transactions.append({
            "id": transaction_id,
            "amount": expense,
            "balance": current_balance,
            "loan": current_loan
        })
        print(f"You are using your loan: ${needed_from_loan:.2f}")
    else:
        print("Not enough balance or loan to cover this expense.")
        break

    transaction_number += 1
    more = input("Do you have another expense? (yes/no): ").strip().lower()
    if more != "yes":
        break

# Final Summary
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

# Final loan usage summary
loan_used = initial_loan - current_loan
if loan_used > 0:
    print(f"You used ${loan_used:.2f} from your loan.")
else:
    print("You didn’t use your loan.")

# Write transactions to file
with open("Transaction.txt", "w") as file:
    file.write("Customer Name: " + full_name + "\n")
    file.write(f"Original Balance: ${initial_balance:.2f}\n")
    file.write(f"Original Loan: ${initial_loan:.2f}\n")
    file.write(f"Total Expenses: ${sum(expenses):.2f}\n")
    file.write(f"Number of Transactions: {len(transactions)}\n\n")
    file.write("Transactions:\n")
    for t in transactions:
        file.write(f"  - ID: {t['id']}, Amount: ${t['amount']:.2f}, "
                   f"Balance Left: ${t['balance']:.2f}, Loan Left: ${t['loan']:.2f}\n")

    if loan_used > 0:
        file.write(f"You used ${loan_used:.2f} from your loan.\n")
    else:
        file.write("You didn’t use your loan.\n")
