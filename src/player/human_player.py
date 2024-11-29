from player.base_player import Player
from game.game_state import GameState
from typing import List

class HumanPlayer(Player):

    def write_message(self, state: GameState):
        text = input(f'{self.name}, please write your message...')
        state.chat.add_message(self.name, text)
        return state
    
    def vote(self, state: GameState, choices: List[Player]) -> Player:
        """"
        Actions where a Player is asked to vote for someone. Can happen during day time for hanging a villager or
        during night time with the werewolves for killing a villager. 

        Args:
            state (GameState): Current state of the Game
            choices (List[Player]): List of players to vote for

        Returns:
            Player: _description_
        """
        
        for idx, player in enumerate(choices):
            print(f'(Game) : Type {idx} for voting for {player}')

        vote_player = -1
        while vote_player < 0:
            try:
                vote_player = int(input('Type the number for the player you want to vote for'))
            except ValueError as e:
                print('Please, type only a single integer')
        
        return state.alive_players[vote_player]

    def __repr__(self):
        return f"Player(name={self.name}, role={self.role}, alive={self.alive})"