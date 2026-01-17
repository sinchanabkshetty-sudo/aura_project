#!/usr/bin/env python3
"""
AURA Command Line Interface - No GUI Required
Bypass GUI issues and run AURA directly from terminal
"""

import os
import sys
import signal
from aura.command_engine import get_engine

def signal_handler(sig, frame):
    print("\n👋 AURA CLI shutting down gracefully...")
    sys.exit(0)

def main():
    print("🚀 AURA Command Line Interface")
    print("=" * 50)
    
    # Initialize engine
    try:
        engine = get_engine()
        print(f"INFO: AURA initialized successfully")
        print(f"INFO: Platform: {engine.os_type}")
        print(f"INFO: Working Directory: {os.getcwd()}")
        print("\n💡 Type commands or 'quit' to exit")
        print("🎯 Examples: 'hello', 'open calculator', 'what time is it'")
        print("-" * 50)
    except Exception as e:
        print(f"ERROR: Failed to initialize AURA: {e}")
        return 1
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Main command loop
    while True:
        try:
            # Get user input
            user_input = input("\n[AURA]> ").strip()
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("👋 Goodbye! AURA CLI shutting down...")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process command
            print("Processing...")
            result = engine.execute_command(user_input)
            
            # Display result
            if isinstance(result, dict):
                message = result.get("message", str(result))
            else:
                message = str(result)
            
            print(f"AURA: {message}")
            
        except KeyboardInterrupt:
            print("\n👋 AURA CLI shutting down gracefully...")
            break
        except EOFError:
            print("\n👋 AURA CLI shutting down gracefully...")
            break
        except Exception as e:
            print(f"ERROR: Error processing command: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())