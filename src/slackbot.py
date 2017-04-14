import os
import time
import threading
from slackclient import SlackClient

class SlackBot(threading.Thread):
    
    __BOT_ID = os.environ.get('BOT_ID')
    __SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

    def __init__(self, command_handler = None):
        threading.Thread.__init__(self)
        if self.__BOT_ID:
            self.__AT_BOT = "<@" + self.__BOT_ID + ">"
        else:
            raise Exception('Please define Bot Id in environment.')

        if self.__SLACK_BOT_TOKEN:
            self.__slack_client = SlackClient(self.__SLACK_BOT_TOKEN)
        else:
            raise Exception('Please define Slack Bot Token in environment.')
        self.__command_handler = command_handler
    
    def __parse_slack_output(self, slack_rtm_output):
        if slack_rtm_output and len(slack_rtm_output) > 0:
            for output in slack_rtm_output:
                if output and 'text' in output and self.__AT_BOT in output['text']:
                    return output['text'].split(self.__AT_BOT)[1].strip().lower(), output['channel']
        return None, None
    
    def __handle_command(self, command, channel):
        message = "Not sure what you mean."
        if self.__command_handler:
            message = self.__command_handler.handle(command)
        else:
            if command.startswith('hi'):
                message = 'Hello, how may I help you ?'
            elif command.startswith('do'):
                message = 'I would love to once you code how to do it.'
            else:
                pass
            
            self.__slack_client.api_call("chat.postMessage", channel= channel, text=message, as_user=True)
    
    def run(self):
        if self.__slack_client.rtm_connect():
            print('Slack bot started and connected')
            while True:
                command, channel = self.__parse_slack_output(self.__slack_client.rtm_read())
                if command and channel:
                    self.__handle_command(command, channel)
                time.sleep(1)
        else:
            print('Slack bot could not connect.')
            raise Exception('Slack bot could not connect.')