# 🚨 Anomaly Detection & Alerting Pipeline

> A Google Colab-based pipeline that automatically detects anomalies in your Amazon seller data and sends email alerts — powered by rolling z-score and Year-over-Year deviation analysis.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Mental Model](#-mental-model)
- [Quick Start](#-quick-start-colab)
- [Critical: Data Setup](#-critical-data-setup)
- [Setting Paths in Config](#-setting-paths-in-config)
- [Running the Pipeline](#-running-the-pipeline)
- [Email Setup](#-email-setup)
- [Backtesting](#-backtesting)
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
- 🔁 **Backtesting support** — Re-run the pipeline on historical data to validate alert quality
- ⚙️ **Configurable thresholds** — Tune sensitivity per data source to reduce noise
- 🧩 **Beginner-friendly setup** — Step-by-step instructions, no DevOps experience needed

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
| **Code** | This GitHub repository | Clone it once to your Drive |
| **Data** | Your personal Google Drive | Add shortcuts + set paths in config |

> ⚠️ **This repo contains ZERO data files.** It is code only. Your data lives in your Google Drive and never touches GitHub. You must connect both correctly for the pipeline to work.

---

## 🚀 Quick Start (Colab)

Follow these steps **in order**. Do not skip ahead.

---

### Step 0 — Open Google Colab

1. Go to [https://colab.research.google.com](https://colab.research.google.com)
2. Sign in with your Google account
3. Click **File → New notebook**
4. You'll run all commands below as cells in this notebook

---

### Step 1 — Mount Your Google Drive

Run this in a Colab cell:

```python
from google.colab import drive
drive.mount('/content/drive')
```

- A popup will ask you to authorize Google Drive access — click **Allow**
- Once mounted, your Drive is accessible at `/content/drive/MyDrive/`

> ⚠️ If you see `drive already mounted` — that's fine! Your Drive is already connected. Move to Step 2.

---

### Step 2 — Clone This Repo Into Your Drive

```bash
!git clone https://github.com/six10-AI-Labs/anomaly-alerting.git /content/drive/MyDrive/anomaly-alerting
```

> ✅ **Run this only once.** The repo will be saved permanently in your Drive.
>
> ⚠️ If you see `destination path already exists` — the repo is already cloned. Skip this step and move on.

After cloning, navigate into the project:

```bash
%cd /content/drive/MyDrive/anomaly-alerting
```

---

### Step 3 — Install Requirements

```bash
!pip install -r requirements.txt
```

This installs all Python libraries needed (pandas, scipy, etc.).

> ℹ️ You may need to re-run this each time you start a new Colab session. Colab resets its environment on disconnect.

---

### Step 4 — Create Your Config File from the Template

```bash
!cp config.template.py config.py
```

Now open `config.py` in the Colab file explorer (left sidebar → 📁 Files → navigate to the project folder) and fill in:

- Your Google Drive folder paths (see [Setting Paths](#-setting-paths-in-config) below)
- Your email credentials (see [Email Setup](#-email-setup) below)
- Your detection thresholds

> ⚠️ **Never commit `config.py` to GitHub.** It contains your credentials. It is already listed in `.gitignore`.

---

## ❗ Critical: Data Setup

This is the most common source of errors. Read carefully.

### The Problem with "Shared with me"

Google Colab can only access files that are **directly in your own Google Drive**. Files that were shared with you — and appear under "Shared with me" — are **not accessible** by Colab unless you take one extra step.

### ❌ What does NOT work

```
Google Drive → "Shared with me" → SomeFolder   ← Colab CANNOT see this
```

### ✅ What you MUST do

For every shared folder that contains your data:

1. Open **Google Drive** in your browser
2. Click **"Shared with me"** in the left sidebar
3. Find the folder you need (e.g., your Sellerise exports folder)
4. **Right-click** the folder
5. Click **"Add shortcut to Drive"**
6. Choose **"My Drive"** as the location and click **Add**
7. Repeat for all data folders (Sellerise, Returns, Inventory, Helium10)

After this, the folders will appear under **My Drive** and Colab will be able to access them.

### 📍 Google Drive Access Summary

| Location | Accessible in Colab? |
|----------|----------------------|
| ✅ My Drive | **Yes** |
| ✅ Shared drives (Team Drives) | **Yes** |
| ❌ Shared with me (no shortcut) | **No** |

---

## 📁 Setting Paths in Config

Once your data folders are in "My Drive" (via shortcuts), you need to tell the pipeline where they are.

### How Paths Work in Colab

All paths in Colab start with:

```
/content/drive/MyDrive/
```

So if you have a folder called `SelleriseData` directly in your Drive, its path is:

```
/content/drive/MyDrive/SelleriseData
```

### How to Find the Exact Path

1. Open the **Files panel** in Colab (click the 📁 folder icon in the left sidebar)
2. Navigate to `drive/MyDrive/`
3. Find the folder you want
4. **Right-click** the folder → **Copy path**
5. Paste that path into `config.py`

### Example `config.py` — Drive Paths Section

```python
DRIVE_FOLDERS = {
    "sellerise":  "/content/drive/MyDrive/YourSelleriseFolder",
    "returns":    "/content/drive/MyDrive/YourReturnsFolder",
    "inventory":  "/content/drive/MyDrive/YourInventoryFolder",
    "helium10":   "/content/drive/MyDrive/YourHelium10Folder",
}
```

> ❌ **DO NOT** paste a Google Drive URL (like `https://drive.google.com/drive/folders/...`). That will not work.
>
> ❌ **DO NOT** copy paths from someone else's setup. Paths are unique to your Drive.
>
> ✅ Always use `/content/drive/MyDrive/...` as the prefix.

---

## ▶️ Running the Pipeline

Once your config is set up, run the pipeline:

```bash
!python main.py
```

The pipeline will:

1. Load CSV/XLSX files from each configured Drive folder
2. Run rolling z-score detection across key metrics
3. Run YoY deviation analysis
4. Print a summary of anomalies detected
5. Send email alerts if anomalies exceed your configured thresholds

You'll see log output like:

```
[INFO] Loading Sellerise data...
[INFO] Loading Returns data...
[INFO] Running z-score detection...
[INFO] Anomalies found: 3
[INFO] Sending email alert...
[INFO] Done.
```

---

## 📧 Email Setup

The pipeline sends alerts via Gmail. You **cannot** use your normal Gmail password — you must generate an **App Password**.

### Why App Passwords?

Google blocks "less secure app" sign-ins. An App Password is a special 16-character password that lets scripts access Gmail safely without bypassing 2FA.

### Step-by-Step: Generate a Gmail App Password

1. Go to your Google Account: [https://myaccount.google.com](https://myaccount.google.com)
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google", enable **2-Step Verification** (if not already on)
4. After enabling 2FA, go back to **Security**
5. Search for **"App passwords"** in the search bar at the top, or scroll to find it
6. Click **App passwords**
7. Under "Select app" choose **Mail**
8. Under "Select device" choose **Other** and type a name like `ColabAnomalyBot`
9. Click **Generate**
10. Copy the **16-character password** shown (spaces don't matter — include or exclude them)

### Add Credentials to `config.py`

```python
EMAIL_CONFIG = {
    "sender_email":    "your.email@gmail.com",
    "sender_password": "abcd efgh ijkl mnop",   # Your 16-char App Password
    "recipient_email": "alerts@yourcompany.com",
    "smtp_server":     "smtp.gmail.com",
    "smtp_port":       587,
}
```

> ⚠️ Use your **App Password**, not your regular Gmail password.
>
> ⚠️ Never share or commit your `config.py` file. It contains sensitive credentials.

---

## 🔁 Backtesting

To test whether the pipeline would have caught anomalies in historical data:

```bash
!python backtest.py
```

Backtesting will:

- Replay the detection logic over your full historical dataset
- Output a table of all anomalies that would have been flagged
- Help you tune thresholds before going live

Use this to validate that your thresholds are catching real issues without too much noise.

---

## 🛠️ Common Errors & Fixes

### ❌ `ModuleNotFoundError: No module named 'google.colab'`

**Cause:** You're running the script outside of Google Colab (e.g., locally on your machine).

**Fix:** This pipeline is designed to run **only inside Google Colab**. Open [colab.research.google.com](https://colab.research.google.com) and run it there.

---

### ❌ `drive already mounted at /content/drive`

**Cause:** You tried to mount Google Drive, but it was already mounted from earlier in the session.

**Fix:** This is not an error — your Drive is already connected. Just skip the mount step and continue.

---

### ❌ `fatal: destination path already exists and is not an empty directory`

**Cause:** You ran the `git clone` command, but the repo was already cloned previously.

**Fix:** Skip the clone step. Navigate to the existing folder:

```bash
%cd /content/drive/MyDrive/anomaly-alerting
```

To pull the latest updates instead:

```bash
!git pull origin main
```

---

### ❌ `KeyError` or `missing config values`

**Cause:** Your `config.py` is incomplete — some required fields are empty or missing.

**Fix:** Open `config.py` and make sure every field has a value. Check:

- All four `DRIVE_FOLDERS` paths are filled in
- `EMAIL_CONFIG` has a valid sender email and App Password
- No field is left as `""` or `None` unless it's optional

---

### ❌ `KeyError: 'asin'`

**Cause:** The pipeline expects a column named `asin` in your data files, but it's missing or named differently (e.g., `ASIN`, `Asin`, `product_id`).

**Fix:**

1. Open one of your source files and check the exact column name
2. Either rename the column in your file to `asin` (lowercase)
3. Or update the column name reference in `config.py` under the column mappings section

---

### ❌ `Empty DataFrame` / `No data loaded`

**Cause:** The pipeline found the folder but couldn't read any files — either the folder is empty, the file format is wrong, or the path is slightly off.

**Fix:**

1. Double-check the path in `config.py` — use the Colab file explorer to confirm
2. Make sure files are `.csv` or `.xlsx` (whichever the pipeline expects)
3. Make sure the folder shortcut was added to **My Drive**, not just "Shared with me"
4. Try printing the path and listing files:

```python
import os
path = "/content/drive/MyDrive/YourFolder"
print(os.listdir(path))
```

---

### ❌ `The repo has no data files — where is my data?`

**This is expected behavior.**

This GitHub repository contains **code only**. No data files, no CSVs, no spreadsheets. Your data lives in your Google Drive and belongs to you. The pipeline connects to your Drive at runtime to read it.

> ✅ If you just cloned the repo and see only `.py` files — that's correct. Add your data paths to `config.py` and the pipeline will find your files automatically.

---

## 📂 Project Structure

```
anomaly-alerting/
│
├── main.py                  # 🚀 Main entry point — runs the full pipeline
├── backtest.py              # 🔁 Backtesting script — replays detection on history
├── config.template.py       # ⚙️  Config template — copy this to config.py
├── config.py                # 🔒 Your personal config (NOT committed to GitHub)
│
├── pipeline/
│   ├── loader.py            # 📂 Loads data from Google Drive folders
│   ├── detector.py          # 🔍 Rolling z-score and YoY deviation logic
│   ├── alerter.py           # 📧 Email alert formatting and sending
│   └── utils.py             # 🛠️  Shared helper functions
│
├── requirements.txt         # 📦 Python dependencies
├── .gitignore               # 🚫 Excludes config.py and data files from Git
└── README.md                # 📖 This file
```

---

## ⚙️ Threshold Tuning

The pipeline uses thresholds to decide what counts as an anomaly. You can adjust these in `config.py` under `DETECTION_THRESHOLDS`.

### Z-Score Threshold

A z-score measures how many standard deviations a value is from the rolling mean. The default is usually `2.0` or `3.0`.

### YoY Threshold

This is the percentage change from the same period last year. Example: `0.30` means flag anything that changed more than 30% YoY.

### Tuning Guide

| Symptom | What it means | What to do |
|--------|---------------|------------|
| 🔔 Too many alerts, mostly false positives | Thresholds are too sensitive | **Increase** z-score threshold (e.g., `2.0` → `2.5`) |
| 🔕 Too few alerts, missing real issues | Thresholds are too loose | **Decrease** z-score threshold (e.g., `3.0` → `2.0`) |
| 📅 YoY alerts firing on seasonal items | Normal seasonal swing flagged | **Increase** YoY threshold or add seasonal exclusions |
| ⚡ Spikes ignored | Large but brief outliers missed | **Decrease** rolling window size in config |

> 💡 **Tip:** Use `backtest.py` to test threshold changes on historical data before going live.

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`. Install with:

```bash
!pip install -r requirements.txt
```

### Key Libraries

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical computations |
| `scipy` | Statistical functions (z-score) |
| `openpyxl` | Reading `.xlsx` files |
| `smtplib` *(stdlib)* | Sending emails via SMTP |
| `google-colab` *(built-in)* | Drive mounting (Colab only) |

---

## 🔒 Security Notes

- `config.py` is listed in `.gitignore` and will **never** be pushed to GitHub
- Never hardcode credentials directly in `main.py` or any tracked file
- Use Gmail App Passwords — never your real password
- Rotate your App Password periodically from your Google Account settings

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

<div align="center">

Built with ❤️ by [six10 AI Labs](https://github.com/six10-AI-Labs)

⭐ Star this repo if it helped you!

</div>
