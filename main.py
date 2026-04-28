"""
main.py - HHBKTendo Spielesammlung - Hauptprogramm
GUI mit tkinter, prozedural programmiert (LN5000, LN5001)

Spiele: Bauernschach, Tic-Tac-Toe
KI: MiniMax mit Alpha-Beta-Pruning
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import math

import database
import auth
import minimax as mm
import pawn_chess as pc
import tictactoe as ttt

# ─────────────────────────────────────────────
# Globaler GIF-Zustand (screen-übergreifende Animation)
# ─────────────────────────────────────────────
_gif = {
    "frames": [],   # ImageTk.PhotoImage-Objekte (einmalig geladen)
    "delays": [],   # Anzeigedauer je Frame in ms
    "idx":    0,    # aktuell angezeigter Frame-Index
    "label":  None, # das Background-Label des aktiven Screens
    "root":   None, # tk.Tk-Referenz für root.after()
}

# ─────────────────────────────────────────────
# Globaler App-Zustand
# ─────────────────────────────────────────────
app_state = {
    "language": "en",          # 'en' oder 'de'
    "current_screen": None,    # aktiver Frame
    "game": None,              # 'pawn_chess' oder 'tictactoe'
    "board": None,             # aktuelles Spielfeld
    "difficulty": 3,           # Suchtiefe (1-5)
    "human_turn": True,        # True = Mensch am Zug
    "selected": None,          # ausgewähltes Feld (Bauernschach)
    "valid_moves": [],         # gültige Züge für ausgewähltes Feld
    "game_over": False,
    "ai_thinking": False,
}

# ─────────────────────────────────────────────
# Farben & Design (CI/Branding LN5060)
# ─────────────────────────────────────────────
COLORS = {
    "bg_dark":           "#1a1a2e",
    "bg_mid":            "#16213e",
    "bg_card":           "#0f3460",
    "accent":            "#e94560",
    "accent2":           "#533483",
    "text_light":        "#eaeaea",
    "text_dim":          "#a0a0b0",
    # Spielfiguren: deutlich verschieden von den Brettfarben
    "white_piece":       "#ffffff",   # Reines Weiß mit dunkler Kontur
    "white_piece_out":   "#222222",   # Kontur Weiß-Figur
    "black_piece":       "#1a1a2e",   # Sehr dunkles Blau
    "black_piece_out":   "#aaaaaa",   # Helle Kontur Schwarz-Figur
    # Brett: beige/braun – jetzt klar von Figuren getrennt
    "board_light":       "#eecc99",
    "board_dark":        "#8b5e3c",
    "highlight":         "#e94560",
    "highlight_out":     "#ff8080",
    "valid_move":        "#2e7d32",
    "valid_move_out":    "#81c784",
    # TTT-Symbole
    "ttt_x":             "#64b5f6",   # Hellblau für X (Mensch)
    "ttt_o":             "#ef5350",   # Rot für O (KI)
    # Buttons & Status
    "btn_bg":            "#e94560",
    "btn_hover":         "#c73652",
    "btn_text":          "#ffffff",
    "win":               "#4caf50",
    "lose":              "#e94560",
    "draw":              "#ff9800",
}

# ─────────────────────────────────────────────
# Übersetzungen (LF4130)
# ─────────────────────────────────────────────
TEXTS = {
    "en": {
        "title": "HHBKTendo Game Collection",
        "login": "Login",
        "register": "Register",
        "play_guest": "Play as Guest",
        "username": "Username",
        "password": "Password",
        "main_menu": "Main Menu",
        "select_game": "Select a Game",
        "pawn_chess": "Pawn Chess",
        "tictactoe": "Tic-Tac-Toe (4 in a Row)",
        "difficulty": "Difficulty",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "expert": "Expert",
        "master": "Master",
        "play": "Play",
        "leaderboard": "Leaderboard",
        "rules": "Rules",
        "abort": "Abort Game",
        "logout": "Logout",
        "back": "Back",
        "your_turn": "Your turn",
        "ai_thinking": "AI is thinking...",
        "you_win": "You win!",
        "ai_wins": "AI wins!",
        "draw": "Draw!",
        "rank": "Rank",
        "player": "Player",
        "wins": "Wins",
        "losses": "Losses",
        "games": "Games",
        "no_entries": "No entries yet.",
        "guest_no_save": "Playing as guest - results won't be saved.",
        "language": "Language",
        "close": "Close",
        "confirm_abort": "Abort the current game?",
        "level": "Level",
        "keep_logged_in": "Keep me logged in",
        "forgot_password": "Forgot password?",
        "reset_password": "Reset Password",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "passwords_no_match": "Passwords do not match.",
        "password_reset_ok": "Password reset. You can now log in.",
    },
    "de": {
        "title": "HHBKTendo Spielesammlung",
        "login": "Anmelden",
        "register": "Registrieren",
        "play_guest": "Als Gast spielen",
        "username": "Benutzername",
        "password": "Passwort",
        "main_menu": "Hauptmenü",
        "select_game": "Spiel auswählen",
        "pawn_chess": "Bauernschach",
        "tictactoe": "Tic-Tac-Toe",
        "difficulty": "Schwierigkeit",
        "easy": "Leicht",
        "medium": "Mittel",
        "hard": "Schwer",
        "expert": "Experte",
        "master": "Meister",
        "play": "Spielen",
        "leaderboard": "Bestenliste",
        "rules": "Regeln",
        "abort": "Spiel abbrechen",
        "logout": "Abmelden",
        "back": "Zurück",
        "your_turn": "Du bist dran",
        "ai_thinking": "KI denkt nach...",
        "you_win": "Du gewinnst!",
        "ai_wins": "KI gewinnt!",
        "draw": "Unentschieden!",
        "rank": "Rang",
        "player": "Spieler",
        "wins": "Siege",
        "losses": "Niederlagen",
        "games": "Spiele",
        "no_entries": "Noch keine Einträge.",
        "guest_no_save": "Gastmodus - Ergebnisse werden nicht gespeichert.",
        "language": "Sprache",
        "close": "Schließen",
        "confirm_abort": "Das aktuelle Spiel abbrechen?",
        "level": "Level",
        "keep_logged_in": "Angemeldet bleiben",
        "forgot_password": "Passwort vergessen?",
        "reset_password": "Passwort zurücksetzen",
        "new_password": "Neues Passwort",
        "confirm_password": "Passwort bestätigen",
        "passwords_no_match": "Passwörter stimmen nicht überein.",
        "password_reset_ok": "Passwort zurückgesetzt. Du kannst dich jetzt anmelden.",
    }
}


def t(key):
    """Gibt den übersetzten Text für den aktuellen Sprachcode zurück."""
    lang = app_state["language"]
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)


# ─────────────────────────────────────────────
# GUI-Hilfsfunktionen
# ─────────────────────────────────────────────
def clear_frame(frame):
    """Entfernt alle Widgets aus einem Frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def make_button(parent, text, command, width=18, bg=None, fg=None):
    """Erstellt einen gestalteten Button (Label-basiert, funktioniert auf macOS)."""
    bg = bg or COLORS["btn_bg"]
    fg = fg or COLORS["btn_text"]
    hover_bg = COLORS["btn_hover"] if bg == COLORS["btn_bg"] else bg
    btn = tk.Label(
        parent, text=text,
        bg=bg, fg=fg, font=("Segoe UI", 11, "bold"),
        cursor="hand2", width=width,
        pady=6, padx=8
    )
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>",    lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>",    lambda e: btn.config(bg=bg))
    return btn


def make_label(parent, text, size=12, bold=False, color=None):
    """Erstellt ein gestaltetes Label."""
    color = color or COLORS["text_light"]
    weight = "bold" if bold else "normal"
    return tk.Label(
        parent, text=text,
        bg=COLORS["bg_dark"], fg=color,
        font=("Segoe UI", size, weight)
    )


def make_entry(parent, show=None):
    """Erstellt ein gestaltetes Eingabefeld."""
    return tk.Entry(
        parent, show=show,
        bg=COLORS["bg_card"], fg=COLORS["text_light"],
        insertbackground=COLORS["text_light"],
        font=("Segoe UI", 12), relief="flat",
        width=22
    )


def make_radio_group(parent, options, variable):
    """Ersetzt tk.Radiobutton durch gestylte, klickbare Zeilen."""
    entries = {}

    def refresh(selected_val):
        for v, (rf, dl, tl) in entries.items():
            if v == selected_val:
                rf.config(bg=COLORS["bg_mid"])
                dl.config(text="◆", fg=COLORS["accent"], bg=COLORS["bg_mid"])
                tl.config(fg=COLORS["text_light"], font=("Segoe UI", 9, "bold"), bg=COLORS["bg_mid"])
            else:
                rf.config(bg=COLORS["bg_card"])
                dl.config(text="◇", fg=COLORS["text_dim"], bg=COLORS["bg_card"])
                tl.config(fg=COLORS["text_dim"], font=("Segoe UI", 9), bg=COLORS["bg_card"])

    for val, label_text in options:
        row = tk.Frame(parent, bg=COLORS["bg_card"], cursor="hand2")
        row.pack(fill="x", pady=1)
        dot = tk.Label(row, text="◇", bg=COLORS["bg_card"],
                       fg=COLORS["text_dim"], font=("Segoe UI", 9), cursor="hand2")
        dot.pack(side="left", padx=(6, 4), pady=2)
        txt = tk.Label(row, text=label_text, bg=COLORS["bg_card"],
                       fg=COLORS["text_dim"], font=("Segoe UI", 9), cursor="hand2")
        txt.pack(side="left", pady=2)
        entries[val] = (row, dot, txt)

        def on_click(v=val):
            variable.set(v)
            refresh(v)

        def on_enter(e, v=val, rf=row, dl=dot, tl=txt):
            if variable.get() != v:
                rf.config(bg=COLORS["bg_mid"])
                dl.config(bg=COLORS["bg_mid"])
                tl.config(bg=COLORS["bg_mid"])

        def on_leave(e, v=val, rf=row, dl=dot, tl=txt):
            if variable.get() != v:
                rf.config(bg=COLORS["bg_card"])
                dl.config(bg=COLORS["bg_card"])
                tl.config(bg=COLORS["bg_card"])

        for widget in (row, dot, txt):
            widget.bind("<Button-1>", lambda e, v=val: on_click(v))
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    refresh(variable.get())


def _load_gif_frames():
    """Lädt alle GIF-Frames einmalig in _gif["frames"] (benötigt Pillow)."""
    try:
        from PIL import Image, ImageTk, ImageEnhance, ImageSequence
        import os
        gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "Mockups", "Assets", "Background",
                                "6m2ocolc0ip91.gif")
        gif = Image.open(gif_path)
        for gif_frame in ImageSequence.Iterator(gif):
            delay = gif_frame.info.get("duration", 100)
            resized = gif_frame.convert("RGBA").resize((820, 700), Image.LANCZOS)
            darkened = ImageEnhance.Brightness(resized).enhance(0.25)
            _gif["frames"].append(ImageTk.PhotoImage(darkened))
            _gif["delays"].append(max(delay, 50))
    except Exception:
        pass


def _gif_tick():
    """Globaler Animations-Takt – läuft unabhängig vom aktiven Screen über root.after()."""
    if not _gif["frames"] or _gif["root"] is None:
        return
    lbl = _gif["label"]
    if lbl is not None:
        try:
            lbl.config(image=_gif["frames"][_gif["idx"]])
        except tk.TclError:
            _gif["label"] = None  # Label wurde zerstört – kein Problem, nächster Screen registriert neu
    _gif["idx"] = (_gif["idx"] + 1) % len(_gif["frames"])
    _gif["root"].after(_gif["delays"][_gif["idx"]], _gif_tick)


def set_gif_background(frame):
    """Legt ein Hintergrund-Label im Frame an und registriert es beim globalen Animator."""
    if not _gif["frames"]:
        return
    bg_lbl = tk.Label(frame, bd=0, bg=COLORS["bg_dark"])
    bg_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)
    _gif["label"] = bg_lbl


def show_screen(root, build_fn):
    """Wechselt zum neuen Screen, zerstört den alten."""
    if app_state["current_screen"]:
        app_state["current_screen"].destroy()
    frame = tk.Frame(root, bg=COLORS["bg_dark"])
    frame.pack(fill="both", expand=True)
    app_state["current_screen"] = frame
    build_fn(root, frame)


# ─────────────────────────────────────────────
# LOGIN / REGISTER SCREEN
# ─────────────────────────────────────────────
def show_forgot_password(root):
    """Öffnet den Passwort-zurücksetzen-Dialog als Toplevel."""
    win = tk.Toplevel()
    win.title(t("reset_password"))
    win.resizable(False, False)
    win.configure(bg=COLORS["bg_dark"])
    win.grab_set()

    card = tk.Frame(win, bg=COLORS["bg_card"], padx=30, pady=24)
    card.pack(padx=20, pady=20)

    tk.Label(card, text=t("reset_password"),
             bg=COLORS["bg_card"], fg=COLORS["accent"],
             font=("Segoe UI", 14, "bold")).pack(pady=(0, 16))

    make_label(card, t("username"), size=10).pack(anchor="w")
    entry_user = make_entry(card)
    entry_user.pack(pady=(2, 10), fill="x")

    make_label(card, t("new_password"), size=10).pack(anchor="w")
    entry_pw1 = make_entry(card, show="*")
    entry_pw1.pack(pady=(2, 10), fill="x")

    make_label(card, t("confirm_password"), size=10).pack(anchor="w")
    entry_pw2 = make_entry(card, show="*")
    entry_pw2.pack(pady=(2, 12), fill="x")

    lbl_msg = tk.Label(card, text="", bg=COLORS["bg_card"],
                       fg=COLORS["accent"], font=("Segoe UI", 10), wraplength=260)
    lbl_msg.pack()

    def do_reset():
        if entry_pw1.get() != entry_pw2.get():
            lbl_msg.config(text=t("passwords_no_match"), fg=COLORS["accent"])
            return
        ok, err = auth.reset_password(entry_user.get(), entry_pw1.get())
        if ok:
            lbl_msg.config(text=t("password_reset_ok"), fg=COLORS["win"])
            win.after(2000, win.destroy)
        else:
            lbl_msg.config(text=err, fg=COLORS["accent"])

    make_button(card, t("reset_password"), do_reset).pack(fill="x", pady=(8, 0))

    # Fenster zentrieren
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_reqwidth()) // 2
    y = (win.winfo_screenheight() - win.winfo_reqheight()) // 2
    win.geometry(f"+{x}+{y}")


def build_login_screen(root, frame):
    """Baut den Login/Register-Screen."""
    set_gif_background(frame)

    # Header: Logo links + Titel rechts, vertikal zentriert
    header_row = tk.Frame(frame, bg=COLORS["bg_dark"])
    header_row.pack(pady=(40, 30))

    login_logo_img = None
    try:
        from PIL import Image, ImageTk
        import os
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "Mockups", "Assets", "Logo",
                                 "Only_Controller_Logo_HHBKTendo.png")
        logo_pil = Image.open(logo_path).convert("RGBA")
        pixels = logo_pil.load()
        bg_color = pixels[0, 0][:3]
        for y in range(logo_pil.height):
            for x in range(logo_pil.width):
                r, g, b, a = pixels[x, y]
                if all(abs(int(c) - int(bg)) <= 30 for c, bg in zip((r, g, b), bg_color)):
                    pixels[x, y] = (r, g, b, 0)
        target_h = 72
        target_w = int(logo_pil.width * target_h / logo_pil.height)
        logo_pil = logo_pil.resize((target_w, target_h), Image.LANCZOS)
        login_logo_img = ImageTk.PhotoImage(logo_pil)
    except Exception:
        pass

    if login_logo_img:
        lbl_logo = tk.Label(header_row, image=login_logo_img, bg=COLORS["bg_dark"])
        lbl_logo.image = login_logo_img
        lbl_logo.pack(side="left", padx=(0, 16))

    text_col = tk.Frame(header_row, bg=COLORS["bg_dark"])
    text_col.pack(side="left")
    tk.Label(text_col, text="BlitzBoard",
             bg=COLORS["bg_dark"], fg=COLORS["accent"],
             font=("Segoe UI", 28, "bold")).pack(anchor="w")
    tk.Label(text_col, text=t("title"),
             bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
             font=("Segoe UI", 13)).pack(anchor="w")

    # Card
    card = tk.Frame(frame, bg=COLORS["bg_card"], padx=30, pady=30)
    card.pack(padx=40, pady=10)

    # Username
    make_label(card, t("username"), size=11).pack(anchor="w")
    entry_user = make_entry(card)
    entry_user.pack(pady=(2, 12), fill="x")

    # Password
    make_label(card, t("password"), size=11).pack(anchor="w")
    entry_pass = make_entry(card, show="*")
    entry_pass.pack(pady=(2, 16), fill="x")

    # Fehleranzeige
    lbl_error = tk.Label(card, text="", bg=COLORS["bg_card"],
                          fg=COLORS["accent"], font=("Segoe UI", 10))
    lbl_error.pack()

    # "Angemeldet bleiben"-Checkbox
    keep_logged_in_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        card, text=t("keep_logged_in"),
        variable=keep_logged_in_var,
        bg=COLORS["bg_card"], fg=COLORS["text_dim"],
        selectcolor=COLORS["bg_mid"],
        activebackground=COLORS["bg_card"],
        activeforeground=COLORS["text_light"],
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(4, 8))

    def do_login():
        ok, result = auth.login(entry_user.get(), entry_pass.get())
        if ok:
            auth.set_current_user(result)
            app_state["language"] = result.get("language", "en")
            if keep_logged_in_var.get():
                auth.save_session(result["id"])
            else:
                auth.clear_session()
            show_screen(root, build_main_menu)
        else:
            lbl_error.config(text=result)

    def do_register():
        ok, result = auth.register(entry_user.get(), entry_pass.get(), app_state["language"])
        if ok:
            ok2, user = auth.login(entry_user.get(), entry_pass.get())
            if ok2:
                auth.set_current_user(user)
                app_state["language"] = user.get("language", "en")
                if keep_logged_in_var.get():
                    auth.save_session(user["id"])
                show_screen(root, build_main_menu)
        else:
            lbl_error.config(text=result)

    def do_guest():
        auth.logout()
        show_screen(root, build_main_menu)

    make_button(card, t("login"), do_login).pack(fill="x", pady=(8, 4))
    make_button(card, t("register"), do_register,
                bg=COLORS["accent2"]).pack(fill="x", pady=4)

    forgot_lbl = tk.Label(card, text=t("forgot_password"),
                          bg=COLORS["bg_card"], fg=COLORS["text_dim"],
                          font=("Segoe UI", 9), cursor="hand2")
    forgot_lbl.pack(anchor="e", pady=(2, 0))
    forgot_lbl.bind("<Button-1>", lambda e: show_forgot_password(root))
    forgot_lbl.bind("<Enter>", lambda e: forgot_lbl.config(fg=COLORS["text_light"]))
    forgot_lbl.bind("<Leave>", lambda e: forgot_lbl.config(fg=COLORS["text_dim"]))

    # Trennlinie
    tk.Frame(card, bg=COLORS["text_dim"], height=1).pack(fill="x", pady=12)

    make_button(card, t("play_guest"), do_guest,
                bg="#444466").pack(fill="x")

    # Sprache wechseln
    def toggle_lang():
        app_state["language"] = "de" if app_state["language"] == "en" else "en"
        show_screen(root, build_login_screen)

    lang_btn = tk.Label(
        frame, text="DE / EN",
        bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
        font=("Segoe UI", 9), cursor="hand2", padx=6, pady=4
    )
    lang_btn.bind("<Button-1>", lambda e: toggle_lang())
    lang_btn.pack(pady=10)


# ─────────────────────────────────────────────
# HAUPTMENÜ
# ─────────────────────────────────────────────
def build_main_menu(root, frame):
    """Baut das Hauptmenü."""
    set_gif_background(frame)

    user = auth.get_current_user()
    name = user["username"] if user else "Guest"

    # Header (bg_dark = transparent zum GIF)
    header = tk.Frame(frame, bg=COLORS["bg_dark"], pady=12)
    header.pack(fill="x")

    # Controller-Logo links neben HHBKTendo
    logo_img = None
    try:
        from PIL import Image, ImageTk
        import os
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "Mockups", "Assets", "Logo", "Only_Controller_Logo_HHBKTendo.png")
        logo_pil = Image.open(logo_path).convert("RGBA")

        # Hintergrundfarbe (Eckpixel oben-links) transparent machen
        pixels = logo_pil.load()
        bg_color = pixels[0, 0][:3]  # RGB des Hintergrunds
        tolerance = 30               # Farbtoleranz für leichte Verläufe
        for y in range(logo_pil.height):
            for x in range(logo_pil.width):
                r, g, b, a = pixels[x, y]
                if all(abs(int(c) - int(bg)) <= tolerance for c, bg in zip((r, g, b), bg_color)):
                    pixels[x, y] = (r, g, b, 0)  # transparent

        # Auf Header-Höhe skalieren, Seitenverhältnis beibehalten
        target_h = 44
        target_w = int(logo_pil.width * target_h / logo_pil.height)
        logo_pil = logo_pil.resize((target_w, target_h), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pil)
    except Exception:
        pass

    if logo_img:
        lbl_logo = tk.Label(header, image=logo_img, bg=COLORS["bg_dark"])
        lbl_logo.image = logo_img  # Referenz halten, sonst löscht Garbage Collector das Bild
        lbl_logo.pack(side="left", padx=(12, 4))
    else:
        tk.Label(header, text="🎮",
                 bg=COLORS["bg_dark"], font=("Segoe UI", 20)).pack(side="left", padx=(16, 2))

    tk.Label(header, text="HHBKTendo",
             bg=COLORS["bg_dark"], fg=COLORS["accent"],
             font=("Segoe UI", 20, "bold")).pack(side="left", padx=(0, 4))
    tk.Label(header, text=f"  {name}",
             bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
             font=("Segoe UI", 11)).pack(side="left")

    def do_logout():
        auth.logout()
        show_screen(root, build_login_screen)

    def toggle_lang():
        app_state["language"] = "de" if app_state["language"] == "en" else "en"
        if user:
            database.update_user_language(user["id"], app_state["language"])
        show_screen(root, build_main_menu)

    lang_btn = tk.Label(
        header, text="DE/EN",
        bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
        font=("Segoe UI", 9), cursor="hand2", padx=6, pady=4
    )
    lang_btn.bind("<Button-1>", lambda e: toggle_lang())
    lang_btn.pack(side="right", padx=5)

    if user:
        make_button(header, t("logout"), do_logout, width=10,
                    bg=COLORS["bg_dark"], fg=COLORS["text_dim"]).pack(side="right", padx=10)
    else:
        make_button(header, t("login"),
                    lambda: show_screen(root, build_login_screen), width=10,
                    bg=COLORS["bg_dark"], fg=COLORS["text_dim"]).pack(side="right", padx=10)

    # Titel
    make_label(frame, t("select_game"), size=16, bold=True).pack(pady=(30, 10))

    # Spielauswahl-Karten
    games_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
    games_frame.pack(pady=10)

    for game_key, label in [("pawn_chess", t("pawn_chess")),
                              ("tictactoe", t("tictactoe"))]:
        card = tk.Frame(games_frame, bg=COLORS["bg_card"], padx=20, pady=20)
        card.pack(side="left", padx=15, pady=10)

        tk.Label(card, text=label,
                 bg=COLORS["bg_card"], fg=COLORS["text_light"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))

        # Schwierigkeit wählen
        tk.Label(card, text=t("difficulty"),
                 bg=COLORS["bg_card"], fg=COLORS["text_dim"],
                 font=("Segoe UI", 10)).pack()

        diff_levels = [
            (1, t("easy")), (2, t("medium")), (3, t("hard")),
            (4, t("expert")), (5, t("master"))
        ]
        diff_var = tk.IntVar(value=3)
        diff_frame = tk.Frame(card, bg=COLORS["bg_card"])
        diff_frame.pack(pady=6)
        make_radio_group(diff_frame, diff_levels, diff_var)

        # Factory-Funktion: verhindert, dass alle Schleifendurchläufe
        # dieselbe Variable referenzieren (Closure-over-loop-variable-Problem)
        def make_play_cmd(gk, dv):
            def cmd():
                app_state["game"] = gk
                app_state["difficulty"] = dv.get()
                show_screen(root, build_game_screen)
            return cmd

        make_button(card, t("play"),
                    make_play_cmd(game_key, diff_var)).pack(pady=(10, 4))

        def make_lb_cmd(gk, dv):
            def cmd():
                show_leaderboard(root, gk, dv.get())
            return cmd

        make_button(card, t("leaderboard"),
                    make_lb_cmd(game_key, diff_var),
                    bg=COLORS["accent2"]).pack(pady=4)


# ─────────────────────────────────────────────
# BESTENLISTE
# ─────────────────────────────────────────────
def show_leaderboard(root, game, difficulty):
    """Zeigt die Bestenliste als Popup."""
    win = tk.Toplevel(root)
    win.title(t("leaderboard"))
    win.configure(bg=COLORS["bg_dark"])
    win.geometry("450x400")
    win.resizable(False, False)

    game_name = t("pawn_chess") if game == "pawn_chess" else t("tictactoe")
    diff_names = ["", t("easy"), t("medium"), t("hard"), t("expert"), t("master")]
    diff_name = diff_names[difficulty] if difficulty <= 5 else str(difficulty)

    tk.Label(win, text=t("leaderboard"),
             bg=COLORS["bg_dark"], fg=COLORS["accent"],
             font=("Segoe UI", 16, "bold")).pack(pady=(20, 4))
    tk.Label(win, text=f"{game_name} – {t('level')}: {diff_name}",
             bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
             font=("Segoe UI", 11)).pack(pady=(0, 15))

    entries = database.get_leaderboard(game, difficulty)

    SEP_COLOR = "#3a3a5a"  # dünne Trennlinie zwischen Spalten
    COLUMNS = [
        (t("rank"),   5),
        (t("player"), 16),
        (t("wins"),   6),
        (t("losses"), 8),
        (t("games"),  6),
    ]

    # Tabellenkopf (Überschriften mittig, Trennlinien zwischen Spalten)
    cols_frame = tk.Frame(win, bg=COLORS["bg_mid"])
    cols_frame.pack(fill="x", padx=20)
    for i, (col, width) in enumerate(COLUMNS):
        if i > 0:
            tk.Frame(cols_frame, bg=SEP_COLOR, width=1).pack(
                side="left", fill="y", pady=4)
        tk.Label(cols_frame, text=col, width=width,
                 bg=COLORS["bg_mid"], fg=COLORS["accent"],
                 font=("Segoe UI", 10, "bold"), anchor="center").pack(side="left", padx=4)

    if not entries:
        tk.Label(win, text=t("no_entries"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_dim"],
                 font=("Segoe UI", 11)).pack(pady=20)
    else:
        for i, entry in enumerate(entries, 1):
            bg = COLORS["bg_dark"] if i % 2 else COLORS["bg_card"]
            row_frame = tk.Frame(win, bg=bg)
            row_frame.pack(fill="x", padx=20)
            row_vals = [
                (str(i),                    5),
                (entry["username"],         16),
                (str(entry["wins"]),         6),
                (str(entry["losses"]),       8),
                (str(entry["total_games"]),  6),
            ]
            for j, (val, width) in enumerate(row_vals):
                if j > 0:
                    tk.Frame(row_frame, bg=SEP_COLOR, width=1).pack(
                        side="left", fill="y", pady=2)
                tk.Label(row_frame, text=val, width=width,
                         bg=bg, fg=COLORS["text_light"],
                         font=("Segoe UI", 10), anchor="w").pack(side="left", padx=4, pady=3)

    make_button(win, t("close"), win.destroy, width=12).pack(pady=20)


# ─────────────────────────────────────────────
# SPIELREGELN POPUP
# ─────────────────────────────────────────────
def show_rules(root, game):
    """Zeigt die Spielregeln als Popup."""
    win = tk.Toplevel(root)
    win.title(t("rules"))
    win.configure(bg=COLORS["bg_dark"])
    win.geometry("420x380")
    win.resizable(False, False)

    lang = app_state["language"]
    if game == "pawn_chess":
        rules_text = pc.RULES_DE if lang == "de" else pc.RULES_EN
    else:
        rules_text = ttt.RULES_DE if lang == "de" else ttt.RULES_EN

    tk.Label(win, text=t("rules"),
             bg=COLORS["bg_dark"], fg=COLORS["accent"],
             font=("Segoe UI", 15, "bold")).pack(pady=(20, 10))

    text_widget = tk.Text(win, bg=COLORS["bg_card"], fg=COLORS["text_light"],
                          font=("Segoe UI", 10), relief="flat",
                          padx=15, pady=15, wrap="word")
    text_widget.pack(fill="both", expand=True, padx=20)
    text_widget.insert("1.0", rules_text)
    text_widget.config(state="disabled")

    make_button(win, t("close"), win.destroy, width=12).pack(pady=15)


# ─────────────────────────────────────────────
# SPIELSCREEN
# ─────────────────────────────────────────────
CELL_SIZE = 72
PIECE_RADIUS = 26

board_canvas = None
status_label = None
game_widgets = {}  # Referenzen auf dynamische Widgets


def build_game_screen(root, frame):
    """Baut den Spielscreen auf."""
    global board_canvas, status_label, game_widgets
    game_widgets = {}
    set_gif_background(frame)

    game = app_state["game"]
    user = auth.get_current_user()

    # Spielfeld initialisieren
    if game == "pawn_chess":
        app_state["board"] = pc.create_board()
    else:
        app_state["board"] = ttt.create_board()

    app_state["human_turn"] = True
    app_state["selected"] = None
    app_state["valid_moves"] = []
    app_state["game_over"] = False
    app_state["ai_thinking"] = False

    # Header (bg_dark = transparent zum GIF)
    header = tk.Frame(frame, bg=COLORS["bg_dark"], pady=10)
    header.pack(fill="x")

    game_name = t("pawn_chess") if game == "pawn_chess" else t("tictactoe")
    diff_names = ["", t("easy"), t("medium"), t("hard"), t("expert"), t("master")]
    diff_name = diff_names[app_state["difficulty"]]

    tk.Label(header, text="BlitzBoard",
             bg=COLORS["bg_dark"], fg=COLORS["accent"],
             font=("Segoe UI", 16, "bold")).pack(side="left", padx=(20, 6))
    tk.Label(header, text=f"{game_name}  |  {t('level')}: {diff_name}",
             bg=COLORS["bg_dark"], fg=COLORS["text_light"],
             font=("Segoe UI", 13, "bold")).pack(side="left", padx=(0, 20))

    def do_abort():
        if messagebox.askyesno(t("abort"), t("confirm_abort")):
            show_screen(root, build_main_menu)

    btn_frame = tk.Frame(header, bg=COLORS["bg_dark"])
    btn_frame.pack(side="right", padx=10)
    make_button(btn_frame, t("rules"),
                lambda: show_rules(root, game), width=10,
                bg=COLORS["accent2"]).pack(side="left", padx=5)
    make_button(btn_frame, t("abort"), do_abort, width=12,
                bg="#666688").pack(side="left", padx=5)

    # Gasthinweis
    if auth.is_guest():
        tk.Label(frame, text=t("guest_no_save"),
                 bg=COLORS["bg_dark"], fg=COLORS["draw"],
                 font=("Segoe UI", 9)).pack(pady=(6, 0))

    # Status-Label
    status_label = tk.Label(frame, text=t("your_turn"),
                             bg=COLORS["bg_dark"], fg=COLORS["text_light"],
                             font=("Segoe UI", 13, "bold"))
    status_label.pack(pady=(12, 6))

    # Spielfeld-Canvas
    canvas_size = CELL_SIZE * 6
    board_canvas = tk.Canvas(frame, width=canvas_size, height=canvas_size,
                              bg=COLORS["bg_dark"], highlightthickness=0)
    board_canvas.pack(pady=10)

    draw_board()

    board_canvas.bind("<Button-1>", on_board_click)

    # Zurück-Button
    game_widgets["back_btn"] = make_button(
        frame, t("main_menu"),
        lambda: show_screen(root, build_main_menu),
        bg="#444466"
    )
    game_widgets["back_btn"].pack(pady=10)
    game_widgets["back_btn"].pack_forget()  # erst nach Spielende zeigen


def draw_board():
    """Zeichnet das Spielfeld und alle Figuren."""
    if not board_canvas:
        return
    board_canvas.delete("all")
    board = app_state["board"]
    game = app_state["game"]
    selected = app_state["selected"]
    valid_moves = app_state["valid_moves"]

    # Nur Zielfelder extrahieren (Index 2,3 im Zug-Tupel: to_row, to_col)
    valid_targets = set((m[2], m[3]) for m in valid_moves) if game == "pawn_chess" else set()

    for row in range(6):
        for col in range(6):
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            # Feldfarbe
            if (row + col) % 2 == 0:
                cell_color = COLORS["board_light"]
            else:
                cell_color = COLORS["board_dark"]

            # Ausgewähltes Feld hervorheben
            is_selected = (selected == (row, col))
            if is_selected:
                cell_color = COLORS["highlight"]

            # Gültige Züge markieren
            is_valid_target = game == "pawn_chess" and (row, col) in valid_targets
            if is_valid_target:
                cell_color = COLORS["valid_move"]

            # Kontur: normale Felder bekommen eine dünne Trennlinie
            border_color = "#444444"
            border_width = 1
            if is_selected:
                border_color = COLORS["highlight_out"]
                border_width = 3
            elif is_valid_target:
                border_color = COLORS["valid_move_out"]
                border_width = 3

            board_canvas.create_rectangle(x0, y0, x1, y1,
                                           fill=cell_color,
                                           outline=border_color,
                                           width=border_width)

            # Figuren zeichnen
            cell = board[row][col]
            cx = x0 + CELL_SIZE // 2
            cy = y0 + CELL_SIZE // 2
            r = PIECE_RADIUS

            if game == "pawn_chess":
                if cell == pc.WHITE:
                    # Weißer Bauer: reines Weiß, dunkle Kontur → sichtbar auf jedem Feld
                    _draw_piece(board_canvas, cx, cy, r,
                                COLORS["white_piece"], COLORS["white_piece_out"])
                    # Kleines "W"-Symbol zur Unterscheidung
                    board_canvas.create_text(cx, cy, text="♙",
                                              fill=COLORS["white_piece_out"],
                                              font=("Arial", 22, "bold"))
                elif cell == pc.BLACK:
                    # Schwarzer Bauer: dunkles Blau, helle Kontur → sichtbar auf jedem Feld
                    _draw_piece(board_canvas, cx, cy, r,
                                COLORS["black_piece"], COLORS["black_piece_out"])
                    board_canvas.create_text(cx, cy, text="♟",
                                              fill=COLORS["black_piece_out"],
                                              font=("Arial", 22, "bold"))

            elif game == "tictactoe":
                if cell == ttt.HUMAN:
                    # X: hellblau, breite Linien, dunkle Umrahmung → gut lesbar
                    d = 20
                    for dx, dy in [(1, 1), (-1, -1)]:
                        board_canvas.create_line(
                            cx - d * dx, cy - d * dy,
                            cx + d * dx, cy + d * dy,
                            fill="#1a237e", width=6)
                    for dx, dy in [(1, -1), (-1, 1)]:
                        board_canvas.create_line(
                            cx - d * dx, cy - d * dy,
                            cx + d * dx, cy + d * dy,
                            fill="#1a237e", width=6)
                    # Heller Vordergrund
                    for dx, dy in [(1, 1), (-1, -1)]:
                        board_canvas.create_line(
                            cx - d * dx, cy - d * dy,
                            cx + d * dx, cy + d * dy,
                            fill=COLORS["ttt_x"], width=3)
                    for dx, dy in [(1, -1), (-1, 1)]:
                        board_canvas.create_line(
                            cx - d * dx, cy - d * dy,
                            cx + d * dx, cy + d * dy,
                            fill=COLORS["ttt_x"], width=3)

                elif cell == ttt.AI:
                    # O: rot, breite Kontur, dunkle Schatten-Oval → gut lesbar
                    board_canvas.create_oval(cx - 22, cy - 22, cx + 22, cy + 22,
                                              outline="#7f0000", width=6)
                    board_canvas.create_oval(cx - 22, cy - 22, cx + 22, cy + 22,
                                              outline=COLORS["ttt_o"], width=3)


def _draw_piece(canvas, cx, cy, r, fill, outline):
    """Zeichnet eine runde Spielfigur mit Schatten-Effekt für Tiefenwirkung."""
    # Schatten (leicht versetzt)
    canvas.create_oval(cx - r + 3, cy - r + 3, cx + r + 3, cy + r + 3,
                        fill="#111111",
                        outline="")
    # Haupt-Oval
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                        fill=fill, outline=outline, width=3)


def on_board_click(event):
    """Verarbeitet Klicks auf das Spielfeld."""
    if app_state["game_over"] or app_state["ai_thinking"]:
        return
    if not app_state["human_turn"]:
        return

    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if not (0 <= row < 6 and 0 <= col < 6):
        return

    game = app_state["game"]

    if game == "pawn_chess":
        handle_pawn_chess_click(row, col)
    elif game == "tictactoe":
        handle_tictactoe_click(row, col)


def handle_tictactoe_click(row, col):
    """Verarbeitet einen Klick im Tic-Tac-Toe."""
    board = app_state["board"]
    if board[row][col] != ttt.EMPTY:
        return

    # Menschlichen Zug ausführen
    app_state["board"] = ttt.apply_move(board, (row, col), False)
    draw_board()

    # Gewinner prüfen
    winner = ttt.check_winner(app_state["board"])
    if winner:
        end_game(winner)
        return

    # KI-Zug
    app_state["human_turn"] = False
    start_ai_turn()


def handle_pawn_chess_click(row, col):
    """Verarbeitet einen Klick im Bauernschach."""
    board = app_state["board"]
    selected = app_state["selected"]
    valid_moves = app_state["valid_moves"]

    # Prüfe ob Ziel eines gültigen Zugs angeklickt
    if selected is not None:
        target_move = next(
            (m for m in valid_moves if m[2] == row and m[3] == col), None
        )
        if target_move:
            app_state["board"] = pc.apply_move(board, target_move, False)
            app_state["selected"] = None
            app_state["valid_moves"] = []
            draw_board()

            winner = pc.check_winner(app_state["board"])
            if winner:
                end_game(winner)
                return

            app_state["human_turn"] = False
            start_ai_turn()
            return

    # Neue Figur auswählen
    if board[row][col] == pc.WHITE:
        all_moves = pc.get_valid_moves(board, False)
        piece_moves = [m for m in all_moves if m[0] == row and m[1] == col]  # Nur Züge dieser Figur (from_row, from_col)
        app_state["selected"] = (row, col)
        app_state["valid_moves"] = piece_moves
    else:
        app_state["selected"] = None
        app_state["valid_moves"] = []

    draw_board()


def start_ai_turn():
    """Startet den KI-Zug in einem separaten Thread (LN5010)."""
    status_label.config(text=t("ai_thinking"), fg=COLORS["text_dim"])
    app_state["ai_thinking"] = True

    def ai_worker():
        game = app_state["game"]
        board = app_state["board"]
        depth = app_state["difficulty"]

        if game == "pawn_chess":
            best_move = mm.get_best_move(
                board, depth,
                pc.get_valid_moves, pc.apply_move,
                pc.evaluate, pc.is_terminal
            )
            if best_move:
                new_board = pc.apply_move(board, best_move, True)
                app_state["board"] = new_board

            winner = pc.check_winner(app_state["board"])

        elif game == "tictactoe":
            best_move = mm.get_best_move(
                board, depth,
                ttt.get_valid_moves, ttt.apply_move,
                ttt.evaluate, ttt.is_terminal
            )
            if best_move:
                new_board = ttt.apply_move(board, best_move, True)
                app_state["board"] = new_board

            winner = ttt.check_winner(app_state["board"])

        app_state["ai_thinking"] = False

        # GUI-Update im Hauptthread
        board_canvas.after(0, lambda: after_ai_turn(winner))

    thread = threading.Thread(target=ai_worker, daemon=True)  # daemon=True: Thread endet automatisch mit dem Programm
    thread.start()


def after_ai_turn(winner):
    """Wird nach dem KI-Zug im Hauptthread aufgerufen."""
    draw_board()
    if winner:
        end_game(winner)
    else:
        app_state["human_turn"] = True
        status_label.config(text=t("your_turn"), fg=COLORS["text_light"])


def end_game(winner):
    """Beendet das Spiel und zeigt das Ergebnis an."""
    app_state["game_over"] = True
    game = app_state["game"]
    user = auth.get_current_user()

    # Gewinner bestimmen
    human_won = winner in ("white", "human")
    ai_won = winner in ("black", "ai")
    is_draw = winner == "draw"

    if human_won:
        msg = t("you_win")
        color = COLORS["win"]
        won = True
    elif ai_won:
        msg = t("ai_wins")
        color = COLORS["lose"]
        won = False
    else:
        msg = t("draw")
        color = COLORS["draw"]
        won = False

    status_label.config(text=msg, fg=color, font=("Segoe UI", 16, "bold"))

    # Ergebnis speichern (LF4080, LF4090)
    if user and not is_draw:
        database.save_result(user["id"], game, app_state["difficulty"], won)

    # Zurück-Button einblenden
    if "back_btn" in game_widgets:
        game_widgets["back_btn"].pack(pady=10)


# ─────────────────────────────────────────────
# PROGRAMMSTART
# ─────────────────────────────────────────────
def main():
    """Startet die Anwendung."""
    database.init_db()

    root = tk.Tk()
    root.title("BlitzBoard")
    root.geometry("820x700")
    root.minsize(720, 600)
    root.configure(bg=COLORS["bg_dark"])

    # GIF-Frames einmalig laden und globalen Animations-Takt starten
    _gif["root"] = root
    _load_gif_frames()
    if _gif["frames"]:
        _gif_tick()

    # Fenstericon: Controller-Logo aus den Assets
    try:
        import os
        from PIL import Image, ImageTk
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "Mockups", "Assets", "Logo",
                                 "Only_Controller_Logo_HHBKTendo.png")
        icon_pil = Image.open(icon_path).convert("RGBA")
        # Hintergrund transparent machen (gleiche Logik wie im Header)
        pixels = icon_pil.load()
        bg_color = pixels[0, 0][:3]
        for y in range(icon_pil.height):
            for x in range(icon_pil.width):
                r, g, b, a = pixels[x, y]
                if all(abs(int(c) - int(bg)) <= 30 for c, bg in zip((r, g, b), bg_color)):
                    pixels[x, y] = (r, g, b, 0)
        icon_pil = icon_pil.resize((32, 32), Image.LANCZOS)
        icon_img = ImageTk.PhotoImage(icon_pil)
        root.iconphoto(True, icon_img)
        root._icon_img = icon_img  # Referenz halten
    except Exception:
        pass

    # Auto-Login: gespeicherte Session laden
    saved_user = auth.load_session()
    if saved_user:
        auth.set_current_user(saved_user)
        app_state["language"] = saved_user.get("language", "en")
        show_screen(root, build_main_menu)
    else:
        show_screen(root, build_login_screen)

    root.mainloop()


if __name__ == "__main__":
    main()
