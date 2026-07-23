
# Billing , technical,  SPAM
import json
from model_setup import call_llm
with open("test_emails.json") as f:
    emails = json.load(f)

# print(emails[0]['body'])
def cleaning_output(text):
    dummy_result = text.split('|')
    category = dummy_result[0].strip()
    reason = dummy_result[1].strip()
    return category, reason


result = {}
for i in emails[:5]:
    body = i['body']
    prompt = f"""
    You are an expert support email classifier 
   for a SaaS product company
    Please classify my email.
                Category should be as follow only.
                - Billing
                - Technical
                - SPAM

                #RULE
                Dont include any other categories.
                OUTPUT FORMAT
                Category | Reason
                {body}

                """
    category, reason = cleaning_output(call_llm(prompt))
    result[i['id']] = {
        'category': category,
        'reason': reason
    }


# store your result into pandas csv/excel
import pandas as pd
df = pd.DataFrame.from_dict(result, orient='index')
df.to_csv('email_classification_results.csv')
print(result)



