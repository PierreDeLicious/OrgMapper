import time
from selenium import webdriver

from src.data.dot_env_loader import lkd_user

print(lkd_user)

driver = webdriver.Chrome('C:\dev\chromedriver\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()