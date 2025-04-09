# -*- coding: utf-8 -*-

import Math
import time
import Const
import Define
import csdefine
import csstatus
import KBEngine
import KBEMath
import csconst
import Functions
from KBEDebug import *
from ObjectScript.Space.SpaceBase import SpaceBase

import ItemFactory
from ConfigObject.Drop import DropItem
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from ConfigObject.TongRewardLoader import g_TongRewardLoader


class SpaceTong( SpaceBase ):
	def __init__( self ):
		SpaceBase.__init__( self )
		self.nagualPosition = (0.0, 0.0, 0.0)
		self.nagualDirection = (0.0, 0.0, 0.0)

	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		spaceData = configData["SpaceData"]
		nagualPosition = Functions.vector3TypeConvert(spaceData["nagualPosition"])
		if nagualPosition:
			self.nagualPosition = KBEMath.Unreal2KBEnginePosition(nagualPosition)
		nagualDirection = Functions.vector3TypeConvert(spaceData["nagualDirection"])
		if nagualPosition:
			self.nagualDirection = KBEMath.Unreal2KBEnginePosition(nagualDirection)
			
	def createTongDropBox(self, selfEntity, tongDBID, allocation, memberDBIDs, rewardKey, level):
		"""
		"""
		config = g_TongRewardLoader.getConfigByKey(rewardKey)
		if config is None: 
			return
		
		#没有人话，也就没必要创建没人捡
		if len(memberDBIDs) <= 0:
			ERROR_MSG("createTongDropBox error, no role %s, %s" %(tongDBID, rewardKey))
			return
		
		items = {}
		for rewardID in config["reward"]:
			rewardItemDatas = []
			def calcRewardDatas(rewardDatas):
				for data in rewardDatas:
					type = data["type"]
					amount = data["amount"]
					goodsid = data["goodsid"]
					# 物品奖励
					if type == csdefine.REWARD_TYPE_ITEM:
						rewardItemDatas.append( data )
			
			rewardDatas = RewardMgr.g_rewardMgr.getReward(rewardID, {"tongLevel" : level})
			calcRewardDatas( rewardDatas )
			for data in rewardItemDatas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
				items[itemInst.uid] = itemInst
				
		if len(items) <= 0:
			ERROR_MSG("create TongDropBox error, item is None [%s -- %s -- %s]" %(rewardKey, tongDBID, level))
			return
		
		#GM创建的话，创建在玩家周边
		position = config["position"]
		if KBEngine.cellAppData.get("TONGDROPBOXPOS", None):
			position = KBEngine.cellAppData["TONGDROPBOXPOS"]
			del KBEngine.cellAppData["TONGDROPBOXPOS"]
		
		args = {
			"notAllocationItems"	: items,
			"freeAllocationItems"	: {},
			"tongDBID"				: tongDBID,
			"allocation"			: allocation,
			"joinDBIDs"				: memberDBIDs,
			"openBoxTime"			: Const.TONG_DROPBOX_OPEN_TIME,
			"modelScale"			: config["modelScale"],
			"modelNumber"			: config["modelNumber"],	
		}
		dropbox = selfEntity.createEntityNear("TongDropBox", position, config["direction"], args)
		if dropbox is None:
			ERROR_MSG("Create Tong DropBox Fail %s, %s, %s" %(tongDBID, memberDBIDs, rewardKey))
			return