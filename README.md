# Grundlagen_KI

In diesem Repository werden die Aufgaben von Grundlagen der KI aus dem 3.Semester Informatik an der HSBI Campus Minden bearbeitet(2025/26)

Die einzelnen Aufgabenblätter werden in Branches dieses Repository´s bearbeitet.

## Blatt 2

### EA.01: Modellierung

**8-Queens-Problem:**

8 Königinnen sollen auf einem 8x8 Brett so verteilt werden, das sie sich gegenseitig vertikal, horizontal und diagonal nicht bedrohen.

**Kodierung:**

Die Darstellung als Array wäre hier möglich:

```java
[1, 5, 8, 6, 3, 7, 2, 4]
```

Der Index des Arrays repräsentiert die Spalten und die Werte zeigen die Zeilen der Position der Königinnen.

**Operatoren:**

Als *Crossover* wäre hier das Tauschen von zwei Teilen der Eltern eine Möglichkeit. Also das Auftrennen der Eltern an der gleichen Stelle.

Für eine Mutation könnte man die zwei Werte des Arrays miteinander vertauschen.

**Fitnessfunktion:**

Wenn man etwas recherchiert findet man folgende Formel zum errechnen von Kombinationen ohne Wiederholung:

$$\binom{8}{2} = \frac{8*7}{2} = 28$$

Das heißt es gibt 8 Königinnen die man als Paar verrechnen kann, da zwei Königinnen einen Konflikt verursachen können. Die Formel gibt an, das es also 28 konfliktfreie Paare geben kann. Man kann als Fitnessformel also annehmen:

$$f(x) = 28 - \text{Anzahl der Konfliktpaare}$$

Wenn man 28 erreicht hat man nicht ein Konfliktpaar auf dem Brett -> perfektes Ergebnis

**Landkarten-Färbeproblem:**

Regionen einer Landkarte sollen mit der minimalen Anzahl an Farben gefärbt werden, wobei niemals zwei aneinander grenzende Länder gleich gefärbt sein dürfen.

**Kodierung:**



### EA.02: Implementierung

### EA.03: Anwendung