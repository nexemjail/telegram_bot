import telegram
from telegram.ext import Updater
import logging
import time
import os
import json
from watson_developer_cloud import DialogV1, SpeechToTextV1

token = '184561786:AAGT5NJjxPSqTm3P4b30_hmGLhnTzgZV34s'

dialog_credinitials = {
    "url": "https://gateway.watsonplatform.net/dialog/api",
    "password": "Mw4bIj47ckGZ",
    "username": "a1d505c8-c92f-4cf7-8fec-9a5df38c53bd"
}
#dialog_id = '84f70117-de7b-4c79-8b1a-1958d06aa467'
dialog_id = 'a103aed4-1141-42da-a618-889f6b634682'

speech_to_text_credentials = {
    "url": "https://stream.watsonplatform.net/speech-to-text/api",
    "password": "Dquwd3TcGsws",
    "username": "62413b3c-e9d3-42e7-a013-5829170dba80"
}

audio_content_type = 'audio/ogg;codecs=opus'

def start(bot, update):
    print 'start called!'
    bot.watson_info = dict()
    bot.credinitials = dialog_credinitials
    bot.watson_info['dialog_id'] = dialog_id
    bot.dialog = DialogV1(username=dialog_credinitials['username'], password = dialog_credinitials['password'])
    response = bot.dialog.conversation(dialog_id)
    print 'got a resp from start'
    bot.speech_to_text = SpeechToTextV1(url=speech_to_text_credentials['url'],
                                        username=speech_to_text_credentials['username'],
                                        password=speech_to_text_credentials['password'])
    bot.watson_info['conversation_id'] = response['conversation_id']
    bot.watson_info['client_id'] = response['client_id']

    bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(response['response']))
    print 'sent a message!'


def echo(bot, update):
    print dir(update.message)
    print update.message.audio 
    if update.message.audio is not None:
        print 'got an audiofile!'
        response = bot.speech_to_text.recognize(update.message.audio, audio_content_type)
        print response
    else:
        print 'text got'
        response = bot.dialog.conversation(bot.watson_info['dialog_id'],update.message.text,bot.watson_info['client_id'],
                    bot.watson_info['conversation_id'])
        print response
    print 'echoing!'
    bot.sendMessage(update.message.chat_id, text ='\n'.join(response['response']))
    print 'message sent!'

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    bot = telegram.Bot(token=token)
    updater = Updater(token=token)
    # updater.dispatcher.telegram_command_handlers.pop('start')
    updater.dispatcher.addTelegramCommandHandler('start', start)
    # updater.dispatcher.telegram_message_handlers.pop()
    updater.dispatcher.addTelegramMessageHandler(echo)
    updater.start_polling()
    print 'polled!'
    if "VCAP_SERVICES" in os.environ:
        vcaps = json.loads(os.environ["VCAP_SERVICES"])
        print vcaps
