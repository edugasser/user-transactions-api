from rest_framework import serializers

from transactions.models import Transaction
from transactions.validations import validate_transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "reference",
            "type",
            "category",
            "account",
            "date",
            "amount"
        )

    def validate(self, data):
        data = super(TransactionSerializer, self).validate(data)
        is_valid, error = validate_transaction(data)
        if not is_valid:
            raise serializers.ValidationError(error)
        return data
