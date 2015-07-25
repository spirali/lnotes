from flask import Flask, render_template, redirect
import os
import sys
import git
from render import renderers
import utils

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SRC_DIR, "templates")
STATIC_DIR = os.path.join(SRC_DIR, "static")

TOPLEVEL = None
CONFIG = None

app = Flask(__name__,
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)
#app.debug = True

@app.route("/")
def start():
    return redirect("/start")

@app.route("/favicon.ico")
def facicon():
    return ""

@app.route("/tree")
def tree():
    paths = []
    for item in git.status(TOPLEVEL):
        status = item[:2]
        f = item[3:]
        print f
        for renderer in renderers:
            if f.endswith(renderer.extension):
                break
        else:
            continue
        file_path = os.path.join(os.path.join(TOPLEVEL, f))
        if os.path.isfile(file_path):
            paths.append(("/" + f[:f.rfind(".")], status))
    paths.sort()

    args = {
        "title": "/tree :: lnotes",
        "path" : "/tree",
        "file_path": "--",
        "git_status" : "--",
        "git_branch" : git.branch_name(TOPLEVEL),
        "style_files" : ("asciidoc.css",),
        "paths" : paths,
    }
    return render_template("tree.html", **args)

def get_renderer(path):
    # TODO: Check if path contains only [a-zA-Z0-9_-]
    for renderer in renderers:
        p = os.path.join(TOPLEVEL, path + renderer.extension)
        if os.path.isfile(p):
            return renderer(p, path)

def render_page(path):
    renderer = get_renderer(path)

    args = {
        "title": "/" + path + " :: lnotes",
        "path": "/" + path,
        "git_branch" : git.branch_name(TOPLEVEL),
    }


    if renderer is None:
        args["file_path"] = os.path.join(TOPLEVEL, path)
        args["git_status"] = "--"
        args["renderers"] = renderers
        args["style_files"] = ("asciidoc.css",)
        return render_template("notfound.html", **args)

    args["file_path"] = renderer.file_path
    args["content"] = renderer.render()
    args["style_files"] = renderer.style_files
    args["is_editable"] = True,
    git_status = git.status_for_file(TOPLEVEL, renderer.file_path)
    if git_status == "":
        git_status = "up-to-date"
    args["git_status"] = git_status
    return render_template("page.html", **args)


@app.route("/<path:path>/.create")
def create_page(path):
    if "." not in path:
        raise Exception("Invalid path")
    file_path = os.path.join(TOPLEVEL, path)
    directory = os.path.dirname(file_path)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            f.write("\nHello world!\n")
    git.add_file(TOPLEVEL, file_path)
    return redirect("/" + path[:path.rfind(".")] + "/.edit")

@app.route("/<path:path>/.edit")
def edit_page(path):
    renderer = get_renderer(path)
    utils.run_detach((CONFIG.get("PROGRAMS", "editor"), renderer.file_path))
    return redirect(renderer.path)

@app.route("/<path:path>/.terminal")
def run_terminal(path):
    utils.run_detach((CONFIG.get("PROGRAMS", "terminal"),))
    return redirect("/" + path)

@app.route("/<path:path>/.git")
def git_view(path):
    return "Not implemented yet"

@app.route("/<path:path>")
def view_page(path):
    return render_page(path)

def check_git():
    print "Git checking ...",
    try:
        print git.version()
    except utils.ProgramException as e:
        print str(e)
        sys.exit(0)

def read_or_make_config():
    import ConfigParser
    c = ConfigParser.RawConfigParser()
    c.add_section("SERVER")
    c.set("SERVER", "port", 7722)
    c.add_section("PROGRAMS")
    c.set("PROGRAMS", "editor", "gvim")
    c.set("PROGRAMS", "terminal", "gnome-terminal")
    config_file = os.path.join(TOPLEVEL, ".lnotes.conf")
    if not os.path.isfile(config_file):
        print "Writing '{0}'".format(config_file)
        with open(config_file, "w") as f:
            c.write(f)
    else:
        print "Reading '{0}'".format(config_file)
        with open(config_file) as f:
            c.readfp(f)
    return c

def init():
    check_git()
    global TOPLEVEL, CONFIG
    try:
        TOPLEVEL = git.toplevel_path(None)
        print "Git repostory ...", TOPLEVEL
    except utils.ProgramException as e:
        print "Working directory does not look like a git repository. Git says:"
        print e.stderr
        sys.exit(0)
    CONFIG = read_or_make_config()

def main():
    app.run(port=CONFIG.getint("SERVER", "port"))


