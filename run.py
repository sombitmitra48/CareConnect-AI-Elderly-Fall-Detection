#!/usr/bin/env python3
"""
CareConnect - AI Guardian for the Elderly
Main entry point for the application
"""

import uvicorn
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="CareConnect - AI Guardian for the Elderly")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8002, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print("🌟 Starting CareConnect - AI Guardian for the Elderly")
    print(f"🚀 Server running on http://{args.host}:{args.port}")
    print(f"📖 Documentation available at http://localhost:{args.port}/docs")
    
    # Change to the CC1 directory where main.py is located
    import sys
    sys.path.append("CC1")
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()