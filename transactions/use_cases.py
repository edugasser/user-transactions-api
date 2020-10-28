from api.serializers.transactions import TransactionSerializer
from transactions.exceptions import TransactionError
from transactions.models import Transaction


class CreateTransactions(object):

    def __init__(self, user_id):
        self.user_id = user_id

    def prepare_transaction(self, transactions: list):
        for transaction_data in transactions:
            transaction_data["user_id"] = self.user_id
            yield Transaction(**transaction_data)

    def execute(self, data: list):
        transaction_request = TransactionSerializer(data=data, many=True)

        if transaction_request.is_valid():
            to_create = list(self.prepare_transaction(transaction_request.data))  # noqa
            Transaction.objects.bulk_create(
                to_create,
                ignore_conflicts=True
            )
        else:
            raise TransactionError(transaction_request.errors)
