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
import missingno as msno
import matplotlib.pyplot as plt
from IPython.display import display

# %%
# Daten laden
df_clickstreams = pd.read_parquet('data/clickstreams.parquet')

rows_initial = len(df_clickstreams)
print(f"Anzahl der Zeilen: {rows_initial}")
print(f"Anzahl der Spalten: {len(df_clickstreams.columns)}")
print(f"\nSpalten: {list(df_clickstreams.columns)}")

# %%
df_clickstreams.head(25)

# %%
df_clickstreams.info()

# %%
df_clickstreams.session_user_id.nunique()

# %%
text_cols = ['session_action', 'session_action_type', 'session_action_detail', 'session_device_type']
for col in text_cols:
    print(df_clickstreams[col].value_counts(dropna=False))
    print('-' * 80)

# %%
