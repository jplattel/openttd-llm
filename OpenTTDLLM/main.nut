/*
 *
 * This GameScript receives commands from the LLM via Admin Port
 * and executes them in the game world or passes them to AI companies.
 * This is a bridge between the LLM and the game world.
 */
class OpenTTDLLM extends AIController {
    function Start();
}

function OpenTTDLLM::Start() {
    this.SetCompanyName();

    local last_command_timestamp = "";

    while (true) {
      require("commands.nut");
      local command_file = Commands();

      if (command_file.timestamp != last_command_timestamp) {
        last_command_timestamp = command_file.timestamp;
        AILog.Info("OpenTTDLLM < " + command_file.length.tostring() + " new commands received with timestamp: " + command_file.timestamp);
        foreach (command in command_file.commands) {
          local result = this.MatchCommand(command);
          if (result != null) {
            this.DataOutput(command_file.timestamp + "|" + command[0] + "|" + result);
          }
        }
      }

      this.Sleep(2);
    }
}

function OpenTTDLLM::DataOutput(message) {
    AILog.Info("OpenTTDLLM > " + message);
}

function OpenTTDLLM::SetCompanyName() {
  if(!AICompany.SetName("OpenTTDLLM")) {
    local i = 2;
    while(!AICompany.SetName("OpenTTDLLM #" + i)) {
      i = i + 1;
      if(i > 255) break;
    }
  }
  AICompany.SetPresidentName("P. Resident");
}

function OpenTTDLLM::MatchCommand(command) {
  switch (command[0]) {
    case "GetName":
      return AICompany.GetName(AICompany.COMPANY_SELF);
    case "GetBankBalance":
      return AICompany.GetBankBalance(AICompany.COMPANY_SELF);
    case "GetMapSize":
      return AIMap.GetMapSizeX() + "," + AIMap.GetMapSizeY();
    case "GetTile":
      return [command[1], command[2], AIMap.GetTile(command[1], command[2])];
    case "GetLoanAmount":
      return AICompany.GetLoanAmount();
    // case "GetEvents":
    //   local events = [];
    //   while (AIEventController.IsEventWaiting()) {
    //     events += AIEventController.GetNextEvent();a
    //   }
    //   return events;
    case "GetTowns":
      local towns = [];
      while (AITownList.Count() > 0) {
        towns += AITownList.Pop();
      }
      return towns;
    default:
      AILog.Info("OpenTTDLLM: Unknown command: " + command[0]);
      return null;
  }
}