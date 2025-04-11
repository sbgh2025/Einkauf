import sqlite3
import tkinter as tk
from tkinter import messagebox

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('einkauf.db')
cursor = conn.cursor()

# Fremdschlüssel-Unterstützung aktivieren
cursor.execute("PRAGMA foreign_keys = ON;")

# Tabelle ART
cursor.execute('''
CREATE TABLE IF NOT EXISTS tbl_art (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    art TEXT NOT NULL,
    bemerkung TEXT
)
''')

# Tabelle FIRMA
cursor.execute('''
CREATE TABLE IF NOT EXISTS tbl_firma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firma TEXT NOT NULL,
    bemerkung TEXT
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS tbl_zahlung(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institut TEXT,
    zahlungsart TEXT NOT NULL CHECK (zahlungsart IN ('Kreditkarte', 'Girokarte', 'Überweisung', 'Forderung', 'Bar')),
    bemerkung TEXT
)
''')






# Tabelle EINKAUF
cursor.execute('''
CREATE TABLE IF NOT EXISTS tbl_einkauf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    e_datum DATE NOT NULL,
    e_summe DECIMAL(10, 2) NOT NULL,
    e_art INTEGER NOT NULL,
    e_firma INTEGER NOT NULL,
    e_zahlung INTEGER NOT NULL,
    e_bemerkung TEXT,
    FOREIGN KEY (e_art) REFERENCES tbl_art(id),
    FOREIGN KEY (e_firma) REFERENCES tbl_firma(id),
    FOREIGN KEY (e_zahlung) REFERENCES tbl_zahlung(id)
)
''')

conn.commit()
