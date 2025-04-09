# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import csstatus
import KBEDebug
import KBEMath
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffBullet( BuffHold ):
	"""
	子弹Buff（碰撞在客户端检测）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._bulletEffectId = {}	# {0：{子弹光效ID:子弹发射夹角}，1：{子弹光效ID:子弹发射夹角}...}
		self._triggerSkillId = 0	# 子弹碰撞时触发技能ID
		self._triggerTimes = 0		# 子弹触发次数上限 0为触发次数无上限（JIRA：CST-4060
		self._arriveSkillId = 0		# 子弹抵达时触发技能ID
		self._blockSkillId = 0		# 子弹撞到障碍物时触发技能ID

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		_bulletEffectList = dictDat["Param1"].split("|")
		i = 0
		for bulletEffect in _bulletEffectList:
			temp = bulletEffect.split(":")
			if len(temp) ==1:
				temp.append(0)
			self._bulletEffectId[i] = temp
			i += 1

		if dictDat["Param2"]:
			self._triggerSkillId = int( dictDat["Param2"] )			
		if dictDat["Param3"]:
			self._triggerTimes = int( dictDat["Param3"] )
		if dictDat["Param4"]:
			self._arriveSkillId = int( dictDat["Param4"] )
		if dictDat["Param5"]:
			self._blockSkillId = int( dictDat["Param5"] )
			
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
			effectCustomIndex = pDict.get("effectCustomIndex")
			if buffIndex == buffData.index:
				ghostCaster = KBEngine.entities.get( buffData.casterID, None )
				target = KBEngine.entities.get( targetID, None )
				trigger = KBEngine.entities.get( triggerID, None )
				if ghostCaster:	#触发伤害技能
					if pDict.get("type") == "Arrive":  # 子弹抵达时
						if self._arriveSkillId and not self.isDestroyBullet(buffData, effectCustomIndex):
							ghostCaster.useSkillToEntity( self._arriveSkillId, targetID )
					elif pDict.get("type") == "Begin":    # 子弹触发时
						if self.stopBulletCheck(target, ghostCaster):
							destroyList = buffData.getTempData("destroyBulletList", [])
							destroyList.append(effectCustomIndex)
							buffData.setTempData("destroyBulletList", destroyList)
							trigger.allClients.OnBuffBulletEnd( buffData.index, effectCustomIndex )
							return
						statusID = 0
						if self._triggerSkillId and not self.isDestroyBullet(buffData, effectCustomIndex):
							statusID = ghostCaster.useSkillToEntity( self._triggerSkillId, targetID )

						if self._triggerTimes > 0 and statusID == csstatus.SKILL_GO_ON:
							#有效的话，触发次数加1
							triggerTimes = buffData.getTempData("bulletTriggerTimes", 0) + 1
							buffData.setTempData("bulletTriggerTimes", triggerTimes)
							
							#触发次数已达上限
							if triggerTimes >= self._triggerTimes:
								receiver.removeBuffByIndex( buffData.index )
								self.doInterrupt( receiver, buffData )				# 触发中断
					elif pDict.get("type") == "Block":    # 子弹碰到障碍物
						Pos = pDict.get("BlockPos", None)
						Pos = KBEMath.Unreal2KBEnginePosition( Pos )
						if self._blockSkillId and not self.isDestroyBullet(buffData, effectCustomIndex) and Pos:
							ghostCaster.useSkillToPosition(self._blockSkillId, Pos)

		
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
			entities = ghostCaster.entitiesInRange(_AOI, "Role", ghostCaster.position)
			_nearestID = 0
			_ndistance = _AOI
			for e in entities: 				# 选择最近目标的ID
				_dis = ghostCaster.position.flatDistTo(e.position)
				if _ndistance > _dis:
					_nearestID = e.id
					_ndistance = _dis
			proxyEntityID = _nearestID

		for key, value in self._bulletEffectId.items():
			receiver.allClients.OnBuffBulletBegin( value[0], float(value[1]), buffData.casterID, buffData.index, proxyEntityID, key )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		for key in self._bulletEffectId:
			receiver.allClients.OnBuffBulletEnd( buffData.index, key )

	def stopBulletCheck(self, receiver, caster):
		"""
		是否挡住子弹检测
		"""
		if receiver and not receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and receiver.hasFlag(csdefine.FLAG_STOP_BULLET):
			if receiver.queryRelation(caster) == csdefine.COMBAT_RELATION_ENEMY:
				return True
		return False

	def isDestroyBullet(self, buffData, effectCustomIndex):
		"""
		是否是已经销毁的子弹
		"""
		destroyList = buffData.getTempData("destroyBulletList", [])
		if effectCustomIndex in destroyList:
			return True
		return False
