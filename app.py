from proxybroker import Broker
import asyncio
import aiohttp
import os

def main():
    loop = asyncio.get_event_loop()
    broker = Broker(max_tries=1, loop=loop)
    host, port = '127.0.0.1', 8080
    types = [('HTTP', 'High')]
    broker.serve(host=host, port=port, types=types, limit=10, max_tries=3,prefer_connect=True, min_req_proxy=5, max_error_rate=0.5, max_resp_time=8, backlog=100, countries=['VN'])
    loop.run_forever()

if __name__ == '__main__':
    main()
