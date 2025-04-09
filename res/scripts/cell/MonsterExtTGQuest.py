# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import KBEDebug
import Monster
import csdefine
import Const

class MonsterExtTGQuest( Monster.Monster ):
	"""
	练兵场 练兵任务
	用于 部队执行任务
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.process = 0
		self.bBeginQuest = 0

	def onPlayerOnLine(self, basePlayerMB):
		self.basePlayerMB = basePlayerMB
		
	def onEnterFree( self ):
		"""
		virtual method
		进入自由状态
		"""
		Monster.Monster.onEnterFree(self)
		if not self.bBeginQuest:
			self.bBeginQuest = 1
			self.beginDoTGQuest()

	def beginDoTGQuest( self ):
		"""开始执行 练兵任务"""
		self.gotoPosition(self.dstPos, 0.5)

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		if self.process == 0:
			self.beginFight()
		if self.process == 1:
			self.onBackHome()
			
	def beginFight( self ):
		"""开始战斗"""
		self.setTemp("extraModelNumber", self.extraModelNumber)
		self.setTemp("armyModelList", self.armyModelList)
		self.setExtraModelNumber( "" )
		self.setArmyModelList([])
		object = self.getScript()
		if object.buffID:
			self.addBuff( self, object.buffID )
			
		player = KBEngine.entities.get( self.basePlayerMB.id )
		if player and player.spaceID == self.spaceID:
			player.client.StartPlayStory(object.sceneID, 1)
			
		self.addTimerCallBack( Const.TRAIN_GROUND_QUEST_FIGHT_TIME, "endFight", () )
		
	def endFight( self ):
		"""结束战斗"""
		self.setExtraModelNumber( self.queryTemp("extraModelNumber" ) )
		self.setArmyModelList( self.queryTemp("armyModelList" ) )
		self.process += 1
		self.gotoPosition( self.initialPosition, 0.0 )
		# 玩家 还在同一个 cell上
		player = KBEngine.entities.get( self.basePlayerMB.id )
		if player:
			player.onTGQuestFightEnd( self.battackID )
		else:			# 玩家可能传送到其他地图，或者下线了
			if self.basePlayerMB and self.basePlayerMB.cell:
				self.basePlayerMB.cell.onTGQuestFightEnd( self.battackID )
		
	def onBackHome( self ):
		"""回到 大本营"""
		player = KBEngine.entities.get( self.basePlayerMB.id )
		if player:
			player.onSoldierBackHome( self.battackID )
		else:			# 玩家可能传送到其他地图，或者下线了
			if self.basePlayerMB and self.basePlayerMB.cell:
				self.basePlayerMB.cell.onSoldierBackHome( self.battackID )
		
		self.destroySelf()