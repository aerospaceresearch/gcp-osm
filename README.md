# GCP-OSM

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

`https://dom.an/<type indicator><payload>`

**Die Doma(i)n ist noch nicht festgelegt!**

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