# Examples

This directory contains client examples that can be used to quickly try out Eliza-GPT and learn how to incorporate it into your own LLM applications.

## openai_chat.py

This example uses the `openai` official Python client from OpenAI. To use this example, install the following dependencies (you should create a virtual environment first):

```bash
(venv) $ pip install eliza-gpt openai
```

You will need two terminal windows. On the first one, start Eliza-GPT:

```
(venv) $ eliza-gpt
Eliza-GPT is running!
Set base_url="http://127.0.0.1:5005/v1" in your OpenAI client to connect.
```

On the second terminal, run the client chat application:

```bash
(venv) $ python openai_chat.py
```

You can now chat away with Eliza.

## langchain_chat.py

This example uses the `langchain` package. To use this example, install the following dependencies (you should create a virtual environment first):

```bash
(venv) $ pip install eliza-gpt langchain openai
```

As with the previous example, you will need two terminal windows. On the first terminal, start Eliza-GPT:

```
(venv) $ eliza-gpt
Eliza-GPT is running!
Set base_url="http://127.0.0.1:5005/v1" in your OpenAI client to connect.
```

On the second terminal, run the client chat application:

```bash
(venv) $ python langchain_chat.py
```

You can now chat with Eliza.
