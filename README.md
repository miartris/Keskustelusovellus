# Keskustelusovellus

Esimerkkiaihetta mukaileva sovellus on internetfoorumi-tyylinen, eli se sisältää eri aihekategorioita jotka sisältävät relevantteja viesteistä koostuvia keskusteluketjuja.\
Viestit voivat sisältää tekstin lisäksi myös pienen upotetun kuvatiedoston.

Käyttäjätyyppejä on kaksi: **ylläpitäjä** ja **peruskäyttäjä**.

## Ominaisuuksia:

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

luo pythonin virtuaaliympäristö, aktivoi se ja asenna riippuvuudet
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt

sovellus käynnistyy projektin juurihakemistossa
```
flask run
```