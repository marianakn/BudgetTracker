from modules.input_helpers import get_valid_number
from modules.customer_data import read_customer_data_manual, read_customer_data_file
from modules.transaction_handler import process_expense
from modules.summary import print_summary, write_to_file


class PersonBudget:
    def __init__(self, name: str, balance: float, loan: float):
        """Initialize the budget for one person with encapsulated attributes."""
        self.__name = name
        self.__balance = balance
        self.__loan = loan
        self.__transactions = []
        self.__transaction_number = 1

        # Create transaction base ID safely
        parts = self.__name.split()
        if len(parts) == 1:
            self.__transaction_base_id = parts[0]
        else:
            self.__transaction_base_id = f"{parts[0]}.{parts[-1]}"

    # Encapsulated getters
    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

    @property
    def loan(self):
        return self.__loan

    @property
    def transactions(self):
        return self.__transactions

    def available_funds(self):
        """Calculate total available funds (balance + loan)."""
        return self.__balance + self.__loan

    def add_expense(self, amount: float):
        """Add an expense using process_expense and update state."""
        result = process_expense(
            amount,
            self.__balance,
            self.__loan,
            self.__transactions,
            self.__transaction_base_id,
            self.__transaction_number
        )
        if result is None:
            return False  # stop adding expenses

        _, self.__balance, self.__loan = result
        self.__transaction_number += 1
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
        print_summary(self.__name, self.__balance, self.__loan, self.__transactions)
        write_to_file(self.__name, self.__balance, self.__loan, self.__transactions)


class OnlineBudget(PersonBudget):
    def __init__(self, name: str, balance: float, loan: float, online_loan: float):
        """Initialize OnlineBudget with an additional online loan."""
        super().__init__(name, balance, loan)
        self.__online_loan = online_loan

    @property
    def online_loan(self):
        return self.__online_loan

    def available_funds(self):
        """Override: total funds include online loan."""
        return self.balance + self.loan + self.__online_loan

    def add_expense(self, amount: float):
        """Override expense: spend in order balance -> loan -> online_loan."""
        if amount <= self.balance:
            # Only balance needed
            new_balance = self.balance - amount
            new_loan = self.loan
            new_online_loan = self.__online_loan
        elif amount <= self.balance + self.loan:
            # Use balance + loan
            remaining = amount - self.balance
            new_balance = 0
            new_loan = self.loan - remaining
            new_online_loan = self.__online_loan
        elif amount <= self.balance + self.loan + self.__online_loan:
            # Use balance + loan + online loan
            remaining = amount - (self.balance + self.loan)
            new_balance = 0
            new_loan = 0
            new_online_loan = self.__online_loan - remaining
        else:
            print("Expense exceeds all available funds.")
            return False

        # Update private attributes
        self._PersonBudget__balance = new_balance
        self._PersonBudget__loan = new_loan
        self.__online_loan = new_online_loan

        # Record transaction
        self._PersonBudget__transactions.append(
            f"Transaction {self._PersonBudget__transaction_number}: Expense {amount}"
        )
        self._PersonBudget__transaction_number += 1
        return True


def main():
    manual = input("Do you want to input name, balance, and loan manually? (yes/no): ").strip().lower()
    if manual == "yes":
        name, balance, loan = read_customer_data_manual()
    else:
        path = input("Enter the file path for 'CustomerData': ").strip()
        name, balance, loan = read_customer_data_file(path)

    online = input("Do you want to add an online loan? (yes/no): ").strip().lower()
    if online == "yes":
        online_loan = get_valid_number("Enter online loan amount: ")
        budget = OnlineBudget(name, balance, loan, online_loan)
    else:
        budget = PersonBudget(name, balance, loan)

    budget.run_expenses_loop()
    budget.summarize()


if __name__ == "__main__":
    main()
#test push
