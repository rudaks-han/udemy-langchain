from langchain_openai import ChatOpenAI, RunnableSequence
from langchain_openai.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
# from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
chat = ChatOpenAI()

prompt = ChatPromptTemplate(
    input_variables=["content"],
    messages=[
        HumanMessagePromptTemplate.from_template("{content}"),
    ]
)


# chain = LLMChain(
#     llm=chat,
#     prompt=prompt,
# )
sequence = RunnableSequence([prompt, chat])

while True:
    content = input(">> ")

    # print(f"You entered: {content}")
    # result = chain({"content": content})
    # result = chain.run({"content": content})
    result = sequence.run({"content": content})
    print(result["text"])
