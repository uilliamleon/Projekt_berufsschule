# HHBKTendo Spielesammlung

Strategiespiele-Prototyp mit MiniMax-KI — entwickelt im Rahmen von Lernfeld 5 am HHBK Düsseldorf.

Die Sammlung enthält **Bauernschach** und **Tic-Tac-Toe (4 gewinnt)**, jeweils auf einem 6×6-Spielfeld gegen eine KI, die den MiniMax-Algorithmus mit Alpha-Beta-Pruning verwendet.

---

## Voraussetzungen

- **Python 3.10 oder neuer**  
  Download: https://www.python.org/downloads/
- **tkinter** (in der Python-Standardbibliothek enthalten)
- **Pillow** – für den Hintergrundeffekt im Hauptmenü:

```bash
C:\Users\lgeldmacher\AppData\Local\Programs\Python\Python313\python.exe -m pip install Pillow
```

> Ohne Pillow startet die App trotzdem — der Hintergrundeffekt wird dann einfach weggelassen.

### tkinter auf macOS nachinstallieren (falls nötig)

```bash
brew install python-tk
```

### tkinter auf Linux nachinstallieren (falls nötig)

```bash
sudo apt install python3-tk
```

---

## Installation und Start

1. Repository klonen oder als ZIP herunterladen und entpacken:

```bash
git clone https://github.com/Tasterloster/Projekt_berufsschule.git
cd Projekt_berufsschule
```

2. Anwendung starten:

```bash
python3 main.py
```

Beim ersten Start wird die Datenbankdatei `games.db` automatisch angelegt.

---

## Projektstruktur

```
Projekt_berufsschule/
│
├── main.py          Hauptprogramm: GUI (Login, Menü, Spielscreen, Bestenliste)
├── auth.py          Benutzerverwaltung: Registrierung, Login, Passwort-Hashing
├── database.py      Datenbankzugriff: SQLite CRUD für Benutzer und Spielergebnisse
├── minimax.py       Spielunabhängiger MiniMax-Algorithmus mit Alpha-Beta-Pruning
├── pawn_chess.py    Spiellogik Bauernschach (Züge, Bewertungsfunktion)
├── tictactoe.py     Spiellogik Tic-Tac-Toe 4-gewinnt (Züge, Bewertungsfunktion)
├── test_all.py      Unittests (TC-01 bis TC-15 aus dem Pflichtenheft)
│
├── games.db         SQLite-Datenbank (wird automatisch erstellt)
│
├── Lastenheft/      Lastenheft des Auftraggebers
└── Pflichtenheft/   Pflichtenheft des Projektteams
```

### Modulbeschreibungen

| Datei | Aufgabe |
|-------|---------|
| `main.py` | Einstiegspunkt. Verwaltet den globalen `app_state` und alle tkinter-Screens. |
| `auth.py` | Login und Registrierung. Passwörter werden als SHA-256 + Salt gespeichert, nie im Klartext. |
| `database.py` | Erstellt die SQLite-Datenbank und stellt Funktionen zum Lesen/Schreiben von Benutzern und Ergebnissen bereit. |
| `minimax.py` | Generischer MiniMax mit Alpha-Beta-Pruning. Erhält spielspezifische Funktionen als Parameter — wiederverwendbar für alle Spiele. |
| `pawn_chess.py` | Regeln, gültige Züge und Bewertungsfunktion für Bauernschach. |
| `tictactoe.py` | Regeln, gültige Züge und Bewertungsfunktion für Tic-Tac-Toe (4 gewinnt, 6×6). |

---

## Spielanleitung

### Anmeldung

Beim Start kann man sich **registrieren**, **einloggen** oder als **Gast** spielen.  
Im Gastmodus werden keine Ergebnisse in der Bestenliste gespeichert.

### Spielstärke einstellen

Vor jedem Spiel kann die Suchtiefe der KI gewählt werden:

| Stufe | Suchtiefe | Verhalten |
|-------|-----------|-----------|
| 1 – Leicht | 1 | Kaum strategisch |
| 2 – Mittel | 2 | Einfache Taktiken |
| 3 – Schwer | 3 | Standard |
| 4 – Experte | 4 | Stark |
| 5 – Meister | 5 | Sehr stark, Zug kann mehrere Sekunden dauern |

### Bauernschach

- Figur anklicken → gültige Züge werden grün markiert
- Zielfeld anklicken → Zug ausführen
- Ziel: einen eigenen Bauern auf die gegnerische Grundlinie bringen

### Tic-Tac-Toe (4 gewinnt)

- Freies Feld anklicken → Stein setzen
- Ziel: vier eigene Steine in einer Reihe, Spalte oder Diagonale

### Spielregeln im Spiel

Über die Schaltfläche **Rules / Regeln** können die Spielregeln jederzeit eingeblendet werden.

### Spiel abbrechen

Über **Quit / Abbrechen** kann ein laufendes Spiel mit Bestätigungsdialog beendet werden.

---

## Datenbank

Die Datei `games.db` wird automatisch beim ersten Start erstellt und enthält zwei Tabellen:

| Tabelle | Inhalt |
|---------|--------|
| `users` | Benutzername, Passwort-Hash (salt:sha256), Spracheinstellung |
| `results` | Spielergebnis je Benutzer, Spiel und Schwierigkeitsgrad |

Die Datenbank kann mit [DB Browser for SQLite](https://sqlitebrowser.org/) oder dem SQLite-CLI (`sqlite3 games.db`) eingesehen werden.

---

## Tests ausführen

```bash
python3 test_all.py
```

Oder mit pytest (falls installiert):

```bash
python3 -m pytest test_all.py -v
```

---

## Technische Hinweise

- Die Anwendung ist **prozedural** programmiert (keine Klassen für Spiellogik).
- Der KI-Zug läuft in einem **separaten Thread**, um die GUI nicht zu blockieren (max. 45 Sekunden).
- Buttons sind als `tk.Label` mit Event-Bindings implementiert, da `tk.Button` auf macOS die Hintergrundfarbe ignoriert.
- Zielplattform laut Lastenheft: **Windows 10/11**. Die Anwendung läuft ebenfalls unter macOS und Linux.

---

*HHBKTendo Research Center | HHBK Düsseldorf | Lernfeld 5 | 2026*
