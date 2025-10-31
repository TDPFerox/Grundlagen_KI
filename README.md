# Grundlagen_KI

In diesem Repository werden die Aufgaben von Grundlagen der KI aus dem 3.Semester Informatik an der HSBI Campus Minden bearbeitet(2025/26)

Die einzelnen Aufgabenblätter werden in Branches dieses Repository´s bearbeitet.

# Games.01: Handsimulation: Minimax und alpha-beta-Pruning

## Aufgabe 1

- B = 3
- E = 9
- F = 2
- G = 6
- C = 2
- D = 1
- A = 3

## Aufgabe 2

Initial: bei A (MAX): α = −∞, β = +∞

1. Besuche B (MIN) (erbt α = −∞, β = +∞)

    - Leaf 8 → B.v = 8 (β_B = 8)

    - Leaf 7 → B.v = 7 (β_B = 7)

    - Leaf 3 → B.v = 3 (β_B = 3) → fertig: B = 3

2. Rückgabe nach A → α_A = max(−∞,3) = 3.

    - Besuche C (MIN) (erbt α = 3, β = +∞)

        - Besuche E (MAX) (erbt α = 3, β = +∞)

        - Leaf 9 → E.v = 9 (v_max = 9), α_local → 9

        - Leaf 1 → E.v bleibt 9

        - Leaf 6 → E.v bleibt 9
        → fertig: E = 9
        Rückgabe nach C → β_C = min(+∞,9) = 9 (aktuell: α_A=3, β_C=9)

    - Besuche F (MAX) (erbt α = 3, β = 9)

        - Leaf 2 → F.v = 2 (v_max = 2), α_local = max(3,2) = 3

        - Leaf 1 → F.v bleibt 2

        - Leaf 1 → F.v bleibt 2

            → fertig: F = 2

            Rückgabe nach C → β_C = min(9,2) = 2

            Nun: β_C = 2 ≤ α_A = 3 ⇒ CUT-OFF am MIN-Knoten C.

            => Die gesamte Kante C→G (und damit ganzes G-Teilbaum) wird nicht untersucht.

    C liefert C = 2 an A. Rückgabe: α_A = max(3,2) = 3 (bleibt 3).

3. Besuche D (MIN) (erbt α = 3, β = +∞)

    - Leaf 2 → D.v = 2 → sofort: D.v = 2 ≤ α_A = 3 ⇒ CUT-OFF
        
        => Die Kanten D→(zweiter Leaf 1) und D→(dritter Leaf 3) werden nicht untersucht.
        
        D liefert D = 2 an A.

Endergebnis (mit Pruning): A = 3 (gleich wie Minimax).

---

Explizit pruned Kanten (bei der gegebenen Reihenfolge L→R):

- Ganzes Teilbaum C→G (kein Blatt von G wurde ausgewertet).

- D → zweiter Blatt (1) und D → dritter Blatt (3) (nur das erste Leaf 2 wurde gelesen).

(Es gibt keine weiteren inneren Cut-offs in E oder F mit dieser Reihenfolge.)

Zur Veranschaulichung: die wichtigen α/β-Stände

- A start: α=−∞,β=+∞
- nach B: A.α = 3
- bei C Beginn: C.α=3, C.β=+∞
- nach E: C.β = 9
- bei F: F.α = 3, F.β = 9 → F.v = 2 → nach F: C.β = 2 ⇒ β_C(=2) ≤ α_A(=3) ⇒ prune G
- bei D: D.α = 3; nach erstem Leaf (2) gilt D.v=2 ≤ α => prune rest

## Aufgabe 3

Allgemeine Strategie:

- Bei einem MAX-Knoten: zuerst die Kinder untersuchen, die wahrscheinlich hohe Werte liefern (so wird α schnell groß → mehr Prunes).

- Bei einem MIN-Knoten: zuerst die Kinder untersuchen, die wahrscheinlich kleine Werte liefern (so wird β schnell klein → mehr Prunes).

Konkreter Vorschlag für größere Anzahl von Abschneidungen in diesem Baum:

- Unter C (MIN) ist das beste Ergebnis, F zuerst auszuwerten (weil F = 2 ist das kleinste der drei). Wenn man F als erstes besucht, erhält C.β = 2 sofort und weil A.α bereits 3 (von B), gilt β_C = 2 ≤ α_A = 3 → C schneidet dann sowohl E als auch G komplett ab. Das würde E (9) und G (6) gar nicht untersuchen → deutlich mehr Pruning als bei der ursprünglichen Reihenfolge (bei der nur G abgeschnitten wurde).

- Ebenso: bei D (MIN) wäre es optimal, falls möglich, das kleinste Blatt (Wert 1) zuerst zu prüfen – das würde ebenfalls sofort abschneiden.

Also: Ja — z. B. unter C: Reihenfolge F, G, E (oder F, E, G) ist besser als die gegebene (E,F,G). Mit dieser optimierten Reihenfolge werden deutlich mehr Zweige abgeschnitten.

# Optimale Spiele: Minimax und alpha-beta-Pruning

## Aufgabe 3 - Vergleich Minimax mit und ohne Alpha-Beta-Pruning

### SZENARIO 1: Leeres Spielfeld (Spielstart)

**Vergleich: Minimax vs. Alpha-Beta-Pruning**

Spielsituation:
```
   |   |  
-----------
   |   |  
-----------
   |   |  
```

| Algorithmus | Besuchte Knoten | Reduzierung |
|------------|-----------------|-------------|
| Minimax OHNE Pruning | 549.946 | - |
| Minimax MIT Pruning | 20.866 | 96.2% |
| **Effizienzgewinn** | **26.36x schneller** | |

---

### SZENARIO 2: Nach dem ersten Zug (Mitte belegt)

Spielsituation:
```
   |   |  
-----------
   | O |  
-----------
   |   |  
```

| Algorithmus | Besuchte Knoten | Reduzierung |
|------------|-----------------|-------------|
| Minimax OHNE Pruning | 40.721 | - |
| Minimax MIT Pruning | 2.184 | 94.6% |
| **Effizienzgewinn** | **18.65x schneller** | |

---

### SZENARIO 3: Mittleres Spiel (4 Züge)

Spielsituation:
```
 X |   | X
-----------
   | O |  
-----------
 O |   |  
```

| Algorithmus | Besuchte Knoten | Reduzierung |
|------------|-----------------|-------------|
| Minimax OHNE Pruning | 186 | - |
| Minimax MIT Pruning | 48 | 74.2% |
| **Effizienzgewinn** | **3.88x schneller** | |

---

### SZENARIO 4: Spätes Spiel (6 Züge)

Spielsituation:
```
 X | O | O
-----------
 O | X |  
-----------
   |   | X
```

| Algorithmus | Besuchte Knoten | Reduzierung |
|------------|-----------------|-------------|
| Minimax OHNE Pruning | 1 | - |
| Minimax MIT Pruning | 1 | 0.0% |
| **Effizienzgewinn** | **1.00x** | |

---

### SZENARIO 5: Kritische Situation (Block erforderlich)

Spielsituation:
```
 X | X |  
-----------
   | O |  
-----------
   |   |  
```

| Algorithmus | Besuchte Knoten | Reduzierung |
|------------|-----------------|-------------|
| Minimax OHNE Pruning | 935 | - |
| Minimax MIT Pruning | 75 | 92.0% |
| **Effizienzgewinn** | **12.47x schneller** | |

---

### ZUSAMMENFASSUNG

| Szenario | Ohne Pruning | Mit Pruning | Reduzierung |
|----------|--------------|-------------|-------------|
| Leeres Spielfeld | 549.946 | 20.866 | 96.2% |
| Nach 1 Zug | 40.721 | 2.184 | 94.6% |
| Mittleres Spiel | 186 | 48 | 74.2% |
| Spätes Spiel | 1 | 1 | 0.0% |
| Kritische Situation | 935 | 75 | 92.0% |
| **GESAMT** | **591.789** | **23.174** | **96.1%** |

**Durchschnittlicher Effizienzgewinn: 25.54x schneller**

#### Interpretation der Ergebnisse

- **Maximaler Effekt am Spielanfang**: Bei einem leeren Spielfeld werden 96.2% der Knoten eingespart
- **Abnehmender Effekt**: Je weniger Züge möglich sind, desto geringer der Pruning-Effekt
- **Extremfall**: Bei nur noch einem möglichen Zug (Szenario 4) gibt es keinen Unterschied
- **Gesamtbilanz**: Über alle Szenarien hinweg werden durchschnittlich 96.1% der Knoten eingespart

---

# Games.03: Minimax vereinfachen

## Theoretische Grundlage

In **Nullsummenspielen** gilt die wichtige Eigenschaft:
```
Min-Value(s) = -Max-Value(s)
```

Das bedeutet: Was für einen Spieler gut ist, ist für den anderen gleichermaßen schlecht.

## Vereinfachung des Algorithmus

Statt zwei separate Funktionen (`min-value` und `max-value`) zu haben, können wir eine einzige Funktion verwenden, die **immer maximiert**:

**Original Minimax:**
```python
def minimax(node, is_maximizing):
    if is_terminal(node):
        return evaluate(node)
    
    if is_maximizing:
        return max(minimax(child, False) for child in children(node))
    else:
        return min(minimax(child, True) for child in children(node))
```

**Vereinfachter Minimax:**
```python
def minimax_simplified(node, player_sign):
    if is_terminal(node):
        return evaluate(node) * player_sign
    
    # Immer maximieren, Ergebnis für Gegner negieren
    return max(-minimax_simplified(child, -player_sign) 
               for child in children(node))
```

## Beispielbaum zur Demonstration

```
                A (MAX)
              / | \
             /  |  \
            B   C   D (MIN)
           / \  |  / \
          3  5  2  9  1  (Blätter)
```

### Evaluierung mit Original Minimax

| Schritt | Knoten | Typ | Berechnung | Ergebnis |
|---------|--------|-----|------------|----------|
| 1 | B1 | Blatt | - | 3 |
| 2 | B2 | Blatt | - | 5 |
| 3 | B | MIN | min(3, 5) | 3 |
| 4 | C1 | Blatt | - | 2 |
| 5 | C | MIN | min(2) | 2 |
| 6 | D1 | Blatt | - | 9 |
| 7 | D2 | Blatt | - | 1 |
| 8 | D | MIN | min(9, 1) | 1 |
| 9 | A | MAX | max(3, 2, 1) | **3** |

### Evaluierung mit Vereinfachtem Minimax

| Schritt | Knoten | Sign | Berechnung | Ergebnis |
|---------|--------|------|------------|----------|
| 1 | B1 | +1 | 3 × (+1) | +3 |
| 2 | B2 | +1 | 5 × (+1) | +5 |
| 3 | B | -1 | max(-3, -5) | -3 → negiert: +3 |
| 4 | C1 | +1 | 2 × (+1) | +2 |
| 5 | C | -1 | max(-2) | -2 → negiert: +2 |
| 6 | D1 | +1 | 9 × (+1) | +9 |
| 7 | D2 | +1 | 1 × (+1) | +1 |
| 8 | D | -1 | max(-9, -1) | -1 → negiert: +1 |
| 9 | A | +1 | max(3, 2, 1) | **3** |

## Ergebnis

Beide Algorithmen liefern **dasselbe Endergebnis: 3**

## Vorteile der Vereinfachung

**Weniger Code**: Nur eine Funktion statt zwei (min-value/max-value)  
**Gleiche Funktionalität**: Identisches Ergebnis  
**Eleganter**: Direktere Implementierung der Spieltheorie  
**Einfachere Erweiterung**: Alpha-Beta-Pruning lässt sich leichter integrieren  
**Weniger Fehleranfällig**: Keine Verwechslung zwischen MIN und MAX  

# Games.04: Suchtiefe begrenzen

**Endzustand - X gewinnt**

```
 X | X | X
-----------
 O | O | 
-----------
   |   | 
```

- X hat 1 volle Linie (erste Reihe): X3=1
- Also: Utility = +1
(Endzustand, keine Eval-Funktion nötig)

**Endzustand - O gewinnt**

```
 X | X | O
-----------
 X | O |  
-----------
   | O |  
```

- O hat 1 volle Linie (zweite Spalte): O3=1
- Utility = −1

**Endzustand - Unentschieden**

```
 X | O | X
-----------
 X | X | O
-----------
 O | X | O
```

- Keine Linie mit 3 gleichen Symbolen → Utility = 0

**Zwischenstand 1 - Frühes Spiel**

```
 X |   |  
-----------
   | O |  
-----------
   |   |  
```

- Linien mit nur 1 X und keinem O:
    - Zeile 1, Spalte 1, Diagonale 1 → X1=3
- Linien mit nur 1 O und keinem X:
    - Zeile 2, Spalte 2, Diagonale 1, Diagonale 2 → O1=4
- X2=0,O2=0

Eval(s)=3⋅0+3−(3⋅0+4)=3−4=−1

O leicht im Vorteil

**Zwischenzustand 2 – X droht mit Sieg**

```
 X | X |  
-----------
 O |   |  
-----------
   | O |  
```
- Linien mit 2 X und keinem O:
    - Zeile 1 → X2=1
- Linien mit 1 X und keinem O (z. B. Diagonale 2): X1=1
- Linien mit 1 O und keinem X (Spalte 2, Diagonale 1): O1=2
- O2=0

Eval(s)=3⋅1+1−(3⋅0+2)=4−2=2

X deutlich im Vorteil

**Zwischenzustand 3 – O droht mit Sieg**

```
 X | X | O
-----------
   | O |  
-----------
   |   | X
```
- O2=1 (mittlere Spalte fast voll mit O)
- X2=0
- X1=2 (einige Linien mit einem X)
- O1=1

Eval(s)=3⋅0+2−(3⋅1+1)=2−4=−2

O deutlich im Vorteil

**Sinvoll weil:**

- Linear und effizient: Berechnet schnell eine Näherung des Gewinnpotenzials beider Spieler.
- Berücksichtigt drohende Gewinne: 2-in-a-row zählt dreifach → Linien kurz vor dem Sieg sind wichtiger.
- Symmetrisch: Vorteil für X ist Nachteil für O (gegenseitige Balance).
- Kontinuierlich: Gibt abgestufte Werte (nicht nur Gewinn/Verlust), ideal bei Suchtiefenbeschränkung.
- Domänenwissen: Spiegelt direkt die Spielstruktur von Tic-Tac-Toe wider (8 mögliche Gewinnlinien).

# Games.05: Minimax generalisiert

- P3-Knoten (von links nach rechts): (1,2,3), (6,1,2), (−1,5,2), (5,4,5)
- P2-Knoten (links, rechts): (1,2,3), (−1,5,2)
- Wurzel (Spieler 1): (1,2,3)

Die Rückwärtsinduktion liefert also als Endergebnis für die Wurzel das Tripel (1,2,3) — und alle inneren Knoten sind wie oben angegeben.