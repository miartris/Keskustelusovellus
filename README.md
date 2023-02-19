# Keskustelusovellus

Esimerkkiaihetta mukaileva sovellus on internetfoorumi-tyylinen, eli se sisältää eri aihekategorioita jotka sisältävät relevantteja viesteistä koostuvia keskusteluketjuja.\
Viestit voivat sisältää tekstin lisäksi myös pienen upotetun kuvatiedoston.

Käyttäjätyyppejä on kaksi: **ylläpitäjä** ja **peruskäyttäjä**.

## Sovelluksen nykytila

- Yksi käyttäjätyyppi, peruskäyttäjä
- Sivulle voi rekisteröityä ja rekisteröidyttyä voi kirjautua sisään. Käyttäjä saa tietoa onnistumisista ja virheistä
- Sisäänkirjautunut käyttäjä voi uloskirjautua
- Etusivulla näytetään kaikki "topics" taulussa olevat aiheet
- Aihealueen sisällä kirjautunut käyttäjä voi luoda viestiketjun. Kaikki aihealueen viestiketjut ja niiden luomisajankohdat listataan allekkain

## Lopullisia ominaisuuksia:

- Käyttäjätilin luominen, sisään- ja uloskirjautuminen
- Lista alueista, alueelle siirtyminen tuo näkyviin listan viestiketjuista joihin siirtyminen tuo näkyville viestit ja kentän viestin kirjoittamiseen
- Käyttäjä voi luoda viestiketjun tai kirjoittaa ketjuun viestin, ja poistaa omia luomuksiaan. Ylläpitäjä voi poistaa kaikkea sisältöä
- Viestejä voidaan "peukuttaa"
- Alueille ja ketjuille on viestimäärät ja aikaleima viimeisimmästä päivityksestä
- Käyttäjillä on profiilit, jotka voivat sisältää esittelyn ja profiilikuvan
- Käyttäjät voivat lähettää toisilleen yksityisviestejä
- Keskustelualueen viestiketjuja ja viestejä voidaan etsiä hakusanalla

## Käynnistysohjeet

Kloonaa ensin projektin koodi omalle laitteelleesi

Luo .env kansio juurihakemistoon ja lisää tietokantayhteys ympäristömuuttujana muodossa "DATABASE_URI=tietokantasi_tähän"
ja flask-sessioita varten sala-avain "SECRET_KEY=avain_tähän"

luo pythonin virtuaaliympäristö, aktivoi se ja asenna riippuvuudet. Linuxilla

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt
```

Tietokannan skeema pitää määrittää komennolla 

```
psql < schema.sql 
```

Tällä hetkellä aiheita voi luoda ainoastaan lisäämällä ne suoraan tietokantaan. Muutaman esimerkkiaiheen saa luotua tietokannan
skeeman määrittämisen jälkeen näin
```
psql < dummy_data.sql
```

sovellus käynnistyy projektin juurihakemistossa

```
flask run
```

