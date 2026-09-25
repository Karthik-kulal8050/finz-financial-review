# Finz — AI-Native Financial Review Application

A financial review application that analyzes transaction data, automatically categorizes transactions, generates monthly Profit & Loss statements, identifies month-to-month financial variances, provides a human review workflow, and offers an AI Financial Analyst for natural-language financial analysis.

---

## Live Demo

[Open Finz Financial Review]https://finz-financial-review-ntmhd2syjj9cwfabpd4eev.streamlit.app/

## Overview

Finz is designed to help a business review transaction data and understand its financial performance without manually analyzing every transaction.

The application combines:

- Deterministic financial calculations
- Rule-based transaction categorization
- Human-in-the-loop review
- Monthly P&L analysis
- Month-to-month variance analysis
- Transaction-level drill-down
- Gemini-powered AI Financial Analyst
- FastAPI backend
- Streamlit frontend
- SQLite database

A key design principle is that **financial numbers are calculated from transaction data using Python**, while the AI layer is used for explanation and financial analysis. This prevents the AI model from inventing financial totals.

---

## Key Features

### 1. Transaction Ingestion

- Upload/read transaction data from Excel.
- Process transaction dates, descriptions, counterparties, and amounts.
- Automatically categorize transactions.
- Store processed transactions in SQLite.

### 2. Automatic Transaction Categorization

Transactions are categorized using deterministic rules based on transaction descriptions.

Supported categories include:

| Category | Examples | Included in P&L |
|---|---|---|
| REVENUE | Food sales, beverage sales, catering payments, delivery payouts | Yes |
| REFUNDS | Refunds and discounts | Yes |
| COGS | Food inventory, beverage inventory, catering food purchases | Yes |
| PAYROLL | Wages, salaries, payroll taxes and benefits | Yes |
| OPERATING_EXPENSE | Rent, software, insurance, marketing, utilities, repairs, etc. | Yes |
| CAPEX | Equipment purchases | No |
| TAX | Sales tax remittance | No |
| FINANCING | Loan principal repayment | No |
| EQUITY | Owner distribution | No |
| LIABILITY | Gift card sales deposits | No |
| UNKNOWN | Unclassified transactions | No |

Unknown transactions are automatically marked for human review.

---

## 3. Human-in-the-Loop Review

Transactions that may require special accounting treatment are placed into a review queue.

Examples include:

- Equipment purchases
- Tax remittances
- Loan principal repayments
- Owner distributions
- Gift card deposits
- Large catering purchases
- Annual license renewals

Users can:

1. Select a transaction.
2. Review its details.
3. Change the category.
4. Change the subcategory.
5. Save the correction.

Human corrections are stored with:

```text
classification_source = human
confidence = 1.0
requires_review = False

4. Monthly Profit & Loss Analysis

The application generates a monthly P&L directly from the categorized transaction data.

The calculation follows:

Gross Revenue
      -
Refunds
      =
Net Revenue

Net Revenue
      -
COGS
      =
Gross Profit

Gross Profit
      -
Payroll
      -
Operating Expenses
      =
Operating Profit

The system excludes non-operating transactions such as capital expenditures, loan principal repayments, owner distributions, taxes, and gift card liabilities from operating profit.

Example Monthly Results
Month	Gross Revenue	Net Revenue	Gross Profit	Operating Profit
January 2026	$128,821.61	$126,399.09	$82,425.32	$14,470.53
February 2026	$127,569.49	$125,617.29	$78,606.40	$6,007.96
March 2026	$154,122.87	$150,535.07	$98,486.43	$18,852.14

## AI Financial Analyst

The application includes a Gemini-powered AI Financial Analyst that allows users to ask natural-language questions about the financial data.

Examples:

- Why did operating profit change from January 2026 to February 2026?
- What was our operating profit in March 2026?
- What was our revenue in February 2026?
- Why did operating profit change from February 2026 to March 2026?

### AI Architecture

The application separates deterministic financial computation from AI-generated explanation.

```text
User Question
      |
      v
Streamlit Frontend
      |
      v
FastAPI Backend
      |
      v
SQLite Database
      |
      v
Python Financial Logic
      |
      +-------------------+
      |                   |
      v                   v
   Monthly P&L       Variance / Profit Impact
      |                   |
      +---------+---------+
                |
                v
        Verified Financial Data
                |
                v
           Gemini API
                |
                v
      Natural Language Explanation