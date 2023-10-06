import os
import openai

from llama_index import StorageContext, load_index_from_storage
from datetime import date

print(os.environ["OPENAI_API_KEY"])
# Request OpenAI Key
#os.environ["OPENAI_API_KEY"] = input("OpenAI key:")
openai.api_key = os.environ["OPENAI_API_KEY"]


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="training_storage")
# load index
index = load_index_from_storage(storage_context)


now = date.today()
INSTRUCTIONS = f'''
    Today's date is {now}.
    Answer only if the question is relevant to student learning standards for mathematics.
    Answer in simple language.
    Refer the "context information" as "New Jersey Student Learning Standards for Mathematics".
    If a specific page number is included in your response, call "context information" the "New Jersey Student Learning Standards for Mathematics" available at: https://www.nj.gov/education/standards/math/Index.shtml
'''


# loop q&a
query_engine = index.as_query_engine()
while True:
    print("")
    question = input("Enter question: ") + INSTRUCTIONS
    response = query_engine.query(question)
    print(response)
