#Installationsanleitung
#Download and install Python
#Eingabeaufforderung öffnen
#cd C:\Users\"USER"\AppData\Local\Programs\Python\Python313\Scripts
#pip install pandas
#pip install plotly
#pip install numpy

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import math
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import random
import plotly.io as pio
import os as os1
from tkinter import messagebox
from PIL import Image, ImageTk
import base64
from PIL import Image
from io import BytesIO

# Abstand der Sonne vom galaktischen Zentrum in LJ
SONNEN_ABSTAND = 27000


#Milchstrasse mit Spiralarmen erstellen: Funktion spiral_arm und rotate_points
def spiral_arm(a, b, theta_min, theta_max, num_points, center_shift=27000, spread=10000):
    """
    Erstellt Punkte entlang eines logarithmischen Spiralarms mit Breite.
    a, b: Parameter der Spiralform
    theta_min, theta_max: Winkelbereich (in Radiant)
    num_points: Anzahl der Punkte
    center_shift: Verschiebung des Milchstraßenzentrums
    spread: Breite des Spiralarms (größerer Wert -> breiterer Arm)
    """
    theta = [theta_min + i * (theta_max - theta_min) / num_points for i in range(num_points)]
    r = [a * math.exp(b * t) for t in theta]
    x = [radius * math.cos(t) + center_shift + random.gauss(0, spread) for radius, t in zip(r, theta)]
    y = [radius * math.sin(t) + random.gauss(0, spread) for radius, t in zip(r, theta)]
    z = [random.gauss(0, 400) for _ in range(num_points)]  # Zufällige Höhenabweichung
    return x, y, z

#Spiralarme der Milchstrasse rotieren
def rotate_points(x, y, angle, center_x=27000):
    """
    Rotiert Punkte um ein verschobenes Zentrum.
    x, y: Listen von Koordinaten
    angle: Rotationswinkel in Radiant
    center_x: x-Koordinate des Zentrums der Rotation
    """
    # Punkte in das lokale Koordinatensystem des Rotationszentrums verschieben
    x_shifted = [xi - center_x for xi in x]
    y_shifted = y  # y bleibt unverändert, da das Zentrum auf der x-Achse liegt

    # Rotation um den Ursprung durchführen
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    x_rotated = [cos_angle * xi - sin_angle * yi for xi, yi in zip(x_shifted, y_shifted)]
    y_rotated = [sin_angle * xi + cos_angle * yi for xi, yi in zip(x_shifted, y_shifted)]

    # Punkte zurück in das globale Koordinatensystem verschieben
    x_final = [xi + center_x for xi in x_rotated]
    y_final = y_rotated
    return x_final, y_final



#Fügt den Kreisen um die Sonne die Abstandsinformation hinzu
def add_distance_labels(data, radii, earth_x=0.00001585501251):
    """
    Fügt den Kreisen um die Sonne Textbeschriftungen mit den Abständen hinzu.
    
    Parameter:
        data: Liste von Plotly-Objekten, die die Kreise enthält.
        radii: Liste von Radien der Kreise (Abstände in Lichtjahren).
    
    Rückgabe:
        Aktualisierte Datenliste mit Textbeschriftungen.
    """
    for radius in radii:
        # Position für die Textbeschriftung (auf der positiven x-Achse)
        text_x = earth_x
        text_y = radius # Beschriftung unten, damit die Schrift nicht inneinander läuft
        text_z = 0

        data.append(
            go.Scatter3d(
                x=[text_x],
                y=[text_y],
                z=[text_z],
                mode="text",
                text=[f"{radius:,} Lj"],
                textposition="bottom center",
                name=f"Distance: {radius} Lj",
                textfont=dict(color="rgb(140,140,140)", size=12),
                showlegend=False,
                hoverinfo='skip'
            )
        )
    return data

#Rotation berechnen, um die Verdrehung der Planetenbahnen gegenüber der Galaktischen x-Ebene zu berechnen
def rotate_coordinates(x, y, z, angle_x, angle_y):
    """
    Dreht die Koordinaten um die x- und y-Achsen.
    
    Parameter:
        x, y, z: Listen der ursprünglichen Koordinaten.
        angle_x: Drehwinkel um die x-Achse (in Grad).
        angle_y: Drehwinkel um die y-Achse (in Grad).
    
    Rückgabe:
        Rotierte Koordinaten (x_rot, y_rot, z_rot).
    """
    # Winkel in Bogenmaß umrechnen
    angle_x = np.radians(angle_x)
    angle_y = np.radians(angle_y)
    
    # Rotationsmatrix für die x-Achse
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    
    # Rotationsmatrix für die y-Achse
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    
    # Originale Koordinaten
    coordinates = np.array([x, y, z])
    
    # Rotieren um x- und y-Achse
    rotated = rotation_y @ (rotation_x @ coordinates)
    
    return rotated[0], rotated[1], rotated[2]



#Planetenbahnen hinzufügen
def add_planet_orbits(orbits):
    """
    Erstellt Planetenbahnen als Kreise um die Sonne in der z=0-Ebene.
    
    Parameter:
        orbits: Liste der Bahnradii in Lichtjahren.
        
    Rückgabe:
        Liste von Plotly-Scatter3d-Objekten, die die Bahnen darstellen.
    """
    theta = [i * 2 * math.pi / 720 for i in range(720)]  # 360 Punkte für glatte Kreise
    orbit_data = []
    
    for orbit_radius in orbits:
        x = [orbit_radius * math.cos(t) for t in theta]
        y = [orbit_radius * math.sin(t) for t in theta]
        z = [0 for _ in theta]  # Ebene z=0
        
        # Ersten Punkt erneut anhängen, um den Kreis zu schließen
        x.append(x[0])
        y.append(y[0])
        z.append(z[0])
        
        #Planetenbahnen in der z-Ebene darstellen
        orbit_data.append(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="none",
                line=dict(color="red", width=2, dash="dot"),
                showlegend=False,
                name=f"Orbit {orbit_radius} LJ",
            )
        )
    
    return orbit_data

#Umrechnen der galaktischen Koordinaten und Abstand in x,y,z Koordinaten
def galactic_to_cartesian(l, b, d):
    """
    Konvertiert galaktische Koordinaten (l, b, d) in kartesische Koordinaten (x, y, z),
    wobei das Zentrum der Milchstraße auf eine Verschiebung (center_shift) relativ zur Sonne gesetzt wird.
    """
    l_rad, b_rad = np.radians(l), np.radians(b)
    x = d * np.cos(b_rad) * np.cos(l_rad)
    y = d * np.cos(b_rad) * np.sin(l_rad)
    z = d * np.sin(b_rad)
    return x, y, z

def show_error(message):
    """Zeigt eine Fehlermeldung als Popup-Fenster an."""
    root = tk.Tk()
    root.withdraw()  # Hauptfenster ausblenden
    messagebox.showerror("Fehler", message)
    root.destroy()

#Laden der Objekte aus dem CSV File
def load_objects_from_csv(file_path):
    """
    Lädt die Objekte aus einer CSV-Datei und berechnet ihre kartesischen Koordinaten.
    Die CSV-Datei sollte die Spalten "object_name", "galactic_l_deg", "galactic_b_deg", "distance_to_sun_Lj", "object_type" enthalten.
    """
    if not os1.path.exists(file_path):  #Check if file exists
        show_error(f"The file '{file_path}' was not found.\nPlease start the program again.")
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    try:
        # CSV-Datei einlesen
        data = pd.read_csv(file_path)
    except Exception as e:
        show_error(f"Failure at reading the file:\n{e}.\nPlease start the program again.")
        raise ValueError(f"Failure at reading the file '{file_path}': {e}")

    
    # Überprüfen, ob die benötigten Spalten vorhanden sind
    required_columns = ["object_name", "galactic_l_deg", "galactic_b_deg", "distance_to_sun_Lj", "object_type"]
    if not all(col in data.columns for col in required_columns):
        show_error(f"The file must contain the colums {required_columns}.\nPlease start the program again.")
        raise ValueError(f"The file must contain the colums {required_columns} .")
    
    x, y, z = galactic_to_cartesian(data["galactic_l_deg"], data["galactic_b_deg"], data["distance_to_sun_Lj"])
    data["x"], data["y"], data["z"] = x, y, z
    return data

#Kreise um die Sonne erstellen für die Abstandsinformation
def create_circles(radii, num_points=360, earth_x=0.00001585501251):
    """
    Erstellt Kreise um die Sonne mit angegebenen Radien.
    radii: Liste von Radien (Lichtjahre)
    num_points: Anzahl der Punkte pro Kreis (je höher, desto glatter der Kreis)
    """
    circles = []
    theta = [2 * math.pi * i / num_points for i in range(num_points)]
    
    for radius in radii:
        x = [radius * math.cos(t) + earth_x for t in theta]
        y = [radius * math.sin(t) for t in theta]
        z = [0] * num_points  # Alle Punkte liegen in der Scheibe

        # Ersten Punkt erneut ans Ende anhängen, um den Kreis zu schließen
        x.append(x[0])
        y.append(y[0])
        z.append(z[0])
        
        circles.append((x, y, z))
    return circles

"""
*************************************************
3D-Darstellung der Objekte aus der CSV-Datei.
*************************************************
"""

def plot_objects_and_milky_way(objects, orbits, clusters, show_markertext, show_hoverinfo, show_lines, show_earthaxis, show_orientationline, show_visibility_limits, show_distances, show_legend):

    """
    *************************************************
    Figure - Layout
    *************************************************
    """

    # Initiale Achsenbereiche
    axis_range = [-100000, 100000]

    # Layout des Diagramms mit angepassten Achsen
    layout = go.Layout(
        #title=dict(text="UniverseTrip", font=dict(size=35), x=0, y=0.98, xref="paper", yref="paper"), # Titel wird durch Bild ersetzt
        font = dict(color="rgb(140,140,140)", size=13),
        scene=dict(
            xaxis=dict(title="x (Lightyears)",range=axis_range,visible=False),  # Bereich für x-Achse visible=False
            yaxis=dict(title="y (Lightyears)",range=axis_range,visible=False),  # Bereich für y-Achse
            zaxis=dict(title="z (Lightyears)",range=axis_range,visible=False),  # Bereich für z-Achse
            aspectmode="cube",   # Macht die Achsen gleichmäßig skaliert
        ),
        updatemenus=[  # Buttons für die Achsenbereiche
            dict(
                type="buttons",
                bgcolor="rgb(30,30,30)", #Farbe Hintergrund inaktive Buttons
                bordercolor="rgb(140,140,140)", #Farbe Button Rand
                borderwidth=1,
                showactive=True,
                font= dict(color="rgb(140,140,140)"),
                x=0, y=0.85,
                xanchor="left",
                yanchor="top",
                buttons=[
                    dict(
                        label="±50 Mrd Lj (Visible universe)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-50000000000, 50000000000],visible=False),
                            yaxis=dict(range=[-50000000000, 50000000000],visible=False),
                            zaxis=dict(range=[-50000000000, 50000000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±10 Mrd Lj",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-10000000000, 10000000000],visible=False),
                            yaxis=dict(range=[-10000000000, 10000000000],visible=False),
                            zaxis=dict(range=[-10000000000, 10000000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±1 Mrd Lj (Laniakea Supercluster)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-1000000000, 1000000000],visible=False),
                            yaxis=dict(range=[-1000000000, 1000000000],visible=False),
                            zaxis=dict(range=[-1000000000, 1000000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±100 Mio Lj (Virgo Supercluster)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-100000000, 100000000],visible=False),
                            yaxis=dict(range=[-100000000, 100000000],visible=False),
                            zaxis=dict(range=[-100000000, 100000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±10 Mio Lj (Local Groupe)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-10000000, 10000000],visible=False),
                            yaxis=dict(range=[-10000000, 10000000],visible=False),
                            zaxis=dict(range=[-10000000, 10000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±1 Mio Lj (Milky Way surroundings)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-1000000, 1000000],visible=False),
                            yaxis=dict(range=[-1000000, 1000000],visible=False),
                            zaxis=dict(range=[-1000000, 1000000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±100k Lj (Milky Way)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-100000, 100000],visible=False),
                            yaxis=dict(range=[-100000, 100000],visible=False),
                            zaxis=dict(range=[-100000, 100000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±10k Lj",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-10000, 10000],visible=False),
                            yaxis=dict(range=[-10000, 10000],visible=False),
                            zaxis=dict(range=[-10000, 10000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±1k Lj",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-1000, 1000],visible=False),
                            yaxis=dict(range=[-1000, 1000],visible=False),
                            zaxis=dict(range=[-1000, 1000],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±100 Lj (Neighboring stars)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-100, 100],visible=False),
                            yaxis=dict(range=[-100, 100],visible=False),
                            zaxis=dict(range=[-100, 100],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±10 Lj",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-9.99998414498749, 10.0000158550125],visible=False),
                            yaxis=dict(range=[-10, 10],visible=False),
                            zaxis=dict(range=[-10, 10],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±1 Lj",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-0.99998414498749, 1.00001585501251],visible=False),
                            yaxis=dict(range=[-1, 1],visible=False),
                            zaxis=dict(range=[-1, 1],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±0.1 Lj (37 Ldays) ",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-0.09998414498749, 0.10001585501251],visible=False),
                            yaxis=dict(range=[-0.1, 0.1],visible=False),
                            zaxis=dict(range=[-0.1, 0.1],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±0.01 Lj (3,7 LTage) (Satellites)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-0.00998414498749, 0.0100158550125100000],visible=False),
                            yaxis=dict(range=[-0.01, 0.01],visible=False),
                            zaxis=dict(range=[-0.01, 0.01],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±0.001 Lj (8,8 Lhours) (Solar System)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-0.00098414498749, 0.00101585501251],visible=False),
                            yaxis=dict(range=[-0.001, 0.001],visible=False),
                            zaxis=dict(range=[-0.001, 0.001],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )]#end args
                    ),#end dict
                    dict(
                        label="±0.0001 Lj (53 Lminutes)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[-0.00008414498749, 0.00011585501251],visible=False),
                            yaxis=dict(range=[-0.0001, 0.0001],visible=False),
                            zaxis=dict(range=[-0.0001, 0.0001],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )#end dict
                        ]#end args
                    ),#end dict
                    dict(
                        label="±0.00001 Lj (5,3 Lminutes)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[0.00000585501251, 0.000025855012510],visible=False),
                            yaxis=dict(range=[-0.00001, 0.00001],visible=False),
                            zaxis=dict(range=[-0.00001, 0.00001],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )#end dict
                        ]#end args
                    ),#end dict
                    dict(
                        label="±0.000001 Lj (32 Lsek)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[0.00001485501251, 0.00001685501251],visible=False), #den Mittelpunkt um die Erdentfernung von der Sonne (0.000015855012510 LJ) verschieben
                            yaxis=dict(range=[-0.000001, 0.000001],visible=False),
                            zaxis=dict(range=[-0.000001, 0.000001],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )#end dict
                        ]#end args
                    ),#end dict
                    dict(
                        label="±0.0000001 Lj (3,2 Lsek) (Earth / Moon)",
                        method="relayout",
                        args=["scene", dict(
                            xaxis=dict(range=[0.00001575501251, 0.00001595501251],visible=False), #den Mittelpunkt um die Erdentfernung von der Sonne (0.000015855012510 LJ) verschieben
                            yaxis=dict(range=[-0.0000001, 0.0000001],visible=False),
                            zaxis=dict(range=[-0.0000001, 0.0000001],visible=False),
                            camera=dict(eye=dict(x=0, y=1.4469, z=0.75))  # Kamerawinkel so berechnen, dass Sonnensystem von Oben mit 62,6° dargestellt wird.
                        )#end dict
                        ]#end args
                    )#end dict
                ]# end buttons
            ) # End dict
        ], #End updatemenus
        annotations=[
            dict(
                text="Scaling:",  # Überschrift
                x=0, y=0.9,                # Oberhalb der Buttons
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=18, color="rgb(140,140,140)"),  # Schriftgröße und Farbe
                xanchor="left",            # Links ausgerichtet
                yanchor="top"
            )#end dict
        ]#end annotation
    )#end go.layout



    """
    *************************************************
    Figure - Data
    *************************************************
    """


           
    # Sonne im Ursprung des galaktischen Koordinatensystems hinzufügen
    data = [
        go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers+text' if show_markertext else 'markers',
            marker=dict(size=3, color='yellow'),
            text='Sun',
            textposition="top center",
            textfont=dict(color="yellow", size=12),
            name='Sun',
            showlegend=False,
            hoverinfo='text' if show_hoverinfo else 'skip',
        )
    ]

    #Kosmische Struktur hinzufügen
    # Universumsgröße in Lichtjahren
    universe_size = 93000000000  # 93 Milliarden Lichtjahre
    radius = universe_size / 2  # Radius der Kugel

    # Anzahl der Punkte (mehr Punkte für bessere Struktur)
    num_points = 100000  

    # Anzahl der Filamente und Startpunkte
    num_filaments = 1000  
    start_points = []
    while len(start_points) < num_filaments:
        x, y, z = np.random.uniform(-radius, radius, 3)
        if x**2 + y**2 + z**2 <= radius**2:  # Punkt innerhalb der Kugel prüfen
            start_points.append((x, y, z))
    start_points = np.array(start_points)

    # Filamente generieren
    points = []
    for x, y, z in start_points:
        for _ in range(num_points // num_filaments):
            dx, dy, dz = np.random.normal(scale=350000000, size=3)
            x, y, z = x + dx, y + dy, z + dz
            if x**2 + y**2 + z**2 <= radius**2:  # Punkt bleibt innerhalb der Kugel
                points.append((x, y, z))

    points = np.array(points)

    data.append(
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="markers",
                marker=dict(
                    size=1,
                    color='rgb(255, 248, 231)', #Sternfarbe entsprechend kosmischer Latte #FFF8E7
                    opacity=0.8,
                ),
                showlegend = False,
                hoverinfo='skip'
            )
        )

    # Ende Kosmische Struktur
    
    """
    # Milchstraßenscheibe erstellen
    theta = [i * 2 * math.pi / 360 for i in range(360)]
    radius = 50000
    disc_x = [radius * math.cos(t) + SONNEN_ABSTAND for t in theta]
    disc_y = [radius * math.sin(t) for t in theta]
    disc_z = [0 for _ in theta]
    
    # Milchstraßenscheibe hinzufügen
    data.append(
        go.Scatter3d(
            x=disc_x, y=disc_y, z=disc_z,
            mode='lines',
            line=dict(color='red', width=10),
            name="Milchstraßenscheibe",
            hoverinfo='skip'
        )
    )
    """
    # Galaxienclusterbezeichnungen hinzufügen
    for cluster in clusters:
        name, l, b, distance = cluster
        x, y, z = galactic_to_cartesian(l, b, distance)

        data.append(
            go.Scatter3d(
                x=[x],
                y=[y],
                z=[z],
                mode="markers+text",
                marker=dict(size=10, color="white"),
                text=[name],
                textposition="top center",
                name=f"Cluster: {name}",
                hoverinfo='skip'
            )
        )
    
    # Parameter für die vier Spiralarme
    spiral_params = [
        {"a": 1200, "b": 0.3, "theta_min": 0, "theta_max": 4 * math.pi, "num_points": 4000, "spread": 2000},
        {"a": 1200, "b": 0.3, "theta_min": 0, "theta_max": 4 * math.pi, "num_points": 4000, "spread": 2000},
        {"a": 1200, "b": 0.3, "theta_min": 0, "theta_max": 4 * math.pi, "num_points": 4000, "spread": 2000},
        {"a": 1200, "b": 0.3, "theta_min": 0, "theta_max": 4 * math.pi, "num_points": 4000, "spread": 2000},
    ]
    # Rotationswinkel für die Spiralarme (in Radiant)
    angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
    # Daten für Spiralarme erstellen
    center_shift = 27000
    for i, (params, angle) in enumerate(zip(spiral_params, angles)):
        x, y, z = spiral_arm(**params, center_shift=center_shift)
        x, y = rotate_points(x, y, angle, center_x=center_shift)  # Punkte um das galaktische Zentrum rotieren
        data.append(
            go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=dict(size=1, color='rgb(255, 248, 231)'), #Sternfarbe entsprechend kosmischer Latte #FFF8E7
                showlegend=False,
                name=f"Spiralarm {i+1}",
                hoverinfo='skip'
            )
        )

    # Planetenbahnen generieren und orientieren
    planet_orbits = add_planet_orbits(orbits)
    for orbit in planet_orbits:
        x_rot, y_rot, z_rot = rotate_coordinates(
            orbit.x, orbit.y, orbit.z,
            angle_x=-62.6, # Neigung um die galaktische Ebene
            angle_y=0
        )
        data.append(
            go.Scatter3d(
                x=x_rot,
                y=y_rot,
                z=z_rot,
                mode="lines",
                line=dict(color="blue", width=3, dash="solid"),
                showlegend=False,
                name=orbit.name,
                hoverinfo='skip'
            )
        )
        
    #Strich in Richtung Milchstrassenzentrum hinzufügen
    if show_orientationline:
        data.append(
            go.Scatter3d(
                x=[0,SONNEN_ABSTAND],
                y=[0,0],
                z=[0,0],
                mode='lines',
                line=dict(color='red', width=3, dash='solid'),  # Farbe und Breite des Strichs
                name='direction to calactic core',
                hoverinfo='skip'
            )
        )
    
    
    #Strich für die Erdachse zum Himmelsnordpol und Südpol hinzufügen
    if show_earthaxis:
        erde_gal_laenge = 0 #Galaktische Koordinaten der Erde um Striche zum Himmelsnord/Suedpol einzeichnen zu können
        erde_gal_breite = 0
        erde_distance = 0.000015855012510
    
        himmelsnordpol_gal_laenge = 122.847444444 #Galaktische Koordinaten von Himmelnordpol
        himmelsnordpol_gal_breite = 27.105444444444
        himmelsnordpol_distance = 50000  #Entefernung in LJ, bis zu der die Striche eingezeichnet werden. 430 LJ = Polaris

        himmelssuedpol_gal_laenge = -57.152555556 #Galaktische Koordinaten von Himmelsuedpol
        himmelssuedpol_gal_breite = -27.105444444444
        himmelssuedpol_distance = 50000 #Entefernung in LJ, bis zu der die Striche eingezeichnet werden. 430 LJ = Polaris

        x_erde, y_erde, z_erde = galactic_to_cartesian(erde_gal_laenge, erde_gal_breite, erde_distance)
        x_hnp, y_hnp, z_hnp = galactic_to_cartesian(himmelsnordpol_gal_laenge, himmelsnordpol_gal_breite, himmelsnordpol_distance)
        x_hsp, y_hsp, z_hsp = galactic_to_cartesian(himmelssuedpol_gal_laenge, himmelssuedpol_gal_breite, himmelssuedpol_distance)
        
        data.append( #Strich von Erde zu Himmelsnordpol einzeichnen
            go.Scatter3d(
                x=[x_hnp,x_erde],
                y=[y_hnp,y_erde],
                z=[z_hnp,z_erde],
                mode='lines',
                line=dict(color='pink', width=3, dash='solid'),  # Farbe und Breite des Strichs
                name='Earth axis<br>to celestial pole',
                hoverinfo='skip'
            )
        )

        data.append( #Strich von Erde zu Himmelssüdpol einzeichnen
            go.Scatter3d(
                x=[x_hsp,x_erde],
                y=[y_hsp,y_erde],
                z=[z_hsp,z_erde],
                mode='lines',
                line=dict(color='pink', width=3, dash='solid'),  # Farbe und Breite des Strichs
                name='Earth axis<br>to south celestial pole',
                showlegend=False,  # Verhindert das Erscheinen in der Legende
                hoverinfo='skip'
            )
        )
    
    
    #Milchstrassen Zentrum hinzufügen
    data.append(
        go.Scatter3d(
            x=[SONNEN_ABSTAND], y=[0], z=[0],
            mode='markers+text' if show_markertext else 'markers',
            marker=dict(size=3, color='black'),
            text='',
            textposition="top center",
            textfont=dict(color="black", size=12),
            name='Galactic Center',
            showlegend=False,
            hoverinfo='text' if show_hoverinfo else 'skip',
        )
    ) 

    # Kreise um die Sonne hinzufügen
    if show_distances:
        circle_radii = [0.0000001, 0.000001, 0.00001, 0.0001,
                        0.001,0.005,
                        0.01,0.05,
                        0.1,0.5,
                        1,5,
                        10,50,
                        100,500,
                        1000,5000,
                        50000,10000,
                        100000,500000,
                        1000000,5000000,
                        10000000,50000000,
                        100000000,500000000,
                        1000000000,5000000000,
                        10000000000,46300000000]# Radien in Lichtjahren
        circles = create_circles(circle_radii)
    
        for i, (x, y, z) in enumerate(circles):
            data.append(
                go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color="rgb(100,100,100)", dash='solid', width=3), #war einst die Farbe rgb(164,196,227)
                    showlegend=False,
                    name=f"{circle_radii[i]} light year",
                    hoverinfo='skip'
                )
            )

        # Textbeschriftungen für die Kreise um die Sonne (Abstände) hinzufügen
        data = add_distance_labels(data, circle_radii)

    # Kreis um die Sonne hinzufügen für Sichtbarkeitsgrenzen
    if show_visibility_limits:
        circle_radii_eye = [9000,2537000,283887000,999000000]  # Radien in Lichtjahren
        circle_radii_eye_labels = ["Visibility limit - single stars with naked eye",
                                   "Visibility limit - objects with naked eye",
                                   "Visibility limit - objects with visual amateur telescope",
                                   "Visibility limit - objects with amateur astrophotography"]  # Individuelle Labels
        circle_eye = create_circles(circle_radii_eye)
    
        for i, (x, y, z) in enumerate(circle_eye):
            data.append(
                go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color="rgb(164,196,227)", width=7, dash='dot'),
                    name=circle_radii_eye_labels[i],  # Label je Kreis setzen
                    showlegend=False,  # Verhindert das Erscheinen in der Legende
                    hoverinfo='skip'
                )
            )
            # Index für die Platzierung des Labels (z. B. viertel Punkt des Kreises)
            label_index = len(x) // 4  # 1/4 des Kreises (90° Position, also unten)
            # Label als separaten Scatter3d-Punkt am Rand des Kreises hinzufügen
            data.append(
               go.Scatter3d(
                   x=[x[label_index]], y=[y[label_index]], z=[z[label_index]],  # Letzter Punkt des Kreises als Label-Position
                   mode='text',
                   text=circle_radii_eye_labels[i],  # Label-Text
                   textposition="bottom center",
                   textfont=dict(color="rgb(164,196,227)"),  # Farbe auf Rot setzen
                   showlegend=False,
                   hoverinfo='skip'
               )
            )
        
    #Planetenbahnen hinzufügen
    planet_orbits = add_planet_orbits(orbits)
    data.extend(planet_orbits)
    
    # Objekte hinzufügen
    colors = {"Star": "yellow", "OS": "blue", "KS": "green", "GX": "red", "PN": "grey", "GN": "orange", "Satelite": "orange", "Planet": "white", "GxCl1": "white", "GxCl2": "white", "GxCl3": "white", "GxCl4": "white", "GxCl1_LAN": "yellow", "GxCl2_LAN": "yellow", "GxCl3_LAN": "yellow", "GxCl4_LAN": "yellow"}


    for obj_type, group in objects.groupby("object_type"):
        color = colors.get(obj_type, "white")
        data.append(go.Scatter3d(
            x=group["x"], y=group["y"], z=group["z"],
            mode='markers+text' if show_markertext else 'markers',
            marker=dict(size=3, color=color),
            text=group["object_name"],
            hoverinfo='text' if show_hoverinfo else 'skip',
            textposition="top center",
            textfont=dict(color=color, size=12), #"rgb(255,255,255)
            name=obj_type
        ))

    # Linien von den Objekten zur z=0 Ebene hinzufügen
    if show_lines:
        x_solid, y_solid, z_solid = [], [], []  # Für durchgezogene Linien (z >= 0)
        x_dash, y_dash, z_dash = [], [], []  # Für gestrichelte Linien (z < 0)

        for _, obj in objects.iterrows():
            x, y, z = obj["x"], obj["y"], obj["z"]

            if z >= 0:
                x_solid.extend([x, x, None])  # None trennt Liniensegmente
                y_solid.extend([y, y, None])
                z_solid.extend([z, 0, None])
            else:
                x_dash.extend([x, x, None])
                y_dash.extend([y, y, None])
                z_dash.extend([z, 0, None])

        # Durchgezogene Linien für Objekte mit z >= 0
        if x_solid:
            data.append(go.Scatter3d(
                x=x_solid, y=y_solid, z=z_solid,
                mode="lines",
                line=dict(color="rgb(150,150,150)", width=2, dash="solid"),  
                name="Object above<br>galactic plane",  
                showlegend=True,
                hoverinfo='skip'
            ))

        # Gestrichelte Linien für Objekte mit z < 0
        if x_dash:
            data.append(go.Scatter3d(
                x=x_dash, y=y_dash, z=z_dash,
                mode="lines",
                line=dict(color="rgb(70,70,70)", width=2, dash="solid"), 
                name="Object below<br>galactic plane",  
                showlegend=True,
                hoverinfo='skip'
            ))
    
    """
    *************************************************
    Figure - erzeugen mit Layout und Data
    *************************************************
    """
    
    # Diagramm erstellen
    fig = go.Figure(data=data, layout=layout)

    """
    *************************************************
    Figure - Layout final updaten
    *************************************************
    """

    fig.layout.paper_bgcolor = '#000000'
    fig.update_layout(scene_camera=dict(eye=dict(x=0, y=1.4469, z=0.75))) #initiale Kameraposition auf x=0 und y ist ein flacher Winkel.
    # Legende anpassen
    fig.update_layout(
        showlegend=show_legend,
        legend=dict(
            itemwidth=50,  # Legenden-Breitenlimit in Pixeln
            title=dict(text='Legend'),
            bgcolor="rgba(0, 0, 0, 0)", # Hintergrundfarbe mit Transparenz
            x=1,          # Position relativ zum Plotbereich (100% der Breite)
            y=1,          # Position relativ zum Plotbereich (100% der Höhe)
            font= dict(color="rgb(150,150,150)"),
            xanchor="right",  # Ausrichtung der Legende
            yanchor="top",   # Ausrichtung der Legende
            bordercolor="black",                 # Rahmenfarbe
            borderwidth=1                        # Rahmenbreite
        )
    )
    # Layout anpassen für fullscreen
    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10),  # Minimale Ränder
    )

    # Mouse hover anpassen
    fig.update_layout(
        hovermode='closest'
    )


    # Bild laden und als base64 encodieren
    img = Image.open("app_data/Logo_small_text.png")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    
    # Titelbild einfügen
    fig.update_layout(
        images=[dict(
            source="data:image/png;base64," + encoded_image,
            xref="paper", yref="paper",
            x=0, y=0.98,
            sizex=0.15, sizey=0.15,
            xanchor="left",
            yanchor="top",
            layer="above",
            sizing="contain"
        )]
    )
    
    # Copyright Vermerk hinzufügen
    fig.add_annotation(
        text="© 2025 Markus Kerbl<br>Version 1.0.0 - 08 April 2025<br>Special thanks to: ChatCPT and SIMBAD Astronomical Database - CDS (Strasbourg)",  # Der Copyright-Text
        xref="paper", yref="paper",          # Koordinaten relativ zur Plotfläche
        x=0, y=0,                            # Unten links
        #xanchor="left", yanchor="bottom",
        align='left',                        # Linksbündig
        showarrow=False,                     # Kein Pfeil
        font=dict(size=12, color="rgb(140,140,140)")     # Schriftgröße und Farbe
     )



    """
    *************************************************
    Figure - Zeigen
    *************************************************
    """

    config = {'displayModeBar':True,
              'displaylogo':False} #Modebar konfigurieren
   
    fig.show(config=config)
    #pio.write_html(fig, "UniverseTrip.html") #HTML File schreiben

"""
*************************************************
GUI creation
*************************************************
"""

def start_gui():
    root = tk.Tk()
    root.title("UniverseTrip - Configuration")
    root.iconbitmap("app_data/favicon.ico")
    root.geometry("500x570")   # Größeres Fenster

    # --- Center window ---
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    # --- Modern styling ---
    root.tk_setPalette(background="#2b2b2b", foreground="white")  # Dunkles Theme
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=6, relief="flat", background="#4CAF50", foreground="white")
    style.configure("TLabel", font=("Arial", 11), background="#2b2b2b", foreground="white")
    style.configure("TCheckbutton", font=("Arial", 11), background="#2b2b2b", foreground="white")
    style.map("TCheckbutton",
          background=[("active", "#3a3a3a"), ("!active", "#2b2b2b")],
          indicatorcolor=[("selected", "#4CAF50"), ("!selected", "#aaaaaa")],
          foreground=[("selected", "white"), ("!selected", "gray")])
    
    # ---------- Variables ----------
    text_var = tk.IntVar(value=0)
    hoverinfo_var = tk.IntVar(value=1)
    line_var = tk.IntVar(value=1)
    earthaxis_var = tk.IntVar(value=0)
    orientationline_var = tk.IntVar(value=0)
    visibility_limits_var = tk.IntVar(value=1)
    distances_var = tk.IntVar(value=1)
    legend_var = tk.IntVar(value=0)  # Standard: Legende anzeigen
    file_path = tk.StringVar(value="objects_UniverseTrip.csv")


    # ---------- Functions ----------
    def select_file():
        filename = filedialog.askopenfilename(filetypes=[("CSV-Files", "*.csv")])
        if filename:
            file_path.set(filename)

    def on_start():
        options = {
            'selected_file': file_path.get(),
            'show_markertext': bool(text_var.get()),
            'show_hoverinfo': bool(hoverinfo_var.get()),
            'show_lines': bool(line_var.get()),
            'show_earthaxis': bool(earthaxis_var.get()),
            'show_orientationline': bool(orientationline_var.get()),
            'show_visibility_limits': bool(visibility_limits_var.get()),
            'show_distances': bool(distances_var.get()),
            'show_legend': bool(legend_var.get())
        }
        root.destroy()
        main(
            options["selected_file"], 
            options["show_markertext"],
            options["show_hoverinfo"],
            options["show_lines"], 
            options["show_earthaxis"], 
            options["show_orientationline"], 
            options["show_visibility_limits"], 
            options["show_distances"],
            options["show_legend"]
        )

    # ---------- Logo ----------
    image = Image.open("app_data/Logo_small.png")
    image = image.resize((60, 60)) # Größe anpassen
    photo = ImageTk.PhotoImage(image)


    # ---------- Header ----------
    header = tk.Label(root, text="UniverseTrip\nConfiguration",image=photo, compound="left", padx= 13, justify="left", font=("Arial", 20, "bold"), anchor="w")
    header.image = photo
    header.pack(fill="x", padx=10, pady=10)

    # ---------- File selection ----------
    file_frame = tk.LabelFrame(root, text="1. Select object file", padx=10, pady=10)
    file_frame.pack(fill="x", padx=20, pady=5)

    tk.Label(file_frame, textvariable=file_path, wraplength=420, height=3, justify="left").pack(anchor="w")
    tk.Button(file_frame, text="Change file", font=("Arial", 12, "bold"), command=select_file).pack(anchor="e", pady=5)

    # ---------- Display options ----------
    options_frame = tk.LabelFrame(root, text="2. Select display options", padx=10, pady=10)
    options_frame.pack(fill="x", padx=20, pady=5)

    ttk.Checkbutton(options_frame, text="Show object names (use for limited amount of objects)", variable=text_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show object names at Mouseover", variable=hoverinfo_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show lines to galactic plane", variable=line_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show Earth axis", variable=earthaxis_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show orientaton line Sun to Galactic center", variable=orientationline_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show visibility limits", variable=visibility_limits_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show distance circles", variable=distances_var).pack(anchor="w")
    ttk.Checkbutton(options_frame, text="Show legend", variable=legend_var).pack(anchor="w")

    # ---------- Start ----------
    start_frame = tk.LabelFrame(root, text="3. Start simulation", padx=10, pady=10)
    start_frame.pack(fill="x", padx=20, pady=10)

    tk.Button(start_frame, text="GO!", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=on_start).pack(pady=5)

    root.mainloop()

"""
*************************************************
Main program
*************************************************
"""
    
def main(file_path, show_markertext, show_hoverinfo, show_lines, show_earthaxis, show_orientationline, show_visibility_limits, show_distances, show_legend):
    # Pfad zur CSV-Datei
    #file_path = "objects_UniverseTrip.csv"  #Dateipfad zur Datendatei, not needed any more bercause this will be defined in GUI

    # Objekte aus der CSV-Datei laden
    objects = load_objects_from_csv(file_path)

    #Radien der Planetenbahnen (in Lichtjahren)(
    orbits = [0.000006130604837, 0.000011415609007, 0.000015855012510, 0.000024099619016, 0.000082234664887, 0.000151468219516, 0.000303570639532, 0.000475121874894, 0.000780172315594] #Planetenbahnen Abstand zur Sonne, Mer, Ven, Erd, Mars, Jup, Sat, Ur, Ne

    # Galaxiencluster-Daten (Name, galaktische Länge, Breite, Sonnenabstand in Lichtjahren)
    clusters = [
        #("Michstraßen Unterguppe", 358.0361,+69.6423,100000),
        #("Andromeda Untergruppe", 121.174, -21.573, 2000000),
        #("NGC 3109 Untergruppe", 262.101645,+23.070174,4000000),
        #("Lokale Gruppe", 196.90362,+52.42248,1500000),
        #("Maffei-Gruppe", 135.8619438310218,-0.5508348562901,12000000),
        #("Sculptor-Gruppe", 97.363851,-87.964547,12000000),
        #("M81-Gruppe", 142.0918223605216,+40.9000561069047,11000000),
        #("CVn-I-Gruppe", 123.3629301340831,+76.0075390900619,15000000),
        #("M83-Gruppe", 314.58357765,+31.97269991,14000000),
        #("Virgo Haufen", 283.8, 74.5, 54000000),
        #("Leo I Gruppe", 234.435360,+57.010408,33000000),
        #("Dorado Gruppe", 265.6312953225876,-43.6912255179016,50000000),
        #("Fornax Gruppe", 236.716405,-53.635640,66000000),
        #("Leo-II-Gruppe", 230.5999,+66.4223,70000000),
        #("Virgo-III-Gruppe", 349.409164,+58.568113,50000000),
        #("Eridanus Galaxienhaufen", 208.773099,-57.808978,70000000),
        #("Coma Cluster", 57.2, 87.8, 320000000)#standardwert
    ]
    
    # 3D-Darstellung
    plot_objects_and_milky_way(objects, orbits, clusters, show_markertext, show_hoverinfo, show_lines, show_earthaxis, show_orientationline, show_visibility_limits, show_distances, show_legend)

if __name__ == "__main__":
    start_gui()
