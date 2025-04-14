# UniverseTrip - A trip into the structure of the universe

UniverseTrip ist ein interaktives 3D-Visualisierungsprogramm zur Darstellung kosmischer Objekte im sichtbaren Universum. Die dargestellten Objekte können über eine Objekt-Datei im CSV-Format vom Benutzer beliebig erstellt und angepasst werden. Die Objekte werden im dreidimensionalen Raum maßstabsgetreu an der richtigen Stelle dargestellt, sodass die räumlichen Zusammenhänge veranschaulicht werden. Mithilfe der intuitiven Bedienung mit der Maus und dem Mausrad kann vom Erde-Mond System bishin zum sichtbaren Universum zoomen und navigieren werden.

Dieses Repository enthält optional auch einen separaten Object-List-Creator, mit dessen Hilfe die Objekt-Dateien automatisch erstellt und konfiguriert werden können. Als Input für diesen Objekt-List-Creator dienen mehrere zur Verfügung gestellte MS-Excel Datein, die die aufbereiteten Objektdaten aus der astronomischen Datenbank SIMBAD enthalten.

---

## Features

UniverseTrip
- 3D-Visualisierung kosmischer Objekte vom Erde-Mond-System bishin zum sichtbaren Universum
- Intuitive Navigation mit der Maus und dem Mausrad durch den dreidimensionalen Raum
- Dargestellte Objekte werden durch eine Objektdatei im CSV Format definiert
- Die CSV-Objektdatei kann beliebig mit dem Object-List-Creator erstellt und manuell zusammengestellt und verändert werden
- Konfiguration der Anzeige über ein GUI

UniverseTrip Object-List-Creator
- Erstellung von Objektdatein auf Basis von auswählbarer Objektdatenbank-Datein
- Filterfunktionen, um nur bestimmt Objekte zur berücksichtigen
- Benutzerdefinierter Dateiname für Ausgabedatei (Objektdatei)

---

## Projektstruktur

/universe-trip/ 
- object_database/                     # Objektdatenbanken, als Input für die Erstellung der Objektdatein
- app_data/                            # Datein, die für die Ausführung des Programmes notwendig sind
- UniverseTrip.py                      # Visualisierungsprogramm
- UniverseTrip_ObjectListCreator.py    # Programm für die Generierung von Objektdatein
- README.md                            # readme
- LICENSE                              # Lizenzfile

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
