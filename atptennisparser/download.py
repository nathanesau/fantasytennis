import platform
from selenium import webdriver
import time
from config import Config

def download_html_file(url, filename):
    """
    cloudflare workaround - mimic actual web browser user
    otherwise, website will block download of html file

    config variables:
    CHROMEDRIVER_PATH
    DOWNLOAD_DIR
    HEADERS

    example:
    download_html_file("https://www.atptour.com/en/scores/current/roland-garros/520/draws", "out.html")
    """
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": Config.DATA_FOLDER, "directory_upgrade": True,
        "safebrowsing.enabled": True }
    chrome_options.add_experimental_option("prefs", preferences)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_options,
        executable_path=Config.CHROMEDRIVER_PATH)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', Config.HEADERS)
    driver.get(url)
    content = driver.page_source
    utf8_content = content.encode('utf-8')
    content_str = str(utf8_content)
    html_file = open(filename, 'w')
    html_file.write(content_str)
    html_file.close()

