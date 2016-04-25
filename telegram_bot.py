import telegram
from telegram.ext import Updater
import logging
import time
import os
import json
from watson_developer_cloud import DialogV1, SpeechToTextV1, PersonalityInsightsV2


pi_credentials = {
    "url": "https://gateway.watsonplatform.net/personality-insights/api",
    "password": "dqAT7Jeb6w0H",
    "username": "982c15b5-11fa-4910-bd4e-efc5e39bc931"
}

bot_token = '184561786:AAGT5NJjxPSqTm3P4b30_hmGLhnTzgZV34s'

dialog_credentials = {
    "url": "https://gateway.watsonplatform.net/dialog/api",
    "password": "Mw4bIj47ckGZ",
    "username": "a1d505c8-c92f-4cf7-8fec-9a5df38c53bd"
}
dialog_id = 'a103aed4-1141-42da-a618-889f6b634682'
dialog_id = '36206774-21b1-4c13-a4f2-8192461f51f6'

speech_to_text_credentials = {
    "url": "https://stream.watsonplatform.net/speech-to-text/api",
    "password": "Dquwd3TcGsws",
    "username": "62413b3c-e9d3-42e7-a013-5829170dba80"
}

obama_text = '';

audio_content_type = 'audio/ogg;codecs=opus'


def start(bot, update):
    print 'start called!'
    bot.watson_info = dict()
    bot.watson_info['dialog_id'] = dialog_id
    bot.personality_insights = PersonalityInsightsV2(url=pi_credentials['url'],
                                                     username=pi_credentials['username'],
                                                     password=pi_credentials['password'])

    bot.dialog = DialogV1(url=dialog_credentials['url'],
                            username=dialog_credentials['username'],
                            password=dialog_credentials['password'])
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
    #print dir(update.message)
    #print update.message.voice
    # if update.message.voice is not None:
    #     print 'got an audiofile!'
    #     voice_file = bot.getFile(update.message.voice.file_id)
    #     voice_file.download('voice.ogg')
    #     response = bot.speech_to_text.recognize(open('voice.ogg', 'rb'), audio_content_type)
    #     print response
    #     if response['results'] and float(response['results'][response['result_index']]['alternatives'][0]['confidence']) >= 0.6:
    #         update.message.text = response['results'][response['result_index']]['alternatives'][0]['transcript']
    #         print update.message.text

    #pi_response = bot.personality_insights.profile(obama_text)

    if update.message.text:
        print 'text got'
        response = bot.dialog.conversation(bot.watson_info['dialog_id'],
                    update.message.text,bot.watson_info['client_id'],
                    bot.watson_info['conversation_id'])
        text = response['response']
        print response
        print 'echoing!'
        for line in text:
            bot.sendMessage(update.message.chat_id, text=line)
    # else:
    #     bot.sendMessage(update.message.chat_id, text="Don't know! Rly, help me and try again!")
    print 'message sent!'

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    bot = telegram.Bot(token=bot_token)
    updater = Updater(token=bot_token)
    # updater.dispatcher.telegram_command_handlers.pop('start')
    updater.dispatcher.addTelegramCommandHandler('start', start)
    # updater.dispatcher.telegram_message_handlers.pop()
    updater.dispatcher.addTelegramMessageHandler(echo)
    updater.start_polling()
    print 'polled!'
    if "VCAP_SERVICES" in os.environ:
        vcaps = json.loads(os.environ["VCAP_SERVICES"])
        print vcaps
