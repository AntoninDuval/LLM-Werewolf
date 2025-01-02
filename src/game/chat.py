import time
from termcolor import cprint
import sys
import threading
import queue
from player.human_player import HumanPlayer
from player.ai_player import RandomAIPlayer
import random


class Chat:

    def __init__(self) -> None:
        self.player_histories = {}
        self.day = 0
        self.current_phase = None

    def add_message_p2p(self, sender, text, recipients=None, color=None):

        if text is None:  # text can be none when AI decide not to answer
            return

        # Create a dictionary to store the message and metadata for the chat history
        message_dict = {
            "day": self.day,
            "phase": self.current_phase,
            "sender": sender,
            "text": text,
        }
        # Content that will be displayed in the chat
        content = f"[{self.current_phase} {self.day}] {sender}: {text}"

        if sender == "Game Master":
            content = f"\033[1m{content}\033[0m"  # Apply bold formatting

        # If recipients are not specified, broadcast to all players
        if recipients is None:
            for history in self.player_histories.values():
                history.append(message_dict)
        else:
            for recipient in recipients:
                if recipient.name in self.player_histories:
                    self.player_histories[recipient.name].append(message_dict)

        cprint(
            content, color=color
        )  # Print the message for visibility of human players
        time.sleep(0.5)

    def discussion(
        self,
        state,
        players_active,  # Players that can send messages in this discussion
        debate_end_time,
        threshold_no_message=5,
    ):
        """
        Allow players to send messages during a phase (debate or werevolves meeting).
        Players can be human or AI.
        A thread is created for each player to handle the input.
        A Queue is used to store the messages from the players.
        AI players post messages periodically or react to new messages.
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

                time.sleep(random.randint(7, 10))  # Simulate thinking time between
                with last_message_lock:
                    current_time = time.time()
                    # Post a new AI message if enough time has passed since the last message
                    if current_time - last_message_time["time"] >= threshold_no_message:
                        ai_message = player.get_message_player(
                            state.get_summary(player)
                        )
                        last_message_time["time"] = time.time()

                    else:
                        # React to the new message (immediate response)
                        ai_message = player.get_message_player(
                            state.get_summary(player)
                        )

                    if ai_message != "":
                        message_queue.put((player.name, ai_message))

                new_message_event.clear()  # Reset the event for future triggers
                time.sleep(
                    5
                )  # Wait Xs after sending a message to avoid spamming the chat

        # Start threads for players
        threads = []
        for player in players_active:

            if isinstance(player, HumanPlayer):
                thread = threading.Thread(
                    target=handle_human_input,
                    args=(player,),
                    name=f"Thread_Human_{player.name}",
                )
            else:
                thread = threading.Thread(
                    target=handle_ai_input,
                    args=(player,),
                    name=f"Thread_AI_{player.name}",
                )
            thread.daemon = True  # Ensure the thread stops when the program ends
            threads.append(thread)
            thread.start()

        last_printed_warning = None  # Keep track of the last second printed

        # Main loop for processing messages
        while time.time() < debate_end_time:

            remaining_time = int(debate_end_time - time.time())
            state.remaining_debate_time = remaining_time

            try:
                player_name, message = message_queue.get(timeout=0.1)
                state.chat.add_message_p2p(
                    player_name, message, recipients=players_active
                )
                new_message_event.set()  # Signal that the message has been processed
            except queue.Empty:
                pass

            # Print a warning message if the time is running out
            if remaining_time < 10 and remaining_time != last_printed_warning:
                print(
                    f"Game Master: Dicussion ends in {remaining_time} seconds...",
                    end="\r",
                )
                last_printed_warning = remaining_time  # Update the last remaining time

        # Simulate a short delay to avoid busy looping
        time.sleep(0.1)

        # Signal threads to stop and wait for them to terminate
        stop_event.set()
        for thread in threads:
            thread.join(timeout=1)

        print("Message collection has ended.")
        return state

    def game_message_2p(self, text, recipients=None):
        print(text)

    def initialize_player(self, player_name):
        """Initialize a chat history for a player."""
        if player_name not in self.player_histories:
            self.player_histories[player_name] = []

    def get_all_messages(self):
        """Return all messages in the chat."""
        return self.player_histories

    def get_chat_history_player(self, player_name, limit=0):
        """Return all last X messages in the chat history of a specific player."""
        chat_history = self.player_histories.get(player_name, [])[-limit:]
        if chat_history is None:
            raise KeyError(f"Player {player_name} does not exist in the chat history.")
        return chat_history
