import datetime

from django.test import SimpleTestCase

from transactions.constants import TransactionType, TransactionCategory
from transactions.validations import validate_transaction


class UserTestCase(SimpleTestCase):
    transactions = None

    def setUp(self):
        self.transaction = {
            "reference": "1234",
            "type": TransactionType.OUTFLOW,
            "category": TransactionCategory.GROCERIES,
            "date": datetime.date.today(),
            "account": "00001",
            "amount": -200
        }

    def test_transaction_valid_outflow_type(self):
        self.transaction["type"] = TransactionType.OUTFLOW
        self.transaction["amount"] = -200

        is_valid, error = validate_transaction(self.transaction)
        self.assertEqual(is_valid, True)
        self.assertEqual(error, None)

    def test_transaction_valid_inflow_type(self):
        self.transaction["type"] = TransactionType.INFLOW
        self.transaction["amount"] = 200

        is_valid, error = validate_transaction(self.transaction)
        self.assertEqual(is_valid, True)
        self.assertEqual(error, None)

    def test_transaction_wrong_outflow_type(self):
        self.transaction["type"] = TransactionType.OUTFLOW
        self.transaction["amount"] = 200

        is_valid, error = validate_transaction(self.transaction)

        self.assertEqual(is_valid, False)
        self.assertEqual(
            error,
            "Outflow transactions must have negative amounts"
        )

    def test_transaction_wrong_inflow_type(self):
        self.transaction["type"] = TransactionType.INFLOW
        self.transaction["amount"] = -200

        is_valid, error = validate_transaction(self.transaction)

        self.assertEqual(is_valid, False)
        self.assertEqual(
            error,
            "Inflow transactions must have positive amounts"
        )
