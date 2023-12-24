import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    base_url='http://localhost:5005/v1',
    api_key=os.environ.get('OPENAI_API_KEY', 'x'),
)
messages = [
    SystemMessage(content="You are a helpful assistant."),
]
stream = True

while True:
    user_message = input("You: ")
    messages.append(HumanMessage(content=user_message))

    if stream:
        # get responses in chunks
        print('Eliza: ', end='', flush=True)
        response = ''
        for chunk in chat.stream(messages):
            if chunk.content is not None:
                print(chunk.content, end='', flush=True)
                response += chunk.content
        print('')
        response = AIMessage(content=response)
    else:
        # get responses all at once
        response = chat(messages)
        print('Eliza:', response.content)

    messages.append(response)
