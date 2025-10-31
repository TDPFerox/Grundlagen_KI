# Implementieren Sie den Minimax-Algorithmus (wie in der VL besprochen) am Beispiel Tic Tac Toe in einer Sprache Ihrer Wahl

import math
import copy

class TicTacToe:
    def __init__(self):
        # Spielfeld: 3x3 Matrix, leere Felder sind None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player = 'X'  # Menschlicher Spieler
        self.ai = 'O'      # KI-Spieler
        self.nodes_visited = 0  # Zähler für besuchte Knoten
        self.nodes_visited_with_pruning = 0  # Zähler für Knoten mit Pruning
    
    def print_board(self):
        """Gibt das aktuelle Spielfeld aus"""
        print("\n")
        for i, row in enumerate(self.board):
            row_display = []
            for cell in row:
                if cell is None:
                    row_display.append(' ')
                else:
                    row_display.append(cell)
            print(f" {row_display[0]} | {row_display[1]} | {row_display[2]} ")
            if i < 2:
                print("-----------")
        print("\n")
    
    def available_moves(self):
        """Gibt eine Liste aller verfügbaren Züge zurück"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    moves.append((i, j))
        return moves
    
    def make_move(self, row, col, player):
        """Führt einen Zug aus"""
        if self.board[row][col] is None:
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        """
        Prüft ob es einen Gewinner gibt
        Rückgabe: 'X', 'O', 'tie', oder None (Spiel läuft noch)
        """
        # Horizontale Linien prüfen
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        
        # Vertikale Linien prüfen
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]
        
        # Diagonale prüfen (links oben nach rechts unten)
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        
        # Diagonale prüfen (rechts oben nach links unten)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]
        
        # Unentschieden prüfen
        if not self.available_moves():
            return 'tie'
        
        # Spiel läuft noch
        return None
    
    
    def minimax_without_pruning(self, depth, is_maximizing):
        """
        Minimax-Algorithmus OHNE Alpha-Beta-Pruning (zum Vergleich)
        depth: Aktuelle Tiefe im Spielbaum
        is_maximizing: True wenn KI (Maximierer) am Zug ist, False wenn Spieler (Minimierer)
        Rückgabe: Bester Score für die aktuelle Position
        """
        self.nodes_visited += 1
        winner = self.check_winner()
        
        # Terminalzustände bewerten
        if winner == self.ai:
            return 10 - depth
        elif winner == self.player:
            return depth - 10
        elif winner == 'tie':
            return 0
        
        if is_maximizing:
            max_score = -math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.ai
                score = self.minimax_without_pruning(depth + 1, False)
                self.board[row][col] = None
                max_score = max(score, max_score)
            return max_score
        else:
            min_score = math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.player
                score = self.minimax_without_pruning(depth + 1, True)
                self.board[row][col] = None
                min_score = min(score, min_score)
            return min_score
    
    def minimax(self, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        """
        Minimax-Algorithmus mit Alpha-Beta-Pruning
        depth: Aktuelle Tiefe im Spielbaum
        is_maximizing: True wenn KI (Maximierer) am Zug ist, False wenn Spieler (Minimierer)
        alpha: Bester Wert für Maximierer (anfangs -∞)
        beta: Bester Wert für Minimierer (anfangs +∞)
        Rückgabe: Bester Score für die aktuelle Position
        """
        self.nodes_visited_with_pruning += 1
        winner = self.check_winner()
        
        # Terminalzustände bewerten
        if winner == self.ai:
            return 10 - depth  # KI gewinnt (bevorzuge schnellere Siege)
        elif winner == self.player:
            return depth - 10  # Spieler gewinnt (bevorzuge längere Niederlagen)
        elif winner == 'tie':
            return 0  # Unentschieden
        
        if is_maximizing:
            # KI ist am Zug - maximiere den Score
            max_score = -math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.ai
                score = self.minimax(depth + 1, False, alpha, beta)
                self.board[row][col] = None
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                # Beta-Cutoff: Wenn alpha >= beta, kann dieser Zweig abgeschnitten werden
                if beta <= alpha:
                    break
            return max_score
        else:
            # Spieler ist am Zug - minimiere den Score
            min_score = math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.player
                score = self.minimax(depth + 1, True, alpha, beta)
                self.board[row][col] = None
                min_score = min(score, min_score)
                beta = min(beta, score)
                # Alpha-Cutoff: Wenn beta <= alpha, kann dieser Zweig abgeschnitten werden
                if beta <= alpha:
                    break
            return min_score
    
    
    def compare_algorithms(self):
        """
        Vergleicht Minimax mit und ohne Alpha-Beta-Pruning
        Zählt die Anzahl der besuchten Knoten für beide Varianten
        """
        print("\n=== Vergleich: Minimax vs. Alpha-Beta-Pruning ===\n")
        
        # Speichere aktuelles Spielfeld
        board_copy = copy.deepcopy(self.board)
        
        # Test ohne Pruning
        self.nodes_visited = 0
        self.minimax_without_pruning(0, True)
        nodes_without_pruning = self.nodes_visited
        
        # Spielfeld wiederherstellen
        self.board = copy.deepcopy(board_copy)
        
        # Test mit Pruning
        self.nodes_visited_with_pruning = 0
        self.minimax(0, True)
        nodes_with_pruning = self.nodes_visited_with_pruning
        
        # Spielfeld wiederherstellen
        self.board = board_copy
        
        # Ergebnisse ausgeben
        print(f"Spielsituation:")
        self.print_board()
        print(f"Minimax OHNE Pruning:  {nodes_without_pruning:6d} Knoten besucht")
        print(f"Minimax MIT Pruning:   {nodes_with_pruning:6d} Knoten besucht")
        print(f"Reduzierung:           {nodes_without_pruning - nodes_with_pruning:6d} Knoten ({100 * (nodes_without_pruning - nodes_with_pruning) / nodes_without_pruning:.1f}%)")
        print(f"Effizienzgewinn:       {nodes_without_pruning / nodes_with_pruning:.2f}x schneller\n")
        
        return nodes_without_pruning, nodes_with_pruning
    
    def find_best_move(self):
        """
        Findet den besten Zug für die KI mittels Minimax mit Alpha-Beta-Pruning
        Rückgabe: (row, col) Tupel mit dem besten Zug
        """
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        
        for move in self.available_moves():
            row, col = move
            self.board[row][col] = self.ai
            score = self.minimax(0, False, alpha, beta)
            self.board[row][col] = None
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
        
        return best_move
    
    def play(self):
        """Hauptspielschleife"""
        print("=== Tic Tac Toe mit Minimax-KI (Alpha-Beta-Pruning) ===")
        print(f"Du spielst als '{self.player}', die KI spielt als '{self.ai}'")
        print("Gib deine Züge als 'Zeile Spalte' ein (0-2, z.B. '1 1' für Mitte)")
        print("Alpha-Beta-Pruning reduziert die Anzahl der zu durchsuchenden Knoten!\n")
        
        current_player = self.player
        
        while True:
            self.print_board()
            winner = self.check_winner()
            
            if winner is not None:
                if winner == 'tie':
                    print("Unentschieden!")
                else:
                    print(f"Spieler {winner} gewinnt!")
                break
            
            if current_player == self.player:
                # Menschlicher Spieler
                while True:
                    try:
                        move_input = input("Dein Zug (Zeile Spalte): ")
                        row, col = map(int, move_input.split())
                        if 0 <= row <= 2 and 0 <= col <= 2:
                            if self.make_move(row, col, self.player):
                                break
                            else:
                                print("Dieses Feld ist bereits belegt!")
                        else:
                            print("Ungültige Eingabe! Gib Zahlen zwischen 0 und 2 ein.")
                    except:
                        print("Ungültige Eingabe! Format: Zeile Spalte (z.B. '1 1')")
                
                current_player = self.ai
            else:
                # KI-Spieler
                print("KI denkt nach...")
                best_move = self.find_best_move()
                if best_move:
                    row, col = best_move
                    self.make_move(row, col, self.ai)
                    print(f"KI spielt: {row} {col}")
                
                current_player = self.player


def run_comparison_scenarios():
    """
    Führt Vergleichstests in verschiedenen Spielsituationen durch
    """
    print("\n" + "="*60)
    print("VERGLEICH: MINIMAX MIT UND OHNE ALPHA-BETA-PRUNING")
    print("="*60)
    
    scenarios = []
    
    # Szenario 1: Leeres Spielfeld (maximale Komplexität)
    print("\n### SZENARIO 1: Leeres Spielfeld (Spielstart) ###")
    game1 = TicTacToe()
    nodes_without_1, nodes_with_1 = game1.compare_algorithms()
    scenarios.append(("Leeres Spielfeld", nodes_without_1, nodes_with_1))
    
    # Szenario 2: Nach einem Zug
    print("\n### SZENARIO 2: Nach dem ersten Zug (Mitte belegt) ###")
    game2 = TicTacToe()
    game2.board[1][1] = 'O'  # KI hat Mitte gespielt
    nodes_without_2, nodes_with_2 = game2.compare_algorithms()
    scenarios.append(("Nach 1 Zug", nodes_without_2, nodes_with_2))
    
    # Szenario 3: Mittleres Spiel (4 Züge gespielt)
    print("\n### SZENARIO 3: Mittleres Spiel (4 Züge) ###")
    game3 = TicTacToe()
    game3.board[0][0] = 'X'
    game3.board[1][1] = 'O'
    game3.board[0][2] = 'X'
    game3.board[2][0] = 'O'
    nodes_without_3, nodes_with_3 = game3.compare_algorithms()
    scenarios.append(("Mittleres Spiel", nodes_without_3, nodes_with_3))
    
    # Szenario 4: Spätes Spiel (6 Züge gespielt)
    print("\n### SZENARIO 4: Spätes Spiel (6 Züge) ###")
    game4 = TicTacToe()
    game4.board[0][0] = 'X'
    game4.board[0][1] = 'O'
    game4.board[1][1] = 'X'
    game4.board[0][2] = 'O'
    game4.board[2][2] = 'X'
    game4.board[1][0] = 'O'
    nodes_without_4, nodes_with_4 = game4.compare_algorithms()
    scenarios.append(("Spätes Spiel", nodes_without_4, nodes_with_4))
    
    # Szenario 5: Kritische Situation (Blockieren notwendig)
    print("\n### SZENARIO 5: Kritische Situation (Block erforderlich) ###")
    game5 = TicTacToe()
    game5.board[0][0] = 'X'
    game5.board[1][1] = 'O'
    game5.board[0][1] = 'X'
    # X droht in [0][2] zu gewinnen
    nodes_without_5, nodes_with_5 = game5.compare_algorithms()
    scenarios.append(("Kritische Situation", nodes_without_5, nodes_with_5))
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("ZUSAMMENFASSUNG")
    print("="*60)
    print(f"{'Szenario':<25} {'Ohne Pruning':>12} {'Mit Pruning':>12} {'Reduzierung':>10}")
    print("-"*60)
    
    total_without = 0
    total_with = 0
    
    for scenario_name, without, with_p in scenarios:
        reduction = 100 * (without - with_p) / without if without > 0 else 0
        print(f"{scenario_name:<25} {without:>12d} {with_p:>12d} {reduction:>9.1f}%")
        total_without += without
        total_with += with_p
    
    print("-"*60)
    total_reduction = 100 * (total_without - total_with) / total_without if total_without > 0 else 0
    print(f"{'GESAMT':<25} {total_without:>12d} {total_with:>12d} {total_reduction:>9.1f}%")
    print(f"\nDurchschnittlicher Effizienzgewinn: {total_without / total_with:.2f}x schneller")
    print("="*60 + "\n")


def main():
    """Hauptfunktion zum Starten des Spiels"""
    print("Wähle einen Modus:")
    print("1 - Gegen die KI spielen")
    print("2 - Algorithmen-Vergleich durchführen")
    
    choice = input("\nDeine Wahl (1 oder 2): ").strip()
    
    if choice == '2':
        run_comparison_scenarios()
    else:
        game = TicTacToe()
        game.play()


if __name__ == "__main__":
    main()