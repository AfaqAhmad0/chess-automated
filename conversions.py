from selenium.webdriver.common.by import By

def square_to_board(square):
    """Convert 'square-XY' to chess board notation."""
    files = "abcdefgh"
    ranks = "87654321"
    try:
        col, row = int(square[7]), int(square[8])
        return ranks[row - 1], files[col - 1]
    except (IndexError, ValueError):
        return None
    

def get_board_state(driver):
    piece_map = {
    "wp": "P", "wn": "N", "wb": "B", "wr": "R", "wq": "Q", "wk": "K",
    "bp": "p", "bn": "n", "bb": "b", "br": "r", "bq": "q", "bk": "k"
}
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


def board_to_fen(board, castling_rights, side):
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
