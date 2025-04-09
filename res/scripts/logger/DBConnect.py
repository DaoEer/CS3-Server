# -*- coding: utf-8 -*-

import Settings

from KBEDebug import *
from DBConnector import DBConnector


"""
"""
db = None
def getCsol3LogDB():
	global db
	if not db:
		try:
			db = DBConnector( **Settings.DB_GAME_LOG_CSOL )
		except:
			INFO_MSG("connect db error")
	return db
		