from json import loads, dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase

from users.models import User
from .fake_transactions import transactions_data
from ..reports.summary_by_category import SummaryByCategory
from ..use_cases import CreateTransactions


class SummaryByCategoryTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            name="user1",
            email="user1@gmail.com",
            age=12
        )
        CreateTransactions(1).execute(transactions_data)

    def test_summary_ok(self):
        user_id = 1
        response = SummaryByCategory.execute(user_id)
        expected = {
            "inflow": {
                "salary": "2500.72",
                "savings": "150.72"
            },
            "outflow": {
                "groceries": "-51.13",
                "rent": "-560.00",
                "transfer": "-150.72"
            }
        }
        # NOTE: DRF returns OrderedDict and we need to compare it with dict.
        # There isn't an elegant way to convert it to dict.
        response = loads(dumps(response, cls=DjangoJSONEncoder))
        self.assertDictEqual(response, expected)

    def test_summary_no_transactions(self):
        user_id = 2
        response = SummaryByCategory.execute(user_id)
        expected = {}
        self.assertDictEqual(response, expected)
