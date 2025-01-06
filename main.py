from deltachat2 import MsgData, events
from deltabot_cli import BotCli
import requests
import os
import moodleclient
import utils

cli = BotCli("deltaup")

@cli.on(events.RawEvent)
def log_event(bot, accid, event):
    bot.logger.info(event)

@cli.on(events.NewMessage(command="/help"))
def help(bot, accid, event):
  msg = event.msg
  text = "Envíame un enlace a un archivo y lo subiré a Cursad. Luego, puedes descargarlo usando la WiFi nacional o datos nacionales\nEjemplo: https://example.com/file.apk\nTamaño máximo por archivo: 100 MB"
  bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=text))

@cli.on(events.NewMessage)
def uploadtocloud(bot, accid, event):
  msg = event.msg
  if msg.text.startswith("http"):
    bot.rpc.send_reaction(accid, msg.id, ["⏳"])
    url = msg.text
    req = requests.get(url, stream=True)
    if req.status_code == 200:
      filename = utils.get_url_file_name(url, req)
      size = int(req.headers.get('content-length', 0)) / (1024 * 1024)
      if size < 100:
        with open(filename, 'wb') as file:
            for chunk in req.iter_content(chunk_size=1024):
                file.write(chunk)
            file.close()
        try:
            newlink = moodleclient.upload_token(filename)
        except Exception as ex:
            bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=str(ex)))
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=newlink))
        os.remove(filename)

if __name__ == "__main__":
    cli.start()
