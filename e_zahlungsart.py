import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('/home/birgit/PycharmProjects/ProjektEinkauf/src/einkauf.db')
cursor = conn.cursor()

conn.commit()

# Funktion zum Einfügen von Daten in tbl_zahlung mit Überprüfung
def insert_zahlung():
    institut = entry_institut.get().strip()
    zahlungsart = combo_zahlungsart.get().strip()
    bemerkung = entry_bemerkung.get().strip()

    if not institut:
        messagebox.showwarning("Eingabefehler", "Bitte füllen Sie das Feld 'Institut' aus.")
        return
    if not zahlungsart:
        messagebox.showwarning("Eingabefehler", "Bitte wählen Sie eine Zahlungsart aus.")
        return

    # Exakte und ähnliche Einträge prüfen
    cursor.execute("SELECT institut FROM tbl_zahlung")
    existing_institute = [row[0] for row in cursor.fetchall()]
    existing_institute_lower = [f.lower() for f in existing_institute]
    institut_lower = institut.lower()

    if institut_lower in existing_institute_lower:
        response = messagebox.askyesno("Doppelung erkannt",
            f"Das Institut '{institut}' existiert bereits.\nTrotzdem speichern?")
        if not response:
            return

    matching_institute = [original for original in existing_institute
                          if original.lower() in institut_lower or institut_lower in original.lower()]

    if matching_institute:
        match_text = ', '.join(matching_institute)
        response = messagebox.askyesno("Teilstring erkannt",
            f"Ähnliches Institut gefunden:\n{match_text}\nTrotzdem speichern?")
        if not response:
            return

    # Datensatz speichern
    cursor.execute("INSERT INTO tbl_zahlung (institut, zahlungsart, bemerkung) VALUES ( ?, ?,?)",
                   (institut, zahlungsart, bemerkung))
    conn.commit()
    messagebox.showinfo("Erfolg", f"Die Zahlung mit Institut '{institut}' wurde gespeichert.")

    # Felder zurücksetzen
    entry_institut.delete(0, tk.END)
    entry_bemerkung.delete(0, tk.END)
    combo_zahlungsart.set("")

# Funktion zum Anzeigen und Löschen von Einträgen
def show_zahlung_liste():
    list_win = tk.Toplevel(root)
    list_win.title("Zahlungsinstitute anzeigen und löschen")

    listbox = tk.Listbox(list_win, width=60)
    listbox.pack(padx=10, pady=10)

    def refresh_listbox():
        listbox.delete(0, tk.END)

        cursor.execute("SELECT institut, zahlungsart, bemerkung FROM tbl_zahlung")

        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]})")

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte einen Eintrag auswählen.", parent=list_win)
            return
        item = listbox.get(selection[0])
        institut_name = item.split(" - ")[0]
        confirm = messagebox.askyesno(
            "Löschen bestätigen",
            f"Soll der Eintrag '{institut_name}' wirklich gelöscht werden?",
            parent=list_win
        )
        if confirm:
            cursor.execute("DELETE FROM tbl_zahlung WHERE institut = ?", (institut_name,))
            conn.commit()
            refresh_listbox()

    btn_delete = tk.Button(list_win, text="Ausgewählten Eintrag löschen", command=delete_selected)
    btn_delete.pack(pady=5)

    refresh_listbox()

# Hauptfenster
root = tk.Tk()
root.title("Zahlung")

# Labels & Eingabefelder
label_institut = tk.Label(root, text="Institut:")
label_institut.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entry_institut = tk.Entry(root, width=40)
entry_institut.grid(row=0, column=1, padx=10, pady=10)

label_zahlungsart = tk.Label(root, text="Zahlungsart:")
label_zahlungsart.grid(row=1, column=0, padx=10, pady=10, sticky="e")

combo_zahlungsart = ttk.Combobox(root, values=["Kreditkarte", "Girokarte","Überweisung", "Einzug", "Forderung","Bar"], state="readonly", width=37)
combo_zahlungsart.grid(row=1, column=1, padx=10, pady=10)

label_bemerkung = tk.Label(root, text="Bemerkung:")
label_bemerkung.grid(row=2, column=0, padx=10, pady=10, sticky="e")

entry_bemerkung = tk.Entry(root, width=40)
entry_bemerkung.grid(row=2, column=1, padx=10, pady=10)

# Buttons
button_add = tk.Button(root, text="Hinzufügen", command=insert_zahlung)
button_add.grid(row=3, column=0, columnspan=2, pady=10)

button_show = tk.Button(root, text="Zahlungen anzeigen & löschen", command=show_zahlung_liste)
button_show.grid(row=4, column=0, columnspan=2, pady=5)

# Anwendung starten
root.mainloop()

# Verbindung schließen
conn.close()
