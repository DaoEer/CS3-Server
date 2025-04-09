# -*- coding: utf-8 -*-
import sys
import imp
import os 
import csconst

import SmartImport

g_datas = {}

from MonsterAI import FSMDatas
DIR_PATH = csconst.CONFIG_PATCH+"npctalk"

def getSourceConfig( scriptID ):
	global g_datas
	if scriptID not in g_datas:
		g_datas[ scriptID  ] = SmartImport.smartImport("npctalk.%s"%scriptID)
	
	return g_datas[ scriptID  ]

def reloadSourceConfig( scriptID ):
	global g_datas
	if scriptID in g_datas:
		g_datas[ scriptID  ] = imp.reload( g_datas[ scriptID  ] )
	else:
		getSourceConfig( scriptID )
		
	return g_datas[ scriptID  ]
	