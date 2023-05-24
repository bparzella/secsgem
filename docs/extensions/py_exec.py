import io
import logging
import os.path
import sys

import docutils.parsers.rst


class ExecDirective(docutils.parsers.rst.Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    def run(self):
        oldStdout, sys.stdout = sys.stdout, io.StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

        try:
            exec('\n'.join(self.content))
            text = sys.stdout.getvalue()
            lines = docutils.statemachine.string2lines(text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [docutils.nodes.error(None, docutils.nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (os.path.basename(source), self.lineno)), docutils.nodes.paragraph(text = str(sys.exc_info()[1])))]
        finally:
            sys.stdout = oldStdout


def setup(app):
    app.add_directive('exec', ExecDirective)