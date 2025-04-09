# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffTransparency(BuffHold):
	"""
	透明buff
	"""
	def __init__(self):
		BuffHold.__init__(self)
		self._startTP = 1.0
		self._endTP = 1.0
		self._enterTime = 0
		self._outTime = 0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		strList = dictDat["Param1"].split("|")
		self._endTP = float(strList[0])
		if len(strList)>1:
			self._startTP = float(strList[1])
		self._enterTime = float( dictDat["Param2"] ) if len( dictDat["Param2"] ) > 0 else 0.0
		self._outTime = float( dictDat["Param3"] ) if len( dictDat["Param3"] ) > 0 else 0.0

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffTransparency  ):		#移除同类buff
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		BuffHold.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.allClients.StartTransparency(self._enterTime, self._startTP, self._endTP )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.allClients.StartTransparency(self._enterTime, self._startTP, self._endTP )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData, reason )
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.allClients.EndTransparency(self._outTime, self._endTP, self._startTP )

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

		clientEntity.StartTransparency(0.0, self._startTP, self._endTP )