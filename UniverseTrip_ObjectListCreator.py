# install astropy:
# pip install astropy

import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

# Mapping-Tabelle für Objekttypen
otype_mapping = {
    "*": "Star",
    "Ma*": "Star",
    "Ma?": "Star",
    "bC*": "Star",
    "bC?": "Star",
    "sg*": "Star",
    "sg?": "Star",
    "s*r": "Star",
    "s?r": "Star",
    "s*y": "Star",
    "s?y": "Star",
    "s*b": "Star",
    "s?b": "Star",
    "WR*": "Star",
    "WR?": "Star",
    "N*": "Star",
    "N*?": "Star",
    "Psr": "Star",
    "Y*O": "Star",
    "Y*?": "Star",
    "Or*": "Star",
    "TT*": "Star",
    "TT?": "Star",
    "Ae*": "Star",
    "Ae?": "Star",
    "out": "Star",
    "of?": "Star",
    "HH": "Star",
    "MS*": "Star",
    "MS?": "Star",
    "Be*": "Star",
    "Be?": "Star",
    "BS*": "Star",
    "BS?": "Star",
    "SX*": "Star",
    "gD*": "Star",
    "dS*": "Star",
    "Ev*": "Star",
    "Ev?": "Star",
    "RG*": "Star",
    "RB?": "Star",
    "HS*": "Star",
    "HS?": "Star",
    "HB*": "Star",
    "HB?": "Star",
    "RR*": "Star",
    "RR?": "Star",
    "WV*": "Star",
    "WV?": "Star",
    "Ce*": "Star",
    "Ce?": "Star",
    "cC*": "Star",
    "C*": "Star",
    "C*?": "Star",
    "S*": "Star",
    "S*?": "Star",
    "LP*": "Star",
    "LP?": "Star",
    "AB*": "Star",
    "AB?": "Star",
    "Mi*": "Star",
    "Mi?": "Star",
    "OH*": "Star",
    "OH?": "Star",
    "pA*": "Star",
    "pA?": "Star",
    "RV*": "Star",
    "RV?": "Star",
    "PN": "PN",
    "PN?": "PN",
    "WD*": "Star",
    "WD?": "Star",
    "Pe*": "Star",
    "Pe?": "Star",
    "a2*": "Star",
    "a2?": "Star",
    "RC*": "Star",
    "RC?": "Star",
    "**": "Star",
    "**?": "Star",
    "EB*": "Star",
    "EB?": "Star",
    "El*": "Star",
    "El?": "Star",
    "SB*": "Star",
    "SB?": "Star",
    "RS*": "Star",
    "RS?": "Star",
    "BY*": "Star",
    "BY?": "Star",
    "Sy*": "Star",
    "Sy?": "Star",
    "XB*": "Star",
    "XB?": "Star",
    "LXB": "Star",
    "LX?": "Star",
    "HXB": "Star",
    "HX?": "Star",
    "CV*": "Star",
    "CV?": "Star",
    "No*": "Star",
    "No?": "Star",
    "SN*": "Star",
    "SN?": "Star",
    "LM*": "Star",
    "LM?": "Star",
    "BD*": "Star",
    "BD?": "Star",
    "Pl": "Star",
    "Pl?": "Star",
    "V*": "Star",
    "V*?": "Star",
    "Ir*": "Star",
    "Er*": "Star",
    "Er?": "Star",
    "Ro*": "Star",
    "Ro?": "Star",
    "Pu*": "Star",
    "Pu?": "Star",
    "Em*": "Star",
    "PM*": "Star",
    "HV*": "Star",
    "Cl*": "OS",
    "Cl?": "OS",
    "GlC": "KS",
    "Gl?": "KS",
    "OpC": "OS",
    "As*": "OS",
    "As?": "OS",
    "St*": "OS",
    "MGr": "OS",
    "ISM": "GN",
    "SFR": "GN",
    "HII": "GN",
    "Cld": "GN",
    "GNe": "GN",
    "RNe": "GN",
    "MoC": "GN",
    "DNe": "GN",
    "glb": "GN",
    "CGb": "GN",
    "HVC": "GN",
    "cor": "GN",
    "bub": "GN",
    "SNR": "PN",
    "SR?": "PN",
    "sh": "GN",
    "flt": "GN",
    "G": "GX",
    "G?": "GX",
    "LSB": "GX",
    "bCG": "GX",
    "SBG": "GX",
    "H2G": "GX",
    "EmG": "GX",
    "AGN": "GX",
    "AG?": "GX",
    "SyG": "GX",
    "Sy1": "GX",
    "Sy2": "GX",
    "rG": "GX",
    "LIN": "GX",
    "QSO": "GX",
    "Q?": "GX",
    "Bla": "GX",
    "Bz?": "GX",
    "BLL": "GX",
    "BL?": "GX",
    "GiP": "GX",
    "GiG": "GX",
    "GiC": "GX",
    "BiC": "GX",
    "IG": "GX",
    "PaG": "GX",
    "AG?": "GX",
    "GrG": "GX",
    "Gr?": "GX",
    "CGG": "GX",
    "ClG": "GX",
    "C?G": "GX",
    "PCG": "GX",
    "PCG?": "GX",
    "SCG": "GX",
    "SC?": "GX",
    "vid": "GX",
    "grv": "undefined",
    "Lev": "undefined",
    "gLS": "undefined",
    "LS?": "undefined",
    "gLe": "undefined",
    "Le?": "undefined",
    "LeI": "undefined",
    "LI?": "undefined",
    "LeG": "undefined",
    "LeQ": "undefined",
    "BH": "undefined",
    "BH?": "undefined",
    "GWE": "undefined",
    "ev": "undefined",
    "var": "undefined",
    "Rad": "undefined",
    "mR": "undefined",
    "cm": "undefined",
    "mm": "undefined",
    "smm": "undefined",
    "HI": "undefined",
    "rB": "undefined",
    "Mas": "undefined",
    "IR": "undefined",
    "FIR": "undefined",
    "MIR": "undefined",
    "NIR": "undefined",
    "Opt": "undefined",
    "EmO": "undefined",
    "blu": "undefined",
    "UV": "undefined",
    "X": "undefined",
    "ULX": "undefined",
    "UX?": "undefined",
    "gam": "undefined",
    "gB": "undefined",
    "mul": "undefined",
    "err": "undefined",
    "PoC": "undefined",
    "PoG": "undefined",
    "?": "undefined",
    "reg": "undefined",
    0: "undefined"
}

# Mapping für lesbare Namen
otype_display_names = {
    "KS": "Kugelsternhaufen",
    "OS": "Offener Sternhaufen",
    "undefined": "Undefinierte Objekte",
    "GN": "Galaktische Nebel",
    "PN": "Planetarische Nebel",
    "Star": "Sterne",
    "GX": "Galaxien"
}

# Liste der verfügbaren Objekttypen
available_types = list(set(otype_mapping.values()))

def select_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("Excel-Dateien", "*.xlsx")]))
    if not file_path.get():
        file_path.set("Keine Datei ausgewählt")

# Funktion zur Verarbeitung der Datei basierend auf der Auswahl
def process_file():
    try:
        min_v = float(entry_min_v.get())
        max_v = float(entry_max_v.get())
        min_dist = float(entry_min_dist.get())
        max_dist = float(entry_max_dist.get())
    except ValueError:
        messagebox.showerror("Fehler", "Bitte gültige Zahlen für die Helligkeit und Entfernung eingeben! Kommazeichen ist '.' (Punkt).")
        return

    output_filename = entry_filename.get().strip()
    if not output_filename:
        messagebox.showerror("Fehler", "Bitte einen gültigen Dateinamen eingeben!")
        return
    if not output_filename.endswith(".csv"):
        output_filename += ".csv"

    selected_types = [otype for otype, var in checkboxes.items() if var.get()]
    if not selected_types:
        messagebox.showwarning("Warnung", "Bitte mindestens einen Objekttyp auswählen!")
        return

    #file_path = "NGC_Objects.xlsx"  # Datei wird durch GUI ausgewählt
    df = pd.read_excel(file_path.get(), sheet_name="Consolidation")

    # RA und DEC in galaktische Koordinaten umrechnen
    coords = SkyCoord(ra=df["ra"].values * u.deg, dec=df["dec"].values * u.deg, frame="icrs")
    galactic_coords = coords.galactic

    # Neue Spalten mit umgerechneten Werten
    df["galaktische länge"] = galactic_coords.l.deg
    df["galaktische breite"] = galactic_coords.b.deg

    # Objekttypen umbenennen und nach Auswahl filtern
    df["otype"] = df["otype"].replace(otype_mapping)
    df = df[df["otype"].isin(selected_types)]

    # Filter nach Helligkeit (V-Wert)
    df = df[(df["V"] >= min_v) & (df["V"] <= max_v)]

    # Filter nach Entfernung (distLj_mean), 0.0 wird ausgeschlossen
    df = df[(df["distLj_mean"] >= 0.0) & (df["distLj_mean"] >= min_dist) & (df["distLj_mean"] <= max_dist)]

    if exclude_zero_distance_var.get():
        df = df[df["distLj_mean"] > 0.0]  # Entfernt Objekte mit Distance = 0.0
    
    if filter_stars_var.get():
        df = df[~df["id"].astype(str).str.contains(r"\S+\s+\S+\s+\S+")]  # Erkennung von IDs mit zwei nicht direkt aufeinanderfolgenden Leerzeichen

    # Relevante Spalten für die CSV-Ausgabe auswählen
    output_df = df[["id", "galaktische länge", "galaktische breite", "distLj_mean", "V", "otype"]]
    output_df.columns = ["object_name", "galactic_l_deg", "galactic_b_deg", "distance_to_sun_Lj", "brightness_mag", "object_type"]

    # Als CSV speichern
    output_df.to_csv(output_filename, index=False, encoding="utf-8")
    messagebox.showinfo("Erfolg", f"Die Datei {output_filename} wurde erfolgreich erstellt!")


"""
*************************************************
GUI erstellen
*************************************************
"""

root = tk.Tk()
root.title("UniverseTrip - Object list creator")
root.iconbitmap("favicon.ico")
root.geometry("500x800")   # Größeres Fenster

# --- Fenster zentrieren ---
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"+{x}+{y}")

# PNG-Bild laden
image = Image.open("Logo_small.png")
image = image.resize((60, 60)) # Größe anpassen
photo = ImageTk.PhotoImage(image)

# --- Modernes Styling ---
root.tk_setPalette(background="#2b2b2b", foreground="white")  # Dunkles Theme
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6, relief="flat", background="#4CAF50", foreground="white")
style.configure("TLabel", font=("Arial", 11), background="#2b2b2b", foreground="white")
style.configure("TCheckbutton", font=("Arial", 11), background="#2b2b2b", foreground="white")
style.map("TCheckbutton",
      background=[("active", "#3a3a3a"), ("!active", "#2b2b2b")],
      indicatorcolor=[("selected", "#4CAF50"), ("!selected", "#aaaaaa")],
      foreground=[("selected", "white"), ("!selected", "#aaaaaa")])

frame = ttk.Frame(root)

# ---------- Header ----------
header = tk.Label(root, text="UniverseTrip\nObject list creator",image=photo, compound="left", padx= 13, justify="left", font=("Arial", 20, "bold"), anchor="w")
header.image = photo
header.pack(fill="x", padx=10, pady=10)


# ---------- Dateiauswahl ----------
file_frame = tk.LabelFrame(root, text="1. Datendatei auswählen", padx=10, pady=10)
file_frame.pack(fill="x", padx=20, pady=5)

file_path = tk.StringVar(value="Keine Datei ausgewählt")
tk.Label(file_frame, textvariable=file_path, wraplength=420, height=3, justify="left").pack(anchor="w")
tk.Button(file_frame, text="Datendatei auswählen", font=("Arial", 12, "bold"), command=select_file).pack(anchor="e", pady=5)

# ---------- Checkboxen ----------
options_frame = tk.LabelFrame(root, text="2. Darzustellende Objekte wählen", padx=10, pady=10)
options_frame.pack(fill="x", padx=20, pady=5)

checkboxes = {}
for otype in available_types:
    display_name = otype_display_names.get(otype, otype)  # Falls kein Mapping vorhanden, Originalname behalten
    var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(options_frame, text=display_name, variable=var)
    chk.pack(anchor="w")
    checkboxes[otype] = var

#Checkbox für Distance 0 ausblenden
exclude_zero_distance_var = tk.BooleanVar(value=False)
chk_exclude_zero_distance = ttk.Checkbutton(options_frame, text="Objekte mit Entfernung = 0 ausblenden", variable=exclude_zero_distance_var)
chk_exclude_zero_distance.pack(anchor="w")

# Checkbox für das Filtern einzelner Sterne aus Sternhaufen
filter_stars_var = tk.BooleanVar(value=False)
chk_filter_stars = ttk.Checkbutton(options_frame, text="Einzelne Sterne aus Sternhaufen entfernen", variable=filter_stars_var)
chk_filter_stars.pack(anchor="w")

# ---------- Datenwerte ----------
minmax_frame = tk.LabelFrame(root, text="3. Minimale und Maximale Datenwerte für darzustellende Objekte auswählen", padx=10, pady=10)
minmax_frame.pack(fill="x", padx=20, pady=5)

# Neuen Frame für Grid-Anordnung erstellen
values_frame = tk.Frame(minmax_frame, bg="#2b2b2b")
values_frame.pack(fill="x", padx=0, pady=0)

# Eingabefelder für Helligkeitsbereich
ttk.Label(values_frame, text="Minimale Helligkeit:").grid(row=0, column=0, sticky="w", padx=0, pady=0)
entry_max_v = ttk.Entry(values_frame, justify="right")
entry_max_v.grid(row=0, column=1, sticky="e", padx=0, pady=0)
entry_max_v.insert(0, "25")  # Standardwert
ttk.Label(values_frame, text="mag").grid(row=0, column=3, sticky="w", padx=5, pady=0)

ttk.Label(values_frame, text="Maximale Helligkeit:").grid(row=1, column=0, sticky="w", padx=0, pady=0)
entry_min_v = ttk.Entry(values_frame, justify="right")
entry_min_v.grid(row=1, column=1, sticky="e", padx=0, pady=0)
entry_min_v.insert(0, "-2.0")  # Standardwert
ttk.Label(values_frame, text="mag").grid(row=1, column=3, sticky="w", padx=5, pady=0)



#Leerzeile
ttk.Label(values_frame, text="", background="#2b2b2b").grid(row=2, column=0, columnspan=2, pady=5)

# Eingabefelder für Entfernungsbereich
ttk.Label(values_frame, text="Minimale Entfernung:").grid(row=3, column=0, sticky="w", padx=0, pady=0)
entry_min_dist = ttk.Entry(values_frame, justify="right")
entry_min_dist.grid(row=3, column=1, sticky="e", padx=0, pady=0)
entry_min_dist.insert(0, "0.0")  # Standardwert
ttk.Label(values_frame, text="Lichtjahre").grid(row=3, column=3, sticky="w", padx=5, pady=0)

ttk.Label(values_frame, text="Maximale Entfernung:").grid(row=4, column=0, sticky="w", padx=0, pady=0)
entry_max_dist = ttk.Entry(values_frame, justify="right")
entry_max_dist.grid(row=4, column=1, sticky="e", padx=0, pady=0)
entry_max_dist.insert(0, "1000000000")  # Standardwert
ttk.Label(values_frame, text="Lichtjahre").grid(row=4, column=3, sticky="w", padx=5, pady=0)

start_frame = tk.LabelFrame(root, text="3. Datendatei erstellen", padx=10, pady=10)
start_frame.pack(fill="x", padx=20, pady=10)

# Neuen Frame für Grid-Anordnung erstellen
startvalues_frame = tk.Frame(start_frame, bg="#2b2b2b")
startvalues_frame.pack(fill="x", padx=0, pady=0)

# Eingabefeld für den Dateinamen
ttk.Label(startvalues_frame, text="Dateiname für die Ausgabe (CSV):").grid(row=0, column=0, sticky="w", padx=0, pady=0)
entry_filename = ttk.Entry(startvalues_frame)
entry_filename.grid(row=0, column=1, sticky="e", padx=0, pady=0)
entry_filename.insert(0, "objects_x.csv")  # Standardwert

tk.Button(start_frame, text="Datei erstellen", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=process_file).pack(anchor="e", pady=10)

root.mainloop()
