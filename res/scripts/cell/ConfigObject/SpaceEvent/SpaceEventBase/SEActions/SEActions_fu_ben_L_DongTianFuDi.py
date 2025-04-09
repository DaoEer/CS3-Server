# -*- coding: utf-8 -*-

# 副本事件行为
import random
import KBEMath
import KBEDebug
import KBEngine
import Functions
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction407( SEActionBase ):
	"""
	洞天福地副本通关成功/失败	
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
			
class SEAction408( SEActionBase ):
	"""
	洞天福地副本创建boss
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
		_probability = 0
		self.probabilityandLevelList  = []
		for s in section["param1"].split('|'):
			ss = s.split(':')
			if len(ss) != 2:
				KBEDebug.ERROR_MSG("config error, probability and level")
				continue
			
			probability = float(ss[0])
			_probability += probability
			self.probabilityandLevelList.append((probability, int(ss[1])))
		
		if _probability > 100:
			KBEDebug.ERROR_MSG("config error, probability over 100")
		
		self.scriptIDList = []
		for s in section['param2'].split(':'):
			lst = [id for id in s.split('|') if id]
			if len(lst) <= 0:
				KBEDebug.ERROR_MSG("config error, scriptIDList")
				continue
			self.scriptIDList.append(lst)
			
		self.positionList = []
		for position in section["param3"].split("|"):
			pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(position))
			self.positionList.append(pos)
		
		self.directionList = []
		for direction in section["param4"].split("|"):
			dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(direction))
			self.directionList.append(dir)
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		if len(self.positionList) != len(self.directionList):
			KBEDebug.ERROR_MSG("config error, direction and position")
			return
		
		if len(self.probabilityandLevelList) != len(self.scriptIDList):
			KBEDebug.ERROR_MSG("config error, scriptID and probabilityandLevel")
			return
		
		_probability = 0.0
		__probability = random.uniform(1, 100)
		for index, probabilityandlevel in enumerate(self.probabilityandLevelList):
			_probability += probabilityandlevel[0]
			if __probability < _probability:
				continue
			
			scriptID = random.choice(self.scriptIDList[index])
			pos = self.positionList[index] if len(self.positionList) > 1 else self.positionList[0]
			dir = self.directionList[index] if len(self.directionList) > 1 else self.directionList[0]
			level = spaceEntity.createArgs.get("level", 0) + probabilityandlevel[1] #比当前进入的玩家高多少级
			spaceEntity.createEntityByScriptID(scriptID, pos, dir, {"spawnPos":pos, "spawnDir": dir, "level": level})
			return
		
SEActionBase.setActionClass("SEAction407", SEAction407)
SEActionBase.setActionClass("SEAction408", SEAction408)
