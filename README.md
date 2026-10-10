# ContentFix — GenAI Content Audit and Migration Assistant

ContentFix is a local Streamlit application for auditing HTML page exports, tracking remediation work, drafting metadata with an optional OpenAI API connection, and exporting audit results.

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The included `sample_site/` contains 300 illustrative HTML pages. The audit works on local HTML files and does not crawl the public internet.

## Features
- BeautifulSoup audit for missing title/description/alt text, broken local links, and formatting issues.
- SQLite issue and fix-request tracking.
- Optional OpenAI-generated alt text and meta descriptions; generated copy must be reviewed before use.
- Excel export using Pandas and openpyxl.
- Power BI-ready CSV exports and a starter report guide in `powerbi/`.

Set `OPENAI_API_KEY` in the environment to enable AI drafting. Without a key, the app remains usable for auditing, tracking, and exports.

## Data and evaluation
The bundled site and benchmark CSVs are demonstration fixtures, not a live customer website or independent validation study. `data/benchmark_review.csv` records a sample 50-output human-review exercise (41 accepted with minor edits). Re-run the audit on your own HTML export before using any reported counts in a portfolio or interview.
