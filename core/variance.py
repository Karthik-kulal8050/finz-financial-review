import pandas as pd


def calculate_monthly_variance(
    pnl: pd.DataFrame,
    previous_month: str,
    current_month: str
) -> dict:

    previous = pnl[pnl["Month"] == previous_month].iloc[0]
    current = pnl[pnl["Month"] == current_month].iloc[0]

    metrics = [
        "Gross Revenue",
        "Refunds",
        "Net Revenue",
        "COGS",
        "Gross Profit",
        "Payroll",
        "Operating Expenses",
        "Operating Profit",
    ]

    variance = {}

    for metric in metrics:

        previous_value = float(previous[metric])
        current_value = float(current[metric])

        change = current_value - previous_value

        if previous_value != 0:
            percentage_change = (
                change / abs(previous_value)
            ) * 100
        else:
            percentage_change = 0

        variance[metric] = {
            "previous": previous_value,
            "current": current_value,
            "change": change,
            "percentage_change": percentage_change,
        }

    return variance


def get_variance_summary(
    pnl: pd.DataFrame,
    previous_month: str,
    current_month: str
) -> pd.DataFrame:

    variance = calculate_monthly_variance(
        pnl,
        previous_month,
        current_month
    )

    rows = []

    for metric, values in variance.items():

        rows.append({
            "Metric": metric,
            "Previous": values["previous"],
            "Current": values["current"],
            "Change": values["change"],
            "Change %": values["percentage_change"],
        })

    return pd.DataFrame(rows)


def get_category_variance(
    df: pd.DataFrame,
    previous_month: str,
    current_month: str
) -> pd.DataFrame:

    data = df.copy()

    data["Date"] = pd.to_datetime(data["Date"])

    data["Month"] = (
        data["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    previous = (
        data[data["Month"] == previous_month]
        .groupby("category")["Amount"]
        .sum()
        .abs()
    )

    current = (
        data[data["Month"] == current_month]
        .groupby("category")["Amount"]
        .sum()
        .abs()
    )

    categories = sorted(
        set(previous.index) |
        set(current.index)
    )
    
    rows = []

    for category in categories:

        previous_value = float(
            previous.get(category, 0)
        )

        current_value = float(
            current.get(category, 0)
        )

        change = current_value - previous_value

        if previous_value != 0:
            percentage_change = (
                change / previous_value
            ) * 100
        else:
            percentage_change = 0

        rows.append({
            "Category": category,
            "Previous": previous_value,
            "Current": current_value,
            "Change": change,
            "Change %": percentage_change,
        })

    return pd.DataFrame(rows)


def calculate_profit_impact(
    pnl: pd.DataFrame,
    previous_month: str,
    current_month: str
) -> pd.DataFrame:

    previous = pnl[
        pnl["Month"] == previous_month
    ].iloc[0]

    current = pnl[
        pnl["Month"] == current_month
    ].iloc[0]

    impacts = []

    # Revenue
    revenue_change = (
        current["Gross Revenue"]
        - previous["Gross Revenue"]
    )

    impacts.append({
        "Driver": "Gross Revenue",
        "Change": revenue_change,
        "Profit Impact": revenue_change
    })

    # Refunds
    refund_change = (
        current["Refunds"]
        - previous["Refunds"]
    )

    # Higher refunds hurt profit,
    # lower refunds help profit.
    impacts.append({
        "Driver": "Refunds",
        "Change": refund_change,
        "Profit Impact": -refund_change
    })

    # COGS
    cogs_change = (
        current["COGS"]
        - previous["COGS"]
    )

    impacts.append({
        "Driver": "COGS",
        "Change": cogs_change,
        "Profit Impact": -cogs_change
    })

    # Payroll
    payroll_change = (
        current["Payroll"]
        - previous["Payroll"]
    )

    impacts.append({
        "Driver": "Payroll",
        "Change": payroll_change,
        "Profit Impact": -payroll_change
    })

    # Operating Expenses
    opex_change = (
        current["Operating Expenses"]
        - previous["Operating Expenses"]
    )

    impacts.append({
        "Driver": "Operating Expenses",
        "Change": opex_change,
        "Profit Impact": -opex_change
    })

    return pd.DataFrame(impacts)

def get_category_transactions(
    df: pd.DataFrame,
    month: str,
    category: str
) -> pd.DataFrame:

    data = df.copy()

    data["Date"] = pd.to_datetime(data["Date"])

    data["Month"] = (
        data["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    result = data[
        (data["Month"] == month) &
        (data["category"] == category)
    ].copy()

    # Sort largest transactions first
    result = result.sort_values(
        by="Amount",
        key=lambda x: x.abs(),
        ascending=False
    )

    return result[
        [
            "Transaction ID",
            "Date",
            "Description",
            "Counterparty",
            "Amount",
            "category",
            "subcategory",
        ]
    ]