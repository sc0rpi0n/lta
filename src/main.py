from slackbot import SlackBot

def main():
    print('Starting slack bot')
    try:
        lta_slack = SlackBot()
        lta_slack.start()
        print('Slack bot started')
        lta_slack.join()
    except Exception as e:
        print (e.message)
    

    print('Slack bot stopped')

if __name__ == '__main__':
    main()