from typing import Tuple

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class GooglePage(BasePage):
    """google page - The first page that appears when navigating to base URL"""
    SEARCH_BOX: Tuple[str, str] = (By.NAME, "q")

    def __init__(self, driver):
        super().__init__(driver)

    def search_text(self, txt) -> None:
        self.fill_text(self.SEARCH_BOX, txt,Keys.ENTER)
        time.sleep(10)
