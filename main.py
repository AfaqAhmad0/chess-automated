import time
from castling import is_castling_available
from conversions import board_to_fen, get_board_state
from driver import setup_driver,config
from clicks import perform_move
from model import setup_stockfish
from turn import turn
from gameover import game_over

side = input("b or w: ").strip().lower()
if side not in ["b", "w"]:
    print("Invalid side. Exiting...")
    exit(1)


def main(castling_rights, driver):
    """Main execution loop."""
    
    stockfish = setup_stockfish()    
    while True:
        board = get_board_state(driver)
        castling_rights = is_castling_available(board,castling_rights)
        fen = board_to_fen(board, castling_rights, side)
        turn_who =  turn(driver)
        print("Turn:", turn_who, "Side:", side)

        if game_over():
            exit(0)
        
        if turn_who == side:            
            stockfish.set_fen_position(fen)
            best_move = stockfish.get_best_move()
            print("Best Move:", best_move)
            print("FEN1:", fen)
            if best_move == None:
                print("_____________________________________")
                exit(0)
            
            perform_move(driver, best_move)
            time.sleep(1)

        else:
            print("Waiting for opponent's move...")
            time.sleep(1)

if __name__ == "__main__":
    castling_rights = "KQkq"    
    debugger_address = config["debugger_address"]
    if debugger_address:
        print(f"Selected debugger address: {debugger_address}")
    else:
        print("No debugger address selected.")
        debugger_address = input("Enter the debugger address: ")

    driver = setup_driver(debugger_address)
    while True:
        try:
            main(castling_rights,driver)
        except Exception as e:
            print("Critical Error, restarting...", e)
            time.sleep(2)
