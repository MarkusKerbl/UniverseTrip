# UniverseTrip - A trip into the structure of the universe

UniverseTrip ist ein interaktives 3D-Visualisierungsprogramm zur Darstellung kosmischer Objekte im sichtbaren Universum. Die dargestellten Objekte können über eine Objekt-Datei im CSV-Format vom Benutzer beliebig erstellt und angepasst werden.

Dieses Repository enthält optional auch einen separaten Object-List-Creator, mit dessen Hilfe die Objekt-Dateien automatisch konfiguriert und erstellt werden können. Als input für diesen Objekt-List-Creator dienen mehrere zur Verfügung gestellte MS-Excel Datein, die die aufbereiteten Objektdaten aus der astronomischen Datenbank SIMBAD enthalten.

---

## Features

UniverseTrip
- 3D-Visualisierung kosmischer Objekte vom Erde-Mond-System bishin zum sichtbaren Universum
- Dargestellte Objekte werden durch eine Objektdatei im CSV Format definiert
- Die CSV-Objektdatei kann beliebig mit dem Object-List-Creator erstellt und manuell zusammengestellt und verändert werden
- Konfiguration der Anzeige über GUI

UniverseTrip Object-List-Creator
- Erstellung von Objektdatein auf Basis von auswählbarer Objektdatenbank-Datein
- Filterfunktionen für:
  - Objekttypen
  - Helligkeit (in Magnituden)
  - Entfernung (in Lichtjahren)
  - Objekte mit Entfernung 0.0 ignoriert werden
- Benutzerdefinierter Dateiname für Ausgabedatei (Objektdatei)

---

## Projektstruktur

universe-trip/ 
├── universe_trip/ # Visualisierungsprogramm 
├── object_list_creator/ # Generierung der Objektdatein
├── README.md 
├── requirements.txt 
└── LICENSE

---

## Installation

bash
git clone https://github.com/dein-benutzername/universe-trip.git
cd universe-trip
pip install -r requirements.txt

---

## Mitgelieferte Objektdaten
FÜr die Erstellung der Objektdaten sind im Ordner "/UniverseTrip_Object_List_Creator/object_databases" Objektdaten aus verschiedenen astronomischen Katalogen zur Verfügung gestellt.
Um das Programm auf einfache Art direkt verwenden zu können, sind im Ordner "/UniverseTrip/" bereits beispielhafte Objektdatein mit dem Namen "objects_xxx.csv" zu finden.  

---

## Verwendung
1. Daten konfigurieren (optional)
bash
Kopieren
Bearbeiten
python config_tool/config_gui.py
Damit kannst du deine Eingabedateien filtern und vorbereiten.

2. Visualisierung starten
bash
Kopieren
Bearbeiten
python universe_trip/visualizer.py
Öffnet die 3D-Darstellung des Universums mit interaktiver Navigation.

---

## Format der Objektdatein
Die CSV-Datei muss folgende Spalten enthalten:
id – Objekt-ID
V – Visuelle Helligkeit
distLj_mean – Mittlere Entfernung in Lichtjahren
objType – Objekttyp
galX, galY, galZ – Galaktische Koordinaten
Beispiel findest du unter data/example.csv.

---
## Format der Objektdatenbankdatei
Die CSV-Datei sollte folgende Spalten enthalten:
id – Objekt-ID
V – Visuelle Helligkeit
distLj_mean – Mittlere Entfernung in Lichtjahren
objType – Objekttyp
galX, galY, galZ – Galaktische Koordinaten
Beispiel findest du unter data/example.csv.

---
## Lizenz
GPL – siehe LICENSE.

---
## Mitmachen
Du hast Ideen oder Verbesserungsvorschläge? Gerne! Issues und Pull Requests sind willkommen!
