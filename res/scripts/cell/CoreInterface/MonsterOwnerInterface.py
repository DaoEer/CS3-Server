# -*- coding- : utf-8 -*-

import json
from ConfigObject.Drop import DropOwner
import csdefine
import KBEngine
import KBEDebug
import Define
from ConfigObject.MonsterOwnership.MonsterOwnershipInst import g_MonsterOwnershipInst

class MonsterOwnerInterface( object ):
	def __init__( self ):
		self.bootyOwnerTypeObj = None
	
	def hasBootOwner( self ):
		return hasattr( self, "bootyOwnerTypeObj" ) and self.bootyOwnerTypeObj

	def setBootyOwnerForNeverChange(self, attacker):
		"""
		设置不变更归属权类型归属者
		"""
		if attacker == None:
			return

		#获取真正的攻击者	
		realAttacker = attacker
		#如果是随从怪则奖励拥有者转移到主人
		if attacker.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and attacker.getMonsterType() == csdefine.MONSTER_TYPE_MONSTER_EXT_CALL and attacker.owner:
			realAttacker = KBEngine.entities.get( attacker.owner.id, None )
		#如果是幻兽则奖励拥有者转移到主人
		elif attacker.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			realAttacker = attacker.getOwnerEntity()
		if not realAttacker:
			return

		bootyOwnerTypeObj = self.selectOwnerTypeObj( realAttacker )
		if bootyOwnerTypeObj:
			self.bootyOwnerTypeObj = bootyOwnerTypeObj
		try:
			self.allClients.CLIENT_OnSetBootyOwner( json.dumps(self.getOwnerTypeAndOwnerID()) )
		except:
			pass

	def setBootyOwner( self, attacker ):
		"""
		<define method>
		设置战利品拥有者
		"""
		ownership = self.getScript().ownership
		#如果归属权是不变更类型直接跳过
		if ownership == Define.MONSTER_OWNER_NEVER_CHANGE:
			return

		if attacker == None:
			return

		#获取真正的攻击者	
		realAttacker = None
		if attacker.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			realAttacker = attacker
		#如果是随从怪则奖励拥有者转移到主人
		elif attacker.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER and attacker.getMonsterType() == csdefine.MONSTER_TYPE_MONSTER_EXT_CALL and attacker.owner:
			realAttacker = KBEngine.entities.get( attacker.owner.id, None )
		#如果是幻兽则奖励拥有者转移到主人
		elif attacker.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			realAttacker = attacker.getOwnerEntity()

		if not realAttacker:
			return

		ownershipObj = g_MonsterOwnershipInst.getObject(ownership)
		if not ownershipObj:
			return
		if not ownershipObj.canAddOwnerCheck(self, realAttacker):
			return

		bootyOwnerTypeObj = self.selectOwnerTypeObj( realAttacker )
		if bootyOwnerTypeObj:
			#先将之前的注册事件进行反注册
			if self.bootyOwnerTypeObj:
				if self.bootyOwnerTypeObj.getType() == csdefine.DROP_OWNER_TYPE_PERSON:
					self.entityEventUnsubscribe(csdefine.ENTITY_EVENT_ROLE_TEAM_JOIN, realAttacker.id)
				elif self.bootyOwnerTypeObj.getType() == csdefine.DROP_OWNER_TYPE_TEAM:
					self.entityEventUnsubscribe(csdefine.ENTITY_EVENT_ROLE_TEAM_LEAVE, realAttacker.id)
			
			self.bootyOwnerTypeObj = bootyOwnerTypeObj
			#单人的注册入队事件
			if bootyOwnerTypeObj.getType() == csdefine.DROP_OWNER_TYPE_PERSON:
				self.entityEventSubscribe(csdefine.ENTITY_EVENT_ROLE_TEAM_JOIN, realAttacker.id, "onPlayerJoinTeam")
			#队伍的注册离队事件
			if bootyOwnerTypeObj.getType() == csdefine.DROP_OWNER_TYPE_TEAM:
				self.entityEventSubscribe(csdefine.ENTITY_EVENT_ROLE_TEAM_LEAVE, realAttacker.id, "onPlayerLeaveTeam")
		try:
			self.allClients.CLIENT_OnSetBootyOwner( json.dumps(self.getOwnerTypeAndOwnerID()) )
		except:
			pass

				
	def calculateBootyOwner( self ):
		"""
		取得战利品的拥有者；
		建议在怪物死亡时（即在onEnterDead()时）再调用此方法，否则如果拥有者不存在的话计算出来的结果可能会是错误的。

		@return: 无
		"""
		owners = {}
		if self.bootyOwnerTypeObj:
			_owners = self.bootyOwnerTypeObj.getOwnerIDs( self )
			owners.update(_owners)
		return owners


	def selectOwnerTypeObj( self, attacker ):
		"""
		选择所有权的类型
		"""
		ownerTypeObj = None
		for t in DropOwner.DOwnerBase.getAllTypes():
			if DropOwner.DOwnerBase.getObject( t ).isUseOwnerType( self, attacker ):
				ownerTypeObj =  DropOwner.DOwnerBase.getObject( t )( attacker, self )
		
		return ownerTypeObj
	
	def getOwnerTypeAndOwnerID( self ):
		"""
		获取怪物所有者列表
		"""	
		lst = []
		if self.bootyOwnerTypeObj:
			dct = {
				"type" : self.bootyOwnerTypeObj.getType(),
				"owner": self.bootyOwnerTypeObj.getOwnerID(),
			}
			lst.append(dct)
		return lst


	def getOwnerIDList( self ):
		"""
		获取怪物所有者ID列表
		"""	
		lst = []
		if self.bootyOwnerTypeObj:
			lst.extend( list(self.bootyOwnerTypeObj.getOwnerIDs(self).keys()) )
		return lst
	
	def onRemoveEnemy( self, entityID ):
		"""
		CST-11836
		移除敌人后，需要更新归属权
		规则：1：玩家是单人，直接移除玩家的归属权
			  2：玩家在队伍中，判断当前队伍中是否还有其余队友在怪物的敌人列表中，如果没有则移除此队伍的归属权
		"""
		#自身死亡移除敌人的时候不清除敌人的归属权
		if self.state == csdefine.ENTITY_STATE_DEAD:
			return

		ownership = self.getScript().ownership
		ownershipObj = g_MonsterOwnershipInst.getObject(ownership)
		if not ownershipObj:
			return
		ownershipObj.onRemoveEnemy(self, entityID)


	def onPlayerJoinTeam(self, eventType, notifierID, args):
		"""
		归属者加入队伍 更新归属权 将归属权变更为队伍
		"""
		if notifierID == self.bootyOwnerTypeObj.getOwnerID():
			self.bootyOwnerTypeObj = None
			owner = KBEngine.entities.get(notifierID, None)
			self.setBootyOwner(owner)

	def onPlayerLeaveTeam(self, eventType, notifierID, args):
		"""
		归属者离队
		"""
		teamID = args[0]
		if self.bootyOwnerTypeObj and self.bootyOwnerTypeObj.getOwnerID() == teamID:
			#选择下一个玩家注册离队事件
			for playerID in self.bootyOwnerTypeObj.getOwnerIDs(self).keys():
				player = KBEngine.entities.get(playerID, None)
				if not player:
					continue
				self.entityEventSubscribe(csdefine.ENTITY_EVENT_ROLE_TEAM_LEAVE, player.id, "onPlayerLeaveTeam")

			#如果走到这里来了，表示当前玩家是队伍中最后一个离队的人，移除掉此队伍的归属权
			self.bootyOwnerTypeObj = None
