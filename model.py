from stockfish import Stockfish
from driver import config
def setup_stockfish():
    """Setup Stockfish engine."""
    stockfish = Stockfish("H:/Rough/chess/stockfish/stockfish-windows-x86-64.exe")
    stockfish.set_skill_level(config["skill_level"])
    stockfish.set_elo_rating(config["elo_rating"])
    return stockfish