import tkinter as tk
from tkinter import filedialog
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from selenium import webdriver

# Load configuration file
with open("config.json", "r") as file:
    config = json.load(file)

def select_driver():
    """Select the chromedriver executable file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring the window to the front
    driver_path = filedialog.askopenfilename(title="Select Chromedriver", 
                                            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")],
                                            parent=root)
    return driver_path

def setup_driver(debugger_address):
    """Setup the Selenium WebDriver."""
    driver_path = config["driver_path"]
    if driver_path:
        print(f"Selected Chromedriver: {driver_path}")
    else:
        driver_path = select_driver()
    if not driver_path or not os.path.isfile(driver_path):
        driver_path = select_driver()

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(driver_path)
    config["driver_path"] = driver_path
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    return webdriver.Chrome(service=service, options=chrome_options)
