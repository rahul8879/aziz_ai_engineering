from tools import get_loan_status, get_emi_schedule,process_refund_request,calculate_prepayment
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import Optional
load_dotenv()

from rag_chain import rag_answer

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# Phase 0 
tools = [get_loan_status, get_emi_schedule, process_refund_request, calculate_prepayment]
llm_with_tools = llm.bind_tools(tools)
# print(response)

tool_map = {
    "get_loan_status": get_loan_status,
    "get_emi_schedule": get_emi_schedule,
    "process_refund_request": process_refund_request,
    "calculate_prepayment": calculate_prepayment
}

ROUTER_PROMPT = """
You are a query classifier for Bajaj Finance helpdesk.

Classify the customer query into ONE of these categories:
- "tool"   : query requires live loan data (needs Loan ID like BFL001)
              Examples: loan status, EMI schedule, prepayment, refund,
              foreclose my loan, close my loan, settle my account
- "policy" : query is about rules, eligibility, charges, documents
              AND follow-up questions about a previous policy answer
              Examples: CIBIL score, foreclosure charges, interest rates,
              documents needed, what happens if I miss EMI,
              "how do you know this", "where did you get this",
              "is this from your policy", "what is your source"
- "general": greeting, thank you, out of scope

Reply with ONLY one word: tool / policy / general
"""

def classify_query(query):
    response = llm.invoke([
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=query),
    ])
    category = response.content.strip()
    if category not in ["tool", "policy", "general"]:
        raise ValueError(f"Invalid category: {category}")
    return category

result = classify_query("hi")
print(f"Query category: {result}")  # Expected output: "tool"
