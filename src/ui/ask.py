import os
import openai

from llama_index import ChatPromptTemplate, StorageContext, load_index_from_storage
from datetime import date

print(os.environ["OPENAI_API_KEY"])
# Request OpenAI Key
#os.environ["OPENAI_API_KEY"] = input("OpenAI key:")
openai.api_key = os.environ["OPENAI_API_KEY"]


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="training_storage")
# load index
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
now = date.today()

# INSTRUCTIONS = f'''
#     Today's date is {now}.
#     Answer only if the question is relevant to student learning standards for mathematics.
#     Answer in simple language.
#     Refer the "context information" as "New Jersey Student Learning Standards for Mathematics".
#     If a specific page number is included in your response, call "context information" the "New Jersey Student Learning Standards for Mathematics" available at: https://www.nj.gov/education/standards/math/Index.shtml
# '''
program = 'New Jersey Student Learning Standards for Mathematics'

# loop q&a

def prepareprompt(now, program, question):
    RULES = f"""
        Never provide a response that contains illegal, hateful, or dangerous responses.
        Only answer questions that are relevant to {program}.
        """

    PROMPT = f"""
        This prompt will have three parts:
        1. CONTEXT, which is information that may help you respond to the prompt.
        2. RULES, which should never be broken when answering the prompt.
        3. QUESTION, which is a user-submitted question that starts with "QUESTION" and ends with "END_QUESTION.
        You should try to answer without breaking the rules. Never break the rules. The rules will be restated at the end of the prompt.
        If you cannot answer a question, or cannot answer with confidence, reply that you do not know the answer.
        CONTEXT:
        Today's date is {now}.
        You an an AI agent providing answers to questions about {program}.
        You may answer in any language specified in the QUESTION.
        Provide all answers in simple language.
        The provided context information is about {program}.
        RULES:
        {RULES}
        QUESTION
        {question}
        END_QUESTION
        RULES:
        {RULES}
        """
        
    return PROMPT

while True:
    print("")
    question = input("Enter question: ") 

    PROMPT = prepareprompt(now, program, question)

    response = query_engine.query(PROMPT)
    print(response)
