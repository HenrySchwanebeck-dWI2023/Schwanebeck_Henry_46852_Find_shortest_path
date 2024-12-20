# EAI: Find the shortest path to a given map (with heuristics).

## Usage
- python main.py <csvfile> <start> <target> <algorithm>
### Example
- python main.py example.csv S G astar

## FAQ
### Modellierung des Graphen
- Übergabe als Adjazenzmatrix mit der Heuristik. Danach findet die Übertragung in eine Liste von Kanten (vertices) statt.

### Modellierung des States
- Ein State wird implizit modliert durch die Kombination der Varibalen: current_node, g_scores, f_scores und came_from.

### Ausgabe des Programms
- Im Erfolgsfall wird der gewählte Algorithmus mit Pfad Kosten und dem gelaufenem Pfad ausgegeben 
- Allgemein wird bei Fehlern auf "Usage:" und die 3 möglichen Algorithmen hingewiesen
- Wenn zu wenige Argumente angegeben werden, wird auf die inkorrekte Anzahl von Argumenten hingewiesen 
- Wenn ein falscher Algorithmus angegeben wird, wird auf einen falschen Algorithmus hingewiesen
- Wenn ein falscher Start- oder Endpunkt angegeben wird, wird dieses erwähnt

### Verwendete Heuristische Funktionen
- Die Art der heuritischen Funktion hängt von den Eingabedaten der CSV Datei ab
- Im Code wird die Heuristik als numerischer Wert verwendet
- Dazu wird die Heuristik als zulässig und konsistent angenommen

### A* vs. Greedy
- A* hat einen höheren Rechenaufwand aber errechnet dafür den optimalen Pfad
- Greedy hat einen geringeren Rechenaufwand und ist dadurch schneller, kann aber dafür in Sackgassen kommen
- A*: nimmt die numerische Schätzung aus der CSV Datei, die die verbleibenden Kosten vom aktuellen Knoten bis zum Ziel schätzen soll
- Greedy: verwendet immer den Nachbarn mit dem geringsten Heuristikwert

## Die Input Matrix
Die Nx(N+1) Matrix ist wie folgt abgebildet.
- Im Falle eines gerichteten Graphen wird wie folgt gelesen
    - Von Zeile nach Spalte
- Ein Knoten zu sich selbst hat immer Kosten 0
- Eine nicht vorhandene Kante ist entweder leer oder -1


https://www.tablesgenerator.com/markdown_tables

|   | A | B | C | D | Heuristic |
|---|---|---|---|---|-----------|
| A | 0 | 1 |   |   | 5         |
| B | 1 | 0 | 1 | 2 | 3         |
| C |   | 1 | 0 | 1 | 1         |
| D |   | 2 | 1 | 0 | 4         |

## Die Suchalgorithmen
Source: WiSe24/Introduction to Artificial Intelligence/Schumann
- Heuristics `h(n)`: guess/estimate path cost from a state to the goal state
- `g(n)`: cost so far to reach node

### Greedy
`f(n) = 0 + h(n)`
### Djikstera
`f(n) = g(n) + 0`
### A*
`f(n) = g(n) + h(n)`