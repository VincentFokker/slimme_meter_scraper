"""Main file."""
import os
import time
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, date, timedelta
from src.slimmemeterdata.comodities import Comodities
from enum import Enum
import platform

load_dotenv(find_dotenv())


class SlimmeMeterLezer:
    """Reads data from the slimme meter portal."""

    def __init__(self) -> None:
        self.base_url = "https://slimmemeterportal.nl"
        self.contract_id = "954400288"
        self.timeslot_start = str(
            int(datetime.timestamp(datetime.fromordinal((date.today() + timedelta(-1)).toordinal()))))
        self.time_range = str(int(60 * 60 * 24))  # 86400

    def run(self) -> str:
        """Main function"""
        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument("window-size=1920x1080")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        if platform.system() == 'Windows':
            browser = webdriver.Chrome(options=options)
        elif platform.system() == 'Linux':
            print("Starting virtual display..")
            from pyvirtualdisplay import Display
            display = Display(visible=False, size=(800, 600))
            display.start()
            prefs = {"download.default_directory": "/home/homeassistant/"}
            options.add_experimental_option('prefs', prefs)
            browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        else:
            raise NotImplementedError

        # Login
        self._login(browser_session=browser)

        # Do a download of energy data
        self._download_data(browser_session=browser, comodity=Comodities.ENERGY)

        # Do a download of gas data
        self._download_data(browser_session=browser, comodity=Comodities.GAS)

        return "Downloaded file"

    def _download_data(self, browser_session: webdriver.Chrome, comodity: Enum) -> None:
        """Download the kw data."""
        print(f"Downloading data for the {comodity.value} comodity.")
        browser_session.get(
            f'{self.base_url}/cust/consumption/chart.xls?commodity={comodity.value}&contract_id={self.contract_id}'
            f'&contracts%5B%5D={self.contract_id}&datatype=consumption&range={self.time_range}&timeslot_start={self.timeslot_start}')
        time.sleep(1)

    def _login(self, browser_session: webdriver.Chrome) -> None:
        """Main function."""
        print("Logging into browser..")
        browser_session.get("https://slimmemeterportal.nl/login")

        # find login fields
        login_user = browser_session.find_element(value='user_session_email')
        login_password = browser_session.find_element(value='user_session_password')

        # send login credentials
        # Get credentials from environment
        login_user.send_keys(os.environ.get("USER"))
        login_password.send_keys(os.environ.get("PASSWORD"))

        # Login
        browser_session.find_element(by=By.NAME, value='commit').click()
        time.sleep(1)
