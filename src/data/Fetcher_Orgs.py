import logging
import json
import time
import pandas as pd
from random import randint
from selenium.webdriver.common.keys import Keys
from datetime import date


def get_orgs_details(driver, target_org=''):
    with open('../../data/static/orgs.json') as f:
        orgs = json.load(f)

    if target_org != '':
        t_orgs = target_org.split(',')
        target_orgs = list()
        for org in orgs:
            for t_org in t_orgs:
                if org['name'] == t_org:
                    target_orgs.append(org)
    else:
        target_orgs = orgs
        logging.info('All orgs in the config file will be considered')

    for org in target_orgs:
        org_name = org['name']

        all_employees_ifo = dict()
        all_employees_ifo[org_name] = dict()
        all_employees_ifo[org_name]['globally'] = 0

        for ticker in org['tickers']:
            logging.info('get_orgs_details: ' + org_name + ' - ' + ticker)
            try:
                driver.get('https://www.linkedin.com/company/' + ticker + '/people/')
                time.sleep(randint(3, 6))
                temp_nb_employees = int(find_nb_employees('', driver))
                all_employees_ifo[org_name]['globally-employees'] = temp_nb_employees
                # The call to find_nb_employees_per_category needs to be after the call find_nb_employees
                # for a given location to load the right page.
                if temp_nb_employees > 0:
                    all_employees_ifo[org_name]['globally-categories'] = find_nb_employees_per_category(driver)

                if temp_nb_employees > 0:
                    with open('../../data/static/cities.json') as file_cities_and_country:
                        cities_and_country = json.load(file_cities_and_country)
                    for country in cities_and_country:
                        for country_key in country:
                            logging.info('get_orgs_details: ' + org_name + ' - ' + ticker + ' ' + country_key)
                            temp_nb_employees = int(find_nb_employees(country_key, driver))
                            all_employees_ifo[org_name][country_key + '-employees'] = temp_nb_employees
                            if temp_nb_employees > 0:
                                all_employees_ifo[org_name][
                                    country_key + '-categories'] = find_nb_employees_per_category(
                                    driver)
                            if temp_nb_employees > 0:
                                for city in country[country_key]:
                                    temp_nb_employees = int(find_nb_employees(city['name'], driver))
                                    all_employees_ifo[org_name][city['name'] + '-employees'] = temp_nb_employees
                                    if temp_nb_employees > 0:
                                        all_employees_ifo[org_name][
                                            city['name'] + '-categories'] = find_nb_employees_per_category(driver)
                                        logging.info(
                                            'get_orgs_details for ' + city['name'] + ' is: ' + str(
                                                all_employees_ifo[org_name][
                                                    city['name'] + '-employees']))
            except Exception as err:
                logging.exception('Process exited prematurely. ' + err.with_traceback())

        df = pd.DataFrame.from_dict(all_employees_ifo)
        path = '../../data/raw/' + date.today().strftime('%Y-%m-%d') + '_' + org['tickers'][0] + '_orgs_employees.csv'
        df.to_csv(path)


def find_nb_employees(location, driver):
    search_filters = driver.find_elements_by_xpath('//button[contains(@class , \'artdeco-pill\')]')

    if len(search_filters) > 0:
        for search_filter in search_filters:
            time.sleep(randint(1, 1))
            search_filter.click()
    if len(location) == 0:
        nb_total_employees = driver.find_elements_by_xpath('//div[@class=\'artdeco-card pb2\']/div[1]')
    else:
        search_element = driver.find_element_by_xpath(
            '//input[contains(@placeholder,\'Search employees by title\')]')
        search_element.send_keys(location)
        time.sleep(randint(1, 1))
        search_element.send_keys(Keys.ENTER)
        time.sleep(randint(3, 6))
        nb_total_employees = driver.find_elements_by_xpath('//div[@class=\'artdeco-card pb2\']/div[1]')

    if len(nb_total_employees) > 0:
        for i_element in nb_total_employees:
            if ' employee' in i_element.text:
                nb_total_employees = ''.join([i for i in i_element.text if i.isdigit()])
    else:
        nb_total_employees = 0

    return nb_total_employees


def find_nb_employees_per_category(driver):
    nb_employees_per_activity = dict()
    driver.find_element_by_xpath('//button[contains(@class , \'artdeco-pagination__button--next\')]').click()
    time.sleep(randint(1, 3))
    if driver.find_element_by_xpath(
            '//button[contains(@class,\'show-more-button\')]').get_attribute('aria-expanded') == 'false':
        driver.find_element_by_xpath(
            '//button[contains(@class,\'show-more-button\')]').click()
        time.sleep(randint(1, 3))
    temp_webelements_categories = driver.find_elements_by_xpath(
        '//span[contains(@class,\'org-people-bar-graph-element__category\')]')

    for temp_webelements_category in temp_webelements_categories:
        if len(temp_webelements_category.text) > 0:
            category = temp_webelements_category.text
            category_number = temp_webelements_category.find_element_by_xpath('./../strong').text
            if category_number != '':
                nb_employees_per_activity[category] = category_number

    return nb_employees_per_activity
