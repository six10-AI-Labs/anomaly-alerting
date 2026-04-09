🚨 Anomaly Alerting

Automated daily anomaly detection for Amazon seller metrics.

This pipeline:

Loads daily exports from Google Drive (Sellerise, Returns, Inventory, Helium10)
Detects anomalies using:
14-day rolling z-score
Year-over-Year deviation
Classifies alerts → Critical / Warning / Watch / Improving
Sends a ranked HTML email digest
🧠 How it works (simple mental model)
Google Drive → Data → Pipeline → Alerts → Email

👉 Code comes from GitHub
👉 Data comes from YOUR Google Drive
👉 You must connect BOTH correctly

⚡ Quick Start (Colab — Recommended)
✅ Step 0 — Open in Google Colab
Open notebook OR create a new one in Colab
✅ Step 1 — Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')
✅ Step 2 — Clone the repo INTO your Drive
!git clone https://github.com/six10-AI-Labs/anomaly-alerting.git /content/drive/MyDrive/anomaly-alerting

⚠️ Run this ONLY ONCE
If you see:

destination path already exists

→ skip this step

✅ Step 3 — Install dependencies
%cd /content/drive/MyDrive/anomaly-alerting
%pip install -r requirements.txt
✅ Step 4 — Create config file
cp config.template.py config.py
⚠️ CRITICAL SECTION — DATA SETUP (MOST COMMON FAILURE)
❌ Problem:

Your data is in “Shared with me”

👉 Colab CANNOT see "Shared with me"

✅ Solution (MANDATORY)

For EACH data folder:

Go to Google Drive
Go to Shared with me
Right click folder → Add shortcut to Drive
Place inside:
My Drive
✅ After this, your structure should look like:
My Drive/
  └── 03 Six10 AI Lab - Interns/
        └── Data Feeds/
              ├── SellerRise Sales Data
              ├── Return Reports
              ├── Inventory Reports
              └── Helium10 Data
🧠 Why this matters
Location	Works in Colab?
My Drive	✅ YES
Shared drives	✅ YES
Shared with me	❌ NO
📂 Step 5 — Set correct paths in config.py

👉 This is where most users mess up.

🔥 Rule:

All paths must follow:

"/content/drive/MyDrive/..."
✅ Example (YOU MUST CHANGE BASED ON YOUR DRIVE)
DRIVE_FOLDERS = {
    "sellerise": "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/SellerRise Sales Data",
    "returns": "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Return Reports",
    "inventory": "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Inventory Reports",
    "helium10": "/content/drive/MyDrive/03 Six10 AI Lab - Interns/Data Feeds/Helium10 Data",
}
✅ How to get exact path (BEST METHOD)

In Colab:

Open left sidebar → Files
Navigate to folder
Right click → Copy path
❗ DO NOT:
Use Google Drive URL ❌
Use "Shared with me" path ❌
Guess paths ❌
⚙️ Step 6 — Run the pipeline
%cd /content/drive/MyDrive/anomaly-alerting
!python main.py
📧 Email Setup (IMPORTANT)

You will be prompted for:

Sender Gmail
Gmail App Password (NOT normal password)
🔐 How to generate App Password
Go to Google Account → Security
Enable 2-Step Verification
Go to:
👉 https://support.google.com/accounts/answer/185833
Generate App Password

Use that (16 characters)

🧪 Optional — Backtest
!python backtest.py

👉 Runs on historical data
👉 No email sent

🧠 Common Errors (and FIXES)
❌ Error: No module named google.colab

👉 You are NOT running in Colab

✔️ Fix: Use Google Colab

❌ Error: Mountpoint must not already contain files

👉 You tried mounting incorrectly

✔️ Fix:

Restart runtime
Run mount FIRST
❌ Error: config.py is missing required values

👉 Your paths are wrong or empty

✔️ Fix:

Recheck DRIVE_FOLDERS
Ensure folders actually exist
❌ Error: KeyError: 'asin'

👉 Your data format is wrong

✔️ Fix:

Ensure Sellerise file has ASIN column
Check preprocessing expectations
❌ Error: No data loaded

👉 Usually path issue

✔️ Fix:

Check folder paths
Ensure files exist inside folders
❌ Repo cloned but no data

👉 Expected behavior

✔️ Fix:

Data is NOT in repo
Must connect your own Drive
📁 Project Structure
anomaly_alerting/
├── config.py
├── config.template.py
├── main.py
├── backtest.py
├── ingestion/
├── preprocessing/
├── detection/
├── alerting/
└── data/   (ignored)
⚙️ Threshold Tuning

Edit config.py:

Too many alerts	Too few alerts
Increase STD_DEV_THRESHOLDS	Decrease it
Increase ABSOLUTE_THRESHOLDS	Decrease it

👉 Target: 5–15 Critical alerts/day

🧾 Requirements
Python 3.10+
Google Colab
Google Drive access
Gmail App Password
Data folders:
Sellerise
Returns
Inventory
Helium10
🧠 Final Understanding (IMPORTANT)

👉 This project = Code + Your Data + Correct Paths

If ANY of these fail → pipeline fails

✅ What a new user MUST do
Clone repo
Mount Drive
Add shared folders → My Drive
Set correct paths
Run pipeline
