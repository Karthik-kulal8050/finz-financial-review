from core.categorization import categorize_transaction


def test_food_sales_is_revenue():
    result = categorize_transaction(
        "POS batch deposit - food sales"
    )

    assert result["category"] == "REVENUE"
    assert result["subcategory"] == "Food Sales"
    assert result["include_in_pnl"] is True
    assert result["requires_review"] is False


def test_equipment_purchase_requires_review():
    result = categorize_transaction(
        "Equipment purchase - new oven"
    )

    assert result["category"] == "CAPEX"
    assert result["include_in_pnl"] is False
    assert result["requires_review"] is True


def test_unknown_transaction_requires_review():
    result = categorize_transaction(
        "Some completely unknown transaction"
    )

    assert result["category"] == "UNKNOWN"
    assert result["requires_review"] is True