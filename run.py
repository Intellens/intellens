#!/usr/bin/env python3
import subprocess
import os
import signal
import sys
import time

def kill_existing_processes():
    """Kill existing processes on ports 8000 and 3000"""
    try:
        subprocess.run(['pkill', '-f', 'uvicorn'], stderr=subprocess.DEVNULL)
        subprocess.run(['pkill', '-f', 'http.server'], stderr=subprocess.DEVNULL)
        time.sleep(1)
    except:
        pass

def start_servers():
    """Start both backend and frontend servers"""
    print("🔄 Stopping existing servers...")
    kill_existing_processes()
    
    print("🚀 Starting backend server...")
    backend_process = subprocess.Popen([
        'python3', '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'
    ], cwd='backend')
    
    time.sleep(3)
    
    print("🌐 Starting frontend server...")
    frontend_process = subprocess.Popen([
        'python3', '-m', 'http.server', '3000'
    ], cwd='frontend')
    
    print("✅ Backend running on http://localhost:8000")
    print("✅ Frontend running on http://localhost:3000")
    print("📁 Open http://localhost:3000 in your browser")
    print("Press Ctrl+C to stop both servers")
    
    def cleanup(signum, frame):
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, cleanup)
    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == "__main__":
    start_servers()