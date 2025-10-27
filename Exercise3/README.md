# Exercise3 – Conway's Game of Life

## Beschreibung

Dieses Projekt implementiert **Conway’s Game of Life**, einen zellulären Automaten auf einem zweidimensionalen Gitter.
Jede Zelle kann **lebendig (O)** oder **tot (.)** sein und ändert ihren Zustand in diskreten Schritten ("Generationen") 
gemäß vier festen Regeln:

1. **Unterbevölkerung:** Eine lebende Zelle mit weniger als 2 lebenden Nachbarn stirbt.
2. **Überbevölkerung:** Eine lebende Zelle mit mehr als 3 lebenden Nachbarn stirbt.
3. **Stabilität:** Eine lebende Zelle mit 2 oder 3 lebenden Nachbarn überlebt.
4. **Geburt:** Eine tote Zelle mit genau 3 lebenden Nachbarn wird lebendig.

Zellen außerhalb des Gitters gelten standardmäßig als tot (`bounded`), können aber optional mit dem Modus `torus` 
so behandelt werden, dass das Gitter "wrap-around" ist (also wie eine Donut-Oberfläche).

---

## Features
- Saubere, klar strukturierte Domänenklasse `GameOfLife` mit intuitiver API:
  - `from_string(...)`, `to_string(...)`
  - `set_alive(x, y, True/False)`, `is_alive(x, y)`
  - `tick()` für den Übergang zur nächsten Generation
- Zwei **Randstrategien**: `bounded` (Standard, außerhalb = tot) und `torus` (Wrap-around).
- Vorgefertigte **Startmuster**: `block` (statisches Stillleben), `blinker` (Oszillator), `glider` (bewegendes Raumschiff).
- **Kommandozeilen-Interface (CLI):** Starten, Steuern und Beobachten von Mustern direkt im Terminal.
- Vollständig **getestet mit pytest**, inkl. Typannotationen (mypy) und Code-Analyse (ruff).
- Wartbarer Code nach **Clean Code**- und **TDD**-Prinzipien.

---

## Installation & Ausführung

```bash
# 1️⃣ Projekt einrichten
cd Exercise3
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2️⃣ Tests ausführen
pytest

# 3️⃣ Programm starten (Beispiel)
# Läuft ein Glider-Muster über 20 Schritte auf einer 20x10 Welt mit Wrap-around und 80ms Pause
python -m game_of_life.cli --pattern glider --width 20 --height 10 --steps 20 --torus --sleep 0.08
```

---

## Beispiele

### Beispiel 1: Stillleben (Block)
```
Initial:
.OO.
.OO.

Nach mehreren Ticks: unverändert (stabil)
```

### Beispiel 2: Oszillator (Blinker)
```
Start:
..O..
..O..
..O..

→ Tick →
.....
.OOO.
.....
```

### Beispiel 3: Glider (bewegend)
```
Start:
.O.
..O
OOO

Nach mehreren Ticks: bewegt sich diagonal über das Gitter
```

---

## Algorithmus zur Berechnung der nächsten Generation ("Score")

Die Berechnung erfolgt **regelbasiert und deterministisch**. Für jede Zelle `(x, y)` wird die Anzahl der lebenden 
Nachbarn `n` in der 8er-Nachbarschaft bestimmt. Anschließend werden die Regeln angewendet:

```text
Wenn Zelle lebendig ist:
    Wenn n < 2 → stirbt (Unterbevölkerung)
    Wenn n == 2 oder n == 3 → überlebt (Stabilität)
    Wenn n > 3 → stirbt (Überbevölkerung)
Wenn Zelle tot ist:
    Wenn n == 3 → wird lebendig (Geburt)
```

Das Ergebnis wird in ein neues Gitter (`next_grid`) geschrieben, um Seiteneffekte zu vermeiden.

---

## Designentscheidungen

### 1️⃣ Datenstruktur
- **2D-Boolean-Matrix (`list[list[bool]]`)** als Hauptspeicherstruktur.
  - Vorteil: einfache Indexierung, intuitive Lesbarkeit, direkte Abbildung der Welt.
  - Alternative: `set[(x, y)]` für große, dünn besiedelte Welten – könnte später leicht integriert werden.

### 2️⃣ Methodenaufbau und Wartbarkeit
- Kleine, klar getrennte Methoden:
  - `_alive_neighbors()` zählt Nachbarn, getrennt von der Logik in `tick()`.
  - `is_alive()` und `set_alive()` kapseln Zugriffe auf den Zustand.
  - Dadurch leicht testbar und verständlich.
- Verwendung von **`__post_init__`** in `dataclass` für saubere Initialisierung und Validierung.

### 3️⃣ Test-Driven Development (TDD)
- Zuerst Tests für Basismethoden (`set_alive`, `is_alive`, `from_string`).
- Danach schrittweise Tests für Regeln (Geburt, Tod, Stabilität).
- Abschließend Integrationstests für komplexe Muster (`block`, `blinker`, `glider`).

Diese Vorgehensweise garantiert **Korrektheit, Lesbarkeit und Erweiterbarkeit**.

---

## CLI Parameterübersicht

| Parameter | Bedeutung | Standard |
|------------|------------|-----------|
| `--width` | Breite des Gitters | 20 |
| `--height` | Höhe des Gitters | 10 |
| `--pattern` | Startmuster (`block`, `blinker`, `glider`) | `blinker` |
| `--steps` | Anzahl der Generationen | 30 |
| `--torus` | Wrap-around aktivieren (statt Rand = tot) | deaktiviert |
| `--sleep` | Pause zwischen den Schritten (Sekunden) | 0.12 |
| `--offset-x` | X-Verschiebung des Musters | 2 |
| `--offset-y` | Y-Verschiebung des Musters | 2 |

---

## Fazit

Diese Implementierung demonstriert einen **sauberen, wartbaren Softwareentwurf** für ein klassisches Algorithmusproblem.  
Durch die klare API, Modularität und Testabdeckung eignet sich der Code hervorragend für Weiterentwicklungen, z. B. GUI, Parallelisierung oder Visualisierung.
