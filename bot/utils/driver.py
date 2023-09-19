import shutup
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

shutup.please()


def get_driver():
    chrome_options = Options()
    if platform.system() == "Linux":
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,2100")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    return driver
