# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csdefine
import csstatus
import cschannel_msgs

PRIMARY_LEVEL_BOSSYCJMD = 1			#初级
INTERMEDIATE_LEVEL_BOSSYCJMD = 2	#中级
SENIOR_LEVEL_BOSSYCJMD = 3			#高级

class MonsterExtYCJMDBoss( Monster.Monster ):
	"""
	CST-8727 勇闯夺命岛Boss
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.itemDict = {} # 物品ID:数量

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD)

	def isBossCanUpLevel( self ):
		"""
		是否可升级
		"""
		return self.levelYCJMD < SENIOR_LEVEL_BOSSYCJMD

	def getYCJMDBossLevel( self ):
		return self.levelYCJMD

	def setYCJMDBossLevel( self, level ):
		"""
		设置Boss新的等级
		"""
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		if self.levelYCJMD == level:
			return

		if min(self.monsterAIGetCurGroupStateObj().getSubStatesID()) != self.monsterAIGetCurSubState():
			self.recordLevelYCJMD = level
			return
		oldLevel = self.levelYCJMD
		self.levelYCJMD = level
		self.onYCJMDBossLevelUp(oldLevel)

	def setYCJMDBossMaxLevel( self ):
		"""
		"""
		self.setYCJMDBossLevel( SENIOR_LEVEL_BOSSYCJMD )

	def onYCJMDBossLevelUp( self, oldLevel ):
		"""
		升级
		"""
		self.triggerEvent(csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, ["levelYCJMD",self.levelYCJMD, oldLevel ])
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			content = self.getUname() + "|" + cschannel_msgs.YCJMD_BOSS_LEVEL_NAME.get(self.levelYCJMD,"")
			for role in spaceEntity._spaceRoles:
				role.statusMessage(csstatus.YCJMD_BOSS_UP_LEVEL,content)

	def monsterAIChangeSubState( self, newState ):
		"""
		改变状态
		"""
		Monster.Monster.monsterAIChangeSubState( self, newState )
		if self.recordLevelYCJMD != self.levelYCJMD and self.recordLevelYCJMD > 1:
			self.setYCJMDBossLevel( self.recordLevelYCJMD )

	def addBossItemDictData( self, itemDict ):
		"""
		增加Boss物品数据
		"""
		for itemID, amount in itemDict.items():
			if itemID in self.itemDict:
				self.itemDict[itemID] += amount
			else:
				self.itemDict[itemID] = amount

	def isBossCanUseItem( self, itemID, amount ):
		"""
		Boss是否可以使用物品
		"""
		if itemID not in self.itemDict:
			return False
		if amount > self.itemDict[itemID]:
			return False
		return True

	def reduceBossItemData( self, itemID, amount ):
		"""
		减少Boss物品数据
		"""
		if itemID not in self.itemDict:
			return
		if self.itemDict[itemID] > amount:
			self.itemDict[itemID] -= amount
		else:
			del self.itemDict[itemID]


	def canStartRevert( self ):
		"""
		能否开启恢复
		"""
		return False

	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行AI
		"""
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		Monster.Monster.onWitnessed( self, isWitnessed )		

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		Monster.Monster.onMoveOver( self, controllerID, userData )
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.removeFlag( csdefine.FLAG_CAN_FLY )
			self.initActionId = self.getScript().getDeadKeepActionID()

