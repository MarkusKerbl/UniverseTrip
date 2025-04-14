# UniverseTrip - A trip into the structure of the universe

UniverseTrip ist ein interaktives 3D-Visualisierungsprogramm zur Darstellung kosmischer Objekte im gesamten sichtbaren Universum. Die dargestellten Objekte können über eine Objekt-Datei im CSV-Format vom Benutzer beliebig erstellt und angepasst werden. Die Objekte werden im dreidimensionalen Raum maßstabsgetreu an der richtigen Stelle dargestellt, sodass die räumlichen Zusammenhänge erkennbar werden. Mithilfe der intuitiven Bedienung mit der Maus und dem Mausrad, kann vom Erde-Mond System bishin zum sichtbaren Universum gezoomt und navigiert werden. Das Visualisierungsprogramm wird nach der Konfiguration der Anzeige im Standardbrwoser geöffnet.

Dieses Repository enthält optional auch einen separaten Object-List-Creator, mit dessen Hilfe die Objekt-Dateien automatisch erstellt und konfiguriert werden können. Als Input für diesen Objekt-List-Creator dienen mehrere zur Verfügung gestellte MS-Excel Datein, die die aufbereiteten Objektdaten aus der astronomischen Datenbank SIMBAD enthalten.

---

## Features

### UniverseTrip
- 3D-Visualisierung kosmischer Objekte vom Erde-Mond-System bishin zum sichtbaren Universum
- Intuitive Navigation mit der Maus und dem Mausrad durch den dreidimensionalen Raum
- Dargestellte Objekte werden durch eine Objektdatei im CSV Format definiert
- Die CSV-Objektdatei kann beliebig mit dem Object-List-Creator erstellt und manuell zusammengestellt und verändert werden
- Konfiguration der Anzeige über ein GUI

### UniverseTrip Object-List-Creator
- Erstellung von Objektdatein auf Basis von auswählbarer Objektdatenbank-Datein
- Filterfunktionen, um nur bestimmt Objekte zur berücksichtigen
- Benutzerdefinierter Dateiname für Ausgabedatei (Objektdatei)

---

## Projektstruktur

/universe-trip/ 
- /object_database/                    # Objektdatenbanken, als Input für die Erstellung der Objektdatein
- /app_data/                           # Datein, die für die Ausführung des Programmes notwendig sind
- UniverseTrip.py                      # Visualisierungsprogramm
- UniverseTrip_ObjectListCreator.py    # Programm für die Generierung von Objektdatein
- README.md                            # readme
- LICENSE                              # Lizenzfile

---

## Installation

Installation unter Windows:
- Download und Installation von Python über https://www.python.org/downloads/
- Öffnen der Eingabeaufforderung
- Navigation zum Ordner, in der PIP.exe enthalten ist über cd XXXXX/
- Installation der notwendigen Zusatzpakete über die Befehle
- pip - install ....


- Öffnen des Visualisierungsprogramms und des Object-List-Creators per Doppelklick auf die .py Datei.

---

## Verwendung
### 1. Objektdatei erstellen (optional)
Die angezeigten Objekte werden in einer Objects_X.csv Datei definiert. Eine Objektdatei kann manuell durch zusammenkopieren von vorhanden Objektdatein erstellt werden oder Toolunterstützt mit dem UniverseTrip_ObjectListCreator.py.

 - UniverseTrip_ObjectListCreator.py öffnen
 - Datenbankdatei aus dem Ordner /object_database/ öffnen
 - Konfiguration, welche Objekte in die object_x.csv Datei übernommen werden sollen
 - Definition der Objekt-Datei
 - Durch Klick auf XXXXXXX wird die Objektdatei erstellt.

### 2. Visualisierung starten
- UniverseTrip.py öffnen
- Objectdatei auswählen
- Konfiguration der Anzeigeoptionen
- Mit Klick auf Button "GO!" wird die Visualisierung im Standardbrwoser geöffnet. Das Laden kann je nach Anzahl der Objekte und Rechenleistung mehrere Sekunden dauern. Bitte um etwas Geduld.

---
## Mitgelieferte Objektdaten
FÜr die Erstellung der Objektdaten sind im Ordner "/object_database/" Objektdaten aus verschiedenen astronomischen Katalogen zur Verfügung gestellt.
Um das Programm auf einfache Art direkt verwenden zu können, sind im Ordner "/UniverseTrip/" bereits beispielhafte Objektdatein mit dem Namen "objects_xxx.csv" zu finden.  

objects_Solarsystem.csv - Objekte des Sonnensystems
objects_Supercluster.csv - Zusammenstellung der Galaxienhaufen
objects_NGC.csv - NGC Katalog (Alle Objekte des NGC Katalogs)
objects_HR.csv - HR Katalog (Alle Sterne die Heller als 6,5mag sind)
objects_M.csv - Messier Katalog (Alle Objekte des Messier Katalogs)
objects_UniverseTrip.csv - UniverseTrip Zusammenstellung (Zusammenfassung der schönsten und erwähnenswerten Objekte sowie eine Darstellung der Superhaufen)

---

## Format der Objektdatein
### Objekt Datein
Die CSV-Datei muss folgende Spalten enthalten:
id – Objekt-ID
V – Visuelle Helligkeit
distLj_mean – Mittlere Entfernung in Lichtjahren
objType – Objekttyp
galX, galY, galZ – Galaktische Koordinaten
Beispiel findest du unter data/example.csv.

### Objektdatenbanken
Die .xlsx Datei sollte folgende Spalten enthalten:
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
