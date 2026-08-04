from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage,ToolMessage
llm = ChatOpenAI(model="gpt-4o-mini")

# prompt = "I received a billing complaint from John about invoice #1042."

# print(llm.invoke(prompt).content[:100])

# call1 = llm.invoke("what was the invoice number.")
# print(call1.content)



# # lets do manual stitching of context or past convesations

# output = llm.invoke(
#     "I received a billing complaint from John about invoice #1042. "
#     "what is his invoice number."
# ).content

# print(output)

# user_turn_1 = "I received a billing complaint from John about invoice #1042. He was charged $500 instead of $250."

# ai_turn_1 = llm.invoke(user_turn_1)

# print(f"User: {user_turn_1}")
# print(f"AI:   {ai_turn_1}")

# user_turn_2 = "What category does his complaint fall under?"

# stitched_prompt_turn2 = f"""\
# Previous conversation:
# User: {user_turn_1}
# AI: {ai_turn_1}

# Now answer:
# User: {user_turn_2}"""

# ai_turn_2 = llm.invoke(stitched_prompt_turn2)
# print(ai_turn_2.content)


output = llm.invoke([
    SystemMessage(content="You are a formal email support agent. ALWAYS respond in exactly 3 bullet points. Never use paragraphs."),
    HumanMessage(content="I have a billing complaint from John about invoice #1042.")

]).content

print("output from llm: ", output)
