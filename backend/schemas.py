from pydantic import BaseModel


class TransactionCorrection(BaseModel):
    transaction_id: str
    category: str
    subcategory: str