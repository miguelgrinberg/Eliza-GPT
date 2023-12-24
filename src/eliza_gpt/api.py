import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'eliza_py'))

from microdot.asgi import Microdot
from eliza_gpt.v1 import api as api_v1


class ElizaGPT(Microdot):
    def __init__(self, api_key=None, avg_response_time=2):
        super().__init__()
        self.mount(api_v1, '/v1')
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.avg_response_time = avg_response_time
