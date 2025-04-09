# -*- coding: utf-8 -*-
import random, Math

import KBEngine
import KBEDebug

import KST_Config
import Extra.Extend as Extend
from PlayerAI.State.CStateInterface import CStateBase
from Extra.SpaceConfigMgr import g_spaceConfigMgr

class CTeleport(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callBackID = 0
		
	def enter(self):
		self._teleport()
		
	def leave(self):
		self.reset()
		
	def reEnter(self):
		self.reset()
		self._teleport()
		
	def reset(self):
		if self.callBackID:
			KBEngine.cancelCallback(self.callBackID)
			self.callBackID = 0
		
	def _teleport(self):
		"""
		"""
		if self.ai.space_test is None:
			KBEDebug.ERROR_MSG("space error")
			return
		
		currentSpace = self.ai.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if currentSpace == self.ai.space_test[1]:
			self.ai.think()
			return
			
		spaceCfg = g_spaceConfigMgr.getSpaceCfgByScriptID(self.ai.space_test[1])
		if spaceCfg is None:
			KBEDebug.ERROR_MSG("space[%s] cfg is None" %(self.ai.space_test[1]))
			return
			
		spawnCfg = g_spaceConfigMgr.getSpaceSpawnCfgByScriptID(self.ai.space_test[1])
		if spawnCfg is None:
			KBEDebug.ERROR_MSG("not found space[%s] spawn" %(self.ai.space_test[1]))
			return

		loop = 0
		cfg = None
		while 1:
			index = random.choice(list(spawnCfg.keys()))
			cfg = spawnCfg.get(index, None)
			if cfg: break
			if loop <= 50:
				loop += 1
				continue
			
			KBEDebug.ERROR_MSG("space[%s] spawn is None" %(self.ai.space_test[1]))
			return
		
		position = cfg.get("position", None)
		if position is None:
			KBEDebug.ERROR_MSG("space[%s] position is None" %(self.ai.space_test[1]))
			return
		
		uepos = Extend.KBEngine2UnrealPosition(Math.Vector3(position))
		posStr = "%s %s %s" %(uepos[0], uepos[1], uepos[2])
		if spaceCfg["EntityType"] == "SpaceCopy" and spaceCfg.get("bunchSpaceScriptID", ""):
			self.ai.owner.GMCommand(self.ai.owner, "gotoBunch", "{} {} {}".format(spaceCfg.get("bunchSpaceScriptID", ""), self.ai.space_test[1], posStr))
		else:
			self.ai.owner.GMCommand(self.ai.owner, "goto", "{} {}".format(self.ai.space_test[1], posStr))
		self.callBackID = KBEngine.callback(60, self.onTeleport)
		
	def onTeleport(self):
		self.callBackID = 0
		self._teleport()

class CTeleportRepeat(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
		self.spaceScriptIDs = []
		if KST_Config.teleport_map_random:
			hashmap = g_spaceConfigMgr.getHashMapCfg()
			for scriptID, cfg in g_spaceConfigMgr.getAllSpace().items():
				if cfg["scriptID"] in hashmap and cfg["EntityType"] in ["SpaceMultiLine", "SpaceCopy"]:
					self.spaceScriptIDs.append(scriptID)
		else:
			for k, v in KST_Config.teleport_maps.items():
				if v[2]:
					self.spaceScriptIDs.append(k)
					
		self.callBackID = 0
		
	def enter(self):
		pass
		
	def leave(self):
		if self.callBackID:
			KBEngine.cancelCallback(self.callBackID)
			self.callBackID = 0
		
	def onTickCallBack(self, tick):
		if KST_Config.teleport_map_random:
			self.onTeleportRandom()
		else:
			self.onTeleport()
		
	def onTeleport(self):
		"""
		配置的指定地图间切换
		"""
		spaceScriptIDs = list(self.spaceScriptIDs)
		spaceScriptID = self.ai.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")

		if spaceScriptID in spaceScriptIDs:
			spaceScriptIDs.remove(spaceScriptID)
		
		if len(spaceScriptIDs) <= 0:
			KBEDebug.ERROR_MSG("CTeleportRepeat, teleport maps error")
			return
		
		spaceScriptID = random.choice(spaceScriptIDs)
		spaceInfo = KST_Config.teleport_maps[spaceScriptID]
		self.ai.owner.GMCommand(self.ai.owner, "goto", "{} {}".format(spaceInfo[0], spaceInfo[1]))
		
	def onTeleportRandom(self):
		"""
		随机切换地图
		"""
		spaceList = list(self.spaceScriptIDs)
		spaceScriptID = self.ai.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if spaceScriptID in spaceList:
			spaceList.remove(spaceScriptID)
		
		if len(spaceList) <= 0:
			KBEDebug.ERROR_MSG("not found space")
			return
			
		spaceScriptID = random.choice(spaceList)
		spaceCfg = g_spaceConfigMgr.getSpaceCfgByScriptID(spaceScriptID)
		if spaceCfg is None:
			KBEDebug.ERROR_MSG("space[%s] cfg is None" %(spaceScriptID))
			return
		
		spawnCfg = g_spaceConfigMgr.getSpaceSpawnCfgByScriptID(spaceScriptID)
		if spawnCfg is None:
			KBEDebug.WARNING_MSG("not found space[%s] spawn" %(spaceScriptID))
			self.addCallBack()
			return
		
		cfg = spawnCfg.get(0, None)
		if cfg is None:
			KBEDebug.WARNING_MSG("space[%s] spawn is None" %(spaceScriptID))
			self.addCallBack()
			return
			
		position = cfg.get("position", None)
		if position is None:
			KBEDebug.ERROR_MSG("space[%s] position is None" %(spaceScriptID))
			return
	
		posStr = "%s %s %s" %(position[0], position[1], position[2])
		if spaceCfg["EntityType"] == "SpaceCopy" and spaceCfg.get("bunchSpaceScriptID", ""):
			self.ai.owner.GMCommand(self.ai.owner, "gotoBunch", "{} {} {}".format(spaceCfg.get("bunchSpaceScriptID", ""), spaceScriptID, posStr))	
		else:
			self.ai.owner.GMCommand(self.ai.owner, "goto", "{} {}".format(spaceScriptID, posStr))	
	
	def addCallBack(self):
		"""
		"""
		if self.callBackID:
			KBEngine.cancelCallback(self.callBackID)
		self.callBackID = KBEngine.callback(0.1, self.ai.think)