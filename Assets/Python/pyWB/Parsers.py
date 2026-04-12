from MapParser import *

import os
import sys

# Ensure Assets/Python is importable when pyWB is run as a script
_pyDir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
if _pyDir not in sys.path:
	sys.path.insert(0, _pyDir)

from ModPaths import get_private_maps_txt_path


def parseBaseMap():
	mapName = "RFC_Earth"
	parser = MapParser()
	parser.read(get_private_maps_txt_path(mapName))
	return parser

def parseScenarioMap(scenario):
	parser = parseBaseMap()
	parser.read(get_private_maps_txt_path(scenario.fileName))
	return parser