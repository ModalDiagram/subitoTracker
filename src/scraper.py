import datetime
import requests
from bs4 import BeautifulSoup
import offer as of
import time

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

def search_offers(item, search_date):
    current_date = datetime.datetime.now()
    if search_date is None:
        search_date = current_date - datetime.timedelta(days=7)

    page_number = 0
    vecchi = 0
    offers = []
    while True:
        page_number += 1
        link_list = 'https://www.subito.it/annunci-italia/vendita/usato/?q=' + item.get("name") + '&o=' + str(page_number)

        time.sleep(1)
        response = requests.get(link_list)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Verifico che la pagina esista controllando che non ci sia la schermata di errore
        if page_exists(soup):
            # Scorro su tutti gli annunci della pagina
            for tag in soup.find_all(attrs={'class': 'item-card'}):
                offer = of.save_offer(tag)
                if offer.is_after(search_date):
                    # print_offer(offer)
                    vecchi = 0
                    if offer.is_shippable() and offer.matches_prices(item.get("minprice"), item.get("maxprice")):
                        offers.append(offer)
                else:
                    vecchi += 1
                    if vecchi == 5:
                        return offers
        else:
            return offers
