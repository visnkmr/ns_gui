import sseclient
import json
# import pprint

# specify the URL of the SSE source
url = "http://localhost:6798/stream"
from sseclient import SSEClient

messages = SSEClient(url)
for msg in messages:
  print(json.loads(msg.data))
  