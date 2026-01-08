---
applyTo: "scripts/*.py"
---
# Guidelines for Python Scripts in the Scripts Folder

1.  **Naming:** Use short, descriptive file names indicating the script's purpose (e.g., `inspect_users.py`, `clean_clickstream.py`).
2.  **Documentation:** Include short comments in German at the beginning of each script describing functionality, input data, and intended output. All variable names should be in English.
3.  **Outputs:**
    * Store all analysis results (Markdown/CSV) in the `scripts/outputs/` folder. All text, summaries, and data descriptions should be in German.
    * **STRICTLY FORBIDDEN:** Do not include any visualization logic, plot generation (e.g., using `matplotlib` or `seaborn`), or figure saving commands in scripts within this folder. These scripts are intended solely for data processing and calculation.
4.  **Self-Correction:** After running an analysis script, you MUST read its output in the `scripts/outputs/` folder.
    * Use commands like `cat scripts/outputs/filename.md` to view the results.
    * If the script crashes, read the error traceback and fix the code.
    * If the output is incomplete or incorrect, refine the script and re-run it until the desired results are achieved.
5.  **Visualizations:** Do not create scripts in the `scripts/` folder specifically for generating charts, graphs, or maps. If a task requires visualization, this part of the requirement must be implemented directly in the Jupytext percent format `.py` file in the root directory.
6.  **Migration & Visual Implementation:** Once the analytical part of a task is verified via a script, migrate its logic to the Jupytext percent format `.py` file. For the visualization component, write the code directly in the notebook file so that plots are rendered inline. Ensure no file-saving code (like `.savefig()`) is included in the notebook environment.
7. **Final Documentation:** Maintain a well-organized `scripts/README.md` file documenting each script's purpose and functionality in German.