import threading
import Queue
from handler import CommandHandler

class CommandListener(threading.Thread):
    

    def __init__(self,command_queue = None, reply_queue = None, command_handler = None):
        super(CommandListener, self).__init__()
        self.__command_queue = command_queue
        self.__reply_queue = reply_queue
        self.stop_request = threading.Event()
        if command_handler:
            self.command_handler = command_handler
        else:
            self.command_handler = CommandHandler()

    def run(self):
        self.__reply_queue.put({'reply' : 'Starting command listener.'})
        while not self.stop_request.isSet():
            try:
                command = self.__command_queue.get(True, 0.05)
                reply_handler, reply = self.__handle(command)
                if reply:
                    self.__reply_queue.put({'reply' : reply, 'handler' : reply_handler})
            except Queue.Empty:
                continue

    def join(self, timeout = None):
        self.stop_request.set()
        super(CommandListener, self).join(timeout)
    
    def __handle(self, command = None):
        # handle the command with attached handler or default handler
        reply_handler = None
        command_text = None
        reply = None
        if 'command' in command:
            command_text = command['command']
            if 'reciever' in command:
                reply_handler = command['reciever']
        if command_text:
            reply = self.command_handler.handle(command_text)
        return reply_handler, reply