
import ConfigObject.Item.ItemBase as ItemBase
import random
import ItemTypeEnum
import KBEDebug

class ItemPetExpFood(ItemBase.ItemBase):
	"""
	原兽特殊食材
	用于 在兽栏中的幻兽 增加经验
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
		self.petQualityMapExp = {}			# { 幻兽品质 ：{随机经验最小值 ： 随机经验最大值} }
		self.foodType = ItemTypeEnum.ORIGIN_PET_FOOD_TYPE_COMMON
		self.CDTimeList = []					# 私有洞府/公有仙府，花费时间CD
		
		expStrList = srcData["Param1"].split("|")
		quelityList = [int(i) for i in srcData["Param2"].split("|")]
		assert len(expStrList) == len(quelityList), "ItemPetExpFood(id:%d) Param1 or Param2 is err!"%self.id
		for i in zip(quelityList, expStrList):
			randList = i[1].split(":")
			self.petQualityMapExp[i[0]] = {int(randList[0]) : int(randList[1])}
			
		self.foodType = int(srcData["Param3"])
		self.CDTimeList = [int(i) for i in srcData["Param4"].split("|")]
				
	def canFeedPet( self, foodType, quality ):
		"""是否是原兽食用食材"""
		if not quality in self.petQualityMapExp:
			return False
		if self.foodType == ItemTypeEnum.ORIGIN_PET_FOOD_TYPE_COMMON:
			return True
		return self.foodType == foodType
				
	def getPetExp( self, quality ):
		""""""
		for min, max in self.petQualityMapExp[quality].items():
			return random.randint(min, max)
		
	def getCDTime(self, spaceType):
		"""获取CD 时间"""
		return self.CDTimeList[spaceType-1]