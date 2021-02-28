import asyncio as aio
import ssl
import pathlib
from websockets import serve, WebSocketServerProtocol, ConnectionClosed
import json
from emoji import Emoji
from res import Response
import os
from helpers import safe_mkdir
from plotting import HBarPlot

def save_print(data, file):
  # print(f'{data}\n')
  file.write(data)

def update_emojis(emojis, dir, emoji):
  name, url = emoji.name, emoji.url

  if any([e.name == name for e in emojis]):
    return emojis
  else:
    emojis.add(Emoji(name, url, dir))
    return emojis
  

async def main(ws: WebSocketServerProtocol, path: str):
  print("Connection established")
  stream_id = await ws.recv() 
  emojis = set()
  emojis_data = {}
  safe_mkdir(f'./log/{stream_id}')

  with open(f'./log/log-{stream_id}.json', mode='a') as f:
    f.write("[\n")
    dir = f'./log/{stream_id}'
    cnt = 0
    plot = HBarPlot("emojis") 
    
    save_print(await ws.recv(), f)

    while True:
      try:
        data_raw = await ws.recv()
        save_print(f',{data_raw}', f)
        data: Response = json.loads(data_raw, object_hook=Response.from_json)

        for emoji in data.emojis:
          emojis = update_emojis(emojis, dir, emoji)

          if not emoji.name in emojis_data:
            emojis_data[emoji.name] = 0

          emojis_data[emoji.name] += 1
         
        plot.update(emojis_data)
        print(data_raw)

        cnt += 1
        if cnt > 15:
          cnt = 0
          f.flush()

        if len(data.emojis) > 0:
          plot.render()

      except ConnectionClosed as e: 
        print(f'Terminated[{e.code}]: \n{e.reason}\n\n')
        f.flush()
        break
    
    plot.save(f'{dir}/emoji-plot.jpeg')
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