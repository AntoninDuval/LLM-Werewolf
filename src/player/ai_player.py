
from player.base_player import Player
from random import choice, randint
from faker import Faker
from typing import List
import random
import time

class RandomAIPlayer(Player):

    def get_message_player(self, state_summary : dict):

        # Get a probability to answer
        if random.random() > 0.3: # 1/2
            user_msg = self.generate_random_sentence(10)
        else:
            return None

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