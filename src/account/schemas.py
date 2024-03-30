
from pydantic import BaseModel


class Account(BaseModel):
    account_number: str
    balance: float
    user_id: int

class Transaction(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: float