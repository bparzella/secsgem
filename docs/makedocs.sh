#!/bin/bash
#sphinx-apidoc -ePfF -H secsgem -A "Benjamin Parzella" -V 0.0 -R 0.0.3 -o .docsources ../secsgem
sphinx-build -b html .docsources .
#rm -fr _builddoc
