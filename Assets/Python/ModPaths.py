# coding: utf-8
"""
Resolve mod filesystem locations from this file's position (Assets/Python).
Works when the mod folder is renamed (e.g. Dawn-of-Civilization) or when
os.getcwd() is not the Civ4 install root.
"""
import os

_ASSETS_PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))


def get_mod_root():
	"""Directory containing Assets/, PrivateMaps/, etc."""
	return os.path.normpath(os.path.join(_ASSETS_PYTHON_DIR, os.pardir, os.pardir))


def get_assets_dir():
	"""Assets/ under the mod root."""
	return os.path.normpath(os.path.join(_ASSETS_PYTHON_DIR, os.pardir))


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
	"""Map editor image/text export tree at mod root (Export/)."""
	return os.path.join(get_mod_root(), "Export")
