#!/usr/bin/env python3
"""
Run script for the APL Context-Aware.

This script provides a convenient way to run the enhanced APL application.
"""

import os
import sys
import argparse
from pathlib import Path

def main():
    """Main function for the run script."""
    parser = argparse.ArgumentParser(description="Run APL Context-Aware")
    
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run in demo mode with learning partner scenario"
    )
    
    parser.add_argument(
        "--compare", "-c",
        action="store_true",
        help="Run comparison demo (context-aware vs standard)"
    )
    
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8083,
        help="Port to run the application on (default: 8083)"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        print("Starting Learning Partner demo...")
        # Will implement this after we create the demo files
        print("Demo mode not yet implemented - running standard mode")
    elif args.compare:
        print("Starting comparison demo...")
        # Will implement this after we create the comparison tools
        print("Comparison mode not yet implemented - running standard mode")
    
    # Run the application
    print(f"Starting APL Context-Aware on port {args.port}...")
    os.environ["APL_PORT"] = str(args.port)
    
    # Execute main.py directly as a script
    import subprocess
    subprocess.run([sys.executable, "main.py", "--port", str(args.port)])

if __name__ == "__main__":
    main()