#!/bin/bash

echo "Ciao, sono il tracker di Subito.it. Scegli cosa fare: "
echo "a) Controllare offerte salvate"
echo "b) Controllare nuove offerte"

read option
# echo "$option"
case "$option" in
  a ) echo "yes"
    ;;
  b ) echo "no"
    ;;
  * ) echo "forse"
    ;;
esac
