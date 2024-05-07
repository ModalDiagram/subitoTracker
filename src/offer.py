import convert_date as cd

class model_offer:
    title = ""
    price = ""
    date = ""
    link = ""
    shippable = ""

    def __str__(self):
        return "Titolo: {}\nPrezzo: {}\nData: {}\nLink: {}\n".format(self.title, self.price, self.date, self.link)

    def is_shippable(self):
        return self.shippable

    def matches_prices(self, minprice, maxprice):
        if minprice is None:
            minprice = 0
        if maxprice is None:
            maxprice = 100000
        return minprice <= self.price <= maxprice

    def is_after(self, date):
        if self.date is None:
            return False

        return self.date > date

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


def analyze_price(offer, tag):
    """
    La funzione trova il prezzo dell'articolo
    :param tag: articolo
    :return:
    """
    price = tag.find_all(attrs={'class': 'SmallCard-module_price__yERv7'})[0]
    price_sped = price.text

    if "€" in price_sped:
        if "Spedizione" in price_sped:
            offer.shippable = True

        price = price_sped.split("€")
        offer.price = float(price[0])
    else:
        offer.price = None

    return offer


def find_date(tag):
    """
    La funzione trova la data dell'articolo
    :param tag:
    :return:
    """
    date = tag.find_all(attrs={'class': 'index-module_date__Fmf-4'})
    if len(date) > 0:
        date = cd.subitotime_to_datetime(date[0].text)
        return date
    else:
        return None


def find_link(tag):
    link = tag.a.get("href")
    return link


def save_offer(tag):
    """
    Salvo tutti gli elementi dell'offerta
    :param tag: tag dell'offerta da analizzare
    :return: ModelOffer con tutti gli elementi dell'offerta
    """

    my_offer = model_offer()
    my_offer = analyze_price(my_offer, tag)
    my_offer.title = find_title(tag)
    my_offer.date = find_date(tag)
    my_offer.link = find_link(tag)

    return my_offer

