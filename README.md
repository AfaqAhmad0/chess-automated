# chess-automated
 automate the chess.com with stockfish

# Chess Bot using Selenium and Stockfish

## Overview
This project is a Chess bot that plays on an online chess platform using Selenium for web automation and Stockfish for AI-based move generation. The bot extracts the board state from the webpage, generates the best possible move using Stockfish, and performs the move automatically.

## Features
- Uses Selenium to interact with an online chess board.
- Extracts real-time board state.
- Converts board state to FEN notation.
- Uses Stockfish to determine the best move.
- Automates move execution on the webpage.
- Tracks castling rights and updates FEN accordingly.

## Requirements
- Python 3.x
- Google Chrome (with remote debugging enabled)
- ChromeDriver (matching your Chrome version)
- Selenium
- Stockfish

## Installation
1. **Install Dependencies:**
   ```sh
   pip install selenium stockfish
   ```
2. **Download ChromeDriver:**
   - Ensure you have Chrome installed.
   - Download the matching [ChromeDriver](https://sites.google.com/chromium.org/driver/) version.
   - Place the `chromedriver.exe` in the correct path and update the script accordingly.

3. **Download Stockfish:**
   - Download [Stockfish](https://stockfishchess.org/download/).
   - Extract and update the script with the correct Stockfish executable path.

4. **Enable Chrome Debugging:**
   Run Chrome with debugging enabled:
   ```sh
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\[YOURUSERNAME]\AppData\Local\Google\Chrome\User Data"
   ```

## Usage
1. **Run the script:**
   ```sh
   python chess.py
   ```
2. **Choose a side:**
   The script will prompt:
   ```
   b or w:
   ```
   Enter `b` for Black or `w` for White.

3. **Bot will play automatically:**
   - It reads the board state.
   - Determines the best move using Stockfish.
   - Performs the move using Selenium.

## Configuration
- **Stockfish Strength:** Adjust in `setup_stockfish()`:
  ```python
  stockfish.set_skill_level(19)
  stockfish.set_elo_rating(3000)
  ```
- **ChromeDriver Path:** Update in `setup_driver()`:
  ```python
  service = Service("H:/Rough/chess/chromedriver-win64/chromedriver.exe")
  ```
- **Stockfish Path:** Update in `setup_stockfish()`:
  ```python
  stockfish = Stockfish("H:/Rough/chess/stockfish/stockfish-windows-x86-64.exe")
  ```

## Troubleshooting
- **Bot Not Moving:**
  - Ensure Chrome is running with debugging enabled.
  - Check if `chromedriver.exe` is in the correct location.
  - Verify Stockfish is correctly installed and working.
- **Errors in Clicking Moves:**
  - The bot may misidentify board positions. Try adjusting delays or debugging `get_board_state()`.
- **Game Not Starting:**
  - Ensure the chess website is open before running the script.

## License
This project is for educational purposes and does not promote unfair play. Use responsibly.

## Acknowledgments
- [Selenium](https://www.selenium.dev/)
- [Stockfish](https://stockfishchess.org/)

## TO DO:
+ Check for game end
+ deal with Promotion
- Restructure the code
- add Randomness
- can use for dataset creation
- miss click error bug

