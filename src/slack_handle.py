import os, threading, Queue, time
from slackclient import SlackClient

class SlackHandle(threading.Thread):

    # bot user id 
    __BOT_ID = os.environ.get('BOT_ID')
    # slack bot token generated from the slack app and integration settings
    __SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

    def __init__(self, command_queue = None):
        super(SlackHandle, self).__init__()
        self.__command_queue = command_queue
        self.stop_request = threading.Event()
        if self.__BOT_ID:
            self.__AT_BOT = "<@" + self.__BOT_ID + ">"
        else:
            raise Exception('Please define Bot Id in environment.')

        if self.__SLACK_BOT_TOKEN:
            self.__slack_client = SlackClient(self.__SLACK_BOT_TOKEN)
        else:
            raise Exception('Please define Slack Bot Token in environment.')
    
    def run(self):
        # try to connect to slack via rtm
        if self.__slack_client.rtm_connect():
            print('Slack bot started and connected')
            while not self.stop_request.isSet():
                # fetch changes and parse rtm json
                command, channel = self.__parse_slack_output(self.__slack_client.rtm_read())
                if command and channel:
                    commandQ = {'command' : command, 'reciever' : { 'handle' : self, 'params' : { 'channel' : channel } } }
                    # print(commandQ)
                    # Queue the commend to be processed by command listner and a command handler execute the command
                    self.__command_queue.put(commandQ)
                time.sleep(1)
        else:
            # there was an error connecting to slack
            print('Slack bot could not connect.')
            raise Exception('Slack bot could not connect.')
    
    def join(self, timeout = None):
        self.stop_request.set()
        super(SlackHandle, self).join(timeout)
    
    # Parse the slack rtm output and fetch the text and channel info from the json
    def __parse_slack_output(self, slack_rtm_output):
        if slack_rtm_output and len(slack_rtm_output) > 0:
            for output in slack_rtm_output:
                if output and 'text' in output and self.__AT_BOT in output['text']:
                    return output['text'].split(self.__AT_BOT)[1].strip().lower(), output['channel']
        return None, None
    
    # method is called by reply processor to send message back to user 
    def handle(self, message =  None, params = {}):
        if message and len(message) > 0 and 'channel' in params:
            self.__slack_client.api_call("chat.postMessage", channel= params['channel'], text=message, as_user=True)