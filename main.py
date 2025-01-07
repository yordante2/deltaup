from deltachat2 import MsgData, events
from deltabot_cli import BotCli
import requests
import os
import moodleclient
import utils

cli = BotCli("echobot")

@cli.on(events.RawEvent)
def log_event(bot, accid, event):
    bot.logger.info(event)

@cli.on(events.NewMessage(command="/help"))
def help(bot, accid, event):
  msg = event.msg
  text = "Envíame un enlace a un archivo y lo subiré a una nube. Luego, puedes descargarlo usando la WiFi nacional o datos nacionales\nEjemplo: https://example.com/file.apk\nTamaño máximo por archivo: 300 MB\n\n⚠️ATENCIÓN⚠️: Este bot está en fase de pruebas, cualquier error puede reportarlo al [admin](https://i.delta.chat/#08E90CB530B253B73134D4A0756A77C9298D12B1&a=zzzzzzzzz%40nine.testrun.org&n=%EA%AA%97%EA%AA%AE%F0%9D%98%B3%E1%A6%94%EA%AA%96%EA%AA%80%F0%9D%93%BD%EA%AB%80&i=eb6zxidbnjF&s=vlMYAXW1lvo)."
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
      if size < 300:
        with open(filename, 'wb') as file:
            for chunk in req.iter_content(chunk_size=1024):
                file.write(chunk)
            file.close()
        try:
            newlink = moodleclient.upload_token(filename)
        except Exception as ex:
            bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=str(ex)))
        bot.rpc.send_reaction(accid, msg.id, [])
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=newlink))
        os.remove(filename)
    if size > 300:
      bot.rpc.send_msg(accid, msg.chat_id, MsgData(text="El archivo excede los 300 MB"))

if __name__ == "__main__":
    cli.start()
