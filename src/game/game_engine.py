from game.game_state import GameState
from game.phases import DayPhase, NightPhase

class GameEngine:
    def __init__(self, n_players, n_werewolfs):
        self.state = GameState(n_players, n_werewolfs)
        self.day_phase = DayPhase(self.state)
        self.night_phase = NightPhase(self.state)

    def run(self):
        while not self.state.game_over:
            self.state.run()
            print(self.state)

        print("Game Over. Winner:", self.state.winner)