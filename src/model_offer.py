class model_offer:
    title = ""
    price = ""
    date = ""
    link = ""

    def toDictionary(self):
        recipe = {"title": self.title, "price": self.price, "date": self.date, "link": self.link}
        return recipe
