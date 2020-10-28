from collections import namedtuple

from transactions.constants import TransactionType

ValidationResponse = namedtuple("ValidationError", "is_valid error")


def validate_transaction(transaction: dict) -> ValidationResponse:
    _type = transaction["type"]

    if _type == TransactionType.INFLOW and transaction["amount"] <= 0:
        return ValidationResponse(
            False,
            "Inflow transactions must have positive amounts"
        )

    if _type == TransactionType.OUTFLOW and transaction["amount"] >= 0:
        return ValidationResponse(
            False,
            "Outflow transactions must have negative amounts"
        )

    return ValidationResponse(True, None)
