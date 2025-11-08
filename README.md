# Grundlagen_KI

In diesem Repository werden die Aufgaben von Grundlagen der KI aus dem 3.Semester Informatik an der HSBI Campus Minden bearbeitet(2025/26)

Die einzelnen Aufgabenblätter werden in Branches dieses Repository´s bearbeitet.

# Blatt 4

## DTL.01: Entscheidungsbäume mit CAL3 und ID3

### Trainingsmenge

| Nr. | Alter | Einkommen | Bildung  | Kandidat |
|-----|-------|-----------|----------|----------|
| 1   | ≥35   | hoch      | Abitur   | O        |
| 2   | <35   | niedrig   | Master   | O        |
| 3   | ≥35   | hoch      | Bachelor | M        |
| 4   | ≥35   | niedrig   | Abitur   | M        |
| 5   | ≥35   | hoch      | Master   | O        |
| 6   | <35   | hoch      | Bachelor | O        |
| 7   | <35   | niedrig   | Abitur   | M        |

---

### 1. CAL3-Baum (S1=4, S2=0.7)

**Wurzelknoten:** Reinheit = 4/7 = 0.571

**Attribut-Reinheiten:**
- Alter: 0.571
- Einkommen: **0.714** ← gewählt
- Bildung: 0.714

**Resultierender Baum:**

```
Einkommen
├── hoch (n=4, Reinheit=0.75)
│   └── O  [Stopp: Reinheit 0.75 ≥ S2=0.7]
│
└── niedrig (n=3, Reinheit=0.67)
    └── M  [Stopp: 3 Beispiele < S1=4]
```

**Genauigkeit:** 5/7 = 71.4%

---

### 2. ID3-Baum

**Gesamtentropie:** H(S) = 0.9852

**Information Gain:**
- Alter: 0.0202
- Einkommen: 0.1281
- Bildung: **0.3060** ← höchster IG, gewählt

**Resultierender Baum:**

```
Bildung
├── Master
│   └── O  [rein: 2×O]
│
├── Bachelor
│   └── Alter
│       ├── ≥35 → M  [Beispiel 3]
│       └── <35 → O  [Beispiel 6]
│
└── Abitur
    └── Einkommen
        ├── hoch → O  [Beispiel 1]
        └── niedrig → M  [Beispiele 4, 7]
```

**Genauigkeit:** 7/7 = 100%

---

### Vergleich

| Kriterium | CAL3 | ID3 |
|-----------|------|-----|
| Wurzelattribut | Einkommen | Bildung |
| Baumtiefe | 1 | 3 |
| Blätter | 2 | 5 |
| Genauigkeit | 71.4% | 100% |

---

## DTL.02: Pruning

### Aufgabe: Vereinfachung des Entscheidungsbaums

**Gegeben:** `x₃(x₂(x₁(C, A), x₁(B, A)), x₁(x₂(C, B), A))`

**Ziel:** Schrittweise Vereinfachung mit Pruning- und Transformationsregeln

---

### Verwendete Regeln

**Pruning-Regeln:**
- **P1:** `xᵢ(C, C) → C` (identische Kinder)
- **P2:** `xᵢ(xᵢ(T₁, T₂), T₃) → xᵢ(T₁, T₂, T₃)` (gleiches Attribut zusammenfassen)
- **P3:** `xᵢ(..., C, ..., C, ...) → C` (wenn alle Pfade zur gleichen Klasse führen)

**Transformationsregeln:**
- **T1:** `xᵢ(xⱼ(T₁, T₂), xⱼ(T₃, T₄)) → xⱼ(xᵢ(T₁, T₃), xᵢ(T₂, T₄))` (Vertauschung)
- **T2:** `xᵢ(T, xⱼ(T₁, T₂)) → xⱼ(xᵢ(T, T₁), xᵢ(T, T₂))` (Distribution)

---

### Schrittweise Vereinfachung

**Ausgangszustand:**
```
x₃(x₂(x₁(C, A), x₁(B, A)), x₁(x₂(C, B), A))
```

---

**Schritt 1:** Anwendung von **T1** (Vertauschung) auf linken Teilbaum `x₂(x₁(C, A), x₁(B, A))`

```
x₃(x₁(x₂(C, B), x₂(A, A)), x₁(x₂(C, B), A))
```

*Erklärung:* `x₂(x₁(C, A), x₁(B, A))` wird zu `x₁(x₂(C, B), x₂(A, A))` durch Vertauschung von x₁ und x₂

---

**Schritt 2:** Anwendung von **P1** auf `x₂(A, A)` im linken Teilbaum

```
x₃(x₁(x₂(C, B), A), x₁(x₂(C, B), A))
```

*Erklärung:* `x₂(A, A) → A` (identische Kinder)

---

**Schritt 3:** Anwendung von **P1** auf `x₃(x₁(x₂(C, B), A), x₁(x₂(C, B), A))`

```
x₁(x₂(C, B), A)
```

*Erklärung:* Beide Teilbäume von x₃ sind identisch, daher `x₃(T, T) → T`

---

**Schritt 4:** Anwendung von **T2** (Distribution) auf `x₁(x₂(C, B), A)`

```
x₂(x₁(C, A), x₁(B, A))
```

*Erklärung:* `x₁(x₂(C, B), A)` wird zu `x₂(x₁(C, A), x₁(B, A))` durch Distribution von x₁ über x₂

---

### Endergebnis

**Vereinfachter Baum:** `x₂(x₁(C, A), x₁(B, A))`

**Zusammenfassung der Schritte:**

| Schritt | Regel | Baum |
|---------|-------|------|
| 0 | - | `x₃(x₂(x₁(C, A), x₁(B, A)), x₁(x₂(C, B), A))` |
| 1 | T1 | `x₃(x₁(x₂(C, B), x₂(A, A)), x₁(x₂(C, B), A))` |
| 2 | P1 | `x₃(x₁(x₂(C, B), A), x₁(x₂(C, B), A))` |
| 3 | P1 | `x₁(x₂(C, B), A)` |
| 4 | T2 | `x₂(x₁(C, A), x₁(B, A))` |

**Reduktion:** Von 3 Attributen auf 2 Attribute, von Tiefe 3 auf Tiefe 2

---

## DTL.03: Machine Learning mit Weka

### Datensätze

**Quellen:**
- Zoo-Datensatz: [zoo.csv](https://github.com/aimacode/aima-data/blob/master/zoo.csv)
- Restaurant-Datensatz: [restaurant.csv](https://github.com/aimacode/aima-data/blob/master/restaurant.csv)

---

### Teil 1: Training mit J48 (C4.5)

#### Zoo-Datensatz

**Entscheidungsbaum (J48):**
```
feathers = false
|   aquatic = false
|   |   predator = false
|   |   |   toothed = false
|   |   |   |   backbone = false: invertebrate
|   |   |   |   backbone = true
|   |   |   |   |   venomous = false: mammal
|   |   |   |   |   venomous = true: reptile
|   |   |   toothed = true
|   |   |   |   fins = false: mammal
|   |   |   |   fins = true: fish
|   |   predator = true
|   |   |   milk = true: mammal
|   |   |   milk = false
|   |   |   |   toothed = true: reptile
|   |   |   |   toothed = false: invertebrate
|   aquatic = true
|   |   predator = false: fish
|   |   predator = true
|   |   |   toothed = true: fish
|   |   |   toothed = false: invertebrate
feathers = true: bird
```

**Ergebnisse:**
- **Korrekt klassifiziert:** 101 Instanzen (100%)
- **Fehlerrate:** 0%
- **Baumgröße:** 19 Knoten, 10 Blätter

**Confusion Matrix:**
```
  a  b  c  d  e  f  g   <-- classified as
 41  0  0  0  0  0  0 | a = mammal
  0 20  0  0  0  0  0 | b = bird
  0  0  5  0  0  0  0 | c = reptile
  0  0  0 13  0  0  0 | d = fish
  0  0  0  0  4  0  0 | e = amphibian
  0  0  0  0  0 10  0 | f = insect
  0  0  0  0  0  0  8 | g = invertebrate
```

**Interpretation:** Perfekte Klassifikation - alle Tierarten wurden korrekt identifiziert.

---

#### Restaurant-Datensatz

**Entscheidungsbaum (J48):**
```
Patrons = None: No
Patrons = Some: Yes
Patrons = Full
|   Hungry = No: No
|   Hungry = Yes
|   |   Type = French: Yes
|   |   Type = Thai
|   |   |   Fri/Sat = No: No
|   |   |   Fri/Sat = Yes: Yes
|   |   Type = Burger: Yes
|   |   Type = Italian: No
```

**Ergebnisse:**
- **Korrekt klassifiziert:** 12 Instanzen (100%)
- **Fehlerrate:** 0%
- **Baumgröße:** 9 Knoten, 6 Blätter

**Confusion Matrix:**
```
 a b   <-- classified as
 6 0 | a = Yes
 0 6 | b = No
```

**Interpretation:** Perfekte Klassifikation auf Trainingsdaten - der Baum kann alle Restaurantentscheidungen korrekt vorhersagen.

---

### Teil 2: ARFF-Format

#### Unterschiede der Attributtypen

| Typ | Beschreibung | Beispiel | Verwendung |
|-----|--------------|----------|------------|
| **nominal** | Kategorische Werte ohne Ordnung | Farbe: {rot, grün, blau} | Qualitative Merkmale |
| **numeric/ordinal** | Numerische Werte mit Ordnung | Alter: 0-100, Preis: 10.5 | Quantitative Merkmale |
| **string** | Freitext | Namen, Beschreibungen | Textdaten (meist nicht für ID3) |

**Wichtig für ID3:**
- ID3 arbeitet nur mit **nominalen** Attributen
- Numerische Attribute müssen diskretisiert werden
- String-Attribute werden nicht unterstützt

#### ARFF-Dateien

**zoo.arff:**
```arff
@relation zoo

@attribute animal_name string
@attribute hair {true, false}
@attribute feathers {true, false}
@attribute eggs {true, false}
@attribute milk {true, false}
@attribute airborne {true, false}
@attribute aquatic {true, false}
@attribute predator {true, false}
@attribute toothed {true, false}
@attribute backbone {true, false}
@attribute breathes {true, false}
@attribute venomous {true, false}
@attribute fins {true, false}
@attribute legs numeric
@attribute tail {true, false}
@attribute domestic {true, false}
@attribute catsize {true, false}
@attribute type {mammal, bird, reptile, fish, amphibian, insect, invertebrate}

@data
aardvark,true,false,false,true,false,false,true,true,true,true,false,false,4,false,false,true,mammal
antelope,true,false,false,true,false,false,false,true,true,true,false,false,4,true,false,true,mammal
...
```

**restaurant.arff (für ID3 - alle nominal):**
```arff
@relation restaurant

@attribute Alt {Yes, No}
@attribute Bar {Yes, No}
@attribute Fri {Yes, No}
@attribute Hun {Yes, No}
@attribute Pat {None, Some, Full}
@attribute Price {$, $$, $$$}
@attribute Rain {Yes, No}
@attribute Res {Yes, No}
@attribute Type {French, Thai, Burger, Italian}
@attribute Est {0-10, 10-30, 30-60, >60}
@attribute WillWait {Yes, No}

@data
Yes,No,No,Yes,Some,$$$,No,Yes,French,0-10,Yes
Yes,No,No,Yes,Full,$,No,No,Thai,30-60,No
...
```

---

### Teil 3: Vergleich ID3 vs. J48

#### Zoo-Datensatz

**ID3-Ergebnisse:**
- **Problem:** ID3 kann nicht mit numerischen Attributen umgehen (legs)
- **Lösung:** Attribut "legs" diskretisieren oder entfernen
- Nach Anpassung: Ähnlicher Baum wie J48, evtl. weniger optimiert

**J48-Ergebnisse (CSV vs. ARFF):**
- Identische Ergebnisse
- 100% Genauigkeit
- Gleiche Baumstruktur

---

#### Restaurant-Datensatz

**Vergleich ID3 vs. J48:**

| Kriterium | ID3 | J48 |
|-----------|-----|-----|
| **Genauigkeit** | 100% | 100% |
| **Baumgröße** | Größer (keine Pruning) | Kompakter (mit Pruning) |
| **Wurzelattribut** | Patrons | Patrons |
| **Attributtypen** | Nur nominal | Nominal + numerisch |

**Hauptunterschiede:**
- **J48** verwendet Pruning → kompakterer Baum
- **J48** kann kontinuierliche Attribute verarbeiten
- **ID3** erstellt oft größere Bäume (Overfitting-Gefahr)
- Beide erreichen 100% auf Trainingsdaten (kleiner Datensatz!)

**CSV vs. ARFF:**
- Funktional identisch
- ARFF bietet explizite Typdeklaration
- ARFF erlaubt Metadaten und Constraints

---

### Fazit

**Erkenntnisse:**
1. J48 (C4.5) ist flexibler als ID3 (numerische Attribute, Pruning)
2. Beide Algorithmen erreichen auf kleinen Datensätzen perfekte Ergebnisse
3. ARFF-Format bietet bessere Kontrolle über Datentypen
4. Vorsicht bei 100% Trainingsgenauigkeit → Overfitting-Risiko bei ungesehenen Daten