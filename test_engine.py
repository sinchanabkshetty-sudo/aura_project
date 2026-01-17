
import sys
import os
# Add current directory to path so we can import aura
sys.path.append(os.getcwd())

from aura.command_engine import AURACommandEngine

def test_engine():
    engine = AURACommandEngine()
    
    test_commands = [
        "open calculator",
        "launch notepad",
        "start chrome",
        "play videos about cars on youtube",
        "watch music video",
        "what time is it",
        "set a timer for 5 minutes",
        "open the mail app",
        "send email to test@example.com",
    ]
    
    print("--- AURA Command Engine Routing Test ---\n")
    for cmd in test_commands:
        print(f"Command: '{cmd}'")
        result = engine.parse_command(cmd)
        if isinstance(result, dict):
            status = result.get('status', 'unknown')
            msg = result.get('message', '')
            print(f"Result Status: {status}")
            print(f"Result Message: {msg}")
        else:
            print(f"Result: {result}")
        print("-" * 30)

if __name__ == "__main__":
    test_engine()
