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

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffChangeBody( BuffHold ):
	"""
	变身buff，所有变身buff都应继承此脚本
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._modelNumber = ""
		self._modelScale = 1.0
		self._ActionId = ""
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
		self._modelNumber = dictDat["Param1"]
		self._modelScale = float( dictDat["Param2"] )
		self._ActionId = dictDat["Param3"]
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.initActionId = self._ActionId
		BuffHold.doBegin( self, receiver, buffData )
		buffData.setTempData( "recordModelScale", receiver.getModelScale() )
		receiver.setExtraModelNumber( self._modelNumber )
		receiver.setModelScale( self._modelScale )
		receiver.addTimerCallBack( 3.0, "setInitActionId", ("",) )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			# receiver.withdrawPetByReason( csdefine.PET_WITHDRAW_CHANGE_BODY )
			receiver.actCounterInc( csdefine.ACTION_FORBID_WIELD )		#限制更换装备，因为换装备会导致模型改变
			receiver.client.OnChangeBodyStart()
		#receiver.allClients.CLIENT_OnPlayAction(self._ActionId,)		#变身Buff新增"初始动作"播放
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doReload( self, receiver, buffData )
		buffData.setTempData( "recordModelScale", receiver.getModelScale() )
		receiver.setExtraModelNumber( self._modelNumber )
		receiver.setModelScale( self._modelScale )
		
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			# receiver.withdrawPetByReason( csdefine.PET_WITHDRAW_CHANGE_BODY )
			receiver.actCounterInc( csdefine.ACTION_FORBID_WIELD )		#限制更换装备，因为换装备会导致模型改变
			receiver.client.OnChangeBodyStart()
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.initActionId = ""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.setModelScale( buffData.getTempData("recordModelScale") )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.setExtraModelNumber("")
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.actCounterDec( csdefine.ACTION_FORBID_WIELD )
			receiver.client.OnChangeBodyEnd()

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