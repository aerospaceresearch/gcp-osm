# GCP-OSM
(German version below)

An automated solution for detection and location of [Ground Control Points](https://www.groundcontrolpoints.com/) build with QR codes.

## Motivation

Wie should a human, when creating photogrammetry, search for GCPs in images and georeference them manually?
With QR codes we have multiple possibilities to automate that process.

## Possible usage of QR codes

QR codes of sufficient size can be placed on the ground.
The QR code then represents its position.
To achieve this multiple solutions are possible:

1. the QR code represents a OSM node and holds a OSM Node ID
2. the QR has its own coordinates encoded
3. the QR code has a number encoded that acts as an ID that later can be used to map to coordinates.

## Possible workflows

### Existing QR codes

1. Take photos
2. Our python script automatically searches for QR codes and creates a GCP table that can be used for e.g. [OpenDroneMap](https://www.opendronemap.org/)
3. ???
4. Profit

### Lay out OSM QR codes

**This workflow currently is just an idea that has not been thought out fully**

1. Create a node with WorkInProgress tag in the region of the final position on OSM
2. Create QR code with OSM Node ID and QR code generator
3. Lay out QR code (paint, print, pave, plant trees/flowers, etc.)
4. Measure the geolocation of the upper left marker with the best possible accuracy
5. Adjust position in OSM and remove WorkInProgess tag

# Format specification

### QR code Format

A QR code with a fixed size of 25x25 pixels will be used.
This code can hold 32 characters of data. 

#### Position

The center of the upper left position marker will be used as reference point.
A QR code contains three position markers.
The upper left one is the one "in the middle".

### URL schema

`https://osm.to/<type indicator><payload>`

The `<type indicator>` can consist of the following values:

* `n/`, or empty: `<payload>` represents an OSM Node ID in Base64
* `w/`: `<payload>` represents an OSM Way ID in Base64
* `a/`: `<payload>` represents an OSM Area Id in Base64
* `r/`: `<payload>` represents an OSM Relation ID in Base64
* `g/`: `<payload>` represents coordinates in OSM short link quad tiles format
* `l/`: `<payload>` represents a (locally defined) ID, which during analysis is linked with coordinates

Way, Area and Relation are not used as GroundControlPoints but instead can be used to reference other OSM objects.

#### Length of data encoded in QR code

The prefix up to `type indicator` is 15 characters long.
This way 15 characters (or 17 for Node IDs) remain for the actual payload.

OSM IDs are 64-bit integers, which in Base64 are 11 characters long.

With 15 character quad tiles one could achieve an accuracy of 0.3 mm around at the equator.

### OSM IDs as Base64 numbers

To avoid wasting space the OSM IDs are formatted in Base64 with a character set which is inspired by the OSM short link format.
The character set is `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_~`, with `A` representing zero, `B` one, and so on.
The number 64 will be represented as `BA`, 65 as `BB` and so on.

## Project setup
### Create virtual environment
`virtualenv -p python3 venv`

### Activate virtual environment
`source venv/bin/activate`

### Install dependencies
`pip3 install -r requirements.txt`

### Install pyzbar
See [pyzbar documentation](https://github.com/NaturalHistoryMuseum/pyzbar#installation)

### Run unittests
`python3 -m unittest

### Run gcp-osm
`python3 main.py -f <filepath>`

# German version

Eine automatisierte Lösung zur Erkennung und Verortung von GroundControlPoints.

Gebaut mit QR-Codes und Openstreetmap

## Motivation

Warum muss man als Mensch nach einer Photogrammetrieaufnahme selber die GCP auf den Bildern suchen und georeferenzieren?

Wir haben mit QR-Codes vielfältige Möglichkeiten geschaffen, diesen Prozess zu automatisieren.

## Der QR-Code

Ein QR-Code wird in ausreichender Größe auf dem Boden ausgebracht. Dabei repräsentiert der QR-Code immer seine Position. Dafür gibt es verschiedene Möglichkeiten:

* Ein OSM Node. Der QR-Code enthält eine OSM Node ID
* Eine festgelegte Koordiante. Der QR-Code enthält direkt die Koordiante
* Eine Nummer. Der QR-Code ist nummeriert und kann im Nachhinein einer Position zugeordnet werden

## Mögliche Workflows

### Vorhandene QR-Codes

1. Bilder aufnehmen
2. Das Python Skript sucht automatisiert auf den Bildern nach QR-Codes und erzeugt eine GCP-Tabelle
3. Nichts mehr, das wars schon :D

### OSM QR-Code verlegen

**Dieser Workflow ist eine Idee, noch nicht zuende gedacht und sollte noch nicht angewendet werden!!**

1. Einen Node mit WorkInProgress Tag auf der ungefähren Position erzeugen
2. Mit der OSM Node-ID und dem QR-Code Generator einen QR-Code erzeugen
3. Den QR-Code ausbringen (malen, drucken, pflastern, Blumen säen, usw)
4. Die Mitte des oberen linken größen Markers möglichst genau einmessen
5. In OSM die Position korrigieren und das WorkInProgress Tag entfernen

# Spezifikation des Formats

### QR-Code Format

Es wird ein QR-Code mit fester Größe von 25x25 Pixeln genutzt. Dieser kann als Daten 32 Zeichen aufnehmen. 

#### Position

Als Referenzpunkt wird die Mitte des großen Positionmarkers oben links genutzt. (Es gibt davon drei Stück, es ist der "mittlere")

### URL-Schema

`https://osm.to/<type indicator><payload>`

Der `<type indicator>` kann folgende Wert haben:

* `n/`, bzw keiner: `<payload>` stellt eine OSM Node ID zur Basis 64 dar
* `w/`: `<payload>` stellt eine OSM Way ID zur Basis 64 dar
* `a/`: `<payload>` stellt eine OSM Area ID zur Basis 64 dar
* `r/`: `<payload>` stellt eine OSM Relation ID zur Basis 64 dar
* `g/`: `<payload>` stellt eine Koordiante im OSM Shortlink quadtiles format
* `l/`: `<payload>` stellt eine (nur lokal definierte) ID da, welche bei der Auswertung mit einer Koordinate verbunden werden muss

Die Way, Area und Relation werden nicht als GroundControlPoints genutzt, sondern können benutzt werden, andere OSM Objekte zu referenzieren.

#### Länge

Der Prefix bis vor den `type indicator` braucht 15 Zeichen. Somit bleiben noch 15 (bzw 17 für Node IDs) Zeichen für die Payload. 

OSM IDs sind 64 Bit Integer, welche zur Basis 64 maximal 11 Zeichen brauchen.

Mit 15 Zeichen Quadtiles kommt man auf eine Genauigkeit von 0.3mm am Äquator.

### OSM IDs als Zahl zur Basis 64

Um die OSM IDs möglichst platzsparend darzustellen, wird diese zur Basis 64 dargestellt, wobei der Zeichensatz an das OSM Shortlink-Format angelehnt ist. (Das Shortlink-Format nutzt hingegen eine binäre Kodierung wie base64).

Der Zeichensatz ist `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_~`, wobei `A` die Null, `B` die Eins, usw repräsentiert. Die Zahl 64 wird als `BA` und die 65 als `BB` dargestellt.

## Installieren / ausführen
### Virtual environment anlegen
`virtualenv -p python3 venv`

### Virtual environment aktivieren
`source venv/bin/activate`

### Dependencies installieren
`pip3 install -r requirements.txt`

### Install pyzbar
Siehe [pyzbar Dokumentation](https://github.com/NaturalHistoryMuseum/pyzbar#installation)

### gcp-osm ausführen
`python3 main.py -f <filepath>`
