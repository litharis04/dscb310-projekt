---
applyTo: "EDA.py"
---

# Rules for Jupytext Percent Format (Main Analysis File)

1.  **EDIT THIS FILE DIRECTLY.** This is the source file for the main Jupyter Notebook (`EDA.ipynb`).
2.  **Syncing:** Changes here will automatically sync to `EDA.ipynb` via Jupytext.
3.  **Format:**
    * Use `# %%` to denote code cell boundaries.
    * Use `# %% [markdown]` for markdown cells.
4.  **Content:**
    * Only add **finalized, working code** here (code that has been tested in the `scripts/` folder).
    * Do not include `print()` outputs or execution logs in this file; they belong in the generated notebook.
    * Use direct outputs (e.g., `display(df)` or simply `df`) at the end of cells for output, suitable for Jupyter execution.