# Nazwa projektu

Projekt ma na celu umożliwienie użytkownikowi:
 - szybkie sprawdzeniem 50 kolekcji z największym volumenem na markecie https://minted.network/
 - wylistowanie wg adresu portfela wszystkich NFT - wypisanie wg nazw kolekcji, ilość sztuk
 - obliczenie wartości każdej kolekcji oraz całego portfela wg obecnego floor price 
 na marketach https://minted.network/ oraz https://app.ebisusbay.com/

## Wymagania systemowe

- Python 3.x
- Biblioteka X
- Biblioteka Y

## Instalacja

1. Sklonuj to repozytorium.
2. Zainstaluj zależności za pomocą komendy 
`pip install -r requirements.txt`
'pip install Flask'
'pip install Flask-SQLAlchemy'
3. Uruchom skrypt `app.py`.


## Użycie

4. Wejdź teraz na stronę:
http://127.0.0.1:5000
5. Za pierwszym razem należy się zarejestrować, następnie możemy się logować tymi danymi.
Wyświetli się lista kolekcji NFT z największym volumenem w ciagu ostatnich 24h na markecie Minted.
Lista jest od największego volumenu w dół. Przy każdej kolekcji mamy różnicę ceny od ostatnich 24h, obecny floor price. 
Program kolorami informuje nas jaka zmiana zaszła - zielony wzrost ceny poniżej 20% , czerwony zmniejszenie ceny do 20% oraz
 na zółto zwiększenie lub zmniejszenie ceny o ponad 20%
 Przy każdej kolekcji mamy przycisk "GO", który przenosi nas na stronę, gdzie wyświetli się 10 kolejnych NFT,
 z danej kolekcji o najniższym floor price.
 6. 

## Kontakt

W przypadku pytań lub problemów z projektem skontaktuj się z nami przez e-mail.

## Licencja

Projekt jest udostępniany na licencji MIT.
