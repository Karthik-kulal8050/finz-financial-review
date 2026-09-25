import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai.tools import (
    get_monthly_pnl,
    get_monthly_variance,
    get_profit_impact
)
import requests


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


SYSTEM_PROMPT = """
You are the AI Financial Analyst for a restaurant financial review application.

Your job is to explain financial information using the financial tools provided.

IMPORTANT RULES:

1. Never invent financial numbers.
2. Never calculate financial totals yourself.
3. Financial numbers must come from the Python financial tools.
4. Clearly distinguish facts from interpretation.
5. When explaining a change in profit, identify the important drivers.
6. Format monetary values to two decimal places.
7. If the available data is insufficient, say so.
8. Keep answers concise and understandable.
"""


# ---------------------------------------------------------
# TOOL DECLARATIONS
# ---------------------------------------------------------

get_monthly_pnl_tool = types.FunctionDeclaration(
    name="get_monthly_pnl",
    description=(
        "Get the calculated monthly P&L from the transaction database. "
        "Use this when the user asks about revenue, refunds, COGS, "
        "gross profit, payroll, operating expenses, or operating profit."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={}
    )
)


get_monthly_variance_tool = types.FunctionDeclaration(
    name="get_monthly_variance",
    description=(
        "Compare financial metrics between two months."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "previous_month": types.Schema(
                type="STRING",
                description="Previous month in YYYY-MM format."
            ),
            "current_month": types.Schema(
                type="STRING",
                description="Current month in YYYY-MM format."
            )
        },
        required=["previous_month", "current_month"]
    )
)


get_profit_impact_tool = types.FunctionDeclaration(
    name="get_profit_impact",
    description=(
        "Calculate how each financial driver affected operating profit "
        "between two months."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "previous_month": types.Schema(
                type="STRING",
                description="Previous month in YYYY-MM format."
            ),
            "current_month": types.Schema(
                type="STRING",
                description="Current month in YYYY-MM format."
            )
        },
        required=["previous_month", "current_month"]
    )
)


tools = types.Tool(
    function_declarations=[
        get_monthly_pnl_tool,
        get_monthly_variance_tool,
        get_profit_impact_tool
    ]
)


# ---------------------------------------------------------
# TOOL EXECUTION
# ---------------------------------------------------------

def execute_tool(name, arguments):

    if name == "get_monthly_pnl":

        result = get_monthly_pnl()

    elif name == "get_monthly_variance":

        result = get_monthly_variance(
            arguments["previous_month"],
            arguments["current_month"]
        )

    elif name == "get_profit_impact":

        result = get_profit_impact(
            arguments["previous_month"],
            arguments["current_month"]
        )

    else:

        raise ValueError(f"Unknown tool: {name}")

    return result.round(2).to_dict(
        orient="records"
    )


# ---------------------------------------------------------
# AI FINANCIAL ANALYST
# ---------------------------------------------------------

def ask_financial_analyst(user_question, api_url):
    """
    Ask Gemini to analyze financial data retrieved
    from the FastAPI backend.
    """

    question = user_question.lower()

    # -------------------------------------------------
    # Get monthly P&L from FastAPI
    # -------------------------------------------------

    pnl_response = requests.get(
        f"{api_url}/pnl",
        timeout=30
    )

    pnl_response.raise_for_status()

    pnl_data = pnl_response.json()

    # -------------------------------------------------
    # Detect whether the user asked for a month-to-month
    # comparison
    # -------------------------------------------------

    month_map = {
        "january": "2026-01",
        "february": "2026-02",
        "march": "2026-03"
    }

    found_months = []

    for month_name, month_value in month_map.items():

        if month_name in question:
            found_months.append(month_value)

    found_months = list(dict.fromkeys(found_months))

    variance_data = []
    profit_impact_data = []

    if len(found_months) >= 2:

        previous_month = found_months[0]
        current_month = found_months[1]

        variance_response = requests.get(
            f"{api_url}/variance",
            params={
                "previous_month": previous_month,
                "current_month": current_month
            },
            timeout=30
        )

        variance_response.raise_for_status()

        variance_result = variance_response.json()

        variance_data = variance_result.get(
            "variance",
            []
        )

        profit_impact_data = variance_result.get(
            "profit_impact",
            []
        )

    # -------------------------------------------------
    # Build context for Gemini
    # -------------------------------------------------

    financial_context = {
        "monthly_pnl": pnl_data,
        "variance": variance_data,
        "profit_impact": profit_impact_data
    }

    prompt = f"""
You are the AI Financial Analyst for a restaurant
financial review application.

Answer the user's question using ONLY the financial
data provided below.

IMPORTANT RULES:

1. Never invent financial numbers.
2. Do not calculate new financial totals yourself.
3. Treat the provided Python/API results as the source
   of truth.
4. Format monetary values with $ and two decimal places.
5. Clearly explain the relevant financial drivers.
6. Distinguish facts from interpretation.
7. If the provided data is insufficient, say so.
8. Keep the answer concise and understandable.

USER QUESTION:
{user_question}

FINANCIAL DATA:
{json.dumps(financial_context, indent=2)}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text