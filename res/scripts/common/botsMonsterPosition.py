# -*- coding: utf-8 -*-
import csconst
import os
import json
import SmartImport
import LoadModule

SPACEPATH = "GameObject/SpaceObject"
SPAWNPATH = "GameObject/SpaceObject/SpawnFile"
GET_GAME_CONFIG = lambda dir : csconst.CONFIG_PATCH + SPAWNPATH
PATH = "res/scripts/bots/BotTasks/config"
FILE_TYPE = ".py"

def loadConfig( spawnFiles ):
	cfg = {}
	for fileName in spawnFiles:
		cfg[fileName] = {}
		spawnDatas = SmartImport.smartImport( "GameObject.SpaceObject.SpawnFile." + fileName + ":" + "Datas" )
		for spawnData in spawnDatas.values():
			if spawnData["scriptID"] in cfg[ fileName ]:
				continue
			else:
				cfg[ fileName ][ spawnData["scriptID"] ] = spawnData["position"]
	#转换编码写入文件
	#cfgText = cfg.decode()
	cfgStr = json.dumps(cfg)
	cfgStr = cfgStr.replace("],", "],\n")
	file = open(os.path.join(PATH,"monsterPosition.py"),"w")
	file.write("Datas=")
	file.write( cfgStr )
	file.close()


def loadObject():
	global g_objectDict
	objConfigs = LoadModule.openJsonPathCfg( SPACEPATH )
	cfg = {}
	for config in objConfigs:
		scriptID = config[ "scriptID" ]
		if "SpawnFile" not in config.keys():
			continue
		spawnFile = config["SpawnFile"]
		if not spawnFile:
			continue
		cfg[scriptID]={}
		spawnDatas = SmartImport.smartImport( "GameObject.SpaceObject.SpawnFile." + spawnFile + ":" + "Datas" )
		for spawnData in spawnDatas.values():
			if spawnData["scriptID"] in cfg[ scriptID ]:
				continue
			else:
				cfg[ scriptID ][ spawnData["scriptID"] ] = spawnData["position"]
	cfgStr = json.dumps(cfg)
	cfgStr = cfgStr.replace("],", "],\n")
	file = open(os.path.join(PATH,"monsterPosition.py"),"w")
	file.write("Datas=")
	file.write( cfgStr )
	file.close()
	print("Load monster position finished!")



def openConfigPath( configPath ):
	"""
	加载文件夹下的所有文件名
	"""
	fileBbjDict = []
	configPath = GET_GAME_CONFIG( configPath )
	if os.path.isdir( configPath ):
		for file in os.listdir( configPath ):
			filePath = configPath + "/" + file
			if os.path.isfile( filePath ) and os.path.splitext(filePath)[1] == FILE_TYPE:
				fileBbjDict.append( file.rsplit("/")[-1].rsplit(".")[0] )
	return fileBbjDict


loadObject()

#loadConfig( openConfigPath("SpawnFile") )