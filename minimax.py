"""
minimax.py - Generischer MiniMax-Algorithmus mit Alpha-Beta-Pruning
Wiederverwendbar für alle Spiele (LF4030, LF4120, LN5040)

Der Algorithmus arbeitet rekursiv und verwendet Callback-Funktionen,
um spielspezifische Logik einzubinden.
"""

import math

# Fixe Endwerte für eindeutige Spielausgänge (weit außerhalb jedes Heuristik-Scores)
SCORE_WIN  =  1000000   # KI gewinnt
SCORE_LOSS = -1000000   # Mensch gewinnt
SCORE_DRAW =  0


def minimax(board, depth, is_maximizing, alpha, beta,
            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn):
    """
    Generischer MiniMax-Algorithmus mit Alpha-Beta-Pruning (LF4120).

    Idee: Die KI (Maximizer) versucht den Score zu maximieren,
    der Mensch (Minimizer) versucht ihn zu minimieren.
    Der Algorithmus durchsucht den Spielbaum rekursiv bis zur
    angegebenen Tiefe und gibt den besten erreichbaren Score zurück.

    Alpha-Beta-Pruning bricht Äste ab, die den Score nicht mehr
    verbessern können – das spart Rechenzeit ohne das Ergebnis
    zu verändern.

    Parameter:
        board         - Aktuelle Spielfelddarstellung (unveränderlich, wird kopiert)
        depth         - Verbleibende Suchtiefe (Spielstärke)
        is_maximizing - True wenn KI (Maximizer), False wenn Mensch (Minimizer)
        alpha         - Bisher bester Score für den Maximizer (-inf am Anfang)
        beta          - Bisher bester Score für den Minimizer (+inf am Anfang)
        get_moves_fn  - fn(board, is_maximizing) -> Liste möglicher Züge
                        (pawn_chess: pc.get_valid_moves | tictactoe: ttt.get_valid_moves)
        apply_move_fn - fn(board, move, is_maximizing) -> neues Board (Kopie)
                        (pawn_chess: pc.apply_move | tictactoe: ttt.apply_move)
        evaluate_fn   - fn(board) -> numerischer Wert (positiv = gut für KI)
                        (pawn_chess: pc.evaluate    | tictactoe: ttt.evaluate)
        is_terminal_fn- fn(board) -> (terminal: bool, score: int oder None)
                        (pawn_chess: pc.is_terminal | tictactoe: ttt.is_terminal)

    Rückgabe:
        Numerischer Bewertungswert des besten Zugs
    """

    # --- Abbruchbedingungen (Blattknoten im Spielbaum) ---

    # Spiel ist entschieden (Sieg/Niederlage/Unentschieden)
    terminal, score = is_terminal_fn(board)
    if terminal:
        return score

    # Maximale Suchtiefe erreicht → Stellung heuristisch bewerten
    if depth == 0:
        return evaluate_fn(board)

    # --- Rekursiver Abstieg ---

    moves = get_moves_fn(board, is_maximizing)

    # Kein Zug möglich: der aktuelle Spieler verliert (Zugzwang)
    if not moves:
        return SCORE_LOSS if is_maximizing else SCORE_WIN

    if is_maximizing:
        # KI-Zug: höchstmöglichen Score suchen
        best_score = -math.inf
        for move in moves:
            new_board = apply_move_fn(board, move, is_maximizing)
            score = minimax(new_board, depth - 1, False, alpha, beta,
                            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)
            best_score = max(best_score, score)

            # alpha = bestes Ergebnis, das der Maximizer bisher sichern kann
            alpha = max(alpha, score)

            # Beta-Cut: der Minimizer hätte diesen Pfad bereits früher abgelehnt
            if beta <= alpha:
                break
        return best_score

    else:
        # Mensch-Zug: niedrigstmöglichen Score suchen
        best_score = math.inf
        for move in moves:
            new_board = apply_move_fn(board, move, is_maximizing)
            score = minimax(new_board, depth - 1, True, alpha, beta,
                            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)
            best_score = min(best_score, score)

            # beta = bestes Ergebnis, das der Minimizer bisher sichern kann
            beta = min(beta, score)

            # Alpha-Cut: der Maximizer hätte diesen Pfad bereits früher abgelehnt
            if beta <= alpha:
                break
        return best_score


def get_best_move(board, depth, get_moves_fn, apply_move_fn,
                  evaluate_fn, is_terminal_fn):
    """
    Findet den besten Zug für die KI (Maximizer) mit MiniMax.

    Diese Funktion ist der Einstiegspunkt: Sie iteriert alle möglichen
    KI-Züge auf der obersten Ebene und ruft minimax() für die
    entstehenden Folgestellungen auf. Der Zug mit dem höchsten
    zurückgegebenen Score wird ausgewählt.

    Rückgabe:
        Bester Zug oder None wenn keine Züge möglich
    """
    best_score = -math.inf
    best_move = None

    # Startwerte für Alpha-Beta (noch kein Ast abgeschnitten)
    alpha = -math.inf
    beta  =  math.inf

    moves = get_moves_fn(board, True)
    if not moves:
        return None

    for move in moves:
        # Zug probeweise ausführen
        new_board = apply_move_fn(board, move, True)

        # Bewertung der Folgestellung aus Sicht des Minimizers (Mensch ist als nächstes dran)
        score = minimax(new_board, depth - 1, False, alpha, beta,
                        get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)

        # Besten Zug merken
        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

    return best_move
