from game.game_state import GameState
from player.base_player import Player

class DayPhase:
    def __init__(self):
        pass

    def execute(self, state: GameState):
        print("Game Master :  Day phase begins.")
        print(f"Game Master :  This is day n°{state.day}")

        state.current_phase = self

        if not state.day == 1:
            self.summary_last_night()

        state = self.debate_phase(state)

        state, vote_result = self.voting_phase(state)

        if vote_result != None:
            state.kill_player(vote_result)
            print(f'Game Master :  {vote_result} was brutally executed...')
        
        return state

    def debate_phase(self, state):
        print('Game Master :  Debate Phase is starting...')
        for player in state.alive_players:
            player.write_message(state)
        return state

    def voting_phase(self, state) -> Player:
        """
        Returns:
            _type_: _description_
        """
        votes = {player.name: 0 for player in state.alive_players}
        
        for current_player in state.alive_players:
            choices = [player for player in state.alive_players if player != current_player]
            vote = current_player.vote(state, choices)  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
        
        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        print (f"Game Master :  Sentenced player is : {most_voted}")
        return state, most_voted

    def summary_last_night(self):
        pass

class NightPhase:
    def __init__(self):
        pass

    def execute(self, state):

        print("Night phase begins.")
        state.current_phase = self

        state = self.werewolf_meeting(state)

        return state
    

    def werewolf_meeting(self, state: GameState):
        
        # Use Chat class to only send this to the werewolf
        state.chat.add_message('Game Master', 'This is the werewolf meeting...')

        list_werewolves = state.get_alive_role('Werewolf')
        list_villagers = state.get_alive_role('Villager')

        votes = {player.name: 0 for player in list_villagers}
        for current_player in list_werewolves:
            vote = current_player.vote(state, list_villagers)  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
        # Determine player with most votes
        most_voted = max(votes, key=votes.get)
        print (f"Game Master :  Killed player is : {most_voted}")
        return most_voted