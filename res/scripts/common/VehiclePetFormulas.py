# -*- coding: utf-8 -*-


"""
幻兽的公式计算
"""
import csdefine
import Singleton
import random
from KBEDebug import *
import ItemTypeEnum
import LoadModule

#幻兽成长度
from Pet import VPetAbilityOutput
from Pet import VPetAbilitySegments
from Pet import VPetAbilityRateSolutions
#幻兽介次相关
from Pet import VPetCorrLevel
from Pet import VPetPotential
from Pet import VPetSealCharm
from Pet import VPetComposeExpend
from Pet import VPetMakeBook



def convertToLevelStep(level):
	"""将等级映射到一个等级段：例如41、43、44、49都属于40级段"""
	return max( int( level / 10 ) * 10, 10 )

class VehiclePetFormulas(Singleton.Singleton):
	"""
	"""
	def __init__( self ):
		self._feedPetCfg = {}
		self.loadDatas()
		
	def loadDatas( self ):
		""""""
		Datas = LoadModule.openJsonCfg("Pet/PetFeedCfg.json")
		for data in Datas:
			foodNum = data.pop("foodNum")
			petQuality = data.pop("quality")
			if not foodNum in self._feedPetCfg:
				self._feedPetCfg[foodNum] = {}
			if not petQuality in self._feedPetCfg[foodNum]:
				self._feedPetCfg[foodNum][petQuality] ={}
				
			self._feedPetCfg[foodNum][petQuality].update( {csdefine.TRADE_PAY_ITEM_MONEY : data["money"]} )
			self._feedPetCfg[foodNum][petQuality].update( {csdefine.TRADE_PAY_ITEM_POTENTIAL : data["potential"]} )
	
	def getLevelByStep( self, step ):
		"""获取介次对应的等级"""
		if step in VPetCorrLevel.Datas:
			return VPetCorrLevel.Datas[step]
		return 0
		
	def getSpeedPlusByStep( self, step, quality ):
		"""
		获取移动速度加成
		"""
		return int( VPetPotential.Datas[step][quality]["speed"] * ItemTypeEnum.PRECENTRATIO )
		
	def getSpeedBaseByStep( self, step, quality ):
		"""
		获取移动速度加成
		"""
		return VPetPotential.Datas[step][quality]["speedBase"] 
		
	def getPetMaxStep( self ):
		"""幻兽最大介次"""
		return max(VPetPotential.Datas)
		
	def getNeedExpNextStep( self, nextStep, quality ):
		"""获取幻兽升下一介所需经验"""
		return VPetPotential.Datas[nextStep][quality]["exp"]
		
	def getAbilityMax( self, quality , takeLevel):
		"""获取成长度最大值"""
		level = convertToLevelStep( takeLevel )
		output = VPetAbilityOutput.Datas.get(level)
		return max(output[quality])

	def rollAbility( self, quality, takeLevel, solution ):
		"""成长度随机"""
		rates = VPetAbilityRateSolutions.Datas.get( solution )
		roll = random.uniform(0,sum(rates.values()))
		rate_stepper = 0
		for key, value in rates.items():
			rate_stepper += value
			if roll <= rate_stepper:
				segment = key
				break
				
		lower, upper = VPetAbilitySegments.Datas.get(segment)
		
		level = convertToLevelStep( takeLevel )
		output = VPetAbilityOutput.Datas.get(level)
		if output is None:
			ERROR_MSG("VehiclePet roll ability err!!Cannot find level(%i) config"%level)
			return 1, 1
		
		output_range = output.get(quality)
		if output_range is None:
			ERROR_MSG("No output range data of level %s grade %s" % (level, grade))
			return 1, 1
		
		DValue = output_range[1] - output_range[0]
		return int( output_range[0] + random.uniform(DValue*lower, DValue*upper) ),output_range[1]

	
	def getSealCharmAmount( self, scriptID, takeLevel, quality ):
		"""获取幻兽封印所需要的封印符的数量"""
		if scriptID in VPetSealCharm.Datas:
			return VPetSealCharm.Datas[scriptID][takeLevel][quality].get("need_sealcharm", 1)
		return 1

	def getSealCharmItemID( self, scriptID, takeLevel, quality ):
		"""获取幻兽封印成幻兽蛋的物品ID"""
		if scriptID in VPetSealCharm.Datas:
			return VPetSealCharm.Datas[scriptID][takeLevel][quality].get("pet_itemID", 0)
		return 0
		
	def getBeastPearlAmount( self, scriptID, takeLevel, quality ):
		"""获取原兽进化所需要的兽灵珠的数量"""
		if scriptID in VPetSealCharm.Datas:
			return VPetSealCharm.Datas[scriptID][takeLevel][quality].get("need_beastpearl", 1)
		return 1

	def getEvolutionItemID( self, scriptID, takeLevel, quality ):
		"""获取原兽进化成幻兽蛋的物品ID"""
		if scriptID in VPetSealCharm.Datas:
			return VPetSealCharm.Datas[scriptID][takeLevel][quality].get("evolution_itemID", 0)
		return 0
		
	def getComposeMoney( self, quality ):
		"""获取幻兽合成所需要的金钱"""
		if quality in VPetComposeExpend.Datas:
			return VPetComposeExpend.Datas[quality].get("money", 1)
		return 1

	def getComposeMaterials( self, quality ):
		"""获取幻兽合成所需要的仙灵果的数量"""
		if quality in VPetComposeExpend.Datas:
			return VPetComposeExpend.Datas[quality].get("xianlingguo", 1)
		return 1

	def getReplacePetSkillElixir(self, skillid, skillQuality):
		"""获取幻兽主动技能替换所需的启化丹"""
		if skillid in VPetMakeBook.Datas:
			return VPetMakeBook.Datas[skillid][skillQuality]["elixir"]
		return 1

	def getUpgradePetSkillPotential( self, skillid, skillQuality ):
		"""获取主动技能升级所需要潜能"""
		if skillid in VPetMakeBook.Datas:
			return VPetMakeBook.Datas[skillid][skillQuality]["needPotential"]
		return 1

	def getReplacePetSkillMoney(self, skillid, skillQuality):
		"""获取幻兽主动技能替换所需的金钱"""
		if skillid in VPetMakeBook.Datas:
			return VPetMakeBook.Datas[skillid][skillQuality]["money"]
		return 1

	def getUpgradePetSkillMoney(self, skillid, skillQuality):
		"""获取幻兽被动技能升级所需的金钱"""
		if skillid in VPetMakeBook.Datas:
			return VPetMakeBook.Datas[skillid][skillQuality]["passive_money"]
		return 1

	def getUpgradePetPassiveSkillProb( self, skillid, skillQuality, bookQuality):
		"""根据残卷获取升级被动技能的概率*10000"""
		if skillid in VPetMakeBook.Datas:
			ProbList = VPetMakeBook.Datas[skillid][skillQuality]["brokenbook"].split("|")
			return int(float(ProbList[bookQuality-1])*100)
		return 0
		
	def getFeedPetCost(self, foodNum, quality):
		"""获取幻兽驯养 额外消耗"""
		if foodNum in self._feedPetCfg and quality in self._feedPetCfg[foodNum]:
			return self._feedPetCfg[foodNum][quality]
		return {}

formulas  = VehiclePetFormulas()