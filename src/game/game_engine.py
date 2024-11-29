from game.game_state import GameState
from game.phases import DayPhase, NightPhase
from player.ai_player import AIPlayer
from player.human_player import HumanPlayer
from random import shuffle

class GameEngine:
    def __init__(self, n_players, n_werewolfs):
        self.state = GameState()

        self.day_phase = DayPhase()
        self.night_phase = NightPhase()

        self.n_players = n_players
        self.n_werewolfs = n_werewolfs

        self.setup_game()

    def run(self):

        while not self.state.game_over:

            self.state.day += 1
            
            self.state = self.day_phase.execute(self.state)
            self.state = self.night_phase.execute(self.state)
            print(self.state)

        print("Game Over. Winner:", self.state.winner)
    

    def setup_game(self):
        roles = ["Werewolf"] * self.n_werewolfs + ["Villager"] * (self.n_players - self.n_werewolfs)
        shuffle(roles)
        for name, role in zip(["Player" + str(i) for i in range(self.n_players)], roles):
            player = HumanPlayer(name=name, role=role)  # Use HumanPlayer for real players
            self.state.add_player(player)