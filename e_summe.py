import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd

# DB-Verbindung
conn = sqlite3.connect("einkauf.db")
cursor = conn.cursor()

# Tkinter Fenster
root = tk.Tk()
root.title("Summenberechnung mit Filtern")
root.geometry("900x650")

# ==== Titel ====
tk.Label(root, text="Einkaufs-Summe berechnen", font=("Arial", 16, "bold")).pack(pady=15)

# ==== Filter Frame ====
frame = tk.Frame(root)
frame.pack(pady=10)

# Datum
tk.Label(frame, text="Von:").grid(row=0, column=0, padx=5)
start_date = DateEntry(frame, date_pattern='yyyy-mm-dd')
start_date.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Bis:").grid(row=0, column=2, padx=5)
end_date = DateEntry(frame, date_pattern='yyyy-mm-dd')
end_date.grid(row=0, column=3, padx=5)

# Art
tk.Label(frame, text="Art:").grid(row=1, column=0, padx=5, pady=10)
art_cb = ttk.Combobox(frame, width=25)
cursor.execute("SELECT id, art FROM tbl_art")
arten = cursor.fetchall()
art_cb['values'] = ["Gesamt"] + [a[1] for a in arten]
art_cb.set("Gesamt")
art_cb.grid(row=1, column=1)

# Firma
tk.Label(frame, text="Firma:").grid(row=1, column=2, padx=5)
firma_cb = ttk.Combobox(frame, width=25)
cursor.execute("SELECT id, firma FROM tbl_firma")
firmen = cursor.fetchall()
firma_cb['values'] = ["Gesamt"] + [f[1] for f in firmen]
firma_cb.set("Gesamt")
firma_cb.grid(row=1, column=3)

# Zahlungsmittel
tk.Label(frame, text="Zahlungsart:").grid(row=2, column=0, padx=5)
zahlung_cb = ttk.Combobox(frame, width=25)
cursor.execute("SELECT DISTINCT zahlungsart FROM tbl_zahlung")
zahlungen = cursor.fetchall()
zahlung_cb['values'] = ["Gesamt"] + [z[0].strip() for z in zahlungen]
zahlung_cb.set("Gesamt")
zahlung_cb.grid(row=2, column=1)

# Institut
tk.Label(frame, text="Institut:").grid(row=2, column=2, padx=5)
institut_cb = ttk.Combobox(frame, width=25)
cursor.execute("SELECT DISTINCT institut FROM tbl_zahlung WHERE institut IS NOT NULL AND institut != ''")
institute = cursor.fetchall()
institut_cb['values'] = ["Gesamt"] + [i[0] for i in institute]
institut_cb.set("Gesamt")
institut_cb.grid(row=2, column=3)

# ==== Ergebnisanzeige ====
label_result = tk.Label(root, text="Gesamtsumme: 0.00 €", font=("Arial", 14))
label_result.pack(pady=20)

# ==== Treeview für Ergebnisanzeige ====
tree_frame = tk.Frame(root)
tree_frame.pack()

columns = ("Summe", "Datum", "Art", "Firma", "Zahlungsart", "Institut")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

# globale Variable zur Speicherung der aktuellen Auswahl
aktuelle_df = pd.DataFrame()

# ==== Funktion: Filter anwenden ====
def berechne_summe():
    global aktuelle_df
    tree.delete(*tree.get_children())

    von = start_date.get()
    bis = end_date.get()
    art = art_cb.get()
    firma = firma_cb.get()
    zahlung = zahlung_cb.get()
    institut = institut_cb.get()

    query = """
        SELECT e.e_summe, e.e_datum, a.art, f.firma, z.zahlungsart, z.institut
        FROM tbl_einkauf e
        JOIN tbl_art a ON e.e_art = a.id
        JOIN tbl_firma f ON e.e_firma = f.id
        JOIN tbl_zahlung z ON e.e_zahlung = z.id
        WHERE e.e_datum BETWEEN ? AND ?
    """
    params = [von, bis]

    if art != "Gesamt":
        query += " AND a.art = ?"
        params.append(art)
    if firma != "Gesamt":
        query += " AND f.firma = ?"
        params.append(firma)
    if zahlung != "Gesamt":
        query += " AND z.zahlungsart = ?"
        params.append(zahlung)
    if institut != "Gesamt":
        query += " AND z.institut = ?"
        params.append(institut)

    cursor.execute(query, params)
    result = cursor.fetchall()

    if not result:
        messagebox.showwarning("Keine Daten", "Keine passenden Einkäufe gefunden.")
        aktuelle_df = pd.DataFrame()
        label_result.config(text="Gesamtsumme: 0.00 €")
        return

    summe = sum([r[0] for r in result])
    label_result.config(text=f"Gesamtsumme: {summe:.2f} €")

    for row in result:
        tree.insert("", tk.END, values=row)

    aktuelle_df = pd.DataFrame(result, columns=columns)

# ==== Exportfunktion ====
def export_to_excel():
    if aktuelle_df.empty:
        messagebox.showwarning("Keine Daten", "Bitte zuerst eine Auswahl berechnen.")
        return
    try:
        file = "Einkauf_Export.xlsx"
        aktuelle_df.to_excel(file, sheet_name="Auswahl", index=False)
        messagebox.showinfo("Export erfolgreich", f"Daten wurden exportiert nach:\n{file}")
    except Exception as e:
        messagebox.showerror("Fehler beim Export", str(e))

# ==== Buttons ====
tk.Button(root, text="Summe berechnen", command=berechne_summe, font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Export nach Excel", command=export_to_excel, font=("Arial", 12)).pack(pady=5)

# Tkinter starten
root.mainloop()
conn.close()
