import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from ai.agent import ask_financial_analyst

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Finz Financial Review",
    page_icon="💰",
    layout="wide"
)


st.title("Finz Financial Review")
st.caption("AI-native financial transaction analysis")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Transactions",
        "Review Queue",
        "Variance Analysis",
        "AI Financial Analyst"
    ]
)


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if page == "Dashboard":

    st.header("Financial Dashboard")

    response = requests.get(
        f"{API_URL}/pnl"
    )

    if response.status_code == 200:

        pnl_data = response.json()

        pnl = pd.DataFrame(pnl_data)

        if not pnl.empty:

            # Get latest month
            latest = pnl.iloc[-1]

            # -----------------------------------------
            # KPI CARDS
            # -----------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Gross Revenue",
                f"${latest['Gross Revenue']:,.2f}"
            )

            col2.metric(
                "Net Revenue",
                f"${latest['Net Revenue']:,.2f}"
            )

            col3.metric(
                "Gross Profit",
                f"${latest['Gross Profit']:,.2f}"
            )

            col4.metric(
                "Operating Profit",
                f"${latest['Operating Profit']:,.2f}"
            )

            st.divider()

            # -----------------------------------------
            # MONTHLY P&L
            # -----------------------------------------

            st.subheader("Monthly P&L")

            display_pnl = pnl.copy()

            numeric_columns = [
                "Gross Revenue",
                "Refunds",
                "Net Revenue",
                "COGS",
                "Gross Profit",
                "Payroll",
                "Operating Expenses",
                "Operating Profit"
            ]

            for column in numeric_columns:

                display_pnl[column] = display_pnl[column].map(
                    lambda x: f"${x:,.2f}"
                )

            st.dataframe(
                display_pnl,
                width=True,
                hide_index=True
            )

            st.divider()

            # -----------------------------------------
            # OPERATING PROFIT TREND
            # -----------------------------------------

            st.subheader("Operating Profit Trend")

            chart = px.line(
                pnl,
                x="Month",
                y="Operating Profit",
                markers=True,
                title="Monthly Operating Profit"
            )

            chart.update_layout(
                yaxis_title="Operating Profit ($)",
                xaxis_title="Month"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

        else:

            st.warning("No P&L data available.")

    else:

        st.error("Could not load P&L data.")


# --------------------------------------------------
# Transactions
# --------------------------------------------------

elif page == "Transactions":

    st.header("Transactions")

    response = requests.get(
        f"{API_URL}/transactions"
    )

    if response.status_code == 200:

        transactions = response.json()

        st.dataframe(
            transactions,
            width=True
        )

    else:

        st.error("Could not load transactions.")


# --------------------------------------------------
# Review Queue
# --------------------------------------------------

elif page == "Review Queue":

    st.header("Review Queue")

    response = requests.get(
        f"{API_URL}/review-queue"
    )

    if response.status_code != 200:

        st.error("Could not load review queue.")

    else:

        review_items = response.json()

        if not review_items:

            st.success(
                "No transactions currently require review."
            )

        else:

            st.write(
                f"Transactions requiring review: "
                f"**{len(review_items)}**"
            )

            review_df = pd.DataFrame(review_items)

            st.dataframe(
                review_df,
                width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("Review Transaction")

            transaction_ids = [
                item["transaction_id"]
                for item in review_items
            ]

            selected_id = st.selectbox(
                "Select transaction",
                transaction_ids
            )

            selected = next(
                item
                for item in review_items
                if item["transaction_id"] == selected_id
            )

            st.write("### Transaction Details")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Description:** "
                    f"{selected['description']}"
                )

                st.write(
                    f"**Amount:** "
                    f"${selected['amount']:,.2f}"
                )

            with col2:

                st.write(
                    f"**Current Category:** "
                    f"{selected['category']}"
                )

                st.write(
                    f"**Current Subcategory:** "
                    f"{selected['subcategory']}"
                )

            st.divider()

            st.subheader("Correct Classification")

            categories = [
                "REVENUE",
                "REFUNDS",
                "COGS",
                "PAYROLL",
                "OPERATING_EXPENSE",
                "CAPEX",
                "TAX",
                "FINANCING",
                "EQUITY",
                "LIABILITY"
            ]

            new_category = st.selectbox(
                "Category",
                categories,
                index=(
                    categories.index(
                        selected["category"]
                    )
                    if selected["category"] in categories
                    else 0
                )
            )

            new_subcategory = st.text_input(
                "Subcategory",
                value=selected["subcategory"]
            )

            if st.button(
                "Save Correction",
                type="primary"
            ):

                correction_data = {
                    "transaction_id": selected_id,
                    "category": new_category,
                    "subcategory": new_subcategory
                }

                correction_response = requests.patch(
                    f"{API_URL}/transactions/correct",
                    json=correction_data
                )

                if correction_response.status_code == 200:

                    st.success(
                        "Correction saved successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to save correction."
                    )

#--------------------------------------------------------
# Variance Analysis
#--------------------------------------------------------

elif page == "Variance Analysis":

    st.header("Month-to-Month Variance Analysis")

    col1, col2 = st.columns(2)

    with col1:

        previous_month = st.selectbox(
            "Previous Month",
            [
                "2026-01",
                "2026-02"
            ]
        )

    with col2:

        current_month = st.selectbox(
            "Current Month",
            [
                "2026-02",
                "2026-03"
            ]
        )

    if previous_month == current_month:

        st.warning(
            "Please select two different months."
        )

    else:

        response = requests.get(
            f"{API_URL}/variance",
            params={
                "previous_month": previous_month,
                "current_month": current_month
            }
        )

        if response.status_code == 200:

            result = response.json()

            variance = pd.DataFrame(
                result["variance"]
            )

            profit_impact = pd.DataFrame(
                result["profit_impact"]
            )

            # ----------------------------------
            # VARIANCE TABLE
            # ----------------------------------

            st.subheader(
                f"{previous_month} → {current_month}"
            )

            st.dataframe(
                variance,
                width=True,
                hide_index=True
            )

            st.divider()

            # ----------------------------------
            # PROFIT IMPACT
            # ----------------------------------

            st.subheader(
                "Profit Impact Drivers"
            )

            st.dataframe(
                profit_impact,
                width=True,
                hide_index=True
            )

            # ----------------------------------
            # PROFIT IMPACT CHART
            # ----------------------------------

            chart = px.bar(
                profit_impact,
                x="Driver",
                y="Profit Impact",
                title="Profit Impact by Driver"
            )

            chart.update_layout(
                xaxis_title="Driver",
                yaxis_title="Profit Impact ($)"
            )

            st.plotly_chart(
                chart,
                width=True
            )
            st.divider()

            st.subheader("Transaction Drill-Down")

            selected_category = st.selectbox(
                "Select a category",
                [
                    "REVENUE",
                    "REFUNDS",
                    "COGS",
                    "PAYROLL",
                    "OPERATING_EXPENSE"
                ]
            )

            transaction_response = requests.get(
                f"{API_URL}/category-transactions",
                params={
                    "month": current_month,
                    "category": selected_category
                }
            )

            if transaction_response.status_code == 200:

                transactions = transaction_response.json()

                if transactions:

                    transaction_df = pd.DataFrame(
                        transactions
                    )

                    st.write(
                        f"Transactions for "
                        f"**{selected_category}** "
                        f"in **{current_month}**"
                    )

                    st.dataframe(
                        transaction_df,
                        width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No transactions found for this category."
                    )

            else:

                st.error(
                    "Could not load category transactions."
                )

        else:

            st.error(
                "Could not calculate variance."
            )


# --------------------------------------------------
# AI Financial Analyst
# --------------------------------------------------

elif page == "AI Financial Analyst":

    st.header(" AI Financial Analyst")

    st.write(
        "Ask questions about revenue, costs, profitability, "
        "and month-to-month financial changes."
    )

    st.info(
        "Financial figures are calculated from transaction data "
        "using deterministic Python logic."
    )

    question = st.text_area(
        "Ask a financial question",
        placeholder=(
            "Example: Why did operating profit change "
            "from January 2026 to February 2026?"
        ),
        height=100
    )

    if st.button("Analyze", type="primary"):

        if not question.strip():

            st.warning("Please enter a financial question.")

        else:

            with st.spinner("Analyzing financial data..."):

                answer = ask_financial_analyst(question)

            st.markdown("### Financial Analyst")

            safe_answer = answer.replace("$", "USD ")
            st.markdown(safe_answer)