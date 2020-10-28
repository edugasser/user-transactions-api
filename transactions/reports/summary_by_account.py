from django.db.models import Sum, Q, QuerySet
from rest_framework import serializers

from transactions.models import Transaction
from transactions.exceptions import InvalidReport


class SummaryByAccountResponse(serializers.Serializer):
    account = serializers.CharField(max_length=200)
    balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_inflow = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=8, decimal_places=2)


class SummaryByAccountRequest(serializers.Serializer):
    from_date = serializers.DateField(required=False, allow_null=True)
    to_date = serializers.DateField(required=False, allow_null=True)
    user = serializers.IntegerField()

    def validate(self, data):
        data = super(SummaryByAccountRequest, self).validate(data)
        if bool(data.get("from_date")) ^ bool(data.get("to_date")):
            raise serializers.ValidationError("A range date is required")
        return data


class SummaryByAccount(object):

    @classmethod
    def execute(cls, params: dict) -> list:
        request = SummaryByAccountRequest(data=params)
        if not request.is_valid():
            raise InvalidReport(request.errors)
        transactions = cls.get_transactions(request.data)
        cleaned = cls.clean_nulls(transactions)
        return SummaryByAccountResponse(cleaned, many=True).data

    @staticmethod
    def clean_nulls(transactions: list) -> list:
        for transaction in transactions:
            if transaction["total_inflow"] is None:
                transaction["total_inflow"] = 0
            if transaction["total_outflow"] is None:
                transaction["total_outflow"] = 0
        return transactions

    @staticmethod
    def get_transactions(params: dict) -> QuerySet:
        filters = {"user": params["user"]}
        if params["from_date"] and params["to_date"]:
            filters["date__gte"] = params["from_date"]
            filters["date__lte"] = params["to_date"]

        transactions = Transaction.objects.filter(**filters).values(
            "account"
        ).annotate(
            balance=Sum("amount"),
            total_inflow=Sum("amount", filter=Q(type="inflow")),
            total_outflow=Sum("amount", filter=Q(type="outflow")),
        ).order_by("account")
        return transactions
