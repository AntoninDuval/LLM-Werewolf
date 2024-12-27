import time
from termcolor import cprint

class Chat:

    def __init__(self) -> None:
        self.player_histories = {}
        self.day = 0
        self.current_phase = None
    
    def add_message_p2p(self, sender, text, recipients=None, color=None):

        if text is None: # text can be none when AI decide not to answer
            return
        
        content = f"[{self.current_phase} {self.day}] {sender}: {text}"

        # Apply bold formatting for Game Master messages
        if sender == "Game Master":
            content = f"\033[1m{content}\033[0m"  # Bold the message

        # If recipients are not specified, broadcast to all players
        if recipients is None:
            for history in self.player_histories.values():
                history.append(content)
        else:
            for recipient in recipients:
                if recipient.name in self.player_histories:
                    self.player_histories[recipient.name].append(content)

        cprint(content, color=color)  # Still print the message for visibility
        time.sleep(0.5)

    def game_message_2p(self, text, recipients=None):
        print(text)

    def initialize_player(self, player_name):
        """Initialize a chat history for a player."""
        if player_name not in self.player_histories:
            self.player_histories[player_name] = []

    def get_all_messages(self):
        """Return all messages in the chat."""
        return self.player_histories
    
    def get_history_player(self, player_name, limit=0):
        """Return all last X messages in the chat history of a specific player."""
        return self.player_histories.get(player_name, [])[-limit:]
    
    
    def summarize(self, player, limit=0):
        """
        Summarize the chat history, showing the last `limit` messages of a player.
        
        :param limit: The number of recent messages to include in the summary.
        """
        recent_messages = self.get_history_player(player)

        summary = "\n".join(
            f"{msg['content']}"
            for msg in recent_messages
        )
        return summary if summary else "No messages yet."