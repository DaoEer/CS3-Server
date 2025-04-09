# -*- coding: utf-8 -*-

# 幻兽数据使用原则：
#	以玩家身上的幻兽数据为基准，对幻兽数据的修改都必须先更新玩家的数据。然后玩家那边才分别更新到幻兽或者客户端


import KBEDebug
import KBEngine
import csconst
import Functions
import Const
import ItemSystemExp
import ItemTypeEnum
import CalcProperties

from VehiclePetFormulas import formulas
from ObjectScript.Pet.PetFactory import g_petFactory


def calcProperty( baseVal, extraVal, percentVal, value ):
	"""
	创世基础计算总公式
	计算值=（基础值+成长值）*（1+加成）+附加值
	result = ( corporeity_base + corporeity_extra ) * ( 1 + corporeity_percent ) + corporeity_value
	( 100 + 0 ) * (1 + 0 / 10000 ) + 0 = 100
	( 100 + 0 ) * (1 + 1000 / 10000 ) + 0 = 110

	@param baseVal: 基础值
	@param extraVal: 成长值
	@param percentVal: 加成,此值为float
	@param value: 附加值
	"""
	return ( baseVal + extraVal ) * ( 1 + percentVal/ItemTypeEnum.PRECENTRATIO ) + value

# ----以下数据需要在\common\GenerateCalcProperties.py文件备份一份(前缀BAK_)，以免出现属性计算错误--------satrt
# 一级属性
VPET_ONE_PROPERTY = [ "corporeity", "strength", "intellect", "discern", "dexterity", ]
# 二级属性
VPET_TWO_PROPERTY = [ "HP_Max", "MP_Max", "damage", "magic_damage", "armor", "magic_armor", "criticalstrike",\
					"parry", "speed", "hitrate", "dodgerate", "gangQiValue_Max", "gangQi_damagePoint", "gangQi_armorPoint",\
					"combatPower", "cure", "ice_damage", "fire_damage", "thunder_damage", "xuan_damage", "ice_armor",\
					"fire_armor", "thunder_armor", "xuan_armor", "damage_ignore", "magic_damage_ignore", "armor_ignore",\
					"magic_armor_ignore", "criticalstrike_ignore", "parry_ignore", "hitrate_ignore", "dodgerate_ignore",\
					"ice_damage_ignore", "fire_damage_ignore", "thunder_damage_ignore", "xuan_damage_ignore", "ice_armor_ignore",\
					"fire_armor_ignore", "thunder_armor_ignore", "xuan_armor_ignore", "depress_resist", "hitback_resist",\
					"control_resist", "insane_resist" ]

# 幻兽客户端数据
VPET_SENT_TO_CLIENT_DATAS = ["uid", "scriptID", "step", "quality", "name", "ability", "ability_Max", "attrSkillBox",\
			 				"HP", "MP", "sleepTime", "noLearnedSkillBox", "passiveSkillBox", "gangQiValue", "petShenTongSKill" ]
VPET_SENT_TO_CLIENT_DATAS.extend( VPET_ONE_PROPERTY )
VPET_SENT_TO_CLIENT_DATAS.extend( VPET_TWO_PROPERTY )

# 幻兽Cell数据
VPET_SENT_TO_CLELL_DATAS = ["uid", "scriptID", "step", "quality", "sleepTime", "name"]
# ----以上数据需要在\common\GenerateCalcProperties.py文件备份一份(前缀BAK_)，以免出现属性计算错误----------end

class VehiclePetImp(CalcProperties.CalcProperties):
	"""
	"""
	def __init__( self ):
		CalcProperties.CalcProperties.__init__( self )
		self._propertiesDict = {}								# 用于存储战斗属性
		self.ownerID = 0
		self.profession = 0
	
	def getName( self ):
		"""获取幻兽名字"""
		if self.name:
			return self.name
		petObject = g_petFactory.getObject( self.scriptID )
		if petObject:
			return petObject.getEntityProperty( "uname" )
		return ""
	
	def updatePetEpitomeDatas( self, attrName, value ):
		"""
		幻兽自动更新客户端、cell数据
		"""
		owner = KBEngine.entities.get( self.ownerID, None )
		if owner:
			if attrName in VPET_SENT_TO_CLELL_DATAS:
				owner.cell.updatePetEpitomeDatas( self.uid, attrName, value )
			if attrName in VPET_SENT_TO_CLIENT_DATAS:
				if hasattr(owner, "client") and owner.client:
					owner.client.updatePetEpitomeDatas( str(self.uid), attrName, str(value) )
		else:
			KBEDebug.INFO_MSG("pet cannot find owner(%d),update attr fail!"%self.ownerID )
	
	def generatePetAttr( self, scriptID, quality, solution, camp ):
		"""
		生成幻兽属性
		"""
		self.uid = KBEngine.genUUID64()
		self.scriptID = str( scriptID )
		self.quality = quality
		self.camp = camp
		self.step = 1
		self.exp = 0
		self.name = ""
		self.attrSkillBox = []
		self.passiveSkillBox = []
		self.noLearnedSkillBox = []
		self.unlockbar = ""
		self.sleepTime = 0
		self.HP = 100
		self.MP = 100
		self.HP_Max = 100
		self.MP_Max = 100
		self.gangQiValue = 100
		self.gangQiValue_Max = 100
		self.gangQiState = 1
		self.gangQi_damagePoint = 0
		self.gangQi_armorPoint = 0
		self.gangQi_qiJieRevive = 100
		self.gangQi_qiYingRevive = 100
		self.cure = 1
		self.petShenTongSKill = []
		
		object = g_petFactory.getObject( self.scriptID )
		if object:
			self.takeLevel = object.getEntityProperty( "takeLevel" )
			self.uname = object.getEntityProperty( "uname" )
			
			if object.ability:							# 如果配置了成长度固定值，则不参与成长度的随机生成
				self.ability = object.ability
				abilityMax = formulas.getAbilityMax( quality, self.takeLevel )
				if abilityMax >= self.ability:
					self.ability_Max = abilityMax
				else:
					self.ability_Max = self.ability
					KBEDebug.ERROR_MSG("pet(%s) get ability_Max error!!"%self.scriptID)
			else:
				self.ability, self.ability_Max = formulas.rollAbility( quality, self.takeLevel, solution )
						
			skillBox = object.getSkillIDByQualityAndStep( quality, self.step )
			self.attrSkillBox.extend( skillBox )
			passiveskill = object.getPassiveSkill( quality )
			if passiveskill :
				self.passiveSkillBox.append( passiveskill )
			noLearnedSkill = object.getNoLearnedSkillID(quality, self.step)
			self.noLearnedSkillBox.extend( noLearnedSkill )
		else:
			KBEDebug.ERROR_MSG("Cannot find pet(scriptID:%s) object"%self.scriptID )
			return
		self.calProperties()
		self.combatPower = self.calcCombatPower()
		self.level = formulas.getLevelByStep(self.step)
			
	def calProperties( self ):
		"""
		计算战斗属性
		"""
		oldHP = self.HP
		oldHP_Max = self.HP_Max
		oldMP = self.MP
		oldMP_Max = self.MP_Max
		oldGangQiValue = self.gangQiValue
		oldGangQiValue_Max = self.gangQiValue_Max
		self.calcBasicProperties()
		self.calcLVOneProperties()
		self.calcLVTwoProperties()
		self.updateHPMPByPercent(oldHP,oldHP_Max,oldMP,oldMP_Max,oldGangQiValue,oldGangQiValue_Max)
		self.combatPower = self.calcCombatPower()
		
	def updateHPMPByPercent(self, oldHP,oldHP_Max,oldMP,oldMP_Max,oldGangQiValue,oldGangQiValue_Max):
		"""
		玩家按纪录的比率设置出生血蓝量罡气
		"""
		if self.HP_Max != 0:
			self.HP = round( (self.HP_Max * oldHP) /oldHP_Max) 
		else:
			KBEDebug.ERROR_MSG("Entity[%d] calcAttachProperties error, HP_Max = 0"%self.id)
		if self.MP_Max != 0:
			self.MP = round((self.MP_Max * oldMP) /oldMP_Max)
		else:
			KBEDebug.ERROR_MSG("Entity[%d] calcAttachProperties error, MP_Max = 0"%self.id)
		if self.gangQiValue_Max != 0:
			self.gangQiValue = round((self.gangQiValue_Max * oldGangQiValue) /oldGangQiValue_Max)
		else:
			KBEDebug.ERROR_MSG("Entity[%d] calcAttachProperties error, gangQiValue_Max = 0"%self.id)

	def calcBasicProperties(self):
		"""
		重新设置基础属性值
		"""
		petObject = g_petFactory.getObject( self.scriptID )
		profession = petObject.getEntityProperty("profession")
		level = formulas.getLevelByStep(self.step)
		pProperty = ItemSystemExp.g_PetPropertyValueCfg.getData(profession, level)
		for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
			vv = int(pProperty.get(key, 0)) 
			self._propertiesDict.update( {value + "_base" : vv } )			#设置属性的xxx_base值
			self._propertiesDict.update( {value + "_extra" : 0 } )			#设置属性的xxx_extra值
			self._propertiesDict.update( {value + "_percent" : 0.0 } )		#设置属性的xxx_percent值
			self._propertiesDict.update( {value + "_value" : 0 } )			#设置属性的xxx_value值
		self._propertiesDict["speed_base"] = formulas.getSpeedBaseByStep(self.step, self.quality)
			
	def calcLVOneProperties( self ):
		"""
		重新计算一级属性
		"""
		self._propertiesDict = self.setPetBaseLVOneProperties(self._propertiesDict)
			
	def getResultPropertyValue(self, value):
		"""
		返回xxx的最终结果
		"""
		return min( max(value, ItemTypeEnum.RESULTPROPERTYRANGE[0]), ItemTypeEnum.RESULTPROPERTYRANGE[1] )
		
	def calcLVTwoProperties( self ):
		"""
		重新计算二级属性
		"""
		self._propertiesDict = self.setPetBaseLVTwoProperties(self._propertiesDict)

	def getExchangeTwoPropertyValue(self, propertyID):
		"""
		获取一级属性兑换的二级属性property的值
		@propertyID,二级属性ID
		"""
		result = 0
		petObject = g_petFactory.getObject( self.scriptID )
		self.profession = petObject.getEntityProperty("profession")
		result = self.getExchangeTwoProperty(propertyID)
		result *= self.getAbilityCorrect()				# 成长度修正值
		return result
	
	def getAbilityCorrect( self ):
		"""幻兽成长度修正值"""
		return (( self.ability + csconst.correctBase ) / csconst.correctDivisor ) ** csconst.correctSquare
		
	#--------------------------------------------幻兽游戏功能-------------------------------------------------------------------
	def setStep( self, step ):
		"""设置介次"""
		self.step = step
		self.updatePetEpitomeDatas( "step", self.step )
		self.onStepChange()
		self.level = formulas.getLevelByStep(self.step)
		
	def onStepChange( self ):
		self.calProperties()
		self.onPetStepChangeSetProperties()
		petObject = g_petFactory.getObject( self.scriptID )
		if petObject:
			skillBox = petObject.getSkillIDByQualityAndStep( self.quality, self.step )
			if skillBox:
				self.attrSkillBox.extend( skillBox )
				self.updatePetEpitomeDatas( "attrSkillBox", self.attrSkillBox )
				for i in skillBox:								#将该技能从未学习主动技能列表删除
					if i in self.noLearnedSkillBox: 
						self.noLearnedSkillBox.remove(i)
				self.updatePetEpitomeDatas( "noLearnedSkillBox", self.noLearnedSkillBox )
				
	def reName( self, name ):
		"""改名字"""
		self.name = name
		self.updatePetEpitomeDatas("name", self.name )

	def setAbility( self, ability):
		"""设置成长度"""
		self.ability = ability
		self.updatePetEpitomeDatas("ability", self.ability )

	def setAbilityMax( self, abilityMax ):
		"""设置成长度上限"""
		self.ability_Max = abilityMax
		self.updatePetEpitomeDatas("ability_Max", self.ability_Max )

	def setAttrSkillBox( self, skill, flag ):
		"""设置主动技能"""
		if "add" == flag:	
			if skill not in self.attrSkillBox:
				self.attrSkillBox.append(skill)
				self.updatePetEpitomeDatas("attrSkillBox", self.attrSkillBox )
				if skill in self.noLearnedSkillBox:					#将该技能从未学习主动技能列表删除
					self.noLearnedSkillBox.remove(i)
					self.updatePetEpitomeDatas( "noLearnedSkillBox", self.noLearnedSkillBox )
		if "sub" == flag:
			if skill in self.attrSkillBox:
				self.attrSkillBox.remove(skill)
				self.updatePetEpitomeDatas("attrSkillBox", self.attrSkillBox )

	def setPassiveSkill( self, passiveSkill, flag):
		"""
		设置被动技能
		"""
		if "add" == flag:
			if passiveSkill not in self.passiveSkillBox:
				self.passiveSkillBox.append(passiveSkill)			
		if "sub" == flag:
			if passiveSkill in self.passiveSkillBox:
				self.passiveSkillBox.remove(passiveSkill)
		self.updatePetEpitomeDatas("passiveSkillBox", self.passiveSkillBox )

	def addShenTongSkill( self, skillID, times):
		"""
		增加神通技能
		"""
		index = -1
		for i, element in enumerate(self.petShenTongSKill):
			if list(element.keys())[0] == skillID:
				index = i
				break
		if index >= 0:
			_times = self.petShenTongSKill[index][skillID]
			_times += times
			_times = min(_times, 1000)
			self.petShenTongSKill[index][skillID] = _times
		else:
			self.petShenTongSKill.append({skillID:times})
		self.updatePetEpitomeDatas("petShenTongSKill", self.petShenTongSKill )

	def removeShenTongSkill( self, skillID ):
		"""
		移除神通技能
		"""
		index = -1
		for i, element in enumerate(self.petShenTongSKill):
			if list(element.keys())[0] == skillID:
				index = i
				break
		if index >= 0:
			del self.petShenTongSKill[index]
		self.updatePetEpitomeDatas("petShenTongSKill", self.petShenTongSKill )
		
	def withdrawPetByDead( self ):
		"""进入死亡状态"""
		self.sleepTime = Functions.getTime( Const.VPET_SLEEP_TIME )
		self.updatePetEpitomeDatas( "sleepTime", self.sleepTime )
		
	def updateDBDatas( self, writeToDBDatas ):
		"""幻兽下线，更新幻兽属性"""
		for attrName, value in writeToDBDatas.items():
			setattr( self, attrName, value )
			self.updatePetEpitomeDatas( attrName, value )