#-*- coding: utf-8 -*-
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from tqdm import tqdm
    import requests, os
    import sys
    import sqlite3
    import time, random
    sys.path.append('library')
    from driver_captcha import my_driver, check_captcha, extension
    from my_database import create_database
    from log_file import program_log
    from parser_file import config_parser, modification_parser
    from waiting import waiting
    from clear_driver_data import delete_cache
except:
    exit('[ERROR!][allegro_v2] no required modules')

def get_v1_link_list():
    while os.path.isfile('_allegro.db-journal'):
        waiting(60, 'Czekam na zwolnienie pliku bazy danych...')
    con, cur = create_database()
    licznik2 = int(licznik) + 3
    cur.execute("""SELECT id, adres_oferty FROM dane_allegro where id > ? and id < ?;""",(str(licznik), str(licznik2)))
    data =  cur.fetchall()
    try:
        last_id = str((data[-1])[0])
    except:
        waiting(3600, 'Brak nowych danych.')
        get_v1_link_list()
    con.close()
    modification_parser(last_id)
    return data, last_id

def scrap(data, driver, last_id):
    def check_if_blocked(driver, ip_span):
        times = 0
        while True:
            try:
                driver.switch_to.default_content()
                iframe = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(iframe)
                if 'Zostałeś zablokowany.' in driver.find_element_by_xpath('//div[@class="captcha__human__title"]').text:
                    ip_span += 1
                    if ip_span > 8:
                        times += 1
                        ip_span = 4
                        waiting(7200, 'Zostałeś zablokowany. Czekam...')
                    driver = delete_cache(driver)
                    driver = extension(driver, ip_span)
                    time.sleep(random.uniform(1, 3))
                    driver.refresh()
                    time.sleep(random.uniform(2, 3))
                else:
                    driver.switch_to.default_content()
                    break
            except:
                driver.switch_to.default_content()
                break
        ended_offer = check_if_load_or_exist(driver)
        return ended_offer

    def check_if_load_or_exist(driver):
        try:
            while True:
                time.sleep(random.uniform(1, 3))
                WebDriverWait(driver, 1).until(EC.element_to_be_located((By.XPATH,'//div[@id="main-frame-error"]')))
                driver.refresh()
                try:
                    WebDriverWait(driver, 1).until(EC.element_to_be_located((By.XPATH,'//div[@id="main-frame-error"]')))
                    driver.refresh()
                except:
                    break
        except:
            pass

        ended_offer = False
        try:
            ended = driver.find_element_by_xpath('//div[@data-box-name="Ended message"]/div/div/div/h4').text
            ended_offer = True
        except:
            try:
                ended = driver.find_element_by_xpath('//div[@data-box-name="Offer killed message container"]/div/div/h3').text
                ended_offer = True
            except:
                ended_offer = False

        try:
            blocked_js = driver.find_element_by_xpath('//p[@id="cmsg"]')
            driver.refresh()
            time.sleep(random.uniform(1, 2))
        except:
            pass

##        try:
##            mess = driver.find_element_by_xpath('//body[@class="meqh_en"]')
##            driver.refresh()
##            time.sleep(random.uniform(1, 2))
##        except:
##            pass
        return ended_offer

    def js_data(element,x_path, single_link, is_captcha, check):
        try:
            time.sleep(random.uniform(3, 5))
            element.click()
            time.sleep(random.uniform(4, 7))
            if check:
                element2 = element.find_elements_by_xpath('//section[@class="_sizcr _1xzdi _ai5yc _1vzz9 _ku8d6 _1o9j9 _1yx73 _1k7mg _10a7o"]/h4')
                for elements in element2:
                    if elements.text == 'Kontakt':
                        element3 = elements.find_elements_by_xpath('..//div[@class="_31b2a_2D760"]/span')
                        for elements in element3:
                            if elements.get_attribute('class') == '_kz8jr _31b2a_5mXDa _31b2a_14F6t':
                                try:
                                    element.find_element_by_xpath('//button[@data-box-name="SellerMobileShow"]').click()
                                    telefon = elements.find_element_by_xpath('..//ul[@class="_17qy1 _1rj80 _1sql3 _3a4zn"]').text
                                except:
                                    telefon = ''
                            if elements.get_attribute('class') == '_kz8jr _31b2a_5mXDa _31b2a_1L727':
                                try:
                                    element.find_element_by_xpath('//button[@data-box-name="SellerEmailShow"]').click()
                                    mail = elements.find_element_by_xpath('..//a[@data-box-name="SellerEmailClick"]').text
                                except:
                                    mail = ''
                try:
                    na_allegro_od = element.find_element_by_xpath('//div[@data-role="account-info"]/div').text
                    na_allegro_od = na_allegro_od.replace('NA ALLEGRO','').replace('\n','')
                except:
                    pass
                try:
                    if_likes = element.find_element_by_xpath('//div[@data-role="recommends"]//p')
                    likes = if_likes.find_element_by_xpath('//p[1]').text
                    dislikes = if_likes.find_element_by_xpath('//p[2]').text
                except:
                    pass
            else:
                likes = ''
                dislikes = ''
                na_allegro_od = ''
                telefon = ''
                mail = ''
            varieble = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,x_path))).text
            exit_button = element.find_element_by_xpath('//button[@class="_13q9y _8hkto _1sql3 _1s3ga _1wulo _1fwkl _62fe8_r7sOX"]')
            driver.execute_script("arguments[0].click();", exit_button)
            is_captcha = False
        except:
            try:
                if 'Brak' in element.find_element_by_xpath('//h3[@class="_1s2v1 _dsf2b _cpwap"]').text:
                    varieble = ''
                else:
                    try:
                        varieble = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,x_path))).text

                    except:
                        varieble = ''
                exit_button = element.find_element_by_xpath('//button[@class="_13q9y _8hkto _1sql3 _1s3ga _1wulo _1fwkl _62fe8_r7sOX"]')
                driver.execute_script("arguments[0].click();", exit_button)
                is_captcha = False
            except:
                driver.refresh()
                try:
                    if 'captcha' in driver.find_element_by_tag_name('iframe').get_attribute('src'):
                        is_captcha = True
                        varieble = ''
                        check_captcha(driver, single_link)
                        ended_offer = check_if_blocked(driver, ip_span)
                        time.sleep(random.uniform(1, 2))
                        exit_button = driver.find_element_by_xpath('//button[@class="_13q9y _8hkto _1sql3 _1s3ga _1wulo _1fwkl _62fe8_r7sOX"]')
                        driver.execute_script("arguments[0].click();", exit_button)
                    else:
                        varieble = ''
                        is_captcha = False
                except:
                   varieble = ''
                   is_captcha = False
        return varieble, is_captcha, telefon, mail

    def refresh(profil_href, ile_osob_ile_sztuk, ile_sztuk, fvat, wersja, cena, dostawa, reklamacja, zwroty, o_sprzedajacym, is_captcha, telefon, mail):
        time.sleep(1)
        driver.execute_script("arguments[0];", driver.get(single_link))
        time.sleep(random.uniform(2, 4))

        try:
            if driver.find_element_by_xpath('//div[@class="error-box"]'):
                driver.execute_script("arguments[0];", driver.get(single_link))
        except:
            pass

        ended_offer = check_if_blocked(driver, ip_span)

        try:
            if 'captcha' in driver.find_element_by_tag_name('iframe').get_attribute('src'):
                check_captcha(driver, single_link)
                ended_offer = check_if_blocked(driver, ip_span)
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

            if ended_offer:
                pass
            else:
                try:
                    find_faktura = driver.find_elements_by_xpath('//div[@class="_17qy1 _f8818_DQKcc"]')
                    for faktura in find_faktura:
                        fvat = faktura.text
                        if 'faktur' in fvat:
                            break
                        else:
                            fvat = ''
                except:
                    pass
                try:
                    try:
                        ile_osob_ile_sztuk = driver.find_element_by_xpath('//div[@class="_1t7v4 _9a071_3U3_6 _1h7wt"]').text
                    except:
                        ile_osob_ile_sztuk = driver.find_element_by_xpath('//div[@class="_1h7wt mgn2_13 _1vryf _1t7v4"]').text
                except:
                    pass
                try:
                    profil_href = driver.find_element_by_xpath('//a[@data-analytics-click-value="SellerAllListing"]').get_attribute("href")
                except:
                    pass
                try:
                    ile_sztuk = driver.find_element_by_xpath('//*[@id="buy-now-form"]/div[1]/div[2]/div[2]').text
                except:
                    pass
                try:
                    cena = driver.find_element_by_xpath('//div[@class="_9a071_1Ov3c"]/div[2]/div').text
                except:
                    pass
                if cena == '' or cena == None:
                    try:
                        cena = driver.find_element_by_xpath('//div[@class="_9a071_1Ov3c"]/div/div').text
                    except:
                        pass
                try:
                    find_wersja = driver.find_elements_by_xpath('//div[@class="_17qy1 _f8818_DQKcc"]')
                    for wersja in find_wersja:
                        wersja = wersja.text
                        if 'cyfrowa' in wersja:
                            break
                        else:
                            wersja = ''
                    if wersja == '':
                        for wersja in find_wersja:
                            wersja = wersja.text
                            if 'elektroniczna' in wersja:
                                break
                            else:
                                wersja = ''
                except:
                    pass
                time.sleep(random.uniform(3, 5))

                while is_captcha:
                    try:
                        is_captcha = False
                        box1 = driver.find_element_by_xpath('//div[@data-box-name="Bars"]')
                        box2 = box1.find_elements_by_xpath('//h2[@class="_1s2v1 _dsf2b _1rj80 _7qjq4"]')
                        driver.execute_script("arguments[0].scrollIntoView();", box1)
                        time.sleep(random.uniform(2, 3))
                        driver.execute_script("window.scrollTo(0, window.scrollY - 200)")
                        for element in box2:
                            header = element.text
                            if 'Dostawa' in header:
                                try:
                                    x_path = '//div[@data-box-name="ShippingInfoShow"]/div/div/div'
                                    #time.sleep(rand_time_1)
                                    check = False
                                    dostawa, is_captcha, telefon, mail = js_data(element,x_path, single_link, is_captcha, check)
                                except:
                                    pass
                            if 'Reklamacja' in header:
                                try:
                                    x_path = '//div[@class="_vnd3k _1nucm"]/div[2]/div/div'
                                    #time.sleep(rand_time_1)
                                    check = False
                                    reklamacja, is_captcha, telefon, mail = js_data(element, x_path, single_link, is_captcha, check)
                                except:
                                    pass
                            if 'Zwroty' in header:
                                try:
                                    x_path = '//div[@class="_vnd3k _1kwvx _1h23x"]/div[1]/div[2]'
                                    #time.sleep(rand_time_1)
                                    check = False
                                    zwroty, is_captcha, telefon, mail = js_data(element, x_path, single_link, is_captcha, check)
                                except:
                                    pass
                            if 'O sprzedającym' in header:
                                try:
                                    x_path = '//section[@class="_sizcr _1xzdi _ai5yc _1vzz9 _ku8d6 _1o9j9 _1yx73 _1k7mg _10a7o"]/div'
                                    #time.sleep(rand_time_1)
                                    check = True
                                    o_sprzedajacym, is_captcha, telefon, mail = js_data(element, x_path, single_link, is_captcha, check)
                                    o_sprzedajacym = o_sprzedajacym.replace('pytanie do sprzedającego','')
                                except:
                                    pass
                    except:
                        pass
        except:
            pass
        return profil_href, ile_osob_ile_sztuk, ile_sztuk, fvat, wersja, cena, dostawa, reklamacja, zwroty, o_sprzedajacym, telefon, mail

    data_list = []
    for single in data:
        single_id = single[0]
        single_link = single[1]
        print(str(single_id) + '/' + str(last_id) + ' ' + single_link)
        profil_href = ''
        ile_osob_ile_sztuk = ''
        ile_sztuk = ''
        fvat = ''
        wersja = ''
        cena = ''
        dostawa = ''
        reklamacja = ''
        zwroty = ''
        o_sprzedajacym = ''
        is_captcha = True
        telefon = ''
        mail = ''
        profil_href, ile_osob_ile_sztuk, ile_sztuk, fvat, wersja, cena, dostawa, reklamacja, zwroty, o_sprzedajacym, telefon, mail = refresh(profil_href, ile_osob_ile_sztuk, ile_sztuk, fvat, wersja, cena, dostawa, reklamacja, zwroty, o_sprzedajacym, is_captcha, telefon, mail)
        try:
            data_list.append(str(single_id) + ',:*,' + profil_href + ',:*,' + ile_osob_ile_sztuk + ',:*,' + ile_sztuk + ',:*,' + fvat + ',:*,' + wersja + ',:*,' + cena + ',:*,' + dostawa + ',:*,' + reklamacja + ',:*,' + zwroty + ',:*,' + o_sprzedajacym + ',:*,' + telefon + ',:*,' + mail)
        except:
            pass
    return data_list

def update_db(data_list):
    while os.path.isfile('_allegro.db-journal'):
        waiting(60, 'Czekam na zwolnienie pliku bazy danych...')
    con, cur = create_database()
    for data in data_list:
        data = data.replace('\n','; ').split(',:*,')
        cur.execute("""UPDATE dane_allegro SET profil_href = ?, ile_osob_ile_sztuk = ?, ile_sztuk = ?, fvat = ?, wersja = ?, cena = ?, dostawa = ?, reklamacja = ?, zwroty = ?, o_sprzedajacym = ?, telefon = ?, mail = ? where id = ?;""",(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],data[11], data[12], data[0]))
    con.commit()
    con.close()

driver = my_driver()
ip_span = 6
driver = extension(driver, ip_span)
while True:
    licznik = config_parser()
    try:
        data, last_id = get_v1_link_list()
    except:
        program_log('[ERROR!][allegro_v2] Unable connect to allegro_v1.db')
        exit()
    try:
        data_list = scrap(data, driver, last_id)
    except:
        program_log('[ERROR!][allegro_v2] Scrap data problem.')
        exit()
    #driver.quit()
    update_db(data_list)
    print('---')
