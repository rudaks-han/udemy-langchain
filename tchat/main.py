from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

# memory_key는
# return_messages는 string이 아니라 object로 리턴하는 것을 의미
memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages",
    return_messages=True,
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

chain = LLMChain(llm=chat, prompt=prompt, memory=memory)

while True:
    content = input(">> ")

    result = chain({"content": content})
    print(result["text"])
