from selenium.webdriver.common.by import By
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
