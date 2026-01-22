#!/usr/bin/env python3
"""
Main entry point for the OpenTTD LLM Agent
"""
import time
import threading
from terminology import in_red, in_green, in_yellow, in_blue

class LogParser:
    def __init__(self, log_file, state):
        self.log_file = open(log_file, "r")
        self.state = state
        self.running = True
        self.log_thread = threading.Thread(target=self._tail_log_file)
        self.log_thread.daemon = True
        self.log_thread.start()
        
    def _tail_log_file(self):
        """Tail the log file and print lines"""
        try:
            with open("openttd.log", "r") as f:
                # Go to end of file
                f.seek(0, 2)
                while self.running:
                    line = f.readline()
                    if line:
                        line = line.rstrip('\n')
                        if line:
                            self.parse_log_line(line)
                    else:
                        time.sleep(0.1)  # Wait a bit before checking again
        except Exception as e:
            print(in_red(f"Error tailing log file: {e}"))
            
    def parse_log_line(self, line):
        if 'OpenTTDLLM <' in line:
            # Incoming data to OpenTTD
            line = line.split("OpenTTDLLM <")[1].strip()
            print("🗺️ <" + in_yellow(line))
        if 'OpenTTDLLM >' in line:
            # Outgoing data from OpenTTD
            line = line.split("OpenTTDLLM >")[1].strip()
            print(in_green(f"🗺️ > {line}"))
            
            timestamp, command, result = line.split('|')
            print(in_blue(f"⚙️ Parsed command: {command}, result: {result}"))
            
            if not self.state.running:
                self.state.running = True
                
            self.state.set_state(command, result)
                    
    def stop(self):
        self.running = False
        if self.log_thread:
            self.log_thread.join()
            
