# -*- coding: utf-8 -*-
import imp
import SmartImport

g_datas = {}

def getSourceConfig( scriptID ):
	mod = SmartImport.smartImport("SpellBoxAdvancedState.%s"%scriptID)
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
		print( "load SpellBoxAdvancedState (%s) failure!!!"%scriptID )
	
	if config:
		return config.Datas
	else:
		return None