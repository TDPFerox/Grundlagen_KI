# Implementieren Sie den Minimax-Algorithmus (wie in der VL besprochen) am Beispiel Tic Tac Toe in einer Sprache Ihrer Wahl

import math
import copy

class TicTacToe:
    def __init__(self):
        # Spielfeld: 3x3 Matrix, leere Felder sind None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player = 'X'  # Menschlicher Spieler
        self.ai = 'O'      # KI-Spieler
    
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
    
    def minimax(self, depth, is_maximizing):
        """
        Minimax-Algorithmus
        depth: Aktuelle Tiefe im Spielbaum
        is_maximizing: True wenn KI (Maximierer) am Zug ist, False wenn Spieler (Minimierer)
        Rückgabe: Bester Score für die aktuelle Position
        """
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
                score = self.minimax(depth + 1, False)
                self.board[row][col] = None
                max_score = max(score, max_score)
            return max_score
        else:
            # Spieler ist am Zug - minimiere den Score
            min_score = math.inf
            for move in self.available_moves():
                row, col = move
                self.board[row][col] = self.player
                score = self.minimax(depth + 1, True)
                self.board[row][col] = None
                min_score = min(score, min_score)
            return min_score
    
    def find_best_move(self):
        """
        Findet den besten Zug für die KI mittels Minimax
        Rückgabe: (row, col) Tupel mit dem besten Zug
        """
        best_score = -math.inf
        best_move = None
        
        for move in self.available_moves():
            row, col = move
            self.board[row][col] = self.ai
            score = self.minimax(0, False)
            self.board[row][col] = None
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def play(self):
        """Hauptspielschleife"""
        print("=== Tic Tac Toe mit Minimax-KI ===")
        print(f"Du spielst als '{self.player}', die KI spielt als '{self.ai}'")
        print("Gib deine Züge als 'Zeile Spalte' ein (0-2, z.B. '1 1' für Mitte)")
        
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


def main():
    """Hauptfunktion zum Starten des Spiels"""
    game = TicTacToe()
    game.play()


if __name__ == "__main__":
    main()