from django.test import TestCase

from users.models import User
from .fake_transactions import transactions_data
from ..exceptions import InvalidReport
from ..reports.summary_by_account import SummaryByAccount
from ..use_cases import CreateTransactions


class SummaryByAccountTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            name="user1",
            email="user1@gmail.com",
            age=12
        )

        CreateTransactions(1).execute(transactions_data)

    def test_summary_without_dates(self):
        response = SummaryByAccount.execute({"user": 1})
        expected = [
            {
                "account": "C00099",
                "balance": "1738.87",
                "total_inflow": "2500.72",
                "total_outflow": "-761.85"
            },
            {
                "account": "S00012",
                "balance": "150.72",
                "total_inflow": "150.72",
                "total_outflow": "0.00"
            }
        ]
        self.assertEqual(response, expected)

    def test_summary_with_dates(self):
        params = {
            "user": 1,
            "from_date": "2020-01-01",
            "to_date": "2020-01-04"
        }
        response = SummaryByAccount.execute(params)
        expected = [
            {
                "account": "C00099",
                "balance": "-51.13",
                "total_inflow": "0.00",
                "total_outflow": "-51.13"
            }
        ]
        self.assertEqual(response, expected)

    def test_summary_with_wrong_dates(self):
        params = {
            "user": 1,
            "from_date": "2020-01-01"
        }
        with self.assertRaises(InvalidReport):
            SummaryByAccount.execute(params)
