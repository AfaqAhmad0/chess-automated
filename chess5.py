import tkinter as tk
from tkinter import filedialog
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from stockfish import Stockfish

import json

# Load configuration file
with open("config.json", "r") as file:
    config = json.load(file)

side = input("b or w: ").strip().lower()

# castling_rights = "KQkq"

def setup_driver(debugger_address):

   
    driver_path = config["driver_path"]
    if driver_path:
        print(f"Selected Chromedriver: {driver_path}")
    else:
        print("No file selected.") 
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.attributes('-topmost', True)  # Bring the window to the front

        # Open file dialog to select the chromedriver
        driver_path = filedialog.askopenfilename(title="Select Chromedriver", 
                                                filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")],
                                                parent=root)

    """Setup Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

piece_map = {
    "wp": "P", "wn": "N", "wb": "B", "wr": "R", "wq": "Q", "wk": "K",
    "bp": "p", "bn": "n", "bb": "b", "br": "r", "bq": "q", "bk": "k"
}

def square_to_board(square):
    """Convert 'square-XY' to chess board notation."""
    files = "abcdefgh"
    ranks = "87654321"
    try:
        col, row = int(square[7]), int(square[8])
        return ranks[row - 1], files[col - 1]
    except (IndexError, ValueError):
        return None

def setup_stockfish():
    """Setup Stockfish engine."""
    stockfish = Stockfish("H:/Rough/chess/stockfish/stockfish-windows-x86-64.exe")
    stockfish.set_skill_level(config["skill_level"])
    stockfish.set_elo_rating(config["elo_rating"])
    return stockfish

def get_board_state(driver):
    """Extract chess board state from the webpage."""
    pieces = driver.find_elements(By.CLASS_NAME, "piece")
    board = [["" for _ in range(8)] for _ in range(8)]
    
    for piece in pieces:
        classes = piece.get_attribute("class").split()
        piece_type = next((cls for cls in classes if len(cls) == 2), None)
        square_class = next((cls for cls in classes if len(cls) == 9), None)
        
        position = square_to_board(square_class)
        if position:
            row, col = int(position[0]) - 1, ord(position[1]) - ord("a")
            board[row][col] = piece_map.get(piece_type, "?")
    # print(board)
    return board

def board_to_fen(board, castling_rights):
    """Convert board state to FEN string."""
    fen_rows = []
    for row in board:
        empty = 0
        fen_row = ""
        for cell in row:
            if cell:
                if empty > 0:
                    fen_row += str(empty)
                    empty = 0
                fen_row += cell
            else:
                empty += 1
        if empty > 0:
            fen_row += str(empty)
        fen_rows.append(fen_row)
    return f"{'/'.join(fen_rows)} {side} {castling_rights} - 0 1"

def get_board_from_fen(fen):
    """Convert FEN string to board representation."""
    rows = fen.split()[0].split("/")
    board = []
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend([""] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    return board

def update_fen(fen, move, castling_rights):
    """Update FEN based on the given move."""
    board = get_board_from_fen(fen)
    start_col, start_row = ord(move[0]) - ord("a"), 8 - int(move[1])
    end_col, end_row = ord(move[2]) - ord("a"), 8 - int(move[3])
    
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ""
    
    return board_to_fen(board, castling_rights)


def perform_move(driver, move):
    """Perform a move on the chess board via Selenium."""
    col_map = {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8"}
    click1 = f"square-{col_map[move[0]]}{move[1]}"
    click2 = f"square-{col_map[move[2]]}{move[3]}"
    
    # for click in [click1, click2]:
    while True:
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, click1)))
            ActionChains(driver).move_to_element(element).click().perform()
            time.sleep(0.5)
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, click2)))
            ActionChains(driver).move_to_element(element).click().perform()
            # print(f"Clicked: {click}")
            break
        except Exception as e:
            print(f"Retrying click: , Error: {e}")
            time.sleep(1)



def is_castling_available(board, castling_rights):
    """Check and update castling rights based on the board state."""
    
    # King and Rook positions for both sides
    positions = {
        "wK": (7, 4), "wRk": (7, 7), "wRq": (7, 0),  # White King, kingside Rook, queenside Rook
        "bK": (0, 4), "bRk": (0, 7), "bRq": (0, 0)   # Black King, kingside Rook, queenside Rook
    }
    
    # If no castling rights are present
    if castling_rights == "-":
        return "-"
    
    # Check if the King or Rooks have moved
    updated_castling_rights = castling_rights
    
    if 'K' in updated_castling_rights and board[positions["wK"][0]][positions["wK"][1]] != 'K':
        updated_castling_rights = updated_castling_rights.replace('K', '')
    if 'Q' in updated_castling_rights and board[positions["wRq"][0]][positions["wRq"][1]] != 'R':
        updated_castling_rights = updated_castling_rights.replace('Q', '')
    if 'k' in updated_castling_rights and board[positions["bK"][0]][positions["bK"][1]] != 'k':
        updated_castling_rights = updated_castling_rights.replace('k', '')
    if 'q' in updated_castling_rights and board[positions["bRq"][0]][positions["bRq"][1]] != 'r':
        updated_castling_rights = updated_castling_rights.replace('q', '')
    
    # If all castling rights are removed, return "-"
    return updated_castling_rights if updated_castling_rights else "-"

def are_fen_positions_equal(fen1, fen2):
    fields1 = fen1.split()[:4]
    fields2 = fen2.split()[:4]
    return fields1 == fields2

def turn(driver):
    move_lines =  driver.find_elements(By.CLASS_NAME, "main-line-row")
    total_moves = 0
    for move_line in move_lines:
        move_line_text = move_line.find_elements(By.CLASS_NAME, "node")
        total_moves += len(move_line_text)
    # print("Move Lines: ", (move_lines))
    if total_moves % 2 == 0:
        return "w"
    else:
        return "b"
    # exit(0)

def main(castling_rights, driver):
    """Main execution loop."""
    
    stockfish = setup_stockfish()
    prev_fen = ""
    
    while True:
        board = get_board_state(driver)

        # print("castling_rights: ",castling_rights)
        castling_rights = is_castling_available(board,castling_rights)
        # print("update_castling_rights: ",castling_rights)

        fen = board_to_fen(board, castling_rights)
        # print("FEN:", fen)
        turn_who =  turn(driver)
        
        if turn_who == side:
            stockfish.set_fen_position(fen)
            best_move = stockfish.get_best_move()
            print("Best Move:", best_move)
            print("FEN1:", fen)


            if best_move == None:
                print("_____________________________________")
            
            updated_fen = update_fen(fen, best_move, castling_rights)
            print("FEN2:", updated_fen)
            prev_fen = updated_fen
            
            perform_move(driver, best_move)
            time.sleep(1)

        else:
            print("Waiting for opponent's move...")
            time.sleep(1)

if __name__ == "__main__":
    castling_rights = "KQkq"
    
    # debugger_address = "localhost:"+input("Enter the debugger address: ")
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
            time.sleep(5)
