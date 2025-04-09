# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import json
import csstatus
import Singleton
from LoadModule import *

from ConfigObject.Chat.ChatBase.ChatMgr import g_chatMgr
from ConfigObject.Talk.TalkBase import NPCTalkLoader
from ConfigObject.Quest.QuestBase import QuestLoader
from ConfigObject.Drop.DropBase import DropMgr
from ConfigObject.Drop.DropBase.DropBoxConfigLoader import g_dropBoxConfigLoader
from ConfigObject.Reward.RewardBase import RewardMgr
from ConfigObject.SpaceEvent.SpaceEventActionsLoader import g_SEActionsLoader
from ConfigObject.SpaceEvent.SpaceEventConditionsLoader import g_SEConditionsLoader
from ConfigObject.Trade.TradeMgr import g_tradeMgr
from ConfigObject.Skill.EffectLoader import g_effects
from ConfigObject.Skill.SkillLoader import g_skills
from ConfigObject.Skill.BuffLoader import g_buffs
from ConfigObject.Skill.SkillPostureLoader import g_skillPosture
from ConfigObject.StoryEvent.StoryEventLoader import g_storyEventLoader
from XiuweiLoader import g_XiuweiMgr
from ExploitLoader import g_exploitMgr
from FactionRelationLoader import g_FactionRelationLoader
from ConfigObject.NavmeshLoader import g_navmeshLoader
from ConfigObject.SpaceEntityRelation.SpaceEntityRelationLoader import g_spaceEntityRelationLoader
from ConfigObject.BunchChildStrategy.StrategyLoader import g_bunchChildStrategyLoader
from PetSkillLearnLoader import g_PetSkillLearn
from TitleLoader import g_titleLoader
from TitleLoader import g_titleRewardLoader
import ActivityBunchModule
from ConfigObject.ReviveCost.ReviveCostLoader import g_reviveCostLoader
from ConfigObject.SpaceCopyYXLMMonsterDataLoader import g_spaceCopyYXLMMonsterDataLoader
from ConfigObject.SpaceEffect.SpaceEffectLoader import g_spaceEffectLoader
from CampMoraleConfigLoader import g_campMoraleConfig
from ConfigObject.MonsterJumpPointLoader import g_MonsterJumpPoint
from ConfigObject.MonsterClientAIDataLoader import g_monsterClientAIDataLoader
from ConfigObject.SystemSwitch.SystemSwitchLoader import g_systemSwitchLoader
from ConfigObject.SpaceCopyNPCFuDaiDataLoader import g_SpaceCopyNPCFuDaiData
from ConfigObject.ShenTongSkillLoader import g_ShenTongSkillLoader
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
from ConfigObject.ActivityReward.ActivityRewardMgr import g_activityRewardMgr
from ConfigObject.SpaceCopyLLBZNoticeLoader import g_SpaceCopyLLBZNotice
from ConfigObject.SpaceCopyLLBZRewardsLoader import g_SpaceCopyLLBZRewards
from ConfigObject.Skill.PassiveSkillBarLoader import g_passiveSkillBars
from ConfigObject.MonsterEscapePointLoader import g_MonsterEscapePoint
from ConfigObject.Barracks.BarracksMgr import g_barracksMgr
from ConfigObject.SpaceCopyTTDRewardsLoader import g_SpaceCopyTTDRewards
from ConfigObject.BuildDepleteLoader import g_BuildDepleteLoader
from ConfigObject.LingQuanProduceLoader import g_LingQuanProduceLoader
from ConfigObject.SpaceCopyTTDRewardRatioLoader import g_SpaceCopyTTDRewardRatioLoader
from ConfigObject.SpaceCopyQianNengLoopRewardLoader import g_SpaceCopyQianNengRewardsLoader
from ConfigObject.JiYuanCfgLoader import g_jiYuanCfgLoader
from ConfigObject.ChuanChengSkillLoader import g_ChuanChengSkillLoader
from ConfigObject.TongRewardLoader import g_TongRewardLoader
from ConfigObject.BHZBPointDataLoader import g_BHZBPointDataLoader
from ConfigObject.TongSpaceCopyRewardLoader import g_TongSpaceCopyRewardLoader

class ConfigLoader( Singleton.Singleton ):
	"""
	游戏对象script工厂类
	"""
	def __init__( self ):
		"""
		要初始化的配置放在这行进行加载
		"""
		g_chatMgr.init( openJsonCfg("Chat/ChatChannelConfig.json"), openJsonCfg("Chat/ChatPageConfig.json") )	
		QuestLoader.g_QuestLoader.loadConfig(openJsonPathConfig("Quest"))
		QuestLoader.g_QuestLoader.loadLoopQuestConfig(openJsonCfg("Quest/QuestConfigs/LoopQuest.json"))
		QuestLoader.g_QuestLoader.loadDailyQuestConfig(openJsonCfg("Quest/QuestConfigs/TongDailyQuest.json"))
		g_SEActionsLoader.init()
		g_SEConditionsLoader.init()
		DropMgr.g_dropMgr.init()
		g_dropBoxConfigLoader.init(openJsonCfg("DropBox/DropBox.json"))
		RewardMgr.g_rewardMgr.init()
		g_tradeMgr.init( openJsonCfg("ShopData/NPCShopData.json"), openJsonCfg("ShopData/NPCRandomLimitShopData.json"), openJsonCfg("Skill/SkillConfigs/skillLearnConfig.json"),openJsonCfg("Skill/SkillConfigs/passiveSkillLearnConfig.json"),\
				openJsonCfg("ShopData/ShopType/ShopTypeCfg.json"), openJsonCfg("ShopData/MysteriousCfg.json"), openJsonCfg("ShopData/MysteriousMerchantCfg.json"), openJsonCfg("ShopData/TongPlunderShopData.json") )
		g_storyEventLoader.init()
		g_XiuweiMgr.init( openJsonCfg("Xiuwei/RoleXiuweiCfg.json"), openJsonCfg( "Xiuwei/MonsterXiuweiCfg.json" ), openJsonCfg("Xiuwei/RoleJingjieCfg.json") )
		g_exploitMgr.init( openJsonCfg("MilitaryRank/MilitaryRankCfg.json") )
		g_FactionRelationLoader.init( openJsonCfg("FactionRelationCfg.json") )
		g_navmeshLoader.init()
		g_spaceEntityRelationLoader.init()
		g_bunchChildStrategyLoader.init()
		g_PetSkillLearn.loadConfig()
		ActivityBunchModule.loadAllBunch()
		g_reviveCostLoader.init()
		g_spaceCopyYXLMMonsterDataLoader.init( openJsonCfg("SpaceCopyYXLMMonsterData.json") )
		g_spaceEffectLoader.init(openJsonCfg("SpaceDynamicEffectCfg.json"))
		g_campMoraleConfig.loadConfig()
		g_MonsterJumpPoint.loadConfig()
		g_monsterClientAIDataLoader.init( openJsonCfg("MonsterClientAIData.json") )
		g_systemSwitchLoader.init(openJsonCfg("SystemSwitchCfg.json"))
		g_SpaceCopyNPCFuDaiData.loadConfig()
		g_ShenTongSkillLoader.loadConfig()
		g_mailContentDataLoader.init( openJsonCfg("Reward/MailContentData.json") )
		g_activityRewardMgr.init( openJsonCfg("Reward/ActivityRewardData.json") )
		g_SpaceCopyLLBZNotice.loadConfig()
		g_SpaceCopyLLBZRewards.loadConfig()
		g_MonsterEscapePoint.loadConfig()
		g_SpaceCopyTTDRewards.loadConfig()
		g_BuildDepleteLoader.loadConfig()
		g_LingQuanProduceLoader.loadConfig()
		g_SpaceCopyTTDRewardRatioLoader.loadConfig()
		g_barracksMgr.init()
		g_SpaceCopyQianNengRewardsLoader.loadConfig()
		g_jiYuanCfgLoader.loadConfig("JiYuanCfg.json")
		g_ChuanChengSkillLoader.loadConfig()
		g_TongRewardLoader.loadConfig("BHReward.json")
		g_BHZBPointDataLoader.init()
		g_TongSpaceCopyRewardLoader.loadConfig("TongSpaceCopyReward.json")
	
	def reloadConfig( self ):
		"""
		配置支持热更新
		"""
		chatChnelCfig = openJsonCfg("Chat/ChatChannelConfig.json")
		if not chatChnelCfig:
			return "Chat/ChatChannelConfig.json"
		chatPageCfig = openJsonCfg("Chat/ChatPageConfig.json")
		if not chatPageCfig:
			return "Chat/ChatPageConfig.json"
		g_chatMgr.init( chatChnelCfig, chatPageCfig )
			
		try:
			g_SEActionsLoader.reloadConfig()
		except:
			return "SpaceEvent.SpaceEventActions.py"
			
		try:
			g_SEConditionsLoader.reloadConfig()
		except:
			return "SpaceEvent.SpaceEventConditions.py"
		
		try:
			DropMgr.g_dropMgr.reloadConfig()
		except:
			return "GameObject/Monster.json"
			
		dropBoxCfig = openJsonCfg("DropBox/DropBox.json")
		if not dropBoxCfig:
			return "DropBox/DropBox.json"
		g_dropBoxConfigLoader.init(dropBoxCfig)
			
		try:
			RewardMgr.g_rewardMgr.reloadConfig()
		except:
			return "Reward.RewardData.py or Reward.RewardNormalData.py"
			
		shopData = openJsonCfg("ShopData/NPCShopData.json")
		randomLimitShopData = openJsonCfg("ShopData/NPCRandomLimitShopData.json")
		skillLearn = openJsonCfg("Skill/SkillConfigs/skillLearnConfig.json")
		passiveSkillLearn = openJsonCfg("Skill/SkillConfigs/passiveSkillLearnConfig.json")
		shopType = openJsonCfg("ShopData/ShopType/ShopTypeCfg.json")
		mysteriousCfg = openJsonCfg("ShopData/MysteriousCfg.json")
		mysteriousMerchantCfg = openJsonCfg("ShopData/MysteriousMerchantCfg.json")
		tongPlunderShopCfg = openJsonCfg("ShopData/TongPlunderShopData.json")
		if shopData is None:return "ShopData/NPCShopData.json"
		if randomLimitShopData is None: return "ShopData/NPCRandomLimitShopData.json"
		if not skillLearn:return "Skill/SkillConfigs/skillLearnConfig.json"
		if not passiveSkillLearn:return "Skill/SkillConfigs/passiveSkillLearnConfig.json"
		if not shopType:return "ShopData/ShopType/ShopTypeCfg.json"
		if mysteriousCfg is None: return "ShopData/MysteriousCfg.json"
		if mysteriousMerchantCfg is None: return "ShopData/MysteriousMerchantCfg.json"
		if tongPlunderShopCfg is None: return "ShopData/TongPlunderShopData.json"
		g_tradeMgr.init( shopData,randomLimitShopData, skillLearn, passiveSkillLearn, shopType, mysteriousCfg, mysteriousMerchantCfg, tongPlunderShopCfg)
			
		try:
			from ObjectScript.ObjectScriptFactory import g_objFactory
			g_objFactory.reloadConfig()
		except:
			return "Monster or NPC or SpellBox or Trap"
			
		if not g_effects.reloadConfig():
			return "Skill/SkillConfigs/SkillEffectTable.json"

		if not g_skills.reloadConfig():
			return "Skill/SkillConfigs/SkillTable.json"
		
		if not g_buffs.reloadConfig():
			return "Skill/SkillConfigs/BuffTable.json"

		if not g_skillPosture.reloadConfig():
			return "Skill/SkillConfigs/SkillPostureConfig.json"
		
		try:
			g_storyEventLoader.reloadConfig()
		except:
			return "StoryEventConfig.py"
			
		roleDHCfg = openJsonCfg("Xiuwei/RoleXiuweiCfg.json")
		roleDJCfg = openJsonCfg("Xiuwei/RoleJingjieCfg.json")
		monsterDHCfg = openJsonCfg( "Xiuwei/MonsterXiuweiCfg.json" )
		if not roleDHCfg:return "Xiuwei/RoleXiuweiCfg.json"
		if not roleDJCfg:return "Xiuwei/RoleJingjieCfg.json"
		if not monsterDHCfg:return "Xiuwei/MonsterXiuweiCfg.json"
		
		g_XiuweiMgr.init( roleDHCfg, monsterDHCfg, roleDJCfg )
			
		try:
			g_FactionRelationLoader.init( openJsonCfg("FactionRelationCfg.json") )
		except:
			return "FactionRelationCfg.json"
		
		try:
			g_navmeshLoader.reloadConfig()
		except:
			return "ConfigObject.NavmeshLoader.py"
		
		try:
			g_bunchChildStrategyLoader.reloadConfig()
		except:
			return "BunchChildStrategyCfg.json"

		try:
			g_titleRewardLoader.reloadConfig()
		except:
			return "TitleData/titleRewardData.py"
		
		try:
			g_titleLoader.reloadConfig()
		except:
			return "TitleData/titleData.json"
		try:
			g_reviveCostLoader.reloadConfig()
		except:
			return "ConfigObject.ReviveCost.ReviveCostLoader"

		try:
			g_spaceCopyYXLMMonsterDataLoader.init( openJsonCfg("SpaceCopyYXLMMonsterData.json") )
		except:
			return "SpaceCopyYXLMMonsterData.json"

		try:
			g_spaceEffectLoader.reloadConfig()
		except:
			return "SpaceDynamicEffectCfg.json"

		try:
			g_campMoraleConfig.reloadConfig()
		except:
			return "CampMoraleReward.json"
			
		try:
			g_MonsterJumpPoint.reloadConfig()
		except:
			return "MonsterJumpPointCfg.json"

		try:
			g_monsterClientAIDataLoader.init( openJsonCfg("MonsterClientAIData.json") )
		except:
			return "MonsterClientAIData.json"

		try:
			g_systemSwitchLoader.reloadConfig()
		except:
			return "SystemSwitchCfg.json"

		try:
			g_SpaceCopyNPCFuDaiData.reloadConfig()
		except:
			return "SpaceCopyNPCFuDaiData.json"

		try:
			g_ShenTongSkillLoader.reloadConfig()
		except:
			return "ShenTong.ShenTongSkillComminution.json"

		try:
			g_mailContentDataLoader.init( openJsonCfg("Reward/MailContentData.json") )
		except:
			return "MailContentData.json"

		try:
			g_activityRewardMgr.init( openJsonCfg("Reward/ActivityRewardData.json") )
		except:
			return "ActivityRewardData.json"
			
		try:
			g_SpaceCopyLLBZNotice.reloadConfig()
		except:
			return "SpaceCopyLLBZNotice.json"

		try:
			g_SpaceCopyLLBZRewards.reloadConfig()
		except:
			return "SpaceCopyLLBZRewards.json"
		
		try:
			g_passiveSkillBars.reloadConfig()
		except:
			return "PassiveSkillBarData.json"

		try:
			g_MonsterEscapePoint.reloadConfig()
		except:
			return "MonsterEscapePointCfg.py"

		try:
			g_barracksMgr.init()
		except:
			return "BarracksData.json"

		try:
			g_SpaceCopyTTDRewards.reloadConfig()
		except:
			return "SpaceCopyTTDRewards.json"

		try:
			g_BuildDepleteLoader.reloadConfig()
		except:
			return "BuildDepleteCfg.json"

		try:
			g_LingQuanProduceLoader.reloadConfig()
		except:
			return "LingQuanProduceCfg.json"

		try:
			g_SpaceCopyTTDRewardRatioLoader.reloadConfig()
		except:
			return "SpaceCopyTTDRewardRatio.json"
			
		try:
			g_SpaceCopyQianNengRewardsLoader.reloadConfig()
		except:
			return "QianNengSpaceLoopReward.json"
			
		try:
			g_jiYuanCfgLoader.reloadConfig("JiYuanCfg.json")
		except:
			return "JiYuanCfg.json"
			
		try:
			g_PetSkillLearn.reloadConfig()
		except:
			return "PetSkillLearnLoader.json"

		try:
			g_ChuanChengSkillLoader.reloadConfig()
		except:
			return "ChuanChengSkillLoader.json"
			
		try:
			g_TongRewardLoader.reloadConfig("BHReward.json")
		except:
			return "BHReward.json"
		try:
			g_BHZBPointDataLoader.init()
		except:
			return "BHZBPointCfg.json"
			
		try:
			g_TongSpaceCopyRewardLoader.reloadConfig("TongSpaceCopyReward.json")
		except:
			return "TongSpaceCopyReward.json"
			
		return 1

#-------global instance--------------------------------------------------
g_configLoader = ConfigLoader()