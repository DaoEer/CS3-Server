# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#cell
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
#common
import csstatus
import csdefine
import ItemFactory
import KBEDebug

VALUE_TYPE_REASON = {
	csdefine.REWARD_TYPE_MONEY: csdefine.MONEY_ADD_REASON_SKILL,  # 金币奖励
	csdefine.REWARD_TYPE_EXP: csdefine.EXP_ADD_REASON_SKILL,  # 经验奖励
	csdefine.REWARD_TYPE_XIUWEI: csdefine.XIUWEI_ADD_REASON_BY_SKILL,  # 修为奖励
	csdefine.REWARD_TYPE_POTENTIAL: csdefine.POTENTIAL_ADD_REASON_SKILL,  # 潜能奖励
	csdefine.REWARD_TYPE_BANGGONG: csdefine.POTENTIAL_ADD_REASON_SKILL,  # 帮贡奖励
	csdefine.REWARD_TYPE_TONG_MONEY: csdefine.POTENTIAL_ADD_REASON_SKILL,  # 帮会资金奖励
	csdefine.REWARD_TYPE_FEATS: csdefine.FEATS_ADD_REASON_SKILL,  # 功勋奖励
	csdefine.REWARD_TYPE_MORALE: csdefine.POTENTIAL_ADD_REASON_SKILL,  # 气运奖励
	csdefine.REWARD_TYPE_PSIONIC: csdefine.POTENTIAL_ADD_REASON_SKILL,  # 灵能奖励
	csdefine.REWARD_TYPE_BINDMONEY: csdefine.POTENTIAL_ADD_REASON_SKILL,# 绑金奖励
	csdefine.REWARD_TYPE_LINGSHI : csdefine.POTENTIAL_ADD_REASON_SKILL, # 灵石奖励
	csdefine.REWARD_TYPE_XUANSHI : csdefine.POTENTIAL_ADD_REASON_SKILL, # 玄石奖励
	csdefine.REWARD_TYPE_XIANSHI : csdefine.POTENTIAL_ADD_REASON_SKILL, # 仙石奖励
}

class EffectReward( EffectSkillBase ):
	"""
	“给予奖励”效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._rewardID = ""
		self.param2Dict = {}
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		self._rewardID = dictDat["Param1"].strip()
		if dictDat["Param2"]:
			for i in dictDat["Param2"].split("|"):
				key, value = i.split(":")
				self.param2Dict[key.strip()] = eval(value)

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		param = {"player": caster}
		param.update(self.param2Dict)
		rewardDatas = RewardMgr.g_rewardMgr.getReward(self._rewardID, param)
		for data in rewardDatas:
			type = data["type"]
			if type == csdefine.REWARD_TYPE_NOTHING:
				continue
			elif type == csdefine.REWARD_TYPE_ITEM:
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(data["goodsid"], data["amount"])
				if not itemInst:
					receiver.statusMessage(csstatus.GM_ITEMID_DONT_EXIST, "")
					return

				reason = receiver.addItem(itemInst, csdefine.ITEM_ADD_BY_SKILL)
				if reason != csstatus.ITEM_GO_ON:
					receiver.statusMessage(reason, "")
			elif type == csdefine.REWARD_TYPE_TITLE:  # 增加称号选项
				RewardMgr.g_rewardMgr.doReward(data, receiver.id, "title")
			else:
				RewardMgr.g_rewardMgr.doReward(data, receiver.id, VALUE_TYPE_REASON[data["type"]])


