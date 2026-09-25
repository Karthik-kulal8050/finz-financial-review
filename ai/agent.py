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

def ask_financial_analyst(user_question):

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[tools],
        temperature=0.2
    )

    chat = client.chats.create(
        model=MODEL_NAME,
        config=config
    )

    response = chat.send_message(user_question)

    while True:

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:

                function_calls.append(
                    part.function_call
                )

        if not function_calls:
            break

        tool_responses = []

        for function_call in function_calls:

            name = function_call.name

            arguments = dict(
                function_call.args
            )

            result = execute_tool(
                name,
                arguments
            )

            tool_responses.append(
                types.Part.from_function_response(
                    name=name,
                    response={
                        "data": result
                    }
                )
            )

        response = chat.send_message(
            tool_responses
        )

    return response.text