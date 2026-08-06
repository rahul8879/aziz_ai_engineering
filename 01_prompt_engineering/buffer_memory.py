from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # what is message placeholder ?? we will go throuigh this one
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory # this is inbuilt memmory in langchain 
from langchain_core.runnables.history import RunnableWithMessageHistory # wait for 15 mint
from langchain_core.messages import HumanMessage, AIMessage

model = ChatOpenAI(model="gpt-4o-mini")

history = InMemoryChatMessageHistory()
#if I want to add any message -->Human or AI message 
# history.add_user_message("I have a billing issue")
# history.add_ai_message("Undrstood you query but I can thelp you")

# history.add_user_message("I have a billing issue")
# history.add_ai_message("Undrstood you query but I can thelp you")

# print(history.messages)

template = ChatPromptTemplate.from_messages([
   ("system","You are a professional email support agent"),
   MessagesPlaceholder(variable_name="history"),
   ("human","{input}")

])

# past_messages = [
#     HumanMessage(content="Billing complaint from John — invoice #1042, overcharged $250."),
#     AIMessage(content="Classified: Billing — High Priority. SLA: 2 hours."),
# ]

# prompt = template.format_messages(history=past_messages, input="I have a billing issue")

# print(prompt)

prompt = ChatPromptTemplate.from_messages([
    ("system", """\
You are a professional email support agent.
Classify complaints as: Billing / Technical / General.
Priority: High (financial impact > $100 or urgent) / Medium / Low.
Remember all customer details throughout the conversation."""),
    MessagesPlaceholder(variable_name="history"),  # ← past turns injected here
    ("human", "{input}"),                           # ← new message here
])

chain = prompt | model | StrOutputParser()

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
# output = get_session_history("session_1")
# get_session_history("session_2")
# print(store)

emails_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


# let me call it emails_chain
cfg = {"configurable":{"session_id":"123rahul"}}


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    r = emails_chain.invoke({"input": user_input}, config=cfg)
    
    print('AI:', r)
    print('store:', store['123rahul'].messages)  # Print the messages for the current session
    