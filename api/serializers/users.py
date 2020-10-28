from rest_framework import serializers

from api.serializers.transactions import TransactionSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "age", "transactions")
