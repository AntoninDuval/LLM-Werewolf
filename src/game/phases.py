from game.game_state import GameState
from player.base_player import Player
from player.ai_player import RandomAIPlayer
from player.human_player import HumanPlayer
import time
import sys
import threading
import queue

DEBATE_TIME = 20

class DayPhase:
    def __init__(self):
        pass

    def execute(self, state: GameState):
        
        # Update the current phase in the chat
        state.chat.current_phase = 'Day'

        state.chat.add_message_p2p(sender="Game Master", text="Day phase begins.")
        state.chat.add_message_p2p( sender="Game Master", text=f"This is day n°{state.day}")

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
        debate_end_time = time.time() + DEBATE_TIME

        state = self.collect_messages(state, debate_end_time)

        return state
        
    def collect_messages(self, state, debate_end_time, threshold_no_message=10):
        """
        Collect messages from players as long as the debate phase is active.
        """
        # Queue to store human player messages from input threads
        message_queue = queue.Queue()
        # Flag to stop input threads gracefully
        stop_event = threading.Event()
        new_message_event = threading.Event()  # Signals when a new message is added

        # Shared timer to track the time since the last message
        last_message_time = {"time": time.time()}
        last_message_lock = threading.Lock()

        def handle_human_input(player):
            """
            Function to handle non-blocking input for human players.
            Adds the input message to the queue.
            """
            while not stop_event.is_set() and time.time() < debate_end_time:
                try:
                    # Prompt the player for input
                    message = input()
                    # Clear the input prompt after the player writes
                    sys.stdout.write("\033[F\033[K")
                    sys.stdout.flush()
                    # Add the message to the queue
                    message_queue.put((player.name, message))
                    with last_message_lock:
                        last_message_time["time"] = time.time()
                except EOFError:
                    break

        def handle_ai_input(player):
            """
            AI player posts a message every X seconds or reacts to a new message.
            """
            while not stop_event.is_set() and time.time() < debate_end_time:

                # Wait for either new_message_event or timeout (for periodic posting)
                new_message_event.wait(timeout=threshold_no_message)

                with last_message_lock:
                    current_time = time.time()
                    # Post a new AI message if enough time has passed since the last message
                    if current_time - last_message_time["time"] >= threshold_no_message:
                        ai_message = player.get_message_player(state.get_summary(player))
                        message_queue.put((player.name, ai_message))
                        last_message_time["time"] = time.time()

                    else:
                        # React to the new message (immediate response)
                        ai_message = player.get_message_player(state.get_summary(player))
                        message_queue.put((player.name, ai_message))

                new_message_event.clear()  # Reset the event for future triggers
                time.sleep(1)  # Check every second

        # Start threads for players
        threads = []
        for player in state.alive_players:
            if isinstance(player, HumanPlayer):
                thread = threading.Thread(target=handle_human_input, args=(player,))
                thread.daemon = True  # Ensure the thread stops when the program ends
                threads.append(thread)
                thread.start()

            elif isinstance(player, RandomAIPlayer):
                thread = threading.Thread(target=handle_ai_input, args=(player,))
                thread.daemon = True
                threads.append(thread)
                thread.start()

        last_printed_warning = None  # Keep track of the last second printed

        # Main loop for processing messages
        while time.time() < debate_end_time:

            try:
                player_name, message = message_queue.get(timeout=0.1)
                state.chat.add_message_p2p(player_name, message)
                new_message_event.set()  # Signal that the message has been processed
            except queue.Empty:
                pass

            remaining_time = int(debate_end_time - time.time())

            if remaining_time < 10 and remaining_time != last_printed_warning:
                print(f"Game Master: Debate phase ends in {remaining_time} seconds...", end="\r")
                last_printed_warning = remaining_time  # Update the last remaining time

        # Simulate a short delay to avoid busy looping
        time.sleep(0.1)

        # Signal threads to stop and wait for them to terminate
        stop_event.set()
        for thread in threads:
            thread.join(timeout=1)

        print("Message collection has ended.")
        return state

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