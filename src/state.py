import json


class State:
    def __init__(self):
        self.running = False
        self.company = {
            "name": "",
            "bank_balance": None,
            "loan_amount": None
        }
        self.map_size = {
            "x": "",
            "y": ""
        }
        self.tiles = {
            
        }
        self.events = [
            
        ]
        self.towns = [
            
        ]
        
    def _write_state(self):
        with open("state.json", "w") as f:
            json.dump(self.__dict__, f) 
        
    def set_state(self, command, result):
        match(command):
            case "GetName":
                self.company["name"] = result
                self.running = True # Used to check if the AI is running
            case "GetBankBalance":
                self.company["bank_balance"] = result
            case "GetLoanAmount":
                self.company["loan_amount"] = result
            case "GetMapSize":
                self.map_size["x"] = result.split(",")[0]
                self.map_size["y"] = result.split(",")[1]
            case "GetTile":
                self.map[result[0]][result[1]] = result[2]
                
        try:
            self._write_state()
        except Exception as e:
            pass
                
    def get_state(self):
        return f"""

## Company State
Name: {self.company["name"]}
Bank Balance: {self.company["bank_balance"]}
Loan Amount: {self.company["loan_amount"]}

## Infrastructure
Map Size: {self.map_size["x"]}x{self.map_size["y"]}

## Events

{", ".join(self.events)}

## Towns

{", ".join(self.towns)}"""