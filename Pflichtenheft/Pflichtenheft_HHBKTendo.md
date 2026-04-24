# Pflichtenheft – HHBKTendo Spielesammlung

**Projekt:** Strategiespiele-Prototyp mit MiniMax-KI
**Auftraggeber:** HHBK Tendo Research Center
**Auftragnehmer:** Projektteam (Lernfeld 5)
**Version:** 2.1
**Datum:** 2026-04-24
**Status:** Entwurf

---

## Inhaltsverzeichnis

1. [Zielbestimmung](#1-zielbestimmung)
2. [Produkteinsatz](#2-produkteinsatz)
3. [Systemübersicht und Architektur](#3-systemübersicht-und-architektur)
4. [Funktionale Anforderungen (MUSS)](#4-funktionale-anforderungen-muss)
5. [Funktionale Anforderungen (SOLL / KANN)](#5-funktionale-anforderungen-soll--kann)
6. [Nicht-funktionale Anforderungen](#6-nicht-funktionale-anforderungen)
7. [Datenmodell](#7-datenmodell)
8. [Benutzerschnittstelle](#8-benutzerschnittstelle)
9. [Globale Variablen und Zustandsmodell](#9-globale-variablen-und-zustandsmodell)
10. [MiniMax-Algorithmus und Bewertungsfunktionen](#10-minimax-algorithmus-und-bewertungsfunktionen)
11. [Testfälle und Abnahmekriterien](#11-testfälle-und-abnahmekriterien)
12. [Dokumentations- und Konzeptanforderungen](#12-dokumentations--und-konzeptanforderungen)
13. [Design und Corporate Identity](#13-design-und-corporate-identity)
14. [Liefergegenstände](#14-liefergegenstände)
15. [Projektplanung](#15-projektplanung)

---

## 1 Zielbestimmung

### 1.1 Mussziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-M01 | LF4000 | Mindestens zwei Strategiespiele sind vollständig spielbar. |
| PF-M02 | LF4010 | Alle Spiele sind in einer einzigen Python-Anwendung mit grafischer Benutzeroberfläche (tkinter) integriert. |
| PF-M03 | LF4020 | Jedes Spiel verwendet ein 6×6-Spielfeld. |
| PF-M04 | LF4030 | Die KI nutzt den MiniMax-Algorithmus für alle Spiele. |
| PF-M05 | LF4040 | Der menschliche Spieler macht immer den ersten Zug; die KI antwortet als zweiter Spieler. |
| PF-M06 | LF4050 | Für jedes Spiel ist die Spielstärke (Suchtiefe 1–5) vor Spielbeginn einstellbar. |
| PF-M07 | LF4060 | Ein laufendes Spiel kann jederzeit abgebrochen werden (mit Bestätigungsdialog). |
| PF-M08 | LF4070 | Benutzer können sich registrieren und anmelden. |
| PF-M09 | LF4080 | Siege und Niederlagen werden je Spiel und Schwierigkeitsgrad in der Datenbank gespeichert. |
| PF-M10 | LF4090 | Im Gastmodus werden keine Ergebnisse gespeichert. |
| PF-M11 | LF4100 | Die Bestenliste ist pro Spiel und Schwierigkeitsgrad separat abrufbar. |
| PF-M12 | LF4110 | Die Spielregeln jedes Spiels sind während des Spiels per Schaltfläche einsehbar. |

### 1.2 Sollziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-S01 | LF4120 | Alpha-Beta-Pruning optimiert den MiniMax-Algorithmus. |
| PF-S02 | LD4220 | Die Bestenliste wird durch SQL-Abfragen aus der Datenbank generiert. |

### 1.3 Kannziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-K01 | LF4130 | Der Benutzer kann die Sprache zwischen Englisch (Standard) und Deutsch umschalten. |
| PF-K02 | LD4230 | Spracheinstellung wird benutzerspezifisch in der Datenbank gespeichert. |
| PF-K03 | LF4000 | Das Spiel Dame kann als drittes Strategiespiel implementiert werden (vereinfachte Regeln, 6×6, MiniMax-KI). |
| PF-K04 | LF4120 | Eine definierte Schnittstelle ermöglicht die Einbindung einer alternativen KI anstelle von MiniMax. |

### 1.4 Abgrenzung (Wont-have)

- Kein Netzwerkbetrieb / Multiplayer (LF4140)

---

## 2 Produkteinsatz

### 2.1 Anwendungsbereich

Freizeitanwendung zum Spielen von Strategiespielen gegen eine KI. Primärzweck: Markttest des MiniMax-Algorithmus und der Spielmechaniken.

### 2.2 Zielgruppe

Testpersonen im Alter 12–99, die Strategiespiele bevorzugen, aus den Märkten: Deutschland, UK, Singapur, USA, Hongkong.

### 2.3 Produktumgebung

| Eigenschaft | Wert |
|-------------|------|
| Betriebssystem | Windows 10 / 11, macOS |
| Programmiersprache | Python 3.10+ |
| GUI-Framework | tkinter (stdlib) |
| Datenbank | SQLite (unabhängig, dateibasiert) |
| Programmierparadigma | Prozedural, funktionsorientiert (keine Klassen für Spiellogik) |

---

## 3 Systemübersicht und Architektur

### 3.1 Modulübersicht

```
HHBKTendo Spielesammlung
│
├── main.py          GUI-Steuerung (Login, Menü, Spielscreen, Bestenliste)
├── auth.py          Authentifizierung (Registrierung, Login, Session)
├── database.py      Datenbankoperationen (SQLite, CRUD)
├── minimax.py       Generischer MiniMax + Alpha-Beta-Pruning (spielunabhängig)
├── pawn_chess.py    Spiellogik Bauernschach (Brett, Züge, Bewertung)
├── tictactoe.py     Spiellogik Tic-Tac-Toe 4-gewinnt (6×6, 4 in einer Reihe, Brett, Züge, Bewertung)
├── test_all.py      Tests, welche die Methoden nach Richtigkeit prüfen (erwartetes Resultat wird geprüft)        
└── games.db         SQLite-Datenbankdatei (auto-generiert beim Start)
```

### 3.2 Schnittstellen zwischen Modulen

Der MiniMax-Algorithmus ist vollständig spielunabhängig. Er erhält spielspezifische Callback-Funktionen:

```
minimax.get_best_move(
    board,           ← aktuelles Spielfeld (2D-Liste)
    depth,           ← Suchtiefe (= Schwierigkeit)
    get_moves_fn,    ← fn(board, is_maximizing) → [Züge]
    apply_move_fn,   ← fn(board, move, is_maximizing) → neues Board
    evaluate_fn,     ← fn(board) → int (positiv = gut für KI)
    is_terminal_fn   ← fn(board) → (bool, int)
)
```

Jedes Spielmodul implementiert exakt diese vier Funktionen. Damit ist **dieselbe KI-Engine** für alle Spiele wiederverwendbar (LN5040).

### 3.3 Datenfluss

```
Benutzerinteraktion (Klick)
    → on_board_click()
    → handle_*_click()
    → Spiellogikmodul (apply_move)
    → draw_board()
    → start_ai_turn() [Thread]
        → minimax.get_best_move()
            → Spiellogikmodul (get_valid_moves, apply_move, evaluate, is_terminal)
        → after_ai_turn() [Hauptthread via .after(0, ...)]
    → end_game() → database.save_result()
```

---

## 4 Funktionale Anforderungen (MUSS)

### 4.1 Spiel: Bauernschach (PF-M01)

**Brettkonfiguration:**
- 6×6 Felder, weiße Bauern (Mensch) in Reihe 5, schwarze Bauern (KI) in Reihe 0
- Repräsentation: `board[row][col]` ∈ {WHITE=1, BLACK=−1, EMPTY=0}

**Erlaubte Züge:**

| Zugart | Bedingung |
|--------|-----------|
| Vorwärtszug | Zielfeld ist leer (direkt vor dem Bauern in Richtung gegnerische Grundlinie) |
| Diagonales Schlagen | Zielfeld enthält gegnerischen Bauern (diagonal vorwärts) |

**Gewinnbedingungen:**

| Zustand | Ergebnis |
|---------|---------|
| Weißer Bauer erreicht Reihe 0 | Mensch gewinnt |
| Schwarzer Bauer erreicht Reihe 5 | KI gewinnt |
| Weiß hat keine Figuren mehr | KI gewinnt |
| Schwarz hat keine Figuren mehr | Mensch gewinnt |
| Aktueller Spieler hat keine gültigen Züge | Gegner gewinnt |

Unentschieden ist nicht möglich.

**Bewertungsfunktion:**
```
score = Σ (Figurwert + Fortschritt × 2 + Zentrumbonus) für KI-Figuren
      − Σ (Figurwert + Fortschritt × 2 + Zentrumbonus) für Menschen-Figuren
```
- Figurwert: 10 Punkte pro Figur
- Fortschritt: Anzahl der Reihen, die eine Figur vorgerückt ist
- Zentrumbonus: +1 für Spalten 1–4

---

### 4.2 Spiel: Tic-Tac-Toe (4 gewinnt) (PF-M01)

**Brettkonfiguration:**
- 6×6 Felder, leer zu Spielbeginn
- Repräsentation: `board[row][col]` ∈ {HUMAN=1, AI=−1, EMPTY=0}

**Spielregeln:**
- Spieler setzen abwechselnd einen Stein auf ein leeres Feld
- Mensch beginnt (X), KI antwortet (O)

**Gewinnbedingungen:**

| Zustand | Ergebnis |
|---------|---------|
| 4 in einer Reihe (horizontal) | Erster Spieler gewinnt |
| 4 in einer Spalte (vertikal) | Erster Spieler gewinnt |
| 4 diagonal | Erster Spieler gewinnt |
| Brett voll (36 Felder), kein Gewinner | Unentschieden |

**Bewertungsfunktion:**
```
score = (3er-Linien KI) × 50 − (3er-Linien Mensch) × 50
      + (2er-Linien KI) × 10 − (2er-Linien Mensch) × 10
      + Zentrumsnähe-Bonus
```
Nur offene Linien (ohne gegnerische Steine im Fenster) werden gezählt.

---

### 4.3 KI-System (PF-M04)

Die KI verwendet den **MiniMax-Algorithmus mit Alpha-Beta-Pruning**. Algorithmus, Spielbaum, Pseudocode und die spielunabhängige Schnittstelle sind vollständig in **Abschnitt 10** dokumentiert.

**Funktionale Anforderungen an das KI-System:**

- Fünf wählbare Schwierigkeitsgrade (Suchtiefe 1–5), einstellbar vor Spielbeginn (PF-M06)
- KI-Zug wird in einem separaten Thread ausgeführt, um die GUI nicht zu blockieren (LN5010)
- Maximale Berechnungszeit: 45 Sekunden pro Zug
- Derselbe Algorithmus wird für alle Spiele verwendet (LN5040)

---

### 4.4 Benutzerverwaltung (PF-M08–M10)

| Funktion | Beschreibung |
|----------|-------------|
| Registrierung | Benutzername (min. 3 Zeichen), Passwort (min. 4 Zeichen), Eindeutigkeit geprüft |
| Login | Benutzername + Passwort, Verifikation gegen gespeicherten Hash |
| Gastmodus | Spiel ohne Registrierung, keine Speicherung |
| Passwort-Hashing | SHA-256 + 16-Byte Zufalls-Salt, Format: `salt:hash` |

---

### 4.5 Bestenliste (PF-M09, M11)

- Speicherung: User-ID, Spielname, Schwierigkeitsgrad, gewonnen (0/1)
- Abfrage: gruppiert nach Benutzer, sortiert nach Siegen absteigend
- Anzeige: Rang, Benutzername, Siege, Niederlagen, Gesamt-Spiele
- Unentschieden (nur Tic-Tac-Toe) werden nicht gespeichert

---

## 5 Funktionale Anforderungen (SOLL / KANN)

### 5.1 Sprachumschaltung (PF-K01)

- Umschaltung zwischen EN (Standard) und DE jederzeit möglich
- Alle UI-Texte, Regeln und Statusmeldungen werden in der gewählten Sprache angezeigt
- Spracheinstellung wird bei eingeloggten Benutzern in der DB persistiert

---

## 6 Nicht-funktionale Anforderungen

| ID | Anforderung | Maßnahme |
|----|-------------|----------|
| NF-01 (LN5000) | Python + geeignetes GUI-Framework | Python 3.10+, tkinter |
| NF-02 (LN5001) | Prozedurale Programmierung | Keine Klassen für Spiellogik; Module mit Funktionen |
| NF-03 (LN5010) | KI-Zug max. 45 Sekunden | KI in separatem Thread |
| NF-04 (LN5020) | Persistente Benutzerdaten | SQLite-Datenbankdatei |
| NF-05 (LN5030) | Passwörter nicht im Klartext | SHA-256 + Salt (auth.py) |
| NF-06 (LN5040) | Wiederverwendbare Software | Generischer MiniMax, spielunabhängige Schnittstelle |
| NF-07 (LN5050) | Intuitive Bedienung | Einheitliches Design, klare Labels, Statusanzeige |
| NF-08 (LN5060) | Brand Identity | Dunkles Farbschema (HHBKTendo CI), konsistentes Layout |
| NF-09 | Plattformkompatibilität | Buttons als `tk.Label` mit Bindings implementiert, da macOS den `bg`/`fg`-Parameter von `tk.Button` ignoriert |

---

## 7 Datenmodell

### 7.1 Tabelle: `users`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | INTEGER PK AUTO | Primärschlüssel |
| username | TEXT UNIQUE NOT NULL | Eindeutiger Benutzername |
| password_hash | TEXT NOT NULL | SHA-256-Hash mit Salt (Format: `salt:hash`) |
| language | TEXT DEFAULT 'en' | Sprachpräferenz |
| created_at | TIMESTAMP | Registrierungszeitpunkt |

### 7.2 Tabelle: `results`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | INTEGER PK AUTO | Primärschlüssel |
| user_id | INTEGER FK | Verweis auf `users.id` |
| game | TEXT | `'pawn_chess'` oder `'tictactoe'` |
| difficulty | INTEGER | Suchtiefe 1–5 |
| won | INTEGER | 1 = Sieg, 0 = Niederlage |
| played_at | TIMESTAMP | Zeitpunkt des Spielendes |

### 7.3 Bestenlisten-Abfrage (SQL)

```sql
SELECT u.username,
       SUM(r.won)       AS wins,
       SUM(1 - r.won)   AS losses,
       COUNT(*)         AS total_games
FROM results r
JOIN users u ON r.user_id = u.id
WHERE r.game = ? AND r.difficulty = ?
GROUP BY r.user_id
ORDER BY wins DESC, losses ASC
LIMIT 10;
```

---

## 8 Benutzerschnittstelle

### 8.1 Bildschirmfluss

```
Startbildschirm (Login/Register)
    ├── [Login]       → Hauptmenü
    ├── [Register]    → Hauptmenü
    └── [Als Gast]    → Hauptmenü
         │
         ├── [Bauernschach spielen] → Spielscreen
         │       ├── [Regeln]      → Regelpopup
         │       ├── [Abbrechen]   → Hauptmenü (mit Bestätigung)
         │       └── [Spielende]   → Ergebnis anzeigen → Hauptmenü
         │
         ├── [Tic-Tac-Toe spielen] → Spielscreen (analog)
         │
         ├── [Bestenliste]         → Bestenlisten-Popup
         └── [Abmelden]            → Startbildschirm
```

### 8.2 Spielfeld-Design

**Bauernschach:**
- Helles Feld: `#eecc99`, Dunkles Feld: `#8b5e3c`
- Weiße Figur: weißer Kreis (`#ffffff`) mit ♙-Symbol, schwarzer Kontur
- Schwarze Figur: dunkler Kreis (`#1a1a2e`) mit ♟-Symbol, helle Kontur
- Ausgewählte Figur: rotes Feld, gültige Züge: grünes Feld

**Tic-Tac-Toe (6×6):**
- X (Mensch): hellblau (`#64b5f6`), dicke Linien
- O (KI): rot (`#ef5350`), dicke Ovallinie

### 8.3 Farbschema (CI)

| Element | Farbe | Hex |
|---------|-------|-----|
| Hintergrund dunkel | Nacht-Marine | `#1a1a2e` |
| Hintergrund Karten | Dunkel-Blau | `#0f3460` |
| Akzent (Buttons, Titel) | HHBKTendo-Rot | `#e94560` |
| Akzent2 (Sekundär) | Lila | `#533483` |
| Text (Standard) | Hellgrau | `#eaeaea` |

---

## 9 Globale Variablen und Zustandsmodell

Das gesamte Laufzeit-Zustand der Anwendung ist im Dictionary `app_state` in `main.py` konzentriert (LN5001):

| Variable | Typ | Bedeutung |
|----------|-----|-----------|
| `app_state["language"]` | str | Aktuelle Sprache ('en'/'de') |
| `app_state["current_screen"]` | tk.Frame | Aktuell angezeigter Screen |
| `app_state["game"]` | str | Aktives Spiel ('pawn_chess'/'tictactoe') |
| `app_state["board"]` | list[list[int]] | Aktuelles 6×6-Spielfeld |
| `app_state["difficulty"]` | int | Suchtiefe 1–5 |
| `app_state["human_turn"]` | bool | True = Mensch am Zug |
| `app_state["selected"]` | tuple\|None | Ausgewählte Figur (Bauernschach) |
| `app_state["valid_moves"]` | list | Gültige Züge der ausgewählten Figur |
| `app_state["game_over"]` | bool | True nach Spielende |
| `app_state["ai_thinking"]` | bool | True während KI-Berechnung |

In `auth.py`:

| Variable | Typ | Bedeutung |
|----------|-----|-----------|
| `current_user` | dict\|None | Aktuell eingeloggter Benutzer (None = Gast) |

---

## 10 MiniMax-Algorithmus und Bewertungsfunktionen

### 10.1 Grundprinzip

MiniMax ist ein rekursiver Entscheidungsalgorithmus für Zwei-Spieler-Nullsummenspiele. Beide Spieler werden als optimal handelnd angenommen:

- Der **Maximizer** (KI) wählt stets den Zug mit dem **höchsten** Bewertungswert.
- Der **Minimizer** (Mensch) wählt stets den Zug mit dem **niedrigsten** Bewertungswert.

Alle Spielstellungen werden mit einer numerischen Bewertung versehen: **positiv = vorteilhaft für die KI, negativ = vorteilhaft für den menschlichen Spieler**. Der Algorithmus simuliert so rekursiv die optimale Reaktion beider Seiten bis zu einer definierten Suchtiefe.

### 10.2 Spielbaum

Der Algorithmus baut einen Baum aller möglichen Spielverläufe auf. Jeder Knoten repräsentiert eine Spielstellung; jeder Ast einen möglichen Zug. An den Blättern (Tiefenlimit oder Spielende) wird die Stellung bewertet:

```
              KI zieht (Maximizer)
             /          |          \
          Zug A        Zug B       Zug C
            |            |           |
       Mensch zieht  Mensch zieht  Mensch zieht   ← Minimizer
        /      \      /      \
    Zug A1   Zug A2  Zug B1  Zug B2
      |          |     |        |
     +10         -5   +3       +8       ← evaluate(board)
```

Der Minimizer wählt auf seiner Ebene das Minimum: Ast A liefert −5 (Minimizer wählt A2), Ast B liefert +3 (Minimizer wählt B1). Der Maximizer wählt daraus das Maximum: **Ast B mit +3** wird gespielt.

### 10.3 Rekursiver Ablauf

Der Algorithmus arbeitet in zwei alternierenden Modi:

**Maximizer-Modus (KI zieht):**
```
best_score = -∞
Für jeden möglichen Zug:
    Führe Zug auf Kopie des Spielfelds aus
    score = minimax(neues Spielfeld, tiefe−1, Minimizer)
    best_score = max(best_score, score)
Gib best_score zurück
```

**Minimizer-Modus (Mensch zieht):**
```
best_score = +∞
Für jeden möglichen Zug:
    Führe Zug auf Kopie des Spielfelds aus
    score = minimax(neues Spielfeld, tiefe−1, Maximizer)
    best_score = min(best_score, score)
Gib best_score zurück
```

**Abbruchbedingungen** (Blätter des Baums):
- Das Spiel ist beendet (Sieg, Niederlage, Unentschieden) → terminaler Score wird sofort zurückgegeben
- Die maximale Suchtiefe ist erreicht → `evaluate(board)` bewertet die aktuelle Stellung heuristisch

### 10.4 Illustrationsdiagramm

```
        maximize (KI)
         /          \
    +3              -2
   minimize       minimize
   /    \         /    \
 +3     +5     -2     -9
```

Die KI wählt den Zug, der zum Wert +3 führt. Begründung: Der Minimizer wählt auf der linken Seite +3 (statt +5, da er den schlechtesten Wert für die KI bevorzugt) und auf der rechten Seite −2. Der Maximizer wählt +3 gegenüber −2.

### 10.5 Alpha-Beta-Pruning

Ohne Optimierung müsste der Algorithmus jeden Ast des Spielbaums vollständig durchsuchen. Alpha-Beta-Pruning reduziert den Rechenaufwand, indem Äste abgeschnitten werden, sobald feststeht, dass sie das Ergebnis nicht mehr verbessern können.

**Zwei Grenzwerte werden mitgeführt:**

- **Alpha (α)**: Der bisher beste garantierte Score für den Maximizer. Wird nach oben weitergegeben und erhöht sich nur.
- **Beta (β)**: Der bisher beste garantierte Score für den Minimizer. Wird nach unten weitergegeben und verringert sich nur.

**Abbruchkriterium:** Sobald `β ≤ α` gilt, werden alle verbleibenden Geschwisterknoten übersprungen.

**Beispiel:**
```
KI bewertet Zug A → Score +8  →  alpha = 8
KI bewertet Zug B, Minimizer schaut B1 an → Score +3  →  beta = 3
Da beta(3) ≤ alpha(8): Züge B2, B3, ... werden nicht mehr berechnet. ✂️
```
Der Minimizer kann bei Ast B höchstens +3 erzwingen – das ist schlechter als das bereits gesicherte +8 aus Ast A. Ast B ist daher irrelevant.

**Einsparung:** Im besten Fall O(b^(d/2)) statt O(b^d) Knoten (b = Verzweigungsgrad, d = Tiefe). Bei Suchtiefe 5 kann dies die Knotenanzahl auf die Wurzel des ursprünglichen Wertes reduzieren.

### 10.6 Terminale Bewertungen

| Zustand | Score |
|---------|-------|
| KI gewinnt | +1.000.000 |
| Mensch gewinnt | −1.000.000 |
| Unentschieden | 0 |
| Tiefenlimit (Blatt) | evaluate(board) |

Die hohen terminalen Werte (±1.000.000) stellen sicher, dass ein tatsächlicher Sieg oder eine Niederlage immer stärker gewichtet wird als jede heuristische Zwischenbewertung, unabhängig davon in welcher Suchtiefe das Spielende erreicht wird.

### 10.7 Schwierigkeitsgrade und Zeitverhalten

Die Suchtiefe des Algorithmus ist direkt an den gewählten Schwierigkeitsgrad gekoppelt. Eine höhere Suchtiefe führt zu einer stärkeren, aber rechenintensiveren KI:

| Level | Suchtiefe | Verhalten |
|-------|-----------|-----------|
| 1 – Leicht | 1 | Nur einen Zug voraus, kaum strategisch |
| 2 – Mittel | 2 | Einfache Taktiken erkannt |
| 3 – Schwer | 3 | Mittlere Planung (Standard) |
| 4 – Experte | 4 | Starke KI, schwer zu schlagen |
| 5 – Meister | 5 | Sehr starke KI, Zug kann mehrere Sekunden dauern |

Der KI-Zug wird in einem separaten Thread ausgeführt (LN5010), damit die GUI während der Berechnung nicht einfriert. Das maximale Zeitlimit beträgt 45 Sekunden pro Zug.

### 10.8 Spielunabhängige Schnittstelle

Die Implementierung in `minimax.py` kennt keine spielspezifische Logik. Alle spielabhängigen Operationen werden als Callback-Funktionen übergeben:

```python
get_best_move(
    board,              # aktuelles Spielfeld (2D-Liste)
    depth,              # Suchtiefe (= gewählter Schwierigkeitsgrad)
    get_moves_fn,       # fn(board, is_maximizing) → Liste aller gültigen Züge
    apply_move_fn,      # fn(board, move, is_maximizing) → neues Board (Kopie)
    evaluate_fn,        # fn(board) → int  (positiv = gut für KI)
    is_terminal_fn      # fn(board) → (bool, int|None)
)
```

Dieselbe KI-Engine wird dadurch für Bauernschach und Tic-Tac-Toe wiederverwendet (LN5040). Ein weiteres Spiel erfordert lediglich die Implementierung dieser vier Funktionen – `minimax.py` selbst bleibt unverändert.

---

## 11 Testfälle und Abnahmekriterien

### 11.1 Funktionstests

| TC-ID | Testfall | Erwartetes Ergebnis |
|-------|----------|---------------------|
| TC-01 | Registrierung mit gültigem Namen/Passwort | Benutzer angelegt, Login möglich |
| TC-02 | Registrierung mit bereits vergebenem Namen | Fehlermeldung "Username already taken" |
| TC-03 | Login mit falschem Passwort | Fehlermeldung "Incorrect password" |
| TC-04 | Gastmodus – Spiel beenden | Kein Eintrag in Datenbank |
| TC-05 | Bauernschach – Zug vorwärts auf leeres Feld | Bauer bewegt sich |
| TC-06 | Bauernschach – Zug auf eigene Figur | Zug wird verweigert |
| TC-07 | Bauernschach – Diagonales Schlagen | Gegnerischer Bauer wird entfernt |
| TC-08 | Bauernschach – Bauer erreicht Grundlinie | Spiel endet mit korrektem Gewinner |
| TC-09 | TTT – 4 in einer Reihe (horizontal) | Spiel endet, Gewinner korrekt |
| TC-10 | TTT – 4 in einer Diagonale | Spiel endet, Gewinner korrekt |
| TC-11 | TTT – Alle 36 Felder belegt ohne Gewinner | Unentschieden angezeigt |
| TC-12 | KI-Zug bei Suchtiefe 5 | KI zieht innerhalb 45 Sekunden |
| TC-13 | Spielabbruch | Bestätigungsdialog, Rückkehr ins Hauptmenü |
| TC-14 | Bestenliste anzeigen | Korrekte Sortierung nach Siegen |
| TC-15 | Sprachwechsel EN → DE | Alle UI-Texte auf Deutsch |

### 11.2 Abnahmekriterien (aus Lastenheft)

- Alle MUSS-Anforderungen (PF-M01 bis PF-M12) sind implementiert und testbar
- Live-Demo zeigt mind. 2 vollständige Spiele gegen KI
- Bestenliste zeigt korrekte Ergebnisse eingeloggter Benutzer
- Passwörter sind nicht im Klartext in der DB gespeichert (prüfbar per DB-Viewer)
- Anwendung startet auf Zielumgebung (Windows 10/11) mit `python main.py`

---

## 12 Dokumentations- und Konzeptanforderungen

### 12.1 Benutzerdokumentation

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|-------------|
| DOC-01 | LD5100 | Die Benutzerdokumentation ermöglicht einer nicht am Projekt beteiligten Person die eigenständige Installation und Ausführung der Anwendung. |

### 12.2 Technische Dokumentation

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|-------------|
| DOC-02 | LD5200 | Beschreibung des Spielverhaltens zur Laufzeit (Zustandsübergänge, Spielablauf). |
| DOC-03 | LD5210 | Erläuterung des MiniMax-Algorithmus und der Bewertungsfunktionen je Spiel, inkl. Schwierigkeitsgrad. |
| DOC-04 | LD5220 | Beschreibung der Software-Architektur (Module, Schnittstellen, Datenfluss). |
| DOC-05 | LD5230 | Beschreibung aller verwendeten globalen Variablen und des zentralen `app_state`-Dictionaries. |

### 12.3 Abschlusspräsentation

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|-------------|
| DOC-06 | LD5300 | SOLL/IST-Vergleich der realisierten Features (Lastenheft vs. Pflichtenheft vs. Umsetzung vs. Test). |
| DOC-07 | LD5310 | SOLL/IST-Vergleich der Projektplanung (Pflichtenheft-Zeitplan vs. tatsächlicher Projektverlauf). |
| DOC-08 | LD5320 | Darstellung wesentlicher Softwarekomponenten oder Ideen (z. B. MiniMax, Bewertungsfunktion, GUI). |
| DOC-09 | LD5330 | Aufführung verwendeter Quellen und Werkzeuge (Bibliotheken, Referenzen, KI-Tools). |
| DOC-10 | LD5340 | Fazit zum Projektverlauf: Zusammenarbeit, Aufwand, Lessons learnt. |

### 12.4 Konzept Corporate Identity & Branding

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|-------------|
| DOC-11 | LD5400 | Das CI-Konzept begründet die gewählten Design-Elemente und enthält ein Mission und Vision Statement für die Marke HHBKTendo. |
| DOC-12 | LD5410 | Englischsprachiges Pitch-Konzept inkl. Skript für eine mündliche Präsentation mit überzeugender Argumentation für potenzielle Investoren und hohem Aufmerksamkeitswert. |

### 12.5 Konzept Arbeitszeitgestaltung

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|-------------|
| DOC-13 | LD5500 | Das Konzept stellt Plan- und IST-Arbeitszeiten gegenüber, benennt Risiken und Herausforderungen und formuliert Empfehlungen für künftige Rahmenbedingungen der Projektarbeit bei HHBKTendo. |

---

## 13 Design und Corporate Identity

### 13.1 Markenidentität (Brand Identity)

HHBKTendo positioniert sich als modernes, technologiegetriebenes Spielestudio mit einem klaren Fokus auf algorithmische KI. Das visuelle Erscheinungsbild soll diesen Anspruch transportieren: **präzise, dunkel, modern** – wie die Oberfläche eines High-End-Gaming-Setups. Die Farbwelt orientiert sich bewusst an professioneller Gaming-Ästhetik und hebt sich damit von den pastelligen UI-Konventionen klassischer Business-Software ab.

**Mission:** Strategiespiele mit echter KI-Herausforderung für ein internationales Publikum zugänglich machen.

**Vision:** HHBKTendo als führende Marke für algorithmisch gestützte Einzelspieler-Strategiespiele im B2C-Markt etablieren.

---

### 13.2 Farbpalette

Die gesamte Farbwelt folgt dem offiziellen **HHBKTendo Design System (Investor Edition)**. Jede Farbe hat eine definierte semantische Rolle und einen CSS-Token-Namen sowie eine korrespondierende Python-Variable.

| CSS-Token | Python-Variable | Hex | Name | Rolle |
|-----------|-----------------|-----|------|-------|
| `--bg-deep` | `BG_DEEP` | `#0d0f1a` | Deep Navy | App-Hintergrund aller Screens |
| `--bg-card` | `BG_CARD` | `#1a2040` | Card Navy | Karten, Container, Dialoge |
| `--bg-mid` | `BG_MID` | `#1e2850` | Mid Navy | Eingabefelder, Surfaces, Header |
| `--primary` | `PRIMARY` | `#e8365d` | Hot Pink | Primär-CTA, Logo, Danger-Aktionen |
| `--secondary` | `SECONDARY` | `#6c3fc5` | Royal Purple | Sekundäre Buttons (Register, Leaderboard) |
| `--accent` | `ACCENT` | `#00d4ff` | Cyber Cyan | Active States, Outlines, Hover |
| `--text-primary` | `TEXT_PRIMARY` | `#ffffff` | White | Primärtext, Labels |
| `--text-secondary` | `TEXT_SECONDARY` | `#8a9cc0` | Slate Blue | Sekundärtext, Statuszeilen |
| `--text-muted` | `TEXT_MUTED` | `#4a5680` | – | Dezenter Text, Hints, Platzhalter |

#### Spielfeld-Farben

| Token | Hex | Verwendung |
|-------|-----|------------|
| `board_light` | `#eecc99` | Helle Felder Bauernschach – klassisches Schach-Beige |
| `board_dark` | `#8b5e3c` | Dunkle Felder Bauernschach – warmes Holzbraun |
| `ttt_x` | `#00d4ff` | X-Stein (Mensch) in Tic-Tac-Toe – orientiert an ACCENT (Cyber Cyan): kühl, präzise |
| `ttt_o` | `#e8365d` | O-Stein (KI) in Tic-Tac-Toe – orientiert an PRIMARY (Hot Pink): aggressiv, Gegner |
| `valid_move` | `#2e7d32` | Gültige Züge (Bauernschach) – Grün: „hier kann ich hin" |
| `highlight` | `#e8365d` | Ausgewählte Figur – PRIMARY Hot Pink: „das ist aktiv" |

---

### 13.2.1 Darkmode - Funktion

### Anforderungen
- Umschaltbar (Light/Dark)
- Speicherung der Auswahl
- Systemeinstellung berücksichtigen

### 13.3 Typografie

Das Design System definiert zwei Schriftfamilien mit unterschiedlichen Einsatzbereichen:

**Display & Headings – Orbitron**

| Einsatz | Schriftart | Gewicht | Größe |
|---------|-----------|---------|-------|
| Logo / Haupttitel (HHBKTendo) | Orbitron | 900 (Black) | 28 pt |
| Screen-Überschriften (H1) | Orbitron | 700 (Bold) | 16 pt |
| Karten-Titel, Spielname (H2) | Orbitron | 400 (Regular) | 13 pt |

**Body, Buttons & Labels – Exo 2**

| Einsatz | Schriftart | Gewicht | Größe |
|---------|-----------|---------|-------|
| Buttons | Exo 2 | 700 (Bold) | 11 pt |
| Labels, Fließtext | Exo 2 | 400 (Regular) | 11–12 pt |
| Statuszeilen, Hints | Exo 2 | 300 (Light) | 9–10 pt |
| Spielfigur-Symbole (Bauernschach) | Exo 2 / System | 700 (Bold) | 22 pt |

Orbitron und Exo 2 sind als Google Fonts frei verfügbar. Im tkinter-Fallback (keine Netzwerkinstallation) werden sie durch `Courier` (Orbitron) bzw. `Helvetica` (Exo 2) ersetzt. Die Zielplattform Windows 10/11 unterstützt beide Schriften ohne Einschränkungen.

---

### 13.4 UI-Mockups

Die folgenden Mockups zeigen den finalen Screenfluss der Anwendung. Farbreferenzen beziehen sich auf die Palette aus Abschnitt 13.2.

#### 13.4.1 Login-Screen

```
┌─────────────────────────────────────────────┐  bg-deep #0d0f1a
│                                             │
│              HHBKTendo                      │  ← primary #e8365d, 28pt Orbitron 900
│        HHBKTendo Game Collection            │  ← text-secondary #8a9cc0, 13pt Exo 2
│                                             │
│  ┌───────────────────────────────────────┐  │  bg-card #1a2040
│  │                                       │  │
│  │  Username                             │  │  ← text-primary #ffffff
│  │  ┌─────────────────────────────────┐  │  │  bg-mid #1e2850
│  │  │                                 │  │  │  ← Eingabefeld
│  │  └─────────────────────────────────┘  │  │
│  │                                       │  │
│  │  Password                             │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │  ••••••••                       │  │  │
│  │  └─────────────────────────────────┘  │  │
│  │                                       │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │            Login                │  │  │  ← primary #e8365d
│  │  └─────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │           Register              │  │  │  ← secondary #6c3fc5
│  │  └─────────────────────────────────┘  │  │
│  │  ─────────────────────────────────    │  │  ← Trennlinie
│  │  ┌─────────────────────────────────┐  │  │
│  │  │        Play as Guest            │  │  │  ← text-muted #4a5680
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
│                              [ DE / EN ]    │  ← text-secondary #8a9cc0
└─────────────────────────────────────────────┘
```

#### 13.4.2 Hauptmenü

```
┌─────────────────────────────────────────────────────────────┐  bg-deep #0d0f1a
│  ████ HHBKTendo   alice              [ DE/EN ]  [ Logout ]  │  bg-mid #1e2850 (Header)
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    Select a Game                            │  ← 16pt Orbitron 700
│                                                             │
│  ┌──────────────────────────┐  ┌──────────────────────────┐ │  bg-card #1a2040
│  │      Pawn Chess          │  │  Tic-Tac-Toe (4 in a Row)│ │  ← 13pt Orbitron 400
│  │                          │  │                          │ │
│  │  Difficulty              │  │  Difficulty              │ │
│  │  ○ Easy                  │  │  ○ Easy                  │ │
│  │  ○ Medium                │  │  ○ Medium                │ │
│  │  ● Hard          ←Standard  │  ● Hard                  │ │
│  │  ○ Expert                │  │  ○ Expert                │ │
│  │  ○ Master                │  │  ○ Master                │ │
│  │                          │  │                          │ │
│  │  ┌──────────────────┐    │  │  ┌──────────────────┐    │ │
│  │  │      Play        │    │  │  │      Play        │    │ │  ← primary #e8365d
│  │  └──────────────────┘    │  │  └──────────────────┘    │ │
│  │  ┌──────────────────┐    │  │  ┌──────────────────┐    │ │
│  │  │   Leaderboard    │    │  │  │   Leaderboard    │    │ │  ← secondary #6c3fc5
│  │  └──────────────────┘    │  │  └──────────────────┘    │ │
│  └──────────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 13.4.3 Spielscreen – Bauernschach

```
┌─────────────────────────────────────────────────────────────┐  bg-deep #0d0f1a
│  ████ Pawn Chess │ Hard │ Your turn          [Rules][Abort] │  bg-mid #1e2850
├─────────────────────────────────────────────────────────────┤
│                                                             │
│          0       1       2       3       4       5          │
│        ┌───────┬───────┬───────┬───────┬───────┬───────┐   │
│   0    │  ♟   │▓▓▓▓▓▓▓│  ♟   │▓▓▓▓▓▓▓│  ♟   │▓▓▓▓▓▓▓│   │  KI-Bauern
│        ├───────┼───────┼───────┼───────┼───────┼───────┤   │  text-secondary #8a9cc0
│   1    │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│       │   │
│        ├───────┼───────┼───────┼───────┼───────┼───────┤   │
│   2    │       │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│   │
│        ├───────┼───────┼───────┼───────┼───────┼───────┤   │
│   3    │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│       │▓▓▓▓▓▓▓│       │   │
│        ├───────┼───────┼───────┼───────┼───────┼───────┤   │
│   4    │       │▓▓▓▓▓▓▓│  ●   │▓▓▓▓▓▓▓│  ○   │▓▓▓▓▓▓▓│   │  ● ausgewählt (primary #e8365d)
│        ├───────┼───────┼───────┼───────┼───────┼───────┤   │  ○ gültiger Zug (#2e7d32)
│   5    │  ♙   │  ♙   │▓▓▓▓▓▓▓│  ♙   │▓▓▓▓▓▓▓│  ♙   │   │  Mensch-Bauern text-primary #fff
│        └───────┴───────┴───────┴───────┴───────┴───────┘   │
│                                                             │
│  ▓ = board_dark #8b5e3c   □ = board_light #eecc99          │
└─────────────────────────────────────────────────────────────┘
```

#### 13.4.4 Spielscreen – Tic-Tac-Toe (4 gewinnt)

```
┌─────────────────────────────────────────────────────────────┐  bg-deep #0d0f1a
│  ████ Tic-Tac-Toe (4 in a Row) │ Hard │ AI is thinking...  │  bg-mid #1e2850
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌───────┬───────┬───────┬───────┬───────┬───────┐      │
│     │       │       │       │       │       │       │      │
│     ├───────┼───────┼───────┼───────┼───────┼───────┤      │
│     │       │   X   │   O   │       │       │       │      │  X = accent #00d4ff (Cyan)
│     ├───────┼───────┼───────┼───────┼───────┼───────┤      │  O = primary #e8365d (Hot Pink)
│     │       │   O   │   X   │   X   │       │       │      │
│     ├───────┼───────┼───────┼───────┼───────┼───────┤      │
│     │       │       │   O   │   X   │       │       │      │
│     ├───────┼───────┼───────┼───────┼───────┼───────┤      │
│     │       │       │       │       │       │       │      │
│     ├───────┼───────┼───────┼───────┼───────┼───────┤      │
│     │       │       │       │       │       │       │      │
│     └───────┴───────┴───────┴───────┴───────┴───────┘      │
│                                                             │
│         X = You (Human)          O = AI                     │
└─────────────────────────────────────────────────────────────┘
```

#### 13.4.5 Ergebnis-Overlay (Spielende)

```
┌─────────────────────────────────────────────────────────────┐
│  ████ Tic-Tac-Toe (4 in a Row) │ Hard │ ...                │
├─────────────────────────────────────────────────────────────┤
│                          ┌───────────────────────────────┐  │
│     [ Spielfeld ]        │                               │  │
│                          │        You win!               │  │  ← win #4caf50
│                          │                               │  │
│                          │  ┌─────────────────────────┐  │  │
│                          │  │      Back to Menu        │  │  │  ← primary #e8365d
│                          │  └─────────────────────────┘  │  │
│                          └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

  Ergebnisfarben:  You win!  → #4caf50 (Grün)
                  AI wins!  → primary #e8365d (Hot Pink)
                  Draw!     → #ff9800 (Orange)
```

#### 13.4.6 Bestenliste (Popup)

```
┌─────────────────────────────────────────┐  bg-deep #0d0f1a
│                                         │
│    Leaderboard – Pawn Chess – Hard      │  ← primary #e8365d, Orbitron Bold
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  Rang  Spieler   Siege  Niederl │    │  bg-card #1a2040
│  │  ────  ───────   ─────  ─────── │    │
│  │   1    alice       7       2    │    │  ← text-primary #ffffff
│  │   2    bob         5       4    │    │
│  │   3    carol       3       1    │    │
│  │   4    dave        1       6    │    │
│  └─────────────────────────────────┘    │
│                                         │
│         ┌─────────────────┐             │
│         │     Close       │             │  ← primary #e8365d
│         └─────────────────┘             │
└─────────────────────────────────────────┘
```

---

### 13.5 Design Tokens

#### Border Radius

| Token | Wert | Verwendung |
|-------|------|------------|
| None | 0 px | Spielfeld-Zellen, tabellarische Bereiche |
| Small | 6 px | Buttons, Eingabefelder |
| Medium | 12 px | Karten, Dialoge |
| Large | 20 px | Panels, Overlays |
| Pill | 100 px | Badge-Labels, Chip-Elemente |

#### Spacing Scale

| Token | Wert | Verwendung |
|-------|------|------------|
| XS | 4 px | Interne Icon-Abstände |
| SM | 8 px | Padding innerhalb von Buttons/Tags |
| MD | 16 px | Standard-Padding in Karten |
| LG | 24 px | Abstand zwischen Sektionen |
| XL | 32 px | Große Außenabstände |
| XXL | 48 px | Screen-seitliche Ränder |

---

### 13.6 Glow & Effekte

Leuchtende Akzente (Glow) verstärken das Gaming-Feeling und heben interaktive Elemente hervor.

| Effekt | CSS-Formel | Verwendung |
|--------|-----------|------------|
| Primary Glow | `box-shadow: 0 0 24px rgba(232, 54, 93, 0.35)` | Primär-Buttons (Login, Play, Close) |
| Secondary Glow | `box-shadow: 0 0 24px rgba(108, 63, 197, 0.35)` | Sekundär-Buttons (Register, Leaderboard) |
| Accent Glow | `box-shadow: 0 0 24px rgba(0, 212, 255, 0.35)` | Aktive Felder, Hover-Zustände |

In tkinter werden Glow-Effekte durch Rahmenfarbe (`highlightbackground`) und leicht hellere Button-Farbe beim Hover simuliert.

---

### 13.7 Python Code-Export

Offizielle Token-Konstanten für die Implementierung in `main.py`:

```python
# HHBKTendo Design System – Color Tokens
BG_DEEP        = "#0d0f1a"   # Deep Navy  – App-Hintergrund
BG_CARD        = "#1a2040"   # Card Navy  – Karten & Container
BG_MID         = "#1e2850"   # Mid Navy   – Eingabefelder / Surfaces

PRIMARY        = "#e8365d"   # Hot Pink   – Primär-CTA, Logo, Danger
SECONDARY      = "#6c3fc5"   # Royal Purple – Sekundäre Buttons
ACCENT         = "#00d4ff"   # Cyber Cyan – Active States, Outlines

TEXT_PRIMARY   = "#ffffff"   # White      – Primärtext
TEXT_SECONDARY = "#8a9cc0"   # Slate Blue – Sekundärtext
TEXT_MUTED     = "#4a5680"   #            – Dezenter Text, Hints
```

---

### 13.8 Designprinzipien

| Prinzip | Umsetzung |
|---------|-----------|
| **Dunkel-First** | Alle Hintergründe dunkel – kein heller Screen in der gesamten App |
| **Farbhierarchie** | Hot Pink (primary) = primär, Royal Purple (secondary) = sekundär, Slate Blue = passiv |
| **Konsistenz** | Alle interaktiven Elemente (Buttons) gleiche Form, Schrift und Padding |
| **Feedback** | Jeder Zustandswechsel hat eine visuelle Entsprechung (Farbe, Symbol) |
| **Plattformkompatibilität** | Buttons als `tk.Label` mit Bindings – funktioniert auf Windows und macOS |
| **Spielfeld-Isolation** | Brett-Farben (Beige/Braun) bewusst aus der CI-Palette herausgehalten, um Spielbereich klar abzugrenzen |

---

### 13.9 CI-Konzept

---

#### 13.9.1 Name und Beschreibung der Marke

**Markenname: HHBKTendo**

Der Name ist eine direkte Zusammensetzung aus zwei Teilen:

- **HHBK** steht für das *Heinrich-Hertz-Berufskolleg* – die Schule, an der das Projekt entstanden ist. Die Abkürzung verankert die Marke bewusst in ihrem Entstehungskontext und signalisiert: Dieses Produkt wurde von echten Menschen mit echtem Bildungsauftrag entwickelt.
- **Tendo** ist dem Namen *Nintendo* – dem bekanntesten Gaming-Unternehmen der Welt – entnommen. Die Anlehnung ist bewusst gewählt: Sie steht für Spielfreude, Qualität und den Anspruch, in der Welt des digitalen Spielens einen eigenen Weg zu gehen.

Zusammen ergibt **HHBKTendo** eine Marke, die schulische Identität mit Gaming-Kultur verbindet: verwurzelt im Bildungskontext, positioniert im Spielemarkt.

Der Produktname der App lautet **BlitzBoard** – ein Titel, der Geschwindigkeit (*Blitz*) mit dem klassischen Brettspiel-Format (*Board*) verbindet. Das Wort *Blitz* steht dabei zugleich für das zentrale Markenversprechen: sofortiger Spieleinstieg, ohne Umwege. BlitzBoard macht klassische Zwei-Spieler-Brettspiele wie Bauernschach und Tic-Tac-Toe digital erlebbar – für Familien und junge Leute, die gemeinsam Spaß haben wollen. Der Produktname wird im Investor-Pitch und im Marketing-Kontext verwendet; in der Anwendung selbst tritt der Markenname HHBKTendo in den Vordergrund.

---

#### 13.9.2 Mission Statement

> **HHBKTendo bietet spaßige und unterhaltende Brettspielklassiker direkt für Endnutzerinnen und Endnutzer (B2C) – einfach zugänglich, modern umgesetzt und stets mit einem Lächeln. Klassische Strategiespiele mit echter KI-Herausforderung werden kostenlos bereitgestellt: ohne Wartezeiten, ohne Einstiegshürden, ohne Kompromisse beim Spielerlebnis.**

Die Mission adressiert ein klar identifiziertes Problem: Langeweile ist universell. Schülerinnen und Schüler in Freistunden, Patientinnen und Patienten in Kliniken, Pendlerinnen und Pendler im Nahverkehr – alle haben ungenutzte Zeit, aber kaum Zugang zu qualitativ hochwertiger, kostenloser Unterhaltung ohne Ablenkungs-Mechanismen (Werbung, In-App-Käufe, Abonnementzwang). HHBKTendo schließt diese Lücke mit einem klaren Grundsatz: *Wer spielen will, spielt – sofort, kostenlos und ohne Schranken.*

---

#### 13.9.3 Vision Statement

> **HHBKTendo wird die beste digitale Brettspielmarke Deutschlands – und macht Familien weltweit die schönsten Brettspielklassiker aller Kulturen digital zugänglich: mit einer wachsenden Spielbibliothek, Partnerschaften mit Schulen und sozialen Einrichtungen sowie einer Community, die klassische Strategiespiele für das digitale Zeitalter neu entdeckt.**

Mittelfristig (6–18 Monate): Erweiterung der Spielbibliothek um Dame und weitere Klassiker aus verschiedenen Kulturen, Einführung eines Cosmetics-Shops (Skins & Boards) sowie aktive Kooperationen mit Schulen und Kliniken.

Langfristig (2–5 Jahre): Positionierung als meistgenutzte kostenlose Brettspiel-App im deutschsprachigen Raum, Expansion in internationale Märkte (UK, Singapur, USA, Hongkong) und Aufbau eines B2B-Lizenzmodells für Marken-Kollaborationen.

**Strategische Wettbewerbsvorteile (aus Investor-Pitch):**

| Faktor | Beschreibung |
|--------|-------------|
| Hohe Update-Frequenz | Neue Spiele erscheinen regelmäßig – Nutzende haben stets einen Grund zurückzukehren |
| Klare Roadmap | Dame, Checkers, vollständiger Shop – Investoren und Nutzende sehen, wohin die Reise geht |
| Kollaborationspotenzial | Marken-Kooperationen (Skins & Boards) eröffnen einen B2B-Umsatzkanal ohne zusätzlichen Entwicklungsaufwand |
| Community-First | Kostenloser Zugang und Klinikpartnerschaften bauen eine loyale Nutzerbasis auf, die als organischer Marketing-Kanal wirkt |

---

#### 13.9.4 Sprachstil und Kommunikation der Marke

**Tonalität:** Modern, jugendlich und direkt – locker, energetisch, einladend, leicht wettbewerbsorientiert, aber nie kindisch. HHBKTendo spricht die Nutzenden wie gleichwertige Gesprächspartner an: respektvoll, knapp, auf den Punkt. Die Ansprache erfolgt in der Du-Form, um Nähe und niedrige Hemmschwelle zu vermitteln.

**Grundprinzipien des Sprachstils:**

| Prinzip | Beispiel (EN) | Beispiel (DE) |
|---------|--------------|---------------|
| Direkt & aktiv | „Your turn." | „Du bist dran." |
| Kurz & prägnant | „You win!" | „Du gewinnst!" |
| Motivierend, nicht bevormundend | „AI is thinking..." | „KI denkt nach..." |
| Fehlermeldungen ohne Schuldzuweisung | „Username already taken." | „Benutzername vergeben." |

**Slogans / Mottos:**

Die Marke verfügt über zwei komplementäre Slogans für unterschiedliche Kommunikationskontexte:

> **(DE) „Spiele, die schlau machen."**
> **(EN) „Classic Games. Real Intelligence."**

Der deutsche Slogan *„Spiele, die schlau machen."* spricht die Kernzielgruppe (Familien, Schülerinnen und Schüler) direkt an: Er verspricht Unterhaltung mit echtem kognitivem Mehrwert. Die Formulierung ist niedrigschwellig, einprägsam und transportiert den Bildungsanspruch ohne belehrend zu wirken.

Der englische Slogan *„Classic Games. Real Intelligence."* richtet sich an internationale Märkte und Investoren: Er benennt das vertraute Spielformat (*Classic Games*) und die technologische Besonderheit (*Real Intelligence* – echter MiniMax-Algorithmus, keine Zufalls-KI) in vier Wörtern. Er fungiert als UI-Tagline auf dem Startscreen und im Pitch-Deck.

**Sprachliche Elemente im GUI:**

| Kontext | Text (EN) | Text (DE) |
|---------|-----------|-----------|
| Startscreen-Tagline | *HHBKTendo Game Collection* | *HHBKTendo Spielesammlung* |
| Spielstart | „Play" | „Spielen" |
| Spielerzug | „Your turn" | „Du bist dran" |
| KI-Zug | „AI is thinking..." | „KI denkt nach..." |
| Sieg | „You win!" | „Du gewinnst!" |
| Niederlage | „AI wins!" | „KI gewinnt!" |
| Unentschieden | „Draw!" | „Unentschieden!" |
| Gastmodus-Hinweis | „Playing as guest – results won't be saved." | „Gastmodus – Ergebnisse werden nicht gespeichert." |
| Spielabbruch | „Abort the current game?" | „Das aktuelle Spiel abbrechen?" |

Die Sprache ist bewusst zweisprachig gehalten (EN Standard, DE optional): Dies spiegelt die internationale Zielgruppenstrategie wider und ermöglicht es, dieselbe App ohne Übersetzungsaufwand in mehreren Märkten einzusetzen.

---

#### 13.9.5 Design-Elemente – konzeptionelle Begründung

Das HHBKTendo Design System ist kein dekoratives Add-on, sondern die visuelle Übersetzung von Mission und Vision. Jede Designentscheidung ist semantisch begründet:

**Farbwahl:**

| Farbe | Hex | Konzeptionelle Bedeutung | Bezug zur Mission/Vision |
|-------|-----|--------------------------|--------------------------|
| Deep Navy | `#0d0f1a` | Konzentration, Tiefe, Ruhe | Spielen als ernsthafte mentale Tätigkeit, kein Ablenkungsfeuerwerk |
| Hot Pink | `#e8365d` | Energie, Aktion, Gefahr | Primäre CTA („Jetzt spielen") – erzeugt Dringlichkeit und Aufmerksamkeit |
| Royal Purple | `#6c3fc5` | Qualität, Tiefe, Sekundäres | Sekundäre Aktionen – unterstützt Hierarchie ohne zu dominieren |
| Cyber Cyan | `#00d4ff` | Technologie, KI, Intelligenz | Visualisierung der KI-Kompetenz; aktive Zustände, Hover-States |
| White | `#ffffff` | Klarheit, Lesbarkeit | Primärtext – maximaler Kontrast auf dunklem Grund |
| Slate Blue | `#8a9cc0` | Neutralität, Dezenz | Sekundärtext – Statuszeilen, Hinweise, ohne zu stören |

**Konzeptioneller Ursprung der Farbwahl – 2-Player-Teamfarben:**

Die ursprüngliche Farbidee für BlitzBoard basiert auf dem klassischen Prinzip der Teamfarben: **Blau** und **Rot** als die zwei gegnerischen Seiten, die in jedem Zwei-Spieler-Spiel aufeinanderprallen. Blau und Rot sind kulturübergreifend als Kontrastpaar bekannt (Sport, Schach, Politik) und erzeugen sofort eine sportlich-dynamische Atmosphäre, die den Wettbewerbsgedanken transportiert.

Im finalen Design-System wurde dieses Konzept in die HHBKTendo-Palette überführt und verfeinert:

| Konzept | Ursprungsidee | Finale Umsetzung |
|---------|--------------|------------------|
| Spieler 1 (Mensch) | Blau 🔵 | Cyber Cyan `#00d4ff` – kühler, präziser Blauton |
| Spieler 2 (KI) | Rot 🔴 | Hot Pink `#e8365d` – aggressiver, warmer Rotton |
| Hintergrund | Dunkel, neutral | Deep Navy `#0d0f1a` – maximaler Kontrast, Gaming-Ästhetik |

Die Farbkombination Deep Navy + Hot Pink + Cyber Cyan positioniert HHBKTendo visuell exakt zwischen *seriösem Technologieprodukt* (dunkles Schema, klare Typografie) und *Gaming-Produkt* (leuchtende Akzente, Glow-Effekte). Die 2-Player-Logik der Ursprungsfarben bleibt dabei erhalten: Im Tic-Tac-Toe-Spielfeld repräsentiert Cyan das X des menschlichen Spielers, Hot Pink das O der KI – Blau gegen Rot, technisch verfeinert.

**Typografie:**

| Schriftart | Rolle | Begründung |
|-----------|-------|------------|
| Orbitron (Display) | Logo, Überschriften | Geometrisch, futuristisch, tech-orientiert – kommuniziert sofort: das ist ein modernes Produkt mit algorithmischem Anspruch |
| Exo 2 (Body) | Buttons, Labels, Fließtext | Humanistisch, sehr lesbar auch bei kleinen Größen – schafft Nähe und Zugänglichkeit gegenüber der technischen Strenge von Orbitron |

Als alternative serifenlose Schriften wurden Inter, Montserrat und Poppins evaluiert. Orbitron und Exo 2 wurden gewählt, da sie den Gaming-Charakter der Marke stärker transportieren als die neutraleren Alternativen, ohne die Lesbarkeit zu beeinträchtigen.

Die Kombination aus einem Display-Font mit technischem Charakter (Orbitron) und einem lesbaren Body-Font (Exo 2) spiegelt die Markenidentität direkt wider: anspruchsvoll in der KI, zugänglich im Spielerlebnis.

**Formensprache:**

Das Design-System kombiniert bewusst zwei gegensätzliche Formsprachen, die jeweils unterschiedliche emotionale Signale senden:

| Formtyp | Einsatz | Wirkung |
|---------|---------|---------|
| **Weiche, runde Formen** (Radius 6–20 px) | Buttons, Karten, Dialoge | Ruhe, Einladung, Spaß – signalisiert: hier kann man entspannt interagieren |
| **Harte, scharfe Formen** (Radius 0 px) | Spielfeld-Zellen | Spannung, Präzision, Wettbewerb – signalisiert: hier zählt jeder Zug |

Die Kombination beider Stile erzeugt eine ausgewogene, dynamische Optik: Die Anwendung fühlt sich einladend an (runde UI-Elemente), ohne die strategische Ernsthaftigkeit des Spiels zu untergraben (scharfes Spielfeld).

Ergänzend dazu folgt die gesamte UI einem **gridartigen Anordnungsprinzip**, das dem Spielfeld selbst nachempfunden ist: Karten, Buttons und Tabellen orientieren sich an klaren, rechteckigen Strukturen. Die Gestaltung wirkt dadurch konsistent und intuitiv – das visuelle System fühlt sich wie eine natürliche Erweiterung des Spielfelds an.

**Designbegründung:**

Das Design ist bewusst reduziert und funktional gehalten. Klare Strukturen unterstützen das strategische Denken der Spielenden, während starke Farbkontraste (Deep Navy gegen Hot Pink / Cyber Cyan) den Wettbewerbscharakter der Spiele hervorheben.

**Symbole und Ikonografie:**

| Symbol | Bedeutung | Einsatz |
|--------|-----------|---------|
| ⚡ Blitz | Energie, Schnelligkeit, Wettkampf | Produktname BlitzBoard; steht für sofortigen Spieleinstieg |
| 🎲 Brett / ♙ ♟ | Klassik, Strategie, Tradition | Spielfiguren und Spielfeld; universell bekannte Symbole |
| 🎮 Gamepad | Digitalität, moderne Gaming-Kultur | Positionierung als digitales Produkt, nicht als physisches Brettspiel |

Die drei Symbole bilden zusammen die Markenerzählung: *Blitz* (sofort, energetisch) + *Brett* (klassisch, strategisch) + *Gamepad* (digital, modern) = HHBKTendo.

**Verbindung zu Mission und Vision:**

Die visuelle Dunkelheit der App schafft einen ablenkungsfreien Fokusraum – passend zur Mission, spaßige und unterhaltende Spielklassiker ohne Kompromisse anzubieten. Die leuchtenden Akzentfarben erzeugen dabei Lebendigkeit und signalisieren: das hier ist kein trockenes Bildungstool, sondern echtes Gaming. Die Formensprache (rund = einladend, scharf = Wettkampf) und die Symbole (Blitz, Brett, Gamepad) verstärken diesen Anspruch auf jeder Ebene der Benutzeroberfläche.

---

#### 13.9.6 Zielgruppenbezug

**Primäre Zielgruppen (aus Investor-Pitch):**

| Zielgruppe | Beschreibung | CI-Relevanz |
|-----------|--------------|-------------|
| Schülerinnen & Schüler | Kurze Spielsessions in Freistunden; kostensensitiv | Kostenloser Einstieg ohne Anmeldepflicht (Gastmodus); schnelle Orientierung durch klares UI |
| Kinder in Langzeit-Kliniken | Begrenzte Ablenkungsmöglichkeiten; teilweise eingeschränkte Motorik | Großes, kontrastreiches Spielfeld; einfache Eingabe per Klick; keine In-App-Käufe die Eltern belasten |
| Pendlerinnen & Pendler | Kurze Sessions; Nutzung unterwegs; zeitkritisch | „Zero Friction" – Sofortstart im Gastmodus, kein Login erforderlich |
| Familien | Generationsübergreifend; bekannte Spiele bevorzugt | Klassikerformat (Bauernschach, Tic-Tac-Toe); deutsche Sprache als Option |
| Gelegenheitsspieler | Kein Vorwissen nötig; suchen schnelle, unkomplizierte Unterhaltung | Sofortstart im Gastmodus; fünf Schwierigkeitsgrade vom Einstieg bis zur Herausforderung |

**Marktgröße (aus Investor-Pitch):**
- 3,5 Milliarden Mobile-Gamer weltweit (Stand 2024)
- Marktvolumen Mobile Gaming: 98 Milliarden USD (Prognose 2030)
- 60 % der Mobile-Gamer spielen Casual- oder Brettspiele

**Was die CI bei der Zielgruppe vermitteln soll:**

1. **Vertrauen**: Das dunkle, konsistente Design ohne Werbe-Pop-ups oder Ablenkungselemente signalisiert: Diese App respektiert die Zeit der Nutzenden.
2. **Kompetenz**: Orbitron als Display-Font und die Cyber-Cyan-Akzente positionieren die KI-Komponente als technologisch ernsthaft – nicht als einfaches Zufallsspiel.
3. **Zugänglichkeit**: Exo 2 als Lesetext, klare Kontraste und kurze Statusmeldungen stellen sicher, dass die App auch für weniger technikaffine Zielgruppen sofort bedienbar ist.
4. **Kostenlosigkeit ohne Qualitätsverlust**: Die visuelle Qualität des Design Systems (Glow-Effekte, professionelle Typografie, konsistente Farbpalette) widerlegt das Vorurteil, kostenlose Apps sähen minderwertig aus. HHBKTendo sieht aus wie ein Premium-Produkt – und ist kostenlos. Das ist das stärkste Marketing-Signal.

**Gestaltungsziele:**

Die Anwendung soll für alle Zielgruppen folgende Grundanforderungen erfüllen:

1. **Schnell verständlich** – keine Einarbeitungszeit, intuitive Navigation
2. **Sofort spielbar** – Spielstart ohne Registrierung möglich (Gastmodus)
3. **Motivation durch Wettbewerb** – KI als echter Gegner, Bestenliste als Anreiz
4. **Strategisches Denken fördern** – fünf Schwierigkeitsgrade, die schrittweise herausfordern

---

**Geschäftsmodell und CI-Strategie (aus Investor-Pitch):**

Das Geschäftsmodell von BlitzBoard ist direkt mit der CI verzahnt: Der kostenlose Einstieg ist kein Kompromiss, sondern das stärkste CI-Signal. Die Preisstruktur unterstreicht das Markenversprechen auf jeder Ebene:

| Tier | Preis | CI-Botschaft |
|------|-------|-------------|
| Free | kostenlos | „Jeder kann spielen" – Mission in Reinform |
| Premium Monthly | €0,99 / Monat | Qualität hat einen fairen Preis |
| Premium Lifetime | €5 einmalig | Langfristige Beziehung statt Abofrustration |
| À la Carte (Skins & Boards) | €0,99–€2,99 | Personalisierung ohne Zwang |

**Zusammenfassung CI-Wirkung:**

> Die Corporate Identity von HHBKTendo kommuniziert in einem Blick: *Moderne digitale Brettspielmarke, echte KI, Spaß für alle – ohne Schranken.* Die Farbwelt (2-Player-Teamfarben, Gaming-Ästhetik), die Typografie (tech-orientiert + lesbar), die Formensprache (einladend + präzise), die Symbolik (Blitz, Brett, Gamepad) und der Sprachstil (jugendlich, direkt, zweisprachig) greifen ineinander, um genau die Nutzenden anzusprechen, die bisher von werbefinanzierten, komplexen oder teuren Apps abgeschreckt wurden: junge Menschen, Familien und Institutionen, die Qualität erwarten, aber keine hohen Preise bezahlen können oder wollen.

---

#### 13.9.7 Fazit

HHBKTendo steht für schnelle, direkt zugängliche Strategiespiele mit klarem Fokus auf Wettbewerb und Entscheidungsfindung. Die Corporate Identity verbindet eine moderne, reduzierte Gestaltung mit einer aktiven und klaren Sprache – und schafft so ein konsistentes, funktionales Nutzererlebnis, das von der Farbwahl über die Typografie bis hin zu jedem einzelnen GUI-Text dieselbe Botschaft trägt: **Spielen. Denken. Gewinnen.**

---

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-04-20 | Erstversion |
| 1.1 | 2026-04-21 | Tic-Tac-Toe zwischenzeitlich auf 3×3 geändert; NF-09 (macOS-Kompatibilität) ergänzt |
| 1.2 | 2026-04-21 | Tic-Tac-Toe gemäß Lastenheft (LF4020) auf 6×6 / 4 in einer Reihe zurückgesetzt; PF-M03, Abschnitt 4.2, Bewertungsfunktion, TC-09–TC-11 wiederhergestellt |
| 1.3 | 2026-04-22 | Abgleich mit Lastenheft: PF-K03 (Dame) und PF-K04 (alternative KI-Schnittstelle) als Kann-Ziele ergänzt; neuer Abschnitt 12 mit Dokumentations- und Konzeptanforderungen (DOC-01–DOC-13) aus LD5100–LD5500; Abschnitt 15.2 Offene Punkte erweitert; Liefergegenstände mit Anforderungsreferenzen verknüpft |
| 1.4 | 2026-04-22 | Neuer Abschnitt 15: Design und Corporate Identity – Farbpalette mit Begründungen, Typografie, Designprinzipien und ASCII-Mockups aller sechs Hauptscreens (Login, Menü, Bauernschach, Tic-Tac-Toe, Ergebnis-Overlay, Bestenliste) |
| 1.5 | 2026-04-22 | Abschnitt 15 auf offizielles HHBKTendo Design System (Investor Edition) aktualisiert: Farbpalette auf 9 PDF-Tokens (Deep Navy, Card Navy, Mid Navy, Hot Pink, Royal Purple, Cyber Cyan, White, Slate Blue, Muted) umgestellt; Typografie von Segoe UI auf Orbitron (Display) + Exo 2 (Body) umgestellt; neue Abschnitte 15.5 Design Tokens (Radius/Spacing), 15.6 Glow & Effekte, 15.7 Python Code-Export ergänzt; alle Mockup-Farbannotationen aktualisiert |
| 1.6 | 2026-04-24 | Neuer Abschnitt CI-Konzept vollständig ergänzt (CI_addon.md): Name & Markenbeschreibung (HHBKTendo + BlitzBoard), Mission Statement, Vision Statement, Sprachstil & Kommunikation (Tonalität, Slogan, GUI-Texttabelle), konzeptionelle Begründung der Design-Elemente (Farbe, Typografie, Formen), Zielgruppenbezug mit Marktdaten aus dem Blitzboard Investor-Pitch |
| 1.7 | 2026-04-24 | Abschnitt MiniMax vollständig überarbeitet und erweitert: Grundprinzip, Spielbaum-Visualisierung, rekursiver Ablauf (Pseudocode für Maximizer und Minimizer), erweitertes Illustrationsdiagramm mit Begründung, Alpha-Beta-Pruning mit Beispiel und Komplexitätsangabe, spielunabhängige Schnittstelle dokumentiert |
| 1.8 | 2026-04-24 | CI-Konzept mit CI_ideas.md und Blitzboard_Pitch erweitert: BlitzBoard-Beschreibung als 2-Player-App für Familien ergänzt; Mission um B2C-Fokus und Tonalität ("mit einem Lächeln") angereichert; Vision um "aller Kulturen" und strategische Wettbewerbsvorteile (4 Pitch-Faktoren) erweitert; Sprachstil um "jugendlich", Du-Ansprache und deutschen Slogan "Spiele, die schlau machen." ergänzt; Design-Elemente um 2-Player-Farbursprung (Blau/Rot), Inter/Montserrat/Poppins als evaluierte Alternativen, Formensprache-Tabelle (rund/scharf) und Symbolik-Tabelle (⚡🎲🎮) erweitert; Zielgruppe um Geschäftsmodell-Tabelle und überarbeitete CI-Wirkungszusammenfassung ergänzt |
| 1.9 | 2026-04-24 | Abschnitte 4.3 und 10 zusammengeführt: 4.3 auf funktionale Anforderungen + Querverweis zu Abschnitt 10 reduziert; Schwierigkeitsgrade-Tabelle und Zeitlimit in neuen Abschnitt 10.7 verschoben; 10.8 (ehemals 10.7) Spielunabhängige Schnittstelle umnummeriert |
| 2.0 | 2026-04-24 | Abschnitt Design & CI vor Liefergegenstände verschoben; Abschnitte umnummeriert: Design → 13, Liefergegenstände → 14, Projektplanung → 15; Inhaltsverzeichnis und alle Querverweise aktualisiert; Changelog in korrekte aufsteigende Reihenfolge gebracht |
| 2.1 | 2026-04-24 | CI-Konzept mit CI_ideas2 abgeglichen: Tonalität um „leicht wettbewerbsorientiert" ergänzt; Formensprache um gridartige Anordnung und Designbegründung erweitert; Zielgruppe „Gelegenheitsspieler" ergänzt; vier Gestaltungsziele hinzugefügt; neuer Abschnitt 13.9.7 Fazit |

*Pflichtenheft erstellt auf Basis des Lastenhefts Strategiespiele V13a, HHBK Tendo Research Center, 2026.*
## 14 Liefergegenstände

| # | Liefergegenstand | Verantwortlich |
|---|-----------------|----------------|
| 1 | Pflichtenheft (dieses Dokument) | Team |
| 2 | Quellcode (alle .py-Dateien + games.db) | Entwickler |
| 3 | Benutzerdokumentation (Installation, Start, Spielanleitung) – Anforderungen DOC-01 | Dokumentation |
| 4 | Technische Dokumentation (Spielverhalten, Algorithmen, Architektur, globale Variablen) – Anforderungen DOC-02 bis DOC-05 | Entwickler |
| 5 | Testprotokoll (TC-01 bis TC-15) | Test |
| 6 | Abschlusspräsentation (SOLL/IST Features & Zeitplan, Softwarekomponenten, Quellen, Fazit) – Anforderungen DOC-06 bis DOC-10 | Team |
| 7 | Konzept Corporate Identity & Branding (Design-Begründung, Mission/Vision) – Anforderung DOC-11 | Design |
| 8 | Pitch-Deck (englischsprachig, Investoren-Argumentation) – Anforderung DOC-12 | Team |
| 9 | Konzept Arbeitszeitgestaltung (Plan vs. IST, Risiken, Empfehlungen) – Anforderung DOC-13 | Projektleitung |

---

## 15 Projektplanung

### 15.1 Projektphasen (Wasserfallmodell)

| Phase | Inhalt | Zeitraum              |
|-------|--------|-----------------------|
| Analysephase | Lastenheft lesen, Pflichtenheft erstellen, WBS, Zeitplan, Ressourcenplan | Woche 1 (Vollzeit)    |
| Design & Implementierung | Architektur, Datenbankdesign, Spiellogik, MiniMax, GUI | Woche 2 (Vollzeit)    |
| Test | Testprotokoll, Bugfixes, Abnahmetests | Woche 2 (Mitte + Ende) |
| Dokumentation | Benutzerdokumentation, Technische Doku, Präsentation, Pitch, CI-Konzept | Woche 2 (Ende)        |
| Abschluss | Live-Demo, Präsentation, Fachgespräch (ca. 20+10 min) | Woche 3 (letzter Tag) |

### 15.2 Offene Punkte

| # | Offener Punkt | Referenz | Status |
|---|---------------|----------|--------|
| 1 | Dame als drittes Spiel implementieren | PF-K03 | Optional / zeitabhängig |
| 2 | Alternative KI-Schnittstelle definieren und implementieren | PF-K04 | Optional / zeitabhängig |
| 3 | Testprotokoll-Dokument erstellen und ausfüllen | TC-01–TC-15 | Ausstehend |
| 4 | Benutzerdokumentation schreiben | DOC-01 | Ausstehend |
| 5 | Technische Dokumentation vervollständigen | DOC-02–DOC-05 | Ausstehend |
| 6 | CI/Branding-Konzept (inkl. Mission/Vision) erstellen | DOC-11 | Ausstehend |
| 7 | Englischsprachigen Pitch erarbeiten | DOC-12 | Ausstehend |
| 8 | Konzept Arbeitszeitgestaltung ausarbeiten | DOC-13 | Ausstehend |

---

