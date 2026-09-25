import pandas as pd


def calculate_pnl(df: pd.DataFrame) -> pd.DataFrame:

    data = df.copy()


    data["Date"] = pd.to_datetime(data["Date"])


    data["Month"] = data["Date"].dt.to_period("M").astype(str)

    # -------------------------------------------------
    # Revenue
    # -------------------------------------------------

    revenue = (
        data[data["category"] == "REVENUE"]
        .groupby("Month")["Amount"]
        .sum()
    )

    # -------------------------------------------------
    # Refunds
    # -------------------------------------------------

    refunds = (
        data[data["category"] == "REFUNDS"]
        .groupby("Month")["Amount"]
        .sum()
    )

    refunds = refunds.abs()

    # -------------------------------------------------
    # COGS
    # -------------------------------------------------

    cogs = (
        data[data["category"] == "COGS"]
        .groupby("Month")["Amount"]
        .sum()
        .abs()
    )

    # -------------------------------------------------
    # Payroll
    # -------------------------------------------------

    payroll = (
        data[data["category"] == "PAYROLL"]
        .groupby("Month")["Amount"]
        .sum()
        .abs()
    )

    # -------------------------------------------------
    # Operating Expenses
    # -------------------------------------------------

    operating_expenses = (
        data[data["category"] == "OPERATING_EXPENSE"]
        .groupby("Month")["Amount"]
        .sum()
        .abs()
    )

    # -------------------------------------------------
    # Combine everything
    # -------------------------------------------------

    months = sorted(data["Month"].unique())

    pnl = pd.DataFrame(index=months)

    pnl.index.name = "Month"

    pnl["Gross Revenue"] = revenue.reindex(months, fill_value=0)

    pnl["Refunds"] = refunds.reindex(months, fill_value=0)

    pnl["Net Revenue"] = (
        pnl["Gross Revenue"] -
        pnl["Refunds"]
    )

    pnl["COGS"] = cogs.reindex(months, fill_value=0)

    pnl["Gross Profit"] = (
        pnl["Net Revenue"] -
        pnl["COGS"]
    )

    pnl["Payroll"] = payroll.reindex(months, fill_value=0)

    pnl["Operating Expenses"] = (
        operating_expenses.reindex(months, fill_value=0)
    )

    pnl["Operating Profit"] = (
        pnl["Gross Profit"]
        - pnl["Payroll"]
        - pnl["Operating Expenses"]
    )

    return pnl.reset_index()