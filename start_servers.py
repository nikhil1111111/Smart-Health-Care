#!/usr/bin/env python3
"""
Smart Healthcare Platform - Server Startup Script
This script starts both the Flask backend and Node.js blog server
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.flask_process = None
        self.node_process = None
        self.running = False

    def check_requirements(self):
        """Check if all requirements are installed"""
        print("🔍 Checking requirements...")

        # Check Python dependencies
        try:
            import flask
            import sqlite3
            print("✅ Python dependencies: OK")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("💡 Run: pip install -r requirements.txt")
            return False

        # Check Node.js dependencies
        if not Path("healthcare-blog/node_modules").exists():
            print("❌ Node.js dependencies not installed")
            print("💡 Run: cd healthcare-blog && npm install")
            return False
        else:
            print("✅ Node.js dependencies: OK")

        return True

    def setup_database(self):
        """Initialize the database"""
        print("🗄️ Setting up database...")
        try:
            result = subprocess.run([sys.executable, "db_setup.py"],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Database setup: Complete")
                return True
            else:
                print(f"❌ Database setup failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Database setup timed out")
            return False
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            return False

    def start_flask_server(self):
        """Start the Flask server"""
        print("🚀 Starting Flask server...")
        try:
            self.flask_process = subprocess.Popen([
                sys.executable, "app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("✅ Flask server started (PID: {})".format(self.flask_process.pid))
            return True
        except Exception as e:
            print(f"❌ Failed to start Flask server: {e}")
            return False

    def start_node_server(self):
        """Start the Node.js blog server"""
        print("🚀 Starting Node.js blog server...")
        try:
            self.node_process = subprocess.Popen([
                "node", "healthcare-blog/server.js"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("✅ Node.js server started (PID: {})".format(self.node_process.pid))
            return True
        except Exception as e:
            print(f"❌ Failed to start Node.js server: {e}")
            return False

    def monitor_servers(self):
        """Monitor server processes"""
        def check_flask():
            if self.flask_process and self.flask_process.poll() is not None:
                print("❌ Flask server has stopped")
                self.running = False

        def check_node():
            if self.node_process and self.node_process.poll() is not None:
                print("❌ Node.js server has stopped")
                self.running = False

        while self.running:
            check_flask()
            check_node()
            time.sleep(2)

    def print_status(self):
        """Print server status and URLs"""
        print("\n" + "="*60)
        print("🏥 SMART HEALTHCARE PLATFORM - SERVER STATUS")
        print("="*60)
        print("✅ Flask Backend Server:")
        print("   - URL: http://localhost:5000")
        print("   - Health: http://localhost:5000/api/diagnosis")
        print("   - Status: {}".format("Running" if self.flask_process and self.flask_process.poll() is None else "Stopped"))
        print()
        print("✅ Node.js Blog Server:")
        print("   - URL: http://localhost:5001")
        print("   - Health: http://localhost:5001/api/health")
        print("   - Status: {}".format("Running" if self.node_process and self.node_process.poll() is None else "Stopped"))
        print()
        print("🌐 Frontend:")
        print("   - Dashboard: http://localhost:5000")
        print("   - Blog Integration: Available in dashboard")
        print("="*60)

    def start_all(self):
        """Start all servers"""
        print("🏥 Smart Healthcare Platform")
        print("="*50)

        if not self.check_requirements():
            return False

        if not self.setup_database():
            return False

        # Start servers
        if not self.start_flask_server():
            return False

        time.sleep(2)  # Wait for Flask to start

        if not self.start_node_server():
            # Stop Flask if Node.js fails
            if self.flask_process:
                self.flask_process.terminate()
            return False

        self.running = True

        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_servers, daemon=True)
        monitor_thread.start()

        # Print status
        self.print_status()

        print("\n✅ All servers started successfully!")
        print("💡 Press Ctrl+C to stop all servers")
        print()

        try:
            # Wait for processes
            while self.running:
                if self.flask_process and self.flask_process.poll() is None:
                    time.sleep(1)
                else:
                    break
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            self.stop_all()

    def stop_all(self):
        """Stop all servers"""
        self.running = False

        if self.flask_process:
            print("🛑 Stopping Flask server...")
            self.flask_process.terminate()
            try:
                self.flask_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.flask_process.kill()

        if self.node_process:
            print("🛑 Stopping Node.js server...")
            self.node_process.terminate()
            try:
                self.node_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.node_process.kill()

        print("✅ All servers stopped")

def main():
    manager = ServerManager()

    def signal_handler(signum, frame):
        print(f"\n🛑 Received signal {signum}")
        manager.stop_all()
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start servers
    success = manager.start_all()

    if not success:
        print("❌ Failed to start servers")
        sys.exit(1)

if __name__ == "__main__":
    main()
