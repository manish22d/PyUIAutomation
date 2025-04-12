import logging
import os

import pytest
import pytest_html
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from utils.config_parser import ConfigParserIni

os.environ['SE_CACHE_PATH'] = './driver'
os.makedirs("screenshots", exist_ok=True)


# reads parameters from pytest command line
def pytest_addoption(parser):
	parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")


def pytest_html_report_title(report):
	report.title = "UI Python Automation !!"


def pytest_sessionstart() -> None:
	"""Loading sensitive data from environment variables.
        and setting selenium logging
    """
	logging.basicConfig(level=logging.WARN)
	logger = logging.getLogger("selenium")
	
	logger.setLevel(logging.INFO)


@fixture(scope="session")
# instantiates ini file parses object
def prep_properties():
	config_reader = ConfigParserIni("props.ini")
	return config_reader


@fixture(scope="session")
def browser(request):
	logger = logging.getLogger("selenium")
	logger.info("launching browser -> '%s", request.config.getoption("--browser"))
	return request.config.getoption("--browser")


@fixture(autouse=True)
def one_time_setup(prep_properties, request, browser):
	logger = logging.getLogger("selenium")
	base_url = prep_properties.config_section_dict("Base Url")["base_url"]
	logger.info("navigating to url -> '%s'", base_url)
	logger.info("Running one time setup")
	if browser in ("chrome", "chrome_headless"):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.set_capability(
			"goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
		)
		chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		chrome_options.add_experimental_option(
			"prefs",
			{
				"profile.default_content_setting_values.notifications": 2,
				"profile.default_content_setting_values.media_stream_mic": 1,
				"profile.default_content_setting_values.geolocation": 1,
				"profile.default_content_setting_values.media_stream_camera": 1,
				"credentials_enable_service": False,
				"profile.password_manager_enabled": False,
			},
		)
		chrome_options.add_argument("disable-dev-shm-usage")
		chrome_options.add_argument("no-sandbox")
		chrome_options.add_argument("allow-file-access-from-files")
		chrome_options.add_argument("use-fake-device-for-media-stream")
		chrome_options.add_argument("use-fake-ui-for-media-stream")
		chrome_options.add_argument("hide-scrollbars")
		chrome_options.add_argument("user-agent=automation")
		chrome_options.add_argument("disable-features=VizDisplayCompositor")
		chrome_options.add_argument("disable-features=IsolateOrigins,site-per-process")
		chrome_options.add_argument("disable-popup-blocking")
		chrome_options.add_argument("disable-dev-shm-usage")
		chrome_options.add_argument("disable-notifications")
		
		driver = webdriver.Chrome(options=chrome_options)
	else:
		driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
	
	if request.cls is not None:
		request.cls.driver = driver
	driver.get(base_url)
	driver.maximize_window()
	yield driver
	logger.info("Running one time tearDown")
	logger.info("Closing browser......")
	driver.quit()


# Hook to attach screenshots to HTML report on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
	# Execute all other hooks to obtain the report object
	outcome = yield
	rep = outcome.get_result()
	
	# Only act on test failure
	if rep.when == "call" and rep.failed:
		driver = item.funcargs.get("driver")  # get the driver fixture
		if driver:
			# Ensure the screenshot folder exists
			screenshot_folder = "screenshots"
			os.makedirs(screenshot_folder, exist_ok=True)
			
			# Save the screenshot
			screenshot_path = f"{screenshot_folder}/{item.name}.png"
			driver.save_screenshot(screenshot_path)
			
			# Attach the screenshot to the HTML report
			if hasattr(item.config, "_html"):
				extra = getattr(rep, "extra", [])
				extra.append(pytest_html.extras.image(screenshot_path))
				rep.extra = extra