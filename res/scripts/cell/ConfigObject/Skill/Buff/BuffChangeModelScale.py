# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
import KBEDebug


class BuffChangeModelScale( BuffHold ):
	"""
	模型缩放Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.modelScalX = 1.0
		self.modelScalY = 1.0
		self.modelScalZ = 1.0
		self.changeTime = 0.0
		self.nomalTime = 0.0
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_FUC
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODEL)
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"]:
			tempStr = dictDat["Param1"].split("|")
			if len(tempStr) == 1:
				self.modelScalX = self.modelScalY = self.modelScalZ = float(tempStr[0])
			elif len(tempStr) == 2:
				self.modelScalX = float(tempStr[0])
				self.modelScalY = float(tempStr[1])
			else:
				self.modelScalX = float(tempStr[0])
				self.modelScalY = float(tempStr[1])
				self.modelScalZ = float(tempStr[2])

		self.changeTime = float( dictDat["Param2"] ) if len( dictDat["Param2"] ) > 0 else 0.0
		self.nomalTime = float( dictDat["Param3"] ) if len( dictDat["Param3"] ) > 0 else 0.0
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doBegin( self, receiver, buffData )
		buffData.setTempData( "recordModelScale", receiver.getModelScale() )
		receiver.allClients.CLIENT_ChangeToDstModelScale( self.changeTime, self.modelScalX, self.modelScalY, self.modelScalZ, receiver.getModelScale() )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doReload( self, receiver, buffData )
		buffData.setTempData( "recordModelScale", receiver.getModelScale() )
		receiver.allClients.CLIENT_ChangeToDstModelScale( self.changeTime, self.modelScalX, self.modelScalY, self.modelScalZ, receiver.getModelScale() )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.allClients.CLIENT_ChangeToNormalModelScale( self.nomalTime,buffData.getTempData("recordModelScale") )		

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

		clientEntity.CLIENT_ChangeToDstModelScale( 0.0, self.modelScalX, self.modelScalY, self.modelScalZ, receiver.getModelScale() )