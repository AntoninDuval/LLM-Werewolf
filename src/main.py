from game.game_engine import GameEngine

if __name__ == "__main__":
    engine = GameEngine(
        n_players=7,
        n_werewolfs=2,
        n_ai=6,
        debate_time=100,
        werewold_meeting_time=30,
        llm_model="gpt-4o",
    )
    engine.run()