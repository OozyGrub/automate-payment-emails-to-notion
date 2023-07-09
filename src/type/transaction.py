import datetime

class Transaction:
    def __init__(self, title: str, created_at: datetime, amount: float):
        self.title = title
        self.created_at = created_at
        self.amount = float(amount)