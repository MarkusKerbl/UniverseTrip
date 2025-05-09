import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

# Mapping table for object types
otype_mapping = {
    "Satelite": "Satelite",
    "Planet": "Planet",
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
    "IG": "PaG",
    "PaG": "PaG",
    "GrG": "GrG",
    "Gr?": "GrG",
    "CGG": "GrG",
    "ClG": "ClG",
    "C?G": "ClG",
    "PCG": "ClG",
    "PCG?": "ClG",
    "SCG": "SCG",
    "SC?": "SCG",
    "vid": "void",
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

# Mapping for real object types to display names, these names are used in the GUI
otype_display_names = {
    "KS": "Globular clusters",
    "OS": "Open star cluster",
    "undefined": "Undefined objects",
    "GN": "galactic nebulae",
    "PN": "Planetary nebulae",
    "Star": "Stars",
    "GX": "Galaxies",
    "SCG": "Galaxy Super Cluster",
    "GrG": "Galaxy groups",
    "ClG": "Galaxy clusters",
    "PaG": "Pairs of galaxies",
    "Satelite": "Satellites",
    "Planet": "Planets",
    "void": "Void"
}

# List of the available object types
available_types = list(set(otype_mapping.values()))

def select_file():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    
    if not path:
        file_path.set("No file selected.")
        #messagebox.showerror("Fehler", "Bitte einen gültigen Dateinamen auswählen!")
        return

    file_path.set(path)
    selected_option.set("manual")  # Markiere die manuelle Auswahl

def update_file_path():
    if selected_option.get() != "manual":
        file_path.set(standard_files[selected_option.get()])

# Function to process the file and create the output CSV
def process_file():
    try:
        min_v = float(entry_min_v.get())
        max_v = float(entry_max_v.get())
        min_dist = float(entry_min_dist.get())
        max_dist = float(entry_max_dist.get())
    except ValueError:
        messagebox.showerror("Error", "Please use a valid number for brightness and distance! Comma symbol is '.' (point).")
        return

    output_filename = entry_filename.get().strip()
    if not output_filename:
        messagebox.showerror("Error", "Please select a valid filename!")
        return
    if not output_filename.endswith(".csv"):
        output_filename += ".csv"

    selected_types = [otype for otype, var in checkboxes.items() if var.get()]
    if not selected_types:
        messagebox.showwarning("Warning", "Bitte mindestens einen Objekttyp auswählen!")
        return

    #file_path = "NGC_Objects.xlsx"  # Datei wird durch GUI ausgewählt
    try:
        df = pd.read_excel(file_path.get(), sheet_name="Consolidation")
    except FileNotFoundError:
        messagebox.showerror("Error", "No file found.")
        return
    except ValueError:
        # Wenn das Arbeitsblatt nicht gefunden wird, eine Fehlermeldung anzeigen
        messagebox.showerror("Error", "The worksheet 'Consolidation' is not available in the file.")
        return


    # convert RA and Dec to Galactic coordinates
    coords = SkyCoord(ra=df["ra"].values * u.deg, dec=df["dec"].values * u.deg, frame="icrs")
    galactic_coords = coords.galactic

    # New columns with galactic coordinates
    df["galactic_l"] = galactic_coords.l.deg
    df["galactic_b"] = galactic_coords.b.deg

    # Replace object types with names which are needed for the UniverseTrip app
    df["otype"] = df["otype"].replace(otype_mapping)
    df = df[df["otype"].isin(selected_types)]
    # Filter by brightness
    df = df[(df["V"] >= min_v) & (df["V"] <= max_v)]

    # Filter by distance
    df = df[(df["distLj_mean"] >= 0.0) & (df["distLj_mean"] >= min_dist) & (df["distLj_mean"] <= max_dist)]

    # In case of distance = 0.0 and option is enabled, remove the object from the list
    if exclude_zero_distance_var.get():
        df = df[df["distLj_mean"] > 0.0]  # Entfernt Objekte mit Distance = 0.0
    
    # Optional: Filter out stars from star clusters by checking for two spaces in the Name
    #if filter_stars_var.get():
    #    df = df[~df["id"].astype(str).str.contains(r"\S+\s+\S+\s+\S+")]  # Erkennung von IDs mit zwei nicht direkt aufeinanderfolgenden Leerzeichen

    # Define the columns for the output file
    output_df = df[["id", "galactic_l", "galactic_b", "distLj_mean", "V", "otype"]]
    output_df.columns = ["object_name", "galactic_l_deg", "galactic_b_deg", "distance_to_sun_Lj", "brightness_mag", "object_type"]

    # Save as .csv file
    output_df.to_csv(output_filename, index=False, encoding="utf-8")
    messagebox.showinfo("Success", f"The file {output_filename} was successfully created!")



#*************************************************
# GUI erstellen
#*************************************************

root = tk.Tk()
root.title("UniverseTrip - Object list creator")
root.iconbitmap("app_data/favicon.ico")
root.geometry("600x900")   # Größeres Fenster

# Center window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"+{x}+{y}")

# Load the logo image
image = Image.open("app_data/Logo_small.png")
image = image.resize((60, 60)) # Größe anpassen
photo = ImageTk.PhotoImage(image)

# Modern design with dark theme
root.tk_setPalette(background="#2b2b2b", foreground="white")  # Dunkles Theme
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6, relief="flat", background="#4CAF50", foreground="white")
style.configure("TLabel", font=("Arial", 11), background="#2b2b2b", foreground="white")
style.configure("TCheckbutton", font=("Arial", 11), background="#2b2b2b", foreground="white")
style.map("TCheckbutton",
      background=[("active", "#3a3a3a"), ("!active", "#2b2b2b")],
      indicatorcolor=[("selected", "#4CAF50"), ("!selected", "#aaaaaa")],
      foreground=[("selected", "white"), ("!selected", "#aaaaaa")])
style.configure("TRadiobutton", 
    font=("Arial", 11),
    background="#2b2b2b",
    foreground="white")
style.map("TRadiobutton",
    background=[("active", "#3a3a3a"), ("!active", "#2b2b2b")],
    foreground=[("disabled", "#666666"), ("selected", "white")])

frame = ttk.Frame(root)

# Header
header = tk.Label(root, text="UniverseTrip\nObject list creator",image=photo, compound="left", padx= 13, justify="left", font=("Arial", 20, "bold"), anchor="w")
header.image = photo
header.pack(fill="x", padx=10, pady=10)

# List of standard catalouge files
standard_files = {
    "db1": "./object_database/database_HR.xlsx",
    "db2": "./object_database/database_M.xlsx",
    "db3": "./object_database/database_NGC.xlsx",
}

selected_option = tk.StringVar(value="manual")
file_path = tk.StringVar(value="No file selected.")

# File selection
file_frame = tk.LabelFrame(root, text="1. Select database file", padx=10, pady=10)
file_frame.pack(fill="x", padx=20, pady=5)

# Radiobuttons for standard files
radio_frame = tk.Frame(file_frame)
radio_frame.pack(anchor="w", pady=5)

ttk.Radiobutton(radio_frame, text="HR catalogue - All Stars until 6.5mag (bare eyes visible)", variable=selected_option, value="db1", command=update_file_path).pack(anchor="w")
ttk.Radiobutton(radio_frame, text="Messier catalogue - Catalogue created by Charles Messier", variable=selected_option, value="db2", command=update_file_path).pack(anchor="w")
ttk.Radiobutton(radio_frame, text="NGC catalogue - New General Catalogue of Nebulae and Clusters of Stars", variable=selected_option, value="db3", command=update_file_path).pack(anchor="w")
ttk.Radiobutton(radio_frame, text="Manual selection", variable=selected_option, value="manual").pack(anchor="w")
tk.Label(file_frame, textvariable=file_path, wraplength=420, height=3, justify="left").pack(anchor="w")

# Buttons for manual file selection
tk.Button(file_frame, text="Select file", font=("Arial", 12, "bold"), command=select_file).pack(anchor="e", pady=5)

#file_path = tk.StringVar(value="No file selected.")
#tk.Label(file_frame, textvariable=file_path, wraplength=420, height=3, justify="left").pack(anchor="w")
#tk.Button(file_frame, text="Select file", font=("Arial", 12, "bold"), command=select_file).pack(anchor="e", pady=5)


# Checkboxes 
options_frame = tk.LabelFrame(root, text="2. Select output options", padx=10, pady=10)
options_frame.pack(fill="x", padx=20, pady=5)

checkboxes = {}
num_columns = 2
row = 0
col = 0

for idx, otype in enumerate(available_types):
    display_name = otype_display_names.get(otype, otype)  # Falls kein Mapping vorhanden, Originalname behalten
    var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(options_frame, text=display_name, variable=var)
    chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)
    checkboxes[otype] = var

    col += 1
    if col >= num_columns:
        col = 0
        row += 1

# Checkbox for excluding objects with distance = 0.0
exclude_zero_distance_var = tk.BooleanVar(value=True)
chk_exclude_zero_distance = ttk.Checkbutton(options_frame, text="Include also objects with distance = 0", variable=exclude_zero_distance_var)
chk_exclude_zero_distance.grid(row=row + 1, column=0, columnspan=2, sticky="w", padx=10, pady=5)


# Checkbox für das Filtern einzelner Sterne aus Sternhaufen
#filter_stars_var = tk.BooleanVar(value=False)
#chk_filter_stars = ttk.Checkbutton(options_frame, text="Einzelne Sterne aus Sternhaufen entfernen", variable=filter_stars_var)
#chk_filter_stars.grid(row=row + 2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

# Set min and max values for brightness and distance
minmax_frame = tk.LabelFrame(root, text="3. Select minimal and maximal data values for objects", padx=10, pady=10)
minmax_frame.pack(fill="x", padx=20, pady=5)

# Create a new frame for the grid layout
values_frame = tk.Frame(minmax_frame, bg="#2b2b2b")
values_frame.pack(fill="x", padx=0, pady=0)

# Input fields for brightness range
ttk.Label(values_frame, text="Minimal brightness:").grid(row=0, column=0, sticky="w", padx=0, pady=0)
entry_max_v = ttk.Entry(values_frame, justify="right")
entry_max_v.grid(row=0, column=1, sticky="e", padx=0, pady=0)
entry_max_v.insert(0, "25")  # Standardwert
ttk.Label(values_frame, text="mag").grid(row=0, column=3, sticky="w", padx=5, pady=0)

ttk.Label(values_frame, text="Maximal brightness:").grid(row=1, column=0, sticky="w", padx=0, pady=0)
entry_min_v = ttk.Entry(values_frame, justify="right")
entry_min_v.grid(row=1, column=1, sticky="e", padx=0, pady=0)
entry_min_v.insert(0, "-2.0")  # Standardwert
ttk.Label(values_frame, text="mag").grid(row=1, column=3, sticky="w", padx=5, pady=0)



# Add empty line between the two sections
ttk.Label(values_frame, text="", background="#2b2b2b").grid(row=2, column=0, columnspan=2, pady=5)

# Input fields for distance range
ttk.Label(values_frame, text="Minimal distance:").grid(row=3, column=0, sticky="w", padx=0, pady=0)
entry_min_dist = ttk.Entry(values_frame, justify="right")
entry_min_dist.grid(row=3, column=1, sticky="e", padx=0, pady=0)
entry_min_dist.insert(0, "0.0")  # Standardwert
ttk.Label(values_frame, text="Lightyears").grid(row=3, column=3, sticky="w", padx=5, pady=0)

ttk.Label(values_frame, text="Maximal distance:").grid(row=4, column=0, sticky="w", padx=0, pady=0)
entry_max_dist = ttk.Entry(values_frame, justify="right")
entry_max_dist.grid(row=4, column=1, sticky="e", padx=0, pady=0)
entry_max_dist.insert(0, "1000000000")  # Standardwert
ttk.Label(values_frame, text="Lightyears").grid(row=4, column=3, sticky="w", padx=5, pady=0)

start_frame = tk.LabelFrame(root, text="3. Create datafile", padx=10, pady=10)
start_frame.pack(fill="x", padx=20, pady=10)

# New frame for the grid layout
startvalues_frame = tk.Frame(start_frame, bg="#2b2b2b")
startvalues_frame.pack(fill="x", padx=0, pady=0)

# Input field for the output filename
ttk.Label(startvalues_frame, text="Name of the object file:").grid(row=0, column=0, sticky="w", padx=0, pady=0)
entry_filename = ttk.Entry(startvalues_frame)
entry_filename.grid(row=0, column=1, sticky="e", padx=0, pady=0)
entry_filename.insert(0, "objects_x.csv")  # Standardwert

tk.Button(start_frame, text="Create file", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=process_file).pack(anchor="e", pady=10)

# Main loop to ceep the window open
root.mainloop()
