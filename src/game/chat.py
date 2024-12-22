import time

class Chat:

    def __init__(self) -> None:
        self.history = []
    
    def add_message_p2p(self, sender, text, day: int, recipients=None):
        content = f"[Day {day}] {sender} : {text}"

        self.history.append({
            "day": day,
            "sender": sender,
            "content": content,
            "recipients": recipients,
            #"phase": state,
        })

        print(content)
        time.sleep(0.5)

    def game_message_2p(self, text, recipients=None):
        print(text)

    def get_all_messages(self):
        """Return all messages in the chat."""
        return self.messages
    
    
    def summarize(self, limit=5):
        """
        Summarize the chat history, showing the last `limit` messages.
        
        :param limit: The number of recent messages to include in the summary.
        """
        recent_messages = self.history[-limit:]


        summary = "\n".join(
            f"{msg['content']}"
            for msg in recent_messages
        )
        return summary if summary else "No messages yet."