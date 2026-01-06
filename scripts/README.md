# Skripte zur Datenanalyse

Dieses Verzeichnis enthält Python-Skripte für die Analyse und Bereinigung von Daten aus `data/user.csv` und `data/clickstreams.parquet`.

## Skripte

### 1. clean_user_data.py
Systematische Datenbereinigung von user.csv.

**Durchgeführte Schritte:**
1. Laden und allgemeine Inspektion der Daten
2. Duplikatsprüfung und -entfernung
3. Datumskonvertierung (in-place)
4. Datumsreihenfolge-Validierung und Entfernung fehlerhafter Zeilen
5. user_gender-Bereinigung (Normalisierung und Entfernung ungültiger Werte)
6. Altersfilterung (Entfernung von Zeilen mit Alter < 18 oder > 90)
7. Analyse eindeutiger Werte in Textspalten (Identifikation seltener Werte)
8. Abhängigkeitsprüfung: first_booking_date ↔ destination_country
9. Analyse fehlender Werte

**Ausgabe:** `scripts/outputs/datenbereinigung_bericht.md`

### 2. visualize_missing_values.py
Visualisierung fehlender Werte mit missingno.

**Erstellt:**
- Matrix-Plot der fehlenden Werte
- Bar-Plot der Datenvollständigkeit pro Spalte
- Heatmap der Korrelation fehlender Werte

**Ausgaben:**
- `scripts/outputs/missing_values_matrix.png`
- `scripts/outputs/missing_values_bar.png`
- `scripts/outputs/missing_values_heatmap.png`

### 3. find_user_csv_errors.py (veraltet)
Umfassendes Fehlererkennungsskript - wurde durch `clean_user_data.py` und strukturierte Analyse ersetzt.

### 4. clean_clickstream_data.py
Systematische Datenbereinigung und Fehleranalyse von clickstreams.parquet.

**Durchgeführte Schritte:**
1. Laden und allgemeine Inspektion der Daten
2. Duplikatsprüfung (Duplikate werden beibehalten)
3. Analyse fehlender Werte
4. Analyse und Bereinigung von '-unknown-' Werten (durch NaN ersetzt)
5. Detaillierte Analyse aller Spalten
6. Visualisierung fehlender Werte mit missingno

**Hinweis:** NaN-Werte in session_action_type und session_action_detail sind legitim (technische Anfragen).

**Ausgaben:**
- `scripts/outputs/clickstreams_bereinigung_bericht.md` (Analysebericht)
- `scripts/outputs/clickstreams_missing_matrix.png` (Matrix-Plot)
- `scripts/outputs/clickstreams_missing_bar.png` (Bar-Plot)
- `data/clickstreams-filtered.parquet` (bereinigte Daten)

## Ausgabedateien

Alle Analyseergebnisse werden im Unterverzeichnis `outputs/` gespeichert:
- Textdateien und Berichte im Markdown-Format (.md)
- Visualisierungen als Bilddateien (.png, .jpg)

## Verwendung

Skripte aus dem Projektstammverzeichnis ausführen:

```bash
cd /home/runner/work/dscb310-projekt/dscb310-projekt

# Datenbereinigung und Fehleranalyse (user.csv)
python scripts/clean_user_data.py

# Visualisierung fehlender Werte (user.csv)
python scripts/visualize_missing_values.py

# Datenbereinigung und Fehleranalyse (clickstreams.parquet)
python scripts/clean_clickstream_data.py
```

## Ergebnisse

### Datenbereinigung:
- **Ursprüngliche Zeilen**: 213.451
- **Bereinigte Zeilen**: 210.721
- **Entfernte Zeilen**: 2.730 (1,28%)
  - 0 Duplikate
  - 29 Datumsreihenfolgefehler
  - 2.701 unrealistische Altersangaben
- **Korrigierte Werte**: 95.685 (user_gender normalisiert)

### Gefundene Inkonsistenzen:
- ✅ Keine Inkonsistenz zwischen first_booking_date und destination_country
- ⚠️ Einige seltene Werte in Textspalten identifiziert (potentielle Tippfehler)

### Clickstreams-Bereinigung:
- **Ursprüngliche Zeilen**: 10.567.737
- **Finale Zeilen**: 10.567.737 (keine Zeilen entfernt)
- **Ersetzte Werte**:
  - '-unknown-' in session_action_type: 1.031.170
  - '-unknown-' in session_action_detail: 1.031.141
  - '-unknown-' in session_device_type: 211.279
- **Legitime NaN-Werte**: session_action_type und session_action_detail (technische Anfragen)
