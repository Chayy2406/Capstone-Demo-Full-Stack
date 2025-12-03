# Project Codex - Medicine Translation System

A full-stack application that converts medicine names from region to region, helping users find equivalent medications across different countries (US, India, UK, Canada, Australia).

## Architecture

The system consists of three main components that communicate via JSON files:

1. **Translation Service** (`translation_service.py`) - Handles language/region translation
2. **Database Lookup Service** (`database_service.py`) - Matches medications from the database
3. **FastAPI Middleware** (`main.py`) - Orchestrates communication between services
4. **React Frontend** - User interface for searching medications

### Data Flow

```
User Input → React Frontend → FastAPI (main.py) → Translation Service
                                                  ↓
                            React Frontend ← FastAPI ← Database Service
```

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### Backend Setup

1. Navigate to the project directory:
```bash
cd "/Users/chay/Desktop/Capstone Demo"
```

2. Create a Python virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

## Running the Application

You need to run the backend services and frontend in separate terminal windows.

### Option 1: Use the Start Script (Recommended)

**Terminal 1 - Backend Services:**
```bash
cd "/Users/chay/Desktop/Capstone Demo"
source venv/bin/activate  # Activate virtual environment
./start_backend.sh
```

This will start all three backend services:
- Translation Service (watches for translation_input.json)
- Database Lookup Service (watches for lookup_input.json)
- FastAPI Middleware (runs on http://localhost:8000)

**Terminal 2 - Frontend:**
```bash
cd "/Users/chay/Desktop/Capstone Demo/frontend"
npm run dev
```

The frontend will be available at: http://localhost:3000

### Option 2: Manual Start (For Debugging)

If you want to run each service separately for debugging:

**Terminal 1 - Translation Service:**
```bash
cd "/Users/chay/Desktop/Capstone Demo"
source venv/bin/activate
python3 translation_service.py
```

**Terminal 2 - Database Service:**
```bash
cd "/Users/chay/Desktop/Capstone Demo"
source venv/bin/activate
python3 database_service.py
```

**Terminal 3 - FastAPI Middleware:**
```bash
cd "/Users/chay/Desktop/Capstone Demo"
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 4 - React Frontend:**
```bash
cd "/Users/chay/Desktop/Capstone Demo/frontend"
npm run dev
```

## Using the Application

1. Open your browser to http://localhost:3000
2. Enter a medicine name (e.g., "Tylenol", "Advil", "Lipitor")
3. Select the "From Country" (where the medicine is from)
4. Select the "To Country" (where you want to find equivalents)
5. Click "Search"
6. View the equivalent medications available in the target country

## Available Medications

The system currently supports the following medications across regions:

**Pain/Fever:**
- Tylenol (US) ↔ Dolo 650/Calpol (India) ↔ Panadol (UK/Australia)
- Advil/Motrin (US) ↔ Brufen/Combiflam (India) ↔ Nurofen (UK/Australia)

**Antihistamine:**
- Benadryl (US/India/Canada) ↔ Nytol/Sleepeaze (UK) ↔ Restavit (Australia)

**Cholesterol:**
- Lipitor (US/Canada/Australia) ↔ Atocor (India) ↔ Generic Atorvastatin (UK)

**Acid Reflux:**
- Prilosec (US) ↔ Omez/Ocid (India) ↔ Losec (UK)
- Nexium (US/Canada/Australia)

## API Endpoints

### POST /process

Processes a medication translation request.

**Request Body:**
```json
{
  "original_language": "US",
  "requested_language": "India",
  "original_medication": "Tylenol"
}
```

**Response:**
```json
{
  "original_language": "US",
  "requested_language": "India",
  "original_medication": "Tylenol",
  "translated_medication": "Tylenol",
  "medication_matches": [
    {
      "generic": "Paracetamol 650mg",
      "brand": "Dolo 650"
    },
    {
      "generic": "Paracetamol 650mg",
      "brand": "Calpol 650"
    }
  ]
}
```

## Project Structure

```
Capstone Demo/
├── main.py                    # FastAPI middleware (THE BACKBONE)
├── translation_service.py     # Translation service
├── database_service.py        # Database lookup service
├── medicines.txt              # Medicine information reference
├── requirements.txt           # Python dependencies
├── start_backend.sh          # Script to start all backend services
├── .gitignore                # Git ignore file
├── README.md                 # This file
└── frontend/
    ├── package.json          # Frontend dependencies
    ├── vite.config.js        # Vite configuration
    ├── index.html            # HTML entry point
    └── src/
        ├── main.jsx          # React entry point
        ├── App.jsx           # Main React component
        ├── App.css           # Application styles
        └── index.css         # Global styles
```

## How It Works

1. User enters medicine information in the React frontend
2. Frontend sends POST request to FastAPI middleware (`/process` endpoint)
3. FastAPI writes `translation_input.json` and waits
4. Translation service detects the file and writes `translation_output.json`
5. FastAPI reads translation result and writes `lookup_input.json`
6. Database service detects the file and writes `lookup_output.json`
7. FastAPI reads database results and returns final response to frontend
8. Frontend displays the equivalent medications

## Troubleshooting

**Services won't start:**
- Make sure virtual environment is activated
- Check if ports 8000 and 3000 are available
- Ensure all dependencies are installed

**No results found:**
- Check that the medicine name is spelled correctly
- The system is case-insensitive but requires the exact brand name
- Try common brands: Tylenol, Advil, Benadryl, Lipitor, Prilosec

**Connection errors:**
- Ensure all backend services are running (translation, database, FastAPI)
- Check that FastAPI is running on port 8000
- Check that React is running on port 3000

## Extending the Database

To add more medications, edit `database_service.py` and add entries to the `MEDICATION_DATABASE` dictionary following this format:

```python
"medicine_name": {
    "US": [{"generic": "Generic Name", "brand": "Brand Name"}],
    "India": [{"generic": "Generic Name", "brand": "Brand Name"}],
    # ... other countries
}
```

## Stopping the Application

**If using start_backend.sh:**
- Press `Ctrl+C` in the terminal running the backend services

**If running manually:**
- Press `Ctrl+C` in each terminal window

**Frontend:**
- Press `Ctrl+C` in the terminal running npm

---

Built for Project Codex Middleware Team
