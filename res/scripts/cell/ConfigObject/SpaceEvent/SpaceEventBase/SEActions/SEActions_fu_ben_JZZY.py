# -*- coding: utf-8 -*-

# 副本事件行为  九字真言
import Math
import Define
import csdefine
import random
import KBEMath
import KBEDebug
import KBEngine
import Functions
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase


class SEAction158( SEActionBase ):
	"""
	CST-4246 程序功能需求(20级)——帮会副本【九字真言】
	副本初始化,创建真言/真言地板/真言虚影
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
		self.scriptIDList = []
		self.positionList = []
		self.directionList = []
		
		#位置和朝向的顺序要一致
		for scriptID in section["param1"].split("|"):
			self.scriptIDList.append(scriptID)
		for position in section["param2"].split("|"):
			pos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(position))
			self.positionList.append(pos)
		for direction in section["param3"].split("|"):
			dir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(direction))
			self.directionList.append(dir)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		if len(self.scriptIDList) != len(self.positionList) or len(self.scriptIDList) != len(self.directionList):
			KBEDebug.ERROR_MSG("SEAction158 config error %d:%d:%d" %(len(self.scriptIDList), len(self.positionList), len(self.directionList)))
			return
		
		for i in range(len(self.scriptIDList)):
			scriptID = self.scriptIDList[i]
			position = self.positionList[i]
			direction = self.directionList[i]
			params = {"spawnPos": Math.Vector3(position), "spawnDir": Math.Vector3(direction), "zhenyanGroupID" : i}
			entity = spaceEntity.createEntityByScriptID(scriptID, Math.Vector3(position), Math.Vector3(direction), params)
			if entity: entity.recordSelfToSpace()
		
class SEAction190( SEActionBase ):
	"""
	CST-4246 九字真言
	随机选择进行腐化
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.corruptSpeed = int(section["param1"])	#真言腐化速度
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		#之前是否已经开始了占领
		if eventParams.get("extraValue", None):
			if len(eventParams["extraValue"].split('|')) >= 2:
				isPlayerOccupy = int(eventParams["extraValue"].split('|')[0])
				curOccupyGroupID = int(eventParams["extraValue"].split('|')[1])
				spaceEntity.onEndOccupy(curOccupyGroupID, isPlayerOccupy)
		
		#如果没有了，那就是说真言抢夺阶段结束了
		if len(spaceEntity.zhenYanMonster) <= len(spaceEntity.hasOccupyZhenYan):
			spaceEntity.getScript().onConditionChange(spaceEntity, "", spaceEntity.id, "OCCUPYEND", "")
			return
		
		#如果没有了，那就是说真言抢夺阶段结束了
		s1 = set(spaceEntity.hasOccupyZhenYan)
		s2 = set(list(spaceEntity.zhenYanMonster.keys()))
		temp = list(s2 - s1)
		if len(temp) <= 0: 
			spaceEntity.getScript().onConditionChange(spaceEntity, "", spaceEntity.id, "OCCUPYEND", "")
			return
		
		#如果当前选择的真言还未完成腐化，其他的完成了占领，那也不要选择下一个
		if spaceEntity.curGroupID >=0: 
			return
		
		#真言（腐化/争夺）
		groupID = random.choice(temp)
		spaceEntity.occupySpeed = self.corruptSpeed
		spaceEntity.onStartOccupy(groupID)
		
class SEAction394( SEActionBase ):
	"""
	清理玩家身上与副本相关的数据
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		for role in spaceEntity._spaceRoles:
			role.clearJZZYData()
			
class SEAction395( SEActionBase ):
	"""
	CST-4246 九字真言
	刚开始，选择几个完成腐化（争夺）
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.amount = int(section["param1"])	#默认腐化的真言数量
		self.maxCorrupt = int(section["param2"])#真言最大腐化值
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		if len(spaceEntity.zhenYanMonster) < self.amount:
			KBEDebug.ERROR_MSG("SEAction395 config error")
			return
		
		spaceEntity.setMaxCorrupt(self.maxCorrupt)
		for groupID in spaceEntity.zhenYanMonster.keys():
			ids = spaceEntity.zhenYanMonster[groupID].values()
			for id in ids:
				entity = KBEngine.entities.get(id)
				if entity and entity.monsterZYType == Define.MONSTER_JZZY_ZY:
					entity.setMaxCorrupt(self.maxCorrupt)
					
		#随机指定boss占领的真言
		groupIDs = list(spaceEntity.zhenYanMonster.keys())
		lst = random.sample(groupIDs, self.amount)
		for groupID in groupIDs:
			#如果是被boss占领的真言，则应该是已经全部腐化
			if groupID in lst: 
				spaceEntity.onEndOccupy(groupID, False) 
	
class SEAction396( SEActionBase ):
	"""
	CST-4246 九字真言
	被boss腐化的真言砸向玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		for groupID in spaceEntity.zhenYanMonster:
			if groupID in spaceEntity.playerOccupyZhenYan:
				continue
			
			temp = spaceEntity.zhenYanMonster[groupID]
			e = KBEngine.entities.get(temp.get(Define.MONSTER_JZZY_ZY, 0), None)
			if e is None: continue
			try:
				e.allClients.onPoundPlayer()
			except:
				pass
				
class SEAction398( SEActionBase ):
	"""
	CST-4246 九字真言
	有一定概率给boss加上某个buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffList = section["param1"].split("|")
		self.randomList = section["param2"].split("|")
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		if len(self.buffList) != self.randomList:
			return
		
		buffList = set(spaceEntity.queryTemp("BOSSGAILVBUFF", []))
		if len(buffList) <= 0:
			return
		
		bossIDList = spaceEntity.getEntityRecord(spaceEntity.getScript().bossID)
		if len(bossIDList) > 0:
			for index, id in enumerate(bossIDList):
				entity = KBEngine.entities.get(id)
				if entity is None: continue
				for buffID in buffList:
					if buffID not in buffList: continue
					radian = random.uniform(0, 1)
					if self.randomList[index] < radian: continue
					entity.addBuff(entity, int(buffID))
					
class SEAction405( SEActionBase ):
	"""
	CST-4246 九字真言
	开启/关闭玩家伤害buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.flag = int(section["param1"])
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		if self.flag:
			spaceEntity.setOpenDamage(True)
		else:
			spaceEntity.setOpenDamage(False)

SEActionBase.setActionClass("SEAction158", SEAction158)
SEActionBase.setActionClass("SEAction190", SEAction190)
SEActionBase.setActionClass("SEAction394", SEAction394)
SEActionBase.setActionClass("SEAction395", SEAction395)
SEActionBase.setActionClass("SEAction396", SEAction396)
SEActionBase.setActionClass("SEAction398", SEAction398)
SEActionBase.setActionClass("SEAction405", SEAction405)