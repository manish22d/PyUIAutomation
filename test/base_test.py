from typing import Union
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.support.wait import WebDriverWait
from pages.google_page import GooglePage


class BaseTest:
    driver: Union[Chrome, Firefox, Edge]
    wait: WebDriverWait
    google_page: GooglePage
