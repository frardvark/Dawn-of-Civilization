from Core import *
from RFCUtils import *
from Parsers import *
from Scenarios import *

import Rise, RegionMap

# Map script may call hooks before getGridSize in some paths; prepareMap() can also
# abort before assignment if PARSER parse fails — never leave PARSER undefined.
PARSER = None


def _ensure_parser():
	global PARSER
	if PARSER is None:
		prepareMap()


lStartingDates = [
	"3000 BC",
	"600 AD",
	"1500 AD",
	"1700 AD",
]


lCustomMapOptions = [
	("Starting Date", lStartingDates, lStartingDates[0]),
]


def getDescription():
	return "Dawn of Civilization"

def getNumCustomMapOptions():
	return len(lCustomMapOptions)

def getCustomMapOptionName(args):
	iOption = args[0]
	
	option_names = dict((i, name) for i, (name, _, _) in enumerate(lCustomMapOptions))
	option_name = option_names[iOption]
	return unicode(option_name)

def getNumCustomMapOptionValues(args):
	iOption = args[0]

	option_values = dict((i, len(options)) for i, (_, options, _) in enumerate(lCustomMapOptions))
	return option_values[iOption]

def getCustomMapOptionDescAt(args):
	iOption, iSelection = args
	
	selection_names = dict((i, dict((j, name) for j, name in enumerate(options))) for i, (_, options, _) in enumerate(lCustomMapOptions))
	selection_name = selection_names[iOption][iSelection]
	return unicode(selection_name)

def getCustomMapOptionDefault(args):
	iOption = args[0]
	
	option_defaults = dict((i, options.index(default)) for i, (_, options, default) in enumerate(lCustomMapOptions))
	return option_defaults[iOption]

def isRandomCustomMapOption(args):
	return 0

def isAdvancedMap():
	return 0

def prepareMap():
	global PARSER
	
	loadScenario()
	PARSER = parseScenarioMap(scenario)

def loadScenario():
	global scenario
	scenario = getScenario()

def getGridSize(args):
	if args[0] == -1:
		return []
	
	prepareMap()
	
	w = int(PARSER.mapDesc.iGridW)
	h = int(PARSER.mapDesc.iGridH)
	if w <= 0 or h <= 0:
		raise RuntimeError(
			"DoC getGridSize: invalid WB grid %sx%s (base map failed to load or PrivateMaps missing). "
			"Ensure PrivateMaps/RFC_Earth.txt exists under the mod root (same folder as Assets)."
			% (w, h)
		)
	# Terrain cell counts for CvMap (RFC_Earth uses plot counts divisible by 4).
	cw = max(1, w // 4)
	ch = max(1, h // 4)
	return cw, ch

def beforeGeneration():
	_ensure_parser()
	data.setup()
	PARSER.prepare()

def generateRandomMap():
	_ensure_parser()
	PARSER.applyPlotTypes()
	PARSER.applyTerrainTypes()

def addFeatures():
	_ensure_parser()
	PARSER.applyFeatures()

def addBonuses():
	_ensure_parser()
	PARSER.applyBonuses()

def addRivers():
	_ensure_parser()
	PARSER.applyRivers()

def addGoodies():
	return

def initRiseAndFall():
	Rise.initMaps()
	RegionMap.init()
	
def afterGeneration():
	_ensure_parser()
	initRiseAndFall()
	scenario.init()
	PARSER.applyDevelopment()
	scenario.apply()
	
def findStartingPlot(args):
	iPlayer = args[0]
	startingPlot = is_minor(iPlayer) and plot(0, 0) or plots.capital(civ(iPlayer))
	
	return map.plotNum(startingPlot.getX(), startingPlot.getY())

def addLakes():
	return 0

def normalizeRemovePeaks():
	return 0

def normalizeRemoveBadFeatures():
	return 0

def normalizeRemoveBadTerrain():
	return 0
	
def normalizeAddFoodBonuses():
	return 0

def normalizeAddGoodTerrain():
	return 0

def startHumansOnSameTile():
	return 0
	
def normalizeStartingPlotLocations():
	return 0

def normalizeAddRiver():
	return 0

def normalizeAddLakes():
	return 0

def normalizeAddExtras():
	return 0

def isSeaLevelMap():
	return 0

def isClimateMap():
	return 0

