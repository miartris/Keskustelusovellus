# Keskustelusovellus

Esimerkkiaihetta mukaileva sovellus on internetfoorumi-tyylinen, eli se sisältää eri aihekategorioita jotka sisältävät relevantteja viesteistä koostuvia keskusteluketjuja.\
Viestit voivat sisältää tekstin lisäksi myös pienen upotetun kuvatiedoston.

Käyttäjätyyppejä on kaksi: **ylläpitäjä** ja **peruskäyttäjä**.

## Sovelluksen lopputila

### Käyttäjä
- Kaksi käyttäjätyyppiä, peruskäyttäjä ja ylläpitäjä
- Sivulle voi rekisteröityä ja rekisteröidyttyä voi kirjautua sisään. Käyttäjä saa tietoa onnistumisista ja virheistä
- Sisäänkirjautunut käyttäjä voi uloskirjautua
### Foorumi
- Etusivulla näytetään kaikki "topics" taulussa olevat aiheet ja vähän sivun tilastoja. Ylläpitäjät näkevät kaavakkeen, jolla aihealueen voi luoda
- Aihealueen sisällä kirjautunut käyttäjä voi luoda viestiketjun. Kaikki aihealueen viestiketjut ja niiden luomisajankohdat listataan allekkain
- Viestiketjun sisällä listataan kaikki viestit allekkain, viimeisen viestin jälkeen sisäänkirjautunut käyttäjä näkee kaavakkeen jolla voi luoda uuden viestin.
- Viestejä voi peukuttaa
### Profiili
- Viestin yhteydessä näkyvästä käyttäjänimestä pääsee kyseisen käyttäjän profiiliin, navigointipalkista pääsee omaan profiiliin
- Profiilissa on vähän tilastotietoa ja käyttäjän esittely sekä kuva. Jos näitä ei ole luotu näkyvillä on vakioarvot
- Käyttäjä voi omassa profiilissaan ladata profiilikuvan ja luoda esittelyn tai muokata sitä

## Mitä ei ehditty toteuttaa:

- Poistotoiminnallisuus
- Käyttäjien väliset yksityisviestit
- Viestien haku avainsanalla
- Kuvaviestit

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

Muutaman esimerkkiaiheen saa luotua tietokannan skeeman määrittämisen jälkeen näin
```
psql < dummy_data.sql
```
Vaihtoehtoisesti sivulle voi rekisteröityä ylläpitäjänä ja luoda niitä etusivulta käsin.

sovellus käynnistyy projektin juurihakemistossa

```
flask run
```

