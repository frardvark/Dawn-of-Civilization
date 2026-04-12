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
	path = get_private_maps_txt_path(mapName)
	parser = MapParser()
	rc = parser.read(path)
	if rc != 0:
		raise IOError(
			"DoC: could not load base worldbuilder map %r (read returned %s). "
			"Copy the mod's PrivateMaps folder next to Assets in the same mod directory."
			% (path, rc)
		)
	if parser.mapDesc.iGridW <= 0 or parser.mapDesc.iGridH <= 0:
		raise IOError(
			"DoC: base map %s has invalid grid size %sx%s."
			% (path, parser.mapDesc.iGridW, parser.mapDesc.iGridH)
		)
	return parser

def parseScenarioMap(scenario):
	parser = parseBaseMap()
	base_w = parser.mapDesc.iGridW
	base_h = parser.mapDesc.iGridH
	scen_path = get_private_maps_txt_path(scenario.fileName)
	rc = parser.read(scen_path)
	if rc != 0:
		raise IOError(
			"DoC: could not load scenario map %s (read returned %s)."
			% (scen_path, rc)
		)
	if parser.mapDesc.iGridW <= 0 or parser.mapDesc.iGridH <= 0:
		parser.mapDesc.iGridW = base_w
		parser.mapDesc.iGridH = base_h
	return parser