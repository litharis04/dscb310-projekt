# Fehleranalyse-Bericht für user.csv

================================================================================

## 1. Altersanalyse (user_age)

### Altersstatistik:

- **Minimalalter:** 1.0
- **Maximalalter:** 2014.0
- **Durchschnittsalter:** 49.67
- **Medianalter:** 34.0

### Benutzer mit unrealistischem Alter (< 18 oder > 90): **2701**

Beispiele:

- user_id: `3qsa4lo7eg`, Alter: 5.0
- user_id: `v2x0ms9c62`, Alter: 2014.0
- user_id: `9ouah6tc30`, Alter: 104.0
- user_id: `rzhouzy2ok`, Alter: 5.0
- user_id: `dc3udjfdij`, Alter: 105.0
- user_id: `5yatk13sko`, Alter: 5.0
- user_id: `ixv5186g1h`, Alter: 95.0
- user_id: `593gkcul8c`, Alter: 5.0
- user_id: `umf1wdk9uc`, Alter: 2014.0
- user_id: `tu2iorbez0`, Alter: 5.0

### Benutzer mit Alter > 80: **2771**

Beispiele:

- user_id: `v2x0ms9c62`, Alter: 2014.0
- user_id: `9ouah6tc30`, Alter: 104.0
- user_id: `dc3udjfdij`, Alter: 105.0
- user_id: `ixv5186g1h`, Alter: 95.0
- user_id: `umf1wdk9uc`, Alter: 2014.0
- user_id: `kqf8b3ta98`, Alter: 94.0
- user_id: `m82epwn7i8`, Alter: 2014.0
- user_id: `2th813zdx7`, Alter: 2013.0
- user_id: `qc9se9qucz`, Alter: 105.0
- user_id: `3amf04n3o3`, Alter: 2014.0

### Benutzer mit extremem Alter (< 0 oder > 120): **781**

Beispiele:

- user_id: `v2x0ms9c62`, Alter: 2014.0
- user_id: `umf1wdk9uc`, Alter: 2014.0
- user_id: `m82epwn7i8`, Alter: 2014.0
- user_id: `2th813zdx7`, Alter: 2013.0
- user_id: `3amf04n3o3`, Alter: 2014.0
- user_id: `6vpmryt377`, Alter: 2014.0
- user_id: `uxy91xb5p2`, Alter: 2014.0
- user_id: `bno0vva4uz`, Alter: 2014.0
- user_id: `h3rrmak4tu`, Alter: 2014.0
- user_id: `fou0j7fhnm`, Alter: 2014.0

## 2. Datumsanalyse

### Datumsbereiche:

- **first_active_date:** 2009-03-19 04:32:55 bis 2014-06-30 23:58:24
- **account_created_date:** 2010-01-01 00:00:00 bis 2014-06-30 00:00:00
- **first_booking_date:** 2010-01-02 00:00:00 bis 2015-06-29 00:00:00

### Zukünftige Datumsangaben:

- **first_active_date in der Zukunft:** 0
- **account_created_date in der Zukunft:** 0
- **first_booking_date in der Zukunft:** 0

### Datumsangaben vor 2000:

- **first_active_date vor 2000:** 0
- **account_created_date vor 2000:** 0
- **first_booking_date vor 2000:** 0

## 3. Fehler in der Datumsreihenfolge

**Hinweis:** Datumsvergleiche werden nur auf Basis des Datums ohne Zeitstempel durchgeführt.

### Zeilen mit first_active_date > account_created_date: **0**


### Zeilen mit account_created_date > first_booking_date: **29**

Beispiele (erste 10):

- user_id: `4ft3gnwmtx`, created: 2010-09-28, booking: 2010-08-02
- user_id: `87mebub9p4`, created: 2010-09-14, booking: 2010-02-18
- user_id: `swrvyedlsp`, created: 2010-05-30, booking: 2010-03-17
- user_id: `adq42kzmnv`, created: 2010-12-23, booking: 2010-04-06
- user_id: `176898y1ju`, created: 2011-03-28, booking: 2010-04-15
- user_id: `8lfswd0jil`, created: 2010-05-20, booking: 2010-05-16
- user_id: `bdm2l1azts`, created: 2012-04-20, booking: 2011-05-18
- user_id: `7tik9xpgdw`, created: 2011-05-03, booking: 2010-06-29
- user_id: `ujd35792qs`, created: 2011-07-15, booking: 2010-09-20
- user_id: `y20qfefzz8`, created: 2011-04-29, booking: 2010-08-03

### Zeilen mit first_active_date > first_booking_date: **0**


## 4. Konsistenz von first_booking_date und destination_country

### Benutzer ohne Buchungsdatum: **124543**

### Benutzer ohne Buchung, aber destination != NDF: **0**

✓ Keine Fehler gefunden

### Benutzer mit Buchung, aber destination = NDF: **0**

✓ Keine Fehler gefunden

## 5. Analyse der Textspalten (Suche nach Tippfehlern)

### user_gender: 4 eindeutige Werte

Top 15 Werte:

- `-unknown-`: 95688
- `MALE`: 63041
- `FEMALE`: 54440
- `OTHER`: 282

### signup_platform: 3 eindeutige Werte

Top 15 Werte:

- `web`: 152897
- `affiliate`: 60008
- `search_engine`: 546

### signup_process: 17 eindeutige Werte

Top 15 Werte:

- `0`: 164739
- `25`: 14659
- `12`: 9329
- `3`: 8822
- `2`: 6881
- `24`: 4328
- `23`: 2835
- `1`: 1047
- `6`: 301
- `8`: 240
- `21`: 196
- `5`: 36
- `20`: 14
- `16`: 11
- `15`: 10

**Seltene Werte (Anzahl ≤ 5):** 2

- `10`: 2
- `4`: 1

### user_language: 25 eindeutige Werte

Top 15 Werte:

- `en`: 206314
- `zh`: 1632
- `fr`: 1172
- `es`: 915
- `ko`: 747
- `de`: 732
- `it`: 514
- `ru`: 389
- `pt`: 240
- `ja`: 225
- `sv`: 122
- `nl`: 97
- `tr`: 64
- `da`: 58
- `pl`: 54

**Seltene Werte (Anzahl ≤ 5):** 3

- `ca`: 5
- `is`: 5
- `hr`: 2

### marketing_channel: 8 eindeutige Werte

Top 15 Werte:

- `direct`: 137727
- `sem-brand`: 26045
- `sem-non-brand`: 18844
- `other`: 8961
- `seo`: 8663
- `api`: 8167
- `content`: 3948
- `remarketing`: 1096

### marketing_provider: 18 eindeutige Werte

Top 15 Werte:

- `direct`: 137426
- `google`: 51693
- `other`: 12549
- `craigslist`: 3471
- `bing`: 2328
- `facebook`: 2273
- `vast`: 829
- `padmapper`: 768
- `facebook-open-graph`: 545
- `yahoo`: 496
- `gsp`: 453
- `meetup`: 347
- `email-marketing`: 166
- `naver`: 52
- `baidu`: 29

**Seltene Werte (Anzahl ≤ 5):** 1

- `daum`: 1

### first_tracked_affiliate: 7 eindeutige Werte

Top 15 Werte:

- `untracked`: 109232
- `linked`: 46287
- `omg`: 43982
- `tracked-other`: 6156
- `product`: 1556
- `marketing`: 139
- `local ops`: 34

### signup_application: 4 eindeutige Werte

Top 15 Werte:

- `Web`: 182717
- `iOS`: 19019
- `Moweb`: 6261
- `Android`: 5454

### first_device: 9 eindeutige Werte

Top 15 Werte:

- `Mac Desktop`: 89600
- `Windows Desktop`: 72716
- `iPhone`: 20759
- `iPad`: 14339
- `Other/Unknown`: 10667
- `Android Phone`: 2803
- `Android Tablet`: 1292
- `Desktop (Other)`: 1199
- `SmartPhone (Other)`: 76

### first_web_browser: 52 eindeutige Werte

Top 15 Werte:

- `Chrome`: 63845
- `Safari`: 45169
- `Firefox`: 33655
- `-unknown-`: 27266
- `IE`: 21068
- `Mobile Safari`: 19274
- `Chrome Mobile`: 1270
- `Android Browser`: 851
- `AOL Explorer`: 245
- `Opera`: 188
- `Silk`: 124
- `Chromium`: 73
- `BlackBerry Browser`: 53
- `Maxthon`: 46
- `Apple Mail`: 36

**Seltene Werte (Anzahl ≤ 5):** 22

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

### destination_country: 12 eindeutige Werte

Top 15 Werte:

- `NDF`: 124543
- `US`: 62376
- `other`: 10094
- `FR`: 5023
- `IT`: 2835
- `GB`: 2324
- `ES`: 2249
- `CA`: 1428
- `DE`: 1061
- `NL`: 762
- `AU`: 539
- `PT`: 217

## 6. Analyse fehlender Werte

Fehlende Werte nach Spalte:

- **first_booking_date:** 124543 (58.35%)
- **user_age:** 87990 (41.22%)
- **first_tracked_affiliate:** 6065 (2.84%)
- **first_booking_date_ts:** 124543 (58.35%)
- **first_booking_date_dt:** 124543 (58.35%)

## 7. Analyse leerer Zeichenketten

✓ Keine leeren Zeichenketten gefunden

## 8. Zusammenfassung aller gefundenen Fehler

================================================================================

| Fehlertyp | Anzahl |
|-----------|--------|
| Unrealistisches Alter (< 18 oder > 90) | 2701 |
| Alter > 80 (Information) | 2771 |
| Extremes Alter (< 0 oder > 120) | 781 |
| account_created_date > first_booking_date | 29 |

**Gesamtzahl der Fehler (mit möglichen Überschneidungen):** 3511

================================================================================
