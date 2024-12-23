from game.game_state import GameState
from player.base_player import Player
from player.ai_player import RandomAIPlayer
from player.human_player import HumanPlayer
import time
from termcolor import cprint
import threading

class DayPhase:
    def __init__(self):
        pass

    def execute(self, state: GameState):
        
        # Update the current phase in the chat
        state.chat.current_phase = 'Day'

        state.chat.add_message_p2p(sender="Game Master", text="Day phase begins.")
        state.chat.add_message_p2p( sender="Game Master", text=f" This is day n°{state.day}")

        state.current_phase = self

        # Summary of the last night
        if not state.day == 1:
            self.summary_last_night()

        # Debate phase
        state = self.debate_phase(state)

        state, vote_result = self.voting_phase(state)

        if vote_result != None:
            state.kill_player(vote_result)
            print(f'Game Master :  {vote_result} was brutally executed by the town..')
        
        return state

    def debate_phase(self, state):
        state.chat.add_message_p2p(sender="Game Master", text="Debate phase begins.")

        # Turn-based discussion
        for player in state.alive_players:
            state_summary = state.get_summary(player)
            message = player.get_message_player(state_summary) # AI need context to send message
            state.chat.add_message_p2p(sender=player, text=message)
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
            state.chat.add_message_p2p('Game Master', f'Player {current_player} voted for {vote} !')

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

        # Start the timer
        debate_end_time = time.time() + self.debate_duration

        # Start a thread to collect messages asynchronously
        input_thread = threading.Thread(target=self.collect_messages, args=(state, debate_end_time))
        input_thread.daemon = True  # Daemonize the thread so it exits with the program
        input_thread.start()

        # Keep track of the timer and show the remaining time
        while time.time() < debate_end_time:
            remaining_time = int(debate_end_time - time.time())
            print(f"Game Master: Debate phase ends in {remaining_time} seconds...", end="\r")
            time.sleep(1)  # Update every second

        print("\nGame Master: The debate phase has ended! No more messages allowed.")
        input_thread.join(timeout=1)  # Ensure thread ends after the debate duration
        
    def collect_messages(self, state, debate_end_time):
        """
        Collect messages from players as long as the debate phase is active.
        """
        while time.time() < debate_end_time:
            for player in state.alive_players:
                if isinstance(player, HumanPlayer):
                    # Non-blocking input for human players
                    message = input(f"{player.name}, write your message: ")
                    state.chat.add_message_p2p(player.name, message)
                elif isinstance(player, RandomAIPlayer):
                    # Generate an AI message
                    ai_message = player.get_message_player(state.get_summary())
                    state.chat.add_message_p2p(player.name, ai_message)
                    time.sleep(1)  # Simulate delay for AI

    def __str__(self):
        return 'Day'

class NightPhase:
    def __init__(self):
        pass

    def execute(self, state):
        
        # Update the current phase in the chat
        state.chat.current_phase = 'Night'

        print("Night phase begins.")
        state.current_phase = self

        state, most_voted = self.werewolf_meeting(state)
        if most_voted != None:
            state.kill_player(most_voted)
            state.chat.add_message_p2p("Game Master", 
                                   f"{most_voted} was brutally murdered in his sleep...",
                                   color='red')

        return state
    

    def werewolf_meeting(self, state: GameState):
        
        # Use Chat class to only send this to the werewolf
        state.chat.add_message_p2p('Game Master', 'This is the werewolf meeting...')

        list_werewolves = state.get_alive_role('Werewolf')
        list_villagers = state.get_alive_role('Villager')

        votes = {player: 0 for player in list_villagers}
        for current_player in list_werewolves:
            vote = current_player.vote(list_villagers, state.get_summary(current_player))  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p("Game Master", 
                                   f"You decided to kill {most_voted} with {votes[most_voted]} votes.")
        
        time.sleep(3)
        return state, most_voted
    
    def __str__(self):
        return 'Night'