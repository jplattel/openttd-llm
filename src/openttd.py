import subprocess
import os

class OpenTTD:
    def __init__(self):
        self.openttd_path_executable_path = os.getenv("OPEN_TTD_PATH_EXECUTABLE_PATH")
        self.process = None
        self.running = False
        self.log_file = open(os.getenv("OPEN_TTD_LOG_FILE"), "w")
        self.start_openttd()
        
        
    def start_openttd(self):
        # Start OpenTTD process with output redirected to file
        self.process = subprocess.Popen(
            [self.openttd_path_executable_path, "-g", "-d", "4"], 
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
