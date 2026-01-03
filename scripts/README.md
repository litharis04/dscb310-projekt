# Skripte-Verzeichnis

Dieses Verzeichnis enthält Python-Skripte für explorative Datenanalysen und Datenverarbeitung.

## Ausgabedateien

Alle Analyseergebnisse werden im Unterverzeichnis `outputs/` gespeichert:
- Textdateien und Berichte im Markdown-Format (.md)
- Visualisierungen als Bilddateien (.png, .jpg)

## Veraltete Skripte

Die folgenden Skripte sind nicht mehr relevant und wurden durch die Hauptanalyse in `EDA.py` ersetzt:

1. ~~**find_user_csv_errors.py**~~ - Wurde durch strukturierte Analyse in EDA.py ersetzt
   - Die ursprüngliche Fehleranalyse wurde vollständig in `EDA.py` integriert
   - Die neue Version folgt einem systematischeren Ansatz mit Datenbereinigung

## Hauptanalyse

Die vollständige Datenaufbereitung und Fehleranalyse für `data/user.csv` befindet sich in:
- **`EDA.py`** (Projektstammverzeichnis) - Hauptanalysedatei im Jupytext-Prozentformat
- **`EDA.ipynb`** (Projektstammverzeichnis) - Automatisch generiertes Jupyter Notebook

### Analyseschritte in EDA.py:
1. Laden und allgemeine Inspektion der Daten
2. Prüfung und Entfernung von Duplikaten
3. Konvertierung von Datumsangaben
4. Prüfung und Korrektur der Datumsreihenfolge
5. Bereinigung von user_gender
6. Filterung unrealistischer Altersangaben (< 18 oder > 90)
7. Prüfung eindeutiger Werte und seltener Einträge
8. Analyse der Abhängigkeit zwischen first_booking_date und destination_country
9. Visualisierung fehlender Werte

## Verwendung

Neue Analyseskripte sollten:
1. In diesem Verzeichnis erstellt werden
2. Klare, beschreibende Namen haben (z.B. `analyze_geo_data.py`)
3. Ausgaben in `outputs/` speichern
4. Nach erfolgreicher Validierung in `EDA.py` integriert werden
