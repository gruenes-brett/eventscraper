
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import activate_venv

from uscrapeme.apiserver import server as application
