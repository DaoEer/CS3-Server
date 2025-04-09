# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#engine
import KBEngine
import KBEDebug
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine



class BuffChangePosture( BuffHold ):
	"""
	变换姿势buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._ModelId = ""
		self._inActionId = ""
		self._outActionId = ""
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
		strList = dictDat["Param1"].split("|")
		self._ModelId = strList[0]
		if len(strList) > 1:
			self._inActionId = strList[1]
		if len(strList) > 2:
			self._outActionId = strList[2]

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		变换开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowPosture(self._ModelId, self._inActionId, "")
		BuffHold.doBegin( self, receiver, buffData )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowPosture(self._ModelId, self._inActionId,self._outActionId)
		BuffHold.doReload( self, receiver, buffData )	

	def doEnd( self, receiver, buffData,reason ):
		"""
		变换结束
		"""
		receiver.allClients.CLIENT_ChangeShowPosture( receiver.getActionNumber(), "", self._outActionId)
		BuffHold.doEnd( self, receiver, buffData,reason )
		
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
		
		clientEntity.CLIENT_ChangeShowPosture(self._ModelId, "", "")

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