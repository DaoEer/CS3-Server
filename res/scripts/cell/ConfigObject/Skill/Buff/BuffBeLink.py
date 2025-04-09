# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop


class BuffBeLink( BuffLoop ):
	"""
	被连线buff
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self.__linkBuffID = 0
	
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
		self.__linkBuffID = int(dictDat["Param1"])
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		linker = KBEngine.entities.get( buffData.casterID )
		if linker and linker.isReal():
			result = linker.addBuff( receiver, self.__linkBuffID )	#给连线者加“连线buff”
			if result:
				linkBuffIndex = linker.findLastBuffByBuffID( self.__linkBuffID )
				if linkBuffIndex != -1:
					linkBuffData = linker.getBuffData( linkBuffIndex )
					linkBuffData.setTempData( "beLinkBuffIndex", buffData.index )
					buffData.setTempData( "linkBuffIndex", linkBuffData.index )
		
		BuffLoop.doBegin( self, receiver, buffData )		#这句必须放后面，确保doLoop的时候连线者已加上“连线buff”，避免“被连线buff”刚加上就中断
	
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		linker = KBEngine.entities.get( buffData.casterID )
		if not linker or not linker.isReal():	#找不到连线者了
			receiver.removeBuff( buffData.index )
		
		elif buffData.getTempData( "linkBuffIndex", -1 ) not in linker.getAttrBuffs():	#连线者没有“连线buff”了
			receiver.removeBuff( buffData.index )
	
	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffLoop.onClientActorCreate( self, receiver, buffData, srcEntityID )
		
		linker = KBEngine.entities.get( buffData.casterID )
		if linker and linker.isReal():
			linkBuffIndex = buffData.getTempData( "linkBuffIndex", -1 )
			if linkBuffIndex != -1 and linkBuffIndex in linker.getAttrBuffs():
				
				#通知对方发起连线
				linkerBuffData = linker.getBuffData( linkBuffIndex )
				buff = receiver.getBuff( linkerBuffData.buffID )
				if buff:
					buff.onBeLinkerCreated( linker, linkerBuffData, receiver.id, srcEntityID  )