from sqlalchemy import Column, String, Float, Boolean
from backend.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        String,
        primary_key=True
    )

    date = Column(String)

    description = Column(String)

    counterparty = Column(String)

    amount = Column(Float)

    category = Column(String)

    subcategory = Column(String)

    include_in_pnl = Column(Boolean)

    requires_review = Column(Boolean)

    confidence = Column(Float)

    classification_source = Column(String)