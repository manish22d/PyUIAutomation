import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
INI_CONFIGS_PATH = os.path.join(ROOT_DIR, "config")
DATA_FILES_PATH = os.path.join(ROOT_DIR, "data")
HTML_REPORT_PATH = os.path.join(ROOT_DIR, "reports")

if not os.path.exists(HTML_REPORT_PATH):
    os.mkdir(HTML_REPORT_PATH)
