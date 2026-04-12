# coding: utf-8
"""
Optional multiplayer desync tracing. Set MP_SYNC_DEBUG True on every client
for one repro, compare CvUtil.pyPrint output, then set back to False.
"""
MP_SYNC_DEBUG = False


def on_begin_player_turn(iGameTurn, iPlayer):
	if not MP_SYNC_DEBUG:
		return
	from CvPythonExtensions import CyGlobalContext
	import CvUtil

	gc = CyGlobalContext()
	game = gc.getGame()
	iActive = game.getActivePlayer()
	bMp = game.isGameMultiPlayer()
	CvUtil.pyPrint(
		"[MP_SYNC_DEBUG] turn=%d beginPlayer=%d activePlayer=%d multiplayer=%d"
		% (iGameTurn, iPlayer, iActive, int(bMp))
	)
