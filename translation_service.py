"""
Mock Translation Service for Project Codex
Watches for translation_input.json and produces translation_output.json
"""
import json
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Simple country to language mapping
COUNTRY_LANGUAGE_MAP = {
    "US": "english",
    "India": "english",
    "UK": "english",
    "Canada": "english",
    "Australia": "english"
}

class TranslationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith("translation_input.json"):
            time.sleep(0.1)  # Small delay to ensure file is written
            self.process_translation()

    def on_modified(self, event):
        if event.src_path.endswith("translation_input.json"):
            time.sleep(0.1)
            self.process_translation()

    def process_translation(self):
        try:
            with open("translation_input.json", "r") as f:
                data = json.load(f)

            original_lang = data.get("original_language", "")
            requested_lang = data.get("requested_language", "")
            original_med = data.get("original_medication", "")

            # Check if languages are supported
            if original_lang not in COUNTRY_LANGUAGE_MAP or requested_lang not in COUNTRY_LANGUAGE_MAP:
                output = {
                    "supported": False,
                    "message": f"Unsupported language combination: {original_lang} to {requested_lang}"
                }
            else:
                # For this demo, we just pass through the medication name
                # In a real system, this would do actual translation
                output = {
                    "supported": True,
                    "translated_medication": original_med,
                    "original_language": original_lang,
                    "requested_language": requested_lang
                }

            with open("translation_output.json", "w") as f:
                json.dump(output, f, indent=2)

            print(f"✓ Translated: {original_med} ({original_lang} → {requested_lang})")

        except Exception as e:
            print(f"Error in translation service: {e}")

if __name__ == "__main__":
    print("🌐 Translation Service Started")
    print("Watching for translation_input.json...")

    event_handler = TranslationHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
