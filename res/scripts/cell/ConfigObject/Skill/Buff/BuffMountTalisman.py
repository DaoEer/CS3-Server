# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#common
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#cell
import Functions


class BuffMountTalisman ( BuffHold ):
	""""
	骑上法宝(自动前进，并只能控制左右)
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.delayTime = 0.0
		self.InputYawScale = 0.0
		self.BuffSpeed = 0
		self.Direction = ""
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_SCENE
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODEL)
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODE)

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"]:
			self.delayTime = float(dictDat["Param1"])
		self.modelid = dictDat["Param2"]
		if dictDat["Param3"]:
			self.InputYawScale = float(dictDat["Param3"])
		if dictDat["Param4"]:
			self.BuffSpeed = int(float(dictDat["Param4"]) * 100)
		self.Direction = dictDat["Param5"]

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doBegin( self, receiver, buffData )
		receiver.setTemp("tempSpeedBase", self.BuffSpeed)
		receiver.tempSpeed = self.BuffSpeed
		receiver.setSpeed((receiver.tempSpeed * csconst.RunRatio) / 100.0 )
		direction = receiver.direction
		if self.Direction != "":
			direction = Functions.vector3TypeConvert(self.Direction)
		receiver.allClients.OnMountTalisman( self.delayTime, self.modelid, self.InputYawScale )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doReload( self, receiver, buffData )
		receiver.setTemp("tempSpeedBase", self.BuffSpeed)
		receiver.tempSpeed = self.BuffSpeed
		receiver.setSpeed((receiver.tempSpeed * csconst.RunRatio) / 100.0 )
		receiver.allClients.OnMountTalisman( 0.0, self.modelid, self.InputYawScale )


	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.allClients.OnDismountTalisman()
		receiver.removeTemp("tempSpeedBase")
		receiver.tempSpeed = 0
		receiver.setSpeed((receiver.speed * csconst.RunRatio) / 100.0 )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL:
			receiver.removeBuffByIndex( buffData.index )
			self.doInterrupt( receiver, buffData )

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffHold.onClientActorCreate( self, receiver, buffData, srcEntityID )
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )

		clientEntity.OnMountTalisman( 0.0, self.modelid, self.InputYawScale )