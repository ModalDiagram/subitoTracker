import json
import os

def get_wishlist():
    wishlist = []
    main_dir = os.path.dirname(__file__)
    with open(os.path.join(main_dir, "../wishlist.json"), "r") as wishlist_file:
        wishlist_json = json.load(wishlist_file)
    for item in wishlist_json:
        if all(k in item.keys() for k in ("name", "minprice", "maxprice")):
            wishlist.append(item)
    return wishlist
