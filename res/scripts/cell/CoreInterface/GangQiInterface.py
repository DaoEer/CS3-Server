# -*- coding: utf-8 -*-

#罡气接口

import math
import Const
import csdefine
import ItemTypeEnum
import ItemSystemExp
import KBEDebug


QI_DUAN_PERSIST_TIME = 2.0	#气短持续时间
QI_YING_REVIVE_TICK = 2.0	#气盈恢复tick
QI_JIE_REVIVE_TICK = 1.0	#气竭恢复tick

class StateBase:
	"""
	基类
	"""
	def __init__( self ):
		pass
	
	@classmethod
	def onEnter( self, entity ):
		pass
	
	@classmethod
	def onLeave( self, entity ):
		pass
	
	@classmethod
	def onReviveGangQi( self, entity, value ):
		pass
	
	@classmethod
	def onRecvGangQiDamage( self, entity, value ):
		pass
	
	@classmethod
	def onEnterFree( self, entity ):
		pass
	
	@classmethod
	def onEnterDead( self, entity ):
		pass

#----------------------------------------
# 气盈

# 状态描述：罡气不为0、罡气缓慢恢复、有格挡效果
# 受到罡气伤害 ——> 进入气短状态
# 罡气一刀减为0 ——> 进入气竭状态
#----------------------------------------

class StateQiYing( StateBase ):
	"""
	"""
	@classmethod
	def onEnter( self, entity ):
		if not entity.gangQi_isFull():
			entity.gangQi_startQiYingRevive()
	
	@classmethod
	def onLeave( self, entity ):
		entity.gangQi_endRevive()
	
	@classmethod
	def onReviveGangQi( self, entity, value ):
		if entity.gangQi_isFull():
			entity.gangQi_endRevive()
	
	@classmethod
	def onRecvGangQiDamage( self, entity, value ):
		if entity.gangQiValue == 0:
			entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JIE )
		else:
			entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_DUAN )
	
	@classmethod
	def onEnterDead( self, entity ):
		entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JUE )

#----------------------------------------
# 气短：

# 状态描述：受到罡气伤害的短时间内、罡气不恢复、有格挡效果
# 期间再次受到罡气伤害 ——> 刷新气短时间
# 持续时间结束 ——> 进入气盈状态
# 罡气减到0 ——> 进入气竭状态
#----------------------------------------

class StateQiDuan( StateBase ):
	"""
	"""
	@classmethod
	def onEnter( self, entity ):
		entity.gangQi_qiDuanOverTimerID = entity.addTimerCallBack( QI_DUAN_PERSIST_TIME, "gangQi_changeState", (csdefine.GANG_QI_STATE_QI_YING,) )
	
	@classmethod
	def onLeave( self, entity ):
		entity.popTimer( entity.gangQi_qiDuanOverTimerID )
		entity.gangQi_qiDuanOverTimerID = 0
	
	@classmethod
	def onRecvGangQiDamage( self, entity, value ):
		if entity.gangQiValue == 0:
			entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JIE )
		else:
			entity.popTimer( entity.gangQi_qiDuanOverTimerID )
			entity.gangQi_qiDuanOverTimerID = entity.addTimerCallBack( QI_DUAN_PERSIST_TIME, "gangQi_changeState", (csdefine.GANG_QI_STATE_QI_YING,) )
	
	@classmethod
	def onEnterDead( self, entity ):
		entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JUE )

#----------------------------------------
# 气竭

# 状态描述：罡气从0恢复到满的过程、罡气快速恢复、无格挡效果
# 罡气回满—>进入气盈状态
#----------------------------------------
class StateQiJie( StateBase ):
	"""
	"""
	@classmethod
	def onEnter( self, entity ):
		entity.addBuff( entity, Const.BUFF_GANG_QI_QI_JIE )
		entity.gangQi_startQiJieRevive()
	
	@classmethod
	def onLeave( self, entity ):
		entity.gangQi_endRevive()
	
	@classmethod
	def onReviveGangQi( self, entity, value ):
		if entity.gangQi_qiJieIsFull():
			entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_YING )
	
	@classmethod
	def onEnterDead( self, entity ):
		entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JUE )

#----------------------------------------
# 气绝

# 状态描述：entity死亡状态
# entity复活 ——> 进入气盈状态
#----------------------------------------
class StateQiJue( StateBase ):
	"""
	"""
	@classmethod
	def onEnter( self, entity ):
		entity.gangQiValue = 0
	
	@classmethod
	def onLeave( self, entity ):
		entity.gangQiValue = entity.gangQiValue_Max
	
	@classmethod
	def onEnterFree( self, entity ):
		if entity.gangQiValue_Max > 0:	#罡气上限为0，复活时不进入气盈状态
			entity.gangQi_changeState( csdefine.GANG_QI_STATE_QI_YING )


TYPE_TO_CLASS_MAP = {	csdefine.GANG_QI_STATE_QI_YING	:		StateQiYing,
						csdefine.GANG_QI_STATE_QI_DUAN	:		StateQiDuan,
						csdefine.GANG_QI_STATE_QI_JIE	:		StateQiJie,
						csdefine.GANG_QI_STATE_QI_JUE	:		StateQiJue,
					}


class GangQiInterface:
	"""
	"""
	def __init__( self ):
		"""
		"""
		pass
	
	def updateGangQiMaxValue( self, oldGangQiValue_Max ):
		"""
		更新罡气上限
		"""
		if self.gangQiValue_Max == oldGangQiValue_Max:
			return
		
		if oldGangQiValue_Max == 0 and self.gangQiValue_Max != 0:
			self.gangQiValue = self.gangQiValue_Max
			self.gangQi_changeState( csdefine.GANG_QI_STATE_QI_YING )	#变得有罡气了，马上回满并进入气盈状态
		elif oldGangQiValue_Max != 0 and self.gangQiValue_Max == 0:
			self.gangQi_changeState( csdefine.GANG_QI_STATE_QI_JUE )	#变得没有罡气了，让其进入气绝状态，使罡气不产生影响

		if self.gangQiValue > self.gangQiValue_Max:
			self.gangQiValue = self.gangQiValue_Max
		if self.gangQiState == csdefine.GANG_QI_STATE_QI_YING and self.gangQiValue < self.gangQiValue_Max:
			self.gangQi_endRevive()
			self.gangQi_startQiYingRevive()
	
	#-----------------------------------------------------
	# 罡气状态
	#-----------------------------------------------------
	def __getStateCls( self ):
		return TYPE_TO_CLASS_MAP.get( self.gangQiState, None )
	
	def gangQi_changeState( self, state ):
		"""
		罡气状态改变
		"""
		if self.gangQiState == state:
			return
		if self.gangQiState:
			self.__getStateCls().onLeave( self )
		self.gangQiState = state
		self.__getStateCls().onEnter( self )
	
	def onEnterFree( self ):
		"""
		entity变为普通状态
		"""
		self.__getStateCls().onEnterFree( self )
	
	def onEnterDead( self ):
		"""
		entity变为死亡状态
		"""
		self.__getStateCls().onEnterDead( self )
	
	#----------------------------------------------------
	#罡气值
	#----------------------------------------------------
	def gangQi_addValue( self, value ):
		"""
		增加罡气值，只做数值的增减，不应加入玩法逻辑
		"""
		validValue = min( self.gangQiValue_Max, self.gangQiValue + value )
		if self.gangQiValue == validValue:
			return 0
		
		oldValue = self.gangQiValue
		self.gangQiValue = validValue
		self.onGangQiValueChanged()
		return self.gangQiValue - oldValue
	
	def gangQi_reduceValue( self, value ):
		"""
		减少罡气值，只做数值的增减，不应加入玩法逻辑
		"""
		validValue = max( 0, self.gangQiValue - value )
		if self.gangQiValue == validValue:
			return 0
		
		oldValue = self.gangQiValue
		self.gangQiValue = validValue
		self.onGangQiValueChanged()
		return oldValue - self.gangQiValue

	def onGangQiValueChanged(self):
		"""
		罡气改变回调
		"""
		oldValue = self.gangQiValuePercent
		newValue = self.gangQiValue/self.gangQiValue_Max
		if oldValue != newValue:
			self.gangQiValuePercent = newValue
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROPERTY_PERCENT_CHANGE, self.id, {"propertyType":"gangQiValue", "oldValue":oldValue,"newValue":newValue } )		

	def gangQi_isFull( self ):
		"""
		罡气值已满？
		"""
		return self.gangQiValue == self.gangQiValue_Max

	def gangQi_qiJieIsFull( self ):
		"""
		罡气气竭进度值已满?
		"""
		if self.gangQi_qiJieProgress == self.gangQiValue_Max:
			self.gangQiValue = self.gangQiValue_Max
			return True
		return False
	
	def gangQi_startQiYingRevive( self ):
		"""
		开始气盈恢复
		"""
		#配置中的罡气自愈率为“每秒自愈百分比 * 1000”, 所以每次tick恢复罡气值需要乘以tick时间
		value = math.ceil((self.gangQiValue_Max * self.gangQi_qiYingRevive * 1.0 / ItemTypeEnum.PRECENTRATIO ) * QI_YING_REVIVE_TICK)
		if value == 0:
			return
		self.gangQi_onReviveTimer( value )	#开始时刻执行一次
		self.gangQi_reviveTimerID = self.addTimerRepeat( QI_YING_REVIVE_TICK, "gangQi_onReviveTimer", (value,) )
	
	def gangQi_startQiJieRevive( self ):
		"""
		开始气竭恢复
		"""
		value = math.ceil((self.gangQiValue_Max * self.gangQi_qiJieRevive * 1.0 / ItemTypeEnum.PRECENTRATIO) * QI_JIE_REVIVE_TICK )
		if value == 0:
			return
		self.gangQi_qiJieOnReviveTimer( value )	#开始时刻执行一次
		self.gangQi_reviveTimerID = self.addTimerRepeat( QI_JIE_REVIVE_TICK, "gangQi_qiJieOnReviveTimer", (value,) )
	
	def gangQi_endRevive( self ):
		"""
		结束恢复
		"""
		if self.gangQi_reviveTimerID:
			self.popTimer( self.gangQi_reviveTimerID )
			self.gangQi_reviveTimerID = 0
			self.gangQi_qiJieProgress = 0
	
	def gangQi_onReviveTimer( self, value ):
		"""
		罡气恢复tick
		"""
		validValue = self.gangQi_addValue( value )
		self.__getStateCls().onReviveGangQi( self, validValue )

	def gangQi_qiJieProgressAdd(self, value):
		"""
		气竭进度值增加, 只是用来模拟气竭时进度条增加
		"""
		validValue = min( self.gangQiValue_Max, self.gangQi_qiJieProgress + value )
		if self.gangQi_qiJieProgress == validValue:
			return 0
		
		oldValue = self.gangQi_qiJieProgress
		self.gangQi_qiJieProgress = validValue
		return self.gangQi_qiJieProgress - oldValue		


	def gangQi_qiJieOnReviveTimer( self, value ):
		"""
		罡气气竭恢复tick
		"""
		validValue = self.gangQi_qiJieProgressAdd( value )
		self.__getStateCls().onReviveGangQi( self, validValue )

	
	def getGangQiDamage( self, receiver, skillRate, skillExtra ):
		"""
		计算罡气伤害
		
		实际罡气伤害 = 技能罡气伤害 *（1 - 罡气防御减伤）
		技能罡气伤害 = 罡气攻击 * 技能附加罡气攻击比例 + 技能附加罡气伤害固定值
		罡气防御减伤 = 罡气防御 /（罡气防御 + 调节系数）
		"""
		baseCombatData = ItemSystemExp.g_CombatNormalDamager.getBaseCombatData( receiver.getLevel(), receiver.getProfession() )
		adjustValue = baseCombatData.get( "GangQiArmorPoint", 0 )	#调节系数
		
		if ( receiver.gangQi_armorPoint + adjustValue ) != 0:
			armor = receiver.gangQi_armorPoint / ( receiver.gangQi_armorPoint + adjustValue )
		else:
			armor = 0
		damage = self.gangQi_damagePoint * skillRate + skillExtra
		resultDamage = damage * ( 1 - armor )
		return math.ceil(resultDamage)
	
	def recvGangQiDamage( self, value ):
		"""
		接受罡气伤害
		"""
		if value <= 0:
			return
		
		if self.gangQiState in [ csdefine.GANG_QI_STATE_QI_JIE, csdefine.GANG_QI_STATE_QI_JUE ]:	#气竭和气绝状态免疫罡气伤害
			return
		
		validValue = self.gangQi_reduceValue( value )
		if validValue:
			self.__getStateCls().onRecvGangQiDamage( self, validValue )
	
	def isInGangQiArmor( self ):
		"""
		处于罡气格挡状态
		"""
		return self.gangQiState in [ csdefine.GANG_QI_STATE_QI_YING, csdefine.GANG_QI_STATE_QI_DUAN ]
	