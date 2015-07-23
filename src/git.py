import utils

def _run_git(path, *args):
    return utils.run(("git",) + args, path).rstrip("\n")

def toplevel_path(path):
    return _run_git(path, "rev-parse", "--show-toplevel")

def ls_files(path):
    return _run_git(path, "ls-files", path).split("\n")

def branch_name(path):
    try:
        return _run_git(path, "rev-parse", "--abbrev-ref", "HEAD")
    except utils.ProgramException:
        return "<Unknown>"

def status(path):
    return _run_git(path, "status", "-uno", "--porcelain").split("\n")

def status_for_file(path, file_path):
    return _run_git(path, "status", "--porcelain", file_path)[:2]

def add_file(path, file_path):
    return _run_git(path, "add", file_path)

def version():
    return _run_git(None, "--version")
