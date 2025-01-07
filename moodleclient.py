import requests
import json
import urllib
from random import randint
from convert import main as convert
import asyncio
import os

#proxy = "socks5://172.104.209.44:1080"

#proxies = {
#  'http': proxy,
#  'https': proxy
#}

def upload_token(filename):
  token = os.getenv("TOKEN")
  host = "https://aulavirtual.upec.cu"
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
  url = f"{host}/draftfile.php/{contextid}/user/draft/{itemid}/{urllib.parse.quote(filename)}"
  newurl = asyncio.run(convert(url))
  newurl = str(newurl).replace("pluginfile.php", "webservice/pluginfile.php").replace("'", "").replace("[", "").replace("]", "")
  newurl = str(newurl) + "?token=" + token
  return newurl
