import os, time
import Queue

from command_listener import CommandListener
from reply_processer import ReplyProcesser
from slack_handle import SlackHandle

# from slackbot import SlackBot
# from handler import CommandHandler

def main():
    # Queue with list of command from different input 
    commandQueue = Queue.Queue()
    
    # Queue with list of reply for different commands
    replyQueue = Queue.Queue()
    
    try:
        # use default command handler for now
        # initialize and start default command queue lister
        commandQueueListner = CommandListener(commandQueue, replyQueue)
        commandQueueListner.setDaemon(True)
        commandQueueListner.start()

        # initialize and start default reply queue processer
        replyQueueProcesser = ReplyProcesser(replyQueue)
        replyQueueProcesser.setDaemon(True)
        replyQueueProcesser.start()

        # initialize and start slack bot
        replyQueue.put({'reply' : 'Starting Slackbot.'})

        slackbot = SlackHandle(commandQueue)
        slackbot.setDaemon(True)
        slackbot.start()


        #loop system until keyboard interrupt 
        try:
            replyQueue.put({'reply' : 'All systems successfully up and running.'})
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print 'interrupted!'

    except Exception as e:
        os.system("espeak 'Oops! Something went wrong.'  2>>/dev/null")
        print('Oops! ' + e.message)


    # kill all threads

    commandQueueListner.join()
    replyQueueProcesser.join()
    slackbot.join()

    print('System shutting down. Manual start will be required.')
    os.system("espeak 'System shutting down. Manual start will be required.'  2>>/dev/null")


    # print('Starting slack bot')
    # os.system("espeak 'Starting slack bot' 2>>/dev/null")
    # try:
    #     handler = CommandHandler()
    #     lta_slack = SlackBot(handler)
    #     lta_slack.setDaemon(True)
    #     lta_slack.start()
    #     lta_slack.join()
    # except Exception as e:
    #     print (e.message)
    #     message = 'espeak "Error, %s" 2>>/dev/null' % e.message 
    #     os.system(message)
    

    # print('Slack bot stopped')
    # os.system("espeak 'Slack bot stopped'  2>>/dev/null")

if __name__ == '__main__':
    main()