# -*- coding: utf-8 -*-

import random
import time
import Math

import Functions
import KBEngine
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffRandomMultipleBullet( BuffHold ):
	"""
	多个方向随机发射子弹Buff（碰撞在客户端检测）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._bulletEffectIDData = {}	#子弹光效ID，{index: effectID, ...}
		#self._triggerSkillIDData = {}	#触发技能ID
		self._spaceMsgData = {}	#需要向副本发送的消息，{effectID: msg, ...}
		self._collisionEffectID = ""
		self._collisionTimes = 1	#碰撞次数

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		for effectInfo in dictDat["Param1"].split("|"):
			effectID, amount = effectInfo.split(":")
			for i in range(int(amount)):
				self._bulletEffectIDData[str(len(self._bulletEffectIDData))] = effectID
		for msgInfo in dictDat["Param2"].split("|"):
			effectID, msg= msgInfo.split(":")
			self._spaceMsgData[effectID] = msg
		self._collisionEffectID = dictDat["Param3"].strip()

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_BULLET_COLLISION, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_BULLET_COLLISION, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_BULLET_COLLISION:
			targetID = pDict.get( "bulletTargetID", 0 )
			buffIndex = pDict.get( "buffIndex", 0 )
			effectID = pDict.get( "effectID", 0 )
			effectIndex = pDict.get( "effectIndex", 0 )
			target = KBEngine.entities.get( targetID, None )
			if not target or target.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
				return
			if buffIndex == buffData.index and targetID != triggerID:	#entity发射子弹光效时光效可能会entity本身发生碰撞
				ghostCaster = KBEngine.entities.get( buffData.casterID, None )
				if ghostCaster:
					spaceEntity = ghostCaster.getCurrentSpace()
					if spaceEntity and getattr(spaceEntity.getScript(), "onConditionChange", None):
						collisionTimesData = buffData.getTempData("collisionTimes", None)	#因为会出现一瞬间光效和玩家产生多次碰撞的情况，所以临时使用临时数据解决
						if collisionTimesData:
							if targetID in collisionTimesData:		#有多个子弹向不同方向发出，不同的子弹可能会同时和不同的玩家产生碰撞
								if effectIndex in collisionTimesData[targetID]:
									if collisionTimesData[targetID][effectIndex] >= self._collisionTimes:
										return
									else:
										collisionTimesData[targetID][effectIndex] += 1
								else:
									collisionTimesData[targetID][effectIndex] = 1
							else:
								collisionTimesData.update({targetID: {effectIndex: 1}})
								collisionTimesData[targetID][effectIndex] = 1
						else:
							buffData.setTempData("collisionTimes", {targetID: {effectIndex: 1}})
							
						msg = self._spaceMsgData[effectID]
						spaceEntity.getScript().onConditionChange( spaceEntity, "", ghostCaster.id, msg, "" )	#向副本发送消息
						target.allClients.CLIENT_OnPlayParticles(target.id, self._collisionEffectID, "", -1.0, Math.Vector3(0,0,0) )
						collisionTimesData = buffData.getTempData("collisionTimes")	#上面获取的collisionTimesData可能为None，需要重新获取
						if collisionTimesData[targetID][effectIndex] >= self._collisionTimes:
							receiver.allClients.OnBuffBulletMultipleEnd(buffData.index, effectID, int(effectIndex))	#碰到玩家后光效消失
				
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		proxyEntityID = -1
		ghostCaster = KBEngine.entities.get( buffData.casterID, None )
		if ghostCaster and ghostCaster.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			proxyEntityID = ghostCaster.id
		elif ghostCaster and ghostCaster.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			_AOI = ghostCaster.getCurrentSpaceObject().getSpaceAoi()
			entities = ghostCaster.entitiesInRangeExtForAI( _AOI, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, "Role" )
			_nearestID = 0
			_ndistance = _AOI
			for e in entities: 				# 选择最近目标的ID
				_dis = ghostCaster.position.flatDistTo(e.position)
				if _ndistance > _dis:
					_nearestID = e.id
					_ndistance = _dis
			proxyEntityID = _nearestID
		
		totalAmount = len(self._bulletEffectIDData)
		tempAngleList = []
		tempIndexList = []
		if totalAmount <= 0:
			KBEDebug.ERROR_MSG("Buff[%s] config error" % self.getID())
			return
			
		averageAngle = 360 / totalAmount
		angle = random.uniform(0, averageAngle)
		for i in range(0, totalAmount):
			tempAngleList.append(i * averageAngle + angle)
		random.shuffle(tempAngleList)	#打乱顺序
		for index in range(len(tempAngleList)):
			sendAngle = tempAngleList[index]
			bulletEffectID = self._bulletEffectIDData[str(index)]
			receiver.allClients.OnBuffBulletMultipleBegin( bulletEffectID, sendAngle, index, buffData.casterID, buffData.index, proxyEntityID )
		
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		if self._bulletEffectIDData:
			for index, bulletEffectID in self._bulletEffectIDData.items():
				receiver.allClients.OnBuffBulletMultipleEnd(buffData.index, bulletEffectID, int(index))