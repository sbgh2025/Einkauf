import sqlite3
import tkinter as tk
from tkinter import messagebox

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('/home/birgit/PycharmProjects/ProjektEinkauf/src/einkauf.db')
cursor = conn.cursor()

conn.commit()

# Funktion zum Einfügen von Daten in tbl_firma mit Überprüfung
def insert_firma():
    firma = entry_firma.get().strip()
    bemerkung = entry_bemerkung.get().strip()

    if not firma:
        messagebox.showwarning("Eingabefehler", "Bitte füllen Sie das Feld 'Firma' aus.")
        return

    firma_lower = firma.lower()

    # Alle existierenden Firmennamen aus der Datenbank holen (lowercased)
    cursor.execute("SELECT firma FROM tbl_firma")
    existing_firmen = [row[0] for row in cursor.fetchall()]
    existing_firmen_lower = [f.lower() for f in existing_firmen]

    # 1. Exakte Übereinstimmung prüfen
    if firma_lower in existing_firmen_lower:
        response = messagebox.askyesno("Doppelung erkannt",
            f"Die Firma '{firma}' existiert bereits.\nTrotzdem speichern?")
        if not response:
            return

    # 2. Teilstring-Prüfung
    matching_firmen = [original for original in existing_firmen
                       if original.lower() in firma_lower or firma_lower in original.lower()]

    if matching_firmen:
        match_text = ', '.join(matching_firmen)
        response = messagebox.askyesno("Teilstring erkannt",
            f"Ähnliche Firma(n) gefunden:\n{match_text}\nTrotzdem speichern?")
        if not response:
            return

    # Datensatz speichern
    cursor.execute("INSERT INTO tbl_firma (firma, bemerkung) VALUES (?, ?)", (firma, bemerkung))
    conn.commit()
    messagebox.showinfo("Erfolg", f"Die Firma '{firma}' wurde gespeichert.")

    # Eingabefelder leeren
    entry_firma.delete(0, tk.END)
    entry_bemerkung.delete(0, tk.END)

# Funktion zum Anzeigen und Löschen von Firmen
def show_firmenliste():
    list_win = tk.Toplevel(root)
    list_win.title("Firmen anzeigen und löschen")

    listbox = tk.Listbox(list_win, width=50)
    listbox.pack(padx=10, pady=10)

    # Funktion zum Aktualisieren der Listbox
    def refresh_listbox():
        if not list_win.winfo_exists():  # Überprüfen, ob das Fenster noch existiert
            return
        listbox.delete(0, tk.END)
        cursor.execute("SELECT id, firma FROM tbl_firma ORDER BY firma")
        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    # Funktion zum Löschen der ausgewählten Firma
    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte eine Firma auswählen.", parent=list_win)
            return
        item = listbox.get(selection[0])
        firma_id = int(item.split(" - ")[0])
        confirm = messagebox.askyesno(
            "Löschen bestätigen",
            "Soll die Firma wirklich gelöscht werden?",
            parent=list_win  # Elternfenster setzen, damit es im Vordergrund bleibt
        )
        if confirm:
            cursor.execute("DELETE FROM tbl_firma WHERE id = ?", (firma_id,))
            conn.commit()
            refresh_listbox()

    btn_delete = tk.Button(list_win, text="Ausgewählte Firma löschen", command=delete_selected)
    btn_delete.pack(pady=5)

    refresh_listbox()

# Hauptfenster
root = tk.Tk()
root.title("Firmenverwaltung")

# Labels & Eingabefelder
label_firma = tk.Label(root, text="Firmenname:")
label_firma.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entry_firma = tk.Entry(root, width=40)
entry_firma.grid(row=0, column=1, padx=10, pady=10)

label_bemerkung = tk.Label(root, text="Bemerkung:")
label_bemerkung.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_bemerkung = tk.Entry(root, width=40)
entry_bemerkung.grid(row=1, column=1, padx=10, pady=10)

# Buttons
button_add = tk.Button(root, text="Hinzufügen", command=insert_firma)
button_add.grid(row=2, column=0, columnspan=2, pady=10)

button_show = tk.Button(root, text="Firmen anzeigen & löschen", command=show_firmenliste)
button_show.grid(row=3, column=0, columnspan=2, pady=5)

# Anwendung starten
root.mainloop()

# Verbindung schließen
conn.close()
