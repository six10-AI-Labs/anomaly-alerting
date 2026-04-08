# Anomaly Alerting

Automated daily anomaly detection for Amazon seller metrics. Compares sales, ACoS, TACoS, margin, conversion rate, return rate, and Helium10 signals against rolling and year-over-year baselines, then sends a ranked HTML email alert.

## How it works

1. Loads daily exports from Google Drive (Sellerise, Returns, Inventory, Helium10)
2. Detects anomalies using z-score (14-day rolling) and year-over-year deviation
3. Classifies alerts as Critical / Warning / Watch / Improving with tier-aware prioritisation
4. Sends a structured HTML email capped at 15 Critical / 10 Warning / 5 Watch / 10 Improving

## Quick start (Google Colab)

**Step 1 — Configure paths**

```bash
cp config.template.py config.py
# Then open config.py and fill in:
#   DRIVE_FOLDER_IDS   — Google Drive folder IDs for each data source
#   DRIVE_FOLDERS      — Mounted Colab paths for each data folder
#   HELIUM10_SNAPSHOT_STORE — path to store daily snapshots
#   EXCEL_OUTPUT_DIR        — path for Excel alert exports
```

> New user? `config.py` ships with empty placeholders. `config.template.py` has instructions for every field.

**Step 2 — Run in Colab**

```python
from google.colab import drive
drive.mount('/content/drive')

%cd /content/drive/MyDrive/YOUR_PATH/anomaly_alerting
%pip install -r requirements.txt

# One-off run
!python main.py

# Or backtest across all historical data (no email sent)
!python backtest.py
```

**Step 3 — Enter email credentials at runtime**

The pipeline prompts for sender email and Gmail App Password — these are never stored in files.  
See [Google App Passwords](https://support.google.com/accounts/answer/185833) to generate one.

## Project structure

```
anomaly_alerting/
├── config.py               # All thresholds and paths (not committed — use template)
├── config.template.py      # Safe placeholder version to share / commit
├── main.py                 # Entry point — runs detection + sends email
├── backtest.py             # Runs detection over historical data without emailing
├── ingestion/
│   └── load_data.py        # Loads and merges all data sources from Drive
├── preprocessing/
│   └── preprocess.py       # Cleans and normalises raw data
├── detection/
│   └── anomaly_detection.py  # Rolling + YoY anomaly scoring
├── alerting/
│   ├── alert_builder.py    # Builds ranked HTML email body
│   └── email_sender.py     # SMTP dispatch
└── data/                   # Local data cache (gitignored)
```

## Threshold tuning

Edit `config.py` to adjust sensitivity:

| Too many alerts | Too few alerts |
|---|---|
| Raise `STD_DEV_THRESHOLDS` values | Lower `STD_DEV_THRESHOLDS` values |
| Raise `ABSOLUTE_THRESHOLDS` floors | Lower `ABSOLUTE_THRESHOLDS` floors |
| Set `SUPPRESS_LESS_THAN_SINGLE = True` | — |

Run `backtest.py` after any change — aim for 5–15 Criticals/day.

## Requirements

- Python 3.10+
- Google Colab (Drive mount) or equivalent environment with Drive access
- Gmail account with App Password enabled
- Daily data exports in Drive from Sellerise, Amazon Returns, Restock Report, Helium10
