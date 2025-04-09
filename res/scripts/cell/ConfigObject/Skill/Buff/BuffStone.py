# -*- coding: utf-8 -*-

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffStone( BuffHold ):
	"""
	石化
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.stoneTime = 0.0
		self.normalTime = 0.0
		self.effectType = 0
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_PERF
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MATERIAL)
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.stoneTime = float( dictDat["Param1"] ) if len( dictDat["Param1"] ) > 0 else 0.0
		self.normalTime = float( dictDat["Param2"] ) if len( dictDat["Param2"] ) > 0 else 0.0
		self.effectType = int( dictDat["Param3"] ) if dictDat["Param3"] else 0
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.allClients.CLIENT_CastToStone( self.stoneTime, self.effectType)
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.allClients.CLIENT_CastToStone( self.stoneTime, self.effectType)

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

		clientEntity.CLIENT_CastToStone( 0.0, self.effectType)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.allClients.CLIENT_CastToNormal( self.normalTime, self.effectType )