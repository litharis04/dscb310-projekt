# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: dabi-projekt
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import missingno as msno
import plotly.express as px 
import matplotlib.pyplot as plt
from IPython.display import display
from datetime import datetime

# %% [markdown]
# # Datenaufbereitung und Fehleranalyse: user.csv
#
# Dieser Notebook führt eine systematische Datenbereinigung und Fehleranalyse durch:
# 1. Laden und allgemeine Inspektion der Daten
# 2. Prüfung und Entfernung von Duplikaten
# 3. Konvertierung von Datumsangaben
# 4. Prüfung und Korrektur der Datumsreihenfolge
# 5. Bereinigung von user_gender
# 6. Filterung unrealistischer Altersangaben
# 7. Prüfung eindeutiger Werte und seltener Einträge
# 8. Analyse der Abhängigkeit zwischen first_booking_date und destination_country
# 9. Visualisierung fehlender Werte

# %% [markdown]
# ## 1. Daten laden und allgemeine Inspektion

# %%
# Daten laden
df_user = pd.read_csv('data/user.csv')

print(f"Anzahl der Zeilen: {len(df_user)}")
print(f"Anzahl der Spalten: {len(df_user.columns)}")
print(f"\nSpalten: {list(df_user.columns)}")

# %%
df_user.head(10)

# %%
df_user.info()

# %%
# Grundlegende Statistiken
df_user.describe()

# %% [markdown]
# ## 2. Prüfung auf Duplikate

# %%
# Duplikate prüfen
anzahl_duplikate = df_user.duplicated().sum()
print(f"Anzahl der Duplikate: {anzahl_duplikate}")

if anzahl_duplikate > 0:
    print(f"\nBeispiele für Duplikate:")
    display(df_user[df_user.duplicated(keep=False)].head(10))
    
    # Duplikate entfernen
    df_user = df_user.drop_duplicates()
    print(f"\n✓ {anzahl_duplikate} Duplikate wurden entfernt")
    print(f"Neue Anzahl der Zeilen: {len(df_user)}")
else:
    print("✓ Keine Duplikate gefunden")

# %% [markdown]
# ## 3. Konvertierung von Datumsangaben
#
# Die Datumsfelder werden in datetime-Format konvertiert:
# - `first_active_timestamp` → datetime (in-place) + neues Feld `first_active_date` (nur Datum)
# - `account_created_date` → datetime (in-place)
# - `first_booking_date` → datetime (in-place)

# %%
# Datumskonvertierung
print("Datumskonvertierung wird durchgeführt...\n")

# first_active_timestamp konvertieren und first_active_date erstellen
df_user['first_active_timestamp'] = pd.to_datetime(
    df_user['first_active_timestamp'], 
    format='%Y%m%d%H%M%S', 
    errors='coerce'
)
df_user['first_active_date'] = df_user['first_active_timestamp'].dt.normalize()

# account_created_date konvertieren
df_user['account_created_date'] = pd.to_datetime(
    df_user['account_created_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)

# first_booking_date konvertieren
df_user['first_booking_date'] = pd.to_datetime(
    df_user['first_booking_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)

print("✓ Datumskonvertierung abgeschlossen\n")
print("Datumsbereiche:")
print(f"  first_active_timestamp: {df_user['first_active_timestamp'].min()} bis {df_user['first_active_timestamp'].max()}")
print(f"  first_active_date: {df_user['first_active_date'].min()} bis {df_user['first_active_date'].max()}")
print(f"  account_created_date: {df_user['account_created_date'].min()} bis {df_user['account_created_date'].max()}")
print(f"  first_booking_date: {df_user['first_booking_date'].min()} bis {df_user['first_booking_date'].max()}")

# %% [markdown]
# ## 4. Prüfung der Datumsreihenfolge
#
# Korrekte Reihenfolge: first_active_date ≤ account_created_date ≤ first_booking_date
#
# Zeilen mit Fehlern werden identifiziert und entfernt.

# %%
# Anzahl der Zeilen vor der Bereinigung
zeilen_vorher = len(df_user)

# Fehlerhafte Datumsreihenfolge identifizieren
# first_active_date > account_created_date
fehler1 = (df_user['first_active_date'].notna()) & \
          (df_user['account_created_date'].notna()) & \
          (df_user['first_active_date'] > df_user['account_created_date'])

# account_created_date > first_booking_date  
fehler2 = (df_user['account_created_date'].notna()) & \
          (df_user['first_booking_date'].notna()) & \
          (df_user['account_created_date'] > df_user['first_booking_date'])

# Kombinierte Fehlermaske
datum_fehler = fehler1 | fehler2

anzahl_datum_fehler = datum_fehler.sum()
print(f"Anzahl der Zeilen mit fehlerhafter Datumsreihenfolge: {anzahl_datum_fehler}")
print(f"  - first_active_date > account_created_date: {fehler1.sum()}")
print(f"  - account_created_date > first_booking_date: {fehler2.sum()}")

if anzahl_datum_fehler > 0:
    print(f"\nBeispiele für fehlerhafte Datumsreihenfolge:")
    display(df_user[datum_fehler][['user_id', 'first_active_date', 'account_created_date', 'first_booking_date']].head(10))
    
    # Fehlerhafte Zeilen entfernen
    df_user = df_user[~datum_fehler]
    print(f"\n✓ {anzahl_datum_fehler} Zeilen mit fehlerhafter Datumsreihenfolge wurden entfernt")
    print(f"Anzahl der Zeilen: {zeilen_vorher} → {len(df_user)}")
else:
    print("✓ Keine Fehler in der Datumsreihenfolge gefunden")

# %% [markdown]
# ## 5. Bereinigung von user_gender
#
# Zulässige Werte: 'female', 'male', 'other', NaN
#
# Alle anderen Werte werden auf NaN gesetzt.

# %%
# Aktuelle eindeutige Werte in user_gender
print("Eindeutige Werte in user_gender:")
print(df_user['user_gender'].value_counts(dropna=False))
print()

# Zulässige Werte definieren
zulaessige_gender = ['female', 'male', 'other', 'FEMALE', 'MALE', 'OTHER']

# Inkonsistenzen identifizieren
ungueltige_gender = ~df_user['user_gender'].isin(zulaessige_gender) & df_user['user_gender'].notna()
anzahl_ungueltige = ungueltige_gender.sum()

print(f"Anzahl der Zeilen mit ungültigem user_gender: {anzahl_ungueltige}")

if anzahl_ungueltige > 0:
    print("\nBeispiele für ungültige Werte:")
    display(df_user[ungueltige_gender][['user_id', 'user_gender']].head(10))

# Normalisierung: Groß-/Kleinschreibung vereinheitlichen
df_user['user_gender'] = df_user['user_gender'].str.lower()

# Ungültige Werte auf NaN setzen
df_user.loc[~df_user['user_gender'].isin(['female', 'male', 'other']), 'user_gender'] = np.nan

print(f"\n✓ user_gender wurde bereinigt")
print("\nBereinigte Werte:")
print(df_user['user_gender'].value_counts(dropna=False))

# %% [markdown]
# ## 6. Filterung unrealistischer Altersangaben
#
# Zeilen mit user_age < 18 oder > 90 werden entfernt.

# %%
# Anzahl der Zeilen vor der Bereinigung
zeilen_vorher = len(df_user)

# Altersstatistik vor der Bereinigung
print("Altersstatistik vor der Bereinigung:")
print(df_user['user_age'].describe())
print()

# Unrealistische Altersangaben identifizieren
alter_zu_jung = df_user['user_age'] < 18
alter_zu_alt = df_user['user_age'] > 90
unrealistisches_alter = alter_zu_jung | alter_zu_alt

anzahl_unrealistisch = unrealistisches_alter.sum()
print(f"Anzahl der Zeilen mit unrealistischem Alter: {anzahl_unrealistisch}")
print(f"  - Alter < 18: {alter_zu_jung.sum()}")
print(f"  - Alter > 90: {alter_zu_alt.sum()}")

if anzahl_unrealistisch > 0:
    print(f"\nBeispiele für unrealistische Altersangaben:")
    display(df_user[unrealistisches_alter][['user_id', 'user_age', 'account_created_date']].head(10))
    
    # Zeilen mit unrealistischem Alter entfernen
    df_user = df_user[~unrealistisches_alter]
    print(f"\n✓ {anzahl_unrealistisch} Zeilen mit unrealistischem Alter wurden entfernt")
    print(f"Anzahl der Zeilen: {zeilen_vorher} → {len(df_user)}")
else:
    print("✓ Keine unrealistischen Altersangaben gefunden")

print("\nAltersstatistik nach der Bereinigung:")
print(df_user['user_age'].describe())

# %% [markdown]
# ## 7. Prüfung eindeutiger Werte in Textspalten
#
# Seltene Werte (< 10 Vorkommen) werden auf mögliche Tippfehler untersucht.

# %%
# Zu prüfende Textspalten
text_spalten = [
    'user_gender', 'signup_platform', 'signup_process', 'user_language',
    'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
    'signup_application', 'first_device', 'first_web_browser', 'destination_country'
]

print("Analyse der Textspalten auf seltene Werte (< 10 Vorkommen):\n")
print("=" * 80)

for spalte in text_spalten:
    print(f"\n{spalte}:")
    print("-" * 80)
    
    werte_haeufigkeit = df_user[spalte].value_counts(dropna=False)
    print(f"Anzahl eindeutiger Werte: {len(werte_haeufigkeit)}")
    
    # Seltene Werte (< 10 Vorkommen)
    seltene_werte = werte_haeufigkeit[werte_haeufigkeit < 10]
    
    if len(seltene_werte) > 0:
        print(f"⚠️  Seltene Werte (< 10 Vorkommen): {len(seltene_werte)}")
        print("\nTop 15 seltene Werte:")
        for wert, anzahl in seltene_werte.head(15).items():
            print(f"  - '{wert}': {anzahl}")
    else:
        print("✓ Keine seltenen Werte gefunden")
    
    # Top 10 häufigste Werte
    print(f"\nTop 10 häufigste Werte:")
    for wert, anzahl in werte_haeufigkeit.head(10).items():
        anteil = (anzahl / len(df_user)) * 100
        print(f"  - '{wert}': {anzahl} ({anteil:.2f}%)")

# %% [markdown]
# ## 8. Analyse der Abhängigkeit: first_booking_date ↔ destination_country
#
# Zweiseitige Prüfung:
# - Wenn first_booking_date = NaN → destination_country sollte 'NDF' sein
# - Wenn destination_country = 'NDF' → first_booking_date sollte NaN sein

# %%
print("Analyse der Abhängigkeit zwischen first_booking_date und destination_country\n")
print("=" * 80)

# Fall 1: Keine Buchung (first_booking_date = NaN), aber destination != NDF
keine_buchung_aber_destination = (df_user['first_booking_date'].isna()) & \
                                  (df_user['destination_country'] != 'NDF')
anzahl_fall1 = keine_buchung_aber_destination.sum()

print(f"\n1. Zeilen ohne Buchungsdatum, aber destination_country != 'NDF': {anzahl_fall1}")

if anzahl_fall1 > 0:
    print("   ❌ INKONSISTENZ gefunden!")
    print("\n   Beispiele:")
    display(df_user[keine_buchung_aber_destination][['user_id', 'first_booking_date', 'destination_country']].head(10))
else:
    print("   ✓ Keine Inkonsistenz")

# Fall 2: Buchung vorhanden (first_booking_date != NaN), aber destination = NDF
buchung_aber_ndf = (df_user['first_booking_date'].notna()) & \
                   (df_user['destination_country'] == 'NDF')
anzahl_fall2 = buchung_aber_ndf.sum()

print(f"\n2. Zeilen mit Buchungsdatum, aber destination_country = 'NDF': {anzahl_fall2}")

if anzahl_fall2 > 0:
    print("   ❌ INKONSISTENZ gefunden!")
    print("\n   Beispiele:")
    display(df_user[buchung_aber_ndf][['user_id', 'first_booking_date', 'destination_country']].head(10))
else:
    print("   ✓ Keine Inkonsistenz")

# Zusammenfassung
print(f"\n" + "=" * 80)
print("ZUSAMMENFASSUNG:")
anzahl_inkonsistenzen = anzahl_fall1 + anzahl_fall2

if anzahl_inkonsistenzen == 0:
    print("✓ Die Abhängigkeit zwischen first_booking_date und destination_country ist konsistent")
else:
    print(f"❌ Insgesamt {anzahl_inkonsistenzen} inkonsistente Zeilen gefunden")

# Statistik
keine_buchung_gesamt = df_user['first_booking_date'].isna().sum()
ndf_gesamt = (df_user['destination_country'] == 'NDF').sum()

print(f"\nStatistik:")
print(f"  - Zeilen ohne Buchungsdatum: {keine_buchung_gesamt}")
print(f"  - Zeilen mit destination_country = 'NDF': {ndf_gesamt}")

# %% [markdown]
# ## 9. Visualisierung fehlender Werte

# %%
# Fehlende Werte pro Spalte
print("Fehlende Werte pro Spalte:\n")
fehlende_werte = df_user.isnull().sum()
fehlende_werte_prozent = (fehlende_werte / len(df_user)) * 100

fehlende_df = pd.DataFrame({
    'Spalte': fehlende_werte.index,
    'Anzahl fehlend': fehlende_werte.values,
    'Prozent fehlend': fehlende_werte_prozent.values
})
fehlende_df = fehlende_df[fehlende_df['Anzahl fehlend'] > 0].sort_values('Anzahl fehlend', ascending=False)

if len(fehlende_df) > 0:
    display(fehlende_df)
else:
    print("✓ Keine fehlenden Werte gefunden")

# %%
# Visualisierung mit missingno - Matrix
if fehlende_df['Anzahl fehlend'].sum() > 0:
    print("Visualisierung fehlender Werte mit missingno:")
    
    # Matrix-Plot
    fig = plt.figure(figsize=(12, 6))
    msno.matrix(df_user, sparkline=False, figsize=(12, 6))
    plt.title('Matrix fehlender Werte in user.csv', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig('scripts/outputs/missing_values_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Matrix-Plot gespeichert: scripts/outputs/missing_values_matrix.png")
    
    # Bar-Plot
    fig = plt.figure(figsize=(12, 6))
    msno.bar(df_user, figsize=(12, 6))
    plt.title('Vollständigkeit der Daten pro Spalte', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig('scripts/outputs/missing_values_bar.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Bar-Plot gespeichert: scripts/outputs/missing_values_bar.png")
    
    # Heatmap-Plot (falls sinnvoll)
    if len(df_user.columns) <= 30:
        fig = plt.figure(figsize=(12, 8))
        msno.heatmap(df_user, figsize=(12, 8))
        plt.title('Korrelation fehlender Werte', fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig('scripts/outputs/missing_values_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ Heatmap gespeichert: scripts/outputs/missing_values_heatmap.png")
else:
    print("Keine fehlenden Werte zum Visualisieren vorhanden")

# %% [markdown]
# ## Zusammenfassung der Datenbereinigung
#
# Nach allen Bereinigungsschritten:

# %%
print("=" * 80)
print("FINALE DATENÜBERSICHT")
print("=" * 80)
print(f"\nAnzahl der Zeilen nach Bereinigung: {len(df_user)}")
print(f"Anzahl der Spalten: {len(df_user.columns)}")

print(f"\nDatentypen:")
df_user.info()

print(f"\nStatistische Zusammenfassung:")
df_user.describe()
