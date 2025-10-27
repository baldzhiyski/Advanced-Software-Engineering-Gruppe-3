# Dokumentation zur Nutzung von Generativer KI

Projekt: Exercise 1 – Kritischer Pfad (CPM)  
Autor: <Leonidas Katsaitis>  
Datum: 2025-10-27

## Zweck dieser Datei
Diese Datei dokumentiert, wo und wie ein Generative-AI-Assistent bei der Bearbeitung der Aufgabe eingesetzt wurde, welche Artefakte daraus entstanden sind, wie die Ergebnisse validiert wurden und welche Prompts (professionell formuliert) die Interaktion nachvollziehbar machen.

## Umfang der KI-Unterstützung
Der KI‑Assistent wurde eingesetzt für:
- technische Ausarbeitung der CPM-Logik (Vorwärts-/Rückwärtsrechnung mit ES/EF/LS/LF und Pufferzeit) inklusive topologischer Sortierung
- Erstellung und Anpassung von Unit-Tests (Pytest) für ein Minimalbeispiel und den Aufgaben-Netzplan (A01..A16),
- kleine API-Erweiterung (`project_duration()`),
- Ergänzung einer kurzen README mit Ausführungs- und Testhinweisen (PowerShell)

Nicht durch KI übernommen: Fachliche Bewertung der Ergebnisse, finaler Review der Berechnungen, Entscheidung über die akzeptierte Modellierung. Diese Schritte wurden manuell überprüft.

## Entstandene Artefakte (durch bzw. mit KI-Unterstützung)
- `Exercise1/critical_path.py` – Implementierung von `Activity` und `CriticalPathAnalyzer` (ES/EF/LS/LF, Slack, Topo-Sort) inkl. `project_duration()`.
- `Exercise1/test/test_criticalPath.py` – Minimaltest; Import-Pfad für Pytest korrigiert.
- `Exercise1/test/test_project_network.py` – Test des Aufgaben-Netzplans; prüft kritischen Pfad und Projektdauer.
- `Exercise1/main.py` – Beispielausführung; gibt kritischen Pfad und Projektdauer sowie alle Zeiten je Aktivität aus.
- `Exercise1/README.md` – Kurzanleitung (Ausführen/Tests unter Windows PowerShell).

## Validierung und Qualitätssicherung
- Automatisierte Tests: `2 passed` (über Pytest)
- Verifizierte Ergebnisse für den Aufgaben-Netzplan (A01..A16):
  - Kritischer Pfad: `A01 → A05 → A12 → A14`
  - Projektdauer: `21` Tage
- Die Skriptausgabe aus `Exercise1/main.py` bestätigt die berechneten ES/EF/LS/LF-Werte und die Pufferzeiten; die Resultate wurden mit der Aufgabenabbildung abgeglichen.

## Professionelle Prompt-Historie (rekonstruiert)
1. Implementiere Teil (b) der Aufgabe „Kritischer Pfad“ in Python:
   - Erstelle Klassen `Activity` und `CriticalPathAnalyzer` mit Vorwärts- und Rückwärtsrechnung (ES/EF/LS/LF, Slack) auf Basis einer topologischen Sortierung.
   - API-Kontrakt: Eingabe Liste von Aktivitäten (ID, Dauer, Abhängigkeiten). Methoden: `get_critical_path()` (Reihenfolge deterministisch) und eine Möglichkeit, die Gesamtdauer zu ermitteln.
   - Schreibe einen Unit-Test für ein kleines Beispiel (A1..A4) und ein Beispielskript.
   - Halte dich an snake_case für Dateinamen und Importe.

2. Benenne das Modul auf snake_case um und bereinige Importe:
   - Lege `Exercise1/critical_path.py` an, migriere Inhalt aus `criticalPath.py`, lösche das alte File.
   - Stelle sicher, dass `main.py` und Tests `from critical_path import ...` verwenden.

3. Führe die Tests aus und behebe Importpfade für Pytest:
   - Starte Pytest auf dem Minimaltest.
   - Falls Importfehler auftreten, ergänze im Test die Anpassung von `sys.path`, sodass `Exercise1` importierbar ist.

4. Ergänze einen Test für den Aufgaben-Netzplan (A01..A16):
   - Erzeuge `test_project_network.py`.
   - Erwarte als kritischen Pfad `A01, A05, A12, A14` und eine Projektdauer von `21`.

5. Erweitere die API um eine Komfortmethode:
   - Implementiere `CriticalPathAnalyzer.project_duration()` und verwende sie in `main.py` zur Ausgabe.

6. Dokumentiere die Nutzung:
   - Erstelle `README.md` mit Befehlen für Windows PowerShell zum Ausführen des Beispiels und der Tests.

7. Bereinige das Repository:
   - Entferne das alte Duplikatmodul und generierte Artefakte (`__pycache__`).

8. Erstelle diese Dokumentation:
   - Verfasse eine verständliche, knappe Dokumentation der KI-Nutzung samt professioneller Prompt-Historie.

## Transparenz und Verantwortlichkeit
- Der generierte Code wurde manuell geprüft und durch Tests abgesichert.
- Es wurden keine urheberrechtlich geschützten Codeblöcke aus externen Quellen kopiert; die Implementierung basiert auf gängigen CPM-Prinzipien.
- Sensible Daten wurden nicht an externe Dienste übermittelt; die Verarbeitung erfolgte auf Repo-Ebene.

## Reproduzierbarkeit (optional)
Führen Sie die folgenden Befehle aus dem Repo-Root in Windows PowerShell aus:

```powershell
# Beispielskript
.\.venv\Scripts\python.exe Exercise1\main.py

# Tests
.\.venv\Scripts\python.exe -m pytest -q
```

## Kontakt / Editierhinweis
Leonidas Katsaitis , st108535@stud.uni-stuttgart.de