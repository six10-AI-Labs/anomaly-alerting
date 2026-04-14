# 🚨 Anomaly Detection & Alerting Pipeline

> A Google Colab-based pipeline that automatically detects anomalies in your Amazon seller data and sends email alerts — powered by rolling z-score and Year-over-Year deviation analysis.

---
#testing
## 📋 Table of Contents

- [Overview](#-overview)
- [Mental Model](#-mental-model)
- [Quick Start — Run Everything in Colab](#-quick-start--run-everything-in-colab)
- [Critical: Data Setup](#-critical-data-setup)
- [Update the Config File](#-update-the-config-file)
- [Email Setup](#-email-setup)
- [Common Errors & Fixes](#-common-errors--fixes)
- [Project Structure](#-project-structure)
- [Threshold Tuning](#-threshold-tuning)
- [Requirements](#-requirements)

---

## 🔍 Overview

This project is a **fully automated anomaly detection pipeline** built to run inside **Google Colab**. It connects to your Google Drive, loads seller data from multiple sources, runs statistical anomaly detection, and fires email alerts when something looks wrong.

### ✨ Features

- 📂 **Multi-source data loading** — Sellerise, Returns, Inventory, and Helium10 data from Google Drive
- 📊 **Rolling Z-Score detection** — Flags metrics that deviate significantly from their recent rolling average
- 📅 **Year-over-Year (YoY) deviation** — Compares current period against the same period last year
- 📧 **Automated email alerts** — Sends formatted alert emails via Gmail when anomalies are detected
- ⚙️ **Configurable thresholds** — Tune sensitivity per data source to reduce noise

---

## 🧠 Mental Model

Before touching any code, read this. It will save you hours of confusion.

```
┌─────────────────────────────────────────────────────────────────┐
│                        HOW THIS WORKS                           │
│                                                                 │
│   GitHub Repo          Your Google Drive        Your Inbox      │
│  ┌──────────┐         ┌──────────────────┐    ┌─────────────┐  │
│  │  Code    │──────▶  │  Data (CSV/XLSX) │    │   Alerts    │  │
│  │  main.py │         │  Sellerise       │    │  📧 Email   │  │
│  │  config  │         │  Returns         │──▶ │            │  │
│  │  utils   │         │  Inventory       │    │  Anomaly X  │  │
│  └──────────┘         │  Helium10        │    │  detected!  │  │
│       │               └──────────────────┘    └─────────────┘  │
│       │                        │                               │
│       └──── Colab Runtime ─────┘                               │
│              (connects both)                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 🔑 The Two Sources — Understand This First

| What | Where it comes from | What you need to do |
|------|--------------------|--------------------|
| **Code** | This GitHub repository | Clone it once to your Drive (Cell 2) |
| **Data** | Your `03 Six10 AI Lab - Interns` shared folder | Add shortcut to My Drive, then set paths in `config.py` |

> ⚠️ **This repo contains ZERO data files.** It is code only. Your data lives in your Google Drive. You must connect both correctly for the pipeline to work.

---

## 🚀 Quick Start — Run Everything in Colab

Open a **new Google Colab notebook** at [colab.research.google.com](https://colab.research.google.com) and run these 4 cells in order.

---

### 📦 Cell 1 — Mount Google Drive

```python
# Cell 1 — Mount Google Drive
# Run this first. A prompt will ask you to authorize access.
from google.colab import drive
drive.mount('/content/drive')
```

---

### 📥 Cell 2 — Clone the Repository into Your Drive *(run only once)*

```python
# Cell 2 — Clone the repository into your Google Drive (run only once)
# This will copy the project into your MyDrive so you don't lose it after session ends.
!git clone https://github.com/six10-AI-Labs/anomaly-alerting.git /content/drive/MyDrive/anomaly-alerting
```

> ✅ Run this **only once**. If you see `destination path already exists` — the repo is already cloned. Skip to Cell 3.

---

### ⚙️ Cell 3 — Configure the Python Path

```python
# Cell 3 — Configure the Python path
# Update REPO_PATH to match where the anomaly_alerting folder lives on your Drive.
# Example: if you saved the project at MyDrive/anomaly-alerting/anomaly_alerting,
# the path below is correct. Adjust only if you moved the folder.
import sys

REPO_PATH = "/content/drive/MyDrive/anomaly-alerting/anomaly_alerting"

if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

print(f"Path configured: {REPO_PATH}")
```

> ⚠️ If you cloned to a different location, update `REPO_PATH` to match. Use the Colab file explorer (📁 left sidebar) to confirm the exact path after cloning.

---

### ▶️ Cell 4 — Run the Pipeline

```python
# Cell 4 — Run the pipeline
# Loads data, detects anomalies, and sends the daily alert digest.
# You will be prompted for a recipient email address before the run starts.
from main import run_pipeline
run_pipeline()
```

> ⚠️ **Before running Cell 4**, you must:
> 1. Complete the [Data Setup](#-critical-data-setup) section below
> 2. Update `config.py` with your data folder paths and email credentials
> 3. **Save `config.py`**, then go to **Runtime → Restart session**, and run all 4 cells again from the top so your changes are picked up

---

## ❗ Critical: Data Setup

This is the most common source of errors. Read carefully before running Cell 4.

### The Problem with "Shared with me"

Google Colab can only access files that are **directly in your own Google Drive**. The `03 Six10 AI Lab - Interns` folder is shared with you — but Colab **cannot** see it unless you add a shortcut first.

### ✅ What You Must Do — Step by Step

1. Open **Google Drive** in your browser
2. Click **"Shared with me"** in the left sidebar
3. Find the folder **`03 Six10 AI Lab - Interns`**
4. **Right-click** it → click **"Add shortcut to Drive"**
5. Choose **"My Drive"** → click **Add**
6. The folder now appears under **My Drive** in the left panel
7. Navigate into it: `03 Six10 AI Lab - Interns → Data Feeds`
8. Inside `Data Feeds`, locate these four folders:
   - `Amazon Sales and Traffic report` → **Sellerise** data
   - `Return Reports` → **Returns** data
   - `Amazon FBA Inventory report` → **Inventory** data
   - `Helium10 Data` → **Helium10** data *(also used for Helium10 Snapshot History)*

### 📍 Google Drive Access Summary

| Location | Accessible in Colab? |
|----------|----------------------|
| ✅ My Drive | **Yes** |
| ✅ Shared drives (Team Drives) | **Yes** |
| ❌ Shared with me (no shortcut added) | **No** |

---

## 📁 Update the Config File

After adding the shortcut, open `config.py` inside the cloned repo in Colab's file explorer (📁 left sidebar → `drive/MyDrive/anomaly-alerting/anomaly_alerting/config.py`) and update the paths.

### How to Find the Exact Path

1. Open the **Files panel** in Colab (📁 icon in the left sidebar)
2. Navigate to `drive → MyDrive → 03 Six10 AI Lab - Interns → Data Feeds`
3. Find the folder you need
4. **Right-click** it → **Copy path**
5. Paste into `config.py`

### Example `config.py` — Drive Paths Section

```python
DRIVE_FOLDERS = {
    "sellerise":          "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Amazon Sales and Traffic report",
    "returns":            "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Return Reports",
    "inventory":          "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Amazon FBA Inventory report",
    "helium10":           "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Helium10 Data",
    "helium10_snapshot":  "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Helium10 Data",
}
```

> ❌ **DO NOT** paste a Google Drive URL (like `https://drive.google.com/drive/folders/...`). That will not work.
>
> ❌ **DO NOT** copy someone else's paths. Paths are specific to your Drive.
>
> ✅ Always start paths with `/content/drive/MyDrive/...`

### After Saving config.py

Go to **Runtime → Restart session** in Colab, then **Run All** cells (1 through 4) from the top. This ensures your updated config is loaded fresh.

---

## 📧 Email Setup

The pipeline sends alerts via Gmail using an **App Password** — not your regular Gmail password.

### Step-by-Step: Generate a Gmail App Password

1. Go to: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   *(Use the Google account whose Drive contains the data)*
2. Under **"Select app"**, choose **"Other"** and type `Colab`
3. Click **Generate**
4. Copy the **16-character password** shown

### Add to `config.py`

```python
EMAIL_CONFIG = {
    "sender_email":    "your.email@gmail.com",
    "sender_password": "xxxx xxxx xxxx xxxx",   # Your 16-character App Password
    "recipient_email": "alerts@yourcompany.com",
}
```

> ⚠️ Use your **App Password** here, not your normal Gmail password.

---

## 🛠️ Common Errors & Fixes

### ❌ `ModuleNotFoundError: No module named 'google.colab'`

**Fix:** This pipeline only runs inside Google Colab. Open [colab.research.google.com](https://colab.research.google.com) and run it there.

---

### ❌ `drive already mounted at /content/drive`

**Fix:** Not an error — your Drive is already connected. Skip Cell 1 and continue from Cell 2.

---

### ❌ `fatal: destination path already exists`

**Fix:** The repo is already cloned. Skip Cell 2. To pull the latest updates instead:

```python
!git -C /content/drive/MyDrive/anomaly-alerting pull origin main
```

---

### ❌ `KeyError` or missing config values

**Fix:** Open `config.py` and make sure every field is filled in. No empty strings `""` or `None` values should remain.

---

### ❌ `KeyError: 'asin'`

**Fix:** One of your data files uses a different column name (e.g., `ASIN` instead of `asin`). Open the file, check the exact column name, and update the column mapping in `config.py`.

---

### ❌ `Empty DataFrame` / `No data loaded`

**Fix:**
1. Confirm the shortcut was added to **My Drive** (not just browsed under "Shared with me")
2. Confirm the path in `config.py` is correct — verify in the Colab file explorer
3. Debug by running:

```python
import os
print(os.listdir("/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds"))
```

---

### ❌ The repo has no CSV or data files — where is my data?

**This is expected.** The GitHub repo is **code only**. Your data lives inside `Data Feeds` in the shared Drive folder. The pipeline reads it from there at runtime.

---

### ❌ Config changes not picked up after editing

**Fix:** After saving `config.py`, go to **Runtime → Restart session**, then run all 4 cells again from Cell 1.

---

## 📂 Project Structure

```
anomaly-alerting/
│
├── anomaly_alerting/
│   ├── main.py              # 🚀 Main entry point — run_pipeline() lives here
│   ├── config.py            # 🔒 Your personal config (NOT committed to GitHub)
│   ├── config.template.py   # ⚙️  Copy this to create config.py
│   ├── detector.py          # 🔍 Rolling z-score and YoY deviation logic
│   ├── loader.py            # 📂 Loads data from Google Drive folders
│   ├── alerter.py           # 📧 Email alert formatting and sending
│   └── utils.py             # 🛠️  Shared helper functions
│
├── requirements.txt         # 📦 Python dependencies
├── .gitignore               # 🚫 Excludes config.py and data files from Git
└── README.md                # 📖 This file
```

---

## ⚙️ Threshold Tuning

Adjust detection sensitivity in `config.py` under `DETECTION_THRESHOLDS`.

| Symptom | What to do |
|--------|------------|
| 🔔 Too many alerts / false positives | **Increase** z-score threshold (e.g. `2.0` → `2.5`) |
| 🔕 Too few alerts / missing real issues | **Decrease** z-score threshold (e.g. `3.0` → `2.0`) |
| 📅 Seasonal items constantly flagged | **Increase** YoY threshold |
| ⚡ Brief spikes being missed | **Decrease** rolling window size |

---

## 📦 Requirements

```bash
!pip install -r requirements.txt
```

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical computations |
| `scipy` | Statistical functions (z-score) |
| `openpyxl` | Reading `.xlsx` files |

---

## 🔒 Security Notes

- `config.py` is in `.gitignore` — it will **never** be pushed to GitHub
- Never hardcode credentials in any tracked file
- Use Gmail App Passwords only — never your real Gmail password

---

<div align="center">

Built with ❤️ by [six10 AI Labs](https://github.com/six10-AI-Labs)

⭐ Star this repo if it helped you!

</div>
