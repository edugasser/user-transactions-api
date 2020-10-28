from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as ApiUser
from users.models import User
from transactions.tests.fake_transactions import transactions_data
from transactions.use_cases import CreateTransactions


class Command(BaseCommand):
    help = "Setup demo stuffs"

    def handle(self, *args, **options):
        user_admin = ApiUser.objects.filter(username="demo").first()
        if not user_admin:
            user_admin = ApiUser.objects.create_superuser(
                'demo', 'demo@example.com', '123')
            user = User.objects.create(
                name="user1",
                email="user@gmail.com",
                age=10
            )
            CreateTransactions(user.id).execute(transactions_data)
