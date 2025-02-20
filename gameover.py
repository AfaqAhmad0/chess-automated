from selenium.webdriver.common.by import By
def gameover(driver):
    game_over = driver.find_elements(By.CLASS_NAME, "game-result")
    if len(game_over) > 0:
        game_over = game_over[0]
        print("Game Over:", game_over.text)
        print("_____________________________________")
        return True
    return False