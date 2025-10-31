# Vereinfachter Minimax-Algorithmus für Nullsummenspiele
# Nutzt die Eigenschaft: Min-Value(s) = -Max-Value(s)

import math
import copy

class TicTacToeSimplified:
    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player = 'X'  # Menschlicher Spieler (Minimierer)
        self.ai = 'O'      # KI-Spieler (Maximierer)
        self.nodes_visited_original = 0
        self.nodes_visited_simplified = 0
    
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
    
    def check_winner(self):
        """Prüft ob es einen Gewinner gibt"""
        # Horizontale Linien prüfen
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        
        # Vertikale Linien prüfen
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]
        
        # Diagonale prüfen
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]
        
        # Unentschieden prüfen
        if not self.available_moves():
            return 'tie'
        
        return None
    
    def evaluate(self, depth):
        """Bewertungsfunktion aus Sicht des Maximierers (KI)"""
        winner = self.check_winner()
        if winner == self.ai:
            return 10 - depth  # KI gewinnt
        elif winner == self.player:
            return depth - 10  # Spieler gewinnt
        else:
            return 0  # Unentschieden
    
    # ============================================================
    # ORIGINAL MINIMAX (mit expliziter Min/Max-Unterscheidung)
    # ============================================================
    
    def minimax_original(self, depth, is_maximizing):
        """
        ORIGINAL Minimax mit expliziter Unterscheidung zwischen MIN und MAX
        """
        self.nodes_visited_original += 1
        winner = self.check_winner()
        
        if winner is not None:
            return self.evaluate(depth)
        
        if is_maximizing:
            # MAX-Spieler (KI)
            max_score = -math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.ai
                score = self.minimax_original(depth + 1, False)
                self.board[row][col] = None
                max_score = max(score, max_score)
            return max_score
        else:
            # MIN-Spieler (Gegner)
            min_score = math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.player
                score = self.minimax_original(depth + 1, True)
                self.board[row][col] = None
                min_score = min(score, min_score)
            return min_score
    
    # ============================================================
    # VEREINFACHTER MINIMAX (Nullsummen-Eigenschaft)
    # ============================================================
    
    def minimax_simplified(self, depth, current_player):
        """
        VEREINFACHTER Minimax für Nullsummenspiele
        
        Kernidee: In einem Nullsummenspiel gilt:
            Min-Value(s) = -Max-Value(s)
        
        Daher können wir immer aus Sicht des aktuellen Spielers maximieren
        und das Ergebnis für den Gegner negieren.
        
        Parameter:
        - depth: Aktuelle Tiefe
        - current_player: Spieler am Zug ('O' = KI, 'X' = Mensch)
        
        Rückgabe: Bester Wert aus Sicht von current_player
        """
        self.nodes_visited_simplified += 1
        winner = self.check_winner()
        
        if winner is not None:
            # Bewertung aus Sicht des aktuellen Spielers
            score = self.evaluate(depth)
            if current_player == self.player:
                # Aus Sicht des Spielers ist die Bewertung invertiert
                return -score
            return score
        
        # Bestimme Gegenspieler
        opponent = self.player if current_player == self.ai else self.ai
        
        # Maximiere aus Sicht des aktuellen Spielers
        best_score = -math.inf
        
        for move in self.available_moves():
            row, col = move
            self.board[row][col] = current_player
            
            # Rekursiver Aufruf für Gegenspieler
            # Negiere das Ergebnis (Nullsummen-Eigenschaft!)
            score = -self.minimax_simplified(depth + 1, opponent)
            
            self.board[row][col] = None
            best_score = max(score, best_score)
        
        return best_score
    
    def compare_algorithms(self):
        """Vergleicht beide Algorithmen"""
        print("\n" + "="*70)
        print("VERGLEICH: Original Minimax vs. Vereinfachter Minimax")
        print("="*70)
        
        board_copy = copy.deepcopy(self.board)
        
        # Test Original Minimax
        print("\n### ORIGINAL MINIMAX (explizite MIN/MAX-Unterscheidung) ###")
        self.nodes_visited_original = 0
        score_original = self.minimax_original(0, True)
        nodes_original = self.nodes_visited_original
        
        # Spielfeld wiederherstellen
        self.board = copy.deepcopy(board_copy)
        
        # Test Vereinfachter Minimax
        print("### VEREINFACHTER MINIMAX (Nullsummen-Eigenschaft) ###")
        self.nodes_visited_simplified = 0
        score_simplified = self.minimax_simplified(0, self.ai)
        nodes_simplified = self.nodes_visited_simplified
        
        # Spielfeld wiederherstellen
        self.board = board_copy
        
        # Ergebnisse
        print("\nSpielsituation:")
        self.print_board()
        
        print(f"Original Minimax:")
        print(f"  - Besuchte Knoten: {nodes_original:6d}")
        print(f"  - Bester Score:    {score_original:6d}")
        
        print(f"\nVereinfachter Minimax:")
        print(f"  - Besuchte Knoten: {nodes_simplified:6d}")
        print(f"  - Bester Score:    {score_simplified:6d}")
        
        print(f"\nErgebnis:")
        if score_original == score_simplified:
            print(f"  ✓ Beide Algorithmen liefern dasselbe Ergebnis: {score_original}")
        else:
            print(f"  ✗ FEHLER: Unterschiedliche Ergebnisse!")
        
        if nodes_original == nodes_simplified:
            print(f"  ✓ Beide besuchen gleich viele Knoten: {nodes_original}")
        else:
            print(f"  ⚠ Unterschiedliche Knotenanzahl (kann durch Implementierung variieren)")
        
        print("="*70 + "\n")
        
        return nodes_original, nodes_simplified


# ============================================================
# BEISPIELBAUM ZUR DEMONSTRATION
# ============================================================

class MiniMaxExampleTree:
    """
    Beispielbaum zur Demonstration des Unterschieds zwischen
    Original und Vereinfachtem Minimax
    """
    
    def __init__(self):
        # Beispielbaum mit vordefinierten Blatt-Werten
        # Struktur: 
        #           A (MAX)
        #         / | \
        #        B  C  D (MIN)
        #       /|  |  |\
        #      3 5  2  9 1 (Blätter)
        
        self.tree = {
            'A': {'type': 'MAX', 'children': ['B', 'C', 'D']},
            'B': {'type': 'MIN', 'children': ['B1', 'B2']},
            'C': {'type': 'MIN', 'children': ['C1']},
            'D': {'type': 'MIN', 'children': ['D1', 'D2']},
            'B1': {'type': 'LEAF', 'value': 3},
            'B2': {'type': 'LEAF', 'value': 5},
            'C1': {'type': 'LEAF', 'value': 2},
            'D1': {'type': 'LEAF', 'value': 9},
            'D2': {'type': 'LEAF', 'value': 1},
        }
        
        self.evaluation_steps_original = []
        self.evaluation_steps_simplified = []
    
    def print_tree(self):
        """Gibt den Baum grafisch aus"""
        print("\n" + "="*60)
        print("BEISPIELBAUM")
        print("="*60)
        print("""
                    A (MAX)
                  / | \\
                 /  |  \\
                B   C   D (MIN)
               / \\  |  / \\
              3  5  2  9  1  (Blätter)
        """)
        print("="*60 + "\n")
    
    def minimax_original_tree(self, node, is_maximizing):
        """Original Minimax für Beispielbaum"""
        node_info = self.tree[node]
        
        if node_info['type'] == 'LEAF':
            value = node_info['value']
            self.evaluation_steps_original.append(f"Blatt {node}: Wert = {value}")
            return value
        
        if is_maximizing:
            max_val = -math.inf
            child_values = []
            for child in node_info['children']:
                val = self.minimax_original_tree(child, False)
                child_values.append(val)
                max_val = max(max_val, val)
            self.evaluation_steps_original.append(
                f"MAX-Knoten {node}: max({', '.join(map(str, child_values))}) = {max_val}"
            )
            return max_val
        else:
            min_val = math.inf
            child_values = []
            for child in node_info['children']:
                val = self.minimax_original_tree(child, True)
                child_values.append(val)
                min_val = min(min_val, val)
            self.evaluation_steps_original.append(
                f"MIN-Knoten {node}: min({', '.join(map(str, child_values))}) = {min_val}"
            )
            return min_val
    
    def minimax_simplified_tree(self, node, player_sign):
        """
        Vereinfachter Minimax für Beispielbaum
        player_sign: +1 für MAX, -1 für MIN
        """
        node_info = self.tree[node]
        
        if node_info['type'] == 'LEAF':
            value = node_info['value'] * player_sign
            self.evaluation_steps_simplified.append(
                f"Blatt {node}: {node_info['value']} * {player_sign:+d} = {value:+d}"
            )
            return value
        
        # Immer maximieren, aber mit negiertem Wert für den Gegner
        max_val = -math.inf
        child_values = []
        for child in node_info['children']:
            # Negiere Spieler-Vorzeichen für Kinder
            val = -self.minimax_simplified_tree(child, -player_sign)
            child_values.append(val)
            max_val = max(max_val, val)
        
        player_type = "MAX" if player_sign == 1 else "MIN"
        self.evaluation_steps_simplified.append(
            f"Knoten {node} ({player_type}, sign={player_sign:+d}): "
            f"max({', '.join(map(str, child_values))}) = {max_val}"
        )
        return max_val
    
    def compare(self):
        """Vergleicht beide Algorithmen am Beispielbaum"""
        self.print_tree()
        
        print("### ORIGINAL MINIMAX (explizite MIN/MAX-Funktionen) ###\n")
        self.evaluation_steps_original = []
        result_original = self.minimax_original_tree('A', True)
        
        print("Evaluierungsschritte:")
        for step in self.evaluation_steps_original:
            print(f"  {step}")
        print(f"\n→ Endergebnis: {result_original}\n")
        
        print("="*60)
        print("\n### VEREINFACHTER MINIMAX (Nullsummen-Eigenschaft) ###\n")
        self.evaluation_steps_simplified = []
        result_simplified = self.minimax_simplified_tree('A', +1)
        
        print("Evaluierungsschritte:")
        for step in self.evaluation_steps_simplified:
            print(f"  {step}")
        print(f"\n→ Endergebnis: {result_simplified}\n")
        
        print("="*60)
        print("\n### VERGLEICH ###\n")
        print(f"Original Minimax:      {result_original}")
        print(f"Vereinfachter Minimax: {result_simplified}")
        
        if result_original == result_simplified:
            print("\n✓ Beide Algorithmen liefern dasselbe Ergebnis!")
        else:
            print("\n✗ FEHLER: Unterschiedliche Ergebnisse!")
        
        print("\n" + "="*60)
        print("ERKLÄRUNG")
        print("="*60)
        print("""
Der vereinfachte Algorithmus nutzt die Nullsummen-Eigenschaft:
  Min-Value(s) = -Max-Value(s)

Statt separate MIN- und MAX-Funktionen zu haben, gibt es nur eine
Funktion, die immer maximiert. Der Trick: Das Ergebnis wird für den
Gegner negiert.

Vorteile:
  + Weniger Code (nur eine Funktion statt zwei)
  + Gleiche Funktionalität
  + Direktere Implementierung der Spieltheorie
  + Einfachere Erweiterung mit Alpha-Beta-Pruning

Die Knotenbewertungen erfolgen unterschiedlich, aber das Endergebnis
ist identisch!
        """)
        print("="*60 + "\n")


def main():
    """Hauptfunktion"""
    print("\n" + "="*70)
    print("VEREINFACHTER MINIMAX FÜR NULLSUMMENSPIELE")
    print("="*70)
    print("\nWähle einen Modus:")
    print("1 - Beispielbaum-Demonstration")
    print("2 - Tic Tac Toe Vergleich (leeres Spielfeld)")
    print("3 - Tic Tac Toe Vergleich (verschiedene Szenarien)")
    
    choice = input("\nDeine Wahl (1, 2 oder 3): ").strip()
    
    if choice == '1':
        # Beispielbaum demonstrieren
        tree_example = MiniMaxExampleTree()
        tree_example.compare()
    
    elif choice == '2':
        # Einzelner Tic Tac Toe Vergleich
        game = TicTacToeSimplified()
        game.compare_algorithms()
    
    elif choice == '3':
        # Mehrere Tic Tac Toe Szenarien
        print("\n### SZENARIO 1: Leeres Spielfeld ###")
        game1 = TicTacToeSimplified()
        game1.compare_algorithms()
        
        print("\n### SZENARIO 2: Nach einem Zug ###")
        game2 = TicTacToeSimplified()
        game2.board[1][1] = 'O'
        game2.compare_algorithms()
        
        print("\n### SZENARIO 3: Mittleres Spiel ###")
        game3 = TicTacToeSimplified()
        game3.board[0][0] = 'X'
        game3.board[1][1] = 'O'
        game3.board[0][2] = 'X'
        game3.board[2][0] = 'O'
        game3.compare_algorithms()
    
    else:
        print("Ungültige Wahl!")


if __name__ == "__main__":
    main()
