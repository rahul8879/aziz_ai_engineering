
import os
from model_setup import call_llm

def load_prompts(filename):
    path = os.path.join('prompts', filename)
    with open(path, 'r') as file:
        return file.read()
    
def cleaning(text):
    val = text.split('\n')
    category = val[0].split(':')[1].strip()
    urgency = val[1].split(':')[1].strip()
    return category

template = load_prompts('cot_prompts.md')

body = """We're evaluating whether to stay on your platform or move to
       Competitor X. The main blockers are: (1) missing Zapier integration,
       (2) no bulk export feature, (3) pricing jumped 40% last renewal."""

prompt = template.format(body=body)
# output = call_llm(prompt)


# print(output)

result = []
for i in range(5):
    val = call_llm(prompt)
    result.append(cleaning(val))

#import counter

from collections import Counter

counter = Counter(result)
print(counter)





