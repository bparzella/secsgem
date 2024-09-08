# Sphinx configuration file for secsgem

import sys
import os
import os.path
import pathlib

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "extensions")))

config_path = pathlib.Path(__file__).parent.resolve()

project = u'secsgem'
copyright = u'2015-2024, Benjamin Parzella'

version = '0.3'
release = '0.3.0-beta.1'

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'myst_parser',
    'py_exec',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.plantuml'
]

templates_path = ['_templates']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

html_theme = 'sphinx_rtd_theme'

exclude_patterns = ['_build']

autodoc_default_flags = ["members", "undoc-members", "show-inheritance", "inherited-members"]
autodoc_member_order = "bysource"

plantuml_path = config_path / "bin" / "plantuml.jar"
plantuml = f"java -jar {plantuml_path}"
plantuml_output_format = "svg"

myst_heading_anchors = 3
