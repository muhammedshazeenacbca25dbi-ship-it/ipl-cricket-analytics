# IPL Matches Dashboard (Streamlit)

## Run in VS Code

1. Extract this ZIP folder.
2. Open the extracted folder in VS Code.
3. Open Terminal → New Terminal.
4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Put your IPL CSV file in this folder (or upload it inside the app).
6. Run:
   ```bash
   python -m streamlit run app.py
   ```

If your CSV is named `matches(1).csv`, type that exact name into the app's **Local CSV filename** field. You can also upload the CSV with the uploader.

Note: the demo charts are placeholders until you load real data. Different IPL CSV files use different column names, so some charts may require a ball-by-ball dataset or matching columns.
