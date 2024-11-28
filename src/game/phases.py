class DayPhase:
    def __init__(self, state):
        self.state = state

    def execute(self):
        print("Day phase begins.")
        print(f"This is day n°{self.state['day']}")

        # Handle discussion and voting
        pass


class NightPhase:
    def __init__(self, state):
        self.state = state

    def execute(self):
        print("Night phase begins.")
        # Handle night actions (e.g., Werewolf kills, Seer investigates)
        pass
