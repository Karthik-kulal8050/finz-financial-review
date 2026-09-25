from backend.database import SessionLocal
from backend.models import Transaction


db = SessionLocal()

try:

    count = db.query(Transaction).count()

    print("Transactions in database:", count)

    transactions = (
        db.query(Transaction)
        .limit(5)
        .all()
    )

    for transaction in transactions:

        print(
            transaction.transaction_id,
            transaction.description,
            transaction.category,
            transaction.amount
        )

finally:

    db.close()