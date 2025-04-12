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
    def test_first(self):

        self.google_page = GooglePage(self.driver)
        self.google_page.search_text("manish")
