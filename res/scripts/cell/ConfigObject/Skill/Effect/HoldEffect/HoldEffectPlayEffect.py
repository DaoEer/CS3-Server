# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import KBEngine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectPlayEffect( HoldEffect ):
	"""
	播放动作、光效、音效
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self._actionID = []
		self._effectID = ""
		self._soundID = ""
		self._actionBeginTime = []
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		actionInfos = dictDat["Param1"].split("|")
		for i in actionInfos:
			actionInfo = i.split(":")
			if len( actionInfo ) > 1:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( actionInfo[1] )			
			else:
				self._actionID.append(actionInfo[0])
				self._actionBeginTime.append( "0.0")
				
		self._effectID = dictDat["Param2"]
		self._soundID = dictDat["Param3"]
	
	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		if not effectData.getTempData("isReloadBuff", False):	#如果是重载buff，不重新加效果，因为在onClientActorCreate时会加
			receiver.setActionIndex()
			effectData.setTempData("actionIndex",receiver.actionIndex)
			receiver.allClients.HoldEffectPlayEffect( effectData.casterID, effectData.index, receiver.actionIndex, self._actionID, self._effectID, self._soundID, self._actionBeginTime )
	
	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.HoldEffectEndEffect( effectData.index, effectData.getTempData("actionIndex", 0) )
		HoldEffect.onEnd( self, effectData, receiver )

	
	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		clientEntity.HoldEffectPlayEffect( effectData.casterID, effectData.index, effectData.getTempData("actionIndex", 0), self._actionID, self._effectID, self._soundID, self._actionBeginTime )		#CST-2568 恢复效果