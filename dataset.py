#!/usr/bin/env python

from sys import argv
from datetime import date
from db import Base, engine, Session, Autoart, Ausstattung, Automodell
from db import Auto, Kunde, Fuehrerschein

if (__name__ == "__main__") or ("initialize" in argv):

    print("Deleting old tables...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    k1 = Kunde(id = 1, vorname = "Hans", nachname = "Mueller",
               plz = "12345", ort = "Buxdehude", strasse = "Hauptstrasse 5",
               email = "hans_mueller@web.de", telnr = "12345-67890")
    k2 = Kunde(id = 2, vorname = "Peter", nachname = "Maier",
               plz = "67890", ort = "Hintertupfingen", strasse = "Hinterhof 42",
               email = "bart@simpson.com", telnr = "123-555-678")
    k3 = Kunde(id = 3, vorname = "Dieter", nachname = "Schlosser",
               plz = "95183", ort = "Nirgendwo", strasse = "Am A. der W. 23",
               email = "foobar@example.org", telnr = "43156-12396")
    k4 = Kunde(id = 4, vorname = "Friedrich", nachname = "Lauert",
               plz = "34561", ort = "Stuttgart", strasse = "Hochweg 48",
               email = "LaFr@online.com", telnr = "35784-37098")
    k5 = Kunde(id = 5, vorname = "Guenther", nachname = "Rack",
               plz = "56872", ort = "Muenchen", strasse = "Bodenseeweg 92",
               email = "TherGuen@gmx.de", telnr = "90834-28907")
    k6 = Kunde(id = 6, vorname = "Horst", nachname = "Schenk",
               plz = "45717", ort = "Berlin", strasse = "Baumschule 13",
               email = "HoSch@t-online.de", telnr = "09345-12096")
    k7 = Kunde(id = 7, vorname = "Wolfgang", nachname = "Hell",
               plz = "57824", ort = "Hamburg", strasse = "Sommerstrasse 4",
               email = "dood@gmail.com", telnr = "12037-95672")

    k1.fuehrerscheine.append(Fuehrerschein(klasse = "B"))
    k1.fuehrerscheine.append(Fuehrerschein(klasse = "C"))
    k2.fuehrerscheine.append(Fuehrerschein(klasse = "A"))
    k3.fuehrerscheine.append(Fuehrerschein(klasse = "B"))
    k4.fuehrerscheine.append(Fuehrerschein(klasse = "B"))
    k5.fuehrerscheine.append(Fuehrerschein(klasse = "B"))
    k5.fuehrerscheine.append(Fuehrerschein(klasse = "C"))
    k6.fuehrerscheine.append(Fuehrerschein(klasse = "B"))
    k6.fuehrerscheine.append(Fuehrerschein(klasse = "C"))
    k7.fuehrerscheine.append(Fuehrerschein(klasse = "B"))

    aa1 = Autoart(id = 1, art = "Limousine")
    aa2 = Autoart(id = 2, art = "Kombi")
    aa3 = Autoart(id = 3, art = "Cabrio")
    aa4 = Autoart(id = 4, art = "Van")
    aa5 = Autoart(id = 5, art = "Kleinbus")
    aa6 = Autoart(id = 6, art = "LKW")
    aa7 = Autoart(id = 7, art = "Pickup")

    am1 = Automodell(id = 1, bezeichnung = "Golf FSI",
                     hersteller = "VW", autoart_id = 1,
                     sitzplaetze = 5, kw = 80, treibstoff = "Super",
                     preistag = 54.70, preiskm = 0.04, achsen = 2,
                     ladevolumen = 350, zuladung = 400, fuehrerschein = "B")
    am2 = Automodell(id = 2, bezeichnung = "Golf Variant TDI",
                     hersteller = "VW", autoart_id = 2,
                     sitzplaetze = 5, kw = 90, treibstoff = "Diesel",
                     preistag = 62.30, preiskm = 0.05, achsen = 2,
                     ladevolumen = 450, zuladung = 500, fuehrerschein = "B")
    am3 = Automodell(id = 3, bezeichnung = "Golf",
                     hersteller = "VW", autoart_id = 1,
                     sitzplaetze = 5, kw = 60, treibstoff = "Super",
                     preistag = 45.00, preiskm = 0.03, achsen = 2,
                     ladevolumen = 350, zuladung = 400, fuehrerschein = "B")
    am4 = Automodell(id = 4, bezeichnung = "Astra",
                     hersteller = "Opel", autoart_id = 1,
                     sitzplaetze = 5, kw = 70, treibstoff = "Super",
                     preistag = 40.70, preiskm = 0.04, achsen = 2,
                     ladevolumen = 330, zuladung = 380, fuehrerschein = "B")
    am5 = Automodell(id = 5, bezeichnung = "528i",
                     hersteller = "BMW", autoart_id = 1,
                     sitzplaetze = 5, kw = 120, treibstoff = "Super",
                     preistag = 83.55, preiskm = 0.07, achsen = 2,
                     ladevolumen = 320, zuladung = 440, fuehrerschein = "B")
    am6 = Automodell(id = 6, bezeichnung = "Taurus",
                     hersteller = "Daimler-Chrysler", autoart_id = 6,
                     sitzplaetze = 3, kw = 340, treibstoff = "Diesel",
                     preistag = 120.30, preiskm = 0.09, achsen = 3,
                     ladevolumen = 20000, zuladung = 4000, fuehrerschein = "C")
    am7 = Automodell(id = 7, bezeichnung = "Sharan",
                     hersteller = "VW", autoart_id = 4,
                     sitzplaetze = 7, kw = 100, treibstoff = "Super",
                     preistag = 85.60, preiskm = 0.05, achsen = 2,
                     ladevolumen = 550, zuladung = 500, fuehrerschein = "B")

    au1 = Ausstattung(id = 1, bezeichnung = "Klimaanlage")
    au2 = Ausstattung(id = 2, bezeichnung = "Anhaengekupplung")
    au3 = Ausstattung(id = 3, bezeichnung = "Navigationssystem")
    au4 = Ausstattung(id = 4, bezeichnung = "Tempomat")

    am1.ausstattungen.append(au1)
    am2.ausstattungen.append(au2)
    am5.ausstattungen.append(au1)
    am5.ausstattungen.append(au3)
    am5.ausstattungen.append(au4)
    am7.ausstattungen.append(au1)
    am7.ausstattungen.append(au2)

    a1 = Auto(kennzeichen = "RV AB 335", kmstand = 45000,
              tuvtermin = date(2004, 05, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 3)
    a2 = Auto(kennzeichen = "RV AB 336", kmstand = 39000,
              tuvtermin = date(2004, 05, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 3)
    a3 = Auto(kennzeichen = "RV AB 337", kmstand = 41000,
              tuvtermin = date(2004, 05, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 3)
    a4 = Auto(kennzeichen = "RV XY 245", kmstand = 18000,
              tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 1)
    a5 = Auto(kennzeichen = "RV XY 246", kmstand = 19000,
              tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 5)
    a6 = Auto(kennzeichen = "RV XY 247", kmstand = 21000,
              tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 2)
    a7 = Auto(kennzeichen = "RV XY 248", kmstand = 35000,
              tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 2)
    a8 = Auto(kennzeichen = "RV XY 249", kmstand = 29050,
              tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 2)
    a9 = Auto(kennzeichen = "RV BQ 591", kmstand = 65000,
              tuvtermin = date(2005, 06, 01), kaufdatum = date(2002, 05, 01),
              modell_id = 4)
    a10 = Auto(kennzeichen = "RV BQ 592", kmstand = 66000,
               tuvtermin = date(2005, 06, 01), kaufdatum = date(2002, 05, 01),
               modell_id = 4)
    a11 = Auto(kennzeichen = "RV BQ 593", kmstand = 64500,
               tuvtermin = date(2005, 06, 01), kaufdatum = date(2002, 05, 01),
               modell_id = 4)
    a12 = Auto(kennzeichen = "RV C 45", kmstand = 150000,
               tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
               modell_id = 6)
    a13 = Auto(kennzeichen = "RV MM 999", kmstand = 16000,
               tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
               modell_id = 5)
    a14 = Auto(kennzeichen = "RV PF 23", kmstand = 25000,
               tuvtermin = date(2005, 04, 01), kaufdatum = date(2002, 05, 01),
               modell_id = 7)

    print("Inserting sample values...")
    session = Session()
    session.add_all([
        k1, k2, k3, k4, k5, k6, k7,
        aa1, aa2, aa3, aa4, aa5, aa6, aa7,
        am1, am2, am3, am4, am5, am6, am7,
        au1, au2, au3, au4,
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14
    ])
    session.commit()
    exit()

