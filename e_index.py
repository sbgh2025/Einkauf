import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Setze das Arbeitsverzeichnis auf den Ordner, in dem sich strom_index.py befindet
script_dir = os.path.dirname(os.path.abspath(__file__))  # Speichert das Verzeichnis von strom_index.py


# Funktion zum Ausführen eines Python-Skripts
def run_script(script_name):
    try:
        # Setze den vollständigen Pfad zum Skript, das ausgeführt werden soll
        script_path = os.path.join(script_dir, script_name)

        # subprocess.run wird verwendet, um das Python-Skript auszuführen
        subprocess.run(["python3", script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fehler", f"Das Skript {script_name} konnte nicht ausgeführt werden.")
    except FileNotFoundError:
        messagebox.showerror("Fehler", f"Das Skript {script_name} wurde nicht gefunden.")


# Tkinter GUI-Klasse
class IndexApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Fenster konfigurieren
        self.title("Index für Python-Programme")
        self.geometry("500x500")

        # Layout
        self.layout = tk.Frame(self)
        self.layout.pack(padx=20, pady=20)

        # Überschrift
        self.title_label = tk.Label(self.layout, text="Wählen Sie ein Programm aus:", font=("Arial", 14))
        self.title_label.pack(pady=10)

        # Button für "Einkauf eintragen"
        self.button_einkauf = tk.Button(self.layout, text="Einkauf eintragen",
                                        command=lambda: run_script("e_einkauf.py"),
                                        bg="lightblue", font=("Arial", 12))
        self.button_einkauf.pack(pady=10, fill=tk.X)

        # Button für "Summe bilden"
        self.button_summe = tk.Button(self.layout, text="Summe bilden",
                                      command=lambda: run_script("e_summe.py"),
                                      bg="lightblue", font=("Arial", 12))
        self.button_summe.pack(pady=10, fill=tk.X)

        # Button für "Art eintragen"
        self.button_art = tk.Button(self.layout, text="Art eintragen", command=lambda: run_script("e_art.py"),
                                    bg="lightblue", font=("Arial", 12))
        self.button_art.pack(pady=10, fill=tk.X)

        # Button für "Firma eintragen"
        self.button_firma = tk.Button(self.layout, text="Firma eintragen", command=lambda: run_script("e_firma.py"),
                                      bg="lightblue", font=("Arial", 12))
        self.button_firma.pack(pady=10, fill=tk.X)

        # Button für "Zahlungsart eintragen"
        self.button_zahlungsart = tk.Button(self.layout, text="Zahlungsart eintragen", command=lambda: run_script("e_zahlungsart.py"),
                                            bg="lightblue", font=("Arial", 12))
        self.button_zahlungsart.pack(pady=10, fill=tk.X)

        # Button für "Datenbank"
        self.button_db = tk.Button(self.layout, text="Datenbank", command=lambda: run_script("e_db.py"),
                                   bg="lightblue", font=("Arial", 12))
        self.button_db.pack(pady=10, fill=tk.X)


if __name__ == "__main__":
    app = IndexApp()
    app.mainloop()
