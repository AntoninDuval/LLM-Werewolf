
from random import shuffle
from game.chat import Chat

class GameState:
    def __init__(self):
        self.players = []  # List of player objects
        self.alive_players = []
        self.dead_players = []
        self.winner = None
        self.game_over = False
        self.current_phase = None
        self.day = 0
        self.chat = Chat()


    def add_player(self, player):
        """Add a new player to the game."""
        self.players.append(player)
        self.alive_players.append(player)

    def kill_player(self, player):
        """Eliminate a player from the game."""
        if player in self.alive_players:
            self.alive_players.remove(player)
            self.dead_players.append(player)
            player.alive = False

    def get_state(self):
        """Provide a summary of the current game state."""
        return {
            "day": self.n_day,
            "alive_players": [p.name for p in self.alive_players],
            "dead_players": [p.name for p in self.dead_players],
            "current_phase": self.current_phase,
        }
    
    def get_alive_role(self, role):
        list_alive = [player for player in self.players if player.role == role]
        return list_alive


    def check_victory(self):
        mafia_count = sum(1 for p in self.alive_players if p.role == "Werewolf")
        villager_count = sum(1 for p in self.alive_players if p.role != "Werewolf")
        if mafia_count == 0:
            self.winner = "Villagers"
            self.game_over = True
        elif mafia_count >= villager_count:
            self.winner = "Werewolves"
            self.game_over = True
        return self.game_over

    def get_alive_players_by_role(self, role):
        """Return a list of alive players with the given role."""
        return [p for p in self.alive_players if p.role == role]
    
    def __str__(self):
        alive_names = ", ".join([p.name for p in self.alive_players])
        dead_names = ", ".join([p.name for p in self.dead_players])
        last_actions = "\n".join(self.history[-5:]) if self.history else "No actions yet."
        return (
            f"Game State Summary:\n"
            f"-------------------\n"
            f"Current Phase: {self.current_phase}\n"
            f"Alive Players: {alive_names}\n"
            f"Dead Players: {dead_names}\n"
            f"Last Actions:\n{last_actions}\n"
            f"Game Over: {'Yes' if self.game_over else 'No'}\n"
            f"Winner: {self.winner if self.winner else 'TBD'}\n"
        )