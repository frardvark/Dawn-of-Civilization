# coding: utf-8
"""
Resolve mod filesystem locations. Civ4 often exposes __file__ relative to the
install root; abspath(__file__) then lands under Beyond the Sword instead of
Mods\\<mod>\\Assets\\Python. We locate Assets by finding Assets\\Maps\\Cities.csv
via sys.path, or by scanning Mods\\* when cwd is the BtS root.
"""
import os
import sys
import json
import time

# #region agent log
def _agent_log(hypothesis_id, location, message, data=None):
	try:
		line = json.dumps({
			"sessionId": "e0b5b6",
			"hypothesisId": hypothesis_id,
			"location": location,
			"message": message,
			"data": data or {},
			"timestamp": int(time.time() * 1000),
		})
		for p in (
			os.path.join(os.environ.get("TEMP", "."), "debug-e0b5b6.log"),
			os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "debug-e0b5b6.log"),
		):
			try:
				with open(os.path.normpath(p), "a") as f:
					f.write(line + "\n")
				break
			except Exception:
				continue
	except Exception:
		pass
# #endregion


def _maps_cities_path_for_assets_python(py_dir):
	assets = os.path.normpath(os.path.join(py_dir, os.pardir))
	return os.path.join(assets, "Maps", "Cities.csv")


def _resolve_assets_python_dir():
	# H1: abspath(__file__) anchored to wrong cwd -> vanilla Beyond the Sword\Assets\Python
	raw = __file__
	d0 = os.path.dirname(os.path.abspath(__file__))
	c0 = _maps_cities_path_for_assets_python(d0)
	_agent_log(
		"H1",
		"ModPaths._resolve_assets_python_dir:primary",
		"primary candidate",
		{"raw_file": raw, "d0": d0, "c0": c0, "c0_exists": os.path.isfile(c0), "cwd": os.getcwd()},
	)
	if os.path.isfile(c0):
		return d0
	# H3: real mod Assets/Python is on sys.path but __file__ resolved wrong
	for entry in sys.path:
		if not entry or not isinstance(entry, basestring):
			continue
		ap = os.path.normpath(os.path.abspath(entry))
		cand_py = ap
		cand_csv = _maps_cities_path_for_assets_python(cand_py)
		if os.path.isfile(cand_csv):
			_agent_log(
				"H3",
				"ModPaths._resolve_assets_python_dir:sys_path_py",
				"matched Assets/Python via sys.path",
				{"entry": entry, "chosen": cand_py},
			)
			return cand_py
		alt_csv = os.path.join(ap, "Assets", "Maps", "Cities.csv")
		if os.path.isfile(alt_csv):
			chosen = os.path.join(ap, "Assets", "Python")
			_agent_log(
				"H3",
				"ModPaths._resolve_assets_python_dir:sys_path_modroot",
				"matched mod root via sys.path",
				{"entry": entry, "chosen": chosen},
			)
			return chosen
	# H5: import-time sys.path incomplete; cwd is BtS root — scan Mods\*
	mods_dir = os.path.join(os.path.abspath(os.getcwd()), "Mods")
	if os.path.isdir(mods_dir):
		try:
			for name in os.listdir(mods_dir):
				mod_root = os.path.join(mods_dir, name)
				if not os.path.isdir(mod_root):
					continue
				cities = os.path.join(mod_root, "Assets", "Maps", "Cities.csv")
				self_modpaths = os.path.join(mod_root, "Assets", "Python", "ModPaths.py")
				if os.path.isfile(cities) and os.path.isfile(self_modpaths):
					chosen = os.path.join(mod_root, "Assets", "Python")
					_agent_log(
						"H5",
						"ModPaths._resolve_assets_python_dir:mods_scan",
						"matched via Mods folder scan",
						{"mod_root": mod_root, "chosen": chosen},
					)
					return chosen
		except Exception as ex:
			_agent_log("H5", "ModPaths._resolve_assets_python_dir:mods_scan_err", str(ex), {})
	_agent_log(
		"H1",
		"ModPaths._resolve_assets_python_dir:fallback",
		"fell back to abspath(__file__) dir (Cities.csv missing everywhere)",
		{"d0": d0},
	)
	return d0


_resolved_assets_python = None


def _get_assets_python_dir():
	global _resolved_assets_python
	if _resolved_assets_python is None:
		_resolved_assets_python = _resolve_assets_python_dir()
		_agent_log(
			"H4",
			"ModPaths._get_assets_python_dir",
			"lazy final _ASSETS_PYTHON_DIR",
			{
				"_ASSETS_PYTHON_DIR": _resolved_assets_python,
				"get_mod_root": os.path.normpath(
					os.path.join(_resolved_assets_python, os.pardir, os.pardir)
				),
				"maps_cities": _maps_cities_path_for_assets_python(_resolved_assets_python),
			},
		)
	return _resolved_assets_python


def get_mod_root():
	"""Directory containing Assets/, PrivateMaps/, etc."""
	d = _get_assets_python_dir()
	return os.path.normpath(os.path.join(d, os.pardir, os.pardir))


def get_assets_dir():
	"""Assets/ under the mod root."""
	d = _get_assets_python_dir()
	return os.path.normpath(os.path.join(d, os.pardir))


def get_maps_file_path(relative_under_maps):
	"""
	Path under Assets/Maps/. relative_under_maps uses '/' or os.sep
	(e.g. 'Settler/Misr.csv', 'Export/BaseTerrain.csv').
	"""
	rel = relative_under_maps.replace("/", os.sep)
	return os.path.join(get_assets_dir(), "Maps", rel)


def get_private_maps_txt_path(stem_without_extension):
	"""Scenario text map in PrivateMaps/ (e.g. RFC_Earth -> RFC_Earth.txt)."""
	return os.path.join(get_mod_root(), "PrivateMaps", stem_without_extension + ".txt")


def get_mod_export_dir():
	"""World builder / map editor export tree at mod root (Export/)."""
	return os.path.join(get_mod_root(), "Export")
