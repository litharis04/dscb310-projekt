---
applyTo: "scripts/*.py"
---
# Guidelines for Python Scripts in the Scripts Folder

1.  **Naming:** Use short, descriptive file names indicating the script's purpose (e.g., `inspect_users.py`, `clean_clickstream.py`).
2.  **Documentation:** Include short comments in German at the beginning of each script describing functionality, input data, and intended output. All variable names should be in English.
3.  **Outputs:**
    * Store all analysis results (Markdown/CSV) and figures (PNG/JPG) in the `scripts/outputs/` folder. All text should be in German.
    * **STRICTLY FORBIDDEN:** Do not use `plt.show()`, `fig.show()`, or any interactive GUI commands. Always use `.savefig()` or write text to files.
    * Use `plt.close()` after saving to free up memory.
4.  **Self-Correction:** After running an analysis script, you MUST read its output in the `scripts/outputs/` folder.
    * Use commands like `cat scripts/outputs/filename.md` to view the results.
    * If the script crashes, read the error traceback and fix the code.
    * If the output is incomplete or incorrect, refine the script and re-run it until the desired results are achieved.
5.  **Visualizations:** For visualization scripts, save the figure and confirm it was created. Do not attempt to "analyze" the image file itself, but ensure the code ran without errors.
6.  **Migration:** Once a script is finalized and verified, add its logic to a new cell to Jupytext percent format .py file (root directory) specified in the prompt. For visualisations, transform the code so that it generates and displays the plot, but do NOT include any file saving code, as plots will be rendered automatically in the notebook environment.
7. **Final Documentation:** Maintain a well-organized `scripts/README.md` file documenting each script's purpose and functionality in German.