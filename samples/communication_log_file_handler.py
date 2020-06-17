#####################################################################
# communication_log_file_handler.py
#
# (c) Copyright 2016, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################

import os
import logging

class CommunicationLogFileHandler(logging.Handler):
    def __init__(self, path, prefix=""):
        logging.Handler.__init__(self)

        self.path = path
        self.prefix = prefix

    def emit(self, record):
        filename = os.path.join(self.path, "{}com_{}.log".format(self.prefix, record.remoteName))
        os.makedirs(os.path.dirname(filename), exist_ok=True)        
        with open(filename, 'a') as f:
            f.write(self.format(record) + "\n")
