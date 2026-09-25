from pathlib import Path

import pandas as pd

from core.categorization import categorize_dataframe
from core.pnl import calculate_pnl


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "transactions.xlsx"
)


def load_data():
    df = pd.read_excel(DATA_FILE)
    return categorize_dataframe(df)


def test_monthly_pnl():
    df = load_data()

    pnl = calculate_pnl(df)

    january = pnl[pnl["Month"] == "2026-01"].iloc[0]
    february = pnl[pnl["Month"] == "2026-02"].iloc[0]
    march = pnl[pnl["Month"] == "2026-03"].iloc[0]

    assert round(january["Operating Profit"], 2) == 14470.53
    assert round(february["Operating Profit"], 2) == 6007.96
    assert round(march["Operating Profit"], 2) == 18852.14

    assert round(january["Gross Revenue"], 2) == 128821.61
    assert round(february["Gross Revenue"], 2) == 127569.49
    assert round(march["Gross Revenue"], 2) == 154122.87