# -*- coding: utf-8 -*-
import sys
import imp
import csconst

from MonsterAI import FSMDatas

import SmartImport

g_datas = {}


def getSourceConfig( scriptID ):
	mod = SmartImport.smartImport("MonsterAI.%s"%scriptID)
	return imp.reload(mod)
	
def getConfig( scriptID ):
	global g_datas
	if scriptID not in g_datas:
		g_datas[ scriptID ] = getSourceConfig( scriptID )
	
	config = g_datas[scriptID]
	
	if config:
		return config.Datas
	else:
		return None


def reloadConfig( scriptID ):
	try:
		global g_datas
		config = getSourceConfig( scriptID )
		g_datas[ scriptID ] = config
	except:
		print( "load monster (%s) AI failure!!!"%scriptID )
	
	if config:
		return config.Datas
	else:
		return None