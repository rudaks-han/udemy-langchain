from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()

queue = Queue()

class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        queue.put(token)

    def on_llm_end(self, response, **kwargs):
        queue.put(None)

    def on_llm_error(self, error, **kwargs):
        queue.put(None)

chat = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

class StramingChain(LLMChain):
    def stream(self, input):
        def task():
            self(input)

        Thread(target=task).start()

        self(input)
        while True:
            token = queue.get()
            if token is None:
                break
            yield token

chain = StramingChain(llm=chat,prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)


# chain = LLMChain(llm=chat,prompt=prompt)
#
# for output in chain.stream(input={"content": "tell me a joke"}):
#     print(output)

# messages = prompt.format_messages(content="tell me a joke")

# print(messages)
#
# for message in chat.stream(messages):
#     print(message.content)