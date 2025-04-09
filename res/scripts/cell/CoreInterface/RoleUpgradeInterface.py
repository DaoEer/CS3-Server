# -*- coding: utf-8 -*-
import time
from KBEDebug import *
import csdefine
import csstatus
from LevelExp import*
from MsgLogger import g_logger
import QuestEventDefine

class RoleUpgradeInterface:
	"""
	角色成长模块
	"""
	def __init__( self ):
		if self.lastUpTime == 0:
			self.lastUpTime = int(self.loginTime)

	def addExp( self, expValue, reasonType ):
		"""
		添加角色经验
		使用例子：self.addExp( 100, csdefine.EXP_ADD_REASON_KILL_MONSTER )
		"""
		if expValue == 0:
			return
		self.showReason( reasonType )
		oldExp = self.exp
		oldLevel = self.level
		self.__addExp( expValue, reasonType )
		self.addPetExp( expValue, reasonType )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.remoteScriptCall( "onAddExp", ( self, expValue, reasonType ) )
		#添加日志
		g_logger.expChangeLog( self.playerDBID, self.getName(), oldExp, oldLevel, self.exp, self.getLevel(), reasonType )

	def getLevel( self ):
		"""
		获取角色等级
		"""
		return self.level

	def setLevel( self, newLevel ):
		"""
		set level of the role
		@type 			newLevel :  int
		@param 			newLevel :  the new level to be set
		"""
		if newLevel == self.level:
			return
		if newLevel > csconst.ROLE_LEVEL_UPPER_LIMIT:
			newLevel = csconst.ROLE_LEVEL_UPPER_LIMIT
		oldLevel = self.level
		self.level = newLevel
		self.onLevelUp( oldLevel )
		self.tong_roleLevelUp()
		
		#添加日志
		useTime = int(time.time()) - self.lastUpTime
		g_logger.roleUpgradeLog( self.playerDBID, self.getName(), oldLevel, newLevel, time.time() )
		g_logger.roleUpLevelLog( self.accountDBID, self.playerDBID, self.getLevel(), useTime, self.lastUpTime)
		
		self.lastUpTime = int(time.time()) 

	def __addExp( self, exp, reasonType ):
		"""
		增加经验
		@type 		exp ：int
		@param 		exp : 增加的经验
		"""
		level = self.level
		if level >= csconst.ROLE_LEVEL_UPPER_LIMIT:
			return

		allExp = exp + self.exp
		RoleLevelExp.init()
		maxExp = RoleLevelExp.getMaxExp( level )
		if not maxExp:
			ERROR_MSG("maxExp is None!")
			return

		while allExp >= maxExp:
			level += 1
			allExp -= maxExp
			maxExp = RoleLevelExp.getMaxExp( level )
			if not maxExp:
				ERROR_MSG("maxExp is None!")
				break
		if level > csconst.ROLE_LEVEL_UPPER_LIMIT : # 将等级限制在限制等级以内
			level = csconst.ROLE_LEVEL_UPPER_LIMIT
			allExp = RoleLevelExp.getMaxExp( level )

		self.exp = allExp
		expStr = "@F%i"%exp
		self.statusMessage( csstatus.ACCOUNT_STATE_GAIN_EXP,expStr )
		if reasonType == csdefine.EXP_ADD_REASON_BY_SPELLBOX:
			self.client.ShowSpellBoxResultMessage( csdefine.SPELL_BOX_RESULT_ADDEXP, exp )
		self.maxExp = RoleLevelExp.getMaxExp( level )
		self.setLevel( level )

	def onLevelUp( self, oldLevel ):
		"""
		levalUp callBack
		"""
		oldGangQiValue_Max = self.gangQiValue_Max
		self.base.onLevelUp( self.level )
		self.statusMessage( csstatus.ACCOUNT_CHANGE_LEVEL, self.level )
		self.updateXiuweiLevel()
		self.updateJingjieLevel()
		self.rewardTitle()
		self.oldCombatPower = self.combatPower
		self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_PROP)	#必须更新修为等级后再更新属性
		self.onCombatPowerChange(self.oldCombatPower,csdefine.CALC_COMBAT_POWER_REASON_PROP)
		self.updatePkModeOnLevelChange( oldLevel )
		self.onSetPetSlotValue()
		self.triggerQuestEvent( QuestEventDefine.EVENT_PLAYER_LEVEL, self.level )
		self.gangQi_addValue(self.gangQiValue_Max - self.gangQiValue)

	def showReason( self, reasonType ):
		"""
		打印增加经验的原因
		"""
		pass

