from game.game_state import GameState
from player.base_player import Player
from player.ai_player import RandomAIPlayer
from player.human_player import HumanPlayer
import time

DEBATE_TIME = 50

class DayPhase:
    def __init__(self):
        pass

    def execute(self, state: GameState):
        """
        Main logic for the day phase.
        """
        # Update the current phase in the chat
        state.chat.current_phase = 'Day'
        state.current_phase = 'Day'

        state.chat.add_message_p2p(sender="Game Master", text="Day phase begins.")
        state.chat.add_message_p2p( sender="Game Master", text=f"This is day n°{state.day}")


        # Summary of the last night
        if not state.day == 1:
            self.summary_last_night()

        # Debate phase
        state = self.debate_phase(state)

        state.chat.add_message_p2p( sender="Game Master", text=f"Your time to vote ! Decide who will be executed. Choose wisely...")

        state, vote_result = self.voting_phase(state)

        if vote_result != None:
            state.chat.add_message_p2p("Game Master", f"{vote_result} was brutally executed by the town...")
            state.kill_player(vote_result)
        
        return state

    def voting_phase(self, state) -> Player:
        """
        Returns:
            _type_: _description_
        """
        votes = {player: 0 for player in state.alive_players}

        for current_player in state.alive_players:
            choices = [player for player in state.alive_players if player != current_player]
            vote = current_player.vote(choices, state.get_summary(current_player))  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
            state.chat.add_message_p2p('Game Master', f'{current_player} voted for {vote} !')

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p("Game Master", 
                                   f"Sentenced player is {most_voted} with {votes[most_voted]} votes.")
        return state, most_voted

    def summary_last_night(self):
        pass

    def debate_phase(self, state):
        """
        Execute the debate phase for a limited amount of time.
        Players can send messages within the time limit.
        """
        state.chat.add_message_p2p(sender="Game Master", text="Debate phase begins. You have limited time to discuss!")

        # Start the timer. Debate should last for 50s.
        debate_end_time = time.time() + 50

        # Start the debate phase
        state = state.chat.discussion(state, 
                                      debate_end_time=debate_end_time,
                                      players_active=state.alive_players)

        return state

    def __str__(self):
        return 'Day'

class NightPhase:
    def __init__(self):
        pass

    def execute(self, state):
        
        # Update the current phase in the chat
        state.chat.current_phase = 'Night'
        state.current_phase = 'Night'

        state.chat.add_message_p2p("Game Master", 
                                   "Night phase begins. Who will the werewolves kill tonight ?",
                                   color='red')

        # Start discussion phase for werewolves if at least 2 are alive
        if len(state.get_alive_role('Werewolf')) >= 2:
            state = self.werewolf_debate(state)

        state, most_voted = self.werewolf_vote(state)

        if most_voted != None:
            state.chat.add_message_p2p("Game Master", 
                                   f"{most_voted} was brutally murdered in his sleep...",
                                   color='red')
            state.kill_player(most_voted)

        return state
    
    def werewolf_debate(self, state: GameState):
        """
        Execute the werewolf debate phase for a limited amount of time.
        Players can send messages within the time limit.
        """
        state.chat.add_message_p2p(sender="Game Master", text="Werewolf meeting begins. You have limited time to discuss!")

        # Start the timer. Werevolves should discuss for 20s.
        debate_end_time = time.time() + 20

        # Start the discussion
        state = state.chat.discussion(state, 
                                      players_active=state.get_alive_role('Werewolf'),
                                      debate_end_time=debate_end_time)

        return state
    

    def werewolf_vote(self, state: GameState):
        
        list_werewolves = state.get_alive_role('Werewolf')
        list_villagers = state.get_alive_role('Villager')

        state.chat.add_message_p2p('Game Master', 
                                   'Time to vote for the player you want to kill !', 
                                   recipients=list_werewolves)

        votes = {player: 0 for player in list_villagers}
        for current_player in list_werewolves:
            vote = current_player.vote(list_villagers, state.get_summary(current_player))  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p("Game Master", 
                                   f"You decided to kill {most_voted} with {votes[most_voted]} votes.",
                                   recipients=list_werewolves)
        
        time.sleep(3)
        return state, most_voted
    
    def __str__(self):
        return 'Night'