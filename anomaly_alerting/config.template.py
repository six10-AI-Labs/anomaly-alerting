# config.template.py
# Copy this file to config.py and fill in every value marked YOUR_*.
# Never commit a config.py that contains real paths or folder IDs.
#
# Usage:
#   cp config.template.py config.py   (then edit config.py)

# =============================================================================
# GOOGLE DRIVE FOLDER IDs
# =============================================================================
# Find these in the share URL of each folder:
#   https://drive.google.com/drive/folders/<FOLDER_ID>
DRIVE_FOLDER_IDS = {
    "sellerise":  "YOUR_SELLERISE_FOLDER_ID",
    "returns":    "YOUR_RETURNS_FOLDER_ID",
    "inventory":  "YOUR_INVENTORY_FOLDER_ID",
    "helium10":   "YOUR_HELIUM10_FOLDER_ID",
}

# =============================================================================
# GOOGLE DRIVE MOUNTED PATHS
# =============================================================================
# After drive.mount('/content/drive') in Colab, set each path to the
# mounted location of the corresponding folder.
# Example: "/content/drive/MyDrive/YourOrg/Data Feeds/SellerRise"
DRIVE_FOLDERS = {
    "sellerise":  "/content/drive/MyDrive/YOUR_PATH/SellerRise Sales Data",
    "returns":    "/content/drive/MyDrive/YOUR_PATH/Return Reports",
    "inventory":  "/content/drive/MyDrive/YOUR_PATH/Amazon Restock Report",
    "helium10":   "/content/drive/MyDrive/YOUR_PATH/Helium10 Data",
}

# =============================================================================
# HELIUM10 SNAPSHOT STORE
# =============================================================================
# Folder where daily Helium10 snapshots are written.
# Must be a mounted Drive path writable by Colab.
HELIUM10_SNAPSHOT_STORE = "/content/drive/MyDrive/YOUR_PATH/helium10_history"

# =============================================================================
# EXCEL OUTPUT DIRECTORY
# =============================================================================
# Folder where alert Excel exports are saved after each run.
EXCEL_OUTPUT_DIR = "/content/drive/MyDrive/YOUR_PATH/outputs"

# =============================================================================
# All other settings are pre-configured in config.py.
# Only the four sections above require environment-specific values.
# =============================================================================
