#!/bin/bash

# Start all backend services for Project Codex

echo "Starting Project Codex Backend Services..."

# Start translation service in background
python3 translation_service.py &
TRANSLATION_PID=$!
echo "Translation Service started (PID: $TRANSLATION_PID)"

# Wait a moment
sleep 1

# Start database service in background
python3 database_service.py &
DATABASE_PID=$!
echo "Database Lookup Service started (PID: $DATABASE_PID)"

# Wait a moment
sleep 1

# Start main FastAPI middleware
echo "Starting FastAPI Middleware..."
uvicorn main:app --reload --port 8000 &
API_PID=$!
echo "FastAPI started (PID: $API_PID)"

echo ""
echo "All services are running!"
echo "Translation Service: PID $TRANSLATION_PID"
echo "Database Service: PID $DATABASE_PID"
echo "FastAPI Middleware: PID $API_PID on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $TRANSLATION_PID $DATABASE_PID $API_PID 2>/dev/null; exit" INT
wait
