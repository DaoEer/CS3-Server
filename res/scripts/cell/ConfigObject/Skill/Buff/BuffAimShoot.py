# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffReplace import BuffReplace


class BuffAimShoot( BuffReplace ):
	"""
	射击模式
	箭射击完，移除此buff！退出射击模式
	"""
	def __init__( self ):
		BuffReplace.__init__( self )
		self._modelNumber = ""			# 变换手中武器
		self._shootNum = -1				# 射击次数(-1表示射击次数没限制)
		self._skillID = 0				# 关联的技能ID，
		self._AimSkillID = 0			# 瞄准模式下点击释放的技能
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffReplace.init( self, dictDat )
		if dictDat["Param2"]:
			self._AimSkillID = int(dictDat["Param2"])
		self._modelNumber = dictDat["Param3"]
		if dictDat["Param4"]:
			self._shootNum = int(dictDat["Param4"])
		if dictDat["Param5"]:
			self._skillID = int(dictDat["Param5"])

	
	def registerEvent( self, receiver, buffData ):
		"""注册buff事件"""
		BuffReplace.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_PROCESS, buffData.index )
	
	def unRegisterEvent( self, receiver, buffData ):
		"""注销buff事件"""
		BuffReplace.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_PROCESS, buffData.index )
	
	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		BuffReplace.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )
		if eventType == csdefine.SKILL_EVENT_PROCESS and pDict["type"] == csdefine.SKILL_EVENT_SKILL_BEGIN and pDict["skillID"] == self._skillID:
			self.doShoot( receiver, buffData )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffReplace.doBegin( self, receiver, buffData )
		receiver.client.EnterShootModel( self._AimSkillID )
		if self._modelNumber:
			receiver.setExtraModelNumber( self._modelNumber )
		buffData.setTempData("ShootNum", self._shootNum )
		
	def doShoot(self, receiver, buffData ):
		"""
		射击
		"""
		shootNum = buffData.getTempData("ShootNum")
		if shootNum == -1:return
		shootNum -= 1
		if shootNum <= 0:
			receiver.removeBuffByIndex( buffData.index )
			return
		buffData.setTempData("ShootNum", shootNum)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffReplace.doEnd( self, receiver, buffData,reason )
		receiver.client.LeaveShootModel()
		if self._modelNumber:
			receiver.setExtraModelNumber( "" )



