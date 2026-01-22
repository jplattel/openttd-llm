#!/usr/bin/env python3
"""
Main entry point for the OpenTTD LLM Agent
"""
import random
import datetime
import time
import json
from terminology import in_red, in_yellow, in_green
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Literal


class CommandDecision(BaseModel):
    """Structured output for LLM command decisions"""
    reasoning: str
    commands: List[Literal[
        "GetName",
        "GetBankBalance", 
        "GetLoanAmount", 
        "GetMapSize",
        "GetTile",
        # "GetEvents", 
        # "GetTowns"
    ]] = Field(..., min_length=0, max_length=2)


class LLM:
    def __init__(self, state):
        self.state = state
        self.command_template = open("commands.nut", "r").read()
        # Initialize OpenAI client for LM Studio
        # LM Studio runs on localhost:1234 by default
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"  # LM Studio doesn't require a real API key
        )
        self.start()

    def start(self):
        print(in_red("Waiting for you to start the AI in OpenTTD with: start_ai OpenTTDLLM"))
        
        # If we can get the company name, we can assume the AI is running
        while not self.state.running:
            self._send_commands([["GetName"]]) 
            time.sleep(1)
            
        print(in_green("🧠 AI is running, starting eval loop"))
        self.loop()
    
    def _reason_about_commands(self, state: str) -> CommandDecision:
        """Use LLM to reason about which commands to execute"""
        system_prompt = """You are the president of a transport company in OpenTTD. 
Your goal is to make strategic decisions to grow your company.

You have access to these commands:
- GetBankBalance: Check your current cash
- GetLoanAmount: Check your current loan
- GetEvents: Get recent game events
- GetMapSize: Get the current map size
- GetTile: Get the tile at a specific location

Based on the current state, decide which commands you need to gather information 
for your next strategic decision. You should select the commands that will give you 
the most relevant information for planning your next move."""

        completion = self.client.beta.chat.completions.parse(
            model="gtp-oss",  # LM Studio model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current state:\n{state}\n\nWhich commands should I execute to gather information for my next decision?"}
            ],
            response_format=CommandDecision,
        )
        
        return completion.choices[0].message.parsed
        
    def loop(self):
        while True:
            state = self.state.get_state()
            
            # Let the LLM reason about which commands to execute
            print(in_red(f"🧠 Start Reasoning"))
            decision = self._reason_about_commands(state)
            print(in_red(f"🧠 LLM Reasoning: {decision.reasoning}..."))
            
            # Convert command names to the format expected by _send_commands
            print(in_red(f"🧠 Commands: {decision.commands}"))
            commands = [[cmd] for cmd in decision.commands]
            self._send_commands(commands)
        
            print(in_red(f"🧠 Sleeping for 20 seconds"))
            time.sleep(20)
            
    def _send_commands(self, commands=[]):
        # print(in_red(f"📋 Executing commands: {', '.join([cmd[0] for cmd in commands])}"))
        command_template = self.command_template.replace("{{ timestamp }}", str(datetime.datetime.now().isoformat()))
        command_template = command_template.replace("{{ length }}", str(len(commands)))
        command_template = command_template.replace("{{ commands }}", json.dumps(commands))
        
        # print(in_yellow(f"Sending commands: [{', '.join(command[0] for command in commands)}]"))
        with open("/Users/joostplattel/Documents/OpenTTD/ai/OpenTTDLLM/commands.nut", "w") as f:
            f.write(command_template)
                