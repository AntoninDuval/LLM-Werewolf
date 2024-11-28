from game.game_engine import GameEngine

if __name__ == "__main__":
    
    engine = GameEngine(n_players=5, n_werewolfs=1)
    engine.run()