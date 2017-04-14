from slackbot import SlackBot
from handler import CommandHandler

def main():
    print('Starting slack bot')
    try:
        handler = CommandHandler()
        lta_slack = SlackBot(handler)
        lta_slack.start()
        lta_slack.join()
    except Exception as e:
        print (e.message)
    

    print('Slack bot stopped')

if __name__ == '__main__':
    main()