"""
Mock Database Lookup Service for Project Codex
Watches for lookup_input.json and produces lookup_output.json
Uses data from medicines.txt to provide medication mappings
"""
import json
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Medication database based on medicines.txt
MEDICATION_DATABASE = {
    # Pain/Fever medications
    "tylenol": {
        "US": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "India": [{"generic": "Paracetamol 650mg", "brand": "Dolo 650"}, {"generic": "Paracetamol 650mg", "brand": "Calpol 650"}],
        "UK": [{"generic": "Paracetamol", "brand": "Panadol"}, {"generic": "Paracetamol", "brand": "Generic Paracetamol"}],
        "Canada": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "Australia": [{"generic": "Paracetamol", "brand": "Panadol"}]
    },
    "dolo 650": {
        "US": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "India": [{"generic": "Paracetamol 650mg", "brand": "Dolo 650"}],
        "UK": [{"generic": "Paracetamol", "brand": "Panadol"}],
        "Canada": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "Australia": [{"generic": "Paracetamol", "brand": "Panadol"}]
    },
    "panadol": {
        "US": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "India": [{"generic": "Paracetamol 650mg", "brand": "Dolo 650"}],
        "UK": [{"generic": "Paracetamol", "brand": "Panadol"}],
        "Canada": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "Australia": [{"generic": "Paracetamol", "brand": "Panadol"}]
    },

    # NSAID pain relievers
    "advil": {
        "US": [{"generic": "Ibuprofen", "brand": "Advil"}, {"generic": "Ibuprofen", "brand": "Motrin"}],
        "India": [{"generic": "Ibuprofen", "brand": "Brufen"}, {"generic": "Ibuprofen-containing", "brand": "Combiflam"}],
        "UK": [{"generic": "Ibuprofen", "brand": "Nurofen"}],
        "Canada": [{"generic": "Ibuprofen", "brand": "Advil"}],
        "Australia": [{"generic": "Ibuprofen", "brand": "Nurofen"}]
    },
    "motrin": {
        "US": [{"generic": "Ibuprofen", "brand": "Advil"}, {"generic": "Ibuprofen", "brand": "Motrin"}],
        "India": [{"generic": "Ibuprofen", "brand": "Brufen"}],
        "UK": [{"generic": "Ibuprofen", "brand": "Nurofen"}],
        "Canada": [{"generic": "Ibuprofen", "brand": "Advil"}],
        "Australia": [{"generic": "Ibuprofen", "brand": "Nurofen"}]
    },
    "nurofen": {
        "US": [{"generic": "Ibuprofen", "brand": "Advil"}],
        "India": [{"generic": "Ibuprofen", "brand": "Brufen"}],
        "UK": [{"generic": "Ibuprofen", "brand": "Nurofen"}],
        "Canada": [{"generic": "Ibuprofen", "brand": "Advil"}],
        "Australia": [{"generic": "Ibuprofen", "brand": "Nurofen"}]
    },

    # Antihistamine
    "benadryl": {
        "US": [{"generic": "Diphenhydramine", "brand": "Benadryl"}],
        "India": [{"generic": "Diphenhydramine", "brand": "Benadryl"}],
        "UK": [{"generic": "Diphenhydramine", "brand": "Nytol Original"}, {"generic": "Diphenhydramine", "brand": "Boots Sleepeaze"}],
        "Canada": [{"generic": "Diphenhydramine", "brand": "Benadryl"}],
        "Australia": [{"generic": "Diphenhydramine", "brand": "Restavit"}]
    },

    # Cholesterol
    "lipitor": {
        "US": [{"generic": "Atorvastatin", "brand": "Lipitor"}],
        "India": [{"generic": "Atorvastatin", "brand": "Atocor"}],
        "UK": [{"generic": "Atorvastatin", "brand": "Generic Atorvastatin"}],
        "Canada": [{"generic": "Atorvastatin", "brand": "Lipitor"}],
        "Australia": [{"generic": "Atorvastatin", "brand": "Lipitor"}]
    },
    "atocor": {
        "US": [{"generic": "Atorvastatin", "brand": "Lipitor"}],
        "India": [{"generic": "Atorvastatin", "brand": "Atocor"}],
        "UK": [{"generic": "Atorvastatin", "brand": "Generic Atorvastatin"}],
        "Canada": [{"generic": "Atorvastatin", "brand": "Lipitor"}],
        "Australia": [{"generic": "Atorvastatin", "brand": "Lipitor"}]
    },

    # Acid reflux
    "prilosec": {
        "US": [{"generic": "Omeprazole", "brand": "Prilosec"}],
        "India": [{"generic": "Omeprazole", "brand": "Omez"}, {"generic": "Omeprazole", "brand": "Ocid"}],
        "UK": [{"generic": "Omeprazole", "brand": "Losec"}],
        "Canada": [{"generic": "Omeprazole", "brand": "Generic Omeprazole"}],
        "Australia": [{"generic": "Omeprazole", "brand": "Generic Omeprazole"}]
    },
    "nexium": {
        "US": [{"generic": "Esomeprazole", "brand": "Nexium"}],
        "India": [{"generic": "Esomeprazole", "brand": "Generic Esomeprazole"}],
        "UK": [{"generic": "Esomeprazole", "brand": "Generic Esomeprazole"}],
        "Canada": [{"generic": "Esomeprazole", "brand": "Nexium"}],
        "Australia": [{"generic": "Esomeprazole", "brand": "Nexium"}]
    }
}

class DatabaseHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith("lookup_input.json"):
            time.sleep(0.1)
            self.process_lookup()

    def on_modified(self, event):
        if event.src_path.endswith("lookup_input.json"):
            time.sleep(0.1)
            self.process_lookup()

    def process_lookup(self):
        try:
            with open("lookup_input.json", "r") as f:
                data = json.load(f)

            translated_med = data.get("translated_medication", "").lower().strip()
            requested_country = data.get("requested_language", "").strip()

            # Look up medication in database
            if translated_med in MEDICATION_DATABASE:
                if requested_country in MEDICATION_DATABASE[translated_med]:
                    matches = MEDICATION_DATABASE[translated_med][requested_country]
                    output = {
                        "success": True,
                        "matches": matches
                    }
                    print(f"✓ Found {len(matches)} match(es) for '{translated_med}' in {requested_country}")
                else:
                    output = {
                        "success": False,
                        "message": f"No data for {translated_med} in {requested_country}"
                    }
                    print(f"✗ No data for '{translated_med}' in {requested_country}")
            else:
                output = {
                    "success": False,
                    "message": f"Medication '{translated_med}' not found in database"
                }
                print(f"✗ Medication '{translated_med}' not found in database")

            with open("lookup_output.json", "w") as f:
                json.dump(output, f, indent=2)

        except Exception as e:
            print(f"Error in database service: {e}")
            output = {
                "success": False,
                "message": str(e)
            }
            with open("lookup_output.json", "w") as f:
                json.dump(output, f, indent=2)

if __name__ == "__main__":
    print("💾 Database Lookup Service Started")
    print("Watching for lookup_input.json...")

    event_handler = DatabaseHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
