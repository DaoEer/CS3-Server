# -*- coding: utf-8 -*-

import csdefine
import csstatus
import QuestEventDefine
from XiuweiLoader import g_XiuweiMgr
from MsgLogger import g_logger

class XiuweiInterface:
	"""
	修为接口
	"""
	def __init__( self ):
		self.initXiuweiLevel()
		self.initJingjieLevel()

	def initXiuweiLevel(self):
		"""
		初始化修为等级
		"""
		xiuweiLevel = g_XiuweiMgr.getRoleXiuweiLevel( self )
		if self.xiuweiLevel != xiuweiLevel:
			self.xiuweiLevel = xiuweiLevel

	def initJingjieLevel(self):
		"""
		初始化境界等级
		"""
		jingjieLevel = g_XiuweiMgr.getRoleJingjieLevel( self )
		if self.jingjieLevel != jingjieLevel:
			self.jingjieLevel = jingjieLevel

	def getXiuwei( self ):
		"""
		获取自身修为值
		"""
		return self.xiuwei
		
	def getXiuweiLevel( self ):
		"""获取修为等级"""
		return self.xiuweiLevel

	def getJingjieLevel( self ):
		"""获取境界等级"""
		return self.jingjieLevel

	def addXiuwei( self, addValue, reason = csdefine.XIUWEI_ADD_REASON_NORMAL ):
		"""
		<define method>
		添加自身修为值
		"""
		oldValue = self.xiuwei
		self.xiuwei += addValue
		if self.xiuwei < 1:
			self.xiuwei = 1
		self.statusMessage( csstatus.ACCOUNT_STATE_GAIN_XIUWEI, addValue )
		self.onXiuWeiChange()
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.remoteScriptCall( "onAddXiuWei", ( self, addValue, reason ) )
		#添加日志
		g_logger.xiuweiChangeLog( self.playerDBID, self.getName(), oldValue, self.xiuwei, reason )
	
	def onXiuWeiChange( self ):
		"""
		修为改变
		"""
		self.updateXiuweiLevel()
		self.updateJingjieLevel()
		self.rewardTitle()
	
	def updateXiuweiLevel( self ):
		"""
		计算修为
		"""
		xiuweiLevel = g_XiuweiMgr.getRoleXiuweiLevel( self )
		if self.xiuweiLevel != xiuweiLevel:
			self.xiuweiLevel = xiuweiLevel
			self.oldCombatPower = self.combatPower
			self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_PROP)
			self.onCombatPowerChange(self.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_PROP)
			self.triggerQuestEvent( QuestEventDefine.EVENT_XIUWEI_LEVEL, xiuweiLevel )

	def updateJingjieLevel( self ):
		"""
		计算境界
		"""
		jingjieLevel = g_XiuweiMgr.getRoleJingjieLevel( self )
		if self.jingjieLevel != jingjieLevel:
			self.jingjieLevel = jingjieLevel

	def addKMGXiuweiRate( self, rate ):
		"""
		添加获得修为倍率
		用于计算杀怪获得更多奖励(如果需要获得1.5倍，rate=0.5)
		"""
		self.kmg_xiuweiRate += rate
		
	def removeKMGXiuweiRate( self, rate ):
		"""移除用于计算杀怪获得更多的修为奖励"""
		self.kmg_xiuweiRate = max(1.0, self.kmg_xiuweiRate - rate )
