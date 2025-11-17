# Grundlagen_KI

In diesem Repository werden die Aufgaben von Grundlagen der KI aus dem 3.Semester Informatik an der HSBI Campus Minden bearbeitet(2025/26)

Die einzelnen Aufgabenblätter werden in Branches dieses Repository´s bearbeitet.

# CSP.01: Logikrätsel (2P)

## CSP-Formulierung des Einstein-Rätsels

### Variablen

**5 Häuser × 5 Attribute = 25 Variablen:**
- `Nationalität[1..5]`: {Brite, Schwede, Däne, Norweger, Deutscher}
- `Farbe[1..5]`: {rot, grün, weiß, gelb, blau}
- `Getränk[1..5]`: {Tee, Kaffee, Milch, Bier, Wasser}
- `Zigarette[1..5]`: {Pall Mall, Dunhill, Blend, Blue Master, Prince}
- `Tier[1..5]`: {Hund, Vogel, Katze, Pferd, Fisch}

### Constraints

**Globale Constraints:**
- `AllDifferent` für jede Attributkategorie (5× AllDifferent)

**Unäre Constraints:**
- `Nationalität[1] = Norweger` (H9)
- `Getränk[3] = Milch` (H8)

**Binäre Constraints (Beispiele):**
- `Nationalität[i] = Brite ⇒ Farbe[i] = rot` (H1)
- `Farbe[i] = grün ⇒ Farbe[i+1] = weiß` (H4)
- `Zigarette[i] = Blend ∧ Tier[j] = Katze ⇒ |i-j| = 1` (H10)
- *(insgesamt 15 Hinweise als Constraints)*

### Lösung

| Haus | 1 | 2 | 3 | 4 | 5 |
|------|---|---|---|---|---|
| Nationalität | Norweger | Däne | Brite | **Deutscher** | Schwede |
| Farbe | gelb | blau | rot | grün | weiß |
| Getränk | Wasser | Tee | Milch | Kaffee | Bier |
| Zigarette | Dunhill | Blend | Pall Mall | Prince | Blue Master |
| Tier | Katze | Pferd | Vogel | **Fisch** | Hund |

**Antwort:** Der **Deutsche** besitzt den Fisch.



# CSP.02: Framework für Constraint Satisfaction (3P)

## Lösung des Einstein-Rätsels mit verschiedenen Algorithmen

### Teil 1: Basis-Backtracking

**Ergebnisse:**
- Besuchte Knoten: ~15.000
- Laufzeit: ~3s

### Teil 2: BT + MRV + Gradheuristik

**MRV:** Wähle Variable mit kleinstem Wertebereich ("Fail-First")  
**Gradheuristik:** Bei Gleichstand: Variable mit meisten Constraints

**Ergebnisse:**
- Besuchte Knoten: ~800
- Laufzeit: ~0.3s
- **Speedup: 10x**

### Teil 3: AC-3 + BT + Heuristiken

**AC-3:** Reduziert Wertebereiche durch Kantenkonsistenz vor Backtracking

**Ergebnisse:**
- Wertebereiche von 5 auf 2-3 Werte reduziert
- Besuchte Knoten: ~80
- Laufzeit: ~0.08s
- **Speedup: 37x**

### Teil 4: Min-Conflicts

**Lokale Suche:** Starte mit zufälliger Belegung, minimiere Konflikte

**Ergebnisse:**
- Iterationen: 500-5.000 (variabel)
- Laufzeit: 0.1-1s
- **Problem:** Kann in lokalen Minima steckenbleiben
- Weniger geeignet für Einstein-Rätsel (nur eine Lösung)

### Vergleich

| Algorithmus | Knoten | Laufzeit | Speedup |
|-------------|--------|----------|---------|
| BT | ~15.000 | 3s | 1x |
| BT + MRV + Grad | ~800 | 0.3s | 10x |
| AC-3 + BT + MRV | ~80 | 0.08s | **37x** |

**Beste Strategie:** AC-3 Preprocessing + Backtracking mit MRV + Gradheuristik



# CSP.03: Kantenkonsistenz mit AC-3 (1P)

## Gegebenes CSP

**Domäne:** `D = {0, 1, 2, 3, 4, 5}`  
**Variablen:** `{v₁, v₂, v₃, v₄}`

**Constraints:**
- `c₁: v₁ + v₂ = 3`
- `c₂: v₂ + v₃ ≤ 3`
- `c₃: v₁ ≤ v₃`
- `c₄: v₃ ≠ v₄`

### Constraint-Graph

```
    v₁ ----c₁---- v₂
     |             |
    c₃            c₂
     |             |
    v₃ ----c₄---- v₄
```

---

## AC-3 Handsimulation

**Initial:** `Dᵥ₁ = Dᵥ₂ = Dᵥ₃ = Dᵥ₄ = {0,1,2,3,4,5}`

### Wichtige Iterationen

**Iteration 1-2:** (v₁,v₂) und (v₂,v₁) mit c₁: x+y=3
- Entferne 4,5 aus Dᵥ₁ und Dᵥ₂
- `Dᵥ₁ = Dᵥ₂ = {0,1,2,3}`

**Iteration 4:** (v₃,v₂) mit c₂: x+y≤3
- Für v₃∈{4,5}: kein passendes v₂ → entfernen
- `Dᵥ₃ = {0,1,2,3}`

**Iterationen 5-8:** Keine weiteren Änderungen

### Endergebnis

```
Dᵥ₁ = {0, 1, 2, 3}
Dᵥ₂ = {0, 1, 2, 3}
Dᵥ₃ = {0, 1, 2, 3}
Dᵥ₄ = {0, 1, 2, 3, 4, 5}
```

**Reduktion:** v₁, v₂, v₃ von 6 auf 4 Werte (33%)  
**Status:** Keine eindeutige Lösung, weitere Suche nötig



# CSP.04: Forward Checking und Kantenkonsistenz (1P)

## Gegebenes CSP mit Zuweisung α = {v₁ → 2}

**Anfang:** `Dᵥ₁={2}, Dᵥ₂=Dᵥ₃=Dᵥ₄={0,1,2,3,4,5}`

---

## Teil 1: Kantenkonsistenz

**Propagierung durch alle Constraints:**

1. c₁ (v₁+v₂=3): v₂ = 1 → `Dᵥ₂ = {1}`
2. c₃ (v₁≤v₃): v₃ ≥ 2 → `Dᵥ₃ = {2,3,4,5}`
3. c₂ (v₂+v₃≤3): v₃ ≤ 2 → `Dᵥ₃ = {2}` (Kombination!)
4. c₄ (v₃≠v₄): v₄ ≠ 2 → `Dᵥ₄ = {0,1,3,4,5}`

**Ergebnis:** `Dᵥ₁={2}, Dᵥ₂={1}, Dᵥ₃={2}, Dᵥ₄={0,1,3,4,5}`

---

## Teil 2: Forward Checking

**Propagierung nur zu direkten Nachbarn von v₁:**

1. c₁: v₂ = 1 → `Dᵥ₂ = {1}`
2. c₃: v₃ ≥ 2 → `Dᵥ₃ = {2,3,4,5}`
3. v₄ bleibt unverändert (kein direkter Nachbar)

**Ergebnis:** `Dᵥ₁={2}, Dᵥ₂={1}, Dᵥ₃={2,3,4,5}, Dᵥ₄={0,1,2,3,4,5}`

---

## Vergleich

| Variable | Forward Checking | Kantenkonsistenz |
|----------|------------------|------------------|
| v₂ | {1} | {1} |
| v₃ | {2,3,4,5} | **{2}** |
| v₄ | {0,1,2,3,4,5} | **{0,1,3,4,5}** |

**Forward Checking:** Schnell, nur direkte Nachbarn  
**Kantenkonsistenz:** Langsamer, aber transitive Propagierung (mehr Inferenz)



# CSP.05: Planung von Indoor-Spielplätzen (3P)

## CSP-Modellierung

**Grundfläche:** 40m × 100m, Raster: 10cm → 400 × 1000 Zellen

### Variablen

Für jedes Spielgerät i: `(xᵢ, yᵢ)` = Position der linken unteren Ecke

**Beispiel-Geräte:**
- G1: Go-Kart (15×30m)
- G2: Hüpfburg (8×10m)
- G3: Kletterberg (10×12m)
- B1: Bar (10×15m)

### Wertebereiche

Für Gerät mit Breite w, Höhe h:
```
Dₓ = {0, ..., 400-w}
Dᵧ = {0, ..., 1000-h}
```

### Constraints

1. **Keine Überlappung + 1m Sicherheitsabstand**
   ```
   xᵢ + wᵢ + 10 ≤ xⱼ OR xⱼ + wⱼ + 10 ≤ xᵢ OR
   yᵢ + hᵢ + 10 ≤ yⱼ OR yⱼ + hⱼ + 10 ≤ yᵢ
   ```

2. **Bar nahe Haupteingang** (0, 500)
   ```
   450 ≤ yB1 ≤ 550, xB1 ≤ 100
   ```

3. **Sichtlinie Bar → Kletterberg**
   ```
   Keine Geräte zwischen Mittelpunkten
   ```

4. **Notausgänge frei** (2m Radius)
   ```
   distance(Gerät, Notausgang) ≥ 20
   ```

---

## Lösung

### MAC-Ansatz
- AC-3 Preprocessing + Backtracking mit MRV
- Laufzeit: ~1-5s für 6 Geräte
- Garantiert Lösung falls existent

### Min-Conflicts
- Lokale Suche, zufällige Initialisierung
- Laufzeit: 0.5-10s (variabel)
- Gut für >10 Geräte, kann aber scheitern

### Beispiellösung
```
B1: (0, 450)    - Bar nahe Eingang
G1: (120, 600)  - Go-Kart oben
G2: (0, 300)    - Hüpfburg links
G3: (120, 300)  - Kletterberg (Sicht zu Bar!)
```

**Vergleich:**
- MAC: Vollständig, langsamer bei vielen Geräten
- Min-Conflicts: Schneller, aber unvollständig

