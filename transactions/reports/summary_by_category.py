from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum, QuerySet

from transactions.models import Transaction


class SummaryByCategory(object):

    @classmethod
    def execute(cls, user_id) -> dict:
        transactions = cls.get_transactions(user_id)
        return cls.build_response(transactions)

    @staticmethod
    def build_response(transactions: list) -> defaultdict:
        response = defaultdict(lambda: defaultdict(Decimal))
        for t in transactions:
            response[t["type"]][t["category"]] += round(t["balance"], 2)
        return response

    @staticmethod
    def get_transactions(user_id: int) -> QuerySet:
        transactions = Transaction.objects.filter(user=user_id).values(
            'category', 'type'
        ).annotate(
            balance=Sum('amount'),
        ).order_by('category', 'type')
        return transactions
