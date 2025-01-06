import requests
import json
import urllib
from random import randint
import os

def upload_token(filename):
  token = os.getenv("TOKEN")
  host = "https://cursad.jovenclub.cu"
  s = requests.session()
  data = {
    "token": token,
    "itemid": "0",
    "filearea": "draft"
  }
  files = {
    "file": (filename, open(filename, "rb"), "application/x-subrip"),
  }
  resp = s.post(f"{host}/webservice/upload.php", data=data, files=files)
  resp = json.loads(resp.text)[0]
  contextid, itemid, filename = resp["contextid"], resp["itemid"], resp["filename"]
  url = f"{host}/webservice/draftfile.php/{contextid}/user/draft/{itemid}/{urllib.parse.quote(filename)}?token={token}"
  return url
