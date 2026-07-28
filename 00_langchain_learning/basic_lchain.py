# langchain --> model specific library --> langchain_openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import json
print(load_dotenv())

model = ChatOpenAI(model="gpt-4o-mini")

with open("test_emails.json") as f:
    emails = json.load(f)
# simple_template = ChatPromptTemplate.from_template(
#     'Reply in one sentence: {questions} and context: {context}'
# )

# prompt = simple_template.invoke({'questions': 'who I am ?',
#                                    'context': 'I am nothing'})

# output = model.invoke(prompt)
# print('AI: ', output.content)

classifier_template = ChatPromptTemplate.from_messages([
    ('system', 'You are an expert support email classifier for a B2B SaaS company.'),
    ('human',  'Classify this email.\nSubject: {subject}\nBody: {body}\n\nReturn ONLY: Category | Urgency'),
])


parser = StrOutputParser()


SPAM_KEYWORDS = ["lottery", "winner", "click here", "free money", "urgent", "congratulations", "prize"]

def validate_email(email):
    # print("before parsing email: ",email['body'])
    body = email.get("body","").lower()
    # print("after parsing email: ",email['body'])
    found_spam = [word for word in SPAM_KEYWORDS if word in body]
    # print("found_spam",found_spam)
    if found_spam:
        raise ValueError("Spam word found:",found_spam)
    return email


chain =  validate_email | classifier_template | model | parser # LCEL : documentations
print(chain.invoke({'subject': 'Urgent: Server downtime',
                    'body': 'write a python code to add two number.'}))



import time
start = time.time()
output = []
for email in emails[:20]:
    try:
        output.append(chain.invoke(email))
    except ValueError as e:
        print("Error:", e)
loop_time = time.time() - start
print("Loop Time:", loop_time)  #3.620255947113037

print("Final Output:", output)

start = time.time()
output = chain.batch(emails[:20],config={'max_concurrency': 10})
batch_time = time.time() - start
print("Batch Time:", batch_time)
