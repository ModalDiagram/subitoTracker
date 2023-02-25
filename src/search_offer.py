#!/usr/bin/env /home/sandro0198/anaconda3/envs/prova/bin/python

# Questo software cerca su subito.it le offerte con le keyword stabilite e nel prezzo ricercato.
# Normalmente, cerca annunci dell'ultima settimana; in alternativa si puo' indicare con -t
# un timestamp da cui iniziare a cercare annunci.
# La flag -a indica se vogliamo chiedere all'utente di salvare le offerte o se
# mandarle per Telegram
# Utilizza un formato del tipo
# python3 -p 30 50 pokemon scarlatto

import json
import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup
from model_offer import model_offer
import convert_date as cdat

# Analisi delle opzioni
# Default
verbose = False
debug = False
price_range = False
initial = False
automatic = False
# Aggiunte
idx = 0
kw = ''
while idx < (len(sys.argv) - 1):
    idx += 1
    match sys.argv[idx]:
        case "-h":
            print("Formato del tipo")
            print("python3 -p 30 50 pokemon scarlatto")
            print("Ricorda di attivare anaconda e l'environment giusto")
            sys.exit()
        case "-p":
            price_min = int(sys.argv[idx + 1])
            price_max = int(sys.argv[idx + 2])
            idx += 2
            price_range = True
        case "-a":
            automatic = True
            token = str(sys.argv[idx + 1])
            chat_id = str(sys.argv[idx + 2])
            idx +=2
        case "-t":
            initial = True
            given_date = datetime.datetime.fromtimestamp(int(sys.argv[idx + 1]))
            idx += 1
        case "-v":
            verbose = True
        case _:
            kw += sys.argv[idx] + '+'


def send_telegram_messages(msg):
    """
    Mando un messaggio col bot se trovo un'offerta e -a è specificato
    :param msg: messaggio da mandare
    """
    request_url = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text=" + msg
    requests.get(request_url)


def create_file_json(offer, name):
    """
    creo un file json contenente l'offerta e lo metto nella
    cartella folder_offers (nella cache)
    :param offer: offerta da salvare
    """
    compact_name = name.replace(" ", "_").lower()
    compact_name = compact_name.replace("/", "_").lower()
    folder_offers = "/home/sandro0198/.cache/search_offer/new_offers"
    if not os.path.exists(folder_offers):
        os.makedirs(folder_offers)
    with open(folder_offers + '/' + compact_name + '.json', 'w') as file:
        file.write(json.dumps(offer, ensure_ascii=False))


def page_exists(page):
    """
    Verifico che la pagina non sia una pagina di errore di Subito
    :param page: pagina da verificare
    :return: true se esiste, false altrimenti
    """
    error_offer = ""
    for error in page.find_all(attrs={'class': 'ErrorLayout_title__FWtf0'}):
        error_offer = error.text
    if "Nessun" in error_offer:
        return False
    return True


def save_offer(tag):
    """
    Salvo tutti gli elementi dell'offerta
    :param tag: tag dell'offerta da analizzare
    :return: ModelOffer con tutti gli elementi dell'offerta
    """
    title = find_title(tag)
    if verbose:
        print("Titolo: " + title)

    price_sped = find_price(tag)
    date = find_date(tag)
    link = find_link(tag)

    my_offer = model_offer()
    my_offer.title = title
    my_offer.price = price_sped
    my_offer.date = date
    my_offer.link = link

    return my_offer


def find_title(tag):
    """
    La funzione trova il titolo dell'articolo
    :param tag: articolo
    :return:
    """
    title = tag.find_all(attrs={'class': 'SmallCard-module_item-title__1y5U3'})[0]
    # print(title)
    title_offer = title.text
    return title_offer


def find_price(tag):
    """
    La funzione trova il prezzo dell'articolo
    :param tag: articolo
    :return:
    """
    price = tag.find_all(attrs={'class': 'SmallCard-module_price__yERv7'})[0]
    price_offer = price.text
    return price_offer


def find_date(tag):
    """
    La funzione trova la data dell'articolo
    :param tag:
    :return:
    """
    date_offer = ""
    date = tag.find_all(attrs={'class': 'index-module_date__Fmf-4'})
    if len(date) > 0:
        date_offer = date[0].text
    return date_offer


def find_link(tag):
    link = tag.a.get("href")
    return link


def check_price(price_sped):
    """
    La funzione controlla che il prezzo sia nel formato giusto,
    che l'articolo abbia un prezzo dichiarato
    e sia possibile la spedizione di subito
    :param price_sped:
    :return:
    """
    if "€" in price_sped:
        if "Spedizione" in price_sped:
            price = price_sped.split("€")
            price = float(price[0])
            if verbose:
                print("Prezzo: " + str(price))

            # Controllo che il prezzo sia nel range
            if price_range:
                if not (price_min <= float(price) <= price_max):
                    return False
            return price
        if verbose:
            print("Spedizione non disponibile")
        return False
    if verbose:
        print("Prezzo non disponibile")
    return False


def check_date(offer_date, current_date, search_date):
    if offer_date == "":
        return False
    offer_date = cdat.ita_to_ts(offer_date, current_date)
    time_diff = offer_date - search_date
    if time_diff.total_seconds() > 0:
        return True
    return False


def print_offer(offer):
    """
    stampa l'offerta
    :param offer:  offerta da stampare
    """
    print("Offerta trovata.")
    print("Titolo: " + offer.title)
    print("Prezzo: " + str(offer.price))
    print("Data: " + offer.date)
    print("Link: " + offer.link)


def find_all_offers():
    check = True
    page_number = 0
    vecchi = 0
    current_date = datetime.datetime.now()

    if not initial:
        search_date = current_date - datetime.timedelta(days=7)
    else:
        search_date = given_date

    while check:
        page_number += 1
        link_list = 'https://www.subito.it/annunci-italia/vendita/usato/?q=' + kw + '&o=' + str(page_number)
        if verbose:
            print(link_list)

        response = requests.get(link_list)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Verifico che la pagina esista controllando che non ci sia la schermata di errore
        if page_exists(soup):
            # Scorro su tutti gli annunci della pagina
            for tag in soup.find_all(attrs={'class': 'item-card'}):
                offer = save_offer(tag)
                if check_date(offer.date, current_date, search_date):
                    # print_offer(offer)
                    vecchi = 0
                    offer.price = check_price(str(offer.price))
                    if offer.price:
                        if not automatic:
                            print_offer(offer)
                            print("Vuoi cercarne un'altra? [y/n]")
                            ask = input()
                            if ask == "n":
                                check = False
                                break
                            print("\n\n")
                        else:
                            create_file_json(offer.toDictionary(), offer.title)
                            send_telegram_messages("Offerta trovata.\n" + json.dumps(offer.toDictionary(), indent=4))
                else:
                    vecchi += 1
                    if vecchi == 5:
                        if verbose:
                            print("Troppo vecchi")
                        check = False
                        break

                if debug:
                    break
        else:
            if verbose:
                print("Finite le pagine")
            break
        if debug:
            break


find_all_offers()
