#-*- coding: utf-8 -*-
try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, OperatingSystem
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import random, time
    import os, sys, requests
    sys.path.append('library')
    from log_file import program_log
except:
    exit('[!] no required modules')

def extension(driver, x):
    driver.switch_to.window(driver.window_handles[0])
    data_server = driver.find_element_by_xpath('//*[@id="servers"]/span[' + str(x) + ']').click()
    time.sleep(7)
    driver.switch_to.window(driver.window_handles[-1])
    return driver

def my_driver():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)
    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()

    ext_dir = r'Z:\Pracownik35\Projekty_stale\Programy_pod_strony\new_allegro\library\extension1\extension1.zip'
    option = webdriver.ChromeOptions()
    option.add_extension(ext_dir)
    option.add_argument("--mute-audio")
    option.add_argument("--window-size=1400,1080")
    option.add_argument(user_agent[0])
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    except:
        program_log('[ERROR!][driver_captcha] Driver error!')
    return driver

def check_captcha(driver):

    def audioToText(mp3Path):
        driver.execute_script('''window.open("","_blank");''')
        #driver.switch_to.window(driver.window_handles[1])
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(googleIBMLink)

        # Upload file
        btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/input')))
        time.sleep(1)
        btn.send_keys(mp3Path)

        # Audio to text is processing
        time.sleep(audioToTextDelay)

        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
        result = " ".join( [ each.text for each in text ] )

        driver.close()
        #driver.switch_to.window(driver.window_handles[1])

        return result

    def saveFile(content,filename):
        with open(filename, "wb") as handle:
            for data in content.iter_content(chunk_size=1000000):
                handle.write(data)

    audioToTextDelay = 14
    filename = 'library/test.mp3'
    googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

    x = 0
    sound_enable = False
    try:
        while sound_enable == False and x < 3:
            if x > 0:
                driver.refresh()
            x = x + 1
            audioBtnFound = False
            try:
                time.sleep(1)
                driver.switch_to.default_content()
                iframe = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                driver.switch_to.frame(iframe)
                try:
                    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                except:
                    pass
                allegroClass = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip')))
                time.sleep(random.uniform(1, 4))
                allegroClass.click()
                allegroClass = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_voice')))
                time.sleep(random.uniform(2, 5))
                allegroClass.click()
                audioBtnFound = True
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'rc-doscaptcha-body-text')))
                    audioBtnFound = False
                except:
                    pass
                if audioBtnFound:
                    while True:
                        driver.switch_to.default_content()
                        iframe = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                        #time.sleep(random.uniform(2, 3))
                        driver.switch_to.frame(iframe)
                        href = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_music'))).get_attribute('src')
                        time.sleep(random.uniform(2, 4))
                        response = requests.get(href, stream=True)
                        saveFile(response,filename)
                        #time.sleep(random.uniform(2, 3))
                        response = audioToText(os.getcwd() + '/' + filename)
                        response = response.split(' ')[-1].replace('.', '')
                        print('Captcha: ' + response)

                        driver.switch_to.window(driver.window_handles[-1])
                        driver.switch_to.default_content()
                        iframe = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                        driver.switch_to.frame(iframe)
                        inputbtn = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_input')))
                        inputbtn.send_keys(response)
                        time.sleep(random.uniform(2, 5))
                        inputbtn.send_keys(Keys.ENTER)
                        driver.switch_to.default_content()
                        #time.sleep(random.uniform(3.5, 5))
                        try:
                            opened = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CLASS_NAME, 'main-wrapper')))
                            sound_enable = True
                            program_log('[INFO*][driver_captcha] Success')
                            break
                        except:
                            continue
            except:
                print('Error')
    except:
        pass
