import pandas as pd

from backend.database import SessionLocal
from backend.models import Transaction
from core.pnl import calculate_pnl
from core.variance import (
    get_variance_summary,
    calculate_profit_impact
)


def get_transactions_dataframe():

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

        return pd.DataFrame(data)

    finally:

        db.close()


def get_monthly_pnl():

    df = get_transactions_dataframe()

    return calculate_pnl(df)


def get_monthly_variance(
    previous_month,
    current_month
):

    pnl = get_monthly_pnl()

    return get_variance_summary(
        pnl,
        previous_month,
        current_month
    )


def get_profit_impact(
    previous_month,
    current_month
):

    pnl = get_monthly_pnl()

    return calculate_profit_impact(
        pnl,
        previous_month,
        current_month
    )