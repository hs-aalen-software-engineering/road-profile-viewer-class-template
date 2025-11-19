# Straßenprofil-Datenbank & Upload-System

> **[DE] Deutsche Version:** Sie lesen sie gerade!
> **[EN] English Version:** For full instructions in English, see [README.md](README.md)

Willkommen zur Übung "Straßenprofil-Datenbank & Upload-System"! Dies ist eine **Gruppenaufgabe**, bei der Sie eine bestehende Dash-Anwendung um Datenbank-Persistenz, Multi-Profil-Auswahl und Datei-Upload-Funktionen erweitern werden.

> **Hinweis:** Fehlermeldungen von automatisierten Prüfungen (GitHub Actions Workflows) erscheinen in **Englisch und Deutsch**.

## 📚 Lernziele

Diese Übung führt Sie in **professionelle Feature-Entwicklungs-Workflows** ein und nutzt moderne Software-Engineering-Praktiken. Sie erleben Ihren ersten vollständigen Entwicklungszyklus - eine pädagogische Vorschau auf Agile/Scrum-Methodologien, die in späteren Vorlesungen behandelt werden.

Durch diese Übung werden Sie:

1. **Professionelle Feature-Entwicklung erleben** mit ordentlichen Planungs-, Implementierungs-, Test- und Review-Zyklen
2. **Datenbanken integrieren** in Web-Anwendungen (SQLite mit FastAPI/SQLModel ODER TinyDB)
3. **REST APIs entwerfen und implementieren** (bei FastAPI-Ansatz)
4. **Multi-Page Dash-Anwendungen erstellen** mit Datei-Upload und Datenvalidierung
5. **Pydantic-Validierung anwenden** für Datenintegrität
6. **Kollaborative Entwicklung praktizieren** mit Feature Branches und Code Reviews
7. **Hohe Testabdeckung erreichen** (90%+ bei neuen Features) mit qualitätsgetriebener Entwicklung
8. **Implementierungsentscheidungen dokumentieren** und technische Planung

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
6. **Datenvalidierung** mit Pydantic-Modellen (validiert hochgeladene JSON-Dateien, z.B. Ablehnung wenn x/y-Koordinatenlisten unterschiedliche Längen haben)

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

### 1. Implementierung (1,5 Punkte)

#### Dropdown-Auswahl (0,6 Punkte)
- [ ] Dropdown-Komponente auf Hauptseite zur Auswahl von Straßenprofilen
- [ ] Dropdown listet alle verfügbaren Profile nach Namen auf
- [ ] Auswahl eines Profils aktualisiert die Visualisierung
- [ ] Standard-Profil beim App-Start vorausgewählt

#### Upload-Seite (0,9 Punkte)
- [ ] Neue Seite/Route in Dash-App erstellen (`/upload`)
- [ ] Datei-Upload-Komponente, die JSON-Dateien akzeptiert
- [ ] Vorschau-Grafik, die hochgeladenes Profil vor dem Speichern zeigt
- [ ] Texteingabe zum Umbenennen des Profils
- [ ] Bestätigungs-Button zum Speichern in Datenbank
- [ ] Erfolgs-/Fehlermeldungen nach Upload
- [ ] Navigation zwischen Hauptseite und Upload-Seite

### 2. Backend & Datenbank (1,0 Punkte)

#### Datenbank-Schema (0,3 Punkte)
- [ ] Straßenprofil-Modell mit Feldern: `id`, `name`, `x_coordinates`, `y_coordinates`
- [ ] Unique-Constraint auf Profilnamen
- [ ] Richtige Datentypen (list/array für Koordinaten)

#### Datenbank-Operationen (0,4 Punkte)
- [ ] Create (neues Profil einfügen)
- [ ] Read (alle Profile abrufen, nach Name/ID abrufen)
- [ ] Update (optional, aber empfohlen)
- [ ] Delete (optional, aber empfohlen)

#### Migration/Seed (0,3 Punkte)
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

> **Wichtig:** Sie sind **vollkommen unabhängig** in Ihrer Herangehensweise an diese Aufgabe. Die folgenden Schritte sind **Vorschläge** zur Orientierung, aber Sie können gerne Ihren eigenen Workflow entwickeln, der am besten für Ihr Team funktioniert!

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

### Schritt 3: Implementierung planen

**Halten Sie ein Team-Meeting ab, um zu entscheiden:**

1. Welcher technische Ansatz? (FastAPI oder TinyDB)
2. Wie teilen Sie die Arbeit auf? (wer macht was)
3. Wie wird Ihre Branch-Strategie aussehen?
4. Wie werden Sie 90% Testabdeckung erreichen?

**Füllen Sie das bereitgestellte Template aus:** `docs/implementation-plan.md`

Das Template ist bereits in Ihrem Repository - passen Sie es an die Bedürfnisse Ihres Teams an.

### Schritt 4: Entwicklungsumgebung einrichten

**Starter-Dateien erstellen:**

```bash
# 1. Pydantic-Modelle
# src/road_profile_viewer/models.py enthält einen STARTER-VORSCHLAG
# Sie sind komplett frei, Ihre eigenen Modelle zu entwerfen!
# Denken Sie daran: Verschieben Sie diese Datei entsprechend Ihrer gewählten Architektur
# (Auf Root-Ebene behalten ODER in database/ oder api/ Ordner verschieben)

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

### Schritt 5: Features entwickeln

**Teilen Sie die Arbeit unter den Teammitgliedern auf.** Erstellen Sie Feature Branches für jede Hauptkomponente. Hier sind einige vorgeschlagene Arbeitspakete, aber Sie können auch anders organisieren:

- Datenbank-Setup und Schema
- Dropdown-Selector-Integration
- Upload-Seite mit Validierung
- API-Endpunkte (falls FastAPI verwendet wird)
- Testing und Coverage

**Beispiel-Workflow für ein Feature:**

```bash
# Erstellen Sie Ihren Feature Branch
git checkout -b feature/ihr-feature-name

# Implementieren Sie Ihr Feature
# Schreiben Sie Tests während der Entwicklung
# Committen Sie inkrementell mit aussagekräftigen Nachrichten

# Pushen und PR mit dem Template erstellen
git push -u origin feature/ihr-feature-name
gh pr create
```

**Denken Sie daran:** Jedes Feature sollte Tests haben, Code-Qualitätsstandards folgen und durch Code Review gehen, bevor es gemergt wird.

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
| **Implementierung** | 1,5 | Dropdown (0,6) + Upload-Seite mit Vorschau/Umbenennung (0,9) |
| **Backend/Datenbank** | 1,0 | Schema (0,3) + CRUD-Operationen (0,4) + Seed-Skript (0,3) |
| **Testing** | 0,5 | 90%+ C1-Abdeckung für neue Features |
| **Git Workflow** | 0,5 | ≥2 Branches, klare Commits, Implementierungsplan |
| **Code Review** | 0,5 | PRs mit Template, Peer Reviews, CI bestanden |
| **BONUS: FastAPI** | +1,0 | REST API + ordentliches Error Handling + Separation of Concerns |
| **Gesamt (TinyDB)** | **4,0** | Maximal erreichbar mit TinyDB-Ansatz |
| **Gesamt (FastAPI)** | **5,0** | Begrenzt auf 5,0 (Bonus erlaubt Fehlertoleranz bis 6,0) |

### Automatisierte Prüfungen

GitHub Actions verifiziert automatisch:

- ✅ **Code-Qualität**: Ruff Linting, Pyright Type Checking
- ✅ **Test-Abdeckung**: pytest-cov mit 90% Schwellenwert für neuen Code
- ✅ **Git Workflow**: ≥2 Feature Branches, mehrere Autoren, Commit-Qualität
- ✅ **PR Reviews**: Alle PRs genehmigt vor Merge
- ✅ **Struktur**: Erforderliche Dateien existieren (database/, models.py, etc.)

> **⚠️ Wichtiger Hinweis zu automatisierten Prüfungen:**
>
> Die GitHub Actions Workflows dienen **nur zur Orientierung** und geben hilfreiche Rückmeldungen während der Entwicklung. Jedoch:
>
> - **Die finale Bewertung erfolgt ausschließlich durch den Dozenten**, nicht durch automatisierte Checks
> - Die Checks sind bewusst offen formuliert und decken möglicherweise nicht alle gültigen Lösungsansätze ab
> - **Blockieren Sie sich nicht**, wenn ein Check fehlschlägt, Sie aber eine gültige alternative Lösung haben - dokumentieren Sie Ihren Ansatz im Implementierungsplan
> - Wenn automatisierte Checks nicht zu Ihren Designentscheidungen passen, ist das in Ordnung! Der Dozent bewertet auf Basis von Korrektheit, nicht Check-Konformität
> - Fokussieren Sie sich darauf, eine funktionierende, gut getestete Anwendung zu bauen, anstatt jede automatisierte Regel zu erfüllen

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
