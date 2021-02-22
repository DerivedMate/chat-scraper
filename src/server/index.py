import asyncio as aio
import ssl
import pathlib
from websockets import serve, WebSocketServerProtocol, ConnectionClosed

def save_print(data, file):
  print(f'{data}\n')
  file.write(data)

async def main(ws: WebSocketServerProtocol, path: str):
  print("Connection established")
  stream_id = await ws.recv() 

  with open(f'./log/log-{stream_id}.json', mode='a') as f:
    f.write("[\n")
    cnt = 0
    
    save_print(await ws.recv(), f)

    while True:
      try:
        save_print(f',{await ws.recv()}', f)

        cnt += 1
        if cnt > 15:
          cnt = 0
          f.flush()

      except ConnectionClosed:
        print(f"Terminated")
        break

    f.write("]")
    f.flush()
    f.close()
  

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_crt = "./lh.crt"
localhost_key = "./lh.key"
ssl_context.load_cert_chain(localhost_crt, localhost_key)

run_server = serve(main, "0.0.0.0", 9001, ssl=ssl_context)
aio.get_event_loop().run_until_complete(run_server)
print("Server ready!")
aio.get_event_loop().run_forever() 