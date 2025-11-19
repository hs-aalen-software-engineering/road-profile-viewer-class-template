# Straßenprofil-Datenbank & Upload-System

> **[DE] Deutsche Version:** Sie lesen sie gerade!
> **[EN] English Version:** For full instructions in English, see [README.md](README.md)

Willkommen zur Übung "Straßenprofil-Datenbank & Upload-System"! Dies ist eine **Gruppenaufgabe**, bei der Sie eine bestehende Dash-Anwendung um Datenbank-Persistenz, Multi-Profil-Auswahl und Datei-Upload-Funktionen erweitern werden.

> **Hinweis:** Fehlermeldungen von automatisierten Prüfungen (GitHub Actions Workflows) erscheinen in **Englisch und Deutsch**.

## 📚 Lernziele

Durch diese Übung werden Sie:

1. **Datenbanken integrieren** in Web-Anwendungen (SQLite mit FastAPI/SQLModel ODER TinyDB)
2. **REST APIs entwerfen und implementieren** (bei FastAPI-Ansatz)
3. **Multi-Page Dash-Anwendungen erstellen** mit Datei-Upload und Datenvalidierung
4. **Pydantic-Validierung anwenden** für Datenintegrität
5. **Kollaborative Entwicklung praktizieren** mit Feature Branches und Code Reviews
6. **Hohe Testabdeckung erreichen** (90%+ bei neuen Features)
7. **Implementierungsentscheidungen dokumentieren** und technische Planung

## 🎯 Aufgabenübersicht

Sie werden die bestehende Straßenprofil-Viewer-Anwendung um folgende Features erweitern:

**Aktueller Stand:**
- Einzelnes Standard-Straßenprofil (fest codiert)
- Kameraposition und Sichtstrahl-Visualisierung
- Schnittpunkt-Berechnung und Anzeige

**Ihre Aufgabe - Hinzufügen:**
1. **Dropdown-Auswahl** zur Auswahl aus mehreren gespeicherten Straßenprofilen
2. **Datenbank-Backend** zur Persistierung von Straßenprofilen
3. **Upload-Seite**, auf der Benutzer neue Profile via JSON-Dateien hinzufügen können
4. **Profil-Vorschau** mit Grafik vor dem Speichern
5. **Profil-Umbenennung** auf der Upload-Seite
6. **Datenvalidierung** mit Pydantic-Modellen

## 🏗️ Technische Ansätze

Sie können zwischen zwei Implementierungsansätzen mit unterschiedlichen Punktwerten wählen:

### Ansatz 1: FastAPI + SQLModel + SQLite (5 Punkte möglich)

**Architektur:**
- **Backend**: FastAPI REST API mit Endpunkten für CRUD-Operationen
- **Datenbank**: SQLite mit SQLModel ORM
- **Frontend**: Dash-App, die die API konsumiert
- **Migration**: Datenbank-Initialisierung und Seeding-Skripte

**Warum dieser Ansatz:**
- Industriestandard-Architektur (Separation of Concerns)
- Skalierbar und testbar
- Anspruchsvoller, ermöglicht volle 5 Punkte

**Hauptkomponenten:**
```
src/road_profile_viewer/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI App
│   └── routes.py        # API Endpunkte
├── database/
│   ├── __init__.py
│   ├── models.py        # SQLModel Datenbankmodelle
│   └── connection.py    # Datenbank-Setup
├── models.py            # Pydantic Validierungsmodelle
└── visualization.py     # Aktualisierte Dash-App mit API-Aufrufen
```

### Ansatz 2: TinyDB (4 Punkte möglich)

**Architektur:**
- **Datenbank**: TinyDB (JSON-basiert, kein separates Backend nötig)
- **Frontend**: Dash-App mit direktem TinyDB-Zugriff
- **Einfacher**: Aller Code in Dash-Anwendung integriert

**Warum dieser Ansatz:**
- Leichtgewichtig und einfach
- Keine API-Schicht nötig
- Gut zum Lernen von Datenbank-Grundlagen

**Hauptkomponenten:**
```
src/road_profile_viewer/
├── database/
│   ├── __init__.py
│   └── db.py            # TinyDB Operationen
├── models.py            # Pydantic Validierungsmodelle
└── visualization.py     # Aktualisierte Dash-App mit TinyDB
```

**Wählen Sie basierend auf:**
- Zeitverfügbarkeit Ihres Teams
- Lernziele (FastAPI lernen wollen?)
- Ambitionsniveau (Ziel: volle 5 Punkte?)

## 📋 Anforderungen

### 1. Implementierung (2 Punkte)

#### Dropdown-Auswahl (0,8 Punkte)
- [ ] Dropdown-Komponente auf Hauptseite zur Auswahl von Straßenprofilen
- [ ] Dropdown listet alle verfügbaren Profile nach Namen auf
- [ ] Auswahl eines Profils aktualisiert die Visualisierung
- [ ] Standard-Profil beim App-Start vorausgewählt

#### Upload-Seite (1,2 Punkte)
- [ ] Neue Seite/Route in Dash-App erstellen (`/upload`)
- [ ] Datei-Upload-Komponente, die JSON-Dateien akzeptiert
- [ ] Vorschau-Grafik, die hochgeladenes Profil vor dem Speichern zeigt
- [ ] Texteingabe zum Umbenennen des Profils
- [ ] Bestätigungs-Button zum Speichern in Datenbank
- [ ] Erfolgs-/Fehlermeldungen nach Upload
- [ ] Navigation zwischen Hauptseite und Upload-Seite

### 2. Backend & Datenbank (1,5 Punkte)

#### Datenbank-Schema (0,5 Punkte)
- [ ] Straßenprofil-Modell mit Feldern: `id`, `name`, `x_coordinates`, `y_coordinates`
- [ ] Unique-Constraint auf Profilnamen
- [ ] Richtige Datentypen (list/array für Koordinaten)

#### Datenbank-Operationen (0,5 Punkte)
- [ ] Create (neues Profil einfügen)
- [ ] Read (alle Profile abrufen, nach Name/ID abrufen)
- [ ] Update (optional, aber empfohlen)
- [ ] Delete (optional, aber empfohlen)

#### Migration/Seed (0,5 Punkte)
- [ ] Skript zur Datenbank-Initialisierung
- [ ] Standard-Profil beim ersten Start einfügen
- [ ] Datenbank-Datei in `.gitignore` (nicht committen)

**FastAPI-Ansatz Bonus (+1 Punkt):**
- [ ] REST API Endpunkte: `GET /profiles`, `POST /profiles`, `GET /profiles/{id}`
- [ ] Ordentliches Error Handling (404, 409 Konflikt, 422 Validierung)
- [ ] FastAPI automatische Dokumentation (`/docs`)
- [ ] Separation of Concerns (API-Schicht getrennt von Dash)

### 3. Datenvalidierung (in Implementierungspunkten enthalten)

- [ ] Pydantic-Modell passend zum Beispiel-JSON-Schema
- [ ] Validierungsregeln:
  - Name: 1-100 Zeichen, nicht leer
  - `x_coordinates` und `y_coordinates`: gleiche Länge, mindestens 2 Punkte
  - Koordinaten müssen numerisch sein (Floats)
- [ ] Klare Fehlermeldungen bei Validierungsfehlern
- [ ] Beispiel-JSON-Datei bereitgestellt in `docs/example-road-profile.json`

### 4. Testing (0,5 Punkte)

- [ ] **90%+ C1-Abdeckung** für alle neuen Features
- [ ] Unit Tests für:
  - Datenbank-Operationen (CRUD)
  - API-Endpunkte (bei FastAPI-Ansatz)
  - Pydantic-Validierung (gültige und ungültige Fälle)
  - Upload-Funktionalität
  - Dropdown-Auswahl-Logik
- [ ] Integrationstests für Upload-Workflow
- [ ] Coverage-Report generiert durch pytest-cov

### 5. Git Workflow & Zusammenarbeit (0,5 Punkte)

- [ ] **Mindestens 2 Feature Branches** mit beschreibenden Namen (z.B. `feature/database-setup`, `feature/upload-page`)
- [ ] **Mehrere Mitwirkende**: Jeder Branch hat Commits von mindestens einem Teammitglied
- [ ] **Inkrementelle Commits** mit beschreibenden Nachrichten (>20 Zeichen)
- [ ] **Implementierungsplan** dokumentiert in `docs/implementation-plan.md`
- [ ] **LLM-Prompts** (falls verwendet) gespeichert im `docs/llm-prompts/` Ordner

### 6. Code Review (0,5 Punkte)

- [ ] Alle Features via **Pull Requests** implementiert
- [ ] PRs verwenden das bereitgestellte **PR-Beschreibungstemplate**
- [ ] Jeder PR von mindestens **einem anderen Teammitglied** reviewt
- [ ] Reviews enthalten substantielles Feedback (nicht nur "LGTM")
- [ ] Alle CI-Checks bestanden vor Merge

## 👥 Gruppenarbeit

### Team-Setup
- **Gruppengröße**: 2-4 Studenten
- **Bildung**: Selbstorganisiert oder durch Dozent zugewiesen
- **Repository**: Ein Repository pro Gruppe via GitHub Classroom

### Kollaborations-Anforderungen

1. **Implementierungsplan** (`docs/implementation-plan.md`):
   ```markdown
   # Implementierungsplan

   ## Teammitglieder
   - [Name] - [Rolle/Verantwortlichkeiten]
   - [Name] - [Rolle/Verantwortlichkeiten]

   ## Technische Entscheidung
   - [ ] FastAPI + SQLModel + SQLite (5 Punkte)
   - [ ] TinyDB (4 Punkte)

   ## Feature-Aufteilung
   | Feature | Branch | Verantwortlich | Status |
   |---------|--------|----------------|--------|
   | Datenbank-Setup | feature/database | [Name] | ✅ |
   | Upload-Seite | feature/upload | [Name] | 🔄 |

   ## Test-Strategie
   [Wie Sie 90% Abdeckung erreichen]
   ```

2. **Branch-Strategie**:
   - Minimum 2 Feature Branches (Empfehlung: 3-4)
   - Vorgeschlagene Branches:
     - `feature/database-setup` - Datenbank-Schema, Modelle, Seed-Skript
     - `feature/dropdown-selector` - Hauptseiten-Dropdown-Integration
     - `feature/upload-page` - Neue Upload-Seite mit Vorschau
     - `feature/api-endpoints` - FastAPI-Routen (falls zutreffend)

3. **Arbeitsverteilung**:
   - Jedes Teammitglied arbeitet an mindestens einem Feature Branch
   - GitHub Issues zur Aufgabenverfolgung verwenden
   - Tägliche Standups (in Issue-Kommentaren dokumentieren)

4. **LLM-Nutzung** (Optional aber empfohlen):
   - Falls Sie ChatGPT, Claude oder andere LLMs nutzen, Prompts speichern
   - Ordner erstellen: `docs/llm-prompts/`
   - Dateinamen: `JJJJ-MM-TT-feature-name.md`
   - Sowohl Prompts als auch relevante Antworten einbeziehen

## 🚀 Erste Schritte

### Schritt 1: Aufgabe annehmen & Team bilden

```bash
# Jedes Teammitglied nimmt die GitHub Classroom Aufgabe an
# Erstes Mitglied erstellt ein neues Team
# Andere Mitglieder treten dem bestehenden Team bei

# Team-Repository klonen
git clone https://github.com/hs-aalen-software-engineering/road-profile-db-TEAM-NAME.git
cd road-profile-db-TEAM-NAME
```

### Schritt 2: Aktuelle Anwendung verstehen

```bash
# Abhängigkeiten installieren
uv sync

# Aktuelle App ausführen, um zu sehen, was sie tut
uv run python -m road_profile_viewer

# Browser öffnen: http://127.0.0.1:8050/
# Mit Winkel-Eingabe spielen, um Strahlenschnitt zu sehen
```

**Code erkunden:**
- `src/road_profile_viewer/main.py` - Einstiegspunkt
- `src/road_profile_viewer/visualization.py` - Dash UI
- `src/road_profile_viewer/geometry.py` - Schnittberechnungen
- `src/road_profile_viewer/road.py` - Aktuelle Profil-Generierung

### Schritt 3: Implementierungsplan erstellen

**Team-Meeting zur Entscheidung:**
1. Welcher Ansatz? (FastAPI oder TinyDB)
2. Wer macht was? (Features Mitgliedern zuweisen)
3. Wie heißen die Branches?
4. Wie 90% Testabdeckung erreichen?

**Dokumentieren in** `docs/implementation-plan.md`

```bash
# docs-Ordner erstellen, falls nicht vorhanden
mkdir docs

# Implementierungsplan erstellen (bereitgestelltes Template verwenden)
# Plan committen
git add docs/implementation-plan.md
git commit -m "Implementierungsplan für Datenbank- und Upload-Features hinzufügen"
git push origin main
```

### Schritt 4: Entwicklungsumgebung einrichten

**Starter-Dateien erstellen:**

```bash
# 1. Pydantic-Modelle-Datei erstellen
# src/road_profile_viewer/models.py hat bereits einen Starter!

# 2. Beispiel-JSON-Format überprüfen
cat docs/example-road-profile.json
```

**Beispiel-JSON-Format** (`docs/example-road-profile.json`):
```json
{
  "name": "bergstrasse",
  "x_coordinates": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0],
  "y_coordinates": [0.0, 2.0, 5.0, 8.0, 6.0, 4.0]
}
```

### Schritt 5: Features implementieren (Team-Zusammenarbeit)

**Mitglied 1: Datenbank-Setup**

```bash
# Feature Branch erstellen
git checkout -b feature/database-setup

# Datenbank-Modul-Struktur erstellen
# Für FastAPI-Ansatz:
mkdir -p src/road_profile_viewer/database
touch src/road_profile_viewer/database/__init__.py
touch src/road_profile_viewer/database/models.py
touch src/road_profile_viewer/database/connection.py

# Für TinyDB-Ansatz:
mkdir -p src/road_profile_viewer/database
touch src/road_profile_viewer/database/__init__.py
touch src/road_profile_viewer/database/db.py

# Datenbankmodelle und Operationen implementieren
# Seed-Skript zum Einfügen des Standard-Profils hinzufügen

# Inkrementell committen
git add .
git commit -m "Datenbankmodelle und Verbindungs-Setup hinzufügen"

# Tests schreiben
git add tests/test_database.py
git commit -m "Datenbank-Operations-Tests hinzufügen (90% Abdeckung)"

# Pushen und PR erstellen
git push -u origin feature/database-setup
gh pr create --title "Datenbank-Setup mit Seed-Skript hinzufügen" \
  --body "[Bereitgestelltes PR-Template verwenden]"
```

**Mitglied 2: Dropdown-Auswahl**

```bash
git checkout -b feature/dropdown-selector

# visualization.py aktualisieren für:
# 1. Dropdown-Komponente hinzufügen
# 2. Profile aus Datenbank abrufen
# 3. Callback aktualisieren für Profil-Auswahl
# 4. Ausgewählte Profil-Daten laden

# Committen und testen
# Pushen und PR erstellen
```

**Mitglied 3: Upload-Seite**

```bash
git checkout -b feature/upload-page

# Neue Seite in Dash-App erstellen:
# 1. dcc.Upload-Komponente hinzufügen
# 2. Vorschau-Grafik hinzufügen
# 3. Umbenennungs-Texteingabe hinzufügen
# 4. Bestätigungs-Button hinzufügen
# 5. Navigation hinzufügen

# Committen, testen, PR
```

**Mitglied 4 (falls 4-Personen-Team): API-Schicht** (nur FastAPI)

```bash
git checkout -b feature/api-endpoints

# FastAPI-App erstellen:
mkdir -p src/road_profile_viewer/api
# REST-Endpunkte implementieren
# API-Tests hinzufügen

# Committen, testen, PR
```

### Schritt 6: Code Review-Prozess

**Für jeden PR:**

1. **Autor**: Sicherstellen, dass CI-Checks bestehen vor Review-Anfrage
2. **Reviewer**: PR prüfen anhand Template-Checkliste
3. **Reviewer**: Lokal testen:
   ```bash
   git fetch origin
   git checkout feature/database-setup
   uv sync
   uv run pytest --cov=src --cov-report=term-missing
   uv run python -m road_profile_viewer
   ```
4. **Reviewer**: Kommentare hinterlassen, Änderungen anfordern oder genehmigen
5. **Autor**: Feedback adressieren, Updates pushen
6. **Merge**: Nur nach Genehmigung + alle CI-Checks bestanden

### Schritt 7: Integration & Testing

```bash
# Nach Merge aller Features, End-to-End verifizieren:

# 1. Frische Installation
uv sync

# 2. Abdeckung für allen neuen Code prüfen
uv run pytest --cov=src --cov-report=html --cov-report=term
# htmlcov/index.html öffnen für detaillierte Abdeckung

# 3. Manuelle Test-Checkliste:
# - [ ] App startet ohne Fehler
# - [ ] Dropdown zeigt Standard-Profil
# - [ ] Verschiedene Profile aus Dropdown auswählbar
# - [ ] Upload-Seite erreichbar
# - [ ] Gültige JSON-Datei hochladbar
# - [ ] Vorschau-Grafik erscheint korrekt
# - [ ] Profil vor Speichern umbenennbar
# - [ ] Profil erscheint im Dropdown nach Upload
# - [ ] Ungültiges JSON zeigt Fehlermeldung
# - [ ] Datenbank persistiert nach App-Neustart

# 4. Code-Qualitätsprüfungen
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## 🔍 Bewertungsrubrik

| Kategorie | Punkte | Kriterien |
|-----------|--------|-----------|
| **Implementierung** | 2,0 | Dropdown (0,8) + Upload-Seite mit Vorschau/Umbenennung (1,2) |
| **Backend/Datenbank** | 1,5 | Schema (0,5) + CRUD-Operationen (0,5) + Seed-Skript (0,5) |
| **Testing** | 0,5 | 90%+ C1-Abdeckung für neue Features |
| **Git Workflow** | 0,5 | ≥2 Branches, klare Commits, Implementierungsplan |
| **Code Review** | 0,5 | PRs mit Template, Peer Reviews, CI bestanden |
| **BONUS: FastAPI** | +1,0 | REST API + ordentliches Error Handling + Separation of Concerns |
| **Gesamt (TinyDB)** | **5,0** | Maximal erreichbar mit TinyDB-Ansatz |
| **Gesamt (FastAPI)** | **6,0** | Begrenzt auf 5,0 (Bonus erlaubt Fehlertoleranz) |

### Automatisierte Prüfungen

GitHub Actions verifiziert automatisch:

- ✅ **Code-Qualität**: Ruff Linting, Pyright Type Checking
- ✅ **Test-Abdeckung**: pytest-cov mit 90% Schwellenwert für neuen Code
- ✅ **Git Workflow**: ≥2 Feature Branches, mehrere Autoren, Commit-Qualität
- ✅ **PR Reviews**: Alle PRs genehmigt vor Merge
- ✅ **Struktur**: Erforderliche Dateien existieren (database/, models.py, etc.)

### Manuelle Bewertung

Dozent wird:
- Ihr Repository klonen
- `uv sync` und `uv run python -m road_profile_viewer` ausführen
- Alle Features testen (Dropdown, Upload, Vorschau, Persistenz)
- Qualität des Implementierungsplans überprüfen
- Code-Architektur-Entscheidungen prüfen
- Test-Strategie verifizieren

## 📄 Erforderliche Dateien Checkliste

**Dokumentation:**
- [ ] `docs/implementation-plan.md` - Plan Ihres Teams
- [ ] `docs/example-road-profile.json` - Bereitgestelltes Beispiel (enthalten)
- [ ] `docs/llm-prompts/` - LLM-Prompts (falls verwendet)

**Code (variiert je nach Ansatz):**

**Beide Ansätze:**
- [ ] `src/road_profile_viewer/models.py` - Pydantic Validierungsmodelle
- [ ] Aktualisierte `src/road_profile_viewer/visualization.py` - Dropdown + Upload-Seite

**FastAPI-Ansatz:**
- [ ] `src/road_profile_viewer/api/main.py` - FastAPI App
- [ ] `src/road_profile_viewer/api/routes.py` - API Endpunkte
- [ ] `src/road_profile_viewer/database/models.py` - SQLModel Modelle
- [ ] `src/road_profile_viewer/database/connection.py` - DB Setup

**TinyDB-Ansatz:**
- [ ] `src/road_profile_viewer/database/db.py` - TinyDB Operationen

**Tests:**
- [ ] `tests/test_models.py` - Pydantic Validierungstests
- [ ] `tests/test_database.py` - Datenbank-Operations-Tests
- [ ] `tests/test_upload.py` - Upload-Funktionalitäts-Tests
- [ ] `tests/test_api.py` - API Endpunkt-Tests (nur FastAPI)

## ❓ Problembehandlung

### "Wie führe ich FastAPI und Dash zusammen aus?"

Bei FastAPI-Ansatz haben Sie zwei Optionen:

**Option 1: Separate Prozesse** (Entwicklung)
```bash
# Terminal 1: FastAPI Backend ausführen
uv run uvicorn road_profile_viewer.api.main:app --reload --port 8000

# Terminal 2: Dash Frontend ausführen
uv run python -m road_profile_viewer
```

**Option 2: Integriert** (Produktionsähnlich)
- Dash-App in FastAPI mit `WSGIMiddleware` mounten
- Einzelner Prozess, einzelner Port
- Komplexer aber saubereres Deployment

### "Datenbank-Datei nicht gefunden"

Stellen Sie sicher, dass Ihr Seed-Skript beim ersten Start läuft:

```python
# In Datenbank-Setup
if not Path("profiles.db").exists():
    init_database()
    seed_default_profile()
```

### "Abdeckung unter 90%"

Fokus auf Testen IHRES neuen Codes:
```bash
# Sehen, was nicht abgedeckt ist
uv run pytest --cov=src/road_profile_viewer/database --cov-report=term-missing

# Häufig nicht getestete Bereiche:
# - Error Handling-Pfade
# - Edge Cases in Validierung
# - Datenbank-Exceptions
```

### "Import-Fehler nach Hinzufügen des Datenbank-Moduls"

Stellen Sie sicher, dass `__init__.py` in allen neuen Ordnern existiert:
```
src/road_profile_viewer/database/
├── __init__.py  ← MUSS EXISTIEREN
├── models.py
└── connection.py
```

### "Dropdown aktualisiert nicht"

Prüfen Sie Ihren Dash-Callback:
```python
@app.callback(
    Output('road-graph', 'figure'),
    Input('profile-dropdown', 'value')  # Auf Dropdown-Änderungen hören
)
def update_graph(selected_profile_name):
    # Profil aus Datenbank nach Namen abrufen
    # Grafik mit neuem Profil aktualisieren
    pass
```

### "JSON-Validierung schlägt immer fehl"

Verifizieren Sie, dass Ihr Pydantic-Modell zum Beispiel-JSON passt:
```python
# Muss list[float] handhaben, nicht str
x_coordinates: list[float]  # ✅
x_coordinates: str          # ❌
```

## 📚 Technische Ressourcen

### FastAPI + SQLModel Ansatz
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [SQLModel Dokumentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Validierung](https://docs.pydantic.dev/latest/)

### TinyDB Ansatz
- [TinyDB Dokumentation](https://tinydb.readthedocs.io/)
- [TinyDB Tutorial](https://tinydb.readthedocs.io/en/latest/getting-started.html)

### Dash Multi-Page Apps
- [Dash Pages](https://dash.plotly.com/urls)
- [Dash Upload Component](https://dash.plotly.com/dash-core-components/upload)

### Testing
- [pytest Dokumentation](https://docs.pytest.org/)
- [pytest-cov Coverage](https://pytest-cov.readthedocs.io/)

## 🆘 Hilfe erhalten

1. **Dokumentation prüfen** - Links oben
2. **Implementierungsplan überprüfen** - Haben Sie dies bedacht?
3. **Im Team-Chat fragen** - Mit Teammitgliedern kollaborieren
4. **CI-Fehlermeldungen prüfen** - Sie sind detailliert!
5. **Sprechstunde** - Dozent verfügbar für Fragen
6. **GitHub Discussions** - Öffentlich fragen, anderen helfen

## 🎉 Erfolgskriterien

Ihre Aufgabe ist abgeschlossen, wenn:

- ✅ Alle Features funktionieren wie persönlich demonstriert
- ✅ Alle automatisierten CI-Checks bestanden
- ✅ Testabdeckung ≥90% für neuen Code
- ✅ Alle PRs reviewt und gemergt
- ✅ Implementierungsplan dokumentiert Ihre Entscheidungen
- ✅ Code-Qualität erfüllt Standards (Ruff, Pyright)

**Herzlichen Glückwunsch zum Aufbau einer Full-Stack-Datenbankanwendung!**

---

**Aufgabe erstellt**: 2025-11-19
**Kurs**: Software Engineering - HS Aalen
**Dozent**: Dominik Mueller
**Max. Punkte**: 5,0 (FastAPI-Ansatz kann Bonus für Fehlertoleranz verdienen)
