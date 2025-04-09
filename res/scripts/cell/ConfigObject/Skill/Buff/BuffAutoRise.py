# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
from ConfigObject.Skill.Buff.BuffRespond import BuffRespond
import csdefine

class BuffAutoRise( BuffRespond ):
	""""
	自动上升Buff
	"""
	def __init__( self ):
		BuffRespond.__init__( self )
		self.riseSpeed = 0.0
		self.rightSpeed = 0.0
		self.cameraLength = 0.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffRespond.init( self, dictDat )
		if dictDat["Param1"]:
			self.riseSpeed = float(dictDat["Param1"])
		if dictDat["Param2"]:
			self.rightSpeed = float(dictDat["Param2"])
		self.cameraLength = float(dictDat["Param3"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffRespond.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffAutoRise ) or isinstance( buff, BuffAutoRise ):
				receiver.removeBuffByID( buffData.buffID )
		
		BuffRespond.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffRespond.doBegin( self, receiver, buffData )
		receiver.actCounterInc( csdefine.ACTION_FORBID_SPELL )
		if receiver.getAllClients():
			receiver.allClients.CLIENT_AutoRise( self.riseSpeed, self.rightSpeed,self.cameraLength )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffRespond.doEnd( self, receiver, buffData,reason )
		receiver.actCounterDec( csdefine.ACTION_FORBID_SPELL )
		if receiver.getAllClients():
			receiver.allClients.CLIENT_StopRise()

