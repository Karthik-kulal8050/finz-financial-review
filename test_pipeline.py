import pandas as pd

from core.categorization import categorize_dataframe
from core.pnl import calculate_pnl

from core.variance import (
    get_variance_summary,
    get_category_variance,
    calculate_profit_impact,
    get_category_transactions
)
from core.review import (
    get_review_queue,
    correct_transaction
)


df = pd.read_excel(
    "data/transactions.xlsx"
)


df = categorize_dataframe(df)


print("\nCATEGORY SUMMARY")
print("=" * 50)

print(
    df["category"]
    .value_counts()
)


print("\nREVIEW ITEMS")
print("=" * 50)

review = df[df["requires_review"]]

print(
    review[
        [
            "Transaction ID",
            "Date",
            "Description",
            "Amount",
            "category",
            "subcategory",
        ]
    ].to_string(index=False)
)



pnl = calculate_pnl(df)


print("\nMONTHLY P&L")
print("=" * 50)

print(
    pnl.to_string(
        index=False
    )
)

# -----------------------------------------
# Variance Analysis
# -----------------------------------------

print("\nJANUARY → FEBRUARY VARIANCE")
print("=" * 70)

variance = get_variance_summary(
    pnl,
    "2026-01",
    "2026-02"
)

print(
    variance.to_string(index=False)
)


print("\nCATEGORY VARIANCE")
print("=" * 70)

category_variance = get_category_variance(
    df,
    "2026-01",
    "2026-02"
)

print(
    category_variance.to_string(index=False)
)

print("\nPROFIT IMPACT")
print("=" * 70)

profit_impact = calculate_profit_impact(
    pnl,
    "2026-01",
    "2026-02"
)

print(
    profit_impact.to_string(index=False)
)

print("\nFEBRUARY COGS TRANSACTIONS")
print("=" * 70)

cogs_transactions = get_category_transactions(
    df,
    "2026-02",
    "COGS"
)

print(
    cogs_transactions.to_string(index=False)
)

print("\nREVIEW QUEUE")
print("=" * 70)

review_queue = get_review_queue(df)

print(review_queue.to_string(index=False))



print("\nBEFORE CORRECTION")
print("=" * 70)

print(
    df[df["Transaction ID"] == "T1179"][
        [
            "Transaction ID",
            "Description",
            "category",
            "subcategory",
            "requires_review",
            "classification_source"
        ]
    ].to_string(index=False)
)


df = correct_transaction(
    df,
    "T1179",
    "COGS",
    "Catering Food"
)


print("\nAFTER CORRECTION")
print("=" * 70)

print(
    df[df["Transaction ID"] == "T1179"][
        [
            "Transaction ID",
            "Description",
            "category",
            "subcategory",
            "requires_review",
            "classification_source"
        ]
    ].to_string(index=False)
)