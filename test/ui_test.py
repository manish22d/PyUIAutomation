from pages import google_page
from test.base_test import BaseTest
import pytest
import unittest
from pages.google_page import GooglePage


class TestUI(BaseTest):
    @classmethod
    def setUpClass(cls):
        print("hello")

    @classmethod
    def tearDownClass(cls):
        print("teardown")

    @pytest.mark.testui
    @pytest.mark.parametrize("case", BaseTest.load_test_data("test_first"))
    def test_first(self,case):
        print(case)
        print(case["data"])
        # self.google_page = GooglePage(self.driver)
        # self.google_page.search_text("manish")

    @pytest.mark.testB
    def test_second(self):
        self.google_page = GooglePage(self.driver)
        self.google_page.search_text("Indira")
