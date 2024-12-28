
from player.base_player import Player
from random import choice, randint
from faker import Faker
from typing import List
import random
import time

class RandomAIPlayer(Player):

    def __init__(self, name, role):
        super().__init__(name, role)
        
        # Set a random number between 0 and 0.5 to determine the frequency of the AI to speak
        self.frequency_speak = random.random() * 0.5

    def get_message_player(self, state_summary : dict):

        message_history_current_phase = self.parse_chat_history(state_summary['chat_history'], 
                                                                phase=state_summary['current_phase'], 
                                                                day=state_summary['current_day'])
        
        # Get 1st word for last message from the chat
        first_word_last_message = message_history_current_phase[-1].split()[0] if message_history_current_phase else None

        # Get a probability to answer
        if random.random() > self.frequency_speak:
            user_msg = self.generate_random_sentence(1)
        else:
            return None
        
        # Add last message seen for debugging
        user_msg += f' (1st word last message seen : "{first_word_last_message}")'

        return user_msg
    
    def vote(self, choices: List[Player], state_summary : dict) -> Player:

        # Make a random vote after waiting for a random amount of time.
        voted_player = choice(choices)
        time.sleep(0.2)
        return voted_player

    
    def generate_random_sentence(self, word_count):
        fake = Faker()
        sentence = " ".join(fake.words(nb=word_count))
        return sentence
    
    def parse_chat_history(self, chat_history, phase, day):
        """Parse the chat history to extract information."""
        # Example of a chat history
        # [{'day': 1, 'phase': 'Day', 'sender': 'Game Master', 'text': 'Day phase begins.'}, {'day': 1, 'phase': 'Day', 'sender': 'Game Master', 'text': 'This is day n°1'}, {'day': 1, 'phase': 'Day', 'sender': 'Game Master', 'text': 'Debate phase begins. You have limited time to discuss!'}, {'day': 1, 'phase': 'Day', 'sender': 'Player2', 'text': 'Hi !'}]

        # Extract the messages from the chat history that are not from the Game Master
        # And from the same phase and day as asked
        messages = [msg['text'] for msg in chat_history if msg['sender'] != 'Game Master' and msg['phase'] == phase and msg['day'] == day]
        return messages
    
