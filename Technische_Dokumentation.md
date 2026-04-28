# Technische Dokumentation – BlitzBoard / HHBKTendo Spielesammlung

## 1. Projektübersicht

**BlitzBoard** (intern auch *HHBKTendo*) ist eine Desktop-Spielesammlung mit zwei Brettspielen, die gegen eine KI gespielt werden können. Die Anwendung ist in Python mit einer tkinter-GUI realisiert und wurde im Rahmen eines Berufsschulprojekts entwickelt.

| Eigenschaft | Wert |
|---|---|
| Sprache | Python 3.x |
| GUI-Framework | tkinter (Standardbibliothek) |
| Datenbank | SQLite (über Standardbibliothek `sqlite3`) |
| Architektur | Prozedural / modulbasiert |
| Unterstützte Sprachen | Deutsch, Englisch |
| Optionale Abhängigkeit | Pillow (`pip install Pillow`) – Hintergrundbild im Hauptmenü |

---

## 2. Systemarchitektur

### 2.1 Modulübersicht

```
BlitzBoard/
├── main.py          # GUI, Screens, globaler App-Zustand
├── minimax.py       # Generischer KI-Algorithmus (MiniMax + Alpha-Beta)
├── pawn_chess.py    # Spiellogik Bauernschach
├── tictactoe.py     # Spiellogik Tic-Tac-Toe (4 gewinnt)
├── database.py      # SQLite-Datenbankzugriff
├── auth.py          # Benutzerverwaltung & Authentifizierung
├── test_all.py      # Unittests (TC-01 bis TC-15)
└── games.db         # SQLite-Datenbankdatei (wird bei Start erstellt)
```

### 2.2 Abhängigkeitsdiagramm

```
main.py
  ├── minimax.py
  ├── pawn_chess.py  ──► minimax.py (Konstanten)
  ├── tictactoe.py   ──► minimax.py (Konstanten)
  ├── database.py
  └── auth.py        ──► database.py
```

`main.py` ist der einzige Einstiegspunkt. Die Spiellogikmodule (`pawn_chess.py`, `tictactoe.py`) kennen nur `minimax.py` für die Score-Konstanten. `minimax.py` selbst hat keine Abhängigkeiten zu anderen Projektmodulen.

---

## 3. Modul-Dokumentation

### 3.1 `main.py` – Hauptprogramm & GUI

Enthält die gesamte GUI-Logik sowie den globalen Anwendungszustand.

#### Globaler App-Zustand (`app_state`)

```python
app_state = {
    "language":      "en",    # Aktuelle Sprache ('en' oder 'de')
    "current_screen": None,   # Aktuell angezeigter tkinter-Frame
    "game":          None,    # Aktives Spiel ('pawn_chess' | 'tictactoe')
    "board":         None,    # Aktuelles Spielfeld (2D-Liste)
    "difficulty":    3,       # MiniMax-Suchtiefe (1–5)
    "human_turn":    True,    # True = Mensch am Zug
    "selected":      None,    # Ausgewählte Figur im Bauernschach (row, col)
    "valid_moves":   [],      # Gültige Züge für ausgewählte Figur
    "game_over":     False,
    "ai_thinking":   False,
}
```

#### Wichtige Funktionen

| Funktion | Beschreibung |
|---|---|
| `main()` | Einstiegspunkt: DB initialisieren, Auto-Login prüfen, Fenster starten |
| `show_screen(root, build_fn)` | Screen-Wechsel: alten Frame zerstören, neuen aufbauen |
| `build_login_screen()` | Login/Register-Bildschirm |
| `build_main_menu()` | Hauptmenü mit Spielauswahl und Schwierigkeitsgrad |
| `build_game_screen()` | Spielfeld-Bildschirm (Canvas + Status-Label) |
| `draw_board()` | Spielfeld auf Canvas neu zeichnen |
| `on_board_click(event)` | Click-Handler: Koordinaten → Spielzug |
| `start_ai_turn()` | Startet KI-Berechnung in einem Daemon-Thread |
| `after_ai_turn(winner)` | Wird nach KI-Zug im Hauptthread aufgerufen (via `canvas.after`) |
| `end_game(winner)` | Spielende: Ergebnis anzeigen und ggf. in DB speichern |
| `show_leaderboard()` | Bestenliste als Toplevel-Popup |
| `show_rules()` | Spielregeln als Toplevel-Popup |
| `t(key)` | Übersetzungsfunktion: gibt Text in aktueller Sprache zurück |
| `make_radio_group(parent, options, variable)` | Baut einen gestylten Schwierigkeits-Selektor aus `tk.Label`-Zeilen (◆/◇ Indikator, Hover-Effekt) als Ersatz für native `tk.Radiobutton`-Widgets |

#### Threading-Konzept

Die KI-Berechnung läuft in einem separaten Daemon-Thread (`threading.Thread`), damit die GUI während des Denkens nicht einfriert. Ergebnis-Updates werden mit `canvas.after(0, callback)` sicher in den tkinter-Hauptthread zurückgegeben.

```
Hauptthread (tkinter)          KI-Thread
      │                             │
      │── start_ai_turn() ─────────►│
      │   (setzt ai_thinking=True)  │
      │                             │── mm.get_best_move(...)
      │   GUI bleibt reaktiv        │
      │                             │
      │◄── canvas.after(0, ...) ────│
      │   after_ai_turn(winner)     │
```

---

### 3.2 `minimax.py` – KI-Algorithmus

Implementiert den **MiniMax-Algorithmus mit Alpha-Beta-Pruning** als spielunabhängige, generische Komponente. Das Modul kennt keine Spielregeln – alle spielspezifischen Details werden als Callback-Funktionen übergeben (Strategy Pattern).

#### Konstanten

```python
SCORE_WIN  =  1_000_000   # Terminal: KI gewinnt
SCORE_LOSS = -1_000_000   # Terminal: Mensch gewinnt
SCORE_DRAW =  0
```

#### `minimax(board, depth, is_maximizing, alpha, beta, get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)`

Rekursive MiniMax-Funktion mit Alpha-Beta-Pruning.

| Parameter | Typ | Beschreibung |
|---|---|---|
| `board` | 2D-Liste | Aktuelles Spielfeld |
| `depth` | int | Verbleibende Suchtiefe |
| `is_maximizing` | bool | `True` = KI (Maximizer), `False` = Mensch (Minimizer) |
| `alpha` | float | Alpha-Wert (initialisiert mit `-inf`) |
| `beta` | float | Beta-Wert (initialisiert mit `+inf`) |
| `get_moves_fn` | callable | `fn(board, is_maximizing) → [Züge]` – pawn_chess: `pc.get_valid_moves`, tictactoe: `ttt.get_valid_moves` |
| `apply_move_fn` | callable | `fn(board, move, is_maximizing) → neues Board` – pawn_chess: `pc.apply_move`, tictactoe: `ttt.apply_move` |
| `evaluate_fn` | callable | `fn(board) → int` (heuristische Bewertung) – pawn_chess: `pc.evaluate`, tictactoe: `ttt.evaluate` |
| `is_terminal_fn` | callable | `fn(board) → (bool, int)` – pawn_chess: `pc.is_terminal`, tictactoe: `ttt.is_terminal` |

**Rückgabe:** Numerische Bewertung des besten gefundenen Zuges.

#### Wie der rekursive Abstieg funktioniert

Der Algorithmus baut gedanklich einen **Spielbaum** auf: Jeder Knoten ist ein Brettzustand, jede Kante ein Zug. `get_moves_fn` liefert an jedem Knoten alle möglichen Züge; für jeden davon erzeugt `apply_move_fn` das neue Brett, und `minimax()` ruft sich selbst mit diesem Brett und `depth - 1` auf.

```
minimax(brett, depth=3, is_maximizing=True)      ← KI ist dran
│
├── get_moves_fn → [Zug1, Zug2, Zug3]
│
├── apply_move(Zug1) → brett_A
│   └── minimax(brett_A, depth=2, is_maximizing=False)   ← Mensch ist dran
│       ├── apply_move(Zug1a) → brett_A1
│       │   └── minimax(brett_A1, depth=1, ...)
│       │       └── minimax(..., depth=0) → evaluate_fn() = −5
│       └── apply_move(Zug1b) → brett_A2
│           └── minimax(..., depth=0) → evaluate_fn() = +20
│
├── apply_move(Zug2) → brett_B
│   └── ...
```

Die Rekursion endet bei `depth == 0` (Suchgrenze erreicht) oder wenn `is_terminal_fn` ein Spielende meldet. Ab diesem Punkt werden die Scores nach oben durchgereicht:

- **Maximizer (KI):** wählt den **höchsten** Score seiner Kinder → `best_score = max(best_score, score)`
- **Minimizer (Mensch):** wählt den **niedrigsten** Score seiner Kinder → `best_score = min(best_score, score)`

```
Tiefe 0 (Blätter):   −5      +20      +3      +8
Tiefe 1 (KI):        max(−5, +20) = +20      max(+3, +8) = +8
Tiefe 2 (Mensch):            min(+20, +8) = +8
```

So simuliert der Algorithmus, dass beide Spieler **optimal** spielen.

#### Heuristische Bewertung (`evaluate_fn`)

Wenn `depth == 0` erreicht ist, weiß der Algorithmus nicht mehr, wer das Spiel letztendlich gewinnt. Stattdessen **schätzt** `evaluate_fn` anhand von Faustregeln, wie gut die Stellung für die KI ist (positiv = gut für KI, negativ = gut für Mensch). Diese Schätzung heißt **heuristische Bewertung**.

#### Alpha-Beta-Pruning

`alpha` und `beta` verfolgen, welche Scores die beiden Seiten bisher garantiert erreichen können:

- **alpha** = bester Score, den die KI bisher sicherstellen kann
- **beta** = bester Score, den der Mensch bisher sicherstellen kann

```
KI-Ebene: Zug A wurde bewertet → Score +10, alpha = +10
  Jetzt wird Zug B untersucht...
    Mensch-Ebene: Zug B1 → Score +3, beta = +3
    if beta(+3) <= alpha(+10): break   ← ABBRUCH
```

Der Mensch würde Zug B auf maximal +3 begrenzen. Da die KI mit Zug A bereits +10 sicher hat, wählt sie Zug B ohnehin nie — der restliche Ast wird nicht mehr berechnet, ohne das Endergebnis zu verändern:

```
      [KI]
     /    \
  +10      [Mensch]
            /    \
          +3      ?   ← wird nie berechnet
```

Das Pruning reduziert die Anzahl der zu evaluierenden Knoten erheblich und macht höhere Suchtiefen praktisch möglich.

#### `get_best_move(board, depth, get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)`

Einstiegspunkt für den KI-Zug. Auf den ersten Blick macht `get_best_move` dasselbe wie die oberste Ebene von `minimax()` — der entscheidende Unterschied ist jedoch: `minimax()` gibt nur einen **Score** (eine Zahl) zurück, keinen Zug. `get_best_move` iteriert daher die KI-Züge selbst, merkt sich welcher Zug welchen Score erzeugt, und gibt am Ende **den Zug** zurück.

```python
for move in moves:
    new_board = apply_move_fn(board, move, True)
    score = minimax(new_board, depth - 1, False, ...)  # bewertet die Folgestellung
    if score > best_score:
        best_move = move   # ← hier wird der Zug gespeichert
```

In den rekursiven Zwischenebenen interessiert der Zug nicht — dort zählt nur der Score für `max()`/`min()`. Die Trennung hält `minimax()` einfacher und wiederverwendbar.

**Rückgabe:** Bester Zug oder `None` wenn keine Züge möglich.

---

### 3.3 `pawn_chess.py` – Bauernschach

Implementiert die komplette Spiellogik für Bauernschach auf einem **6×6-Spielfeld**.

#### Konstanten

```python
BOARD_SIZE = 6
EMPTY =  0
WHITE =  1   # Mensch, zieht von Zeile 5 nach oben (Richtung Zeile 0)
BLACK = -1   # KI,    zieht von Zeile 0 nach unten (Richtung Zeile 5)

WHITE_BASELINE = 0   # Ziel für Weiß
BLACK_BASELINE = 5   # Ziel für Schwarz
```

#### Startaufstellung

```
Zeile 0: ♟ ♟ ♟ ♟ ♟ ♟   (Schwarz / KI)
Zeile 1: . . . . . .
Zeile 2: . . . . . .
Zeile 3: . . . . . .
Zeile 4: . . . . . .
Zeile 5: ♙ ♙ ♙ ♙ ♙ ♙   (Weiß / Mensch)
```

#### Zug-Format

Tupel `(from_row, from_col, to_row, to_col)`

#### Funktionen

| Funktion | Beschreibung |
|---|---|
| `create_board()` | Erstellt das Startbrett |
| `get_valid_moves(board, is_maximizing)` | Alle gültigen Züge: vorwärts (wenn frei) + diagonal schlagen |
| `apply_move(board, move, is_maximizing)` | Führt Zug aus, gibt `deepcopy` des neuen Boards zurück |
| `is_terminal(board)` | Prüft Endebedingungen, gibt `(bool, score)` zurück |
| `evaluate(board)` | Heuristische Bewertung: Figurenanzahl + Fortschritt + Zentralbonus |
| `check_winner(board)` | Gibt `'white'`, `'black'` oder `None` zurück |

#### Gewinnbedingungen

1. Ein Bauer erreicht die gegnerische Grundlinie
2. Alle gegnerischen Bauern wurden geschlagen
3. Der Gegner hat keine gültigen Züge mehr

#### Bewertungsfunktion (`evaluate`)

```
Für jede BLACK-Figur:  +10 (Grundwert) + row * 2 (Fortschritt) + 1 (Zentrum)
Für jede WHITE-Figur:  -10 (Grundwert) - (5-row) * 2 (Fortschritt) - 1 (Zentrum)
```

---

### 3.4 `tictactoe.py` – Tic-Tac-Toe (4 gewinnt)

Implementiert **4-gewinnt auf einem 6×6-Spielfeld**. Beide Spieler setzen abwechselnd Steine auf ein beliebiges freies Feld.

#### Konstanten

```python
BOARD_SIZE = 6
EMPTY =  0
HUMAN =  1   # Spielt X
AI    = -1   # Spielt O
WIN_LENGTH = 4   # 4 in einer Reihe zum Gewinnen
```

#### Funktionen

| Funktion | Beschreibung |
|---|---|
| `create_board()` | Leeres 6×6-Brett |
| `get_valid_moves(board, is_maximizing)` | Nur Felder angrenzend an bereits gesetzte Steine (verbessert Alpha-Beta-Effizienz); auf leerem Brett: 4 Mittelfelder |
| `apply_move(board, move, is_maximizing)` | Setzt Stein, gibt Flachkopie zurück (`[row[:] for row in board]`) |
| `is_terminal(board)` | Prüft 4-in-einer-Reihe und volles Brett |
| `evaluate(board)` | Bewertet offene 2er/3er-Reihen + Zentralbonus |
| `check_winner(board)` | Gibt `'human'`, `'ai'`, `'draw'` oder `None` zurück |

#### Optimierungen in `get_valid_moves`

- Kandidatenzüge sind nur Felder mit Nachbarn (Abstand 1) zu bereits gesetzten Steinen. Das reduziert den Verzweigungsgrad erheblich.
- Kandidaten werden nach Zentrumsnähe sortiert, sodass Alpha-Beta-Pruning früher greift.
- Auf leerem Brett werden nur die 4 Mittelfelder angeboten.

#### Bewertungsfunktion (`evaluate`)

```
+50 pro offene KI-Dreier-Reihe
-50 pro offene Mensch-Dreier-Reihe
+10 pro offene KI-Zweier-Reihe
-10 pro offene Mensch-Zweier-Reihe
+Zentralbonus (bis +3) pro KI-Stein in Feldmitte
```

---

### 3.5 `database.py` – Datenbankschicht

Verwaltet alle SQLite-Operationen. Die Datenbankdatei `games.db` liegt im selben Verzeichnis wie das Skript.

#### Datenbankschema

**Tabelle `users`**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `id` | INTEGER PK | Auto-Increment |
| `username` | TEXT UNIQUE | Benutzername (mind. 3 Zeichen) |
| `password_hash` | TEXT | `salt:sha256hash` |
| `language` | TEXT | `'en'` oder `'de'` (Standard: `'en'`) |
| `created_at` | TIMESTAMP | Registrierungsdatum |

**Tabelle `results`**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `id` | INTEGER PK | Auto-Increment |
| `user_id` | INTEGER FK | Verweis auf `users.id` |
| `game` | TEXT | `'pawn_chess'` oder `'tictactoe'` |
| `difficulty` | INTEGER | Schwierigkeitsstufe 1–5 |
| `won` | INTEGER | `1` = Sieg, `0` = Niederlage |
| `played_at` | TIMESTAMP | Zeitpunkt des Spiels |

#### Funktionen

| Funktion | Beschreibung |
|---|---|
| `init_db()` | Tabellen anlegen (inkl. Migration für ältere DBs) |
| `get_connection()` | Verbindung öffnen (`row_factory = sqlite3.Row`) |
| `register_user(username, password_hash, language)` | Neuen User eintragen, gibt ID oder `None` zurück |
| `get_user_by_username(username)` | User-Dict oder `None` |
| `get_user_by_id(user_id)` | User-Dict oder `None` |
| `save_result(user_id, game, difficulty, won)` | Spielergebnis speichern |
| `get_leaderboard(game, difficulty, limit=10)` | Top-10 nach Siegen, gefiltert nach Spiel + Schwierigkeit |
| `get_user_stats(user_id, game=None)` | Statistiken eines Users (optional nach Spiel gefiltert) |
| `update_user_language(user_id, language)` | Sprachpräferenz speichern |

---

### 3.6 `auth.py` – Authentifizierung

Verwaltet Login, Registrierung, Session-Persistenz und das aktuelle Benutzerobjekt.

#### Passwort-Hashing

```
hash_password("geheim")
  → salt = os.urandom(16).hex()   # 32-stelliger Hex-String
  → hash = SHA-256(salt + password)
  → gespeicherter Wert: "salt:hash"
```

Jedes Passwort erhält einen eigenen zufälligen Salt, sodass gleiche Passwörter unterschiedliche Hashes erzeugen (Rainbow-Table-Schutz).

#### Session-Persistenz (Auto-Login)

Bei aktivierter Option "Angemeldet bleiben" wird die User-ID in `session.json` im Projektverzeichnis gespeichert. Beim nächsten Start lädt `load_session()` die ID und ruft `get_user_by_id()` in der DB auf.

#### Funktionen

| Funktion | Beschreibung |
|---|---|
| `register(username, password, language)` | Validierung + Hashing + DB-Eintrag |
| `login(username, password)` | Hash-Vergleich, gibt User-Dict zurück |
| `logout()` | `current_user = None` + Session-Datei löschen |
| `set_current_user(user)` | Setzt den globalen Benutzer |
| `get_current_user()` | Gibt aktuellen User zurück (`None` = Gast) |
| `is_logged_in()` | `True` wenn eingeloggt |
| `is_guest()` | `True` wenn Gast |
| `save_session(user_id)` | Schreibt `session.json` |
| `load_session()` | Liest `session.json` und gibt User zurück |
| `clear_session()` | Löscht `session.json` |

#### Validierungsregeln

- Benutzername: mindestens 3 Zeichen (nach Strip)
- Passwort: mindestens 4 Zeichen

---

## 4. Spielablauf

### 4.1 Programmstart

```
main()
 ├── database.init_db()
 ├── auth.load_session()
 │    ├── Session vorhanden → build_main_menu
 │    └── Keine Session    → build_login_screen
 └── root.mainloop()
```

### 4.2 Spielrunde

```
build_game_screen()
  └── Spielfeld initialisieren + Canvas binden

Mensch-Zug:
  on_board_click()
    ├── Bauernschach: handle_pawn_chess_click()
    └── Tic-Tac-Toe:  handle_tictactoe_click()
          ├── Zug anwenden
          ├── Gewinner prüfen → end_game()
          └── start_ai_turn()

KI-Zug (Daemon-Thread):
  mm.get_best_move(board, depth, get_moves_fn, ...)
    └── canvas.after(0, after_ai_turn)

after_ai_turn():
  ├── draw_board()
  ├── Gewinner? → end_game()
  └── Sonst: human_turn = True

end_game(winner):
  ├── Status-Label anpassen
  ├── database.save_result() (nur bei eingeloggtem User)
  └── Zurück-Button einblenden
```

---

## 5. Schwierigkeitsgrade

Die Schwierigkeit entspricht direkt der **MiniMax-Suchtiefe**:

| Stufe | Tiefe | Bezeichnung |
|---|---|---|
| 1 | 1 | Leicht |
| 2 | 2 | Mittel |
| 3 | 3 | Schwer (Standard) |
| 4 | 4 | Experte |
| 5 | 5 | Meister |

Eine höhere Tiefe bedeutet mehr vorausschauende Züge und eine stärkere KI, erhöht aber auch die Rechenzeit.

---

## 6. Testabdeckung (`test_all.py`)

Die Tests sind in `unittest` geschrieben und abdeckend für alle Kernmodule. Für Tests mit Datenbankzugriff wird eine temporäre SQLite-Datenbank in einem Temp-Verzeichnis verwendet (`tempfile.mkstemp`), sodass keine Produktionsdaten beeinflusst werden.

### Testklassen

| Klasse | Modul | Testfälle |
|---|---|---|
| `TestTicTacToe` | `tictactoe.py` | Brett erstellen, Züge, Gewinner, Terminal, Bewertung |
| `TestPawnChess` | `pawn_chess.py` | Brett erstellen, Züge (TC-05–07), Gewinner (TC-08), Terminal |
| `TestMiniMax` | `minimax.py` | Gewinnzug nehmen, Blockieren (TC-12), Zeitlimit |
| `TestAuth` | `auth.py` | Hashing, Verify, Session-Status |
| `TestDatabase` | `database.py` | Tabellen, CRUD, Bestenliste (TC-14), Trennung nach Schwierigkeit |
| `TestAuthWithDB` | `auth.py` + `database.py` | Register (TC-01–02), Login (TC-03), Gastmodus (TC-04) |
| `TestSession` | `auth.py` | Auto-Login, Session-Datei, Neustart-Simulation |
| `TestLanguage` | `database.py` + `auth.py` | Sprachspeicherung, Update, Isolation |

### Tests ausführen

```bash
# Standard
python test_all.py

# Mit pytest (ausführlicher Output)
python -m pytest test_all.py -v
```

---

## 7. Design & Internationalisierung

### Farbschema (Dark Theme)

Das Design verwendet ein einheitliches Dunkelblau-Farbschema (definiert im `COLORS`-Dict in `main.py`):

| Zweck | Farbe |
|---|---|
| Hintergrund dunkel | `#1a1a2e` |
| Hintergrund mittel | `#16213e` |
| Akzentfarbe (Rot) | `#e94560` |
| Akzentfarbe 2 (Lila) | `#533483` |
| Brett hell | `#eecc99` |
| Brett dunkel | `#8b5e3c` |
| Gültiger Zug | `#2e7d32` |

### Benutzerdefinierte UI-Komponenten

Native tkinter-Widgets werden konsequent durch eigene Label-basierte Komponenten ersetzt, um das Dark-Theme korrekt darzustellen (native Widgets ignorieren Hintergrundfarben auf macOS):

| Komponente | Implementierung | Ersetzt |
|---|---|---|
| Buttons | `tk.Label` + `<Button-1>`-Binding | `tk.Button` |
| Schwierigkeits-Selektor | `make_radio_group()` — Label-Zeilen mit ◆/◇-Indikator, Hover-Highlight und `tk.IntVar`-Bindung | `tk.Radiobutton` |

Der Schwierigkeits-Selektor in `make_radio_group()` zeigt den ausgewählten Eintrag mit Akzentfarbe und Fettschrift (◆), alle anderen gedimmt (◇). Hover-Effekte und Klick-Handler sind direkt auf alle drei Zeilen-Widgets gebunden.

### Mehrsprachigkeit

Alle UI-Texte sind im `TEXTS`-Dict in `main.py` als `{'en': {...}, 'de': {...}}` hinterlegt. Die Hilfsfunktion `t(key)` liest den aktuellen Sprachcode aus `app_state["language"]` und gibt den entsprechenden Text zurück. Die Spracheinstellung wird pro Benutzer in der Datenbank gespeichert.

---

## 8. Dateistruktur zur Laufzeit

```
Projekt-Verzeichnis/
├── main.py
├── minimax.py
├── pawn_chess.py
├── tictactoe.py
├── database.py
├── auth.py
├── test_all.py
├── games.db         ← wird bei erstem Start angelegt
└── session.json     ← wird bei "Angemeldet bleiben" angelegt
```

`games.db` und `session.json` sind Laufzeit-Artefakte und werden automatisch erstellt. Sie können gelöscht werden, um die Anwendung in den Ausgangszustand zurückzusetzen.