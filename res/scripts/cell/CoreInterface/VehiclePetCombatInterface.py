# -*- coding: utf-8 -*-

#engine
import KBEngine
#common
import csdefine
import csconst
import csstatus
import Functions
import ItemSystemExp
import ItemTypeEnum
import KBEDebug
#cell
import Const
import math
from FightRuleMgr import g_fightMgr
from CoreInterface import CombatInterface
from VehiclePetFormulas import formulas
from CoreInterface import VehiclePetAIInterface
from ObjectScript.Pet.PetFactory import g_petFactory
from StateInterface.VehiclePetStateInterface import VehiclePetStateInterface
import CoreInterface.GangQiInterface as GangQiInterface

FIND_ENEMY_RANGE	= 10	#默认的搜索敌人范围

class VehiclePetCombatInterface( VehiclePetStateInterface, CombatInterface.CombatInterface ):
	"""
	幻兽战斗接口
	"""
	def __init__( self ):
		VehiclePetStateInterface.__init__(self)
		CombatInterface.CombatInterface.__init__( self )
		self.level = formulas.getLevelByStep( self.step )
		self.timeBack = 0

	def addDamageList( self, entityID, damage ):
		"""
		"""
		CombatInterface.CombatInterface.addDamageList( self, entityID, damage )
		entity = KBEngine.entities.get( entityID )
		owner = self.getOwnerEntity()
		if entity and self.canBuildEnemyRelation( entity ):
			g_fightMgr.buildEnemyRelation( owner, entity )

	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		CombatInterface.CombatInterface.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		self.onPeteRecvieDamage( casterID )

	def onPeteRecvieDamage( self, casterID ):
		"""
		玩家之间的幻兽脱战
		"""
		enemy = KBEngine.entities.get( casterID )
		owner = self.getOwnerEntity()
		if self.timeBack and (enemy.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or enemy.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET):
			self.popTimer(self.timeBack)
			self.timeBack = 0
		if (casterID in self.enemyList or casterID in self.damageList) and (enemy.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or enemy.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET): 
			if self.getState() == csdefine.ENTITY_STATE_DEAD:
				if self.id in enemy.enemyList:
					enemy.addTimerCallBack( 8, "removeEnemy", (self.id,))
			if self.enemyList:
				for casterID in self.enemyList:
					self.timeBack = self.addTimerCallBack( 8, "onDamageListCompare", ( self.id, casterID, ))
			else:
				for casterID in self.damageList:
					self.timeBack = self.addTimerCallBack( 8, "onDamageListCompare", ( self.id, casterID, ))

	#-----------------------幻兽离开战斗回血相关-----------------------------------------------------------
	def onRemoveEnemy( self, entityID ):
		"""
		"""
		CombatInterface.CombatInterface.onRemoveEnemy( self, entityID )
		if len( self.enemyList ) == 0:
			self.changeState( csdefine.ENTITY_STATE_FREE )	
	
	def onEnterFree( self ):
		"""
		virtual method
		进入自由状态
		"""
		VehiclePetStateInterface.onEnterFree( self )
		GangQiInterface.GangQiInterface.onEnterFree( self )

		#尝试开启自愈
		self.startRevertTimer()
		KBEDebug.DEBUG_MSG("onEnterFree")

	def onLeaveFree( self ):
		"""
		离开自由状态
		"""
		VehiclePetStateInterface.onLeaveFree( self )

		#停止自愈
		self.stopRevertTimer()

	#-----------------------幻兽血槽规则-----------------------------------------------------------
	def onHPChanged( self, oldValue ):
		"""
		血量改变回调
		"""
		CombatInterface.CombatInterface.onHPChanged( self, oldValue )
		self.onActiveBloodSlot()

	def onActiveBloodSlot( self ):
		"""
		是否有激活血槽
		"""
		owner = self.getOwnerEntity()
		if owner is None:return

		if not owner.isActiveHP:
			return				# 玩家没有激活该功能

		percentHP = int(math.floor(self.HP/self.HP_Max*100))
		if percentHP >= owner.percentHP:
			return				# 幻兽血量还没低于玩家设置的百分比

		if not self.findBuffsByBuffID( csconst.PET_USE_BLOOD_SLOT_BUFF ):
			self.addBuff( self, csconst.PET_USE_BLOOD_SLOT_BUFF )

	def onMPChanged( self, oldValue ):
		"""
		MP改变回调
		"""
		CombatInterface.CombatInterface.onMPChanged( self, oldValue )
		self.onActiveBlueChannel()

	def onActiveBlueChannel( self ):
		"""
		是否激活蓝槽
		"""
		owner = self.getOwnerEntity()
		if owner is None:return

		if not owner.isActiveMP:
			return				# 玩家没有激活该功能

		percentMP = int(math.floor(self.MP/self.MP_Max*100))
		if percentMP >= owner.percentMP:
			return				# 幻兽血量还没低于玩家设置的百分比

		if not self.findBuffsByBuffID( csconst.PET_USE_BLUE_CHANNEL_BUFF ):
			self.addBuff( self, csconst.PET_USE_BLUE_CHANNEL_BUFF )

	#-----------------------Property-----------------------------------------------------------
	def getLevel( self ):
		return self.level
		
	def getProfession( self ):
		"""获取职业"""
		return self.profession
	
	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		profession = self.profession
		level = formulas.getLevelByStep( self.step )
		return ItemSystemExp.g_PetPropertyValueCfg.getData(profession, level)
	
	def getEquipAttachProperties(self):
		"""
		为了在CombatInterface中统一处理属性计算
		"""
		return {}
		
	def getExchangeTwoPropertyValue(self, propertyID):
		"""
		获取一级属性兑换的二级属性property的值
		@propertyID,二级属性ID
		"""
		result = 0
		result = self.getExchangeTwoProperty(propertyID)
		result *= self.getAbilityCorrect()				# 成长度修正值
		return result
	
	def getAbilityCorrect( self ):
		"""幻兽成长度修正值"""
		return (( self.ability + csconst.correctBase ) / csconst.correctDivisor ) ** csconst.correctSquare

	def calcBaseProperties(self):
		"""
		重新设置基础属性值, xxx_base
		"""
		self.setVehiclePetBaseProperties()

	def calcExtraProperties(self):
		"""
		计算属性的成长值，xxx_extra
		装备只影响属性成长值
		"""
		buffdic = self.getBuffProperties().get("_extra", {})
		dic = ItemSystemExp.combineDict(buffdic, self.getEquipAttachProperties().get("_extra", {}))
		self.setVehiclePetExtraProperties(dic)
		
	#--------------------------------------技能------------------------------------------------------------------
	def setCooldown( self, cooldownDict ):
		"""
		设置冷却时间
		"""
		CombatInterface.CombatInterface.setCooldown( self, cooldownDict )
		self.updateCooldownToClient(cooldownDict)

	def changeCooldown( self, cooldownDict ):
		"""
		增/减CD
		"""
		CombatInterface.CombatInterface.changeCooldown( self, cooldownDict )
		self.updateCooldownToClient(cooldownDict)

	def updateCooldownToClient( self, cooldownDict ):
		"""
		更新冷却时间数据到客户端
		"""
		if len(self.attrCooldowns) == 0:
			return
		owner = self.getOwnerEntity()
		if owner is None:return
		
		idList = []
		endTimeList = []
		persistTimeList = []
		currTime = Functions.getTime()
		for dDict in self.attrCooldowns:
			if dDict["id"] in cooldownDict:
				idList.append( str(dDict["id"]) )
				endTimeList.append( str(dDict["endTime"]) )
				persistTimeList.append( str(dDict["persistTime"]) )
		owner.clientEntity( self.id ).SetCooldown( idList, endTimeList, persistTimeList )


#---------战斗属性计算------------------------------------------------------------------------
	def calcAttachProperties( self ):
		"""
		重新计算战斗属性
		"""
		CombatInterface.CombatInterface.calcAttachProperties(self)
		self.calcCombatPower()

	def calcCombatPower(self):
		"""
		重新计算战斗力
		"""
		M1 = 0.0
		correct = self.getAbilityCorrect()
		M1 = self.getVehiclePetPropertyFactor(correct)

		M2 = 0.0
		petObject = g_petFactory.getObject( self.scriptID )
		profession = petObject.getEntityProperty( "profession", 1 )
		if profession in csconst.PROFESSION_CORRECTION_FACTOR:
			M2 = self.getProfessionCorrectoin().get(profession, 0.0)
		
		self.combatPower = int(round((M1-M2*correct)/50))