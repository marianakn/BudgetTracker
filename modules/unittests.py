import unittest
from modules.transaction_handler import process_expense


class TestProcessExpenseBoundary(unittest.TestCase):

    def test_expense_equal_to_balance_plus_loan(self):
        #Boundary test: expense exactly equals balance + loan
        transactions = []
        txn_id, balance, loan = process_expense(
            expense=300,
            balance=100,
            loan=200,
            transactions=transactions,
            transaction_base_id="T",
            transaction_number=10
        )

        # Since expense == balance + loan, it should succeed
        self.assertEqual(txn_id, "T-10")
        self.assertEqual(balance, 0.0)   # all balance used
        self.assertEqual(loan, 0.0)      # all loan used
        self.assertEqual(transactions[-1]["amount"], 300)

if __name__ == "__main__":
    unittest.main()