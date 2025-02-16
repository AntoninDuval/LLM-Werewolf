from game.game_state import GameState
from player.base_player import Player
from player.ai_player import RandomAIPlayer
from player.human_player import HumanPlayer
import time


class DayPhase:
    def __init__(self, debate_time):
        self.debate_time = debate_time

    def execute(self, state: GameState):
        """
        Main logic for the day phase.
        """

        state.chat.add_message_p2p(sender="Game Master", text="Day phase begins.")
        state.chat.add_message_p2p(
            sender="Game Master", text=f"This is day n°{state.day}"
        )

        # Update the current phase in the chat
        state.chat.current_phase = "Day Debate"
        state.current_phase = "Day Debate"

        # Debate phase
        state = self.debate_phase(state, self.debate_time)

        # Update the current phase in the chat
        state.chat.current_phase = "Day Execution"
        state.current_phase = "Day Execution"

        state.chat.add_message_p2p(
            sender="Game Master",
            text=f"Your time to vote ! Decide who will be executed. Choose wisely...",
        )

        state, vote_result = self.voting_phase(state)

        if vote_result != None:
            state.chat.add_message_p2p(
                "Game Master", f"{vote_result} was brutally executed by the town..."
            )
            state.kill_player(vote_result)

        return state

    def voting_phase(self, state) -> Player:
        """
        Returns:
            _type_: _description_
        """
        votes = {player: 0 for player in state.alive_players}

        for current_player in state.alive_players:
            choices = [
                player for player in state.alive_players if player != current_player
            ]
            vote = current_player.vote(
                choices, state.get_summary(current_player)
            )  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1
            state.chat.add_message_p2p(
                "Game Master", f"{current_player} voted for {vote.name} !"
            )

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p(
            "Game Master",
            f"Sentenced player is {most_voted} with {votes[most_voted]} votes.",
        )
        state.chat.add_message_p2p(
            "Game Master",
            f"{most_voted}, you can share your last words with the town. Make it count !",
        )
        time.sleep(5)
        state.chat.add_message_p2p(most_voted, most_voted.last_words(state.get_summary(most_voted)))
        time.sleep(3)
        return state, most_voted

    def debate_phase(self, state, debate_time=50):
        """
        Execute the debate phase for a limited amount of time.
        Players can send messages within the time limit.
        """
        state.chat.add_message_p2p(
            sender="Game Master",
            text="Debate phase begins. You have limited time to discuss!",
        )

        # Start the timer.
        debate_end_time = time.time() + debate_time

        # Start the debate phase
        state = state.chat.discussion(
            state, debate_end_time=debate_end_time, players_active=state.alive_players
        )

        return state

    def __str__(self):
        return "Day"


class NightPhase:
    def __init__(self, werewold_meeting_time):
        self.werewold_meeting_time = werewold_meeting_time

    def execute(self, state):

        # Update the current phase in the chat
        state.chat.current_phase = "Night"
        state.current_phase = "Night"

        state.chat.add_message_p2p(
            "Game Master",
            "Night phase begins. Who will the werewolves kill tonight ?",
            color="red",
        )

        # Start discussion phase for werewolves if at least 2 are alive
        if len(state.get_alive_role("Werewolf")) >= 2:
            state = self.werewolf_debate(state, self.werewold_meeting_time)

        state, most_voted = self.werewolf_vote(state)

        if most_voted != None:
            state.chat.add_message_p2p(
                "Game Master",
                f"{most_voted} was brutally murdered in his sleep...",
                color="red",
            )
            state.kill_player(most_voted)

        return state

    def werewolf_debate(self, state: GameState, werewold_meeting_time=20):
        """
        Execute the werewolf debate phase for a limited amount of time.
        Players can send messages within the time limit.
        """

        # Update the current phase in the chat
        state.chat.current_phase = "Werewolf Meeting"
        state.current_phase = "Werewolf Meeting"

        state.chat.add_message_p2p(
            sender="Game Master",
            text="Werewolf meeting begins. You have limited time to discuss!",
        )

        # Start the timer. Werevolves should discuss for 20s.
        debate_end_time = time.time() + werewold_meeting_time

        # Start the discussion
        state = state.chat.discussion(
            state,
            players_active=state.get_alive_role("Werewolf"),
            debate_end_time=debate_end_time,
        )

        return state

    def werewolf_vote(self, state: GameState):

        state.chat.current_phase = "Werewolf Vote"
        state.current_phase = "Werewolf Vote"

        list_werewolves = state.get_alive_role("Werewolf")
        list_villagers = state.get_alive_role("Villager")

        state.chat.add_message_p2p(
            "Game Master",
            "Time to vote for the player you want to kill !",
            recipients=list_werewolves,
        )

        votes = {player: 0 for player in list_villagers}
        for current_player in list_werewolves:
            vote = current_player.vote(
                list_villagers, state.get_summary(current_player)
            )  # Players decide whom to vote for
            if vote in votes:
                votes[vote] += 1

        # Determine player with most votes
        most_voted = max(votes, key=votes.get)

        state.chat.add_message_p2p(
            "Game Master",
            f"You decided to kill {most_voted} with {votes[most_voted]} votes.",
            recipients=list_werewolves,
        )

        time.sleep(3)
        return state, most_voted

    def __str__(self):
        return "Night"
