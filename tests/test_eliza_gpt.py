import json
import pytest
from eliza_gpt import ElizaGPT
from eliza_gpt.cli import main  # noqa: F401
from microdot.test_client import TestClient


@pytest.mark.asyncio
async def test_eliza_gpt():
    app = ElizaGPT(api_key='test', avg_response_time=0.01)
    client = TestClient(app)

    r = await client.post('/v1/chat/completions')
    assert r.status_code == 401

    r = await client.post(
        '/v1/chat/completions', headers={'Authorization': 'Bearer test'},
    )
    assert r.status_code == 400

    r = await client.post(
        '/v1/chat/completions', headers={'Authorization': 'Bearer test'},
        body={
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
            ],
        }
    )
    assert r.status_code == 400

    r = await client.post(
        '/v1/chat/completions', headers={'Authorization': 'Bearer test'},
        body={
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'I like Python.'},
            ],
        }
    )
    assert r.status_code == 200
    assert r.headers['Content-Type'].startswith('application/json')
    assert r.json['choices'][0]['message']['role'] == 'assistant'
    assert len(r.json['choices'][0]['message']['content']) > 0

    r = await client.post(
        '/v1/chat/completions', headers={'Authorization': 'Bearer test'},
        body={
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'I like Python.'},
            ],
            'stream': True,
            'seed': 123,
        }
    )
    assert r.status_code == 200
    assert r.headers['Content-Type'].startswith('text/event-stream')
    lines = r.body.splitlines()
    count = 0
    for line in lines:
        if line.startswith(b'data: '):
            if line == b'data: [DONE]':
                break
            count += 1
            chunk = json.loads(line[6:])
            assert chunk['choices'][0]['delta']['role'] == 'assistant'
            assert len(chunk['choices'][0]['delta']['content']) > 0
    assert count > 0
