#!/usr/bin/env python3
"""
Main entry point for the OpenTTD LLM Agent
"""
import random
import datetime
import time
import json
import subprocess
import threading
from terminology import in_red, in_green, in_yellow, in_blue


OPEN_TTD_LOG_FILE = "openttd.log"

class OpenTTD:
    def __init__(self):
        self.process = None
        self.running = False
        self.log_file = open(OPEN_TTD_LOG_FILE, "w")
        self.start_openttd()
        
        
    def start_openttd(self):
        # Start OpenTTD process with output redirected to file
        self.process = subprocess.Popen(
            ["/Applications/OpenTTD.app/Contents/MacOS/openttd", "-g", "-d", "4"], 
            stdout=self.log_file,
            stderr=subprocess.STDOUT
        )
        
    def stop(self):
        """Stop the OpenTTD process"""
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

class LogParser:
    def __init__(self, game_state):
        self.game_state = game_state
        self.log_file = open(OPEN_TTD_LOG_FILE, "r")
        self.log_thread = threading.Thread(target=self._tail_log_file)
        self.log_thread.daemon = True
        self.log_thread.start()
        self.running = True
        
    def _tail_log_file(self):
        """Tail the log file and print lines"""
        import time
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
            print(in_yellow(line))
        if 'OpenTTDLLM >' in line:
            # Outgoing data from OpenTTD
            print(in_green(line))
            line = line.split("OpenTTDLLM >")[1].strip()
            timestamp, command, result = line.split('|')
            print(in_blue(f"Command: {command}, Result: {result}"))
            
            if not self.game_state.running:
                self.game_state.running = True
                
            self.game_state.set_state(command, result)
            
        
    def stop(self):
        self.running = False
        if self.log_thread:
            self.log_thread.join()
            

class State:
    def __init__(self):
        self.running = False
        self.company = {
            "name": "",
            "bank_balance": 0,
            "loan_amount": 0
        }
        self.events = [
            
        ]
        self.towns = [
            
        ]
        
        
    def set_state(self, command, result):
        if command == "GetName":
            self.company["name"] = result
        elif command == "GetBankBalance":
            self.company["bank_balance"] = result
        elif command == "GetLoanAmount":
            self.company["loan_amount"] = result
        elif command == "GetEvents":
            self.events = result
        elif command == "GetTowns":
            self.towns = result
            
    def get_state(self):
        return f"""

## Company State
Name: {self.company["name"]}
Bank Balance: {self.company["bank_balance"]}
Loan Amount: {self.company["loan_amount"]}

## Infrastructure

## Events

{", ".join(self.events)}

## Towns

{", ".join(self.towns)}"""

class LLM:
    def __init__(self, state):
        self.state = state
        self.command_template = open("commands.nut", "r").read()
        self.start()

    def start(self):
        print(in_red("Waiting for you to start the AI in OpenTTD with: start_ai OpenTTDLLM"))
        
        # If we can get the company name, we can assume the AI is running
        while not self.state.running:
            self._send_commands([["GetName"]]) 
            time.sleep(1)
        
        # Actual loop
        while True:
            self._send_commands([["GetBankBalance"], ["GetLoanAmount"]])
            time.sleep(1)
            print(self.state.get_state())
            time.sleep(random.randint(5, 15))
            
    def _send_commands(self, commands=[]):
        command_template = self.command_template.replace("{{ timestamp }}", str(datetime.datetime.now().isoformat()))
        command_template = command_template.replace("{{ length }}", str(len(commands)))
        command_template = command_template.replace("{{ commands }}", json.dumps(commands))
        
        # print(in_yellow(f"Sending commands: [{', '.join(command[0] for command in commands)}]"))
        with open("/Users/joostplattel/Documents/OpenTTD/ai/OpenTTDLLM/commands.nut", "w") as f:
            f.write(command_template)
                

if __name__ == "__main__":
    
    state = State()
    openttd = OpenTTD()
    log_parser = LogParser(state)
    llm = LLM(state)

    
    try:
        # Keep the main thread alive
        openttd.process.wait()
    except KeyboardInterrupt:
        print("\nShutting down OpenTTD and Log Parser...")
        openttd.stop()
        log_parser.stop()
        print("Shutdown complete")