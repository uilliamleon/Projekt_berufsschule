"""
database.py - Datenbankoperationen für HHBKTendo Spielesammlung
Verwendet SQLite als unabhängiges DBMS (LN5020, LD4200)
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "games.db")


def get_connection():
    """Erstellt und gibt eine Datenbankverbindung zurück."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Erlaubt Spalten-Zugriff per Name und dict()-Konvertierung
    return conn


def init_db():
    """Initialisiert die Datenbank mit allen benötigten Tabellen."""
    conn = get_connection()
    cursor = conn.cursor()

    # Benutzertabelle (LD4200)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Spielergebnisse (LD4210)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            won INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Migration: Sprachspalte nachrüsten falls DB schon existiert (LD4200)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Spalte existiert bereits

    conn.commit()
    conn.close()


def register_user(username, password_hash, language="en"):
    """
    Registriert einen neuen Benutzer.
    Gibt True zurück bei Erfolg, False wenn Benutzername bereits vergeben.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, language) VALUES (?, ?, ?)",
            (username, password_hash, language)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username):
    """Gibt Benutzerdaten anhand des Benutzernamens zurück."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_user_by_id(user_id):
    """Gibt Benutzerdaten anhand der ID zurück."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def save_result(user_id, game, difficulty, won):
    """
    Speichert ein Spielergebnis in der Datenbank (LD4210).
    won: 1 = Sieg, 0 = Niederlage
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results (user_id, game, difficulty, won) VALUES (?, ?, ?, ?)",
        (user_id, game, difficulty, int(won))
    )
    conn.commit()
    conn.close()


def get_leaderboard(game, difficulty, limit=10):
    """
    Gibt die Bestenliste für ein bestimmtes Spiel und Schwierigkeitsgrad zurück (LD4220).
    Sortiert nach Siegen absteigend.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            u.username,
            SUM(r.won) AS wins,
            SUM(1 - r.won) AS losses,
            COUNT(*) AS total_games
        FROM results r
        JOIN users u ON r.user_id = u.id
        WHERE r.game = ? AND r.difficulty = ?
        GROUP BY r.user_id
        ORDER BY wins DESC, losses ASC
        LIMIT ?
    """, (game, difficulty, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_stats(user_id, game=None):
    """Gibt Statistiken eines Benutzers zurück, optional gefiltert nach Spiel."""
    conn = get_connection()
    cursor = conn.cursor()
    if game:
        cursor.execute("""
            SELECT game, difficulty,
                   SUM(won) AS wins, SUM(1-won) AS losses, COUNT(*) AS total
            FROM results
            WHERE user_id = ? AND game = ?
            GROUP BY game, difficulty
            ORDER BY difficulty
        """, (user_id, game))
    else:
        cursor.execute("""
            SELECT game, difficulty,
                   SUM(won) AS wins, SUM(1-won) AS losses, COUNT(*) AS total
            FROM results
            WHERE user_id = ?
            GROUP BY game, difficulty
            ORDER BY game, difficulty
        """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_password(username, new_password_hash):
    """Aktualisiert den Passwort-Hash eines Benutzers."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (new_password_hash, username)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def update_user_language(user_id, language):
    """Aktualisiert die Spracheinstellung eines Benutzers (LD4230)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET language = ? WHERE id = ?",
        (language, user_id)
    )
    conn.commit()
    conn.close()
