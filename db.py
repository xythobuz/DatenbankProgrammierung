#!/usr/bin/env python

# http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
# http://docs.sqlalchemy.org/en/rel_1_0/orm/relationships.html

from sys import argv
from sqlalchemy import create_engine, event, Table, Column, ForeignKey
from sqlalchemy import Integer, Float, String, Date, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

printSQL = True
if "quiet" in argv:
    printSQL = False

Base = declarative_base()
engine = create_engine("sqlite:///dapro.db", echo = printSQL)
Session = sessionmaker(bind = engine)

# Workaround for 'BEGIN/COMMIT' bug in pysqlite driver
# http://docs.sqlalchemy.org/en/rel_1_0/dialects/sqlite.html#pysqlite-serializable
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    dbapi_connection.isolation_level = None

# Enable custom transaction concurrency control
# http://sqlite.org/lang_transaction.html
@event.listens_for(engine, "begin")
def do_begin(conn):
    conn.execute("BEGIN IMMEDIATE")

class Autoart(Base):
    __tablename__ = "autoart"
    id = Column(Integer, primary_key = True)
    art = Column(String)

modell_hat_ausstattung = Table("modhatausst", Base.metadata,
    Column("mid", Integer, ForeignKey("automodell.id")),
    Column("aid", Integer, ForeignKey("ausstattung.id")))

class Ausstattung(Base):
    __tablename__ = "ausstattung"
    id = Column(Integer, primary_key = True)
    bezeichnung = Column(String)
    modelle = relationship("Automodell",
                           secondary = modell_hat_ausstattung,
                           back_populates = "ausstattungen")

class Automodell(Base):
    __tablename__ = "automodell"
    id = Column(Integer, primary_key = True)
    bezeichnung = Column(String)
    hersteller = Column(String)
    sitzplaetze = Column(Integer)
    kw = Column(Integer)
    treibstoff = Column(String)
    preistag = Column(Float)
    preiskm = Column(Float)
    achsen = Column(Integer, default = 2)
    ladevolumen = Column(Integer)
    zuladung = Column(Integer)
    fuehrerschein = Column(String)
    autoart_id = Column(Integer, ForeignKey("autoart.id"))
    autoart = relationship("Autoart")
    ausstattungen = relationship("Ausstattung",
                                 secondary = modell_hat_ausstattung,
                                 back_populates = "modelle")
    autos = relationship("Auto", back_populates = "modell")

class Auto(Base):
    __tablename__ = "auto"
    kennzeichen = Column(String, primary_key = True)
    kmstand = Column(Integer)
    tuvtermin = Column(Date)
    kaufdatum = Column(Date)
    modell_id = Column(Integer, ForeignKey("automodell.id"))
    modell = relationship("Automodell", back_populates = "autos")

class Kunde(Base):
    __tablename__ = "kunde"
    id = Column(Integer, primary_key = True)
    vorname = Column(String)
    nachname = Column(String)
    plz = Column(String)
    ort = Column(String)
    strasse = Column(String)
    email = Column(String)
    telnr = Column(String)
    fuehrerscheine = relationship("Fuehrerschein", back_populates = "kunde")

class Fuehrerschein(Base):
    __tablename__ = "fuehrerschein"
    klasse = Column(String, primary_key = True)
    kunde_id = Column(Integer, ForeignKey("kunde.id"), primary_key = True)
    kunde = relationship("Kunde", back_populates = "fuehrerscheine")

class Reservierung(Base):
    __tablename__ = "reservierung"
    id = Column(Integer, primary_key = True)
    beginn = Column(DateTime)
    ende = Column(DateTime)
    kunde_id = Column(Integer, ForeignKey("kunde.id"))
    kunde = relationship("Kunde")
    modell_id = Column(Integer, ForeignKey("automodell.id"))
    modell = relationship("Automodell")

