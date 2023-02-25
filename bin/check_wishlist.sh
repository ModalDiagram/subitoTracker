#!/bin/bash

while read -r token; do
  read -r chatid
  break;
done < "$HOME/PycharmProjects/subitoTracker/bin/secrets.txt"
wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
  read -r timestamp < $HOME/.cache/search_offer/last_check.txt
  while read -r line; do
    nome=${line#*:}
    range=${line%:*}
    $HOME/PycharmProjects/subitoTracker/src/search_offer.py -p $range -i -a $token $chatid -t $timestamp $nome
  done < "$HOME/PycharmProjects/subitoTracker/wishlist.txt"

  echo $(date +"%s") > $HOME/.cache/search_offer/last_check.txt
fi
