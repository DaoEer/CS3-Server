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

import time
#cell
import ItemFactory
import csstatus
import Functions
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop
#common
import KBEDebug
import csdefine
import Const

# 葫芦运输状态
LMZC_SPACE_MOVE_CRYSTAL_TYPE_1 = 1			# 葫芦在敌对阵营
LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 = 2			# 葫芦在运输过程
LMZC_SPACE_MOVE_CRYSTAL_TYPE_3 = 3			# 葫芦在我方阵营

class BuffLingMai( BuffLoop ):
	"""
	灵脉战场
	检测葫芦是否离开营地
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self._distce = 0.0							# 离开(进入)范围，减少（增加）灵能
		self._powerPoint = 0						# 灵能点（离开营地减少\进入营地增加）
		
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
		self._distce = float( dictDat["Param1"] )
		self._powerPoint = int( dictDat["Param2"] )
		
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffLoop.doBegin( self, receiver, buffData )
		if receiver.camp == csdefine.CAMP_TAOSIM:
			if self._distceToTaosim( receiver ) < self._distce:
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_3 )
				return
			if self._distceToDemon( receiver ) < self._distce:
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_1 )
				return
			buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		else:
			if self._distceToDemon( receiver ) < self._distce:
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_3 )
				return
			if self._distceToTaosim( receiver ) < self._distce:
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_1 )
				return
			buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		
		type = buffData.getTempData( "StateType", 1 )
		if type == LMZC_SPACE_MOVE_CRYSTAL_TYPE_3:
			self.detectInside( receiver, buffData )
		elif type == LMZC_SPACE_MOVE_CRYSTAL_TYPE_2:
			self.detectMiddle( receiver, buffData )
		elif type == LMZC_SPACE_MOVE_CRYSTAL_TYPE_1:
			self.detectOutside( receiver, buffData )
			
	def detectInside( self, receiver, buffData ):
		"""在我方阵营"""
		if receiver.camp == csdefine.CAMP_TAOSIM:
			if self._distceToTaosim( receiver ) > self._distce:
				receiver.getCurrentSpace().grabGourdLeave( receiver.id, receiver.camp, -self._powerPoint )
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		else:
			if self._distceToDemon( receiver ) > self._distce:
				receiver.getCurrentSpace().grabGourdLeave( receiver.id, receiver.camp, -self._powerPoint )
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		
	def detectMiddle( self, receiver, buffData ):
		"""在运输葫芦途中"""
		if receiver.camp == csdefine.CAMP_TAOSIM:
			if self._distceToTaosim( receiver ) < self._distce:
				receiver.getCurrentSpace().grabGourdEnter( receiver.id, receiver.camp, self._powerPoint )
				buffData.setTempData("StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_3 )
			elif self._distceToDemon( receiver ) < self._distce:
				receiver.getCurrentSpace().grabGourdEnter( receiver.id, csdefine.CAMP_DEMON, self._powerPoint )
				buffData.setTempData("StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_1 )
		else:
			if self._distceToDemon( receiver ) < self._distce:
				receiver.getCurrentSpace().grabGourdEnter( receiver.id, receiver.camp, self._powerPoint )
				buffData.setTempData("StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_3 )
			elif self._distceToTaosim( receiver ) < self._distce:
				receiver.getCurrentSpace().grabGourdEnter( receiver.id, csdefine.CAMP_TAOSIM, self._powerPoint )
				buffData.setTempData("StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_1 )
		
	
	def detectOutside( self, receiver, buffData ):
		"""在敌方阵营"""
		if receiver.camp == csdefine.CAMP_DEMON:
			if self._distceToTaosim( receiver ) > self._distce:
				receiver.getCurrentSpace().grabGourdLeave( receiver.id, csdefine.CAMP_TAOSIM, -self._powerPoint )
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		else:
			if self._distceToDemon( receiver ) > self._distce:
				receiver.getCurrentSpace().grabGourdLeave( receiver.id, csdefine.CAMP_DEMON, -self._powerPoint )
				buffData.setTempData( "StateType", LMZC_SPACE_MOVE_CRYSTAL_TYPE_2 )
		
	def _distceToTaosim( self, receiver ):
		"""玩家与仙道阵营的距离"""
		return receiver.position.distTo( Const.LMZC_CREATE_TAOSIM_CENTER_POS )
	
	def _distceToDemon( self, receiver ):
		"""玩家与魔道阵营的距离"""
		return receiver.position.distTo( Const.LMZC_CREATE_DEMON_CENTER_POS )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffLoop.doEnd( self, receiver, buffData, reason )
