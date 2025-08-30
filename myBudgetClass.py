from modules.input_helpers import get_valid_number
from modules.customer_data import read_customer_data_manual, read_customer_data_file
from modules.transaction_handler import process_expense
from modules.summary import print_summary, write_to_file


class MyBudget:
    def __init__(self, name=None, balance=0.0, loan=0.0):
        """Initialize a MyBudget instance."""
        self.name = name
        self.balance = balance
        self.loan = loan
        self.transactions = []
        self.transaction_number = 1
        self.transaction_base_id = None

    def load_customer_data(self, manual=True, path=None):
        """Load customer data manually or from file."""
        if manual:
            self.name, self.balance, self.loan = read_customer_data_manual()
        else:
            self.name, self.balance, self.loan = read_customer_data_file(path)

        # Create transaction base ID
        parts = self.name.split()
        if len(parts) == 1:
            self.transaction_base_id = parts[0]
        else:
            self.transaction_base_id = f"{parts[0]}.{parts[-1]}"

    def add_expense(self, expense):
        """Process a single expense transaction."""
        result = process_expense(
            expense,
            self.balance,
            self.loan,
            self.transactions,
            self.transaction_base_id,
            self.transaction_number,
        )
        if result is None:
            return False  # expense rejected or exit condition
        _, self.balance, self.loan = result
        self.transaction_number += 1
        return True

    def run_expenses_loop(self):
        """Interactive loop for adding expenses."""
        while True:
            expense = get_valid_number("Enter an expense amount: ")
            if not self.add_expense(expense):
                break
            more = input("Do you have another expense? (yes/no): ").strip().lower()
            if more != "yes":
                break

    def summarize(self):
        """Print and save summary of transactions."""
        print_summary(self.name, self.balance, self.loan, self.transactions)
        write_to_file(self.name, self.balance, self.loan, self.transactions)


def main():
    budget = MyBudget()

    # Ask user whether to enter manually or from file
    while True:
        manual = input("Do you want to input name, balance and loan manually? (yes/no): ").strip().lower()
        if manual in ("yes", "no"):
            break
        print("Please answer 'yes' or 'no'.")

    if manual == "yes":
        budget.load_customer_data(manual=True)
    else:
        path = input("Enter the file path for 'CustomerData': ").strip()
        budget.load_customer_data(manual=False, path=path)

    budget.run_expenses_loop()
    budget.summarize()


if __name__ == "__main__":
    main()
