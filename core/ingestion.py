import pandas as pd

from core.categorization import categorize_dataframe
from backend.database import SessionLocal
from backend.models import Transaction


def load_transactions_from_excel(file_path):

    # 1. Read Excel file
    df = pd.read_excel(file_path)

    # 2. Categorize transactions
    df = categorize_dataframe(df)

    # 3. Open database session
    db = SessionLocal()

    try:

        # 4. Clear existing transactions
        db.query(Transaction).delete()

        # 5. Insert transactions
        for _, row in df.iterrows():

            transaction = Transaction(
                transaction_id=row["Transaction ID"],
                date=str(row["Date"]),
                description=row["Description"],
                counterparty=row["Counterparty"],
                amount=float(row["Amount"]),
                category=row["category"],
                subcategory=row["subcategory"],
                include_in_pnl=bool(row["include_in_pnl"]),
                requires_review=bool(row["requires_review"]),
                confidence=float(row["confidence"]),
                classification_source=row["classification_source"]
            )

            db.add(transaction)

        # 6. Save everything
        db.commit()

    except Exception:

        # Undo changes if something goes wrong
        db.rollback()

        raise

    finally:

        # Always close the database session
        db.close()

    return df