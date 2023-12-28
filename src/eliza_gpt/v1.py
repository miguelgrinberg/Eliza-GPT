import asyncio
import random
import time
import uuid
from microdot import Microdot
from microdot.sse import sse_response
from eliza_py.utils.startup import setup as eliza_setup
from eliza_py.utils.response import generate_response as run_eliza
from eliza_py.eliza import GENERAL_SCRIPT_PATH, SCRIPT_PATH

api = Microdot()
general_script, script, memory_inputs, _ = eliza_setup(
    GENERAL_SCRIPT_PATH, SCRIPT_PATH)
system_fingerprint = uuid.uuid4().hex


async def get_response_from_eliza(messages):
    memory_stack = []
    response = ''
    for msg in messages:
        response = run_eliza(msg, script, general_script['substitutions'],
                             memory_stack, memory_inputs)
        await asyncio.sleep(0)
    response = response.replace('Eliza: ', '')
    response = response.replace('\nYou: ', '')
    return response


@api.post('/chat/completions')
async def chat_completions(request):
    if request.app.api_key is not None:  # pragma: no branch
        if request.headers.get('Authorization') != \
                f'Bearer {request.app.api_key}':
            return {'error': 'Invalid API key'}, 401
    if request.json is None:
        return {'error': 'No data provided'}, 400

    messages = [msg['content'] for msg in request.json.get('messages', [])
                if msg['role'] == 'user']
    if len(messages) == 0:
        return {'error': 'No messages provided'}, 400

    chat_id = uuid.uuid4().hex
    created = int(time.time())
    model = request.json.get('model', 'eliza-gpt')
    seed = request.json.get('seed')
    if seed:
        random.seed(seed)
    response = await get_response_from_eliza(messages)

    if not request.json.get('stream', False):
        if request.app.avg_response_time:  # pragma: no branch
            await asyncio.sleep(
                random.random() * request.app.avg_response_time * 2)
        return {
            'id': chat_id,
            'created': created,
            'model': model,
            'system_fingerprint': system_fingerprint,
            'choices': [
                {
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': response,
                    },
                    'finish_reason': 'stop',
                    'logprobs': None,
                }
            ]
        }

    async def send_chunks(request, sse):
        chunks = response.split(' ')
        for i in range(len(chunks)):
            last_chunk = i == len(chunks) - 1
            if request.app.avg_response_time:  # pragma: no branch
                await asyncio.sleep(
                    random.random() * request.app.avg_response_time * 2 / 10)
            await sse.send({
                'id': chat_id,
                'created': created,
                'model': model,
                'system_fingerprint': system_fingerprint,
                'object': 'chat.completion.chunk',
                'choices': [
                    {
                        'index': 0,
                        'delta': {
                            'role': 'assistant',
                            'content': chunks[i] + ('' if last_chunk else ' ')
                        },
                        'finish_reason': 'stop' if last_chunk else None,
                    },
                ],
            })
        await sse.send('[DONE]')

    return sse_response(request, send_chunks)
