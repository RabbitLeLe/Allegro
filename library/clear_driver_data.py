from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def delete_cache(driver):
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/clearBrowserData')
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 2 + Keys.DOWN * 2)
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)
    actions.perform()
    time.sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return driver