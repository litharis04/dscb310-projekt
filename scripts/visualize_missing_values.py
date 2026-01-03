"""
Skript zur Visualisierung fehlender Werte in user.csv

Dieses Skript erstellt Visualisierungen der fehlenden Werte mit missingno:
- Matrix-Plot
- Bar-Plot
- Heatmap (Korrelation fehlender Werte)

Eingabe: Bereinigte user.csv Daten (nach clean_user_data.py)
Ausgabe: PNG-Dateien in scripts/outputs/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import missingno as msno
import os

# Ausgabeverzeichnis erstellen
os.makedirs('scripts/outputs', exist_ok=True)

print("Lade und bereinigte Daten...")

# Daten laden
df_user = pd.read_csv('data/user.csv')

# Duplikate entfernen
df_user = df_user.drop_duplicates()

# Datumskonvertierung
df_user['first_active_timestamp'] = pd.to_datetime(
    df_user['first_active_timestamp'], 
    format='%Y%m%d%H%M%S', 
    errors='coerce'
)
df_user['first_active_date'] = df_user['first_active_timestamp'].dt.normalize()
df_user['account_created_date'] = pd.to_datetime(
    df_user['account_created_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)
df_user['first_booking_date'] = pd.to_datetime(
    df_user['first_booking_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)

# Datumsreihenfolge-Validierung
error1 = (df_user['first_active_date'].notna()) & \
         (df_user['account_created_date'].notna()) & \
         (df_user['first_active_date'] > df_user['account_created_date'])
error2 = (df_user['account_created_date'].notna()) & \
         (df_user['first_booking_date'].notna()) & \
         (df_user['account_created_date'] > df_user['first_booking_date'])
df_user = df_user[~(error1 | error2)]

# user_gender bereinigen
df_user['user_gender'] = df_user['user_gender'].str.lower()
df_user.loc[~df_user['user_gender'].isin(['female', 'male', 'other']), 'user_gender'] = np.nan

# Altersfilterung
df_user = df_user[~((df_user['user_age'] < 18) | (df_user['user_age'] > 90))]

print(f"Bereinigte Daten: {len(df_user)} Zeilen")

# Fehlende Werte analysieren
missing_count = df_user.isnull().sum().sum()
print(f"Fehlende Werte gesamt: {missing_count}")

if missing_count > 0:
    print("\nErstelle Visualisierungen...")
    
    # 1. Matrix-Plot
    print("  - Matrix-Plot...")
    fig = plt.figure(figsize=(12, 6))
    msno.matrix(df_user, sparkline=False, figsize=(12, 6))
    plt.title('Matrix fehlender Werte in user.csv', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig('scripts/outputs/missing_values_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    ✓ Gespeichert: scripts/outputs/missing_values_matrix.png")
    
    # 2. Bar-Plot
    print("  - Bar-Plot...")
    fig = plt.figure(figsize=(12, 6))
    msno.bar(df_user, figsize=(12, 6))
    plt.title('Vollständigkeit der Daten pro Spalte', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig('scripts/outputs/missing_values_bar.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    ✓ Gespeichert: scripts/outputs/missing_values_bar.png")
    
    # 3. Heatmap (nur wenn sinnvoll)
    if len(df_user.columns) <= 30:
        print("  - Heatmap...")
        fig = plt.figure(figsize=(12, 8))
        msno.heatmap(df_user, figsize=(12, 8))
        plt.title('Korrelation fehlender Werte', fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig('scripts/outputs/missing_values_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("    ✓ Gespeichert: scripts/outputs/missing_values_heatmap.png")
    
    print("\n✓ Alle Visualisierungen erfolgreich erstellt")
else:
    print("\nKeine fehlenden Werte zum Visualisieren vorhanden")
