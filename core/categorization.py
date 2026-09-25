import pandas as pd

RULES = [
    # ---------------- REVENUE ----------------
    {
        "pattern": "POS batch deposit - food sales",
        "category": "REVENUE",
        "subcategory": "Food Sales",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "POS batch deposit - beverage sales",
        "category": "REVENUE",
        "subcategory": "Beverage Sales",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Catering invoice payment",
        "category": "REVENUE",
        "subcategory": "Catering",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Delivery marketplace payout",
        "category": "REVENUE",
        "subcategory": "Delivery Sales",
        "include_in_pnl": True,
        "requires_review": False,
    },

    # ---------------- REFUNDS ----------------
    {
        "pattern": "Refunds and discounts",
        "category": "REFUNDS",
        "subcategory": "Refunds & Discounts",
        "include_in_pnl": True,
        "requires_review": False,
    },

    # ---------------- COGS ----------------
    {
        "pattern": "Food inventory purchase",
        "category": "COGS",
        "subcategory": "Food Inventory",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Beverage inventory purchase",
        "category": "COGS",
        "subcategory": "Beverage Inventory",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Large catering event food purchase",
        "category": "COGS",
        "subcategory": "Catering Food",
        "include_in_pnl": True,
        "requires_review": True,
    },

    # ---------------- PAYROLL ----------------
    {
        "pattern": "Payroll - hourly kitchen and FOH wages",
        "category": "PAYROLL",
        "subcategory": "Hourly Wages",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Manager salary payroll",
        "category": "PAYROLL",
        "subcategory": "Manager Salary",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Payroll taxes and benefits",
        "category": "PAYROLL",
        "subcategory": "Payroll Taxes & Benefits",
        "include_in_pnl": True,
        "requires_review": False,
    },

    # ---------------- OPERATING EXPENSES ----------------
    {
        "pattern": "Rent",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Rent",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "POS/software subscription",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Software",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Insurance premium",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Insurance",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Accounting/bookkeeping",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Accounting",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "To-go packaging and disposables",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Packaging",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Internet and phone",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Internet & Phone",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Utilities - electric/gas/water",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Utilities",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Cleaning and linen service",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Cleaning",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Marketing - local ads",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Marketing",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Repairs and maintenance",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Repairs & Maintenance",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Office/admin supplies",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Office Supplies",
        "include_in_pnl": True,
        "requires_review": False,
    },
    {
        "pattern": "Annual license renewal",
        "category": "OPERATING_EXPENSE",
        "subcategory": "License",
        "include_in_pnl": True,
        "requires_review": True,
    },
    {
        "pattern": "Delivery platform commission",
        "category": "OPERATING_EXPENSE",
        "subcategory": "Delivery Commission",
        "include_in_pnl": True,
        "requires_review": False,
    },

    # ---------------- CAPEX ----------------
    {
        "pattern": "Equipment purchase - new oven",
        "category": "CAPEX",
        "subcategory": "Equipment",
        "include_in_pnl": False,
        "requires_review": True,
    },

    # ---------------- TAX ----------------
    {
        "pattern": "Sales tax remittance",
        "category": "TAX",
        "subcategory": "Sales Tax",
        "include_in_pnl": False,
        "requires_review": True,
    },

    # ---------------- FINANCING ----------------
    {
        "pattern": "Loan principal repayment",
        "category": "FINANCING",
        "subcategory": "Loan Principal",
        "include_in_pnl": False,
        "requires_review": True,
    },

    # ---------------- EQUITY ----------------
    {
        "pattern": "Owner distribution",
        "category": "EQUITY",
        "subcategory": "Owner Distribution",
        "include_in_pnl": False,
        "requires_review": True,
    },

    # ---------------- LIABILITY ----------------
    {
        "pattern": "Gift card sales deposit",
        "category": "LIABILITY",
        "subcategory": "Gift Card Liability",
        "include_in_pnl": False,
        "requires_review": True,
    },
]


def categorize_transaction(description: str) -> dict:

    description = str(description).strip()

    for rule in RULES:
        if rule["pattern"].lower() in description.lower():

            return {
                "category": rule["category"],
                "subcategory": rule["subcategory"],
                "include_in_pnl": rule["include_in_pnl"],
                "requires_review": rule["requires_review"],
                "confidence": 1.0,
                "classification_source": "rule",
            }

    # Unknown transaction
    return {
        "category": "UNKNOWN",
        "subcategory": "Unclassified",
        "include_in_pnl": False,
        "requires_review": True,
        "confidence": 0.0,
        "classification_source": "unclassified",
    }


def categorize_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    results = df["Description"].apply(categorize_transaction)

    result_df = pd.DataFrame(results.tolist(), index=df.index)

    return pd.concat([df.copy(), result_df], axis=1)