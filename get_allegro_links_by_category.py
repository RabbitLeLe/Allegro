#-*- coding: utf-8 -*-
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time, random
    import sqlite3
    import sys, os
    sys.path.append('library')
    from parser_file import parser_data
    from my_database import create_database
    from log_file import program_log
    from driver_captcha import my_driver, check_captcha, extension
    from waiting import waiting
except:
    exit('[ERROR!][allegro] no required modules')

class main:

    ip_span = 4
    data_list = []
    driver = ''

    def __init__(self, path):
        length = len(path)
        for item in range(len(path)):
            value = (path[item]).split('/')
            path[item] = value

    def chrome(self):
        driver = my_driver()
        self.driver = extension(driver, self.ip_span)

    def check_if_blocked(self, driver):
        times = 0
        while True:
            try:
                iframe = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(iframe)
                if 'Zostałeś zablokowany.' in driver.find_element_by_xpath('//div[@class="captcha__human__title"]').text:
                    self.ip_span += 1
                    if self.ip_span > 8:
                        times += 1
                        self.ip_span = 4
                        waiting(7200, 'Zostałeś zablokowany. Czekam...')
                    driver = extension(driver, self.ip_span)
                    time.sleep(random.uniform(1, 3))
                    driver.refresh()
                    time.sleep(5)
                else:
                    driver.switch_to.default_content()
                    break
            except:
                driver.switch_to.default_content()
                break
        allegro.check_if_load_or_exist(driver)

    def check_if_load_or_exist(self, driver):
        try:
            while True:
                WebDriverWait(driver, 3).until(EC.element_to_be_located((By.XPATH,'//*[@id="main-frame-error"]')))
                driver.refresh()
        except:
            pass

        try:
            blocked_js = driver.find_element_by_xpath('//p[@id="cmsg"]')
            driver.refresh()
            time.sleep(random.uniform(1, 2))
        except:
            pass

        try:
            mess = driver.find_element_by_xpath('//button[@id="reload-button"]')
            if mess.text == 'Odśwież':
                #driver.refresh()
                mess.click()
                time.sleep(random.uniform(1, 2))
        except:
            pass

        try:
            details = driver.find_element_by_xpath('//button[@id="details-button"]')
            if details.text == 'Szczegóły':
                driver.refresh()
                time.sleep(random.uniform(1, 2))
        except:
            pass

    def if_captcha(self, driver):
        try:
            captcha = driver.find_element_by_tag_name('iframe').get_attribute('src')
        except:
            captcha = 'none'

        if 'captcha' in captcha:
            try:
                iframe = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(iframe)
                if 'Zostałeś zablokowany.' in driver.find_element_by_xpath('//div[@class="captcha__human__title"]').text:
                    allegro.check_if_blocked(driver)
                else:
                    driver.switch_to.default_content()
            except:
                pass
            check_captcha(driver)
            allegro.check_if_blocked(driver)

            try:
                captcha = driver.find_element_by_tag_name('iframe').get_attribute('src')
            except:
                captcha = 'none'
            if 'captcha' in captcha:
                check_captcha(driver)
            try:
                ac_click = WebDriverWait(driver, random.uniform(4, 6)).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-role="accept-consent"]')))
                ac_click.click()
            except:
                pass
        else:
            try:
                ac_click = WebDriverWait(driver, random.uniform(2, 4)).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-role="accept-consent"]')))
                ac_click.click()
            except:
                pass

    def get_category_map(self, path):

        driver = self.driver

        def filt_cont(driver):
            filters_Container = driver.find_element_by_xpath('//div[@data-role="filtersContainer"]')
            categories_container = filters_Container.find_element_by_xpath('//div[@data-role="Categories"]')
            filters_container = filters_Container.find_element_by_xpath('//div[@data-box-name="filters container"]')
            return categories_container, filters_container

        def _element(_element1, i_):
            link = []
            driver.execute_script("arguments[0];", driver.get(_element1))
            allegro.check_if_blocked(driver)
            allegro.if_captcha(driver)
            categories_container, filters_container = filt_cont(driver)
            li_ = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/section/div[2]/ul/li[' + str(i_) + ']/div/a')
            categories = categories_container.find_elements_by_xpath('//ul/li[@data-role="LinkItem"]/div/a')
            for _element2 in categories:
                link.append(str(_element2.get_attribute('href')))
            print(link)
            #driver.execute_script('''window.open("","_blank");''')
            #driver.switch_to.window(driver.window_handles[-1])
            return link

        def _element7():
            driver.execute_script("arguments[0];", driver.get(element11))
            allegro.check_if_blocked(driver)
            allegro.if_captcha(driver)
            categories_container, filters_container = filt_cont(driver)

        link1 = []
        link2 = []
        link3 = []
        link4 = []
        link = []

        category1 = path[0]
        url = 'https://allegro.pl/kategoria/' + category1
        try:
            category2 = path[1]
            is_category2 = True
        except:
            category2 = ' '
            is_category2 = False
        try:
            category3 = path[2]
            is_category3 = True
        except:
            category3 = ' '
            is_category3 = False
        try:
            category4 = path[3]
            is_category4 = True
        except:
            category4 = ' '
            is_category4 = False

        driver.execute_script("arguments[0];", driver.get(url))
        time.sleep(random.uniform(1, 3))
        allegro.check_if_blocked(driver)
        allegro.if_captcha(driver)

        try:
            categories_container, filters_container = filt_cont(driver)
            categories2 = categories_container.find_elements_by_xpath('//ul/li[@data-role="LinkItem"]/div/a')
            if is_category2:
                i_2 = 0
                for element2 in categories2:
                    i_2 += 1
                    dc2 = element2.text
                    print(dc2)
                    if dc2.lower().replace(' ','-') == category2:
                        time.sleep(1)
                        element2.click()
                        allegro.check_if_blocked(driver)
                        allegro.if_captcha(driver)
                        categories_container, filters_container = filt_cont(driver)
                        try:
                            li_ = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/section/div[2]/ul/li[' + str(i_2) + ']/div/a')
                            is_end = False
                        except:
                            is_end = True
                        if not is_end:
                            categories3 = categories_container.find_elements_by_xpath('//ul/li[@data-role="LinkItem"]/div/a')
                            if is_category3:
                                i_3 = 0
                                for element3 in categories3:
                                    i_3 += 1
                                    dc3 = element3.text
                                    print(dc3)
                                    if dc3.lower().replace(' ','-') == category3:
                                        time.sleep(1)
                                        element3.click()
                                        allegro.check_if_blocked(driver)
                                        allegro.if_captcha(driver)
                                        categories_container, filters_container = filt_cont(driver)
                                        try:
                                            li_ = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/section/div[2]/ul/li[' + str(i_3) + ']/div/a')
                                            is_end = False
                                        except:
                                            is_end = True
                                        if not is_end:
                                            categories4 = categories_container.find_elements_by_xpath('//ul/li[@data-role="LinkItem"]/div/a')
                                            if is_category4:
                                                i_4 = 0
                                                for element4 in categories4:
                                                    i_4 += 1
                                                    dc4 = element4.text
                                                    print(dc4)
                                                    if dc4.lower().replace(' ','-') == category4:
                                                        time.sleep(1)
                                                        element4.click()
                                                        allegro.check_if_blocked(driver)
                                                        allegro.if_captcha(driver)
                                                        categories_container, filters_container = filt_cont(driver)
                                                        try:
                                                            li_ = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/section/div[2]/ul/li[' + str(i_4) + ']/div/a')
                                                            is_end = False
                                                        except:
                                                            is_end = True
                                                        if not is_end:
                                                            categories4 = categories_container.find_elements_by_xpath('//ul/li[@data-role="LinkItem"]/div/a')
                                                            _element7()
                                                            allegro.get_data(driver)
                                                        else:
                                                            allegro.get_data(driver)
                                            else:
                                                for element4 in categories4:
                                                    link3.append(str(element4.get_attribute('href')))
                                                print(link3)
                                                #driver.execute_script('''window.open("","_blank");''')
                                                #driver.switch_to.window(driver.window_handles[-1])
                                                i_5 = 0
                                                for element5 in link3:
                                                    i_5 += 1
                                                    try:
                                                        link4 = _element(element5, i_5)
                                                        i_6 = 0
                                                        for element6 in link4:
                                                            i_6 += 1
                                                            try:
                                                                link5 = _element(element6, i_6)
                                                                i_7 = 0
                                                                for element7 in link5:
                                                                    i_7 += 1
                                                                    _element7()
                                                                    allegro.get_data(driver)
                                                            except:
                                                                allegro.get_data(driver)
                                                    except:
                                                        allegro.get_data(driver)
                                        else:
                                            allegro.get_data(driver)
                            else:
                                for element3 in categories3:
                                    link2.append(str(element3.get_attribute('href')))
                                print(link2)
                                #driver.execute_script('''window.open("","_blank");''')
                                #driver.switch_to.window(driver.window_handles[-1])
                                i_4 = 0
                                for element4 in link2:
                                    i_4 += 1
                                    try:
                                        link3 = _element(element4, i_4)
                                        i_5 = 0
                                        for element5 in link3:
                                            i_5 += 1
                                            try:
                                                link4 = _element(element5, i_5)
                                                i_6 = 0
                                                for element6 in link4:
                                                    i_6 += 1
                                                    try:
                                                        link4 = _element(element6, i_6)
                                                        i_7 = 0
                                                        for element7 in link5:
                                                            i_7 += 1
                                                            _element7()
                                                            allegro.get_data(driver)
                                                    except:
                                                        allegro.get_data(driver)
                                            except:
                                                allegro.get_data(driver)
                                    except:
                                        allegro.get_data(driver)
                        else:
                            allegro.get_data(driver)
            else:
                for element2 in categories2:
                    link1.append(str(element2.get_attribute('href')))
                print(link1)
                #driver.execute_script('''window.open("","_blank");''')
                #driver.switch_to.window(driver.window_handles[-1])
                i_3 = 0
                for element3 in link1:
                    i_3 += 1
                    try:
                        link2 = _element(element3, i_3)
                        i_4 = 0
                        for element4 in link2:
                            i_4 += 1
                            try:
                                link3 = _element(element4, i_4)
                                i_5 = 0
                                for element5 in link3:
                                    i_5 += 1
                                    try:
                                        link4 = _element(element5, i_5)
                                        i_6 = 0
                                        for element6 in link4:
                                            i_6 += 1
                                            try:
                                                link5 = _element(element6, i_6)
                                                i_7 = 0
                                                for element7 in link5:
                                                    i_7 += 1
                                                    _element7()
                                                    allegro.get_data(driver)
                                            except:
                                                allegro.get_data(driver)
                                    except:
                                        allegro.get_data(driver)
                            except:
                                allegro.get_data(driver)
                    except:
                        allegro.get_data(driver)
        except:
            pass

    def get_data(self, driver):
        if_next = True
        while if_next:
            try:
                opbox_listing = driver.find_element_by_xpath('//div[@class="opbox-listing"]')
                articles_href = opbox_listing.find_elements_by_xpath('//article[@data-role="offer"]/div/div[2]/div[1]/h2/a')
                self.data_list = []
                for article_href in articles_href:
                    href = ''
                    title = ''
                    stan = ''
                    wersja_gry = ''
                    price = ''
                    data = ''
                    ile_osob_kupilo = ''
                    print('--------------------------------------')
                    try:
                        title = article_href.text
                    except:
                        title = 'Error!!!'
                    print(title)
                    try:
                        href = article_href.get_attribute('href')
                        href = (str(href).split('redirect=')[-1]).replace('%3A',':').replace('%2F','/').replace('%3F','?').replace('%3D','=').replace('%26','&').replace('%253A',':')
                    except:
                        href = 'Error!!!'
                    print(href)
                    if 'bi_s=ads' not in href:
                        try:
                            cur.execute("""SELECT id FROM dane_allegro as da where da.adres_oferty like ? and da.tytul_ogloszenia like ?;""",(href,title))
                            check_if_exists = cur.fetchone()
                            if check_if_exists == None:
                                try:
                                    data = article_href.find_elements_by_xpath('../../div[@class="mpof_z0 m7er_k4"]/div/dl/dt')
                                    count = 0
                                    for param_title in data:
                                        count += 1
                                        if param_title.text == 'Stan':
                                            stan = param_title.find_element_by_xpath('../dd[' + str(count) + ']').text
                                        if param_title.text == 'Wersja gry':
                                            wersja_gry = param_title.find_element_by_xpath('../dd[' + str(count) + ']').text
                                        if stan != '' and wersja_gry!= '':
                                            break
                                    print(stan)
                                    print(wersja_gry)
                                    try:
                                        price = article_href.find_element_by_xpath('../../../div[@class="_9c44d_3AMmE"]/div').text
                                        print(price)
                                    except: pass
                                    try:
                                        ile_osob_kupilo = article_href.find_element_by_xpath('../../../div[@class="_9c44d_3K52C"]/div[@class="mpof_ki m389_6m munh_56_l"]').text
                                        print(ile_osob_kupilo)
                                    except: pass
                                    self.data_list.append(href + ',:*,' + title + ',:*,' + stan + ',:*,' + wersja_gry + ',:*,' + price + ',:*,' + ile_osob_kupilo)
                                except:
                                    self.data_list.append('error' + ',:*,' + ' ' + ',:*,' + ' ' + ',:*,' + ' ' + ',:*,' + ' ' + ',:*,' + ' ')
                            else:
                                pass
                        except:
                            pass
                allegro.update_db()
                try:
                    time.sleep(random.uniform(2, 5))
                    next_page = driver.find_element_by_xpath('//div[@data-role="paginationBottom"]//a[@rel="next"]')
                    next_page. click()
                    allegro.check_if_blocked(driver)
                    allegro.if_captcha(driver)
                    check = driver.find_element_by_xpath('//div[@data-role="itemsContainer"]/div[@data-role="loader"]').get_attribute('class')
                    x = 0
                    while check != 'mp7g_ca munh_56 m3h2_56 _e219d_peRCm mpof_5r':
                        check = driver.find_element_by_xpath('//div[@data-role="itemsContainer"]/div[@data-role="loader"]').get_attribute('class')
                        time.sleep(1)
                        x += 1
                        if x > 5:
                            driver.refresh()
                            allegro.check_if_blocked(driver)
                            allegro.if_captcha(driver)
                            break
                    if_next = True
                    time.sleep(random.uniform(2, 5))
                except:
                    if_next = False
            except:
                pass

    def update_db(self):
        while os.path.isfile('_allegro.db-journal'):
            waiting(60, 'Czekam na zwolnienie pliku bazy danych...')
        for data in self.data_list:
            data = data.replace('\n','; ').split(',:*,')
            cur.execute('INSERT INTO dane_allegro (id, adres_oferty, tytul_ogloszenia, stan, wersja, cena, ile_osob_kupilo) VALUES (NULL,?,?,?,?,?,?);', (data[0], data[1], data[2], data[3], data[4], data[5]))
        con.commit()

licznik, path = parser_data()
con, cur = create_database()
allegro = main(path)
allegro.chrome()

for item in range(len(path)):
    single_path = path[item]
    con, cur = create_database()
    allegro.get_category_map(single_path)
    con.close()
