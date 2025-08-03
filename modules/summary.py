def print_summary(name, initial_balance, initial_loan, transactions):
    print("\n=== Expense Summary ===")
    print("Customer Name:", name)
    print(f"Original Balance: ${initial_balance:.2f}")
    print(f"Original Loan: ${initial_loan:.2f}")
    print(f"Total Expenses: ${sum(t['amount'] for t in transactions):.2f}")
    print(f"Number of Transactions: {len(transactions)}\n")

    print("Transactions:")
    for t in transactions:
        print(f"  - ID: {t['id']}, Amount: ${t['amount']:.2f}, "
              f"Balance Left: ${t['balance']:.2f}, Loan Left: ${t['loan']:.2f}")

    loan_used = initial_loan - transactions[-1]['loan'] if transactions else 0
    print(f"You {'used' if loan_used else 'didn’t use'} ${loan_used:.2f} from your loan." if loan_used else "You didn’t use your loan.")

def write_to_file(name, initial_balance, initial_loan, transactions, file_path="Transaction.txt"):
    with open(file_path, "w") as f:
        f.write(f"Customer Name: {name}\n")
        f.write(f"Original Balance: ${initial_balance:.2f}\n")
        f.write(f"Original Loan: ${initial_loan:.2f}\n")
        f.write(f"Total Expenses: ${sum(t['amount'] for t in transactions):.2f}\n")
        f.write(f"Number of Transactions: {len(transactions)}\n\n")
        f.write("Transactions:\n")
        for t in transactions:
            f.write(f"  - ID: {t['id']}, Amount: ${t['amount']:.2f}, "
                    f"Balance Left is : ${t['balance']:.2f}, Loan Left: ${t['loan']:.2f}\n")
        loan_used = initial_loan - transactions[-1]['loan'] if transactions else 0
        f.write(f"You used ${loan_used:.2f} from your loan.\n" if loan_used else "You didn’t use your loan.\n")
