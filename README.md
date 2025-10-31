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