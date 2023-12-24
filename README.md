# Eliza-GPT

[![Build status](https://github.com/miguelgrinberg/eliza-gpt/workflows/build/badge.svg)](https://github.com/miguelgrinberg/eliza-gpt/actions) [![codecov](https://codecov.io/gh/miguelgrinberg/eliza-gpt/branch/main/graph/badge.svg)](https://codecov.io/gh/miguelgrinberg/eliza-gpt)

[Eliza](https://en.wikipedia.org/wiki/ELIZA), the classic chatbot from the 1960s, running on OpenAI's [Chat Completions API](https://platform.openai.com/docs/api-reference/chat).

## Why?

The main reason is that this seemed like a fun project to help me acquire a greater understanding of the Chat Completions API from OpenAI, which has become a sort of standard for turn-based conversation between a human and a machine.

But also, it is great to have a fast and free service with negligible resource consumption that can be used as a stand-in for a real LLM when the quality of the responses do not matter, such as while doing development or testing.

## How To Use

Eliza-GPT is written in Python and can be installed with `pip`:

    $ pip install eliza-gpt

Once installed, run it to start it as a local service on your computer:


    $ eliza-gpt
    Eliza-GPT is running!
    Set base_url="http://127.0.0.1:5005/v1" in your OpenAI client to connect.

### Configuration

Run with `--help` to learn about configuration options, which include:

- Setting the listening IP address and port.
- Adding an API key for authentication.
- Changing the (simulated) response times. Set to 0 to have near immediate responses.

### Connecting With a Chat Client

If you are using the official Python client from OpenAI, add the `base_url` option to it as follows:

    openai_client = OpenAI(base_url='http://127.0.0.1:5005/v1')

If you use Langchain, then use the following to connect to Eliza-GPT:

    chat = ChatOpenAI(base_url='http://127.0.0.1:5005/v1')

If you have a custom client that talks directly to the chat completions endpoint, configure `http://127.0.0.1:5005/v1` as your endpoint.

Eliza-GPT supports both the direct and streaming interfaces.

## Examples

The [examples](https://github.com/miguelgrinberg/Eliza-GPT/tree/main/examples) directory includes demonstration applications implemented with the OpenAI client and Langchain.

## Implementation Details

Eliza-GPT implements a portion of the OpenAI Chat Completions API, ignoring anything that isn't useful. In particular, at this time only the `/v1/chat/completions` endpoint is implemented. Any other endpoint from the OpenAI API will return a 404 error to the caller.

The following aspects of the Chat Completions endpoint are currently supported:

- The chat history given in the `messages` argument. Only messages with role `user` are used to "prime" Eliza so that it provides a reasonable response.
- The `stream` argument, which determines if the response should be given in a single JSON object or as a stream of Server-Sent Events.
- The `seed` option, which makes it possible to have deterministic responses.

These are not used or not implemented:

- Any messages in the chat history that have a role different than `user`.
- Model names. Eliza-GPT returns the requested model name in the response.
- The `n` argument, which controls how many responses are returned. Eliza-GPT always returns a single response.
- The `max_tokens` argument.
- Temperature and other LLM-specific tuning parameters.
- The `stop` argument.
- Anything related to tools or functions that the model may call.
- Anything related to log probabilities.

## Credits

The Eliza chatbot used in this project is called [Eliza.py](https://github.com/rdimaio/eliza-py) and was created by Riccardo Di Maio.
