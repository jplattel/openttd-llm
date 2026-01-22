#!/usr/bin/env python3
"""
Main entry point for the OpenTTD LLM Agent
"""
from src.openttd import OpenTTD
from src.log_parser import LogParser
from src.state import State
from src.llm import LLM

# Load environment variables from .env file
from dotenv import load_dotenv; load_dotenv()

def main():
    state = State()
    openttd = OpenTTD()
    log_parser = LogParser(state)
    llm = LLM(state)
    
    try:
        # Keep the main thread alive
        openttd.process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        openttd.stop()
        log_parser.stop()
        llm.stop()
        print("Shutdown complete")

if __name__ == "__main__":
    main()