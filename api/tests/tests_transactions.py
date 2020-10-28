import datetime
import json

from django.contrib.auth.models import User as ApiUser
from rest_framework.test import APITestCase

from transactions.constants import TransactionType, TransactionCategory
from transactions.models import Transaction
from users.models import User


class TransactionsTestCase(APITestCase):
    create_transaction_url = "/api/users/{user_id}/transactions/"

    def setUp(self):
        api_user = ApiUser.objects.create_user('admin', '123')
        self.client.force_authenticate(api_user)

        user = User.objects.create(
            name="user1",
            email="user1@gmail.com",
            age=12
        )
        Transaction.objects.create(
            user=user,
            reference="123",
            type=TransactionType.OUTFLOW,
            category=TransactionCategory.GROCERIES,
            date=datetime.date.today(),
            account="00001",
            amount=100
        )

    def test_single_transaction_created_ok(self):
        data = [
            {
                "reference": "1234",
                "type": TransactionType.OUTFLOW,
                "category": TransactionCategory.GROCERIES,
                "date": "2020-01-01",
                "account": "00001",
                "amount": -200
            }
        ]
        response = self.client.post(
            self.create_transaction_url.format(user_id=1),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_multiple_transaction_created_ok(self):
        data = [
            {
                "reference": "1234",
                "type": TransactionType.OUTFLOW,
                "category": TransactionCategory.GROCERIES,
                "date": "2020-01-01",
                "account": "00001",
                "amount": -200
            },
            {
                "reference": "12345",
                "type": TransactionType.OUTFLOW,
                "category": TransactionCategory.GROCERIES,
                "date": "2020-01-01",
                "account": "00001",
                "amount": -200
            }
        ]
        response = self.client.post(
            self.create_transaction_url.format(user_id=1),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_duplicated_transaction(self):
        data = [
            {
                "reference": "1234",
                "type": TransactionType.OUTFLOW,
                "category": TransactionCategory.GROCERIES,
                "date": "2020-01-01",
                "account": "00001",
                "amount": -200
            },
            {
                "reference": "1234",
                "type": TransactionType.OUTFLOW,
                "category": TransactionCategory.GROCERIES,
                "date": "2020-01-01",
                "account": "00001",
                "amount": -200
            }
        ]
        response = self.client.post(
            self.create_transaction_url.format(user_id=1),
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
