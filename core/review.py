import pandas as pd


def get_review_queue(df):

    review_df = df[df["requires_review"] == True].copy()

    review_df = review_df.sort_values(
        by="Amount",
        key=lambda x: x.abs(),
        ascending=False
    )

    return review_df[
        [
            "Transaction ID",
            "Date",
            "Description",
            "Counterparty",
            "Amount",
            "category",
            "subcategory",
            "confidence",
            "classification_source"
        ]
    ]


def correct_transaction(
    df,
    transaction_id,
    new_category,
    new_subcategory
):

    df = df.copy()

    mask = df["Transaction ID"] == transaction_id

    df.loc[mask, "category"] = new_category
    df.loc[mask, "subcategory"] = new_subcategory

    df.loc[mask, "classification_source"] = "human"

    df.loc[mask, "confidence"] = 1.0

    df.loc[mask, "requires_review"] = False

    return df