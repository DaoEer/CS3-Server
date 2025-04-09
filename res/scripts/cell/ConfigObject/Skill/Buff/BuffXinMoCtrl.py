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


class BuffXinMoCtrl( BuffHold ):
	"""
	心魔附身状态buff：只能对玩家用
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.excludeSkillList = []
		self.actForbidList = []
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if dictDat["Param1"]:
			self.actForbidList = [int(i) for i in dictDat["Param1"].split("|")]
		if dictDat["Param2"]:
			self.excludeSkillList = [int(i) for i in dictDat["Param2"].split("|")]
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if not receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.onXinMoCtrlStart( self.excludeSkillList, self.actForbidList )
		receiver.addStateFlag(csdefine.STATE_FLAG_XIN_MO)
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.onXinMoCtrlStart( self.excludeSkillList, self.actForbidList )
		receiver.addStateFlag(csdefine.STATE_FLAG_XIN_MO)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.client.onXinMoCtrlEnd()
		receiver.removeStateFlag(csdefine.STATE_FLAG_XIN_MO)