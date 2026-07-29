from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from typing import Literal
from dotenv import load_dotenv
load_dotenv()
import json
import pandas as pd
with open("test_emails.json") as f:
    emails = json.load(f)
class EmailClassification(BaseModel):
    category : Literal['Billing','technical','Feature request','Other'] = Field(description='the category of the support email')
    urgency: Literal['High', 'Medium', 'Low'] = Field(
        description='Urgency based on business impact'
    )

    confidence: int = Field(
        description='Confidence score from 1 to 10',
        ge=1,   # ge = greater than or equal (Pydantic v2!)
        le=10   # le = less than or equal
    )

    reasoning: str = Field(
        description='One sentence explanation of the classification'
    )
    

parser = PydanticOutputParser(pydantic_object=EmailClassification)

# print(parser.get_format_instructions())

cot_prompt = ChatPromptTemplate.from_messages([
    ('system', '''You are an expert support email classifier.

Classification Rules:
- Login broken after payment → Billing (NOT Technical)
- App crashes → Technical
- Pricing complaints + evaluating alternatives → Churn Risk
- Feature requests → Feature Request

Think step by step before classifying.

{format_instruction}'''),
     ('human', 'Subject: {subject}\nBody: {body}')
]).partial(format_instruction= parser.get_format_instructions())

llm = ChatOpenAI(model="gpt-4o-mini")

chain = cot_prompt | llm | parser

data = {
    'id': [email['id'] for email in emails[:20]],
    'body': [email['body'] for email in emails[:20]],
    'category':[],
    'urgency':[],
    'confidence': [],
    'reasoning': []
}

output = chain.batch(emails,config={"max_concurrency": 10})

for i, email in enumerate(emails):
    data['category'].append(output[i].category)
    data['urgency'].append(output[i].urgency)
    data['confidence'].append(output[i].confidence)
    data['reasoning'].append(output[i].reasoning)

df = pd.DataFrame(data)
# save the output
df.to_csv("email_classification_output.csv", index=False)
