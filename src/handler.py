class CommandHandler():

    def __init__(self):
        pass
    
    def sayhi(self, command):
        return 'Hello, I am LTA. How may I help you ?'
    
    def do(self, command):
        return 'I would love to finish your request once you teach me how to do it.'
    
    def unknown_command(self, command):
        return 'I am not sure what you mean. I do not know how to process that request.'
    
    def random(self):
        return 'I did something.'

    def handle(self, command = 'hi'):
        command_switcher = {
            'hi' : self.sayhi,
            'hi.' : self.sayhi,
            'hi!' : self.sayhi,
            'hello' : self.sayhi,
            'hello.' : self.sayhi,
            'hello!' : self.sayhi,
            'do' : self.do,
            'do something' : self.random,
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