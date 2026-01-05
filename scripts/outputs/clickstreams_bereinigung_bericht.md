# Datenbereinigung und Fehleranalyse: clickstreams.parquet

## 1. Daten laden und allgemeine Inspektion

- **Anzahl der Zeilen**: 10,567,737
- **Anzahl der Spalten**: 6
- **Spalten**: ['session_user_id', 'session_action', 'session_action_type', 'session_action_detail', 'session_device_type', 'time_passed_in_seconds']

- **Speicherverbrauch**: 2979.52 MB

### Datentypen

| Spalte | Datentyp |
|--------|----------|
| session_user_id | object |
| session_action | object |
| session_action_type | object |
| session_action_detail | object |
| session_device_type | object |
| time_passed_in_seconds | float64 |

## 2. Prüfung auf Duplikate

- **Anzahl der Duplikate**: 252,536
- **Prozentsatz**: 2.39%

⚠️ **Hinweis**: Duplikate werden beibehalten, da sie legitime wiederholte Aktionen sein könnten.
Falls gewünscht, können Duplikate in einer späteren Analyse entfernt werden.

## 3. Analyse fehlender Werte (vor Bereinigung)

| Spalte | Fehlend | Prozent |
|--------|---------|--------|
| session_user_id | 34,496 | 0.33% |
| session_action | 79,626 | 0.75% |
| session_action_type | 1,126,204 | 10.66% |
| session_action_detail | 1,126,204 | 10.66% |
| session_device_type | 0 | 0.0% |
| time_passed_in_seconds | 136,031 | 1.29% |

ℹ️ **Hinweis zu NaN-Werten in session_action_type und session_action_detail:**
Diese leeren Werte (None/NaN) sind **legitim** und repräsentieren technische Anfragen an die Website.
Sie werden nicht als Fehler betrachtet und bleiben unverändert.

## 4. Analyse von '-unknown-' Werten

'-unknown-' ist ein Platzhalter für unbekannte Werte und sollte durch NaN ersetzt werden.

| Spalte | '-unknown-' Anzahl | Prozent |
|--------|-------------------|--------|
| session_action_type | 1,031,170 | 9.76% |
| session_action_detail | 1,031,141 | 9.76% |
| session_device_type | 211,279 | 2.00% |

### Korrelation von '-unknown-' Werten

- session_action_type UND session_action_detail sind '-unknown-': 1,031,141
- NUR session_action_type ist '-unknown-': 29
- NUR session_action_detail ist '-unknown-': 0
- session_device_type ist '-unknown-': 211,279

## 5. Bereinigung durchführen

### 5.1 '-unknown-' durch NaN ersetzen

- **session_action_type**: 1,031,170 Werte ersetzt
- **session_action_detail**: 1,031,141 Werte ersetzt
- **session_device_type**: 211,279 Werte ersetzt

## 6. Analyse der Spalten nach Bereinigung

### session_action

- **Eindeutige Werte**: 359
- **Fehlende Werte**: 79,626

**Top 10 häufigste Werte:**

| Aktion | Anzahl | Prozent |
|--------|--------|--------|
| show | 2,768,278 | 26.20% |
| index | 843,699 | 7.98% |
| search_results | 725,226 | 6.86% |
| personalize | 706,824 | 6.69% |
| search | 536,057 | 5.07% |
| ajax_refresh_subtotal | 487,744 | 4.62% |
| update | 365,130 | 3.46% |
| similar_listings | 364,624 | 3.45% |
| social_connections | 339,000 | 3.21% |
| reviews | 320,591 | 3.03% |

### session_action_type

- **Eindeutige Werte**: 9
- **Fehlende Werte**: 2,157,374

| Typ | Anzahl | Prozent |
|-----|--------|--------|
| view | 3,560,902 | 33.70% |
| data | 2,103,770 | 19.91% |
| click | 1,996,183 | 18.89% |
| NaN | 1,126,204 | 10.66% |
| nan | 1,031,170 | 9.76% |
| submit | 623,357 | 5.90% |
| message_post | 87,103 | 0.82% |
| partner_callback | 19,132 | 0.18% |
| booking_request | 18,773 | 0.18% |
| modify | 1,139 | 0.01% |
| booking_response | 4 | 0.00% |

### session_action_detail

- **Eindeutige Werte**: 154
- **Fehlende Werte**: 2,157,345

**Top 10 häufigste Werte:**

| Detail | Anzahl | Prozent |
|--------|--------|--------|
| view_search_results | 1,776,885 | 16.81% |
| p3 | 1,376,550 | 13.03% |
| wishlist_content_update | 706,824 | 6.69% |
| user_profile | 656,839 | 6.22% |
| change_trip_characteristics | 487,744 | 4.62% |
| similar_listings | 364,624 | 3.45% |
| user_social_connections | 336,799 | 3.19% |
| update_listing | 269,779 | 2.55% |
| listing_reviews | 269,021 | 2.55% |
| dashboard | 152,952 | 1.45% |

### session_device_type

- **Eindeutige Werte**: 13
- **Fehlende Werte**: 211,279

| Gerät | Anzahl | Prozent |
|-------|--------|--------|
| Mac Desktop | 3,594,286 | 34.01% |
| Windows Desktop | 2,658,539 | 25.16% |
| iPhone | 2,105,031 | 19.92% |
| Android Phone | 839,637 | 7.95% |
| iPad Tablet | 683,414 | 6.47% |
| Android App Unknown Phone/Tablet | 273,652 | 2.59% |
| nan | 211,279 | 2.00% |
| Tablet | 139,886 | 1.32% |
| Linux Desktop | 28,373 | 0.27% |
| Chromebook | 22,348 | 0.21% |
| iPodtouch | 8,198 | 0.08% |
| Windows Phone | 2,047 | 0.02% |
| Blackberry | 979 | 0.01% |
| Opera Phone | 68 | 0.00% |

### time_passed_in_seconds

- **Fehlende Werte**: 136,031
- **Min**: 0.0
- **Max**: 1799977.0
- **Mittelwert**: 19405.81
- **Median**: 1147.00
- **Standardabweichung**: 88884.24

⚠️ **Extreme Werte (> 1.000.000 Sekunden / 11+ Tage)**: 24,755

### session_user_id

- **Eindeutige Benutzer**: 135,483
- **Fehlende Werte**: 34,496

## 7. Fehlende Werte nach Bereinigung

| Spalte | Fehlend | Prozent |
|--------|---------|--------|
| session_user_id | 34,496 | 0.33% |
| session_action | 79,626 | 0.75% |
| session_action_type | 2,157,374 | 20.41% |
| session_action_detail | 2,157,345 | 20.41% |
| session_device_type | 211,279 | 2.0% |
| time_passed_in_seconds | 136,031 | 1.29% |

## 8. Zusammenfassung

- **Ursprüngliche Anzahl der Zeilen**: 10,567,737
- **Finale Anzahl der Zeilen**: 10,567,737
- **Anzahl der Spalten**: 6

### Durchgeführte Bereinigungen:

1. ✅ '-unknown-' in session_action_type durch NaN ersetzt
2. ✅ '-unknown-' in session_action_detail durch NaN ersetzt
3. ✅ '-unknown-' in session_device_type durch NaN ersetzt

### Legitime NaN-Werte (keine Bereinigung notwendig):

- NaN in session_action_type und session_action_detail: Technische Anfragen
- Diese Werte wurden **nicht** als Fehler behandelt

### Hinweise für weitere Analyse:

- Duplikate wurden beibehalten (könnten legitime wiederholte Aktionen sein)
- Extreme Zeitwerte wurden beibehalten (zur weiteren Untersuchung)
- Fehlende session_user_id könnten auf anonyme Sitzungen hinweisen
- Fehlende session_action könnten auf unvollständige Protokollierung hinweisen

