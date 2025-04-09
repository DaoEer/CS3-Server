# -*- coding: utf-8 -*-


from KBEDebug import *
from FaceStyle import FaceStyle
import ItemTypeEnum
import LoadModule
import json
import csconst
import csdefine
import Const

class RoleModelInterface:
	def __init__(self):
		if self.coatModelTemp:
			self.coatModel = self.coatModelTemp
			self.coatModelTemp = ""
		coatItemInst = self.getItemInstByOrder( ItemTypeEnum.EQUIP_COAT )
		if coatItemInst:
			self.setCoatModel("eCoatModel", coatItemInst.modelSources[self.getGender()])

	def getModelDict( self ):
		"""
		获取模型列表
		"""
		modelList = {}
		modelList["modelNumber"] = self.modelNumber
		modelList["headModel"] = self.headModel
		modelList["cloakModel"] = self.cloakModel
		modelList["bodyModel"] = self.bodyModel
		modelList["hairModel"] = self.hairModel
		modelList["adornModel"] = self.adornModel
		modelList["suitsModel"] = self.suitsModel
		modelList["hatModel"] = self.hatModel
		modelList["coatModel"] = self.coatModel
		modelList["wristModel"] = self.wristModel
		modelList["handModel"] = self.handModel
		modelList["waistModel"] = self.waistModel
		modelList["pantsModel"] = self.pantsModel
		modelList["shoesModel"] = self.shoesModel
		modelList["necklaceModel"] = self.necklaceModel
		modelList["rringModel"] = self.rringModel
		modelList["weaponModel"] = self.weaponModel
		modelList["fabaoModel"] = self.fabaoModel
		modelList["headAdornModel"] = self.headAdornModel
		modelList["faceAdornModel"] = self.faceAdornModel
		modelList["backAdornModel"] = self.backAdornModel
		modelList["waistAdornModel"] = self.waistAdornModel
		
		return modelList


	def onHeadWield(self, item):
		"""
		装备头部回调
		"""
		if self.headModel != item.modelSources[self.getGender()]:
			self.headModel = item.modelSources[self.getGender()]

	def onHeadUnWield(self, item):
		"""
		卸载头部装备回调
		"""
		self.headModel = self.getModelPartDataByPartKey("headModel")

	def onHatWield(self, item):
		"""
		装备帽子
		"""
		if self.hatModel != item.modelSources[self.getGender()]:
			self.hatModel = item.modelSources[self.getGender()]

	def onHatUnWield(self, item):
		"""
		"""
		self.hatModel = self.getModelPartDataByPartKey("hatModel")

	def onCoatWield(self, item):
		"""
		装备coat回调
		"""
		if self.coatModel != item.modelSources[self.getGender()]:
			self.setCoatModel("eCoatModel", item.modelSources[self.getGender()])

	def onCoatUnWield(self, item):
		"""
		卸载coat回调
		"""
		self.setCoatModel("eCoatModel", self.getModelPartDataByPartKey("coatModel"))

	def onWristWield(self, item):
		"""
		护腕
		"""
		if self.wristModel != item.modelSources[self.getGender()]:
			self.wristModel = item.modelSources[self.getGender()]

	def onWristUnWield(self, item):
		"""
		护腕
		"""
		self.wristModel = self.getModelPartDataByPartKey("wristModel")

	def onHandWield(self, item):
		"""
		手套
		"""
		if self.handModel != item.modelSources[self.getGender()]:
			self.handModel = item.modelSources[self.getGender()]

	def onHandUnWield(self, item):
		"""
		手套
		"""
		self.handModel = self.getModelPartDataByPartKey("handModel")

	def onWaistWield(self, item):
		"""
		腰带
		"""
		if self.waistModel != item.modelSources[self.getGender()]:
			self.waistModel = item.modelSources[self.getGender()]

	def onWaistUnWield(self, item):
		"""
		腰带
		"""
		self.waistModel = self.getModelPartDataByPartKey("waistModel")

	def onPantsWield(self, item):
		"""
		装备裤子回调
		"""
		if self.pantsModel != item.modelSources[self.getGender()]:
			self.pantsModel = item.modelSources[self.getGender()]

	def onPantsUnWield(self, item):
		"""
		卸载裤子装备回调
		"""
		self.pantsModel = self.getModelPartDataByPartKey("pantsModel")

	def onShoesWield(self, item):
		"""
		装备鞋子回调
		"""
		if self.shoesModel != item.modelSources[self.getGender()]:
			self.shoesModel = item.modelSources[self.getGender()]

	def onShoesUnWield(self, item):
		"""
		卸载鞋子装备回调
		"""
		self.shoesModel = self.getModelPartDataByPartKey("shoesModel")

	def onNecklaceWield(self, item):
		"""
		装备项链回调
		"""
		if self.necklaceModel != item.modelSources[self.getGender()]:
			self.necklaceModel = item.modelSources[self.getGender()]

	def onNecklaceUnWield(self, item):
		"""
		卸载项链装备回调
		"""
		self.necklaceModel = self.getModelPartDataByPartKey("necklaceModel")


	def onRingWield(self, item):
		"""
		装备戒指回调
		"""
		if self.itemsBag.getOrderID(item.uid) == ItemTypeEnum.EQUIP_RING:		#左手戒指
			if self.lringModel != item.modelSources[self.getGender()]:
				self.lringModel = item.modelSources[self.getGender()]
		else:		#右手戒指
			if self.rringModel != item.modelSources[self.getGender()]:
				self.rringModel = item.modelSources[self.getGender()]

	def onRingUnWield(self, item):
		"""
		卸载戒指回调
		"""
		if self.itemsBag.getOrderID(item.uid) == ItemTypeEnum.EQUIP_RING:		#左手戒指
			self.lringModel = self.getModelPartDataByPartKey("lringModel")
		else:		#右手戒指
			self.rringModel = self.getModelPartDataByPartKey("rringModel")

	def onCloakWield(self, item):
		"""
		装备披风回调
		"""
		if self.cloakModel != item.modelSources[self.getGender()]:
			self.setCloakModel("eCarrierId",item.modelSources[self.getGender()])

	def onClockUnWield(self, item):
		"""
		卸载披风回调
		"""
		self.setCloakModel("eCarrierId",self.getModelPartDataByPartKey("cloakModel"))

	def onBodyWield(self, item):
		"""
		装备上身回调
		"""
		if self.bodyModel != item.modelSources[self.getGender()]:
			self.bodyModel = item.modelSources[self.getGender()]

	def onBodyUnWield(self, item):
		"""
		卸载装备回调
		"""
		self.bodyModel = self.getModelPartDataByPartKey("bodyModel")

	def onWeaponWield(self, item):
		"""
		装备武器回调
		"""
		# 左手武器模型|右手武器模型|左手骨架武器模型|右手骨架武器模型
		modelPart = item.modelSources[self.getGender()].split("|", 2)
		weaponModelStr = modelPart[0]
		if len(modelPart) > 1:
			weaponModelStr = modelPart[0] + "|" + modelPart[1]
		if self.weaponModel != weaponModelStr:
			self.weaponModel = weaponModelStr
			if len(modelPart) >= 3 and self.skeletalWeaponModel != modelPart[2]:
				self.skeletalWeaponModel = modelPart[2]

	def onWeaponUnWield(self, item):
		"""
		卸载武器装备回调
		"""
		self.weaponModel = self.getModelPartDataByPartKey("weaponModel")
		self.skeletalWeaponModel = self.getModelPartDataByPartKey("skeletalWeaponModel")

	def onSuitsWield(self, item):
		"""
		装备suits回调
		"""
		if self.suitsModel != item.modelSources[self.getGender()]:
			self.suitsModel = item.modelSources[self.getGender()]

	def onSuitsUnWield(self, item):
		"""
		卸载suits回调
		"""
		self.suitsModel = self.getModelPartDataByPartKey("suitsModel")

	def onFabaoWield(self, item):
		"""
		装备suits回调
		"""
		if self.fabaoModel != item.modelSources[self.getGender()]:
			self.fabaoModel = item.modelSources[self.getGender()]

	def onFabaoUnWield(self, item):
		"""
		卸载法宝回调
		"""
		self.fabaoModel = self.getModelPartDataByPartKey("fabaoModel")


	def getModelPartDataByPartKey( self, key ):
		"""
		获得某装备部位的数据
		"""
		datas = LoadModule.openJsonCfg("InitModelTable.json")
		modelStr = csconst.ROLE_INIT_MODULE[self.getGender()].get(self.getProfession(),"Default")
		return datas[modelStr][key]


	def ReqFaceData(self,srcEntityID):

		if not self.validateClientCall( srcEntityID ):
			return

		faceModelData = self.faceModel
		if faceModelData==None or faceModelData == b'':
			faceModelData=b'[]'
		faceData=json.loads(bytes.decode(faceModelData))

		faceModel = {"infos": faceData}
		faceStyle = FaceStyle().createObjFromDict(json.loads(self.faceStyle))
		if self.getAllClients():
			self.allClients.CLIENT_OnReqFaceData(faceModel, faceStyle)

#-------------------------------------------------外观---------------------------------------------------
	def setStoreAppearanceByType(self, aType, value, itemID = 0):
		"""
		设置商城外观	
		"""
		if aType == 21: 	#时装
			self.setCoatModel("sCoatModel", value)
		elif aType == 13: 	#发型
			self.setHairModel("sHairModel", value)
		elif aType == 15:	#头饰
			self.setHeadAdornModel("sHeadAdornModel", value)
		elif aType == 16:	#面饰
			self.setFaceAdornModel("sFaceAdornModel", value)
		elif aType == 17:	#背饰
			self.setBackAdornModel("sBackAdornModel", value, itemID)
		elif aType == 18:	#腰饰
			self.setWaistAdornModel("sWaistAdornModel", value)
		elif aType == 34:	#披风
			self.setCloakModel("sCloakModel", value)
		elif aType == 38:	#环身
			self.bodyLightEffect = value
		elif aType == -1:	#坐骑
			self.setCarrierId("sCarrierId", value)
		self.client.OnUpdateStoreAppearance(aType)

	def setCoatModel(self, key, value):
		"""
		换时装
		key:
		sCoatModel(商城外观上衣)> eCoatModel(装备上衣)
		"""
		self.appearance.update({key:value})
		if self.coatModel == value:
			return
			
		sCoatModel = self.appearance.get("sCoatModel", "")
		eCoatModel = self.appearance.get("eCoatModel", "")
		self.coatModel = sCoatModel if sCoatModel else eCoatModel
		
	def clearCoatModel( self, key ):
		"""
		"""
		if key in self.appearance:
			msCoatModel = self.appearance.pop( key )
			if self.coatModel == msCoatModel:
				sCoatModel = self.appearance.get("sCoatModel", "")
				eCoatModel = self.appearance.get("eCoatModel", "")
				self.coatModel = sCoatModel if sCoatModel else eCoatModel

	def setHairModel(self, key, value):
		"""
		换发型
		key:
		sHairModel(商城外观发型)> eHairModel(模型发型)
		"""
		self.appearance.update({key:value})
		if self.hairModel == value:
			return
		sHairModel = self.appearance.get("sHairModel", "")
		eHairModel = self.appearance.get("eHairModel", "")
		self.hairModel = sHairModel if sHairModel else eHairModel

	def setHeadAdornModel(self, key, value):
		"""
		换头饰
		key:
		sHeadAdornModel(商城外观头饰)> eHeadAdornModel(装备头饰)
		"""
		self.appearance.update({key:value})
		if self.headAdornModel == value:
			return
		sHeadAdornModel = self.appearance.get("sHeadAdornModel", "")
		eHeadAdornModel = self.appearance.get("eHeadAdornModel", "")
		self.headAdornModel = sHeadAdornModel if sHeadAdornModel else eHeadAdornModel

	def setFaceAdornModel(self, key, value):
		"""
		换面饰
		key:
		sFaceAdornModel(商城外观面饰)> eFaceAdornModel(装备面饰)
		"""
		self.appearance.update({key:value})
		if self.faceAdornModel == value:
			return
		sFaceAdornModel = self.appearance.get("sFaceAdornModel", "")
		eFaceAdornModel = self.appearance.get("eFaceAdornModel", "")
		self.faceAdornModel = sFaceAdornModel if sFaceAdornModel else eFaceAdornModel

	def setBackAdornModel(self, key, value, itemID):
		"""
		换背饰
		key:
		sBackAdornModel(商城外观背饰)> eBackAdornModel(装备背饰)
		"""
		self.appearance.update({key:value})
		if self.backAdornModel == value:
			return
		sBackAdornModel = self.appearance.get("sBackAdornModel", "")
		eBackAdornModel = self.appearance.get("eBackAdornModel", "")
		self.backAdornModel = sBackAdornModel if sBackAdornModel else eBackAdornModel

		backAdornParam = ""
		if str(itemID) in self.storeBackAdornParam:
			backAdornParam = self.storeBackAdornParam[str(itemID)]
		self.backAdornParam = backAdornParam

	def setWaistAdornModel(self, key, value):
		"""
		换腰饰
		key:
		sWaistAdornModel(商城外观腰饰)> eWaistAdornModel(装备腰饰)
		"""
		self.appearance.update({key:value})
		if self.waistAdornModel == value:
			return
		sWaistAdornModel = self.appearance.get("sWaistAdornModel", "")
		eWaistAdornModel = self.appearance.get("eWaistAdornModel", "")
		self.waistAdornModel = sWaistAdornModel if sWaistAdornModel else eWaistAdornModel

	def setCloakModel(self, key, value):
		"""
		换披风
		key:
		sCloakModel(商城外观披风)> eCloakModel(装备披风)
		"""
		self.appearance.update({key:value})
		if self.cloakModel == value:
			return
		sCloakModel = self.appearance.get("sCloakModel", "")
		eCloakModel = self.appearance.get("eCloakModel", "")
		self.cloakModel = sCloakModel if sCloakModel else eCloakModel

	def setCarrierId(self, key, value):
		"""
		换坐骑
		key:
		sCarrierId(商城坐骑ID)> eCarrierId(幻兽原本坐骑ID)
		"""
		self.appearance.update({key:value})
		if self.carrierId == value:
			return
		sCarrierId = self.appearance.get("sCarrierId", "")
		eCarrierId = self.appearance.get("eCarrierId", "")
		self.carrierId = sCarrierId if sCarrierId else eCarrierId
		
	def setModelChangeColor( self, colorScheme ):
		"""
		改变模型颜色
		(因为bodyModel 会保存到数据库，所以保险起见用另一个数据保存到数据库。)
		角色的变色方案（1：为美术版本，2：为程序版本）
		"""
		oldColorScheme = self.colorScheme
		self.colorScheme = colorScheme
		if colorScheme == csdefine.MODEL_COLOR_SCHEME_MS:
			self.coatModelTemp = self.coatModel
			tempCamp = self.getFinalCamp()
			gender = self.getGender()
			profession = self.getProfession()
			if tempCamp in Const.COLOR_SCHEME_MODEL_COLOR and gender in Const.COLOR_SCHEME_MODEL_COLOR[tempCamp] and \
			profession in Const.COLOR_SCHEME_MODEL_COLOR[tempCamp][gender]:
				modelID = Const.COLOR_SCHEME_MODEL_COLOR[tempCamp][gender][profession]
				self.coatModel = modelID
				
		if oldColorScheme == csdefine.MODEL_COLOR_SCHEME_MS and self.coatModelTemp:
			self.coatModel = self.coatModelTemp
			