# MyWajarScope — MDIT 2026 (SDG 8)

Interactive district dashboard: *Does having a job mean having decent work?*
Built on official OpenDOSM data (household income, poverty, labour force, district GDP).

## Run on your laptop
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```
Opens at http://localhost:8501

## Put it online (free, link stays live for judging)
1. Create a **public GitHub repo** (e.g. `mywajarscope`) and upload everything in this `app/` folder
   (`app.py`, `style.css`, `requirements.txt`, `data/`, `.streamlit/config.toml`).
2. Go to https://share.streamlit.io → sign in with GitHub → **Create app**.
3. Pick the repo, branch `main`, main file `app.py` → **Deploy**.
4. Copy the `https://<name>.streamlit.app` link into the report and submission form.

Tip: open the link once a day until judging ends (free apps sleep after inactivity; they wake on visit).

## Tabs
- **Map**: animated district map; pick a state in the sidebar to glide in; colour by type, gap index, income, poverty, unemployment or participation.
- **District profile**: one-district view with radar vs Malaysia, 2019→2024 trend, suggested action areas, similar districts doing better, and a downloadable district brief.
- **District types**: K-Means clusters and the "employed but not well-paid" evidence.
- **Priority list**: Decent Work Gap Index with adjustable weights, or data-driven Entropy-TOPSIS; agreement check between both; CSV download.
- **2019 → 2024**: income growth and poverty change by type; compare districts.
- **Drivers & what-if**: Random Forest drivers, out-of-fold validation chart, and a what-if simulator.
- **About**: animated, scroll-driven infographic of data, method, findings, SDG alignment and limitations.

English / Bahasa Melayu toggle at the top right.

## Updating the data
Re-run `mdit_analysis.ipynb`, then copy `outputs/dashboard_district_2022.csv` into `app/data/`.
