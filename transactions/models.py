from django.db import models

from transactions.constants import TransactionType, TransactionCategory
from users.models import User


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    reference = models.CharField(
        max_length=10,
        unique=True
    )
    type = models.CharField(
        max_length=10,
        choices=TransactionType.ALL
    )
    category = models.CharField(
        max_length=20,
        choices=TransactionCategory.ALL
    )
    date = models.DateField()

    account = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.reference}: {self.type} {self.date}"
