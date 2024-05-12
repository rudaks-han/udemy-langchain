from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

api_key = "sk-xxx"

llm = OpenAI(openai_api_key=api_key)

code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"],
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
)

# result = llm("Write a very very short poem")
result = code_chain({"language": "python", "task": "return a list of numbers"})

print(result)
