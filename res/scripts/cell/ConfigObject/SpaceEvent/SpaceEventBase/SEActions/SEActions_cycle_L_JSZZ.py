# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import random
import math
import Math
import csarithmetic

class SEAction297( SEActionBase ):
	"""
	金树种子 怪物刷新
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|") # 怪物的scriptID列表
		self.choiceNumber = int( section["param2"] )  # 选择scriptID的数量
		self.radius = float( section["param3"] ) #距离金树种子的距离
		self.choiceDirNumber = int(section["param4"].split("|")[0]) ##随机选择|将圆分开的块数
		self.splitDirNumber = int(section["param4"].split("|")[1])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if len( self.scriptIDs ) < self.choiceNumber:
			KBEDebug.ERROR_MSG("SEAction297 param1 len = %i < param2 number =%i"%( len(self.scriptIDs),self.choiceNumber )  )
			return
		if self.choiceDirNumber > self.splitDirNumber:
			KBEDebug.ERROR_MSG("SEAction297 param4 choiceDirNumber = %i > param4 splitDirNumber =%i"%( self.choiceDirNumber,self.splitDirNumber ))
			return
		theta = (2 * math.pi) / self.splitDirNumber
		dirList = []
		for i in range(0,self.splitDirNumber):
			dirList.append(i * theta)

		randomDirList = random.sample( dirList, self.choiceDirNumber )
		tempDirList = []
		if self.choiceNumber > len(randomDirList):
			tempDirList.extend(randomDirList)
			amount = self.choiceNumber - len( randomDirList )
			for i in range(0,amount):
				dir = random.choice(randomDirList)
				tempDirList.append( dir )
		else:
			tempDirList.extend(random.sample( randomDirList, self.choiceNumber ))

		if len( tempDirList ) != self.choiceNumber:
			KBEDebug.ERROR_MSG("SEAction297 tempDirList is error")
			return
		treeEntitys = spaceEntity.getEntityMailBoxRecord(spaceEntity.getScript().treeScriptID)
		if not len(treeEntitys):
			return

		scriptIDs = random.sample( self.scriptIDs, self.choiceNumber )
		for scriptID in scriptIDs:
			index = scriptIDs.index( scriptID )
			radian = tempDirList[index]
			pos = spaceEntity.getPositionByRadian(treeEntitys[0].position,self.radius,radian)
			yaw = csarithmetic.getYawByVector3((treeEntitys[0].position - pos))
			spaceEntity.createEntityByScriptID( scriptID,pos,Math.Vector3(0,0,yaw),{} )

class SEAction298( SEActionBase ):
	"""
	金树种子 NPC刷新
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|") # NPC的scriptID列表
		self.radius = float( section["param2"] ) #距离金树种子的距离

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		treeEntitys = spaceEntity.getEntityMailBoxRecord(spaceEntity.getScript().treeScriptID)
		if not len(treeEntitys):
			return

		for scriptID in self.scriptIDs:
			index = self.scriptIDs.index( scriptID )
			radian = index * math.pi/2
			pos = spaceEntity.getPositionByRadian(treeEntitys[0].position,self.radius,radian)
			yaw = csarithmetic.getYawByVector3((pos - treeEntitys[0].position))
			spaceEntity.createEntityByScriptID( scriptID,pos,Math.Vector3(0,0,yaw),{} )

class SEAction299( SEActionBase ):
	"""
	金树种子 友方怪物销毁
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		monster = KBEngine.entities.get(eventParams["entityID"],None)
		if not monster:
			return
		scriptID = monster.queryTemp("RecordNPCScriptID")
		if not scriptID:
			return

		spaceEntity.createEntityByScriptID(scriptID,monster.spawnPos,monster.spawnDir,{} )


class SEAction300( SEActionBase ):
	"""
	金树种子 灵石刷新
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|") 	#灵石ID|灵石ID....
		self.amounts = section["param2"].split("|")   	#对应数量|对应数量....
		self.minRadius = float(section["param3"])		#最小半径
		self.maxRadius = float( section["param4"] ) 	#最大半径

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		treeEntitys = spaceEntity.getEntityMailBoxRecord(spaceEntity.getScript().treeScriptID)
		if not len(treeEntitys):
			return

		for scriptID in self.scriptIDs:
			index = self.scriptIDs.index( scriptID )
			amount = int(self.amounts[index])
			while amount:
				pos = csarithmetic.getPositionByByLinks( treeEntitys[0].position,self.minRadius,self.maxRadius )
				spaceEntity.createEntityByScriptID(scriptID,pos,Math.Vector3(0,0,0),{})
				amount -= 1

class SEAction302( SEActionBase ):
	"""
	金树种子 收到通知设置当前阶段的时长
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		curStage = int(eventParams["extraValue"].split("|")[0])
		curStageTime = int(eventParams["extraValue"].split("|")[1])
		curStageRewardMoney = int( eventParams["extraValue"].split("|")[2] )
		spaceEntity.setCurrentStageData( curStage, curStageTime,curStageRewardMoney )

class SEAction303( SEActionBase ):
	"""
	金树种子 设置下次刷怪的时长
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.longTime = int( section["param1"] ) #时长

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setNextRefreshMonsterTime( self.longTime )

class SEAction317( SEActionBase ):
	"""
	金树种子 玩家进入副本添加种植的检测区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player and player.getClient():
				player.client.CLIENT_AddJSZZCircleArea( spaceEntity.scriptID, spaceEntity.getScript().getPlantCenterPos(), spaceEntity.getScript().getPlantRadius() )

class SEAction318( SEActionBase ):
	"""
	金树种子 移除种植的检测区域
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player and player.getClient():
				player.client.CLIENT_ClearJSZZCircleArea()
				player.client.ShowJSZZProtectWin( spaceEntity.getScript().rewardItemIDs )

SEActionBase.setActionClass("SEAction297", SEAction297)
SEActionBase.setActionClass("SEAction298", SEAction298)
SEActionBase.setActionClass("SEAction299", SEAction299)
SEActionBase.setActionClass("SEAction300", SEAction300)
SEActionBase.setActionClass("SEAction302", SEAction302)
SEActionBase.setActionClass("SEAction303", SEAction303)
SEActionBase.setActionClass("SEAction317", SEAction317)
SEActionBase.setActionClass("SEAction318", SEAction318)
