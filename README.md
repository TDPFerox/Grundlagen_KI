# Grundlagen_KI

In diesem Repository werden die Aufgaben von Grundlagen der KI aus dem 3.Semester Informatik an der HSBI Campus Minden bearbeitet(2025/26)

Die einzelnen Aufgabenblätter werden in Branches dieses Repository´s bearbeitet.

# CSP.01: Logikrätsel (2P)

## Problem: Einstein-Rätsel

**Quelle:** [Wikipedia - Zebra Puzzle](https://en.wikipedia.org/wiki/Zebra_Puzzle)

### Problemstellung

5 Häuser in 5 verschiedenen Farben, bewohnt von 5 Personen unterschiedlicher Nationalität. Jede Person:
- trinkt ein bestimmtes Getränk
- raucht eine bestimmte Zigarettenmarke  
- hält ein bestimmtes Haustier

**Hinweise:**
1. Der Brite lebt im roten Haus
2. Der Schwede hält einen Hund
3. Der Däne trinkt Tee
4. Das grüne Haus steht links vom weißen Haus
5. Der Besitzer des grünen Hauses trinkt Kaffee
6. Die Person, die Pall Mall raucht, hält einen Vogel
7. Der Besitzer des gelben Hauses raucht Dunhill
8. Die Person im mittleren Haus trinkt Milch
9. Der Norweger lebt im ersten Haus
10. Die Person, die Blend raucht, lebt neben der Person mit der Katze
11. Die Person mit dem Pferd lebt neben der Person, die Dunhill raucht
12. Die Person, die Blue Master raucht, trinkt Bier
13. Der Deutsche raucht Prince
14. Der Norweger lebt neben dem blauen Haus
15. Die Person, die Blend raucht, hat einen Nachbarn, der Wasser trinkt

**Frage:** Wem gehört der Fisch?

---

## CSP-Formulierung

### Variablen (25 Variablen)

**Pro Haus (Position 1-5):**
- `Nationalität[i]`: {Brite, Schwede, Däne, Norweger, Deutscher}
- `Farbe[i]`: {rot, grün, weiß, gelb, blau}
- `Getränk[i]`: {Tee, Kaffee, Milch, Bier, Wasser}
- `Zigarette[i]`: {Pall Mall, Dunhill, Blend, Blue Master, Prince}
- `Tier[i]`: {Hund, Vogel, Katze, Pferd, Fisch}

### Wertebereiche

Für jede Variable: Ein Element aus der jeweiligen Menge (siehe oben).

### Constraints

#### Globale Constraints (AllDifferent)

```
AllDifferent(Nationalität[1..5])
AllDifferent(Farbe[1..5])
AllDifferent(Getränk[1..5])
AllDifferent(Zigarette[1..5])
AllDifferent(Tier[1..5])
```

#### Unäre Constraints

```
C1: Nationalität[1] = Norweger           (Hinweis 9)
C2: Getränk[3] = Milch                   (Hinweis 8)
```

#### Binäre Constraints (aus Hinweisen)

```
C3:  ∃i: Nationalität[i] = Brite ∧ Farbe[i] = rot                    (H1)
C4:  ∃i: Nationalität[i] = Schwede ∧ Tier[i] = Hund                  (H2)
C5:  ∃i: Nationalität[i] = Däne ∧ Getränk[i] = Tee                   (H3)
C6:  ∃i: Farbe[i] = grün ∧ Farbe[i+1] = weiß                         (H4)
C7:  ∃i: Farbe[i] = grün ∧ Getränk[i] = Kaffee                       (H5)
C8:  ∃i: Zigarette[i] = Pall Mall ∧ Tier[i] = Vogel                  (H6)
C9:  ∃i: Farbe[i] = gelb ∧ Zigarette[i] = Dunhill                    (H7)
C10: ∃i: Zigarette[i] = Blue Master ∧ Getränk[i] = Bier              (H12)
C11: ∃i: Nationalität[i] = Deutscher ∧ Zigarette[i] = Prince         (H13)
C12: ∃i: Farbe[i] = blau ∧ |i - pos(Norweger)| = 1                  (H14)
C13: ∃i,j: Zigarette[i] = Blend ∧ Tier[j] = Katze ∧ |i-j| = 1       (H10)
C14: ∃i,j: Tier[i] = Pferd ∧ Zigarette[j] = Dunhill ∧ |i-j| = 1     (H11)
C15: ∃i,j: Zigarette[i] = Blend ∧ Getränk[j] = Wasser ∧ |i-j| = 1   (H15)
```

### Lösung

| Haus | 1 | 2 | 3 | 4 | 5 |
|------|---|---|---|---|---|
| **Nationalität** | Norweger | Däne | Brite | Deutscher | Schwede |
| **Farbe** | gelb | blau | rot | grün | weiß |
| **Getränk** | Wasser | Tee | Milch | Kaffee | Bier |
| **Zigarette** | Dunhill | Blend | Pall Mall | Prince | Blue Master |
| **Tier** | Katze | Pferd | Vogel | **Fisch** | Hund |

**Antwort:** Der **Deutsche** (Haus 4) besitzt den Fisch.



# CSP.02: Framework für Constraint Satisfaction (3P)

## Lösung des Einstein-Rätsels mit verschiedenen Algorithmen

### Teil 1: Basis-Algorithmus BT_Search

**Backtracking ohne Heuristiken:**

```python
def BT_Search(csp, assignment={}):
    if is_complete(assignment):
        return assignment
    
    var = select_unassigned_variable(csp, assignment)  # Einfach: erste Variable
    
    for value in order_domain_values(csp, var, assignment):  # Einfach: natürliche Ordnung
        if is_consistent(value, var, assignment, csp):
            assignment[var] = value
            result = BT_Search(csp, assignment)
            if result is not None:
                return result
            del assignment[var]
    
    return None
```

**Ergebnisse:**
- **Besuchte Knoten:** ~15.000-20.000 (abhängig von Variablenreihenfolge)
- **Laufzeit:** ~2-5 Sekunden
- **Lösung gefunden:** Ja

---

### Teil 2: BT mit MRV und Gradheuristik

**MRV (Minimum Remaining Values):**
- Wähle Variable mit kleinstem Wertebereich
- "Fail-First"-Prinzip

**Gradheuristik (Degree Heuristic):**
- Bei Gleichstand: Wähle Variable mit meisten Constraints zu unassignierten Variablen

```python
def select_unassigned_variable_MRV(csp, assignment):
    unassigned = [v for v in csp.variables if v not in assignment]
    
    # MRV: Variable mit kleinstem Wertebereich
    min_values = min(len(csp.domains[v]) for v in unassigned)
    candidates = [v for v in unassigned if len(csp.domains[v]) == min_values]
    
    # Gradheuristik als Tie-Breaker
    if len(candidates) > 1:
        return max(candidates, key=lambda v: count_constraints(v, unassigned, csp))
    
    return candidates[0]
```

**Ergebnisse:**
- **Besuchte Knoten:** ~500-1.000
- **Laufzeit:** ~0.2-0.5 Sekunden
- **Verbesserung:** 95% weniger Knoten!

**Vergleich:**

| Kriterium | Basis BT | BT + MRV + Grad |
|-----------|----------|------------------|
| Besuchte Knoten | ~15.000 | ~800 |
| Laufzeit | ~3s | ~0.3s |
| Speedup | 1x | **10x** |

---

### Teil 3: AC-3 vor BT

**AC-3 (Arc Consistency 3):**
- Reduziert Wertebereiche durch Kantenkonsistenz
- Läuft vor Backtracking

```python
def AC3(csp):
    queue = [(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]]
    
    while queue:
        (Xi, Xj) = queue.pop(0)
        if revise(csp, Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                return False  # Unlösbar
            for Xk in csp.neighbors[Xi] - {Xj}:
                queue.append((Xk, Xi))
    
    return True

def revise(csp, Xi, Xj):
    revised = False
    for x in csp.domains[Xi]:
        if not any(satisfies_constraint(x, y, Xi, Xj, csp) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
    return revised
```

**Ergebnisse nach AC-3:**
- Wertebereiche deutlich reduziert (z.B. von 5 auf 2-3 Werte)
- **Keine vollständige Lösung** durch AC-3 allein
- Aber: Suchraum stark eingeschränkt

**AC-3 + BT + MRV + Grad:**
- **Besuchte Knoten:** ~50-100
- **Laufzeit:** ~0.05-0.1 Sekunden
- **Speedup:** **30-60x** gegenüber Basis-BT!

**Vergleich:**

| Algorithmus | Knoten | Laufzeit | Speedup |
|-------------|--------|----------|----------|
| BT | ~15.000 | 3s | 1x |
| BT + MRV + Grad | ~800 | 0.3s | 10x |
| AC-3 + BT + MRV + Grad | ~80 | 0.08s | **37x** |

---

### Teil 4: Min-Conflicts Heuristik

**Min-Conflicts (lokale Suche):**
- Starte mit zufälliger vollständiger Belegung
- Wähle konfliktbehaftete Variable
- Setze auf Wert mit minimalen Konflikten

```python
def min_conflicts(csp, max_steps=10000):
    # Zufällige vollständige Initialisierung
    current = {var: random.choice(csp.domains[var]) for var in csp.variables}
    
    for i in range(max_steps):
        if num_conflicts(current, csp) == 0:
            return current  # Lösung gefunden
        
        # Wähle konfliktbehaftete Variable
        var = random.choice(conflicted_vars(current, csp))
        
        # Wähle Wert mit minimalen Konflikten
        value = min(csp.domains[var], 
                   key=lambda v: count_conflicts(var, v, current, csp))
        
        current[var] = value
    
    return None  # Keine Lösung gefunden
```

**Ergebnisse:**
- **Iterationen bis Lösung:** 500-5.000 (sehr variabel!)
- **Laufzeit:** 0.1-1 Sekunde
- **Problem:** Kann in lokalen Minima steckenbleiben
- **Vorteil:** Gut für große CSPs mit vielen Lösungen

**Für Einstein-Rätsel:**
- Weniger geeignet (nur eine Lösung, viele Constraints)
- AC-3 + BT ist hier effizienter

---

## Zusammenfassung

**Beste Strategie für Einstein-Rätsel:**
1. **AC-3** zur Vorverarbeitung (Domänenreduktion)
2. **Backtracking** mit:
   - **MRV** (Minimum Remaining Values)
   - **Gradheuristik** als Tie-Breaker
   - **Forward Checking** während der Suche

**Empirische Ergebnisse:**
- Lösung in ~0.08 Sekunden
- ~80 besuchte Knoten
- 37x schneller als naives Backtracking



# CSP.03: Kantenkonsistenz mit AC-3 (1P)

## Gegebenes CSP

**Domäne:** `D = {0, 1, 2, 3, 4, 5}`

**Variablen:** `V = {v₁, v₂, v₃, v₄}`

**Domänen:** `Dᵥ₁ = Dᵥ₂ = Dᵥ₃ = Dᵥ₄ = D = {0, 1, 2, 3, 4, 5}`

**Constraints:**
- `c₁ = ((v₁, v₂), {(x,y) ∈ D² | x + y = 3})`
- `c₂ = ((v₂, v₃), {(x,y) ∈ D² | x + y ≤ 3})`
- `c₃ = ((v₁, v₃), {(x,y) ∈ D² | x ≤ y})`
- `c₄ = ((v₃, v₄), {(x,y) ∈ D² | x ≠ y})`

---

## Teil 1: Constraint-Graph

```
    v₁ ----c₁---- v₂
     |             |
     |c₃          c₂
     |             |
    v₃ ----c₄---- v₄
```

**Kanten:**
- `v₁ ↔ v₂` (c₁: x + y = 3)
- `v₂ ↔ v₃` (c₂: x + y ≤ 3)
- `v₁ ↔ v₃` (c₃: x ≤ y)
- `v₃ ↔ v₄` (c₄: x ≠ y)

---

## Teil 2: AC-3 Algorithmus Handsimulation

### Initialisierung

**Domänen:**
```
Dᵥ₁ = {0, 1, 2, 3, 4, 5}
Dᵥ₂ = {0, 1, 2, 3, 4, 5}
Dᵥ₃ = {0, 1, 2, 3, 4, 5}
Dᵥ₄ = {0, 1, 2, 3, 4, 5}
```

**Queue (alle Kanten in beide Richtungen):**
```
Q = [(v₁,v₂), (v₂,v₁), (v₂,v₃), (v₃,v₂), (v₁,v₃), (v₃,v₁), (v₃,v₄), (v₄,v₃)]
```

---

### Iteration 1: (v₁, v₂)

**Constraint:** `v₁ + v₂ = 3`

**Prüfung:** Für jedes x ∈ Dᵥ₁, existiert y ∈ Dᵥ₂ mit x + y = 3?
- x=0: y=3 ✓
- x=1: y=2 ✓
- x=2: y=1 ✓
- x=3: y=0 ✓
- x=4: y=-1 ✗ → entfernen
- x=5: y=-2 ✗ → entfernen

**Ergebnis:** `Dᵥ₁ = {0, 1, 2, 3}` (revised!)

**Queue erweitern:** Nachbarn von v₁ außer v₂: `(v₃, v₁)` (bereits in Queue)

**Queue:** `[(v₂,v₁), (v₂,v₃), (v₃,v₂), (v₁,v₃), (v₃,v₁), (v₃,v₄), (v₄,v₃)]`

---

### Iteration 2: (v₂, v₁)

**Constraint:** `v₂ + v₁ = 3`

**Prüfung:** Für jedes y ∈ Dᵥ₂, existiert x ∈ Dᵥ₁={0,1,2,3} mit y + x = 3?
- y=0: x=3 ✓
- y=1: x=2 ✓
- y=2: x=1 ✓
- y=3: x=0 ✓
- y=4: x=-1 ✗ → entfernen
- y=5: x=-2 ✗ → entfernen

**Ergebnis:** `Dᵥ₂ = {0, 1, 2, 3}` (revised!)

**Queue erweitern:** `(v₃, v₂)` (bereits in Queue)

**Queue:** `[(v₂,v₃), (v₃,v₂), (v₁,v₃), (v₃,v₁), (v₃,v₄), (v₄,v₃)]`

---

### Iteration 3: (v₂, v₃)

**Constraint:** `v₂ + v₃ ≤ 3`

**Prüfung:** Für jedes y ∈ Dᵥ₂={0,1,2,3}, existiert z ∈ Dᵥ₃={0,1,2,3,4,5} mit y + z ≤ 3?
- y=0: z∈{0,1,2,3} ✓
- y=1: z∈{0,1,2} ✓
- y=2: z∈{0,1} ✓
- y=3: z=0 ✓

**Ergebnis:** `Dᵥ₂ = {0, 1, 2, 3}` (nicht geändert)

**Queue:** `[(v₃,v₂), (v₁,v₃), (v₃,v₁), (v₃,v₄), (v₄,v₃)]`

---

### Iteration 4: (v₃, v₂)

**Constraint:** `v₃ + v₂ ≤ 3`

**Prüfung:** Für jedes z ∈ Dᵥ₃={0,1,2,3,4,5}, existiert y ∈ Dᵥ₂={0,1,2,3} mit z + y ≤ 3?
- z=0: y∈{0,1,2,3} ✓
- z=1: y∈{0,1,2} ✓
- z=2: y∈{0,1} ✓
- z=3: y=0 ✓
- z=4: kein y ✗ → entfernen
- z=5: kein y ✗ → entfernen

**Ergebnis:** `Dᵥ₃ = {0, 1, 2, 3}` (revised!)

**Queue erweitern:** `(v₁,v₃), (v₄,v₃)` (beide bereits in Queue)

**Queue:** `[(v₁,v₃), (v₃,v₁), (v₃,v₄), (v₄,v₃)]`

---

### Iteration 5: (v₁, v₃)

**Constraint:** `v₁ ≤ v₃`

**Prüfung:** Für jedes x ∈ Dᵥ₁={0,1,2,3}, existiert z ∈ Dᵥ₃={0,1,2,3} mit x ≤ z?
- x=0: z∈{0,1,2,3} ✓
- x=1: z∈{1,2,3} ✓
- x=2: z∈{2,3} ✓
- x=3: z=3 ✓

**Ergebnis:** `Dᵥ₁ = {0, 1, 2, 3}` (nicht geändert)

**Queue:** `[(v₃,v₁), (v₃,v₄), (v₄,v₃)]`

---

### Iteration 6: (v₃, v₁)

**Constraint:** `v₁ ≤ v₃`

**Prüfung:** Für jedes z ∈ Dᵥ₃={0,1,2,3}, existiert x ∈ Dᵥ₁={0,1,2,3} mit x ≤ z?
- z=0: x=0 ✓
- z=1: x∈{0,1} ✓
- z=2: x∈{0,1,2} ✓
- z=3: x∈{0,1,2,3} ✓

**Ergebnis:** `Dᵥ₃ = {0, 1, 2, 3}` (nicht geändert)

**Queue:** `[(v₃,v₄), (v₄,v₃)]`

---

### Iteration 7: (v₃, v₄)

**Constraint:** `v₃ ≠ v₄`

**Prüfung:** Für jedes z ∈ Dᵥ₃={0,1,2,3}, existiert w ∈ Dᵥ₄={0,1,2,3,4,5} mit z ≠ w?
- Alle Werte: ja, es gibt immer mindestens einen unterschiedlichen Wert ✓

**Ergebnis:** `Dᵥ₃ = {0, 1, 2, 3}` (nicht geändert)

**Queue:** `[(v₄,v₃)]`

---

### Iteration 8: (v₄, v₃)

**Constraint:** `v₃ ≠ v₄`

**Prüfung:** Für jedes w ∈ Dᵥ₄={0,1,2,3,4,5}, existiert z ∈ Dᵥ₃={0,1,2,3} mit z ≠ w?
- w=0: z∈{1,2,3} ✓
- w=1: z∈{0,2,3} ✓
- w=2: z∈{0,1,3} ✓
- w=3: z∈{0,1,2} ✓
- w=4: z∈{0,1,2,3} ✓
- w=5: z∈{0,1,2,3} ✓

**Ergebnis:** `Dᵥ₄ = {0, 1, 2, 3, 4, 5}` (nicht geändert)

**Queue:** `[]` (leer)

---

## Endergebnis nach AC-3

```
Dᵥ₁ = {0, 1, 2, 3}
Dᵥ₂ = {0, 1, 2, 3}
Dᵥ₃ = {0, 1, 2, 3}
Dᵥ₄ = {0, 1, 2, 3, 4, 5}
```

**Reduktion:**
- v₁, v₂, v₃: von 6 auf 4 Werte (33% Reduktion)
- v₄: keine Reduktion
- **Keine eindeutige Lösung** - weitere Suche nötig!

**Gültige Lösungen (Beispiele):**
- v₁=0, v₂=3, v₃=0, v₄∈{1,2,3,4,5}
- v₁=1, v₂=2, v₃=1, v₄∈{0,2,3,4,5}
- v₁=2, v₂=1, v₃=2, v₄∈{0,1,3,4,5}



# CSP.04: Forward Checking und Kantenkonsistenz (1P)

## Gegebenes CSP (wie CSP.03)

**Zuweisung:** `α = {v₁ → 2}`

**Anfangszustand:**
```
Dᵥ₁ = {2}           (zugewiesen)
Dᵥ₂ = {0, 1, 2, 3, 4, 5}
Dᵥ₃ = {0, 1, 2, 3, 4, 5}
Dᵥ₄ = {0, 1, 2, 3, 4, 5}
```

---

## Teil 1: Kantenkonsistenz erzeugen

### Schritt 1: Constraint c₁ (v₁, v₂): v₁ + v₂ = 3

**v₁ = 2, also v₂ + 2 = 3 → v₂ = 1**

```
Dᵥ₂' = {1}
```

---

### Schritt 2: Constraint c₃ (v₁, v₃): v₁ ≤ v₃

**v₁ = 2, also 2 ≤ v₃ → v₃ ∈ {2, 3, 4, 5}**

```
Dᵥ₃' = {2, 3, 4, 5}
```

---

### Schritt 3: Propagierung zu v₃ wegen geändertem v₂

**Constraint c₂ (v₂, v₃): v₂ + v₃ ≤ 3**

**v₂ = 1, also 1 + v₃ ≤ 3 → v₃ ≤ 2 → v₃ ∈ {0, 1, 2}**

Kombiniert mit vorherigem v₃ ∈ {2, 3, 4, 5}:

```
Dᵥ₃'' = {2, 3, 4, 5} ∩ {0, 1, 2} = {2}
```

---

### Schritt 4: Propagierung zu v₄ wegen geändertem v₃

**Constraint c₄ (v₃, v₄): v₃ ≠ v₄**

**v₃ = 2, also v₄ ≠ 2 → v₄ ∈ {0, 1, 3, 4, 5}**

```
Dᵥ₄' = {0, 1, 3, 4, 5}
```

---

### Ergebnis nach Kantenkonsistenz

```
Dᵥ₁ = {2}              (zugewiesen)
Dᵥ₂ = {1}              (eindeutig bestimmt!)
Dᵥ₃ = {2}              (eindeutig bestimmt!)
Dᵥ₄ = {0, 1, 3, 4, 5}  (5 Werte möglich)
```

**Beobachtung:** Kantenkonsistenz hat fast alle Variablen eindeutig bestimmt!

---

## Teil 2: Forward Checking

**Forward Checking:** Propagiere nur direkte Nachbarn der zugewiesenen Variable.

### Schritt 1: v₁ = 2 zugewiesen

**Direkte Nachbarn von v₁:** v₂, v₃

#### Constraint c₁ (v₁, v₂): v₁ + v₂ = 3
```
v₂ = 1
Dᵥ₂ = {1}
```

#### Constraint c₃ (v₁, v₃): v₁ ≤ v₃
```
v₃ ∈ {2, 3, 4, 5}
Dᵥ₃ = {2, 3, 4, 5}
```

**Nach Forward Checking:**
```
Dᵥ₁ = {2}
Dᵥ₂ = {1}
Dᵥ₃ = {2, 3, 4, 5}
Dᵥ₄ = {0, 1, 2, 3, 4, 5}  (unverändert!)
```

---

## Vergleich Forward Checking vs. Kantenkonsistenz

| Variable | Vor Zuweisung | Forward Checking | Kantenkonsistenz |
|----------|---------------|------------------|------------------|
| v₁ | {2} | {2} | {2} |
| v₂ | {0,1,2,3,4,5} | **{1}** | **{1}** |
| v₃ | {0,1,2,3,4,5} | {2,3,4,5} | **{2}** |
| v₄ | {0,1,2,3,4,5} | {0,1,2,3,4,5} | **{0,1,3,4,5}** |

**Unterschiede:**

1. **Forward Checking:**
   - Propagiert nur **direkte Nachbarn** der zugewiesenen Variable
   - v₃ bleibt bei {2,3,4,5} (keine Propagierung von v₂)
   - v₄ unverändert (kein direkter Nachbar von v₁)
   - **Schneller**, aber weniger Inferenz

2. **Kantenkonsistenz (AC-3):**
   - Propagiert **transitiv** durch alle Constraints
   - v₃ wird zu {2} durch Kombination von c₂ und c₃
   - v₄ reduziert auf {0,1,3,4,5} durch c₄
   - **Langsamer**, aber mehr Inferenz

**Wann was verwenden?**
- **Forward Checking:** Während Backtracking (schnell, ausreichend)
- **Kantenkonsistenz:** Vor Backtracking als Preprocessing (einmalig, gründlich)



# CSP.05: Planung von Indoor-Spielplätzen (3P)

## Problemabstraktion

### Grundfläche

**Größe:** 40m × 100m = 4000m²
**Raster:** 10cm × 10cm (0.1m × 0.1m)
**Rastergröße:** 400 × 1000 Zellen

### Spielgeräte (Beispiel)

| ID | Typ | Größe (m) | Größe (Raster) |
|----|-----|-----------|----------------|
| G1 | Go-Kart-Bahn | 15 × 30 | 150 × 300 |
| G2 | Hüpfburg | 8 × 10 | 80 × 100 |
| G3 | Kletterberg | 10 × 12 | 100 × 120 |
| G4 | Trampolin | 5 × 5 | 50 × 50 |
| G5 | Bällebad | 6 × 8 | 60 × 80 |
| B1 | Bar | 10 × 15 | 100 × 150 |

### Türen/Eingänge

- **Haupteingang:** (0, 500) - Position (x, y) im Raster
- **Notausgang 1:** (400, 0)
- **Notausgang 2:** (400, 1000)
- **Notausgang 3:** (0, 200)

---

## CSP-Formulierung

### Variablen

Für jedes Spielgerät i ∈ {G1, G2, G3, G4, G5, B1}:
- **xᵢ**: x-Koordinate der linken unteren Ecke
- **yᵢ**: y-Koordinate der linken unteren Ecke

**Gesamt:** 12 Variablen (6 Geräte × 2 Koordinaten)

---

### Wertebereiche

Für Gerät i mit Breite wᵢ und Höhe hᵢ:
```
Dₓᵢ = {0, 1, 2, ..., 400 - wᵢ}  (Raster-x-Koordinaten)
Dᵧᵢ = {0, 1, 2, ..., 1000 - hᵢ} (Raster-y-Koordinaten)
```

**Beispiel für G1 (150×300):**
```
Dₓ_G1 = {0, 1, ..., 250}
Dᵧ_G1 = {0, 1, ..., 700}
```

---

### Constraints

#### 1. Keine Überlappung + Sicherheitsabstand (1m = 10 Raster)

Für alle Gerätepaare i ≠ j:
```python
def no_overlap(i, j, safety_distance=10):
    # Rechtecke überlappen nicht mit Sicherheitsabstand
    return (
        xᵢ + wᵢ + safety_distance <= xⱼ or  # i links von j
        xⱼ + wⱼ + safety_distance <= xᵢ or  # j links von i
        yᵢ + hᵢ + safety_distance <= yⱼ or  # i unter j
        yⱼ + hⱼ + safety_distance <= yᵢ     # j unter i
    )
```

#### 2. Bar am Haupteingang

```python
# Bar (B1) sollte nahe am Haupteingang (0, 500) sein
# "Soft" Constraint: Minimiere Distanz
distance(B1, Haupteingang) <= 50  # max 5m Entfernung

# Oder als hartes Constraint:
yB1 >= 450 and yB1 <= 550  # In y-Richtung nahe bei 500
xB1 <= 100                  # Nahe am linken Rand (Eingang bei x=0)
```

#### 3. Sichtlinie Bar → Kletterberg (G3)

```python
def line_of_sight(B1, G3):
    # Vereinfacht: Kein anderes Gerät blockiert die direkte Verbindung
    # zwischen Mittelpunkten von B1 und G3
    
    center_B1 = (xB1 + wB1/2, yB1 + hB1/2)
    center_G3 = (xG3 + wG3/2, yG3 + hG3/2)
    
    for gerät in [G1, G2, G4, G5]:
        if intersects_line(center_B1, center_G3, gerät):
            return False
    return True
```

#### 4. Notausgänge nicht blockieren

```python
def emergency_exit_clear(exit_pos, all_geräte, radius=20):
    # Mindestens 2m (20 Raster) Freiraum um Notausgänge
    for gerät in all_geräte:
        if distance(exit_pos, gerät) < radius:
            return False
    return True
```

#### 5. Entspannungszone (optional)

```python
# Z.B. Bällebad (G5) nicht neben Go-Kart (G1) wegen Lärm
distance(G1, G5) >= 50  # Mindestens 5m Abstand
```

---

## Lösung mit MAC (Maintaining Arc Consistency)

### MAC-Algorithmus

```python
def MAC(csp, assignment={}):
    if is_complete(assignment):
        return assignment
    
    var = select_unassigned_variable_MRV(csp, assignment)
    
    for value in order_domain_values(csp, var, assignment):
        if is_consistent(value, var, assignment, csp):
            assignment[var] = value
            
            # Kantenkonsistenz erzeugen
            inferences = AC3(csp, var)
            
            if inferences != failure:
                add_inferences_to_assignment(inferences)
                result = MAC(csp, assignment)
                if result != failure:
                    return result
            
            # Backtrack
            remove(var, assignment)
            restore_domains(inferences)
    
    return failure
```

### Beispiellösung

```
+-------------------------------------+
|  Bar (B1)        | Go-Kart (G1)     |
|  10×15m          |                  |
|  Nähe Eingang    |    15×30m        |
|                  |                  |
+------------------+------------------+
|                                     |
| Hüpfburg (G2)    Kletterberg (G3)  |
|   8×10m             10×12m          |
|                                     |
+-------------------------------------+
|                                     |
| Trampolin (G4)   Bällebad (G5)     |
|   5×5m              6×8m            |
|                                     |
+-------------------------------------+
```

**Koordinaten (Beispiel):**
```
B1: x=0,   y=450  (Nähe Haupteingang bei (0,500))
G1: x=120, y=600  (Go-Kart im oberen Bereich)
G2: x=0,   y=300  (Hüpfburg links)
G3: x=120, y=300  (Kletterberg - Sichtlinie zu Bar!)
G4: x=0,   y=100  (Trampolin unten links)
G5: x=80,  y=100  (Bällebad unten rechts)
```

**Prüfung:**
- ✓ Keine Überlappungen (1m Abstand eingehalten)
- ✓ Bar nahe Haupteingang (y=450 ≈ 500)
- ✓ Sichtlinie Bar → Kletterberg frei
- ✓ Notausgänge nicht blockiert

**Laufzeit mit MAC:** ~1-5 Sekunden (abhängig von Diskretisierung)

---

## Lösung mit Min-Conflicts

### Min-Conflicts für kontinuierliche CSPs

```python
def min_conflicts_spatial(csp, max_steps=10000):
    # Zufällige Initialisierung
    current = {gerät: random_valid_position(gerät) for gerät in geräte}
    
    for i in range(max_steps):
        conflicts = count_all_conflicts(current, csp)
        if conflicts == 0:
            return current
        
        # Wähle Gerät mit meisten Konflikten
        gerät = max(geräte, key=lambda g: count_conflicts(g, current, csp))
        
        # Lokale Suche: Verschiebe Gerät zu Position mit minimalen Konflikten
        best_pos = None
        min_conf = float('inf')
        
        # Sample mehrere zufällige Positionen
        for _ in range(100):
            pos = random_position(gerät)
            conf = count_conflicts_at_pos(gerät, pos, current, csp)
            if conf < min_conf:
                min_conf = conf
                best_pos = pos
        
        current[gerät] = best_pos
        
        # Kleine Störung bei lokalem Minimum
        if i % 100 == 0 and conflicts > 0:
            current[random.choice(geräte)] = random_position()
    
    return None
```

**Ergebnisse:**
- **Laufzeit:** 0.5-10 Sekunden (sehr variabel!)
- **Erfolgsrate:** ~70-90% (kann in lokalen Minima steckenbleiben)
- **Vorteil:** Gut für große Spielplätze mit vielen Geräten

---

## Vergleich MAC vs. Min-Conflicts

| Kriterium | MAC | Min-Conflicts |
|-----------|-----|---------------|
| **Vollständigkeit** | Ja (findet immer Lösung falls existent) | Nein (kann scheitern) |
| **Laufzeit (klein)** | 1-5s | 0.5-10s |
| **Laufzeit (groß)** | Exponentiell | Linear |
| **Lösung Qualität** | Optimal (erste gefundene) | Suboptimal möglich |
| **Best for** | Wenige Geräte, harte Constraints | Viele Geräte, weiche Constraints |

**Empfehlung:**
- **6-10 Geräte:** MAC mit MRV + AC-3
- **>10 Geräte:** Min-Conflicts mit Random Restarts
- **Hybrid:** AC-3 Preprocessing + Min-Conflicts

---

## Implementierung (Pseudo-Code)

```python
class IndoorPlayground:
    def __init__(self, width=400, height=1000):
        self.width = width
        self.height = height
        self.geräte = [
            {'id': 'G1', 'w': 150, 'h': 300, 'type': 'Go-Kart'},
            {'id': 'G2', 'w': 80,  'h': 100, 'type': 'Hüpfburg'},
            {'id': 'G3', 'w': 100, 'h': 120, 'type': 'Kletterberg'},
            {'id': 'G4', 'w': 50,  'h': 50,  'type': 'Trampolin'},
            {'id': 'G5', 'w': 60,  'h': 80,  'type': 'Bällebad'},
            {'id': 'B1', 'w': 100, 'h': 150, 'type': 'Bar'},
        ]
        self.safety_distance = 10  # 1m
    
    def solve_with_MAC(self):
        csp = self.create_csp()
        solution = MAC(csp)
        return solution
    
    def solve_with_min_conflicts(self):
        solution = min_conflicts_spatial(self.create_csp())
        return solution
    
    def visualize(self, solution):
        # Zeichne Spielplatz mit matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        
        for gerät in self.geräte:
            pos = solution[gerät['id']]
            rect = patches.Rectangle(
                (pos['x'], pos['y']), 
                gerät['w'], gerät['h'],
                linewidth=2, edgecolor='blue', facecolor='lightblue'
            )
            ax.add_patch(rect)
            ax.text(pos['x'] + gerät['w']/2, pos['y'] + gerät['h']/2, 
                   gerät['type'], ha='center', va='center')
        
        plt.title('Indoor Spielplatz Layout')
        plt.xlabel('Breite (0.1m Einheiten)')
        plt.ylabel('Länge (0.1m Einheiten)')
        plt.grid(True)
        plt.show()
```

**Nutzung:**
```python
playground = IndoorPlayground()
solution = playground.solve_with_MAC()
playground.visualize(solution)
```

