import argparse
from eliza_gpt.api import ElizaGPT


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', type=str, default='127.0.0.1',
        help='The host or IP address to listen on (default "127.0.0.1")')
    parser.add_argument(
        '--port', type=int, default=5005,
        help='The port to listen on (default 5005)')
    parser.add_argument(
        '--debug', action='store_true',
        help='Show incoming requests in the terminal')
    parser.add_argument(
        '--api-key', type=str, default=None,
        help='The API key to use for authentication')
    parser.add_argument(
        '--avg-response-time', type=float, default=2,
        help='The average response time in seconds (default 2 seconds)')
    args = parser.parse_args()

    print('Eliza-GPT is running!')
    print(f'Set base_url="http://{args.host}:{args.port}/v1" in your OpenAI '
          'client to connect.')
    app = ElizaGPT(api_key=args.api_key,
                   avg_response_time=args.avg_response_time)
    app.run(host=args.host, port=args.port, debug=args.debug)
