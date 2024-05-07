import wishlist as wl
import scraper
import telegram
from datetime import datetime
from os.path import exists

def main():
    wishlist = wl.get_wishlist()
    last_search = None
    if exists("/tmp/subitotracker.txt"):
        with open("/tmp/subitotracker.txt", "r") as cache_file:
            last_search = datetime.strptime(cache_file.readline(), '%y-%m-%d %H:%M:%S')

    max_last_date = datetime.today()
    for item in wishlist:
        offers = scraper.search_offers(item, last_search)
        if (len(offers) > 0) and (offer_last_date := max(offer.date for offer in offers)) > max_last_date:
            max_last_date = offer_last_date
        bot = telegram.Telegram_bot()
        bot.send_offers(offers)

    # saving the time of the last search so that we can discard offers older than this (they have already been sent)
    with open("/tmp/subitotracker.txt", "w") as cache_file:
        cache_file.write(max_last_date.strftime('%y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    main()
