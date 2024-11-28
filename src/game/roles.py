class Role:
    def __init__(self, name):
        self.name = name

class Werewolf(Role):
    def __init__(self):
        super().__init__("Werewolf")

    def perform_night_action(self, state):
        # Logic for targeting a player
        pass

class Villager(Role):
    def __init__(self):
        super().__init__("Villager")