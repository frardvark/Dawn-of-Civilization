from CvPythonExtensions import *


def null(cls, name, *args, **kwargs):
	def __init__(self, *args, **kwargs):
		cls.__init__(self, *args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return 0
	
	def __getattribute__(self, name):
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False
		
	funcs = (__init__, __call__, __getattribute__, __setattr__, __delattr__, __nonzero__)
	return type(name, (cls,), dict((func.__name__, func) for func in funcs))


NullCity = null(CyCity, "NullCity")


class _NullPlayerIterStub(object):
	"""CyPlayer.firstCity/nextCity/firstUnit/nextUnit return (CyXxx or None, iter). Core._iterate unpacks that; NullPlayer used to return self from __getattribute__, which caused TypeError: unpack non-sequence (MP-007)."""

	__slots__ = ()

	def __call__(self, *args, **kwargs):
		return (None, 0)


_nullplayer_iter_stub = _NullPlayerIterStub()

_null_player_singleton = None


def get_null_player():
	"""Singleton placeholder when a Civ has no player slot. Used by Core.player(); pickle-safe via __reduce__."""
	global _null_player_singleton
	if _null_player_singleton is None:
		_null_player_singleton = NullPlayer()
	return _null_player_singleton


class NullPlayer(CyPlayer):

	def __init__(self, *args, **kwargs):
		super(NullPlayer, self).__init__(*args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return self
	
	def __reduce__(self):
		return (get_null_player, ())
	
	def __getattribute__(self, name):
		if name in ("firstCity", "nextCity", "firstUnit", "nextUnit"):
			return _nullplayer_iter_stub
		# BugData pickles data.__dict__; cPickle looks up __getstate__/__reduce__ via instance __getattribute__.
		# Returning self for those breaks reduce (PicklingError: ... must be string or tuple).
		if len(name) > 4 and name[:2] == "__" and name[-2:] == "__":
			return object.__getattribute__(self, name)
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False


class NullTeam(CyTeam):

	def __init__(self, *args, **kwargs):
		super(NullTeam, self).__init__(*args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return self
	
	def __getattribute__(self, name):
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False


class Civ(int):

	def __new__(cls, value, *args, **kwargs):
		return super(cls, cls).__new__(cls, value)


NoCiv = Civ(-1)