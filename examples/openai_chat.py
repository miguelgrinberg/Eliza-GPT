from openai import OpenAI

openai_client = OpenAI(base_url='http://localhost:5005/v1')
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]
stream = True  # set to False to get all responses at once

while True:
    user_message = input("You: ")
    messages.append({"role": "user", "content": user_message})

    if stream:
        # this returns the responses in chunks
        stream = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )
        print('Eliza: ', end='', flush=True)
        response = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='', flush=True)
                response += chunk.choices[0].delta.content
        print('')

    else:
        # this returns the response all at once
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        response = completion.choices[0].message.content
        print('Eliza:', response)

    messages.append({"role": "assistant", "content": response})
