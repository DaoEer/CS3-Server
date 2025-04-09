# -*- coding: utf-8 -*-

#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#common
import csdefine


class BuffAutoMoveForward( BuffHold ):
	"""
	玩家自动前进buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.yawScale = 0.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )

		if dictDat["Param1"]:
			self.yawScale = float(dictDat["Param1"])	

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff目前只适用于玩家
			return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffAutoMoveForward ):
				receiver.removeBuffByID( buffData.buffID )
		BuffHold.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		变换开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.OnStartRoleAutoMove( self.yawScale )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.OnStartRoleAutoMove( self.yawScale )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.client.OnDisRoleAutoMove()
		BuffHold.doEnd( self, receiver, buffData,reason )
