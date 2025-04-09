# -*- coding: utf-8 -*-


"""
usage:
	可战斗对象基类

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#common
import csdefine
import csconst
import ItemSystemExp
import ItemTypeEnum
import CalcProperties
import KBEDebug
import KBEngine
import math
#cell
import CoreInterface.SkillInterface as SkillInterface
import CoreInterface.CSkillInterface as CSkillInterface
import CoreInterface.EntityRelationTable as EntityRelationTable
import CoreInterface.GangQiInterface as GangQiInterface
import Const
import csstatus


CHECK_POSITION_TIME = 10.0


def calcProperty( baseVal, extraVal, percentVal, value ):
	"""
	创世基础计算总公式
	计算值=（基础值+成长值）*（1+加成）+附加值
	result = ( corporeity_base + corporeity_extra ) * ( 1 + corporeity_percent ) + corporeity_value-
	( 100 + 0 ) * (1 + 0 / 10000 ) + 0 = 100
	( 100 + 0 ) * (1 + 1000 / 10000 ) + 0 = 110

	@param baseVal: 基础值
	@param extraVal: 成长值
	@param percentVal: 加成,此值为float
	@param value: 附加值
	"""
	return ( baseVal + extraVal ) * ( 1 + percentVal/ItemTypeEnum.PRECENTRATIO ) + value


class CombatInterface( SkillInterface.SkillInterface,  CSkillInterface.CSkillInterface, EntityRelationTable.EntityRelationTable, GangQiInterface.GangQiInterface, CalcProperties.CalcProperties ):
	def __init__( self ):
		SkillInterface.SkillInterface.__init__( self )
		CSkillInterface.CSkillInterface.__init__( self )
		EntityRelationTable.EntityRelationTable.__init__( self )
		GangQiInterface.GangQiInterface.__init__( self )
		CalcProperties.CalcProperties.__init__( self )
		
#		# 测试设置HP,MP初值
#		self.HP_Max = 100
#		self.setHP( 100 )
#		self.MP_Max = 50
#		self.setMP( 50 )
		self.buffproperties = { "_extra" : {}, "_percent" : {}, "_value" : {}, "_base" : {} }
		if KBEngine.cellAppData.has_key( "openCheckPos" ):
			self.openCheckPos()
		self.calcAttachProperties()
	
	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		SkillInterface.SkillInterface.doEnterSpace( self )

	def doLeaveSpace( self ):
		"""
		离开一个空间调用（在doEnterSpace之后）
		"""
		SkillInterface.SkillInterface.doLeaveSpace( self )
		

	def onSkillInterrupted( self, skillID, reason ):
		"""
		virtual method
		当施法被打断时的通知
		"""
		SkillInterface.SkillInterface.onSkillInterrupted(self, skillID, reason)

	def onSkillEnd( self, skillInstance, castResult ):
		"""
		virtual method.
		技能结束

		@param  skillInstance: 技能实例
		@type   skillInstance: SPELL
		"""
		SkillInterface.SkillInterface.onSkillEnd( self, skillInstance, castResult )

	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		SkillInterface.SkillInterface.beforeDestroy( self )
		self.buffproperties.clear()
	
	#----------服务器&客户端位置同步检测---------------------------------------------------------
	def openCheckPos( self ):
		"""
		打开位置同步检测
		"""
		self.checkPosTimerID = self.addTimerRepeat( CHECK_POSITION_TIME, "onCheckPosTimer", () )

	def closeCheckPos( self ):
		"""
		关闭位置同步检测
		"""
		if self.checkPosTimerID != 0:
			self.popTimer( self.checkPosTimerID )
			self.checkPosTimerID = 0

	def onCheckPosTimer( self ):
		"""
		位置同步检测timer回调
		"""
		self.allClients.CLIENT_CheckClientPosition()
		
	def CELL_receivePosFromClient( self, srcEntityID, clientPos ):
		"""
		<Exposed Method>
		发送位置到服务器
		"""
		distance = self.position.distTo( clientPos )
		if distance > 1.0:
			KBEDebug.DEBUG_MSG( "Check position error, %s(%s) space:%s server position:%s client position:%s distance:%s" %(\
			self, self.id, self.getCurrentSpaceScriptID(), self.position, clientPos, distance ) )
	
	#-------------------------------------------------------------------------
	def receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		"""
		<Define method>
		接收伤害
		"""
		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return
		
		isUnyielding = 0
		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			if int(self.HP - damage ) <= 1:
				isUnyielding = 1

		oldHP = self.HP
		if isUnyielding:
			self.setHP(1)
		else:
			self.setHP( self.HP - damage )
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.setMP( 0 )
			self.onBeKill( casterID, deadEffect, actForbid )
		
		finalDamage = oldHP - self.HP
		self.onReceiveDamage( casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
	
	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		try:
			self.allClients.ReceiveSkill( casterID, skillID, csdefine.DAMAGE_TYPE_PHYSICS, finalDamage, int(isCritical), int(isParry) )
		except:
			KBEDebug.CRITICAL_MSG( "thow error Data: casterID=%i, skillID=%i, damageType=%i, damage=%i " % \
			( casterID, skillID, damageType, damage ) )
	
	def onBeKill( self, killerID, deadEffect, actForbid ):
		"""
		被击杀
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ON_DIE, killerID, { "actForbid": actForbid, "type" : csdefine.SKILL_EVENT_RECEIVER_DIE } )
		killer = KBEngine.entities.get( killerID, None )
		if killer:
			killer.triggerSkillEvent(csdefine.SKILL_EVENT_ON_DIE, self.id , { "actForbid": actForbid, "type" : csdefine.SKILL_EVENT_CASTER_DIE } )
		
	def addHP( self, addValue ):
		newValue = self.HP + addValue
		self.setHP( newValue )
	
	def setHP( self, value ):
		"""
		设置HP
		"""
		if value < 1.0:
			value = 0
		elif value > self.HP_Max:
			value = self.HP_Max

		oldValue = self.HP
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			value = min(0, value)
		self.HP = value
		if oldValue != value:
			self.onHPChanged( oldValue )
		if self.HP <= 0:
			self.changeState( csdefine.ENTITY_STATE_DEAD )
	
	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		self.onHPPercentChanged()

	def onHPPercentChanged(self):
		oldValue = self.HPPercent
		newValue = self.HP/self.HP_Max
		if oldValue != newValue:
			self.HPPercent = newValue
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROPERTY_PERCENT_CHANGE, self.id, {"propertyType":"HP", "oldValue":oldValue,"newValue":newValue } )

	def addMP( self, addValue ):
		newValue = self.MP + addValue
		self.setMP( newValue )
	
	def setMP( self, value ):
		"""
		设置MP
		"""
		if value < 1.0:
			value = 0
		elif value > self.MP_Max:
			value = self.MP_Max

		oldValue = self.MP
		self.MP = value
		if oldValue != value:
			self.onMPChanged( oldValue )
	
	def onMPChanged( self, oldValue ):
		"""
		MP改变回调
		"""
		self.onMPPercentChanged()
		if self.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			#触发魔法值改变事件
			self.triggerEvent( csdefine.ENTITY_EVENT_MP_CHANGE , "" )


	def onMPPercentChanged(self):
		oldValue = self.MPPercent
		newValue = self.MP/self.MP_Max
		if oldValue != newValue:
			self.MPPercent = newValue
			self.triggerSkillEvent( csdefine.SKILL_EVENT_PROPERTY_PERCENT_CHANGE, self.id, {"propertyType":"MP", "oldValue":oldValue,"newValue":newValue } )

	def setHPAttrValue( self, value ):
		if value < 1.0:
			value = 0
		elif value > self.HP_Max:
			value = self.HP_Max
		oldValue = self.HP
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			value = min(0, value)
		self.HP = value
		if oldValue != value:
			self.onHPChanged( oldValue )

	def setMPAttrValue( self, value ):
		if value < 1.0:
			value = 0
		elif value > self.MP_Max:
			value = self.MP_Max
		oldValue = self.MP
		self.MP = value
		if oldValue != value:
			self.onMPChanged( oldValue )

	def isWillDead(self, damage):
		"""
		受术者是否会死亡
		"""
		if self.HP == 0 and self.getState() == csdefine.ENTITY_STATE_DEAD:
			return False

		if self.hasEffectState( csdefine.EFFECT_STATE_UNYIELDING ):
			return False

		return damage >= self.HP

#---------战斗属性计算------------------------------------------------------------------------
	def calcAttachProperties( self, reason = csdefine.CALC_COMBAT_POWER_REASON_DEFAULT):
		"""
		重新计算战斗属性
		"""
		oldHP = self.HP
		oldHP_Max = self.HP_Max
		oldMP = self.MP
		oldMP_Max = self.MP_Max
		oldGangQiValue_Max = self.gangQiValue_Max
		self.calcBasicProperties()
		self.calcLVOneProperties()
		#self.printPropertyResult()
		self.calcLVTwoProperties()
		self.calcResultProperties()
		#self.printPropertyResult()

		#调用对应的RoleCombatInterface和MonsterCombatInterface中的updateBornHPMP方法
		self.updateHPMPByPercent(oldHP,oldHP_Max,oldMP,oldMP_Max)
		self.updateGangQiMaxValue( oldGangQiValue_Max )
		#在重新计算属性之后要设置实际的移动速度
		self.initSpeed()
	
	def updateHPMPByPercent(self, oldHP,oldHP_Max,oldMP,oldMP_Max):
		"""
		玩家按纪录的比率设置出生血蓝量
		"""
		if self.HP_Max != 0:
			HP = self.HP_Max * oldHP /oldHP_Max
			if HP>0 and HP<1:
				HP = 1

			self.setHP(round(HP))
		else:
			KBEDebug.ERROR_MSG("Entity[%d] calcAttachProperties error, HP_Max = 0"%self.id)
		if self.MP_Max != 0:
			MP = self.MP_Max * oldMP /oldMP_Max
			if MP>0 and MP<1:
				MP = 1
			self.setMP(round(MP))
		else:
			KBEDebug.ERROR_MSG("Entity[%d] calcAttachProperties error, MP_Max = 0"%self.id)

	def calcBasicProperties(self):
		"""
		重新计算基础属性
		"""
		self.calcBaseProperties()
		self.calcExtraProperties()
		self.calcPrecentProperties()
		self.calcValueProperties()
	
	#----------------------------获取属性数据，重新对属性的4个值进行赋值-----------------------

	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		#由子类具体实现
		pass

	def calcBaseProperties(self):
		"""
		重新设置基础属性值, xxx_base
		"""
		pass
		

	def calcExtraProperties(self):
		"""
		计算属性的成长值，xxx_extra
		装备只影响属性成长值
		"""
		pass

	def calcPrecentProperties(self):
		"""
		计算属性的增长百分比， xxx_precent
		buff影响属性的增长百分比
		"""
		buffdic = self.getBuffProperties().get("_percent", {})
		dic = ItemSystemExp.combineDict(buffdic, self.getEquipAttachProperties().get("_percent", {}))
		self.setPrecentProperties(dic)

	def calcValueProperties(self):
		"""
		计算属性附加值， xxx_value
		buff影响属性的附加值
		"""
		buffdic = self.getBuffProperties().get("_value", {})
		dic = ItemSystemExp.combineDict(buffdic, self.getEquipAttachProperties().get("_value", {}))
		self.setValueProperties(dic)

	def setBuffProperties( self, pDict ):
		"""
		<Define method>
		设置buff属性（百分比、附加值）
		"""
		keylist = ["_extra", "_base", "_percent", "_value"]
		for key in keylist:
			if key in self.buffproperties:
				self.buffproperties[key] = ItemSystemExp.combineDict(self.buffproperties[key], pDict.get(key, {}))
			
	def getBuffProperties( self ):
		"""
		获取buff添加的属性
		"""
		return self.buffproperties

	#----------------------------获取属性数据，重新对属性的4个值进行赋值-----------------------
	def getBaseResultPropertyValue(self, value):
		"""
		返回xxx_base最终结果
		"""
		return min( max(value, ItemTypeEnum.BASEPROPERTYRANGE[0]), ItemTypeEnum.BASEPROPERTYRANGE[1] )

	def getExtraResultPropertyValue(self, value):
		"""
		返回xxx_extra最终结果
		"""
		return min( max(value, ItemTypeEnum.EXTRAPROPERTYRANGE[0]), ItemTypeEnum.EXTRAPROPERTYRANGE[1] )

	def getPrecentResultPropertyValue(self, value):
		"""
		返回xxx_precent的最终结果
		"""
		return min( max(value, ItemTypeEnum.PRECENTPROPERTYRANGE[0]), ItemTypeEnum.PRECENTPROPERTYRANGE[1] )

	def getValueResultPropertyValue(self, value):
		"""
		返回xxx_value的最终结果
		"""
		return min( max(value, ItemTypeEnum.VALUEPROPERTYRANGE[0]), ItemTypeEnum.VALUEPROPERTYRANGE[1] )

	def getResultPropertyValue(self, value):
		"""
		返回xxx的最终结果
		"""
		return min( max(value, ItemTypeEnum.RESULTPROPERTYRANGE[0]), ItemTypeEnum.RESULTPROPERTYRANGE[1] )
		

	def calcLVOneProperties( self ):
		"""
		重新计算一级属性
		"""
		self.setLVOneProperties()

	
	def getExchangeTwoPropertyValue(self, propertyID):
		"""
		获取一级属性兑换的二级属性property的值
		@propertyID,二级属性ID
		"""
		return self.getExchangeTwoProperty(propertyID)

	def calcLVTwoProperties( self ):
		"""
		重新计算二级属性
		"""
		self.setLVTwoProperties()

	def calcResultProperties(self):
		"""
		计算属性的最终值
		"""
		pass
		
	#---------攻击目标------------------------------------------------------------------------
	def setTargetID(self, newTargetID):
		"""
		设置攻击目标ID
		"""
		self.targetID  = newTargetID

	def getTargetID(self):
		"""
		得到攻击目标ID
		"""
		return self.targetID

	#----------嘲讽者目标ID---------------------------------------------------------------
	def setTauntID( self, newTauntID ):
		"""
		设置嘲讽者ID
		"""
		self.tauntID = newTauntID

	def getTauntID( self ):
		"""
		获得嘲讽者ID
		"""
		return self.tauntID


	#----------------自动恢复-------------------------------------------------------------

	def canStartRevert( self ):
		"""
		能否开启恢复
		"""
		KBEDebug.DEBUG_MSG( "canStartRevert revertTimerID[%d], state[%d], healingrate[%d]"%(self.revertTimerID, self.state, self.healingrate) )
		if self.revertTimerID != 0:return False
		if self.state != csdefine.ENTITY_STATE_FREE:	return False	#非自由状态不能开始自动恢复
		if self.healingrate <= 0:	return False	#自愈值不大于0，也就不会开启自愈功能
		return True

	def startRevertTimer( self ):
		"""
		启动HP和MP自动恢复
		"""
		KBEDebug.DEBUG_MSG("startRevertTimer")
		if self.canStartRevert():
			self.revertTimerID = self.addTimerRepeat( Const.FREE_START_TIME, "onRevertTimer", () )
			KBEDebug.DEBUG_MSG("startRevertTimer successs")

	def canStopRevert( self ):
		"""
		能否关闭恢复
		"""
		if self.HP >= self.HP_Max and self.MP >= self.MP_Max:	#满血满蓝状态下关闭恢复
			return True
		return False

	def stopRevertTimer( self ):
		"""
		停止HP和MP的自动恢复
		"""
		if self.revertTimerID:
			self.popTimer( self.revertTimerID )
			self.revertTimerID = 0

	def onRevertTimer( self ):
		"""
		恢复HP和MP
		math.ceil 向上取整
		"""
		if self.HP < self.HP_Max:
			self.addHP( math.ceil((self.HP_Max * self.healingrate * 1.0 / ItemTypeEnum.PRECENTRATIO ) * Const.FREE_START_TIME) )					# 每秒恢复10HP、MP，仅用测试使用
		if self.MP < self.MP_Max:
			self.addMP( math.ceil((self.MP_Max * self.healingrate * 1.0 / ItemTypeEnum.PRECENTRATIO ) * Const.FREE_START_TIME) )

		#恢复完之后停止timer
		if self.canStopRevert():
			self.stopRevertTimer()

	#---------------------- timer --------------------------
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		SkillInterface.SkillInterface.timerValeDelCB( self, timerArg )
			
	def CELL_receiveDirectionFromClient(self, srcEntityID, direction):
		"""
		<Exposed Method>
		发送朝向到服务器
		"""
		self.direction = direction


	#---------------------------------仇恨列表--------------------------------------------
	def addRelatedHatred(self, entityID, value):
		"""
		增加自然连带仇恨
		"""
		for enemyID in self.enemyList.keys():
			enemy = KBEngine.entities.get(enemyID, None)
			if enemy and enemy.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				enemy.autoAddRelatedHatred(entityID, value)
