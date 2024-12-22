from game.game_state import GameState
from game.phases import DayPhase, NightPhase
from player.ai_player import RandomAIPlayer
from termcolor import cprint
from player.human_player import HumanPlayer
from random import shuffle
import time
import json

class GameEngine:
    def __init__(self, n_players, n_werewolfs, n_ai):

        self.title_screen()
        self.state = GameState()

        self.day_phase = DayPhase()
        self.night_phase = NightPhase()

        self.n_players = n_players
        self.n_werewolfs = n_werewolfs
        self.n_ai = n_ai
        
        with open("./src/game/roles.json") as file:
            self.roles_txt = json.load(file)

        self.setup_game()

    def title_screen(self):
        time.sleep(1.5)
        with open('./src/extras/title_screen.txt', 'r') as file:
            for line in file:
                cprint(line, "red")
        time.sleep(2)

    def run(self):

        while not self.state.game_over:
            print('='*70)

            self.state.day += 1
            self.state.chat.day = self.state.day # Track the current day to print in the chat
            
            self.state = self.day_phase.execute(self.state)

            self.state.check_victory()

            print('='*70)

            cprint('Night is comming', 'red')

            self.state = self.night_phase.execute(self.state)
            self.state.check_victory()
            #print(self.state.get_summary())
            time.sleep(5)

        print("Game Over. Winner:", self.state.winner)
    

    def setup_game(self):
        roles = ["Werewolf"] * self.n_werewolfs + ["Villager"] * (self.n_players - self.n_werewolfs)
        type_players = ["Human"] * (self.n_players-self.n_ai) + ["AI"] * self.n_ai
        shuffle(roles)
        shuffle(type_players)
        for name, role, type_player in zip(["Player" + str(i) for i in range(self.n_players)], roles, type_players):

            if type_player == 'Human':
                player = HumanPlayer(name=name, role=role)  # Use HumanPlayer for real players
                self.state.add_player(player)
                cprint(self.roles_txt[role]["introduction_msg"], 
                    self.roles_txt[role]["introduction_msg_color"])
            elif type_player == 'AI':
                player = RandomAIPlayer(name=name, role=role)
                self.state.add_player(player)

            