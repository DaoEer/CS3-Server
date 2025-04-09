#coding:utf-8

import sys
import KBEDebug
import ItemTypeEnum
from ObjectScript.ObjectScriptBase import EntityPropertyLoader

class PetPropertyLoader( EntityPropertyLoader.EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.EntityPropertyLoader.__init__( self )
		self._skillIDs = {}
		self.foodType = ItemTypeEnum.ORIGIN_PET_FOOD_TYPE_COMMON

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.EntityPropertyLoader.initData( self, configData )
			if 'Uname' in configData:
				self.setEntityProperty("uname",str(configData["Uname"]))			# 名称

			if 'profession' in configData:
				self.setEntityProperty("profession",int(configData["profession"]))			# 种族

			if 'takeLevel' in configData:
				self.setEntityProperty("takeLevel",int(configData["takeLevel"]))			# 可携带等级

			if 'carrierId' in configData:
				self.carrierId = str(configData["carrierId"])			# 载具模型编号
			
			if "foodType" in configData:
				self.foodType = int(configData["foodType"])
			
			skillStrs = ["Skills_1", "Skills_2", "Skills_3", "Skills_4", "Skills_5" ]
			for skillStr in skillStrs:
				if skillStr in configData:
					index = int( skillStr.split("_")[1] )
					self._skillIDs[index] = {}
					
					skillIDs = configData[skillStr].split("|")
					for skillID in skillIDs:
						idStr = skillID.split(":")
						if len( idStr ) >= 2:
							self._skillIDs[index].update( {int(idStr[0]) : int(idStr[1])} )
			
		else:
			KBEDebug.WARNING_MSG("PetPropertyLoader::initData() configData is none!!!")
