from player.base_player import Player
from utils.chat_utils import clear_input_after_enter
from typing import List

class HumanPlayer(Player):

    def get_message_player(self, state_summary: dict):

        user_msg = clear_input_after_enter(f'{self.name}, please write your message...')

        return user_msg
    
    def vote(self, choices: List[Player], state_summary : dict) -> Player:
        """"
        Actions where a Player is asked to vote for someone. Can happen during day time for hanging a villager or
        during night time with the werewolves for killing a villager. 

        Args:
            choices (List[Player]): List of players to vote for

        Returns:
            Player: _description_
        """
        
        for idx, player in enumerate(choices):
            print(f'(Game) : Type {idx} for voting for {player}')

        id_vote_player = -1
        while id_vote_player < 0:
            try:
                id_vote_player = int(input('Type the number for the player you want to vote for'))
            except ValueError as e:
                print('Please, type only a single integer')
        
        return choices[id_vote_player]
    
    def ask_username(self):
        self.name = clear_input_after_enter("What is your name ?")

    def __repr__(self):
        return f"Player(name={self.name}, role={self.role}, alive={self.alive})"