from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
def perform_move(driver, move, side="w"):
    """Perform a move on the chessboard via Selenium."""
    
    col_map = {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8"}
    click1 = f"square-{col_map[move[0]]}{move[1]}"
    click2 = f"square-{col_map[move[2]]}{move[3]}"
    click3 = None

    if len(move) == 5:  # Pawn promotion
        click3 = f"promotion-piece.{side}{move[4]}"
        print(f"Promotion: {click3}")

    try:
        # Click the starting square
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, click1)))
        ActionChains(driver).move_to_element(element).click().perform()
        print(f"Clicked1: {click1}")
        time.sleep(0.5)

        # Click the destination square
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, click2)))
        ActionChains(driver).move_to_element(element).click().perform()
        print(f"Clicked2: {click2}")
        time.sleep(1)

        # If it's a promotion, select the promoted piece
        if click3:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, click3)))

            print(f"element: {element}")
            ActionChains(driver).move_to_element(element).click().perform()
            print(f"Clicked3: {click3}")
            time.sleep(0.5)

    except Exception as e:
        print(f"Error in move {move}: {e}")
