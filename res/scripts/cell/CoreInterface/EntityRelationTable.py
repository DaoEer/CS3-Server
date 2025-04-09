# -*- coding: utf-8 -*-
"""
usage:
	对象关系表

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#engine
import KBEngine
#common
import KBEDebug
import csdefine
import csconst
import Const
#cell
from FightRuleMgr import g_fightMgr


class EntityRelationTable:
	"""
	entity互动信息表
	"""
	def __init__( self ):
		"""
		初始化属性
		"""
		pass

#----------敌人列表处理-------------------------------------------------
	def addEnemyCheck( self, entityID ):
		"""
		extend method.
		"""
		if entityID in self.enemyList:
			return False
		
		if self.id == entityID:
			return False
		
		entity = KBEngine.entities.get( entityID )
		if entity is None:
			return False
		
		if entity.spaceID != self.spaceID:
			return False
		
		return True
	
	#-----------------------------for FightRuleMgr--------------------------------
	def addEnemy( self, entityID ):
		"""
		<define method>
		procedure method.
		@description
			添加一个敌人到战斗列表
		"""
		if not self.addEnemyCheck( entityID ):
			return
		
		self.enemyList[ entityID ] = KBEngine.time()
		self.enemyList = self.enemyList
		self.onAddEnemy( entityID )
	
	def removeEnemy( self, entityID ):
		"""
		<define method>
		将这个敌人从所有列表中删除 （取消该敌人）
		"""
		if not entityID in self.enemyList:
			return
		self.enemyList.pop( entityID )
		self.enemyList = self.enemyList
		self.removeEnemyDmgList( entityID )
		self.removeEnemyCureList( entityID )
		self.removeEnemyHatredList(entityID)
		self.onRemoveEnemy( entityID )
	
	#----------------call back------------------------
	def onAddEnemy( self, entityID ):
		"""
		"""
		if self.getState() != csdefine.ENTITY_STATE_FIGHT and self.getState() != csdefine.ENTITY_STATE_SHOW and self.getState() != csdefine.ENTITY_STATE_PEAD:
			self.changeState( csdefine.ENTITY_STATE_FIGHT )
		self.onEnemyListChange( entityID )
	
	def onRemoveEnemy( self, entityID ):
		"""
		"""
		self.onEnemyListChange( entityID )
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			#触发当前攻击对象从敌人列表中移除事件
			if entityID == self.getTargetID():
				self.setTargetID(0)
				self.triggerEvent(csdefine.ENTITY_EVENT_ATTACKER_REMOVE,"")
	
	def onEnemyListChange( self, entityID ):
		"""
		战斗信息表有改动通知
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			#触发战斗列表改变事件
			triggerEntity = KBEngine.entities.get(entityID, None)
			self.triggerEvent(csdefine.ENTITY_EVENT_ENEMY_CHANGED,[], triggerEntity)
	
	#----------------public------------------------
	def hasEnemy( self, entityID ):
		"""
		是否是自身敌人列表的敌人
		"""
		return entityID in self.enemyList
	
	def findFirstEnemyByTime( self ):
		"""
		根据先后进入敌人列表的时间寻找第一个敌人(既当前此表中时间最早的)
		"""
		return self.getEnemyByIndex( 1 )
	
	def getEnemyByIndex( self, index ):
		"""
		根据进入次序获得敌人
		"""
		enemyList = sorted(self.enemyList.items(), key = lambda asd:asd[1] )
		eid = 0
		if index and  len( enemyList ) >= index:
			eid = enemyList[ index - 1 ][ 0 ]
		
		return eid
	
	def findLastEnemyByTime( self ):
		"""
		根据先后进入敌人列表的时间寻找最后一个攻击我的敌人(既当前此表中时间最迟的)
		"""
		t = 0
		eid = 0
		for entityID, time in self.enemyList.items():
			if t < time:
				eid = entityID
				t = time
		return eid
	
	def findEnemyByEntityType( self, entityType ):
		"""
		查找某entity类型的敌人
		"""
		resultList = []
		for entityID in self.enemyList:
			enemy = KBEngine.entities.get( entityID )
			if not enemy:
				continue
			if enemy.getEntityFlag() == entityType:
				resultList.append( entityID )
		return resultList
	
	def findEnemyByMaxDamage( self ):
		"""
		寻找对我造成伤害最大的敌人
		"""
		if len( self.damageList ):
			return sorted(self.damageList,key=lambda x:self.damageList[x])[-1]
		else:
			return 0
	
	def findEnemyByMaxCure( self ):
		"""
		寻找治疗量最大的敌人
		"""
		if len( self.cureList ):
			return sorted(self.cureList,key=lambda x:self.cureList[x])[-1]
		else:
			return 0
	
	def removeEnemyDmgList( self, entityID ):
		"""
		将这个敌人从伤害列表中删除
		"""
		if entityID in self.damageList:
			self.damageList.pop( entityID )
			self.onDamageListChange( entityID )
	
	def removeEnemyCureList( self, entityID ):
		"""
		将这个敌人从治疗列表中删除
		"""
		if entityID in self.cureList:
			self.cureList.pop( entityID )
			self.onCureListChange( entityID )
	
	def resetEnemyList( self ):
		"""
		重置所有敌人信息表
		"""
		bwe = KBEngine.entities
		enemyList = list( self.enemyList )
		g_fightMgr.breakGroupEnemyRelationByIDs( self, enemyList )
		
		if len( self.enemyList ) > 0:
			self.enemyList.clear()
			self.onEnemyListChange( -1 )
		if len( self.damageList ) > 0:
			self.damageList.clear()
			self.onDamageListChange( -1 )
		if len( self.cureList ) > 0:
			self.cureList.clear()
			self.onCureListChange( -1 )
	
	def canBuildEnemyRelation( self, targetEntity ):
		"""
		能否建立战斗关系
		"""
		#减少对于queryRelation调用次数，已经在敌人列表就没必要再建立战斗关系了
		if targetEntity.id in self.enemyList:
			return False
			
		if not hasattr( self, "getState" ) or not hasattr( targetEntity, "getState" ):
			return False
		
		if self.getState() in csconst.NOT_FIGHT_STATES or targetEntity.getState() in csconst.NOT_FIGHT_STATES:
			return False
		
		if self.queryRelation( targetEntity ) != csdefine.COMBAT_RELATION_ENEMY:
			return False
		
		return True

	def isEnemyRelation( self, targetEntity ):
		"""
		判断是否敌对
		"""
		if targetEntity.id in self.enemyList:
			return True

		if not hasattr( self, "getState" ) or not hasattr( targetEntity, "getState" ):
			return False
		
		if self.getState() in csconst.NOT_FIGHT_STATES or targetEntity.getState() in csconst.NOT_FIGHT_STATES:
			return False
		
		if self.queryRelation( targetEntity ) != csdefine.COMBAT_RELATION_ENEMY:
			return False
		
		return True

	def updateRelation(self):
		"""
		"""
		self.updateEnemyList()


	def updateEnemyList(self):
		"""
		关系改变
		关系不再是敌对的话，马上从敌人列表移除 CST-2128
		"""
		for id in dict(self.enemyList):
			entity = KBEngine.entities.get(id)
			if not entity:	# 找不到目标的话，会有其他机制清空敌人列表，这里不做处理
				continue
			if self.queryRelation( entity ) != csdefine.COMBAT_RELATION_ENEMY:
				g_fightMgr.breakEnemyRelation( self ,entity )


#----------战斗伤害列表处理---------------------------------------------
	def addDamageList( self, entityID, damage ):
		"""
		<define method>
		添加伤害列表
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		
		entity = KBEngine.entities.get( entityID )
		if entity and self.canBuildEnemyRelation( entity ):
			g_fightMgr.buildEnemyRelation( self, entity )
		
		if entityID in self.damageList:
			self.damageList[ entityID ] += damage
		else:
			self.damageList[ entityID ] = damage
		self.onDamageListChange( entityID )

	def resetDamageList( self ):
		"""
		重置伤害列表
		"""
		self.damageList.clear()
		self.onDamageListChange( -1 )

	def onDamageListChange( self, entityID ):
		"""
		伤害信息表有改动通知
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			self.triggerEvent(csdefine.ENTITY_EVENT_DAMAGE_CHANGED,"")

#----------玩家与玩家战斗是否脱战处理---------------------------------------------

	def onDamageListCompare( self, entityID, casterID ):
		"""
		比较伤害列表是否变化
		"""
		entity = KBEngine.entities.get( entityID )
		caster = KBEngine.entities.get( casterID )
		if caster:
			g_fightMgr.breakEnemyRelation( entity, caster )

#----------战斗好友列表处理---------------------------------------------
	def addFriendList( self, entityID ):
		"""
		<define method>
		添加好友列表
		@param entityID  : entityID
		"""
		if not entityID in self.friendList:
			self.friendList.append( entityID )
			self.onFriendListChange( entityID )

	def onFriendListChange( self, entityID ):
		"""
		友方信息表有改动通知
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			self.triggerEvent(csdefine.ENTITY_EVENT_FRIEND_CHANGED,"")

	def hasFriend( self, entityID ):
		"""
		是否是自身敌人列表的敌人
		"""
		return entityID in self.friendList

	def removeAIFriend( self, entityID ):
		"""
		删除一个友方单位
		"""
		if self.hasFriend( entityID ):
			self.friendList.pop( entityID )
			self.onFriendListChange( entityID )

	def resetFriendList( self ):
		"""
		重置好友信息表
		"""
		self.friendList = []
		self.onFriendListChange( -1 )

#----------战斗治疗列表处理---------------------------------------------
	def addCureList( self, entityID, cure ):
		"""
		<define method>
		添加治疗列表
		@param entityID  : entityID
		@param cure		 : 治疗值
		"""
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		
		entity = KBEngine.entities.get( entityID )
		if entity and self.canBuildEnemyRelation( entity ):
			g_fightMgr.buildEnemyRelation( self, entity )
		
		if entityID in self.cureList:
			self.cureList[ entityID ] += cure
		else:
			self.cureList[ entityID ] = cure
		self.onCureListChange( entityID )

	def onCureListChange( self, entityID ):
		"""
		治疗信息表有改动通知
		"""
		#触发AI治愈列表改变事件
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			self.triggerEvent(csdefine.ENTITY_EVENT_DAMAGE_CHANGED,"")

	def resetCureList( self ):
		"""
		重置治疗列表
		"""
		self.cureList.clear()
		self.onCureListChange( -1 )

#----------------------------------仇恨列表处理(暂时只支持怪物)-----------------------------------------
	def addHatredList( self, entityID, value ):
		"""
		<define method>
		添加仇恨列表
		@param entityID  : entityID
		@param Value	 : 仇恨值
		"""
		try:
			self.hatredList
		except:
			return

		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		entity = KBEngine.entities.get( entityID )
		if not entity:
			return
		if entity.getEntityFlag() == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			entityID, entity = self.getGhostReceiverOwner(entity)
		# 仇恨值最小值为0
		hatredValue = value
		if entityID in self.hatredList:
			hatredValue = self.hatredList[ entityID ] + value
		hatredValue = max(0, hatredValue)
		self.hatredList[ entityID ] = hatredValue

		if self.hatredList[ entityID ] > 0 and self.canBuildEnemyRelation( entity ):
			g_fightMgr.buildEnemyRelation( self, entity )

		self.onHatredListChange( entityID )

	def resetHatredList( self ):
		"""
		重置伤害列表
		"""
		try:
			self.hatredList
		except:
			return
		self.hatredList.clear()
		self.onHatredListChange( -1 )

	def onHatredListChange( self, entityID ):
		"""
		伤害信息表有改动通知
		"""
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			self.triggerEvent(csdefine.ENTITY_EVENT_HATRED_CHANGED,"")

	def findEnemyByMaxHatred( self ):
		"""
		寻找对我造成仇恨最大的敌人
		"""
		try:
			self.hatredList
		except:
			return 0

		if len( self.hatredList ):
			return sorted(self.hatredList,key=lambda x:self.hatredList[x])[-1]
		else:
			return 0

	def removeEnemyHatredList( self, entityID ):
		"""
		将这个敌人从伤害列表中删除
		"""
		try:
			self.hatredList
		except:
			return
		if entityID in self.hatredList:
			self.hatredList.pop( entityID )
			self.onHatredListChange( entityID )

	def getGhostReceiverOwner(self, Ghoster):
		"""
		获得傀儡单位的主人
		"""
		_flag = Ghoster.getEntityFlag()
		_owerID = Ghoster.getOwnerEntity().id
		target = Ghoster.getOwnerEntity()
		while _flag == csdefine.ENTITY_FLAG_GHOST_RECEIVER:
			try:
				target = target.getOwnerEntity()
				_flag = target.getEntityFlag()
				_owerID = target.id
			except:
				return _owerID, target
		return _owerID, target
			