# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#common
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#cell
import Functions


class BuffMountStone ( BuffHold ):
	""""
	玩家踩石头，玩家可跳跃（CST-9346）
	"""
	def __init__( self ):
		BuffHold.__init__( self )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
#		if dictDat["Param1"]:
#			self.delayTime = float(dictDat["Param1"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			tempBuffDataList = list(receiver.getAttrBuffs().values())
			for buffData in tempBuffDataList:
				buff = caster.getBuff( buffData.buffID )
				if isinstance( buff, BuffMountStone ) :
					return False
			return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		caster = KBEngine.entities.get(buffData.casterID)
		if caster and caster.isEntityFlag(csdefine.ENTITY_FLAG_MONSTER):
			caster.setSyncPosClient( receiver.id )
			bBegin = 1
			receiver.allClients.CLIENT_OnMountStone( caster.id, bBegin )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		caster = KBEngine.entities.get(buffData.casterID)
		if caster:
			caster.setSyncPosClient( 0 )
		receiver.allClients.CLIENT_OnDisMountStone()
		BuffHold.doEnd( self, receiver, buffData,reason )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffHold.onClientActorCreate( self, receiver, buffData, srcEntityID )
		bBegin = 0
		receiver.allClients.CLIENT_OnMountStone( caster.id, bBegin )
