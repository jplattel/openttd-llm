import subprocess


class OpenTTD:
    def __init__(self, log_file):
        self.process = None
        self.running = False
        self.log_file = open(log_file, "w")
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
