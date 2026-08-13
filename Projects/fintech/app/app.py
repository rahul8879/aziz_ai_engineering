from tools import get_loan_status, get_emi_schedule,process_refund_request,calculate_prepayment
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")


tools = [get_loan_status, get_emi_schedule, process_refund_request, calculate_prepayment]
llm_with_tools = llm.bind_tools(tools)
# print(response)

tool_map = {
    "get_loan_status": get_loan_status,
    "get_emi_schedule": get_emi_schedule,
    "process_refund_request": process_refund_request,
    "calculate_prepayment": calculate_prepayment
}

SYSTEM_PROMPT ="""
You are a professional  Finance customer support agent.

You have access to:
1. TOOLS  — for live loan data (status, EMI, prepayment, refund)
             Use when customer provides a Loan ID (BFL + digits)

RULES:
- Loan ID present → use tools
- Format all amounts with Rs and commas (e.g., Rs 8,450)
- Be warm, concise, and professional
- If a loan is not found, ask customer to double-check the Loan ID

"""

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Return existing chat history or create a new one for this session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def run_chat_turn(user_message:str,session_id):
    history = get_session_history(session_id)
    messages = [{'role':"system","content":SYSTEM_PROMPT}]
    messages.extend(history.messages)
    messages.append(HumanMessage(content=user_message))
    tools_used = []

    response = llm_with_tools.invoke(messages)

    while response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tools_used.append(tool_name)
            tool_fn = tool_map.get(tool_name)
            if tool_fn:
                result = tool_fn.invoke(tool_args)
            else:
                result = {"error":"tool is not available"}

            messages.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]

            ))
        response = llm_with_tools.invoke(messages)

    history.add_user_message(user_message)
    history.add_ai_message(response.content)
    return response.content, tools_used

