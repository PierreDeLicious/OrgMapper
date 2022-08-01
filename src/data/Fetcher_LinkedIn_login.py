import time
import logging

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint

from src.data.Fetcher_Orgs import get_orgs_details
from src.tools import dot_env_loader


def login_LinkedIn(driver):
    login_button = driver.find_elements_by_class_name('nav__button-secondary')

    if len(login_button) > 0:
        # start if there was no login prior
        # LinkedIn can be sending a text message to authenticate the user/device
        login_button.click()
        time.sleep(randint(3, 6))
        driver.find_element_by_id('username').send_keys(dot_env_loader.lkd_user)
        time.sleep(randint(1, 3))
        driver.find_element_by_id('password').send_keys(dot_env_loader.lkd_pwd)
        time.sleep(randint(1, 3))
        driver.find_element_by_class_name('login__form_action_container').click()
        time.sleep(randint(323, 426))
        logging.info('The user was not logged in, but is now.')




