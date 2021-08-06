from configparser import ConfigParser
import sys, time

def parser_data():

    def fixchar_table(word):
        word = word.replace('Ĺ›', 'ś')
        word = word.replace('Ĺ‚', 'ł')
        word = word.replace('ĺ‚', 'ł')
        word = word.replace('ĹĽ', 'ż')
        word = word.replace('Ăł', 'ó')
        word = word.replace('Ĺ„', 'ń')
        word = word.replace('ĺ„', 'ń')
        word = word.replace('Ä‡', 'ć')
        word = word.replace('Ĺş', 'ź')
        word = word.replace('Ä…', 'ą')
        word = word.replace('Ä™', 'ę')
        return word

    def check_space_char(checkes):
        checkes2 = []
        for check in checkes:
            if ' ' in check[0]:
                check = check[1:]
            if ' ' in check[-1]:
                check = check[:-1]
            checkes2.append(check)
        return checkes2

    path = []
    parser = ConfigParser()
    parser.read('settings/config_file.ini')
    #parser.read('../settings/config_file.ini')

    licznik = parser.get('allegro_config','licznik')

    for key in parser['enter_data']:
        value = parser.get('enter_data', key)
        value = (value.lower()).replace(' ','-')
        value = fixchar_table(value)
        path.append(value)

    return licznik, path

def config_parser():
    parser = ConfigParser()
    parser.read('settings/config_file.ini')
    licznik = parser.get('allegro_config','licznik')
    return licznik

def modification_parser(licznik):
    parser = ConfigParser()
    parser.read('settings/config_file.ini')
    parser['allegro_config']['licznik'] = str(licznik)
    with open('settings//config_file.ini', 'w') as configfile:
        parser.write(configfile)
        configfile.close()