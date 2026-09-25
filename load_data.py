from core.ingestion import load_transactions_from_excel


df = load_transactions_from_excel(
    "data/transactions.xlsx"
)

print("Transactions loaded:", len(df))
print("Database ingestion successful.")