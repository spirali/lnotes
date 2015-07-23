import subprocess
import os

class ProgramException(Exception):

    def __init__(self, args, stderr):
        self.args = args
        self.stderr = stderr
        Exception.__init__(self, "Execution of '{0}' failed.\n{1}".format(self.args, self.stderr))

def run(args, cwd=None):
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise ProgramException(args, stderr)
        return stdout
    except OSError as e:
        raise ProgramException(args, str(e))

def run_detach(args):
    os.system(" ".join(args))
    #os.spawnl(os.P_NOWAIT, args)
