# **Aufgabe 2b)**



**Algorithmus zur Berechnung des Scores:**

Der Algorithmus berechnet den Score in drei Hauptphasen: Frame-Erstellung, Bonusberechnung und Summierung des Gesamtscores.



**0. Erfassung / Vorverarbeitung der Würfe**

Jeder Wurf wird über die Methode *roll(int pins)* gespeichert. Dabei wird geprüft, ob die Eingabe gültig ist (0 ≤ Pins ≤ 10) und ob noch weitere Würfe erlaubt sind. Alle gültigen Würfe werden in einer Liste *rolls* gespeichert, die die gesamte Spielfolge abbildet. Dadurch bleibt der Zustand des Spiels nachvollziehbar und konsistent.



1. **Erstellung der Frames:**

Die Methode *createFrames()* gruppiert die gespeicherten Würfe zu einzelnen Frames.

Ein Strike wird als eigenes Frame gespeichert.

Ein normales Frame besteht aus zwei Würfen.

Im 10. Frame kann bei einem Strike oder Spare ein dritter Wurf hinzukommen.

Alle Frames werden in einer Liste *frames* gespeichert, die das Spiel logisch in 10 Abschnitte unterteilt. 

Dadurch kann die weitere Berechnung unabhängig von der ursprünglichen Wurfliste erfolgen.



**2. Bonusberechnung:**

Für jedes Frame wird geprüft, ob es sich um einen Strike oder Spare handelt. 

Bei einem Strike werden die Punkte der nächsten zwei Würfe als Bonus addiert.

Bei einem Spare wird der nächste Wurf als Bonus hinzugefügt.

Diese Berechnung ist in eigenen Methoden (*calculateStrikeBonus()* und *calculateSpareBonus()*) gekapselt, was die Logik klar trennt und die Wiederverwendbarkeit verbessert.



**3. Berechnung des Gesamtscores:**

Zum Schluss summiert die Methode *calculateTotalScore()* alle Frame-Scores und addiert die berechneten Boni.

Die Methode *score()* koordiniert den gesamten Ablauf, ruft die Teilschritte auf und liefert den endgültigen Gesamtscore zurück.





**Designentscheidung 1 – Datenstruktur und Kapselung:**

Wir verwenden zwei voneinander getrennte Listen:



*rolls* zur Speicherung aller einzelnen Würfe,

*frames* zur strukturierten Darstellung der 10 Spielabschnitte.

Diese Trennung verbessert die Übersicht und ermöglicht eine einfache Nachverfolgung der Wurfabfolge. Außerdem kapselt die Klasse **Frame** die Logik einzelner Frames (z. B. Strike-/Spare-Prüfung), wodurch der Code modularer und leichter testbar wird.





**Designentscheidung 2 – Wartbarkeit und TDD**

Der Code ist in kleine, fokussierte Methoden unterteilt, die jeweils eine klar definierte Aufgabe erfüllen. Dadurch ist der Programmablauf transparent und leicht verständlich.

Die Implementierung erfolgte nach dem Prinzip des Test-Driven Development: 

Für jede Regel des Bowling-Spiels wurde zunächst ein JUnit-Test erstellt (z. B. für Strikes, Spares, 10. Frame, ungültige Eingaben). 

Anschließend wurde der Code so entwickelt, dass alle Tests erfolgreich durchlaufen.

Dieses Vorgehen führte zu einer robusten und modularen Implementierung, bei der jede Änderung sofort getestet und validiert werden kann.

Durch den Einsatz von TDD wurde eine Testabdeckung von 100 % erreicht, was die Zuverlässigkeit, Wartbarkeit und langfristige Stabilität des Codes erheblich verbessert. (Bild von der 100% Testcoverage ist im Branch; kann man am Ende in die Latex-Abgabe hinzufügen)

