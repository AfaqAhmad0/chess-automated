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
