from game.game_state import GameState
from game.phases import DayPhase, NightPhase
from player.ai_player import RandomAIPlayer
from player.llm_player import LLMPlayer
from llm.llm_handler import LangChainHandler
from termcolor import cprint
from player.human_player import HumanPlayer
from random import shuffle
import time
import json
import random
from dotenv import load_dotenv
import os

load_dotenv()
# Access the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")


class GameEngine:
    def __init__(
        self,
        n_players,
        n_werewolfs,
        n_ai,
        debate_time,
        werewold_meeting_time,
        llm_model="gpt-4o",
    ):

        self.title_screen()
        self.state = GameState()

        self.day_phase = DayPhase(debate_time=debate_time)
        self.night_phase = NightPhase(werewold_meeting_time=werewold_meeting_time)

        self.n_players = n_players
        self.n_werewolfs = n_werewolfs
        self.n_ai = n_ai
        self.llm_model = llm_model

        with open("./src/game/roles.json") as file:
            self.roles_txt = json.load(file)

        # Load the personalities of the LLM AI players
        with open("./src/extras/personality_traits.json") as file:
            self.personalities = json.load(file)

        self.setup_game()

    def title_screen(self):
        time.sleep(1.5)
        with open("./src/extras/title_screen.txt", "r") as file:
            for line in file:
                cprint(line, "red")
        time.sleep(2)

        # Ask player to press Enter to start the game, and delete the line afterwards
        input("Press Enter to start the game...")
        print(chr(27) + "[2J")  # Clear the screen

    def run(self):

        while not self.state.game_over:
            print("=" * 70)

            self.state.increment_day()

            self.state = self.day_phase.execute(self.state)

            self.state.check_victory()

            if self.state.game_over:
                break

            print("=" * 70)

            cprint("Night is comming", "red")

            self.state = self.night_phase.execute(self.state)
            self.state.check_victory()
            time.sleep(5)

        print("Game Over. Winner:", self.state.winner)

    def setup_game(self):
        roles = ["Werewolf"] * self.n_werewolfs + ["Villager"] * (
            self.n_players - self.n_werewolfs
        )
        type_players = ["Human"] * (self.n_players - self.n_ai) + ["AI"] * self.n_ai
        shuffle(roles)
        shuffle(type_players)
        for name, role, type_player in zip(
            ["Player" + str(i) for i in range(self.n_players)], roles, type_players
        ):

            if type_player == "Human":
                player = HumanPlayer(
                    name=name, role=role
                )  # Use HumanPlayer for real players
                self.state.add_player(player)
                cprint(
                    self.roles_txt[role]["introduction_msg"],
                    self.roles_txt[role]["introduction_msg_color"],
                )

            elif type_player == "AI":
                # Pick a random personality of the dict and remove it
                personality = self.personalities.pop(
                    random.choice(list(self.personalities.keys()))
                )
                player = LLMPlayer(
                    name=name,
                    role=role,
                    llm_handler=LangChainHandler(
                        model=self.llm_model, api_key=openai_api_key
                    ),
                    strategy=self.roles_txt[role]["strategy"],
                    personality=personality[role],
                )
                self.state.add_player(player)

        time.sleep(3)
        # Notice the werewolves who are their allies
        werewolves = self.state.get_alive_role("Werewolf")
        
        for werewolf in werewolves:
            allies =  [player.name for player in werewolves if player != werewolf]
            werewolf.update_allies(allies)
            self.state.chat.add_message_p2p(
            "Game Master",
            "Werewolf, you are allied with "
            + str(allies),
            recipients=[werewolf],
            )
            
        time.sleep(1)
