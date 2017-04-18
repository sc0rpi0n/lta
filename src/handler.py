import os, platform

class CommandHandler():

    def __init__(self):
        pass
    
    def sayhi(self, command):
        return 'Hello, I am LTA. How may I help you ?'
    
    def do(self, command):
        return 'I would love to finish your request once you teach me how to do it.'
    
    def unknown_command(self, command):
        return 'I am not sure what you mean. I do not know how to process that request.'
    
    def say(self, command):
        message = 'espeak "%s" 2>>/dev/null' % command.split('say')[1].strip().lower() 
        os.system(message)
        return 'Did you hear me say ' + command.split('say')[1].strip().lower()
    
    def systeminfo(self, command):
        os.system('espeak "I am here." 2>>/dev/null')
        return "dist: %s \n system: %s \n machine: %s \n platform: %s \n uname: %s \n version: %s \n mac_ver: %s \n  %s" % (
            str(platform.dist()),
            platform.system(),
            platform.machine(),
            platform.platform(),
            platform.uname(),
            platform.version(),
            platform.mac_ver(),
            os.popen('vcgencmd measure_temp').readline(),
            )

    def handle(self, command = 'hi'):
        command_switcher = {
            'hi' : self.sayhi,
            'hi.' : self.sayhi,
            'hi!' : self.sayhi,
            'hello' : self.sayhi,
            'hello.' : self.sayhi,
            'hello!' : self.sayhi,
            'do' : self.do,
            'say' : self.say,
            'system_info' : self.systeminfo,
        }
        try:
            command_start = command.split(' ')[0]
            if command_start and len(command_start) > 0:
                func = command_switcher.get(command_start,self.unknown_command)
            else:
                func = self.unknown_command
        except Exception as e:
            func = self.unknown_command
        return func(command)
