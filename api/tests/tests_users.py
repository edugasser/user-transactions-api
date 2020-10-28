import datetime
import json

from django.contrib.auth.models import User as ApiUser
from rest_framework.test import APITestCase

from transactions.constants import TransactionType, TransactionCategory
from transactions.models import Transaction
from users.models import User


class UserTestCase(APITestCase):
    user_url = "/api/users/"
    summary_by_account_url = "/api/users/{user_id}/summary-by-account/"
    summary_by_category_url = "/api/users/{user_id}/summary-by-category/"

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

    def test_get_user_ok(self):
        response = self.client.get(
            "/api/users/1/",
            content_type='application/json'
        )
        expected = {
            "id": 1,
            "name": "user1",
            "email": "user1@gmail.com",
            "age": 12,
            "transactions":  [
                {
                    'account': '00001',
                    'amount': '100.00',
                    'category': 'groceries',
                    'date': '2020-10-08',
                    'reference': '123',
                    'type': 'outflow'
                }
            ]
        }
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(response.status_code, 200)

    def test_user_doest_not_exists(self):
        response = self.client.get("/api/users/23423/")
        self.assertEqual(response.status_code, 404)

    def test_user_created_ok(self):
        data = {"name": "new", "email": "new@gmail.com", "age": 23}
        response = self.client.post(
            self.user_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_user_wrong_creation(self):
        data = {"name": "new", "email": "new", "age": 23}
        response = self.client.put(
            self.user_url,
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 405)

    def test_summay_by_account_ok(self):
        response = self.client.get(
            self.summary_by_account_url.format(user_id=1),
            content_type='application/json'
        )
        expected = [
            {
                "account": "00001",
                "balance": "100.00",
                "total_inflow": "0.00",
                "total_outflow": "100.00"
            }
        ]
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(response.status_code, 200)

    def test_summay_by_category_ok(self):
        response = self.client.get(
            self.summary_by_category_url.format(user_id=1),
            content_type='application/json'
        )
        expected = {"outflow": {"groceries": 100.0}}
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(response.status_code, 200)
