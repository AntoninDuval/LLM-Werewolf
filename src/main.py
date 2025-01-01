from game.game_engine import GameEngine

if __name__ == "__main__":
    engine = GameEngine(n_players=6, n_werewolfs=2, n_ai=5)
    engine.run()