class TransactionType(object):
    INFLOW = "inflow"
    OUTFLOW = "outflow"

    ALL = (
        (INFLOW, "inflow"),
        (OUTFLOW, "outflow")
    )


class TransactionCategory(object):
    GROCERIES = "groceries"
    TRANSFER = "transfer"
    SALARY = "salary"
    RENT = "rent"
    OTHER = "other"
    SAVINGS = "savings"

    ALL = (
        (GROCERIES, "groceries"),
        (TRANSFER, "transfer"),
        (SALARY, "salary"),
        (RENT, "rent"),
        (OTHER, "other"),
        (SAVINGS, "savings")
    )
