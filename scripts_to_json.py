import json
import os

APP_NAME = "ersteingabe_lead"  # Deine App

# Verzeichnis mit den Server Scripts
SCRIPT_DIR = os.path.join(os.getcwd(), APP_NAME, "server_scripts")
FIXTURE_FILE = os.path.join(os.getcwd(), APP_NAME, "fixtures", "server_script.json")

# Bestehende Server Scripts einlesen (falls vorhanden)
if os.path.exists(FIXTURE_FILE):
    with open(FIXTURE_FILE, "r") as f:
        existing_data = json.load(f)
else:
    existing_data = []

# Neue Server Scripts erstellen
server_scripts = []

for script_file in os.listdir(SCRIPT_DIR):
    if script_file.endswith(".py"):
        script_path = os.path.join(SCRIPT_DIR, script_file)
        with open(script_path, "r") as f:
            script_content = f.read()
        
        # JSON-Format für Server Script in ERPNext
        script_entry = {
            "doctype": "Server Script",
            "name": script_file.replace(".py", ""),
            "script": script_content
        }
        server_scripts.append(script_entry)

doWrite=False
# Gehe durch alle script_entrys und füge sie zu existing_data hinzu
for script_entry in server_scripts:
    print(f"Server Script: {script_entry['name']}")
    # Suche nach einem bestehenden Server Script mit dem gleichen Namen
    existing_script = next((s for s in existing_data if s["name"] == script_entry["name"]), None)
    print(f"existing_script: {existing_script['name']}")
    if existing_script:
        # Ersetze nur den Wert von "script" mit dem neuen Wert
        existing_script["script"] = script_entry["script"]
        doWrite=True

if doWrite:
    # Schreibe die Daten in die JSON-Datei
    with open(FIXTURE_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)

print(f"Server Scripts wurden exportiert nach: {FIXTURE_FILE}")
