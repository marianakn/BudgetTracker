def process_expense(expense, balance, loan, transactions, transaction_base_id, transaction_number):
    transaction_id = f"{transaction_base_id}-{transaction_number}"
    if expense <= balance:
        balance -= expense
        print(f"Remaining balance: ${balance:.2f}")
    elif expense <= balance + loan:
        needed_from_loan = expense - balance
        loan -= needed_from_loan
        balance = 0.0
        print(f"You are using your loan: ${needed_from_loan:.2f}")
    else:
        print("Not enough balance or loan to cover this expense.")
        return None, balance, loan

    transactions.append({
        "id": transaction_id,
        "amount": expense,
        "balance": balance,
        "loan": loan
    })
    return transaction_id, balance, loan
