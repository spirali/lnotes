from jinja2 import Markup
import utils

class Renderer(object):

    style_files = ("asciidoc.css",)
    initial_content = ""

    def __init__(self, file_path, path):
        self.path = path
        self.file_path = file_path


class TextRenderer(Renderer):

    extension = ".txt"
    name = "Plan text"

    def render(self):
        with open(self.file_path) as f:
            content = f.read().decode("UTF-8")
        return Markup("<pre>{}</pre>".format(Markup.escape(content)))


class ExternalRenderer(Renderer):

    def render(self):
        string = utils.run(self.get_args())
        return Markup(string.decode("UTF-8"))


class MarkdownRenderer(ExternalRenderer):

    extension = ".md"
    name = "Markdown"

    def get_args(self):
        return ("markdown", self.file_path)


class AsciidocRenderer(ExternalRenderer):

    extension = ".adoc"
    name = "Asciidoc"

    def get_args(self):
        return ("asciidoctor", "-a", "notitle!", "-s", "-o", "-", self.file_path)


renderers = [ AsciidocRenderer,
              MarkdownRenderer,
              TextRenderer ]
