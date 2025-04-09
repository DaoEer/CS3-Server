# -*- coding: utf-8 -*-
import imp

import Math
import KBEDebug
import KBEngine
import LoadModule
from Singleton import Singleton
from SmartImport import smartImport

PATH = "GameObject/SpaceObject"
HASHMAPPATH = "res/scripts/bots/PlayerAI/config/DT_HashMapCfg.json"
NPCPOINTDATAPATH = "res/scripts/bots/PlayerAI/config/NPCPointDatasTable.json"

class SpaceConfigMgr(Singleton):
	"""
	地图配置管理器
	"""
	def __init__(self):
		"""
		"""
		self._spacedct = {}			#所有地图配置
		self._spaceSpawndct = {}	#刷新点配置
		self._hashMap = {}	
		self._npcPointData = {}
		self.init()
		
	def init(self):
		"""
		"""
		objConfigs = LoadModule.openJsonPathCfg( PATH )
		for config in objConfigs:
			if config["scriptID"] in self._spacedct:
				KBEDebug.ERROR_MSG("space[%s] config has exists" %(config["scriptID"]))
				continue
				
			self._spacedct[ config["scriptID"] ] = config
			
		objConfig = LoadModule.openFile( HASHMAPPATH )
		for config in objConfig:
			if config["Name"] in self._hashMap:
				KBEDebug.ERROR_MSG("hashmap[%s] has exists" %(config["Name"]))
				return
		
			self._hashMap[config["Name"]] = config
			
		objConfig = LoadModule.openFile( NPCPOINTDATAPATH )
		for config in objConfig:
			if config["Name"] in self._npcPointData:
				KBEDebug.ERROR_MSG("space[%s] NPC POINT data has exists" %(config["Name"]))
				return
				
			self._npcPointData[config["Name"]] = config["NPCIDToPositions"]
			
	def getAllSpace(self):
		"""
		"""
		return self._spacedct
		
	def getHashMapCfg(self):
		"""
		"""
		return self._hashMap
		
	def getNPCPointBySpaceID(self, scriptID, npcID):
		"""
		"""
		data = self._npcPointData.get(scriptID, None)
		if data and npcID:
			for d in data:
				if d["NPCID"] == npcID:
					return Math.Vector3(d["Position"]["X"], d["Position"]["Y"], d["Position"]["Z"])
		return None
		
	def getNPCPointsBySpaceID(self, scriptID):
		"""
		"""
		return self._npcPointData.get(scriptID, None)
			
	def getSpaceCfgByScriptID(self, scriptID):
		"""
		"""
		return self._spacedct.get(scriptID, None)
		
	def getSpaceSpawnCfgByScriptID(self, scriptID):
		"""
		"""
		if scriptID not in self._spacedct:
			return None
			
		if scriptID not in self._spaceSpawndct:
			self.loadSpawnCfg(scriptID)
		return self._spaceSpawndct.get(scriptID, None)
			
	def loadSpawnCfg(self, scriptID):
		"""
		"""
		cfg = self._spacedct[scriptID]
		spawnFile = cfg.get("SpawnFile", None)
		if spawnFile:
			spawnDatas = smartImport( "GameObject.SpaceObject.SpawnFile." + spawnFile + ":" + "Datas" )
			self._spaceSpawndct[scriptID] = spawnDatas
		else:
			self._spaceSpawndct[scriptID] = None
			KBEDebug.ERROR_MSG("load space[%s] spawn error" %(scriptID))
			
g_spaceConfigMgr = SpaceConfigMgr()


	