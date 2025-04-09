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


class BuffUsurp( BuffHold ):
	"""
	附身buff(CST-3704 环任务【灵魂之誓】玩法功能 专用)  怪物对玩家添加此buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.effectIDs = "" 					#摄像机绑定的光效
		self.moveTime = 0.0 				#摄像机移动时间
		self.destroyEffectID = ""				#怪物销毁光效
		self.delayTime=0.0 					#特效延迟时间

	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.effectIDs = dictDat["Param1"]
		self.moveTime = float(dictDat["Param2"])
		self.destroyEffectID = dictDat["Param3"]
		self.delayTime = float(dictDat["Param4"])

	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False

		if not receiver.isInSpaceCopy():
			return False

		spaceEntity = receiver.getCurrentSpace()
		if not spaceEntity.canUsurp(caster):
			return False

		return BuffHold.addBuffCheck( self, caster, receiver )
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		buffDataList = list(receiver.getAttrBuffs().values())
		for buffData in buffDataList:
			buff = receiver.getBuff( buffData.buffID )
			if isinstance( buff, BuffUsurp ):	#移除掉其他变身buff和姿势变换buff和骑上法宝buff
				receiver.removeBuffByID( buffData.buffID )
		
		BuffHold.receiveSuccess( self, caster, receiver )
	

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		buffData.setTempData("isValid",True)
		BuffHold.doBegin( self, receiver, buffData )
		casterID = buffData.casterID
		receiver.cameraMove(casterID, self.effectIDs, self.moveTime, self.delayTime)


	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		buffData.setTempData("isValid",False)
		BuffHold.doEnd( self, receiver, buffData, reason )
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:
			spaceEntity.usurpEnd(receiver)