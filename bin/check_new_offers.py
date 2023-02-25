#!/usr/bin/env python

import json
import os


def save_offer(offer, file):
    dest_dir = '/home/sandro0198/.cache/search_offer/saved_offers/'
    os.replace(dir_path + file, dest_dir + file)


def discard_offer(offer, file):
    os.remove(dir_path + file)
    # print(str(offer["code"]))


dir_path = '/home/sandro0198/.cache/search_offer/new_offers/'

for file in os.listdir(dir_path):
    with open(dir_path + file, "r") as file_offer:
        offer = json.load(file_offer)
    print("Offerta trovata.")
    print(json.dumps(offer, indent=4))
    print("Cosa vuoi farci?")
    print("a) Salvala\nb) Scartala\nc) Ci penso dopo\nd) Esci")
    ask = input()
    match ask:
        case "a":
            save_offer(offer, file)
        case "b":
            discard_offer(offer, file)
        case "d":
            break
