import json
from model_setup import call_llm

body = """We're evaluating whether to stay on your platform or move to 
       Competitor X. The main blockers are: (1) missing Zapier integration, 
       (2) no bulk export feature, (3) pricing jumped 40% last renewal."""

prompt = f"""
    You are an expert support email classifier 
    for a SaaS product company
    Please classify my email.
    Category should be as follow only.
    - Billing
    - Technical
    - Feature Request
    - SPAM

    #RULE
    Dont include any other categories.
    OUTPUT FORMAT
    Category | URGENCY
    {body}

    """


output = call_llm(prompt)
print(output)