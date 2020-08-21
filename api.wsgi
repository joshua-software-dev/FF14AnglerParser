#! /usr/bin/env python3

import sys
import os


dir_name = os.path.dirname(__file__)
sys.path.append(dir_name)
sys.path.append(os.path.join(os.path.dirname(__file__), 'dependencies'))


from ff14angler.apiServer.application import application
