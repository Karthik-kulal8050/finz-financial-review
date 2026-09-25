from fastapi import FastAPI
from backend.database import SessionLocal
from backend.models import Transaction
from backend.schemas import TransactionCorrection
import pandas as pd
from core.pnl import calculate_pnl
from core.variance import (
    get_variance_summary,
    calculate_profit_impact,
    get_category_transactions
)
from pathlib import Path

from backend.database import Base, engine
from core.ingestion import load_transactions_from_excel



app = FastAPI(
    title="Finz Financial Review API"
)

DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "transactions.xlsx"
)


@app.on_event("startup")
def initialize_database():

    Base.metadata.create_all(bind=engine)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Transaction dataset not found: {DATA_FILE}"
        )

    load_transactions_from_excel(DATA_FILE)





@app.get("/")
def home():
    return {
        "message": "Finz Financial Review API is running"
    }


@app.get("/transactions")
def get_transactions():

    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        return [
            {
                "transaction_id": t.transaction_id,
                "date": t.date,
                "description": t.description,
                "counterparty": t.counterparty,
                "amount": t.amount,
                "category": t.category,
                "subcategory": t.subcategory,
                "requires_review": t.requires_review,
                "confidence": t.confidence,
                "classification_source": t.classification_source
            }
            for t in transactions
        ]

    finally:
        db.close()


@app.get("/review-queue")
def get_review_queue():

    db = SessionLocal()

    try:

        transactions = (
            db.query(Transaction)
            .filter(Transaction.requires_review == True)
            .all()
        )

        return [
            {
                "transaction_id": t.transaction_id,
                "date": t.date,
                "description": t.description,
                "amount": t.amount,
                "category": t.category,
                "subcategory": t.subcategory,
                "confidence": t.confidence,
                "classification_source": t.classification_source
            }
            for t in transactions
        ]

    finally:
        db.close()


@app.patch("/transactions/correct")
def correct_transaction(
    correction: TransactionCorrection
):

    db = SessionLocal()

    try:

        transaction = (
            db.query(Transaction)
            .filter(
                Transaction.transaction_id
                == correction.transaction_id
            )
            .first()
        )

        if transaction is None:

            return {
                "error": "Transaction not found"
            }

        transaction.category = correction.category

        transaction.subcategory = correction.subcategory

        transaction.classification_source = "human"

        transaction.confidence = 1.0

        transaction.requires_review = False

        db.commit()

        return {
            "message": "Transaction corrected successfully",
            "transaction_id": transaction.transaction_id
        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


@app.get("/pnl")
def get_pnl():

    db = SessionLocal()

    try:

        transactions = db.query(Transaction).all()

        data = [
            {
                "Transaction ID": t.transaction_id,
                "Date": t.date,
                "Amount": t.amount,
                "category": t.category,
                "subcategory": t.subcategory,
            }
            for t in transactions
        ]

        df = pd.DataFrame(data)

        pnl = calculate_pnl(df)

        return pnl.to_dict(orient="records")

    finally:

        db.close()



@app.get("/variance")
def get_variance(
    previous_month: str,
    current_month: str
):

    db = SessionLocal()

    try:

        transactions = db.query(Transaction).all()

        data = [
            {
                "Transaction ID": t.transaction_id,
                "Date": t.date,
                "Amount": t.amount,
                "category": t.category,
                "subcategory": t.subcategory,
            }
            for t in transactions
        ]

        df = pd.DataFrame(data)

        pnl = calculate_pnl(df)

        variance = get_variance_summary(
            pnl,
            previous_month,
            current_month
        )

        profit_impact = calculate_profit_impact(
            pnl,
            previous_month,
            current_month
        )

        return {
            "variance": variance.to_dict(
                orient="records"
            ),
            "profit_impact": profit_impact.to_dict(
                orient="records"
            )
        }

    finally:

        db.close()


@app.get("/category-transactions")
def category_transactions(
    month: str,
    category: str
):

    db = SessionLocal()

    try:

        transactions = db.query(Transaction).all()

        data = [
            {
                "Transaction ID": t.transaction_id,
                "Date": t.date,
                "Description": t.description,
                "Counterparty": t.counterparty,
                "Amount": t.amount,
                "category": t.category,
                "subcategory": t.subcategory
            }
            for t in transactions
        ]

        df = pd.DataFrame(data)

        result = get_category_transactions(
            df,
            month,
            category
        )

        return result.to_dict(
            orient="records"
        )

    finally:

        db.close()