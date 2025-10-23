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
[1, 8, 3, 6, 5, 4, 7, 2]
```

Der Index des Arrays repräsentiert die Spalten und die Werte zeigen die Zeilen der Position der Königinnen.

**Operatoren:**

Als *Crossover* wäre hier das Tauschen von zwei Teilen der Eltern eine Möglichkeit. Also das Auftrennen der Eltern an der gleichen Stelle.

Für eine Mutation könnte man die zwei Werte des Arrays miteinander vertauschen (Swap-Mutation)

**Fitnessfunktion:**

Wenn man etwas recherchiert findet man folgende Formel zum errechnen von Kombinationen ohne Wiederholung:

$$\binom{8}{2} = \frac{8*7}{2} = 28$$

Das heißt es gibt 8 Königinnen die man als Paar verrechnen kann, da zwei Königinnen einen Konflikt verursachen können. Die Formel gibt an, das es also 28 konfliktfreie Paare geben kann. Man kann als Fitnessformel also annehmen:

$$f(x) = 28 - \text{Anzahl der Konfliktpaare}$$

Wenn man 28 erreicht hat man nicht ein Konfliktpaar auf dem Brett -> perfektes Ergebnis

**Landkarten-Färbeproblem:**

Regionen einer Landkarte sollen mit der minimalen Anzahl an Farben gefärbt werden, wobei niemals zwei aneinander grenzende Länder gleich gefärbt sein dürfen.

**Kodierung:**

Der Einfachheit halber kann man hier wieder den gleichen Ansatz verfolgen wie bei den Königinnen:

```java
[1, 2, 3, 4, 5, 1]
```

Diesmal ist jeder ein Index ein bestimmtes Land und der Wert im Array eine bestimmte Farbe.

**Operatoren:**

Auch hier würde wieder als *Crossover* das Austauschen von identisch aufgeteilten Elternteilen funktionieren.

Als *Mutation* würde hier auch wieder die Swap-Mutation gehen. Desweiteren müsste es eine Mutation geben, welche den Wert von nur einem Feld gegen einen anderen tauschen, um Farben rauszutauschen und so näher dem Ziel von möglichst wenig Farben zu kommen.

**Fitnessfunktion:**

Hier greift eine ähnliche herangehensweise wie schon beim Queens-Problem, nur das hier noch erweitert werden muss, um die Bedingung, möglichst wenig Farben zu nutzen, zu ergänzen.

Die wichtige Regel: keine Konflikte

$$f(x) = M - Konflikte$$

$M$ ist hier die maximale Anzahl möglicher Konflikte

Zusätzlich möglichst wenig Farben:

$$f(x) = -(\text{genutzte Farben})$$

das kann man mit Konflikten verrechnen:

$$f(x) = -((M - Konflikte) + genutzte Farben)$$

Im Netz findet man hier jetzt noch die Gewichtung der beiden Faktoren, um die Konflikte bei der Beurteilung der Fitness als wichtiger zu wiegen als die Farben, da es sich hierbei um die wichtigere Regel handelt.

$$f(x) = -(\alpha * (M - Konflikte) + \beta * \text{genutzte Farben}) $$

**Simulated Annealing:**

Für Simulated Annealing braucht man zusätzlich zu den bisher definierten Sachen noch einen "Temperaturwert" welcher angewandt wird wenn ein akzeptanzkriterium geprüft wird. Das kann einfach sein das der neue Zustand besser sein muss als der alte und dann wird dieser mit einer errechneten Wahrscheinlichkeit aus dem Konflikt und der Temperatur aktzeptiert.

### EA.02: Implementierung

**8-Queens-Problem:**

| Populationsgröße | Max. Gen. |    SR [%] | AES (Eval.) | AES (Gen.) | Ø Fitness | Bemerkung                                     |
| ---------------: | --------: | --------: | ----------: | ---------: | --------: | --------------------------------------------- |
|               10 |       100 |     23.52 |      510.06 |      50.01 |     27.06 | niedrige Erfolgsrate, geringe Vielfalt        |
|               20 |       100 |     30.83 |      544.77 |      26.24 |     27.18 | stabile Konvergenz                            |
|               30 |       100 | **31.34** |      581.87 |      18.40 |     27.19 | beste Rate bei 100 Gen., aber höherer Aufwand |
|               10 |       200 |     28.02 |      632.86 |      62.29 |     27.14 | längere Laufzeit, etwas besser                |
|               20 |       200 |     29.02 |      560.01 |      27.00 |     27.16 | ähnlich stabil wie 20/100                     |
|               30 |       200 |     30.80 |      584.14 |      18.47 |     27.18 | kaum besser, trotz doppelter Gen.-Zahl        |

Wie man der Tabelle entnehmen kann ist für meine Implementierung die Kombination von 100 Generationen und einer Populationsgröße von 30 das Optimum erreicht. Hier ist der Rechenaufwand aber bereits sehr hoch. 200 Generationen bringen keine nennenswerte Verbesserung, die beste Fitness meist schon innerhalb der ersten 100 Generationen gefunden wird.

Die Anzahl der Eltern war bei diesen Versuchen immer 5.

### EA.03: Anwendung