from threading import Thread
import time
from time import sleep

from KnowledgeBase import KnowledgeBase

CLEANUP_PERIOD = 15 * 60     # Time given in seconds
CHANNEL_LIFETIME = 60 * 60   # Time given in seconds

class ChannelsManager:
    class __ChannelsManager:
        def __init__(self):
            self.communicationChannels = []
            self.data = KnowledgeBase()
            
        def generate_uniqueToken(self):
            # Find an unique ID
            new_token = 1
            while any(channel['token'] == new_token for channel in self.communicationChannels):
                new_token += 1
                
            # Add the channel to the list
            channel = {
                "token": new_token,
                "timestamp": time.time(),
                "responses": []
            }
            self.communicationChannels.append(channel)
            
            return new_token
        
        def check_tokenPresent(self, token):
            for channel in self.communicationChannels:
                if channel['token'] == token:
                    return True
            return False
        
        def check_questionsAnswered(self, token):
            for channel in self.communicationChannels:
                if channel['token'] == token:
                    responses = channel['responses']
            
            rule = self.data.rules
            for response in responses:
                if response == True:
                    rule = rule['true']
                else:
                    rule = rule['false']
                    
            return 'condition' not in rule

        def update_responses(self, token, response):
            for channel in self.communicationChannels:
                if channel['token'] == token:
                    channel['responses'].append(response)

        def get_responseForToken(self, token):
            for channel in self.communicationChannels:
                if channel['token'] == token:
                    responses = channel['responses']
                    
            rule = self.data.rules
            if len(responses) == 0:
                return {
                    'question': True,
                    'text': str(rule['condition']['question'])
                }
            else:
                for response in responses:
                    if response == True:
                        rule = rule['true']
                    else:
                        rule = rule['false']
                if 'condition' in rule:
                    return {
                        'question': True,
                        'text': str(rule['condition']['question'])
                    }
                else:
                    return {
                        'question': False,
                        'text': str(rule['answer'])
                    }
                    
        def get_results(self, token):
            for channel in self.communicationChannels:
                if channel['token'] == token:
                    responses = channel['responses']
                    
            return self.data.filter_universitiesPrograms(responses)
            
    instance = None
    def __init__(self):
        if not ChannelsManager.instance:
            ChannelsManager.instance = ChannelsManager.__ChannelsManager()
            thread_channelsCleanUp = Thread(target=self._token_cleanUp)
            thread_channelsCleanUp.start()
            
    def _token_cleanUp(self):
        while True:
            sleep(CLEANUP_PERIOD)
            now = time.time()
            active_channels = [channel for channel in ChannelsManager.instance.communicationChannels if (now - channel["timestamp"]) < CHANNEL_LIFETIME]
            ChannelsManager.instance.communicationChannels = active_channels
