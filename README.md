# subitoTracker
Tracker di subito manuale o automatico con bot Telegram

# Funzionamento
Una ricerca tipo sarebbe:

python3 src/search_offer.py -p 10 20 caricatore (con 10-20 range di prezzo e caricatore nome dell'articolo).

Il programma cerca la pagina di subito con il titolo dato e la analizza.
Per ciascun articolo:

* se il prezzo è compreso nel range
* se è disponibile la spedizione
* se non è stato visto in precedenza (blacklist)

la fornisce all'utente che può decidere se cercarne un'altra.

# Flag -a
Se la flag -a è fornita (per automatic) invece di dare l'offerta all'utente manda un messaggio con bot di Telegram
(token e chat_id da specificare nel file) bin/secrets.txt nel formato:  
token  
chat_id  
(ad esempio:  
1232345909:asdkfjkl  
3405231  
).
Inoltre, la salva come file json per essere ripresa dopo attraverso gli script in bin/.

# Blacklist
Il programma salva il timestamp dell'ultima ricerca nella cache (directory da modificare nel file) e scarta le offerte
con timestamp precedente. Può anche essere specificato con flag -t.

# Periodicità
Si può modificare il file wishlist.txt e poi chiamare periodicamente lo script bin/check_wishlist.sh per lanciare search_offer.py con ciascun elemento della wishlist e nel range di prezzo specificato.
