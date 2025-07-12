from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from modules.document_qa import answer_question

template = """
You are the CFO of BAGIC. Based on the latest earnings call data, write a confident and insightful investor comment for the following concern:

{prompt}

Use professional language and relevant performance metrics.
"""

def generate_cfo_comment(user_input):
llm = ChatOpenAI(temperature=0.5)
prompt = PromptTemplate(input_variables=["prompt"], template=template)
context = answer_question(user_input)
final_prompt = prompt.format(prompt=user_input + "\nContext: " + context)
return llm.predict(final_prompt)