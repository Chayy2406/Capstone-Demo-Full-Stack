from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Codex Translation API",
    description="Healthcare medication translation service",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Country to language mapping (from translation_service.py)
SUPPORTED_COUNTRIES = {"US", "India", "UK", "Canada", "Australia"}

# Medication database (from database_service.py)
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
    "acetaminophen": {
        "US": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "India": [{"generic": "Paracetamol 650mg", "brand": "Dolo 650"}],
        "UK": [{"generic": "Paracetamol", "brand": "Panadol"}],
        "Canada": [{"generic": "Acetaminophen", "brand": "Tylenol"}],
        "Australia": [{"generic": "Paracetamol", "brand": "Panadol"}]
    },
    "paracetamol": {
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
    "ibuprofen": {
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
    "brufen": {
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
    "diphenhydramine": {
        "US": [{"generic": "Diphenhydramine", "brand": "Benadryl"}],
        "India": [{"generic": "Diphenhydramine", "brand": "Benadryl"}],
        "UK": [{"generic": "Diphenhydramine", "brand": "Nytol Original"}],
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
    "atorvastatin": {
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
    "omeprazole": {
        "US": [{"generic": "Omeprazole", "brand": "Prilosec"}],
        "India": [{"generic": "Omeprazole", "brand": "Omez"}],
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
    },
    "esomeprazole": {
        "US": [{"generic": "Esomeprazole", "brand": "Nexium"}],
        "India": [{"generic": "Esomeprazole", "brand": "Generic Esomeprazole"}],
        "UK": [{"generic": "Esomeprazole", "brand": "Generic Esomeprazole"}],
        "Canada": [{"generic": "Esomeprazole", "brand": "Nexium"}],
        "Australia": [{"generic": "Esomeprazole", "brand": "Nexium"}]
    }
}


class UserInput(BaseModel):
    original_language: str
    requested_language: str
    original_medication: str


class FinalOutput(BaseModel):
    original_language: str
    requested_language: str
    original_medication: str
    translated_medication: str
    medication_matches: list


def translate_medication(original_country: str, requested_country: str, medication: str) -> dict:
    """Translate medication - validates countries are supported."""
    if original_country not in SUPPORTED_COUNTRIES:
        return {"supported": False, "message": f"Unsupported country: {original_country}"}
    if requested_country not in SUPPORTED_COUNTRIES:
        return {"supported": False, "message": f"Unsupported country: {requested_country}"}

    return {
        "supported": True,
        "translated_medication": medication
    }


def lookup_medication(medication: str, country: str) -> dict:
    """Look up medication equivalents in the target country."""
    med_lower = medication.lower().strip()

    if med_lower in MEDICATION_DATABASE:
        if country in MEDICATION_DATABASE[med_lower]:
            return {
                "success": True,
                "matches": MEDICATION_DATABASE[med_lower][country]
            }
        return {
            "success": False,
            "message": f"No data for {medication} in {country}"
        }

    return {
        "success": False,
        "message": f"Medication '{medication}' not found in database"
    }


@app.get("/")
def root():
    return {"status": "ok", "message": "Codex Translation API"}


@app.post("/api/process", response_model=FinalOutput)
def process_medication(data: UserInput):
    """Process medication translation request."""

    # Validate input
    if not data.original_language.strip():
        raise HTTPException(400, "Original language cannot be empty")
    if not data.requested_language.strip():
        raise HTTPException(400, "Requested language cannot be empty")
    if not data.original_medication.strip():
        raise HTTPException(400, "Original medication cannot be empty")

    original_country = data.original_language.strip()
    requested_country = data.requested_language.strip()
    medication = data.original_medication.strip()

    # Step 1: Translate (validate countries)
    translation_result = translate_medication(original_country, requested_country, medication)

    if not translation_result.get("supported"):
        raise HTTPException(400, f"Translation error: {translation_result.get('message')}")

    translated_medication = translation_result.get("translated_medication")
    if not translated_medication:
        raise HTTPException(500, "Translation did not return a medication name")

    # Step 2: Look up medication in database
    lookup_result = lookup_medication(translated_medication, requested_country)

    if not lookup_result.get("success"):
        raise HTTPException(404, lookup_result.get("message", "No matching medications found"))

    matches = lookup_result.get("matches", [])

    # Format final response
    final_matches = [
        {"generic": m.get("generic"), "brand": m.get("brand")}
        for m in matches
    ]

    return {
        "original_language": original_country,
        "requested_language": requested_country,
        "original_medication": medication,
        "translated_medication": translated_medication,
        "medication_matches": final_matches
    }
