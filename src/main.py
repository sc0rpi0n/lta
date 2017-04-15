import os

from slackbot import SlackBot
from handler import CommandHandler

def main():
    print('Starting slack bot')
    os.system("espeak 'Starting slack bot' 2>>/dev/null")
    try:
        handler = CommandHandler()
        lta_slack = SlackBot(handler)
        lta_slack.start()
        lta_slack.join()
    except Exception as e:
        print (e.message)
        message = 'espeak "%s" 2>>/dev/null' % e.message 
        os.system(message)
    

    print('Slack bot stopped')
    os.system("espeak 'Slack bot stopped'  2>>/dev/null")

if __name__ == '__main__':
    main()