# -*- coding: utf-8 -*-
import KBEDebug
import Functions
import csconst
import ItemTypeEnum
from ImpInterface.VehiclePetImp import *
from VehiclePetFormulas import formulas
from ObjectScript.Pet.PetFactory import g_petFactory

class PetCellEpitome( VehiclePetImp ):
	def __init__( self ):
		VehiclePetImp.__init__( self )
	
	def initData( self, data ):
		self.uid = data[ "uid" ]
		self.scriptID = data[ "scriptID" ]
		self.quality = data[ "quality" ]
		self.step = data[ "step" ]
		self.exp = data[ "exp" ]
		self.sleepTime = data[ "sleepTime" ]
		self.name = data[ "name" ]
	
	@classmethod
	def getDictFromObj(self, obj):
		data = {}
		data[ "uid" ] = obj.uid
		data[ "scriptID" ] = obj.scriptID
		data[ "quality" ]	= obj.quality
		data[ "step" ] = obj.step
		data[ "exp" ] = obj.exp
		data[ "sleepTime" ] = obj.sleepTime
		data[ "name" ] = obj.name
		return data

	@classmethod
	def createObjFromDict( self, data ):
		obj = PetCellEpitome()
		obj.initData( data )
		return obj

	def isSameType(self, obj):
		return isinstance( obj, PetCellEpitome )

class PetBaseEpitome( PetCellEpitome ):
	def __init__( self ):
		VehiclePetImp.__init__( self )
	
	def initData( self, data ):
		self.uid = data[ "uid" ] 
		self.scriptID = data[ "scriptID" ]
		self.name = data[ "name" ]
		self.ability = data[ "ability" ]
		self.ability_Max = data[ "ability_Max" ]
		self.quality = data[ "quality" ]
		self.step = data[ "step" ]
		self.exp = data["exp"]
		self.attrSkillBox = data[ "attrSkillBox" ]
		self.passiveSkillBox = data[ "passiveSkillBox" ]
		self.noLearnedSkillBox = data[ "noLearnedSkillBox" ]
		self.HP = data[ "HP" ]
		self.MP = data[ "MP" ]
		self.sleepTime = data[ "sleepTime" ]
		self.gangQiValue = data[ "gangQiValue" ]
		self.camp = data[ "camp" ]
		self.level = data[ "level" ]
		self.uname = data[ "uname" ]
		self.takeLevel = data[ "takeLevel" ]
		#------------一级属性-------------
		self.corporeity = data[ "corporeity" ]
		self.strength = data[ "strength" ]
		self.intellect = data[ "intellect" ]
		self.discern = data[ "discern" ]
		self.dexterity = data[ "dexterity" ]
		#------------二级属性-------------
		self.HP_Max = data[ "HP_Max" ]
		self.MP_Max = data[ "MP_Max" ]
		self.damage = data[ "damage" ]
		self.magic_damage = data[ "magic_damage" ]
		self.armor = data[ "armor" ]
		self.magic_armor = data[ "magic_armor" ]
		self.criticalstrike = data[ "criticalstrike" ]
		self.parry = data[ "parry" ]
		self.speed = data[ "speed" ]
		self.hitrate = data[ "hitrate" ]
		self.dodgerate = data[ "dodgerate" ]		
		self.gangQiValue_Max = data[ "gangQiValue_Max" ]
		self.gangQiState = data[ "gangQiState" ]
		self.gangQi_damagePoint = data[ "gangQi_damagePoint" ]
		self.gangQi_armorPoint = data[ "gangQi_armorPoint" ]
		self.gangQi_qiJieRevive = data[ "gangQi_qiJieRevive" ]
		self.gangQi_qiYingRevive = data[ "gangQi_qiYingRevive" ]
		self.combatPower = data["combatPower"]
		self.cure = data["cure"]
		self.ice_damage = data[ "ice_damage" ]
		self.fire_damage = data[ "fire_damage" ]
		self.thunder_damage = data[ "thunder_damage" ]
		self.xuan_damage = data[ "xuan_damage" ]
		self.ice_armor = data[ "ice_armor" ]
		self.fire_armor = data[ "fire_armor" ]
		self.thunder_armor = data[ "thunder_armor" ]
		self.xuan_armor = data[ "xuan_armor" ]

		self.damage_ignore = data[ "damage_ignore" ]
		self.magic_damage_ignore = data[ "magic_damage_ignore" ]
		self.armor_ignore = data[ "armor_ignore" ]
		self.magic_armor_ignore = data[ "magic_armor_ignore" ]
		self.criticalstrike_ignore = data[ "criticalstrike_ignore" ]
		self.parry_ignore = data[ "parry_ignore" ]
		self.hitrate_ignore = data[ "hitrate_ignore" ]
		self.dodgerate_ignore = data[ "dodgerate_ignore" ]

		self.ice_damage_ignore = data[ "ice_damage_ignore" ]
		self.fire_damage_ignore = data[ "fire_damage_ignore" ]
		self.thunder_damage_ignore = data[ "thunder_damage_ignore" ]
		self.xuan_damage_ignore = data[ "xuan_damage_ignore" ]
		self.ice_armor_ignore = data[ "ice_armor_ignore" ]
		self.fire_armor_ignore = data[ "fire_armor_ignore" ]
		self.thunder_armor_ignore = data[ "thunder_armor_ignore" ]
		self.xuan_armor_ignore = data[ "xuan_armor_ignore" ]

		self.depress_resist = data[ "depress_resist" ]
		self.hitback_resist = data[ "hitback_resist" ]
		self.control_resist = data[ "control_resist" ]
		self.insane_resist = data[ "insane_resist" ]	

		self.initShenTongSkill( data[ "petShenTongSKill" ] )
	
	def initShenTongSkill( self, data ):
		""""""
		self.petShenTongSKill = []
		for skill in data:
			self.petShenTongSKill.append({skill["key"]: skill["value"]})

	def pickDataForClient( self ):
		data = {}
		for property in VPET_SENT_TO_CLIENT_DATAS:
			if property == "uid":
				data[ "uid" ] = str(self.uid)
			elif property == "attrSkillBox":
				data[ "attrSkillBox" ] = list(self.attrSkillBox)
			elif property == "passiveSkillBox":
				data[ "passiveSkillBox" ] = list(self.passiveSkillBox)
			elif property == "noLearnedSkillBox":
				data[ "noLearnedSkillBox" ] = list(self.noLearnedSkillBox)
			else:
				data = self.pickPetDataForClient(data)
		
		return Functions.toJsonString( data )
	
	def getDictForPetCreate( self ):
		"""
		目前来说幻兽的数据分两部份，一部份是配置的固定数据，一部份是要储存的数据
		"""
		data = {}
		data[ "uid" ] = self.uid
		data[ "scriptID" ] = self.scriptID
		data[ "name" ] = self.name
		data[ "ability" ] = self.ability
		data[ "quality" ]	= self.quality
		data[ "step" ] = self.step
		data[ "exp" ] = self.exp
		data[ "attrSkillBox" ] = self.attrSkillBox
		data[ "passiveSkillBox" ] = self.passiveSkillBox
		data[ "noLearnedSkillBox" ] = self.noLearnedSkillBox
		data["level"] = formulas.getLevelByStep(self.step)
		data["HP"] = self.HP
		data["MP"] = self.MP
		data["HP_Max"] = self.HP_Max
		data["MP_Max"] = self.MP_Max
		data[ "gangQiValue" ] = self.gangQiValue
		data[ "gangQiValue_Max" ] = self.gangQiValue_Max
		data[ "gangQiState" ] = self.gangQiState
		data[ "gangQi_damagePoint" ] = self.gangQi_damagePoint
		data[ "gangQi_armorPoint" ] = self.gangQi_armorPoint
		data[ "gangQi_qiJieRevive" ] = self.gangQi_qiJieRevive
		data[ "gangQi_qiYingRevive" ] = self.gangQi_qiYingRevive
		data[ "combatPower" ] = self.combatPower
		data[ "cure" ] = self.cure
		data[ "petShenTongSKill" ] = self.packShenTongSkill()
		return data
	
	def packShenTongSkill( self ):
		""""""
		temp = []
		for element in self.petShenTongSKill:
			tempDict = {}
			tempDict["key"] = list(element.keys())[0]
			tempDict["value"] = list(element.values())[0]
			temp.append(tempDict)
		return temp


	@classmethod
	def getDictFromObj(self, obj):
		data = {}
		data[ "uid" ] = obj.uid
		data[ "scriptID" ] = obj.scriptID
		data[ "name" ] = obj.name
		data[ "ability" ] = obj.ability
		data[ "ability_Max" ] = obj.ability_Max
		data[ "quality" ]	= obj.quality
		data[ "step" ] = obj.step
		data[ "exp" ] = obj.exp
		data[ "attrSkillBox" ] = obj.attrSkillBox
		data[ "passiveSkillBox" ] = obj.passiveSkillBox
		data[ "noLearnedSkillBox" ] = obj.noLearnedSkillBox
		data[ "HP" ] = obj.HP
		data[ "MP" ] = obj.MP
		data["sleepTime"] = obj.sleepTime
		data[ "gangQiValue" ] = obj.gangQiValue
		data[ "camp" ] = obj.camp
		data[ "level" ] = obj.level
		data[ "uname" ] = obj.uname
		data[ "takeLevel" ] = obj.takeLevel
		#------------一级属性-------------
		data[ "corporeity" ] = obj.corporeity
		data[ "strength" ] = obj.strength
		data[ "intellect" ] = obj.intellect
		data[ "discern" ] = obj.discern
		data[ "dexterity" ] = obj.dexterity
		#------------二级属性-------------
		data[ "HP_Max" ] = obj.HP_Max
		data[ "MP_Max" ] = obj.MP_Max
		data[ "damage" ] = obj.damage
		data[ "magic_damage" ] = obj.magic_damage
		data[ "armor" ] = obj.armor
		data[ "magic_armor" ] = obj.magic_armor
		data[ "criticalstrike" ] = obj.criticalstrike
		data[ "parry" ] = obj.parry
		data[ "speed" ] = obj.speed
		data[ "hitrate" ] = obj.hitrate
		data[ "dodgerate" ] = obj.dodgerate
		data[ "gangQiValue_Max" ] = obj.gangQiValue_Max
		data[ "gangQiState" ] = obj.gangQiState
		data[ "gangQi_damagePoint" ] = obj.gangQi_damagePoint
		data[ "gangQi_armorPoint" ] = obj.gangQi_armorPoint
		data[ "gangQi_qiJieRevive" ] = obj.gangQi_qiJieRevive
		data[ "gangQi_qiYingRevive" ] = obj.gangQi_qiYingRevive
		data[ "combatPower" ] = obj.combatPower
		data[ "cure" ] = obj.cure
		data[ "ice_damage" ] = obj.ice_damage
		data[ "fire_damage" ] = obj.fire_damage
		data[ "thunder_damage" ] = obj.thunder_damage
		data[ "xuan_damage" ] = obj.xuan_damage
		data[ "ice_armor" ] = obj.ice_armor
		data[ "fire_armor" ] = obj.fire_armor
		data[ "thunder_armor" ] = obj.thunder_armor
		data[ "xuan_armor" ] = obj.xuan_armor

		data[ "damage_ignore" ] = obj.damage_ignore
		data[ "magic_damage_ignore" ] = obj.magic_damage_ignore
		data[ "armor_ignore" ] = obj.armor_ignore
		data[ "magic_armor_ignore" ] = obj.magic_armor_ignore
		data[ "criticalstrike_ignore" ] = obj.criticalstrike_ignore
		data[ "parry_ignore" ] = obj.parry_ignore
		data[ "hitrate_ignore" ] = obj.hitrate_ignore
		data[ "dodgerate_ignore" ] = obj.dodgerate_ignore

		data[ "ice_damage_ignore" ] = obj.ice_damage_ignore
		data[ "fire_damage_ignore" ] = obj.fire_damage_ignore
		data[ "thunder_damage_ignore" ] = obj.thunder_damage_ignore
		data[ "xuan_damage_ignore" ] = obj.xuan_damage_ignore
		data[ "ice_armor_ignore" ] = obj.ice_armor_ignore
		data[ "fire_armor_ignore" ] = obj.fire_armor_ignore
		data[ "thunder_armor_ignore" ] = obj.thunder_armor_ignore
		data[ "xuan_armor_ignore" ] = obj.xuan_armor_ignore

		data[ "depress_resist" ] = obj.depress_resist
		data[ "hitback_resist" ] = obj.hitback_resist
		data[ "control_resist" ] = obj.control_resist
		data[ "insane_resist" ] = obj.insane_resist

		data[ "petShenTongSKill" ] = obj.packShenTongSkill()
		
		return data

	@classmethod
	def createObjFromDict( self, data ):
		obj = PetBaseEpitome()
		obj.initData( data )
		return obj

	def isSameType(self, obj):
		return isinstance( obj, PetBaseEpitome )

	def getAbilityCorrect( self ):
		"""幻兽成长度修正值"""
		return (( self.ability + csconst.correctBase ) / csconst.correctDivisor ) ** csconst.correctSquare

	def calcCombatPower(self):
		"""
		没出站时计算战斗力
		"""
		M1 = 0.0
		correct = self.getAbilityCorrect()
		M1 = self.getVehiclePetPropertyFactor(correct)

		M2 = 0.0
		petObject = g_petFactory.getObject( self.scriptID )
		profession = petObject.getEntityProperty( "profession", 1 )
		if profession in csconst.PROFESSION_CORRECTION_FACTOR:
			M2 = self.getProfessionCorrectoin().get( profession, 0.0)

		return int(round((M1-M2*correct)/50))
		
	#-------------------------------------------------------------------------------------
	# 虚拟原兽继承虚拟幻兽，公共接口
	#-------------------------------------------------------------------------------------
	def getWildness( self ):
		"""野性值"""
		return 0
		
	def isEvolution( self ):
		"""是否已进化"""
		return 1

	def isCDTime( self ):
		"""CD时间"""
		return self.sleepTime > Functions.getTime()
	
	def setCDTime( self, time):
		"""
		原兽的sleepTime属性为喂养CD时间
		幻兽的sleepTime属性为召唤CD时间
		"""
		self.sleepTime = time
		
	def addExp( self, playerMB, exp ):
		""""""
		self.exp += exp
		needExp = formulas.getNeedExpNextStep( self.step+1, self.quality )
		if self.exp >= needExp:
			self.exp -= needExp
			self.step += 1
			self.level = formulas.getLevelByStep(self.step)
			self.calProperties()
			self.onOriginPetStepChangeSetProperties(playerMB)

class OriginPetEpitome( PetBaseEpitome ):
	"""原兽数据"""
	def __init__( self ):
		PetBaseEpitome.__init__( self )
		self.wildness = 0
		self.bEvolution = 0
		
	def generatePetAttr( self, scriptID, quality, solution, camp ):
		"""
		生成幻兽属性
		"""
		PetBaseEpitome.generatePetAttr( self, scriptID, quality, solution, camp )
		self.wildness = 100
		self.bEvolution = 0
		
	def reduceWildness( self, subWildness ):
		"""
		减低野性
		"""
		self.wildness = max(0, self.wildness-subWildness )
	
	def canEvolution( self ):
		"""是否能进化"""
		return self.wildness == 0
	
	def isEvolution( self ):
		"""是否已经进化"""
		return self.bEvolution
		
	def evolution( self ):
		"""进化"""
		self.bEvolution = 1
		
	def getWildness( self ):
		"""野性值"""
		return self.wildness

	def updateOriginPetEpitomeDatas( self, playerMB, attrName, value ):
		"""
		幻兽原兽自动更新客户端
		"""
		KBEDebug.ERROR_MSG("attrName: ", attrName, "  value: ", value)
		if attrName in VPET_SENT_TO_CLIENT_DATAS:
			if hasattr(playerMB, "client") and playerMB.client:
				playerMB.client.updateOriginPetEpitomeDatas( str(self.uid), attrName, str(value) )
		
	def initData( self, data ):
		PetBaseEpitome.initData( self, data )
		self.exp = data["exp"]
		self.wildness = data["wildness"]
		self.bEvolution = data["bEvolution"]
	
	@classmethod
	def getDictFromObj(self, obj):
		data = PetBaseEpitome.getDictFromObj( obj)
		data[ "exp" ] = obj.exp
		data["wildness"] = obj.getWildness()
		data["bEvolution"] = obj.isEvolution()
		return data

	@classmethod
	def createObjFromDict( self, data ):
		obj = OriginPetEpitome()
		obj.initData( data )
		return obj

	def isSameType(self, obj):
		return isinstance( obj, OriginPetEpitome ) or isinstance( obj, PetBaseEpitome )			# 因为需要相互转换，所以在这里也定义

baseInst = PetBaseEpitome()
cellInst = PetCellEpitome()
originPetInst = OriginPetEpitome()