#-*- coding: utf-8 -*-
import sqlite3
import os

def create_database():
    entries = os.listdir()
    is_entry = False
    for entry in entries:
        if '.db' in entry:
            is_entry = True
            break
    if is_entry:
        con = sqlite3.connect(entry)
    else:
        con = sqlite3.connect('_allegro.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dane_allegro (
                id INTEGER PRIMARY KEY ASC,
                adres_oferty varchar NOT NULL,
                tytul_ogloszenia varchar,
                stan varchar,
                wersja varchar,
                cena varchar,
                ile_osob_kupilo varchar,
                nazwa_uzytkownika varchar,
                ile_osob_ile_sztuk varchar,
                ile_sztuk varchar,
                fvat varchar,
                dostawa varchar,
                reklamacja varchar,
                zwroty varchar,
                o_sprzedajacym varchar,
                telefon varchar,
                mail varchar,
                likes_konta varchar,
                dislikes_konta varchar,
                na_allegro_od varchar
                )""")
    return con, cur