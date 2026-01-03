# Skripte zur Datenanalyse

Dieses Verzeichnis enthält Python-Skripte für die Analyse und Bereinigung von Daten aus `data/user.csv`.

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

## Ausgabedateien

Alle Analyseergebnisse werden im Unterverzeichnis `outputs/` gespeichert:
- Textdateien und Berichte im Markdown-Format (.md)
- Visualisierungen als Bilddateien (.png, .jpg)

## Verwendung

Skripte aus dem Projektstammverzeichnis ausführen:

```bash
cd /home/runner/work/dscb310-projekt/dscb310-projekt

# Datenbereinigung und Fehleranalyse
python scripts/clean_user_data.py

# Visualisierung fehlender Werte
python scripts/visualize_missing_values.py
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
