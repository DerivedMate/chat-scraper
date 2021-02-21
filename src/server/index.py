import asyncio as aio
import ssl
import pathlib
from websockets import serve, WebSocketServerProtocol, ConnectionClosed

async def main(ws: WebSocketServerProtocol, path: str):
  while True:
    try:
      print(f'{await ws.recv()}\n')
    except ConnectionClosed:
      print(f"Terminated")
      break
  

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_crt = "./lh.crt"
localhost_key = "./lh.key"
ssl_context.load_cert_chain(localhost_crt, localhost_key)

run_server = serve(main, "0.0.0.0", 9001, ssl=ssl_context)
aio.get_event_loop().run_until_complete(run_server)
print("Server ready!")
aio.get_event_loop().run_forever() 