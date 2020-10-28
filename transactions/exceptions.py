class InvalidReport(Exception):
    def __init__(self, error: str):
        self.error = error


class TransactionError(Exception):
    def __init__(self, error: str):
        self.error = error
