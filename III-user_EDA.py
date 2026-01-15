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
# TO DO: Добавить сезонность
# TO DO: Скомпоновать некоторые графики / изменить размер
# TO DO: Поработать с цветами
# TO DO: Больше комментариев и описаний в Markdown
# TO DO: DataFrame.melt() для упрощения `booked_*` графиков
# TO DO: user_gender и user_age в один столбец (с помощью melt?)

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from IPython.display import display

# %%
df_user_raw = pd.read_parquet('data/user_filtered.parquet')

# %%
df_user = df_user_raw.copy()

# %%
df_user.head(10)

# %% [markdown]
# # 1. Gesamtentwicklung

# %% [markdown]
# ## 1.1. Kumulative Buchungen

# %%
# Neue Spalten für kumulative Zählungen
df_user.sort_values('account_created_date', inplace=True)
df_user['total_users_cumulative'] = range(1, len(df_user) + 1)
df_user['booked'] = df_user['destination_country'] != 'NDF'
df_user['booked_cumulative'] = df_user['booked'].cumsum()

# %%
# Kumulative Anzahl neuer Benutzer über die Zeit
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_user['account_created_date'], df_user['total_users_cumulative'], label='Gesamtanzahl Benutzer')
ax.plot(df_user['account_created_date'], df_user['booked_cumulative'], label='Benutzer mit Buchung')
ax.set(
    title='Kumulative Anzahl neuer Benutzer',
    xlabel='Datum',
    ylabel='Anzahl Benutzer'
)
ax.legend()
plt.show()

# %%
# Detaiiliertere Statistiken nach Zielort
for destination in df_user['destination_country'].unique():
    if destination != 'NDF':
        df_user[f'booked_{destination}'] = df_user['destination_country'] == destination
        df_user[f'booked_{destination}_cumulative'] = df_user[f'booked_{destination}'].cumsum()

# Separater Zähler für Buchungen außerhalb der USA, da diese häufig sind
df_user['booked_non_US'] = (df_user['destination_country'] != 'US') & (df_user['destination_country'] != 'NDF')
df_user['booked_non_US_cumulative'] = df_user['booked_non_US'].cumsum()

# %%
# Visualisierung der kumulativen Buchungen nach Zielort (USA vs. Nicht-USA)
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_user['account_created_date'], df_user['booked_US_cumulative'], label='Benutzer mit Buchung in den USA')
ax.plot(df_user['account_created_date'], df_user['booked_non_US_cumulative'], label='Benutzer mit Buchung außerhalb der USA')
ax.set(
    title='Kumulative Anzahl neuer Benutzer mit Buchung nach Zielort',
    xlabel='Datum',
    ylabel='Gesamtanzahl Benutzer mit Buchung'
)
ax.legend()
plt.show()

# %%
# Visualisierung der kumulativen Buchungen nach Zielort (außerhalb der USA)
fig, ax = plt.subplots(figsize=(12, 6))
for destination in df_user['destination_country'].unique():
    if destination != 'NDF' and destination != 'US':
        ax.plot(df_user['account_created_date'], df_user[f'booked_{destination}_cumulative'], label=f'Benutzer mit Buchung in {destination}')
ax.set(
    title='Kumulative Anzahl neuer Benutzer mit Buchung außerhalb der USA',
    xlabel='Datum',
    ylabel='Gesamtanzahl Benutzer mit Buchung'
)
ax.legend()
plt.show()

# %% [markdown]
# ## 1.2. Buchungen nach Monat

# %%
# Monatliche Zusammenfassung der Benutzer und Buchungen
df_user['month'] = df_user['account_created_date'].dt.to_period('M')
df_monthly_summary = df_user.groupby('month').agg(
    total_users = ('user_id', 'count'),
    booked_users = ('booked', 'sum'),
    booked_US = ('booked_US', 'sum'),
    booked_FR = ('booked_FR', 'sum'),
    booked_DE = ('booked_DE', 'sum'),
    booked_CA = ('booked_CA', 'sum'),
    booked_GB = ('booked_GB', 'sum'),
    booked_AU = ('booked_AU', 'sum'),
    booked_IT = ('booked_IT', 'sum'),
    booked_ES = ('booked_ES', 'sum'),
    booked_NL = ('booked_NL', 'sum'),
    booked_PT = ('booked_PT', 'sum'),
    booked_other = ('booked_other', 'sum'),
    booked_non_US = ('booked_non_US', 'sum'),
).reset_index()
df_monthly_summary['conversion_rate'] = round(df_monthly_summary['booked_users'] / df_monthly_summary['total_users'] * 100, 2)

# %%
df_monthly_summary.head()

# %%
# Visualisierung von Registrierungen, Buchungen und Conversion Rate auf zwei Achsen
fig, ax1 = plt.subplots(figsize=(16, 8))

# X-Achse (Monate) vorbereiten
df_monthly_summary['month_str'] = df_monthly_summary['month'].astype(str)

# Linke Achse: Conversion Rate
color_cv = 'tab:red'
ax1.set_xlabel('Monat')
ax1.set_ylabel('Conversion Rate (%)', color=color_cv)
ln1 = ax1.plot(df_monthly_summary['month_str'], df_monthly_summary['conversion_rate'], 
               color=color_cv, marker='o', linewidth=3, label='Conversion Rate')
ax1.tick_params(axis='y', labelcolor=color_cv)
ax1.set_ylim(0, df_monthly_summary['conversion_rate'].max() * 1.2)

# Rechte Achse: Anzahl Benutzer
ax2 = ax1.twinx()
color_reg = 'tab:blue'
color_book = 'tab:green'
ax2.set_ylabel('Anzahl der Benutzer', color='black')
ln2 = ax2.plot(df_monthly_summary['month_str'], df_monthly_summary['total_users'], 
               color=color_reg, linestyle='--', marker='s', label='Registrierungen')
ln3 = ax2.plot(df_monthly_summary['month_str'], df_monthly_summary['booked_users'], 
               color=color_book, linestyle='-.', marker='^', label='Buchungen')
ax2.tick_params(axis='y', labelcolor='black')

# Legende erstellen
ax1.legend(loc=(0.005,0.95))
ax2.legend(loc=(0.005,0.87))

fig.suptitle('Monatliche Benutzerregistrierungen, Buchungen und Conversion Rate')

# X-Achse Formatierung verbessern
ax1.tick_params(axis='x', rotation=45, labelsize=10)

# Gitterlinien hinzufügen
ax2.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
plt.show()

# %%
# Zusätzliche prozentuale Spalten für Buchungen nach Zielort
for destination in df_user['destination_country'].unique():
    if destination != 'NDF' and destination != 'US':
        df_monthly_summary[f'booked_{destination}_percent'] = df_monthly_summary[f'booked_{destination}'] / df_monthly_summary['booked_non_US']

# %%
# Visualisierung der monatlichen Buchungen nach Zielort (außer USA) als Flächendiagramm
fig, ax = plt.subplots(figsize=(16, 8))
ax.stackplot(df_monthly_summary['month_str'],
             df_monthly_summary['booked_FR_percent'],
             df_monthly_summary['booked_DE_percent'],
             df_monthly_summary['booked_CA_percent'],
             df_monthly_summary['booked_GB_percent'],
             df_monthly_summary['booked_AU_percent'],
             df_monthly_summary['booked_IT_percent'],
             df_monthly_summary['booked_ES_percent'],
             df_monthly_summary['booked_NL_percent'],
             df_monthly_summary['booked_PT_percent'],
             df_monthly_summary['booked_other_percent'],
             labels=['Frankreich', 'Deutschland', 'Kanada', 'Großbritannien', 
                     'Australien', 'Italien', 'Spanien', 'Niederlande', 'Portugal', 'Other'],
             alpha=0.8)

ax.set(
    title='Monatliche Buchungen nach Zielort (außer USA)',
    xlabel='Monat',
    ylabel='Anzahl der Buchungen'
)

ax.legend(loc='upper left')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.show()


# %% [markdown]
# # 2. NDF vs Buchungen

# %%
def plot_share_vs_conversion(column_name, size=(16, 8), color_share='lightgrey', color_cv='gold', sortby=['user_share', False]):
    """Erstellt ein Balkendiagramm, das den Benutzeranteil und die Conversion Rate für eine gegebene Spalte darstellt."""

    # Berechne die Zusammenfassung
    df_summary = df_user.groupby(column_name).agg(
        total_users = ('user_id', 'count'),
        booked_users = ('booked', 'sum')
    ).reset_index()
    df_summary['conversion_rate'] = round(df_summary['booked_users'] / df_summary['total_users'] * 100, 2)
    df_summary['user_share'] = round(df_summary['total_users'] / df_summary['total_users'].sum() * 100, 2)
    global_conversion = round(df_summary['booked_users'].sum() / df_summary['total_users'].sum() * 100, 2)

    df_summary = df_summary.sort_values(by=sortby[0], ascending=sortby[1])

    # Erstelle das Balkendiagramm
    fig, ax = plt.subplots(figsize=size)

    # Setze Achsenbeschriftungen
    ax.set_xlabel(column_name, fontsize=12)
    ax.set_ylabel('Anteil (%)', fontsize=12)
    ax.set_ylim(0, 100)

    # Zeichne die Balkendiagramme
    bar1 = ax.bar(df_summary[column_name], df_summary['user_share'], color=color_share, width=0.8, alpha=0.6, label='Anteil der Benutzer')
    bar2 = ax.bar(df_summary[column_name], df_summary['conversion_rate'], color=color_cv, width=0.3, alpha=0.6, label='Conversion Rate')
    ln1 = ax.axhline(y=global_conversion, color='tomato', linestyle='--', label='Durchschnittliche Conversion Rate')

    # Füge Datenbeschriftungen hinzu
    # ax.bar_label(bar1, fmt='%.2f%%', fontsize=9, color='dimgray')
    ax.bar_label(bar2, fmt='%.2f%%', padding=3, fontsize=9, weight='bold', color='dimgray')

    # Füge Legende und Formatierung hinzu
    # ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')

    # Ausgabe
    fig.suptitle(f'Benutzeranteil und Conversion Rate nach {column_name}', fontsize=16)
    fig.tight_layout()
    plt.show()


# %%
plot_share_vs_conversion('user_gender')

bins = list(range(18, 63, 4)) + [float('inf')]
labels = [f'{i}-{i+3}' for i in range (18, 62, 4)] + ['62+']

df_user['age_group'] = pd.cut(df_user['user_age'], bins=bins, labels=labels, right=False)

plot_share_vs_conversion('age_group', sortby=['age_group', True])

# %%
plot_share_vs_conversion('signup_platform')
plot_share_vs_conversion('first_tracked_affiliate')
plot_share_vs_conversion('signup_application')

# %%
plot_share_vs_conversion('marketing_channel')
plot_share_vs_conversion('marketing_provider')

# %%
plot_share_vs_conversion('first_device')
plot_share_vs_conversion('first_web_browser')


# %% [markdown]
# # 3. Korrelationen

# %%
def categorical_correlation_analysis(var1, var2, df=df_user, min_sample=25):
    """
    Vollständige Korrelationsanalyse zwischen zwei kategorialen Spalten.
    """
    print("="*60)
    print(f"Korrelationsanalyse: {var1} vs {var2}")
    print("="*60)
    
    # 1. Basisinformationen
    print(f"\n1. Datenüberblick:")
    print(f"   {var1}: {df[var1].nunique()} eindeutige Werte")
    print(f"   {var2}: {df[var2].nunique()} eindeutige Werte")
    print(f"   Gesamtbeobachtungen: {len(df)}")
    
    # 2. Chi-Quadrat-Test
    ct = pd.crosstab(df[var1], df[var2])
    chi2, p, dof, expected = chi2_contingency(ct)
    
    print(f"\n2. Pearsons Chi-Quadrat-Test:")
    print(f"   χ² = {chi2:.2f}")
    print(f"   p-Wert = {p:.3f}")
    print(f"   Freiheitsgrade = {dof}")
    
    # 3. Interpretation
    print(f"\n3. Interpretation:")
    if p < 0.01:
        print(f"   Sehr hohe Signifikanz nachgewiesen (p < 0.01)")
    elif p < 0.05:
        print(f"   Hohe Signifikanz nachgewiesen (p < 0.05)")
    else:
        print(f"   Keine Signifikanz nachgewiesen (p ≥ 0.05)")
    
    # 4. Visualisierungen
    print(f"\n4. Visualisierung:")
    fig, ax = plt.subplots(3, 1, figsize=(20, 20))
    
    # Absolute Werte
    sns.heatmap(ct, fmt='d', annot=True, cmap='Blues', ax=ax[0], cbar_kws={'label': 'Häufigkeit'})
    ax[0].set(
        title=f'Absolute Häufigkeiten\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )
    
    # Normalisierte Werte (pro Zeile)
    normalized = ct.div(ct.sum(axis=1), axis=0)
    sns.heatmap(normalized, annot=True, fmt='.2%', cmap='YlOrRd', ax=ax[1], cbar_kws={'label': 'Prozent (%)'})
    ax[1].set(
        title=f'Normalisiert pro Zeile (%)\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )
    
    # Affinitäten
    global_avg = ct.sum(axis=0) / ct.sum().sum()
    lift_matrix = normalized.div(global_avg, axis=1)

    low_data_mask = ct < min_sample
    lift_matrix[low_data_mask] = np.nan

    sns.heatmap(lift_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=1.0, vmin=0.5, vmax=2.0, ax=ax[2], cbar_kws={'label': 'Affinität'})
    ax[2].set(
        title=f'Affinitäten\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )

    fig.suptitle(f'Zusammenhangsanalyse: {var1} und {var2} | χ²={chi2:.1f}, p={p:.3f}', 
                 fontsize=14, y=1.02)
    fig.tight_layout()
    plt.show()

    # Stärkste Assoziationen
    print(f"\n5. Stärkste Assoziationen:")
    
    # Finden der Maximalwerte in jeder Zeile
    for row in normalized.index:
        max_col = normalized.loc[row].idxmax()
        max_value = normalized.loc[row, max_col]
        print(f'    {row}: {max_col} ({max_value:.2%})')
    print('')


# %%
categorical_cols = ['user_gender', 'age_group', 'signup_platform', 'signup_process', 'user_language', 'marketing_channel',
                    'marketing_provider', 'first_tracked_affiliate', 'signup_application', 'first_device', 'first_web_browser']
for col in categorical_cols:
    categorical_correlation_analysis(col, 'destination_country', min_sample=50)
    print('-' * 150)

# %% [markdown]
# # 4. Zusammenfassung und Ausblick

# %% [markdown]
# Tipps für die Marketingabteilung:
# 1. Niedrige Konversionsraten für mobile Geräte erfordern eine Überarbeitung der mobilen Version der Website und der App.
# 2. ...
