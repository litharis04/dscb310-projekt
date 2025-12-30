---
applyTo: "scripts/*.py"
---
# Guidelines for Python Scripts in the Scripts Folder

1.  **Naming:** Use short, descriptive file names indicating the script's purpose (e.g., `inspect_users.py`, `clean_clickstream.py`).
2.  **Documentation:** Include comments at the beginning of each script describing functionality, input data, and intended output.
3.  **Outputs:**
    * Store all analysis results (text/CSVs) and figures (PNG/JPG) in the `scripts/outputs/` folder.
    * **STRICTLY FORBIDDEN:** Do not use `plt.show()`, `fig.show()`, or any interactive GUI commands. Always use `.savefig()` or write text to files.
4.  **Self-Correction:** After running a script, you MUST read its output in the `outputs` folder.
    * Use commands like `cat scripts/outputs/filename.txt` to view the results.
    * If the script crashes, read the error traceback and fix the code.
5.  **Visualizations:** For visualization scripts, save the figure and confirm it was created. Do not attempt to "analyze" the image file itself, but ensure the code ran without errors.
6.  **Migration:** Once a script is finalized and verified, add its logic to a new cell in `EDA.py` (root directory).