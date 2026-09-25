from pathlib import Path

import pandas as pd

from core.categorization import categorize_dataframe
from core.pnl import calculate_pnl
from core.variance import calculate_profit_impact


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "transactions.xlsx"
)


def test_january_to_february_profit_impact():

    df = pd.read_excel(DATA_FILE)
    df = categorize_dataframe(df)

    pnl = calculate_pnl(df)

    impact = calculate_profit_impact(
        pnl,
        "2026-01",
        "2026-02"
    )

    drivers = impact.set_index("Driver")

    assert round(
        drivers.loc["Gross Revenue", "Profit Impact"],
        2
    ) == -1252.12

    assert round(
        drivers.loc["Refunds", "Profit Impact"],
        2
    ) == 470.32

    assert round(
        drivers.loc["COGS", "Profit Impact"],
        2
    ) == -3037.12

    assert round(
        drivers.loc["Payroll", "Profit Impact"],
        2
    ) == -3113.92

    assert round(
        drivers.loc["Operating Expenses", "Profit Impact"],
        2
    ) == -1529.73