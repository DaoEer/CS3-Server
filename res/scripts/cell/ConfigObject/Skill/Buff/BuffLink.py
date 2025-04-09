# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop


class BuffLink( BuffLoop ):
	"""
	连线buff
	负责播连线光效、发起重连
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self.__effectID = ""
		self.__distance = 0.0
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		self.__effectID = dictDat["Param1"]
		if dictDat["Param2"]:
			self.__distance = float(dictDat["Param2"])
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if caster.position.distTo( receiver.position ) > self.__distance:	#这里检测一下距离，避免距离过远时buff也能持有1个周期
			return False
		return BuffLoop.addBuffCheck( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		beLinker = KBEngine.entities.get( buffData.casterID )	#被连线者给我加的buff，但是我才是发起连线的一方
		if beLinker:
			receiver.allClients.BuffPlayLinkEffect( beLinker.id, buffData.index, self.__effectID )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffLoop.doEnd( self, receiver, buffData, reason )
		receiver.allClients.BuffEndPlayLinkEffect( buffData.index, )
	
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		beLinker = KBEngine.entities.get( buffData.casterID )
		if not beLinker or not beLinker.isReal():
			receiver.removeBuff( buffData.index )
		
		elif buffData.getTempData( "beLinkBuffIndex", -1 ) not in beLinker.getAttrBuffs():		#被连线者没有“被连线buff”了
			receiver.removeBuff( buffData.index )
		
		elif self.__distance > 0:
			if receiver.position.distTo( beLinker.position ) > self.__distance:			#超过距离了
				receiver.removeBuff( buffData.index )
	
	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffLoop.onClientActorCreate( self, receiver, buffData, srcEntityID )
		
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		beLinker = KBEngine.entities.get( buffData.casterID )
		if beLinker and beLinker.isReal():
			clientEntity.BuffPlayLinkEffect( beLinker.id, buffData.index, self.__effectID )
	
	def onBeLinkerCreated( self, receiver, buffData, beLinkerID, srcEntityID ):
		"""
		收到被连接者通知：他某客户端上创建好了
		"""
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		try:	#不一定有连接者的客户端
			clientEntity.BuffPlayLinkEffect( beLinkerID, buffData.index, self.__effectID )
		except:
			pass