import json

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers.users import UserSerializer
from transactions.exceptions import InvalidReport, TransactionError
from transactions.reports.summary_by_account import SummaryByAccount
from transactions.reports.summary_by_category import SummaryByCategory
from transactions.use_cases import CreateTransactions
from users.models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=True, name="Summary by account",
            url_path="summary-by-account")
    def summary_by_account(self, request, pk):
        params = {
            "user": pk,
            "from_date": request.GET.get("from_date"),
            "to_date": request.GET.get("to_date")
        }
        try:
            response = SummaryByAccount.execute(params)
        except InvalidReport as error:
            raise serializers.ValidationError(error)

        return Response(response)

    @action(methods=["get"], detail=True, name="Summary by category",
            url_path="summary-by-category")
    def summary_by_category(self, request, pk):
        response = SummaryByCategory.execute(pk)
        return Response(response)

    @action(methods=["post"], detail=True, name="Create transactions")
    def transactions(self, request, pk):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            raise serializers.ValidationError("Invalid request format")

        try:
            CreateTransactions(pk).execute(data)
        except TransactionError as error:
            raise serializers.ValidationError(error)

        return Response()


