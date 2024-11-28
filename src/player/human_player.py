from player.base_player import Player

class HumanPlayer(Player):
    def take_action(self, state):
        pass

    def __repr__(self):
        return f"Player(name={self.name}, role={self.role}, alive={self.alive})"