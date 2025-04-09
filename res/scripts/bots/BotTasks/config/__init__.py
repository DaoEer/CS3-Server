# -*- coding: utf-8 -*-
import sys
import imp
import csconst


def getSourceConfig( taskCfg ):
	cfgPach = "res/scripts/bots/BotTasks/config/%s.py"%taskCfg
	return imp.load_source(taskCfg, cfgPach)
	
def getConfig( taskCfg ):
	config = None
	if taskCfg in sys.modules:
		config = sys.modules[taskCfg]
	else:
		try:
			config = getSourceConfig( taskCfg )
		except:
			print( "======> load monster (%s) AI failure!!!"%taskCfg )
		
	if config:
		return config.Datas
	else:
		return None

def reloadConfig( taskCfg ):
	try:
		config = getSourceConfig( taskCfg )
	except:
		print( "======> load monster (%s) AI failure!!!"%taskCfg )
	
	if config:
		return config.Datas
	else:
		return None