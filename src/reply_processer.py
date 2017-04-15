import os, threading, Queue, time

class ReplyProcesser(threading.Thread):

    def __init__(self, reply_queue = None):
        super(ReplyProcesser, self).__init__()
        self.__reply_queue = reply_queue
        self.stop_request = threading.Event()
    
    def run(self):
        while not self.stop_request.isSet():
            try:
                reply = self.__reply_queue.get(True, 0.05)
                message = None
                if 'reply' in reply and len(reply['reply']) > 0:
                    message = reply['reply']
                if 'handler' in reply:
                    handler = reply['handler']
                    handler['handle'].handle(message, handler['params'])
                else:
                    # default use espeak to relay message
                    if message:
                        os.system('espeak "%s" 2>>/dev/null' % message)
                        time.sleep(0.5)
            except Queue.Empty as e:
                continue
    
    def join(self, timeout = None):
        self.stop_request.set()
        super(ReplyProcesser, self).join(timeout)