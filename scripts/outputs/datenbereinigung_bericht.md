# Datenbereinigung: user.csv

================================================================================

## 1. Daten laden und allgemeine Inspektion

- **Anzahl Zeilen**: 213451
- **Anzahl Spalten**: 16
- **Spalten**: user_id, account_created_date, first_active_timestamp, first_booking_date, user_gender, user_age, signup_platform, signup_process, user_language, marketing_channel, marketing_provider, first_tracked_affiliate, signup_application, first_device, first_web_browser, destination_country

### Datentypen:

- `user_id`: object
- `account_created_date`: object
- `first_active_timestamp`: int64
- `first_booking_date`: object
- `user_gender`: object
- `user_age`: float64
- `signup_platform`: object
- `signup_process`: int64
- `user_language`: object
- `marketing_channel`: object
- `marketing_provider`: object
- `first_tracked_affiliate`: object
- `signup_application`: object
- `first_device`: object
- `first_web_browser`: object
- `destination_country`: object

## 2. Duplikatsprüfung

- **Anzahl Duplikate**: 0
- ✓ Keine Duplikate gefunden

## 3. Datumskonvertierung

- `first_active_timestamp` → datetime + neues Feld `first_active_date` (normalisiert)
- `account_created_date` → datetime
- `first_booking_date` → datetime

### Datumsbereiche:

- **first_active_timestamp**: 2009-03-19 04:32:55 bis 2014-06-30 23:58:24
- **first_active_date**: 2009-03-19 00:00:00 bis 2014-06-30 00:00:00
- **account_created_date**: 2010-01-01 00:00:00 bis 2014-06-30 00:00:00
- **first_booking_date**: 2010-01-02 00:00:00 bis 2015-06-29 00:00:00

## 4. Datumsreihenfolge-Validierung

Korrekte Reihenfolge: first_active_date ≤ account_created_date ≤ first_booking_date

- **Fehler gefunden**: 29
  - first_active_date > account_created_date: 0
  - account_created_date > first_booking_date: 29
- **Aktion**: Fehlerhafte Zeilen werden entfernt
- **Neue Zeilenanzahl**: 213422

## 5. user_gender Bereinigung

### Ursprüngliche Werte:

- `-unknown-`: 95685
- `MALE`: 63026
- `FEMALE`: 54429
- `OTHER`: 282

### Zulässige Werte: 'female', 'male', 'other', NaN

- **Ungültige Werte gefunden**: 95685
- **Aktion**: Ungültige Werte werden auf NaN gesetzt

### Bereinigte Werte:

- `nan`: 95685
- `male`: 63026
- `female`: 54429
- `other`: 282

## 6. Altersfilterung

Gültige Werte: 18 ≤ user_age ≤ 90

### Altersstatistik vor Filterung:

- **Minimum**: 1.00
- **Maximum**: 2014.00
- **Durchschnitt**: 49.67
- **Median**: 34.00

- **Ungültige Altersangaben**: 2701
  - Alter < 18: 158
  - Alter > 90: 2543
- **Aktion**: Zeilen mit ungültigem Alter werden entfernt
- **Neue Zeilenanzahl**: 210721

### Altersstatistik nach Filterung:

- **Minimum**: 18.00
- **Maximum**: 90.00
- **Durchschnitt**: 36.48
- **Median**: 34.00

## 7. Analyse eindeutiger Werte in Textspalten

Prüfung auf seltene Werte (< 10 Vorkommen) als mögliche Tippfehler

### user_gender

- **Anzahl eindeutiger Werte**: 4
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `nan`: 94949 (45.06%)
- `male`: 61895 (29.37%)
- `female`: 53599 (25.44%)
- `other`: 278 (0.13%)

### signup_platform

- **Anzahl eindeutiger Werte**: 3
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `web`: 150954 (71.64%)
- `affiliate`: 59222 (28.10%)
- `search_engine`: 545 (0.26%)

### signup_process

- **Anzahl eindeutiger Werte**: 17
- **Seltene Werte (< 10)**: 2

**Seltene Werte:**

- `10`: 2
- `4`: 1

**Top 10 häufigste Werte:**

- `0`: 162507 (77.12%)
- `25`: 14579 (6.92%)
- `12`: 9248 (4.39%)
- `3`: 8718 (4.14%)
- `2`: 6744 (3.20%)
- `24`: 4283 (2.03%)
- `23`: 2819 (1.34%)
- `1`: 1026 (0.49%)
- `6`: 296 (0.14%)
- `8`: 238 (0.11%)

### user_language

- **Anzahl eindeutiger Werte**: 25
- **Seltene Werte (< 10)**: 3

**Seltene Werte:**

- `ca`: 5
- `is`: 5
- `hr`: 2

**Top 10 häufigste Werte:**

- `en`: 203692 (96.66%)
- `zh`: 1623 (0.77%)
- `fr`: 1136 (0.54%)
- `es`: 902 (0.43%)
- `ko`: 738 (0.35%)
- `de`: 728 (0.35%)
- `it`: 503 (0.24%)
- `ru`: 379 (0.18%)
- `pt`: 235 (0.11%)
- `ja`: 223 (0.11%)

### marketing_channel

- **Anzahl eindeutiger Werte**: 8
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `direct`: 136034 (64.56%)
- `sem-brand`: 25679 (12.19%)
- `sem-non-brand`: 18582 (8.82%)
- `other`: 8810 (4.18%)
- `seo`: 8542 (4.05%)
- `api`: 8095 (3.84%)
- `content`: 3900 (1.85%)
- `remarketing`: 1079 (0.51%)

### marketing_provider

- **Anzahl eindeutiger Werte**: 18
- **Seltene Werte (< 10)**: 2

**Seltene Werte:**

- `wayn`: 7
- `daum`: 1

**Top 10 häufigste Werte:**

- `direct`: 135738 (64.42%)
- `google`: 50957 (24.18%)
- `other`: 12400 (5.88%)
- `craigslist`: 3406 (1.62%)
- `bing`: 2299 (1.09%)
- `facebook`: 2253 (1.07%)
- `vast`: 821 (0.39%)
- `padmapper`: 757 (0.36%)
- `facebook-open-graph`: 538 (0.26%)
- `yahoo`: 491 (0.23%)

### first_tracked_affiliate

- **Anzahl eindeutiger Werte**: 8
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `untracked`: 107916 (51.21%)
- `linked`: 45648 (21.66%)
- `omg`: 43421 (20.61%)
- `tracked-other`: 6045 (2.87%)
- `nan`: 5990 (2.84%)
- `product`: 1529 (0.73%)
- `marketing`: 139 (0.07%)
- `local ops`: 33 (0.02%)

### signup_application

- **Anzahl eindeutiger Werte**: 4
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `Web`: 180206 (85.52%)
- `iOS`: 18898 (8.97%)
- `Moweb`: 6193 (2.94%)
- `Android`: 5424 (2.57%)

### first_device

- **Anzahl eindeutiger Werte**: 9
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `Mac Desktop`: 88350 (41.93%)
- `Windows Desktop`: 71737 (34.04%)
- `iPhone`: 20601 (9.78%)
- `iPad`: 14170 (6.72%)
- `Other/Unknown`: 10560 (5.01%)
- `Android Phone`: 2775 (1.32%)
- `Android Tablet`: 1270 (0.60%)
- `Desktop (Other)`: 1183 (0.56%)
- `SmartPhone (Other)`: 75 (0.04%)

### first_web_browser

- **Anzahl eindeutiger Werte**: 52
- **Seltene Werte (< 10)**: 26

**Seltene Werte:**

- `Camino`: 9
- `TenFourFox`: 8
- `wOSBrowser`: 6
- `CoolNovo`: 6
- `Avant Browser`: 4
- `Opera Mini`: 4
- `Mozilla`: 3
- `Opera Mobile`: 2
- `SlimBrowser`: 2
- `Crazy Browser`: 2
- `Flock`: 2
- `Comodo Dragon`: 2
- `TheWorld Browser`: 2
- `OmniWeb`: 2
- `Arora`: 1

**Top 10 häufigste Werte:**

- `Chrome`: 63045 (29.92%)
- `Safari`: 44502 (21.12%)
- `Firefox`: 33186 (15.75%)
- `-unknown-`: 27056 (12.84%)
- `IE`: 20760 (9.85%)
- `Mobile Safari`: 19053 (9.04%)
- `Chrome Mobile`: 1251 (0.59%)
- `Android Browser`: 838 (0.40%)
- `AOL Explorer`: 238 (0.11%)
- `Opera`: 183 (0.09%)

### destination_country

- **Anzahl eindeutiger Werte**: 12
- **Seltene Werte (< 10)**: 0

**Top 10 häufigste Werte:**

- `NDF`: 123233 (58.48%)
- `US`: 61382 (29.13%)
- `other`: 9920 (4.71%)
- `FR`: 4960 (2.35%)
- `IT`: 2783 (1.32%)
- `GB`: 2284 (1.08%)
- `ES`: 2218 (1.05%)
- `CA`: 1404 (0.67%)
- `DE`: 1042 (0.49%)
- `NL`: 750 (0.36%)

## 8. Abhängigkeitsprüfung: first_booking_date ↔ destination_country

Erwartete Konsistenz:
- first_booking_date = NaN → destination_country = 'NDF'
- destination_country = 'NDF' → first_booking_date = NaN

### Inkonsistenzen:

- **Keine Buchung, aber destination != 'NDF'**: 0
- **Buchung vorhanden, aber destination = 'NDF'**: 0

✓ **Keine Inkonsistenzen gefunden - Daten sind konsistent**

### Statistik:

- **Zeilen ohne Buchungsdatum**: 123233
- **Zeilen mit destination_country = 'NDF'**: 123233

## 9. Analyse fehlender Werte

### Fehlende Werte pro Spalte:

| Spalte | Anzahl fehlend | Prozent |
|--------|----------------|----------|
| first_booking_date | 123233 | 58.48% |
| user_gender | 94949 | 45.06% |
| user_age | 87987 | 41.76% |
| first_tracked_affiliate | 5990 | 2.84% |

## Zusammenfassung

================================================================================

### Datenstatistik:

- **Ursprüngliche Zeilen**: 213451
- **Nach Duplikatsentfernung**: 213451
- **Nach Datumsvalidierung**: 213422
- **Nach Altersfilterung**: 210721
- **Finale Zeilenanzahl**: 210721
- **Entfernte Zeilen gesamt**: 2730 (1.28%)

### Durchgeführte Bereinigungen:

1. Duplikate entfernt: 0
2. Datumsreihenfolgefehler entfernt: 29
3. user_gender normalisiert: 95685 Werte korrigiert
4. Ungültige Altersangaben entfernt: 2701
5. Abhängigkeitsprüfung: 0 Inkonsistenzen gefunden

================================================================================
