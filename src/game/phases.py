from game.game_state import GameState
from player.base_player import Player
from player.ai_player import RandomAIPlayer
from player.human_player import HumanPlayer
import time
from termcolor import cprint

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
            print(f'Game Master :  {vote_result} was brutally executed by the town..')
        
        return state

    def debate_phase(self, state):
        print('Game Master :  Debate Phase is starting...')
        # Turn-based discussion
        for player in state.alive_players:
            state_summary = state.get_summary()
            message = player.get_message_player(state_summary) # AI need context to send message
            state.chat.add_message_p2p(sender=player, text=message, day=state.day)
        return state

    def voting_phase(self, state) -> Player:
        """
        Returns:
            _type_: _description_
        """
        votes = {player: 0 for player in state.alive_players}
        
        state_summary = state.get_summary()

        for current_player in state.alive_players:
            choices = [player for player in state.alive_players if player != current_player]
            vote = current_player.vote(choices, state_summary)  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
            state.chat.add_message_p2p('Game Master', f'Player {current_player} voted for {vote} !', state.day)

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p("Game Master", 
                                   f"Sentenced player is {most_voted} with {votes[most_voted]} votes.",
                                   state.day)
        return state, most_voted

    def summary_last_night(self):
        pass

    def __str__(self):
        return 'Day'

class NightPhase:
    def __init__(self):
        pass

    def execute(self, state):

        print("Night phase begins.")
        state.current_phase = self

        state, most_voted = self.werewolf_meeting(state)
        if most_voted != None:
            state.kill_player(most_voted)
            cprint(f'Game Master :  {most_voted} was brutally murdered in his sleep...', 'red')

        return state
    

    def werewolf_meeting(self, state: GameState):
        
        # Use Chat class to only send this to the werewolf
        state.chat.add_message_p2p('Game Master', 'This is the werewolf meeting...', state.day)

        list_werewolves = state.get_alive_role('Werewolf')
        list_villagers = state.get_alive_role('Villager')

        state_summary = state.get_summary()

        votes = {player: 0 for player in list_villagers}
        for current_player in list_werewolves:
            vote = current_player.vote(list_villagers, state_summary)  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
        # Determine player with most votes
        most_voted = max(votes, key=votes.get)
        print (f"Game Master :  Killed player is : {most_voted}")
        time.sleep(3)
        return state, most_voted
    
    def __str__(self):
        return 'Night'