from modules.input_helpers import get_valid_number
from modules.customer_data import read_customer_data_manual, read_customer_data_file
from modules.transaction_handler import process_expense
from modules.summary import print_summary, write_to_file


class PersonBudget:
    def __init__(self, name: str, balance: float, loan: float):
        """Initialize the budget for one person."""
        self.name = name
        self.balance = balance
        self.loan = loan
        self.transactions = []
        self.transaction_number = 1

        # Create transaction base ID safely
        parts = self.name.split()
        if len(parts) == 1:
            self.transaction_base_id = parts[0]
        else:
            self.transaction_base_id = f"{parts[0]}.{parts[-1]}"

    def add_expense(self, amount: float):
        """Add an expense using process_expense and update state."""
        result = process_expense(
            amount,
            self.balance,
            self.loan,
            self.transactions,
            self.transaction_base_id,
            self.transaction_number
        )
        if result is None:
            return False  # stop adding expenses

        _, self.balance, self.loan = result
        self.transaction_number += 1
        return True

    def run_expenses_loop(self):
        """Loop for entering multiple expenses interactively."""
        while True:
            expense = get_valid_number("Enter an expense amount: ")
            if not self.add_expense(expense):
                break
            more = input("Do you have another expense? (yes/no): ").strip().lower()
            if more != "yes":
                break

    def summarize(self):
        """Print and write the summary of all transactions."""
        print_summary(self.name, self.balance, self.loan, self.transactions)
        write_to_file(self.name, self.balance, self.loan, self.transactions)


def main():
    # Get user input for initial data
    manual = input("Do you want to input name, balance and loan manually? (yes/no): ").strip().lower()
    if manual == "yes":
        name, balance, loan = read_customer_data_manual()
    else:
        path = input("Enter the file path for 'CustomerData': ").strip()
        name, balance, loan = read_customer_data_file(path)

    # Create PersonBudget object
    budget = PersonBudget(name, balance, loan)

    # Run interactive expense loop
    budget.run_expenses_loop()

    # Print + save summary
    budget.summarize()


if __name__ == "__main__":
    main()

