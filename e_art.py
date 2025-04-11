import sqlite3
import tkinter as tk
from tkinter import messagebox

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('/home/birgit/PycharmProjects/ProjektEinkauf/src/einkauf.db')
cursor = conn.cursor()

conn.commit()

# Funktion zum Einfügen von Daten in tbl_art mit Überprüfung
def insert_art():
    art = entry_art.get().strip()
    bemerkung = entry_bemerkung.get().strip()

    if not art:
        messagebox.showwarning("Eingabefehler", "Bitte füllen Sie das Feld 'Art' aus.")
        return

    art_lower = art.lower()

    # Alle existierenden Arten aus der Datenbank holen (lowercased)
    cursor.execute("SELECT art FROM tbl_art")
    existing_arten = [row[0] for row in cursor.fetchall()]
    existing_arten_lower = [f.lower() for f in existing_arten]

    # 1. Exakte Übereinstimmung prüfen
    if art_lower in existing_arten_lower:
        response = messagebox.askyesno("Doppelung erkannt",
            f"Die Art '{art}' existiert bereits.\nTrotzdem speichern?")
        if not response:
            return

    # 2. Teilstring-Prüfung
    matching_arten = [original for original in existing_arten
                      if original.lower() in art_lower or art_lower in original.lower()]

    if matching_arten:
        match_text = ', '.join(matching_arten)
        response = messagebox.askyesno("Teilstring erkannt",
            f"Ähnliche Art(en) gefunden:\n{match_text}\nTrotzdem speichern?")
        if not response:
            return

    # Datensatz speichern
    cursor.execute("INSERT INTO tbl_art (art, bemerkung) VALUES (?, ?)", (art, bemerkung))
    conn.commit()
    messagebox.showinfo("Erfolg", f"Die Art '{art}' wurde gespeichert.")

    # Eingabefelder leeren
    entry_art.delete(0, tk.END)
    entry_bemerkung.delete(0, tk.END)

# Funktion zum Anzeigen und Löschen von Arten
def show_art_liste():
    list_win = tk.Toplevel(root)
    list_win.title("Arten anzeigen und löschen")

    listbox = tk.Listbox(list_win, width=50)
    listbox.pack(padx=10, pady=10)

    # Funktion zum Aktualisieren der Listbox
    def refresh_listbox():
        if not list_win.winfo_exists():  # Überprüfen, ob das Fenster noch existiert
            return
        listbox.delete(0, tk.END)
        cursor.execute("SELECT id, art FROM tbl_art ORDER BY art")
        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    # Funktion zum Löschen der ausgewählten Art
    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte eine Art auswählen.", parent=list_win)
            return
        item = listbox.get(selection[0])
        art_id = int(item.split(" - ")[0])
        confirm = messagebox.askyesno(
            "Löschen bestätigen",
            "Soll die Art wirklich gelöscht werden?",
            parent=list_win  # Elternfenster setzen, damit es im Vordergrund bleibt
        )
        if confirm:
            cursor.execute("DELETE FROM tbl_art WHERE id = ?", (art_id,))
            conn.commit()
            refresh_listbox()

    btn_delete = tk.Button(list_win, text="Ausgewählte Art löschen", command=delete_selected)
    btn_delete.pack(pady=5)

    refresh_listbox()

# Hauptfenster
root = tk.Tk()
root.title("Artenverwaltung")

# Labels & Eingabefelder
label_art = tk.Label(root, text="Art:")
label_art.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entry_art = tk.Entry(root, width=40)
entry_art.grid(row=0, column=1, padx=10, pady=10)

label_bemerkung = tk.Label(root, text="Bemerkung:")
label_bemerkung.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_bemerkung = tk.Entry(root, width=40)
entry_bemerkung.grid(row=1, column=1, padx=10, pady=10)

# Buttons
button_add = tk.Button(root, text="Hinzufügen", command=insert_art)
button_add.grid(row=2, column=0, columnspan=2, pady=10)

button_show = tk.Button(root, text="Arten anzeigen & löschen", command=show_art_liste)
button_show.grid(row=3, column=0, columnspan=2, pady=5)

# Anwendung starten
root.mainloop()

# Verbindung schließen
conn.close()
