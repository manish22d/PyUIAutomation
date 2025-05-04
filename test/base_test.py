from typing import Union
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.support.wait import WebDriverWait
from pages.google_page import GooglePage
import json
import inspect


class BaseTest:
	driver: Union[Chrome, Firefox, Edge]
	wait: WebDriverWait
	google_page: GooglePage
	
	@classmethod
	def load_test_data(cls,func_name):
		class_name = inspect.stack()[1].function
		path = f"resources/test_data/{class_name}/{func_name}.json"
		
		with open(path) as f:
			return [case for case in json.load(f) if case.get("enabled", True)]
