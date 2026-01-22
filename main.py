#!/usr/bin/env python3
"""
Main entry point for the OpenTTD LLM Agent
"""
from src.openttd import OpenTTD
from src.log_parser import LogParser
from src.state import State
from src.llm import LLM

OPEN_TTD_LOG_FILE = "openttd.log"

def main():
    state = State()
    openttd = OpenTTD(OPEN_TTD_LOG_FILE)
    log_parser = LogParser(OPEN_TTD_LOG_FILE, state)
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