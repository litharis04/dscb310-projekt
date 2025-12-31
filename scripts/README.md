# Skripte zur Fehleranalyse von user.csv

Dieses Verzeichnis enthält Skripte zur Analyse und Dokumentation von Fehlern in der Datei `data/user.csv`.

## Skripte

1. **find_user_csv_errors.py** - Umfassendes Fehlererkennungsskript
   - Analysiert unrealistische Altersangaben
   - Überprüft Datumsreihenfolge
   - Validiert Konsistenz von Buchung/Ziel
   - Sucht nach Tippfehlern in Textspalten

## Ausgabedateien

Alle Analyseergebnisse werden im Unterverzeichnis `outputs/` gespeichert:

- **user_csv_fehler_bericht.md** - Umfassender Bericht in Markdown-Format (Deutsch) ⭐ **HAUPTBERICHT**

## Schnellzusammenfassung der Ergebnisse

### Gefundene Fehler:
1. **Altersfehler**: 3.511 Einträge mit unrealistischem Alter
   - 2.701 Einträge mit Alter < 18 oder > 90
   - 2.771 Einträge mit Alter > 80 (zur Information)
   - 781 Einträge mit Alter > 120
2. **Datumsreihenfolgefehler**: 29 Einträge (nach Korrektur des Zeitstempelproblems)
3. **Buchungskonsistenz**: ✅ Keine Fehler gefunden
4. **Tippfehler in Texten**: ✅ Keine Tippfehler gefunden

### Hauptänderungen:
- **Altersgrenze** von > 100 auf > 90 gesenkt
- **Datumsvergleiche** werden nur auf Basis des Datums ohne Zeitstempel durchgeführt
- Dies behebt das Problem mit `account_created_date` (00:00:00 Uhrzeit)
- Variable `df` wurde in `df_user` umbenannt

### Empfehlungen:
1. Altersdaten bereinigen (unrealistische Werte durch NaN ersetzen)
2. Für die 29 Einträge mit account_created_date > first_booking_date Quelldaten überprüfen

## Verwendung

Skripte aus dem Projektstammverzeichnis ausführen:

```bash
cd /home/runner/work/dscb310-projekt/dscb310-projekt
python scripts/find_user_csv_errors.py
```

## Integration mit EDA.py

Der finalisierte Analysecode wurde zu `EDA.py` im Projektstammverzeichnis hinzugefügt und folgt dem Jupytext-Prozentformat. Dies ermöglicht die Ausführung der Analyse als Jupyter-Notebook.
