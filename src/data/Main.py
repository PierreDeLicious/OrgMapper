import time
import logging
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from random import randint

from src.data.Fetcher_LinkedIn_login import login_LinkedIn
from src.data.Fetcher_Orgs import get_orgs_details


def main():

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='../../data/logs/' + date.today().strftime('%Y-%m-%d') + '-debug.log', filemode='w',
                        level=logging.DEBUG)
    logging.info('OrgMapper3 process started')

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-data-dir=C:/Users/pdele/IdeaProjects/OrgMapper3/selenium-user-data")
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('http://www.linkedin.com/')
    time.sleep(randint(3, 6))

    login_LinkedIn(driver)
    # get_orgs_details(driver, 'Aion Bank')
    # get_orgs_details(driver, 'UBS')
    # get_orgs_details(driver, 'SIX, Danske Bank, Metrosoft')
    get_orgs_details(driver)

    driver.quit()
    logging.info('OrgMapper3 process finished')


if __name__ == '__main__':
    main()
