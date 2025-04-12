from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from pages.base_page import BasePage
from typing import Tuple


class RandomPage(BasePage):
	"""google page - The first page that appears when navigating to base URL"""
	SEARCH_BOX: Tuple[str, str] = (By.NAME, "q")
	
	def __init__(self, driver):
		super().__init__(driver)
	
	def login(self):
		self.click(self.SEARCH_BOX)
		
