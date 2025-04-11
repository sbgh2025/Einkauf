import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('einkauf.db')
cursor = conn.cursor()


# Dictionaries für ID ↔ Anzeige
def load_maps():
    global art_map, art_id_map, firma_map, firma_id_map, zahlung_map, zahlung_id_map, zahlungsart_map

    cursor.execute("SELECT id, art FROM tbl_art")
    art_options = cursor.fetchall()
    art_map = {name: id for id, name in art_options}
    art_id_map = {id: name for id, name in art_options}

    cursor.execute("SELECT id, firma FROM tbl_firma")
    firma_options = cursor.fetchall()
    firma_map = {name: id for id, name in firma_options}
    firma_id_map = {id: name for id, name in firma_options}

    cursor.execute("SELECT id, institut, zahlungsart FROM tbl_zahlung")
    zahlung_options = cursor.fetchall()
    zahlung_map = {f"{inst} - {art}": id for id, inst, art in zahlung_options}
    zahlung_id_map = {id: f"{inst} - {art}" for id, inst, art in zahlung_options}
    zahlungsart_map = {id: art for id, inst, art in zahlung_options}


load_maps()


# Funktion zum Einfügen von Daten
def insert_einkauf():
    datum = calendar.get_date()
    summe = entry_summe.get().strip()
    bemerkung = entry_bemerkung.get().strip()
    summe = summe.replace(',', '.')

    if not datum or not summe or not e_art.get() or not e_firma.get() or not e_zahlung.get():
        messagebox.showwarning("Eingabefehler", "Bitte füllen Sie alle Felder aus.")
        return

    try:
        summe = float(summe)
        if summe <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Eingabefehler", "Die Summe muss eine gültige Dezimalzahl größer als 0 sein.")
        return

    art_id = art_map.get(e_art.get())
    firma_id = firma_map.get(e_firma.get())
    zahlung_id = zahlung_map.get(e_zahlung.get())

    cursor.execute('''
        INSERT INTO tbl_einkauf (e_datum, e_summe, e_art, e_firma, e_zahlung, e_bemerkung)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datum, summe, art_id, firma_id, zahlung_id, bemerkung))
    conn.commit()
    messagebox.showinfo("Erfolg", "Der Einkauf wurde erfolgreich gespeichert.")

    entry_summe.delete(0, tk.END)
    entry_bemerkung.delete(0, tk.END)
    e_art.set('')
    e_firma.set('')
    e_zahlung.set('')

    refresh()


# Funktion zum Laden der Einkäufe für das ausgewählte Datum
def refresh():
    for row in tree.get_children():
        tree.delete(row)

    gewaehltes_datum = calendar.get_date()

    cursor.execute('''
        SELECT e.id, e.e_datum, e.e_summe, e.e_art, e.e_firma, e.e_zahlung, e.e_bemerkung,
               z.zahlungsart
        FROM tbl_einkauf e
        LEFT JOIN tbl_zahlung z ON e.e_zahlung = z.id
        WHERE e.e_datum = ?
        ORDER BY e.e_datum DESC
    ''', (gewaehltes_datum,))

    for row in cursor.fetchall():
        id_, datum, summe, art_id, firma_id, zahlung_id, bemerkung, zahlungsart = row
        art = art_id_map.get(art_id, f"#{art_id}")
        firma = firma_id_map.get(firma_id, f"#{firma_id}")
        zahlung = zahlung_id_map.get(zahlung_id, f"#{zahlung_id}")
        tree.insert("", tk.END, iid=id_, values=(
            datum, f"{summe:.2f}", art, firma, zahlung, zahlungsart, bemerkung
        ))


# Funktion zum Leeren der Anzeige
def clear_tree():
    for row in tree.get_children():
        tree.delete(row)


# Funktion zum Löschen eines Eintrags
def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Auswahl fehlt", "Bitte wählen Sie einen Datensatz zum Löschen aus.")
        return

    confirm = messagebox.askyesno("Löschen bestätigen", "Möchten Sie den ausgewählten Datensatz wirklich löschen?")
    if confirm:
        for item in selected:
            cursor.execute("DELETE FROM tbl_einkauf WHERE id = ?", (item,))
        conn.commit()
        refresh()
        messagebox.showinfo("Erfolg", "Datensatz gelöscht.")


# Tkinter Fenster
root = tk.Tk()
root.title("Einkauf hinzufügen & verwalten")

# Eingabe-Formular
tk.Label(root, text="Einkaufsdatum:").grid(row=0, column=0, padx=10, pady=5)
calendar = Calendar(root, date_pattern='yyyy-mm-dd')
calendar.grid(row=0, column=1, padx=10, pady=5)
calendar.bind("<<CalendarSelected>>", lambda e: refresh())  # Automatisches Aktualisieren

tk.Label(root, text="Summe:").grid(row=1, column=0, padx=10, pady=5)
entry_summe = tk.Entry(root, width=40)
entry_summe.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Art:").grid(row=2, column=0, padx=10, pady=5)
e_art = ttk.Combobox(root, width=37, values=list(art_map.keys()))
e_art.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Firma:").grid(row=3, column=0, padx=10, pady=5)
e_firma = ttk.Combobox(root, width=37, values=list(firma_map.keys()))
e_firma.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Zahlung (Institut + Art):").grid(row=4, column=0, padx=10, pady=5)
e_zahlung = ttk.Combobox(root, width=37, values=list(zahlung_map.keys()))
e_zahlung.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Bemerkung:").grid(row=5, column=0, padx=10, pady=5)
entry_bemerkung = tk.Entry(root, width=40)
entry_bemerkung.grid(row=5, column=1, padx=10, pady=5)

tk.Button(root, text="Hinzufügen", command=insert_einkauf).grid(row=6, column=0, columnspan=2, pady=10)

# Trennlinie
ttk.Separator(root, orient='horizontal').grid(row=7, columnspan=2, sticky="ew", pady=10)

# Anzeige der Tabelle
tree = ttk.Treeview(root, columns=("Datum", "Summe", "Art", "Firma", "Zahlung", "Zahlungsart", "Bemerkung"),
                    show="headings", height=10)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Buttons unter der Tabelle
tk.Button(root, text="Ausgewählten Eintrag löschen", command=delete_selected).grid(row=9, column=0, pady=10)
tk.Button(root, text="Anzeige leeren", command=clear_tree).grid(row=9, column=1, pady=10)

# Starte mit Anzeige für heutiges Datum
refresh()

# Tkinter starten
root.mainloop()

# Verbindung schließen
conn.close()
