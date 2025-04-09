# -*- coding: utf-8 -*-

import KBEngine
import Singleton
from LoadModule import *
from ConfigObject.Shop.ShopMgr import g_shopMgr
from ConfigObject.ShopMall.ShopMallMgr import g_shopMallMgr
from ConfigObject.Coupon.CouponMgr import g_couponMgr
from ConfigObject.Reward.OnlineRewardMgr import g_onlineRewardMgr
from ConfigObject.Store.StoreMgr import g_storeMgr
from ConfigObject.Reward.ActivityRewardMgr import g_activityRewardMgr
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
from ConfigObject.BHZBPointDataLoader import g_BHZBPointDataLoader
from ConfigObject.LbcConfigLoader import g_lbcConfigData
from ConfigObject.AuctionCfgLoader import g_AuctionCfgLoader

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()


class ConfigLoader( Singleton.Singleton ):
	"""
	游戏对象script工厂类
	"""
	def __init__( self ):
		"""
		要初始化的配置放在这行进行加载
		"""
		g_shopMgr.init( openJsonCfg("ShopData/NPCShopData.json"), openJsonCfg("ShopData/NPCRandomLimitShopData.json"), openJsonCfg("ShopData/ShopType/ShopTypeCfg.json") )
		g_shopMallMgr.init( openJsonCfg("ShopMallData/ShopMallData.json"))
		g_couponMgr.init( openJsonCfg("CouponData/CouponData.json"))
		g_onlineRewardMgr.init()
		g_storeMgr.init()
		g_activityRewardMgr.init( openJsonCfg("Reward/ActivityRewardData.json") )
		g_mailContentDataLoader.init( openJsonCfg("Reward/MailContentData.json") )
		g_BHZBPointDataLoader.init()
		g_lbcConfigData.init(openJsonCfg("LbcConfig.json"))
		g_AuctionCfgLoader.init(openJsonCfg("AuctionCfg.json"))
		g_CrondDatas.load("Crond/Crond.json", "Crond/CrondData.json")

	def reloadConfig( self ):
		g_shopMgr.init( openJsonCfg("ShopData/NPCShopData.json"), openJsonCfg("ShopData/NPCRandomLimitShopData.json"), openJsonCfg("ShopData/ShopType/ShopTypeCfg.json"))
		KBEngine.globalData["ShopManager"].reload()
		g_shopMallMgr.init( openJsonCfg("ShopMallData/ShopMallData.json"))
		g_couponMgr.init( openJsonCfg("CouponData/CouponData.json"))
		g_onlineRewardMgr.init()
		g_storeMgr.init()
		g_activityRewardMgr.init( openJsonCfg("Reward/ActivityRewardData.json") )
		g_mailContentDataLoader.init( openJsonCfg("Reward/MailContentData.json") )
		g_BHZBPointDataLoader.init()
		g_lbcConfigData.init(openJsonCfg("LbcConfig.json"))
		g_AuctionCfgLoader.init(openJsonCfg("AuctionCfg.json"))
		g_CrondDatas.load("Crond/Crond.json", "Crond/CrondData.json")

#-------global instance--------------------------------------------------
g_configLoader = ConfigLoader()