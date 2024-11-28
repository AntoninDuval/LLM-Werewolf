
class Chat:

    def __init__(self) -> None:
        self.history = []
    
    def add_message(self, player_name, text, state, recipients=None):
        content = f"{player_name} : {text} /n"

        self.history.append({
            "sender": player_name,
            "content": content,
            "recipients": recipients,
            "phase": state,
        })

        print(content)

    def get_all_messages(self):
        """Return all messages in the chat."""
        return self.messages
    
    def summarize(self, limit=5):
        """
        Summarize the chat history, showing the last `limit` messages.
        
        :param limit: The number of recent messages to include in the summary.
        """
        recent_messages = self.messages[-limit:]
        summary = "\n".join(
            f"[{msg['phase']}] {msg['sender']}: {msg['content']}"
            for msg in recent_messages
        )
        return summary if summary else "No messages yet."