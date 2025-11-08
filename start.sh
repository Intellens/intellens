#!/bin/bash

# Kill existing processes on ports 8000 and 3000
echo "Stopping existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

sleep 2

# Start backend
echo "Starting backend..."
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 3

# Start frontend (simple HTTP server)
echo "Starting frontend..."
cd ../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo "✅ Backend running on http://localhost:8000"
echo "✅ Frontend running on http://localhost:3000"
echo "📁 Open http://localhost:3000 in your browser"
echo "Press Ctrl+C to stop both servers"

# Cleanup function
cleanup() {
    echo "\nStopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT
wait