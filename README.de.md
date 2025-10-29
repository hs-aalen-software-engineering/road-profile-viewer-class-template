# Refactoring-Übung: Vom Monolithen zu Modulen

> **[DE]** Dies ist die deutsche Version. **[EN]** For English instructions, see [README.md](README.md)

Willkommen zur Refactoring-Übung! Diese Aufgabe vertieft die Konzepte aus **Vorlesung 4: Refactoring - Vom Monolithen zu Modulen**.

## 📚 Lernziele

Durch diese Übung wirst du:

1. **Den Refactoring-Workflow aus Vorlesung 4 anwenden**, um monolithischen Code in modulare Komponenten zu transformieren
2. **Feature-Branch-Entwicklung nutzen** (Vorlesung 3 Teil 1) mit korrektem Git-Workflow
3. **CI/CD-Praktiken befolgen** (Vorlesung 3 Teil 2) mit automatischen Qualitätsprüfungen
4. **Inkrementelle Commits üben**, die den schrittweisen Refactoring-Prozess zeigen
5. **An Peer-Code-Review teilnehmen**, um voneinander zu lernen

## 🎯 Aufgabenübersicht

Du wirst die monolithische `src/road_profile_viewer/main.py` (390 Zeilen) in vier fokussierte Module umstrukturieren:

- `geometry.py` - Reine Mathematikfunktionen (Strahlenschnittpunkt-Berechnungen)
- `road.py` - Straßenprofil-Generierung
- `visualization.py` - Dash-UI-Schicht
- `main.py` - Vereinfachter Einstiegspunkt (~20 Zeilen)

**Das ist genau das, was du in Vorlesung 4 gelernt hast!** Folge der Vorlesung Schritt für Schritt.

## 📋 Anforderungen

### 1. Git-Workflow (25 Punkte)

- [ ] Erstelle einen Feature-Branch: `feature/refactor-to-modules`
- [ ] Mache **mindestens 3 inkrementelle Commits** (einen pro Modul-Extraktion)
- [ ] Schreibe **beschreibende Commit-Nachrichten** (> 10 Zeichen)
- [ ] Erstelle einen **Pull Request** von deinem Feature-Branch zu `main`
- [ ] **Merge NICHT** bevor alle Checks bestehen und du Peer-Review-Freigabe hast

### 2. Code-Struktur (35 Punkte)

- [ ] Erstelle `geometry.py` mit:
  - `calculate_ray_line()`-Funktion
  - `find_intersection()`-Funktion
  - Korrekten Docstrings und Type Hints

- [ ] Erstelle `road.py` mit:
  - `generate_road_profile()`-Funktion
  - Korrekten Docstrings

- [ ] Erstelle `visualization.py` mit:
  - `create_dash_app()`-Funktion
  - Dem gesamten Dash-UI-Code
  - Imports von `geometry` und `road`

- [ ] Vereinfache `main.py` auf:
  - **Weniger als 30 Zeilen**
  - Nur Imports von `visualization`
  - Nur die `main()`-Funktion und `if __name__ == '__main__'`

### 3. Code-Qualität (25 Punkte)

- [ ] **Ruff Linting** besteht (keine Stil-Verstöße)
- [ ] **Ruff Formatierung** besteht (Code ist korrekt formatiert)
- [ ] **Pyright** besteht (keine Typ-Fehler)
- [ ] **Korrekte Imports** ohne zirkuläre Abhängigkeiten
- [ ] **Abhängigkeitsfluss**: `main → visualization → geometry/road`

### 4. Peer Review (15 Punkte)

- [ ] **Review anfragen** von einem Kommilitonen
- [ ] **Freigabe erhalten** vor dem Mergen
- [ ] **Einen anderen PR reviewen** und konstruktives Feedback geben

## 🚀 Schritt-für-Schritt-Anleitung

### Schritt 1: Repository klonen

```bash
# GitHub Classroom erstellt ein Repo für dich - klone es
git clone https://github.com/hs-aalen-software-engineering/refactoring-DEIN-USERNAME.git
cd refactoring-DEIN-USERNAME
```

### Schritt 2: Feature-Branch erstellen

```bash
# Stelle sicher, dass du auf main bist und aktuell
git checkout main
git pull origin main

# Erstelle Feature-Branch
git checkout -b feature/refactor-to-modules

# Überprüfe, dass du auf dem neuen Branch bist
git branch
```

### Schritt 3: Geometry-Modul extrahieren

**Folge Vorlesung 4, Abschnitt 6.2**

1. Erstelle `geometry.py` im **src/road_profile_viewer/ Verzeichnis** (auf gleicher Ebene wie `src/road_profile_viewer/`)
2. Kopiere `calculate_ray_line()` und `find_intersection()` aus `src/road_profile_viewer/main.py`
3. Füge die korrekten Imports hinzu: `import numpy as np`
4. Füge Type Hints hinzu (siehe Vorlesung 4 Beispiel)
5. Teste, dass es funktioniert (keine Fehler beim Import)

**Committe deinen Fortschritt:**

```bash
git add geometry.py
git commit -m "Extrahiere Geometrie-Funktionen nach geometry.py

- Verschiebe calculate_ray_line() und find_intersection()
- Füge Type Hints und Docstrings hinzu
- Bereite modulares Testing vor"
```

### Schritt 4: Road-Modul extrahieren

**Folge Vorlesung 4, Abschnitt 6.3**

1. Erstelle `road.py` im **src/road_profile_viewer/ Verzeichnis**
2. Kopiere `generate_road_profile()` aus `src/road_profile_viewer/main.py`
3. Füge korrekte Imports und Docstrings hinzu

**Committe deinen Fortschritt:**

```bash
git add road.py
git commit -m "Extrahiere Straßengenerierung nach road.py

- Verschiebe generate_road_profile()
- Trenne Datengenerierung von Geometrie und UI"
```

### Schritt 5: Visualization-Modul extrahieren

**Folge Vorlesung 4, Abschnitt 6.4**

1. Erstelle `visualization.py` im **src/road_profile_viewer/ Verzeichnis**
2. Kopiere `create_dash_app()` und den gesamten UI-Code aus `src/road_profile_viewer/main.py`
3. Füge Imports hinzu (nutze relative Imports innerhalb des Packages):
   ```python
   from .geometry import calculate_ray_line, find_intersection
   from .road import generate_road_profile
   ```
   **Hinweis:** Der `.` bedeutet "aus dem gleichen Package" - so funktionieren Python-Packages!

**Committe deinen Fortschritt:**

```bash
git add visualization.py
git commit -m "Extrahiere UI-Schicht nach visualization.py

- Verschiebe create_dash_app() und gesamten Dash-Code
- Importiere von geometry- und road-Modulen
- Vollständige Separation of Concerns"
```

### Schritt 6: main.py vereinfachen

**Folge Vorlesung 4, Abschnitt 6.4 (Ende)**

1. Die monolithische `main.py` existiert bereits in `src/road_profile_viewer/`
2. Ersetze sie durch eine vereinfachte Version (~20 Zeilen):

```python
"""
Road Profile Viewer - Einstiegspunkt

Dies ist der Haupteinstiegspunkt für die Road Profile Viewer Anwendung.
Alle Funktionalität ist in separaten Modulen implementiert.
"""

from .visualization import create_dash_app


def main():
    """Hauptfunktion zum Starten der Dash-Anwendung."""
    app = create_dash_app()
    print("Starte Road Profile Viewer...")
    print("Öffne deinen Browser und navigiere zu: http://127.0.0.1:8050/")
    print("Drücke Ctrl+C um den Server zu stoppen.")
    app.run(debug=True)


if __name__ == '__main__':
    main()
```

**Hinweis:** Auch hier nutze relative Imports (`.visualization`), da wir innerhalb des Packages sind!

**Committe deinen Fortschritt:**

```bash
git add main.py
git commit -m "Erstelle vereinfachte main.py Einstiegspunkt

- Nur Imports von visualization-Modul
- Fungiert als Einstiegspunkt (~20 Zeilen)
- Vervollständigt Refactoring zur modularen Struktur"
```

### Schritt 7: Lokale Checks ausführen

**Teste alles, bevor du pushst!**

```bash
# Installiere Dependencies
uv sync

# Führe Qualitätschecks aus (diese MÜSSEN bestehen)
uv run ruff check .
uv run ruff format --check .
uv run pyright

# Wenn du Fehler siehst, behebe sie und committe die Fixes
```

### Schritt 8: Pushen und Pull Request erstellen

```bash
# Pushe deinen Feature-Branch
git push -u origin feature/refactor-to-modules

# Erstelle PR mit GitHub CLI (empfohlen)
gh pr create --title "Refactor: Teile Monolithen in fokussierte Module" \
  --body "Refactored src/road_profile_viewer/main.py in modulare Struktur:

- geometry.py: Strahlenschnittpunkt-Mathematik
- road.py: Straßengenerierung
- visualization.py: Dash UI
- main.py: Einstiegspunkt (~20 Zeilen)

Alle Code-Qualitätschecks bestehen.
Bereit für Review!"

# Oder erstelle PR manuell im GitHub-Webinterface
```

### Schritt 9: Auf CI-Checks warten

**GitHub Actions führt automatisch aus:**

- ✅ Strukturcheck (überprüft, ob Dateien existieren, Imports korrekt sind, etc.)
- ✅ Git-Workflow-Check (überprüft Feature-Branch, inkrementelle Commits)
- ✅ Code-Qualitätscheck (Ruff, Pyright)

**Schaue im "Actions"-Tab auf GitHub für die Ergebnisse.**

Wenn Checks fehlschlagen, lies die Fehlermeldungen, behebe die Probleme, committe und pushe erneut.

### Schritt 10: Peer Review einholen

**Teile deinen PR-Link mit einem Kommilitonen:**

```
Hey! Kannst du meinen Refactoring-PR reviewen?
https://github.com/hs-aalen-software-engineering/refactoring-DEIN-USERNAME/pull/1
```

**Als Reviewer überprüfe:**

- [ ] PR ist vom `feature/refactor-to-modules` Branch
- [ ] Mindestens 3 inkrementelle Commits existieren
- [ ] Alle 4 Dateien existieren (`geometry.py`, `road.py`, `visualization.py`, `main.py`)
- [ ] `main.py` ist vereinfacht (< 30 Zeilen)
- [ ] Funktionen sind in den korrekten Modulen
- [ ] Imports fließen korrekt (keine zirkulären Abhängigkeiten)
- [ ] Alle CI-Checks bestehen (grüne Häkchen)

**Wie man approved:**

1. Gehe zum PR
2. Klicke "Files changed" Tab
3. Reviewe den Code
4. Klicke "Review changes" → "Approve" → "Submit review"

### Schritt 11: PR mergen

**Sobald du hast:**
- ✅ Alle CI-Checks bestehen
- ✅ Peer-Review-Freigabe

**Merge deinen PR:**

```bash
# Mit GitHub CLI
gh pr merge --squash

# Oder klicke "Merge pull request" im GitHub-Webinterface
```

**Glückwunsch! Du hast die Refactoring-Übung abgeschlossen! 🎉**

## 🔍 Wie du bewertet wirst

### Automatische Checks (85 Punkte)

GitHub Actions überprüft automatisch:

| Check | Punkte | Was wird überprüft |
|-------|--------|-------------------|
| **Strukturcheck** | 35 | Alle Dateien existieren, Funktionen in korrekten Modulen, Imports korrekt |
| **Git-Workflow** | 25 | Feature-Branch, 3+ Commits, beschreibende Nachrichten |
| **Code-Qualität** | 25 | Ruff, Pyright bestehen; keine zirkulären Abhängigkeiten |

### Manuelle Überprüfung (15 Punkte)

Dozent überprüft:

- Du hast Peer-Review-Freigabe erhalten
- Das Review war substantiell (nicht nur "LGTM")

## ❓ Fehlerbehebung

### "Import-Fehler beim lokalen Ausführen"

Stelle sicher, dass du alle Module im **src/road_profile_viewer/ Verzeichnis** erstellst. Das ist die korrekte Python-Package-Struktur!

```
✅ Korrekte Struktur:
road-profile-viewer-DEIN-USERNAME/
├── README.md
├── pyproject.toml
├── tests/
│   └── test_smoke.py
└── src/
    └── road_profile_viewer/       ← Alle Module gehen HIERHIN
        ├── __init__.py
        ├── geometry.py            ← ERSTELLE DIES
        ├── road.py                ← ERSTELLE DIES
        ├── visualization.py       ← ERSTELLE DIES
        └── main.py                ← VEREINFACHE DIES (ursprünglich 390 Zeilen → ~20 Zeilen)

❌ Falsche Struktur:
road-profile-viewer-DEIN-USERNAME/
├── geometry.py                    ← FALSCH! Nicht in src/
├── road.py                        ← FALSCH! Nicht in src/
└── src/
    └── road_profile_viewer/
        └── main.py
```

### "Ruff-Fehler"

Wenn du Ruff-Fehler bekommst, behebe sie! Die monolithische `main.py` folgt bereits PEP 8, aber beim Extrahieren könntest du Probleme einführen:

```python
# ❌ Häufige Fehler beim Extrahieren:
def generate_road_profile(num_points=100,x_max=80):  # Fehlendes Leerzeichen nach Komma
    y=0.015 * x_norm**3 * x_max                      # Fehlende Leerzeichen um =
    return x,y                                        # Fehlendes Leerzeichen nach Komma

# ✅ Korrekt:
def generate_road_profile(num_points=100, x_max=80):
    y = 0.015 * x_norm**3 * x_max
    return x, y
```

**Auto-Fix für die meisten Probleme:**
```bash
uv run ruff check --fix .
uv run ruff format .
```

### "Strukturcheck schlägt fehl: main.py zu lang"

Deine `main.py` sollte **~20 Zeilen** sein, nicht 390! Du solltest eine **neue** `main.py` mit nur dem Einstiegspunkt erstellen, nicht die gesamte Originaldatei kopieren.

### "Zirkuläre Abhängigkeit erkannt"

Stelle sicher, dass Abhängigkeiten in eine Richtung fließen:

```
✅ Korrekt:
main.py → visualization.py → geometry.py, road.py

❌ Falsch:
geometry.py → visualization.py → geometry.py (ZIRKULÄR!)
```

**Regel:** Module niedrigerer Ebene (`geometry.py`, `road.py`) sollten NICHT von Modulen höherer Ebene (`visualization.py`, `main.py`) importieren.

### "Keine Peer-Review-Freigabe"

Frage einen Kommilitonen! Teile deinen PR-Link im Kurs-Chat oder während der Vorlesung.

Wenn du Hilfe beim Finden eines Reviewers brauchst, kontaktiere den Dozenten.

### "CI-Checks laufen nicht"

Stelle sicher:
1. Du hast einen PR erstellt (nicht nur auf main gepusht)
2. Der PR ist von deinem Feature-Branch zu `main`
3. Schaue im "Actions"-Tab nach Fehlern

## 📚 Referenz

- **Vorlesung 4**: Vollständiges Refactoring-Tutorial
- **Vorlesung 3 Teil 1**: Feature-Branch-Workflow
- **Vorlesung 3 Teil 2**: CI/CD-Automatisierung
- **Vorlesung 2**: Code-Qualität (PEP 8, Ruff)

## 🆘 Hilfe bekommen

1. **Lies Vorlesung 4 nochmal** - Sie hat Schritt-für-Schritt-Anleitungen!
2. **Prüfe CI-Fehlermeldungen** - Sie sagen dir genau, was falsch ist
3. **Frage im Kurs-Chat** - Helft einander!
4. **Sprechstunde** - Dozent ist für Fragen verfügbar

Viel Erfolg! 🚀

---

**Aufgabe erstellt**: 2025-10-29
**Kurs**: Software Engineering - HS Aalen
**Dozent**: Dominik Mueller
