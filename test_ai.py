from ai.agent import ask_financial_analyst


question = "Why did operating profit change from January 2026 to February 2026?"


answer = ask_financial_analyst(question)


print("\nAI FINANCIAL ANALYST")
print("=" * 70)
print(answer)