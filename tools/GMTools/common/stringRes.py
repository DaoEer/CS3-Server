# -*- coding: utf-8 -*-
import collections

from . import LogDefine
from . import csdefine
from . import ItemTypeEnum
from . import tooldefine

#-------------------------------------------------------------------
#日志类型
#-------------------------------------------------------------------
LOG_TYPE_DICT_1 = {
	LogDefine.LOG_TYPE_QUEST: "任务",
	LogDefine.LOG_TYPE_ITEM: "物品",
	LogDefine.LOG_TYPE_COIN: "货币",
	LogDefine.LOG_TYPE_PRO: "属性",
	LogDefine.LOG_TYPE_EQUIP: "装备",
	LogDefine.LOG_TYPE_RELATION: "人物关系",
	LogDefine.LOG_TYPE_PET: "宠物",
	LogDefine.LOG_TYPE_TRADE: "交易",
	LogDefine.LOG_TYPE_MAIL: "邮件",
	LogDefine.LOG_TYPE_TONG: "帮会",
	LogDefine.LOG_TYPE_SKILL: "技能",
	LogDefine.LOG_TYPE_RECHARGE: "充值",
	LogDefine.LOG_TYPE_ACCOUNT: "账号",
	LogDefine.LOG_TYPE_ROLE: "角色",
	LogDefine.LOG_TYPE_VEND: "摆摊",
}

LOG_TYPE_DICT_2 = {}

#-------------------------------------------------------------------
#地图名称
#-------------------------------------------------------------------
SPACE_CH_DICT = {
	"L_JSC": "太虚洞天",
	"L_JSC_Planes101": "下界试炼",
	"L_JSC_Planes102": "营救风橙",
	"L_JSC_Planes103": "救援道场",
	"L_JSC_Planes104": "坐忘峰之战",
	"L_JSC_Planes105": "追击玄机子",
	"fu_ben_zhuangyuan2_1": "测试区域一",
	"fu_ben_zhuangyuan2_2": "测试区域二",
	"fu_ben_zhuangyuan2_3": "测试区域三",
	"L_HLD": "火灵岛",
	"L_BJG": "逍遥门",
	"L_YSC": "盘古洞天",
	"L_YSC_Planes001": "下界试炼",
	"L_YSC_Planes002": "营救抱朴子",
	"L_YSC_Planes003": "太寅道场",
	"L_YSC_Planes004": "试剑台之战",
	"L_YSC_Planes005": "魔道秘密道场",
	"L_YXG": "玉虚宫",
	"L_DJD": "东极岛",
	"L_TSHJ": "天书幻境",
	"L_TXHJ": "太虚幻境",
	"L_YeWai_Planes301": "上古秘境",
	"L_XLD": "修罗殿",
	"L_XYM": "逍遥门",
	"L_TQG": "太清宫",
	"L_FMC": "凤鸣城",
	"L_KWSM_Planes001": "玄蜂沼泽",
	"L_KWSM_Planes002": "赤猿道场",
	"L_KWSM_Planes003": "鬼雉妖窟",
	"L_FMNL_Planes001": "望月坡",
	"L_FMNL_Planes002": "望月窟",
	"L_FMNL_Planes003": "千妖万魔林",
}

#-------------------------------------------------------------------
#金钱类型
#-------------------------------------------------------------------
MONEY_CH_DICT = {
	csdefine.COIN_TYPE_GOLD: "金元宝",
	csdefine.COIN_TYPE_SILVER: "银元宝",
	csdefine.COIN_TYPE_MONEY: "金币",
}

#-------------------------------------------------------------------
#货币类型及变更原因
#-------------------------------------------------------------------
COIN_CH_DICT = {
	LogDefine.LT_MONEY_CHANGE:"金钱",
	LogDefine.LT_XIANSHI_CHANGE: "仙石",
	LogDefine.LT_LINGSHI_CHANGE: "灵石",
	LogDefine.LT_XUANSHI_CHANGE: "玄石",
	LogDefine.LT_BINDMONEY_CHANGE: "绑金",
}

COIN_XIANSHI_CHANGE_CH_DICT={
	csdefine.CHANGE_XIANSHI_NORMAL: "默认方式",
	csdefine.CHANGE_XIANSHI_UNLOCKBAGGRID: "解锁背包格",
	csdefine.CHANGE_XIANSHI_PETCAGES:"解锁幻兽格子",
	csdefine.CHANGE_XIANSHI_INTENSIFY_SAVESLOT: "解锁强化保存栏位",
	csdefine.CHANGE_XIANSHI_GM_SET: "GM指令设置",
	csdefine.CHANGE_XIANSHI_AUGMENT_SIGNIN: "补签消耗",
	csdefine.CHANGE_XIANSHI_COMPOSE_EQUIP: "装备打造消耗",
	csdefine.CHANGE_XIANSHI_CHARGE: "充值兑换",
	csdefine.CHANGE_XIANSHI_RECAST_EQUIP: "使用元宝重铸",
	csdefine.CHANGE_XIANSHI_RESET_EQUIP: "使用元宝洗练",
	csdefine.CHANGE_XIANSHI_BY_MAILL: "邮件",
	csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME: "商城消费",
	csdefine.CHANGE_XIANSHI_BY_TRADE: "灵石寄售",
	csdefine.CHANGE_XIANSHI_BY_INTENSIFY_EQUIP: "装备强化",
	csdefine.CHANGE_XIANSHI_BY_RESET_EQUIP: "装备回火",
	csdefine.CHANGE_XIANSHI_BY_SAVE_INTENSIFY_EQUIP: "装备备份",
	csdefine.CHANGE_XIANSHI_BY_RESET_INTENSIFY_EQUIP: "装备还原",
	csdefine.CHANGE_XIANSHI_BY_UNLOCK_PASSIVESKILLBAR: "解锁被动技能",
	csdefine.CHANGE_XIANSHI_PETCOMPOSE: "合成幻兽",
}

COIN_LINGSHI_CHANGE_CH_DICT = {
	csdefine.CHANGE_LINGSHI_BY_STORE: "商城购买",
	csdefine.CHANGE_LINGSHI_BY_MAILL:"邮件",
	csdefine.CHANGE_LINGSHI_BY_SHOP_CONUSUME:"商城消费"
}

COIN_XUANSHI_CHANGE_CH_DICT = {
	csdefine.CHANGE_XUANSHI_CHARGE: "充值兑换",
	csdefine.CHANGE_XUANSHI_GM_SET: "GM指令设置",
	csdefine.CHANGE_XUANSHI_SILVERPRESENT: "领取玄石奖励",
	csdefine.CHANGE_XUANSHI_SHOP_CONUSUME: "商城消费",
	csdefine.CHANGE_XUANSHI_SHOP_REBATE: "商城消费返利",
}

MONEY_ADD_REASON_CH_DICT = {
	csdefine.MONEY_ADD_REASON_DROP_MONSTER: "怪物身上掉落",
	csdefine.MONEY_ADD_REASON_QUEST_REWARD: "任务奖励",
	csdefine.MONEY_ADD_REASON_ROLE_TRADE: "玩家交易",
	csdefine.MONEY_ADD_REASON_SELL_ITEM: "出售物品",
	csdefine.MONEY_ADD_REASON_RETURN_ITEM: "退回物品",
	csdefine.MONEY_ADD_REASON_USE_GIFT_ITEM: "打开礼包",
	csdefine.MONEY_ADD_REASON_FROM_STORE: "从仓库取钱",
	csdefine.MONEY_ADD_REASON_LINGSHI_TRADE: "灵石寄售",
	csdefine.MONEY_ADD_REASON_GM_COMMAND: "GM命令",
	csdefine.MONEY_ADD_REASON_SPACE_SENTLEMENT: "副本结算",
	csdefine.MONEY_ADD_REASON_SPAR_HUN_TING: "晶石狩猎场",
	csdefine.MONEY_ADD_REASON_TONGCONTRI_TO_MONEY: "帮会解散 帮贡转化为钱",
	csdefine.MONEY_ADD_REASON_MAIL: "邮件"
}
MONEY_SUB_REASON_CH_DICT = {
	csdefine.MONEY_SUB_REASON_SPACE_RANDOM: "副本随机减少",
	csdefine.MONEY_SUB_REASON_NPC_TALK: "NPC对话消耗",
	csdefine.MONEY_SUB_REASON_SHOP_BUY: "商店购买物品消费",
	csdefine.MONEY_SUB_REASON_EQUIP_REPAIR: "装备修理消耗",
	csdefine.MONEY_SUB_REASON_UNLOCK_GRID: "解锁背包格",
	csdefine.MONEY_SUB_REASON_LINGSHI_TRADE: "灵石寄售",
	csdefine.MONEY_SUB_REASON_PAY_FOR_MAIL_BILL: "邮件资费",
	csdefine.MONEY_SUB_REASON_COMPOSE_PET: "合成幻兽",
	csdefine.MONEY_SUB_REASON_REPLACE_PET_SKILL: "替换幻兽技能",
	csdefine.MONEY_SUB_REASON_UPGRADE_PET_SKILL: "升级幻兽技能",
	csdefine.MONEY_SUB_REASON_ACTIVATE_CAGE: "激活幻兽笼子",
	csdefine.MONEY_SUB_REASON_ADD_ENTTIME: "添加有效聊天时间",
	csdefine.MONEY_SUB_REASON_ROLE_REVIVE: "玩家复活",
	csdefine.MONEY_SUB_REASON_COMMONUTION_SKILL: "精研技能",
	csdefine.MONEY_SUB_REASON_TELEPORT: "玩家传送消耗",
	csdefine.MONEY_SUB_REASON_TONG_DONATE: "帮会捐献",
	csdefine.MONEY_SUB_REASON_GM_COMMAND: "GM命令",
	csdefine.MONEY_SUB_REASON_ROLE_TRADE: "玩家交易",
	csdefine.MONEY_SUB_REASON_CREATE_TONG: "创建帮会",
	csdefine.MONEY_SUB_REASON_LEARN_TONG_SKILL: "学习帮会技能",
	csdefine.MONEY_SUB_REASON_INTENSIFY_EQUIP: "装备强化",
	csdefine.MONEY_SUB_REASON_RESET_EQUIP: "装备回火",
	csdefine.MONEY_SUB_REASON_SAVE_INTENSIFY_EQUIP: "装备保存",
	csdefine.MONEY_SUB_REASON_RESET_INTENSIFY_EQUIP: "装备还原",
	csdefine.MONEY_SUB_REASON_SHUFFLE_EQUIP: "装备洗练",
	csdefine.MONEY_SUB_REASON_RECOST_EQUIP: "装备重铸",
	csdefine.MONEY_SUB_REASON_TRANSFER_EQUIP: "装备传星",
	csdefine.MONEY_SUB_REASON_COMPOSE_EQUIP: "打造装备",
	csdefine.MONEY_SUB_REASON_UNLOCK_PASSIVESKILLBAR: "解锁被动技能栏位",
	csdefine.MONEY_SUB_REASON_UPGRADE_SKILL: "升级技能",
	csdefine.MONEY_SUB_REASON_BARRACKS: "玩家兵营",
	csdefine.MONEY_SUB_REASON_COMPOSE_TOOL: "工具打造",
	csdefine.MONEY_SUB_REASON_JADE_UPGRADE: "玲珑玉令升级消耗",
	csdefine.MONEY_SUB_REASON_MELTHING: "淬炼",
	csdefine.MONEY_SUB_REASON_GET_JADE: "获得玲珑玉令",
	csdefine.MONEY_SUB_REASON_REFLASH_LHMJ_SHOP: "轮回秘境商店刷新",
}


COIN_CHANGE_REASON_DICT = {
	LogDefine.LT_MONEY_CHANGE: {
		csdefine.MONEY_CHANGE_TYPE_ADD: MONEY_ADD_REASON_CH_DICT,
		csdefine.MONEY_CHANGE_TYPE_SUB: MONEY_SUB_REASON_CH_DICT,
	},
	LogDefine.LT_XIANSHI_CHANGE: COIN_XIANSHI_CHANGE_CH_DICT,
	LogDefine.LT_LINGSHI_CHANGE: COIN_LINGSHI_CHANGE_CH_DICT,
	LogDefine.LT_XUANSHI_CHANGE: COIN_XUANSHI_CHANGE_CH_DICT,
	LogDefine.LT_BINDMONEY_CHANGE: {
		csdefine.MONEY_CHANGE_TYPE_ADD: MONEY_ADD_REASON_CH_DICT,
		csdefine.MONEY_CHANGE_TYPE_SUB: MONEY_SUB_REASON_CH_DICT,
	},
}

#-------------------------------------------------------------------
#邮件类型
#-------------------------------------------------------------------
MAIL_CH_DICT = {
	csdefine.MAIL_TYPE_READ: "阅读邮件",
	csdefine.MAIL_TYPE_SEND: "发送邮件",
	csdefine.MAIL_TYPE_EXTRACT: "提取邮件",
	csdefine.MAIL_TYPE_DEL: "删除邮件",
}
#-------------------------------------------------------------------
#删除邮件分类
#-------------------------------------------------------------------
MAIL_DEL_CH_DICT = {
	csdefine.LT_MAIL_DEL_TYPE_ACTIVE : "主动删除",
	csdefine.LT_MAIL_DEL_TYPE_TIME_ARRIVE : "时间达到",
	csdefine.LT_MAIL_DEL_TYPE_BEREPLACED : "被其他新邮件顶替"
}

#-------------------------------------------------------------------
#物品品质
#-------------------------------------------------------------------
ITEM_QUALITY_CH_DICT = {
	csdefine.QUALITY_WHITE: "白色",
	csdefine.QUALITY_BLUE: "蓝色",
	csdefine.QUALITY_GOLD: "金色",
	csdefine.QUALITY_PINK: "粉色",
	csdefine.QUALITY_GREEN: "地阶绿色",
	csdefine.QUALITY_GREEN_TIAN: "天阶绿色",
	csdefine.QUALITY_GREEN_SHENG: "圣阶绿色",
}

#-------------------------------------------------------------------
#物品初始化绑定类型定义
#-------------------------------------------------------------------
ITEM_ITEM_SRCBindType_CH_DICT = {
	csdefine.ITEM_SRCBINDTYPE_NONE_BIND:"无绑定",
	csdefine.ITEM_SRCBINDTYPE_PICKUP_BIND:"拾取绑定",
	csdefine.ITEM_SRCBINDTYPE_EQUIP_BIND:"装备绑定",
	csdefine.ITEM_SRCBINDTYPE_IS_BIND:"默认绑定",
}


#-------------------------------------------------------------------
#玩家级别
#-------------------------------------------------------------------
ROLE_DAOHENG_LEVEL_CH_DICT = collections.OrderedDict()
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"1": {
		"playerLevel": 1,
		"daoheng": 6,
		"ch":{
			csdefine.CAMP_TAOSIM: "仙兵",
			csdefine.CAMP_DEMON: "魔兵",
		},
	}
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"2": {
		"playerLevel": 10,
		"daoheng": 1700,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙兵",
			csdefine.CAMP_DEMON: "魔兵",
		}
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"3": {
		"playerLevel": 15,
		"daoheng": 11900,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙兵",
			csdefine.CAMP_DEMON: "魔兵",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"4": {
		"playerLevel": 20,
		"daoheng": 23900,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙师",
			csdefine.CAMP_DEMON: "魔师",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"5": {
		"playerLevel": 25,
		"daoheng": 99100,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙师",
			csdefine.CAMP_DEMON: "魔师",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"6": {
		"playerLevel": 30,
		"daoheng": 284000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙师",
			csdefine.CAMP_DEMON: "魔师",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"7": {
		"playerLevel": 35,
		"daoheng": 918000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙灵",
			csdefine.CAMP_DEMON: "魔灵",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"8": {
		"playerLevel": 40,
		"daoheng": 2858000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙灵",
			csdefine.CAMP_DEMON: "魔灵",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"9": {
		"playerLevel": 45,
		"daoheng": 6159000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙灵",
			csdefine.CAMP_DEMON: "魔灵"
		}
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"10": {
		"playerLevel": 50,
		"daoheng": 11560000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙将",
			csdefine.CAMP_DEMON: "魔将",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"11": {
		"playerLevel": 55,
		"daoheng": 19850000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙将",
			csdefine.CAMP_DEMON: "魔将",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"12": {
		"playerLevel": 60,
		"daoheng": 31250000,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙将",
			csdefine.CAMP_DEMON: "魔将",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"13": {
		"playerLevel": 65,
		"daoheng": 46464779,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙君",
			csdefine.CAMP_DEMON: "魔君",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"14": {
		"playerLevel": 70,
		"daoheng": 66406661,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙君",
			csdefine.CAMP_DEMON: "魔君",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"15": {
		"playerLevel": 75,
		"daoheng": 91510820,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙君",
			csdefine.CAMP_DEMON: "魔君",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"16": {
		"playerLevel": 80,
		"daoheng": 125155460,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙王",
			csdefine.CAMP_DEMON: "魔王",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"17": {
		"playerLevel": 85,
		"daoheng": 163514886,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙王",
			csdefine.CAMP_DEMON: "魔王",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"18": {
		"playerLevel": 90,
		"daoheng": 211635956,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙王",
			csdefine.CAMP_DEMON: "魔王",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"19": {
		"playerLevel": 95,
		"daoheng": 272764076,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙皇",
			csdefine.CAMP_DEMON: "魔皇",
		}
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"20": {
		"playerLevel": 100,
		"daoheng": 342096790,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙皇",
			csdefine.CAMP_DEMON: "魔皇",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"21": {
		"playerLevel": 105,
		"daoheng": 427311747,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙皇",
			csdefine.CAMP_DEMON: "魔皇",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"22": {
		"playerLevel": 110,
		"daoheng": 528105558,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙帝",
			csdefine.CAMP_DEMON: "魔帝",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"23": {
		"playerLevel": 115,
		"daoheng": 644857710,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙帝",
			csdefine.CAMP_DEMON: "魔帝",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"24": {
		"playerLevel": 120,
		"daoheng": 790151872,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙帝",
			csdefine.CAMP_DEMON: "魔帝",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"25": {
		"playerLevel": 125,
		"daoheng": 945589705,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙尊",
			csdefine.CAMP_DEMON: "魔尊"
		}
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"26": {
		"playerLevel": 130,
		"daoheng": 1130485504,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙尊",
			csdefine.CAMP_DEMON: "魔尊",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"27": {
		"playerLevel": 135,
		"daoheng": 1353863247,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙尊",
			csdefine.CAMP_DEMON: "魔尊"
		}
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"28": {
		"playerLevel": 140,
		"daoheng": 1596436194,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙神",
			csdefine.CAMP_DEMON: "魔圣",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"29": {
		"playerLevel": 145,
		"daoheng": 1883286137,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙神",
			csdefine.CAMP_DEMON: "魔圣",
		},
	},
})
ROLE_DAOHENG_LEVEL_CH_DICT.update({
	"30": {
		"playerLevel": 150,
		"daoheng": 2210508805,
		"ch": {
			csdefine.CAMP_TAOSIM: "仙神",
			csdefine.CAMP_DEMON: "魔圣",
		},
	},
})

#-------------------------------------------------------------------
#玩家聊天频道
#-------------------------------------------------------------------
CHAT_TYPE_DICT = {
	csdefine.CHAT_TYPE_NEARBY: "附近",
	csdefine.CHAT_TYPE_SPACE: "地图",
	csdefine.CHAT_TYPE_WORLD: "世界",
	csdefine.CHAT_TYPE_WHISPER: "密语",
	csdefine.CHAT_TYPE_GROUP: "讨论组",
	csdefine.CHAT_TYPE_TEAM: "队伍",
	csdefine.CHAT_TYPE_COLLECTIVE: "团队",
	csdefine.CHAT_TYPE_GANG: "帮会",
	csdefine.CHAT_TYPE_ALIANCE: "联盟",
	csdefine.CHAT_TYPE_SCHOOL: "门派",
	csdefine.CHAT_TYPE_CAMP: "阵营",
	csdefine.CHAT_TYPE_BATTLESPACE: "战场",
	csdefine.CHAT_TYPE_TIANYIN: "天音",
	csdefine.CHAT_TYPE_XIANYIN: "仙音",
	csdefine.CHAT_TYPE_SYSTEM: "系统",
	csdefine.CHAT_TYPE_FRIEND: "好友",
}


ACTIVITY_NAME_FOR_KEY_DICT = {
	#key: 活动名称
	"SparHunTingMgr_SignUp": "晶石狩猎场报名",
	"SparHunTingMgr_Start": "晶石狩猎场开始",
	"CampLMZCCopyMgr_Start": "灵脉战场",
	"CampFrozenFightCopyMgr_Start": "冰雪之战",
	"CampYXLMCopyMgr_Start": "英雄王座",
	"YeZhanFengQi_Start": "血斗凤栖镇",
	"ShiFangCheng_SignUpStart": "十方城报名",
	"ShiFangCheng_Start": "十方城开始",
	"FirstTongStarcraft_SignUpStart": "帮会争霸第一场报名",
	"FirstTongStarcraft_Start": "帮会争霸第一场开启",
	"CampActivityRandomFitMgr_Start": "阵营战场随机匹配开始",
	"BHZB_SignUpStart": "帮会争霸报名",
	"BHZB_Start": "帮会争霸开始",
	"TongPlunderManager_SignUp": "帮会掠夺战报名",
	"TongPlunderManager_Start": "帮会掠夺战开始",
}
#-------------------------------------------------------------------
#门派分类
#-------------------------------------------------------------------
MENPAI_TYPE_DICT = {	#阵营-职业
	csdefine.CAMP_TAOSIM: {
		csdefine.CLASS_FIGHTER: "昆仑",
		csdefine.CLASS_SWORDMAN: "玉虚",
		csdefine.CLASS_ARCHER: "蓬莱",
		csdefine.CLASS_MAGE: "太清",
	},
	csdefine.CAMP_DEMON: {
		csdefine.CLASS_FIGHTER: "修罗",
		csdefine.CLASS_SWORDMAN: "逍遥",
		csdefine.CLASS_ARCHER: "缥缈",
		csdefine.CLASS_MAGE: "摩柯",
	},
}

#所有职业
ALL_MENPAI_RES = "所有门派"


#-------------------------------------------------------------------
#状态
#-------------------------------------------------------------------
STATE_DICT = {
	True:	"在线",
	False:	"下线",
}


#-------------------------------------------------------------------
#角色性别
#-------------------------------------------------------------------
ROLE_GENDER_DICT = {
	csdefine.MALE: "男性",
	csdefine.FEMALE: "女性",
}


#-------------------------------------------------------------------
#地图名称
#-------------------------------------------------------------------
MAP_NAME_DICT = {
	'L_BHD_2': '冰火岛',
	'fu_ben_L_HZMG_JSGC': '金沙古城',
	'L_TGLX': '太古灵穴',
	'L_WXTDZ_01': '万象天斗阵',
	'L_XLFZ_DYC': '降龙法阵第一层',
	'fu_ben_L_ZLQJ_1': '副本真龙棋局(单人)',
	'fu_ben_L_FST': '副本风煞坛',
	'L_LXD': '龙汐岛',
	'L_HYHZ_04': '狐妖幻阵',
	'L_JX': '金星',
	'cycle_L_LYSL': '雷域危机',
	'L_TSYJ': '土神遗迹',
	'L_HLSY_LOOP': '环任务用幻灵神域',
	'fu_ben_L_HLG': '副本浩灵谷',
	'L_SMZZ_01': '锁仙宮',
	'L_YLG': '隐龙谷',
	'fu_ben_L_ZLQJ_Boss': 'boss战demo新地图',
	'L_SLT_05': '锁灵塔',
	'L_SLT_04': '锁灵塔',
	'L_HYHZ_07': '狐妖幻阵',
	'L_TQG': '太清宫',
	'fu_ben_L_HLTC': '幻莲天池',
	'L_TYG': '太阳宫',
	'L_HLD_01': '火灵岛',
	'L_XLD': '修罗殿',
	'L_QYSX': '青玉圣像',
	'L_XLFZ_DSC': '降龙法阵第三层',
	'L_KLZ': '昆仑宗',
	'fu_ben_L_ZSG': '镇煞宫',
	'fu_ben_L_HZMG_BWK': '宝物库',
	'fu_ben_L_TTY_1': '副本通天崖(单人)',
	'L_JSYH': '九煞阴河',
	'cycle_L_HHMJ': '火海秘境',
	'L_SJFBSP': '收集法宝碎片',
	'L_SLT_02': '锁灵塔',
	'L_M_E_Profile': '程序测试',
	'L_YGD': '云光洞',
	'L_SMZZ': '神脉沼泽',
	'L_FLS': '飞来石',
	'fu_ben_L_HZMG_TMZP': '天命',
	'L_PLG': '蓬莱阁',
	'fu_ben_L_HZMG_YLXF': '云岚仙峰',
	'L_PMG': '缥缈阁',
	'fu_ben_L_HLTC1': '幻莲天池PLUS',
	'L_SLT_01': '锁灵塔',
	'fu_ben_L_HKY_Boss': 'boss战demo',
	'cycle_L_WXHJ': '五行画卷',
	'L_HYDK': '火焰洞窟',
	'fu_ben_L_JTLY': '副本九天灵狱',
	'L_HYHZ_02': '狐妖幻阵',
	'L_WSD': '巫神殿',
	'L_JAIL': '监狱',
	'L_QYDC': '青云道场',
	'L_XLFZ_DEC': '降龙法阵第二层',
	'L_YMGJ': '幽魔古境',
	'fu_ben_L_LCZ_1': '雷池阵',
	'L_SGMJ': '上古秘境',
	'L_WZGHZ_05': '五庄观幻阵',
	'fu_ben_L_XYHY': '副本仙隐画院',
	'L_SYX': '蛇炎星第一层',
	'fu_ben_L_ZLQJ': '副本真龙棋局',
	'L_BHD': '冰火岛',
	'L_TMG': '天魔宫',
	'L_WZGHZ_06': '五庄观幻阵',
	'L_HYHZ_06': '狐妖幻阵',
	'L_YXG': '玉虚宫',
	'L_ZLY': '涿鹿原',
	'cycle_L_LHZS': '灵魂之誓',
	'L_SMZZ_mo': '神脉沼泽',
	'L_XG_01': '穿越峡谷',
	'L_WZGHZ_07': '五庄观幻阵',
	'L_TXHJ_01': '太虚幻境',
	'L_WZGHZ_08': '五庄观幻阵',
	'L_HYHZ_05': '狐妖幻阵',
	'fu_ben_JSSLC': '副本晶石狩猎场',
	'L_SLHJ': '蜃楼幻境',
	'L_JYDT': '九焱洞天',
	'L_SXK': '失心窟',
	'L_TLDC': '天罗道场',
	'L_DBDT_mo': '多宝洞天',
	'fu_ben_L_TTY': '副本通天崖',
	'L_BQXB': '阪泉西部',
	'L_YZD': '瑶泽岛',
	'fu_ben_L_LCZ': '雷池阵',
	'L_WZGHZ_03': '五庄观幻阵',
	'cycle_L_LSMC': '灵兽牧场',
	'L_HYHZ_08': '狐妖幻阵',
	'L_HYHZ_01': '狐妖幻阵',
	'L_TSHJ_001': '天书幻境',
	'cycle_L_RSGY': '人参果园',
	'L_XYM': '逍遥门',
	'L_HLD': '火灵岛',
	'L_WZGHZ_01': '五庄观幻阵',
	'L_LYG': '烈阳谷',
	'L_FMC': '凤鸣城',
	'L_HLSY': '幻灵神域',
	'L_HYDK_02': '寻找十金乌',
	'L_HHFZ': '荷花法阵',
	'fu_ben_L_HYZY': '副本荒月庄园',
	'fu_ben_L_BXZZ': '冰雪之战',
	'L_TMDC': '天沐道场',
	'L_YSC': '盘古洞天',
	'fu_ben_JSSLC1': '副本晶石狩猎场',
	'L_KWSM': '昆吾山脉',
	'fu_ben_L_LMZC': '灵脉战场',
	'L_THG': '天火谷',
	'fu_ben_L_HZMG_QYZP': '气运',
	'fu_ben_L_HZMG_CSG': '藏书阁',
	'L_HYHZ_03': '狐妖幻阵',
	'L_TSHJ': '天书幻境',
	'L_WSS': '万寿山',
	'fu_ben_qinglong1': '副本剿灭赤龙寨',
	'fu_ben_qinglong1_1': '副本剿灭赤龙寨',
	'cycle_L_HQLZ': '龙珠密岛',
	'L_JXY_01': '化身妖魔',
	'fu_ben_L_LDWJ': '副本灵岛危机',
	'cycle_L_LJHY': '灵箭化元',
	'fu_ben_fengmingxunbao1': '副本金殿探宝',
	'L_TXHJ': '太虚幻境',
	'L_JSC': '太虚洞天',
	'L_MKZ': '木傀寨',
	'L_WZGHZ_02': '五庄观幻阵',
	'L_MHD': '摩诃殿',
	'L_XHJD': '星核禁地',
	'fu_ben_L_LYZT': '副本炼狱之塔',
	'L_BHD_1': '冰火岛',
	'cycle_L_LYSH': '灵域狩魂',
	'L_BQDB': '阪泉东部',
	'fu_ben_L_CBK': '副本藏宝库',
	'fu_ben_SFC': '副本真龙棋局(单人)',
	'fu_ben_L_HZMG': '幻阵迷宫',
	'L_XHL': '玄火岭',
	'fu_ben_L_QFGT': '副本琴风古亭',
	'fu_ben_L_LZG': '副本雷泽谷',
	'fu_ben_YZFQ': '凤栖镇（个人竞技）',
	'L_BHLD': '帮会地图',
	'L_JYHD': '九幽寒洞',
	'fu_ben_L_BHMY': '副本冰火魔狱',
	'cycle_L_PSDBGZ': '破碎的八卦阵',
	'L_WZGHZ_04': '五庄观幻阵',
	'L_HYDK_01': '救援十金乌',
	'L_XCMJ': '星辰秘境',
	'fu_ben_L_HYZY_1': '副本荒月庄园(单人)',
	'L_YLF': '阎龙府',
	'L_SLT_03': '锁灵塔',
	'L_YGG': '耀光阁',
	'fu_ben_fengmingxunbao1_1': '副本金殿探宝',
	'L_DBDT': '多宝洞天',
	'L_MXG': '冥仙谷',
	'L_FMNL': '凤鸣南麓',
	'L_DJD': '东极岛',
	'fu_ben_L_TCDL': '逃出丹炉',
	'L_SLT_06': '锁灵塔',
	'fu_ben_L_HKY': '副本火奎崖',
	'fu_ben_L_ZLMJ': '副本烛龙秘境',
	'fu_ben_L_WFSZ': '副本五方石阵',
	'fu_ben_L_HKY_1': '副本火奎崖',
	'L_JX_02': '金星',
	'L_YYQZ': '阴阳棋阵',
}

#-------------------------------------------------------------------
#物品部位
#-------------------------------------------------------------------
ITEM_ORDER_DICT = {
	csdefine.ITEM_ORDER_BAG: "包裹",
	csdefine.ITEM_ORDER_STORE: "仓库",
	csdefine.ITEM_ORDER_WEAR: "穿戴",
}

#----------------------------------------------
#物品大类
#----------------------------------------------
ITEM_TYPE_DICT = {
	csdefine.ITEM_TYPE_DEFAULT: "默认",
	csdefine.ITEM_TYPE_WEAPON: "武器",
	csdefine.ITEM_TYPE_HAT: "帽子",
	csdefine.ITEM_TYPE_COAT: "衣服",
	csdefine.ITEM_TYPE_PANTS: "裤子",
	csdefine.ITEM_TYPE_BELT: "腰带",
	csdefine.TEM_TYPE_WRIST: "护腕",
	csdefine.ITEM_TYPE_GLOVES: "手套",
	csdefine.ITEM_TYPE_SHOES: "鞋子",
	csdefine.ITEM_TYPE_NECKLACE: "项链",
	csdefine.ITEM_TYPE_RING: "戒指",
	csdefine.ITEM_TYPE_FASHION: "时装",
	csdefine.ITEM_TYPE_VARIA: "杂物",
	csdefine.ITEM_TYPE_BDRUG: "气血药",
	csdefine.ITEM_TYPE_EDRUG: "内息药",
	csdefine.ITEM_TYPE_PBDRUG: "幻兽气血药",
	csdefine.ITEM_TYPE_PEDRUG: "幻兽内息药",
	csdefine.ITEM_TYPE_PETEGG: "幻兽蛋",
	csdefine.ITEM_TYPE_SYSTEM: "系统功能",
	csdefine.ITEM_TYPE_SPAR: "晶核",
	csdefine.ITEM_TYPE_MATERIAL: "材料",
	csdefine.ITEM_TYPE_SCROLL: "卷轴",
	csdefine.ITEM_TYPE_CHARM: "符咒",
	csdefine.ITEM_TYPE_GIFT: "礼包",
	csdefine.ITEM_TYPE_PPSKILL: "幻兽被动技能书",
	csdefine.ITEM_TYPE_QUEST: "任务物品",
	csdefine.ITEM_TYPE_ACTIVE: "活动物品",
	csdefine.ITEM_TYPE_COPY: "副本物品",
	csdefine.ITEM_TYPE_COPY_YXWZ1: "英雄王座战魂",
	csdefine.ITEM_TYPE_COPY_YXWZ2: "英雄王座红药",
	csdefine.ITEM_TYPE_COPY_YXWZ3: "英雄王座蓝药",
	csdefine.ITEM_TYPE_COPY_YXWZ4: "英雄王座固定物品",
	csdefine.ITEM_TYPE_PART_EQUIP: "半成品装备",
	csdefine.ITEM_TYPE_BPRINT: "图纸",
	csdefine.ITEM_TYPE_JADE:"玲珑玉令",
}

#-------------------------------------------------------------------
#物品添加删除操作类型
#-------------------------------------------------------------------
ITEM_ADD_DEL_TYPE_DICT = {
	LogDefine.LT_ITEM_ADD: "添加物品",
	LogDefine.LT_ITEM_DEL: "删除物品",
	LogDefine.LT_ITEM_SET_AMOUNT: "设置数值",
	LogDefine.LT_ITEM_TRAN_STORE: "转入仓库",
	LogDefine.LT_ITEM_TALK_STORE: "取出仓库",
}

#-------------------------------------------------------------------
#添加、删除物品原因（途径 ）
#-------------------------------------------------------------------
ITEM_ADD_REASON_DICT = {
	csdefine.ITEM_ADD_BY_PICKUP: "拾取增加物品",
	csdefine.ITEM_ADD_BY_SYS: "系统赠送",
	csdefine.ITEM_ADD_BY_NPCTRADE: "NPC处购买",
	csdefine.ITEM_ADD_BY_ROLETRADE: "玩家交易",
	csdefine.ITEM_ADD_BY_QUEST: "任务奖励获得物品",
	csdefine.ITEM_ADD_BY_QUESTACTION: "任务行为获得物品",
	csdefine.ITEM_ADD_BY_GM_COMMAND: "GM添加物品",
	csdefine.ITEM_ADD_BY_SKILL: "技能添加物品",
	csdefine.ITEM_ADD_BY_BORN_GAIN: "出生赋值",
	csdefine.ITEM_ADD_BY_ADDCHECK: "添加物品检测，并不会添加物品",
	csdefine.ITEM_ADD_BY_STALLTRADE: "摆摊",
	csdefine.ITEM_ADD_BY_USE_GIFT_ITEM: "打开礼包",
	csdefine.ITEM_ADD_BY_SHOPMALLTRADE: "商城处购买",
	csdefine.ITEM_ADD_BY_OPEN_SPELLBOX: "打开宝箱",
	csdefine.ITEM_ADD_BY_SPELLBOX_KEY: "特殊获得宝箱钥匙",
	csdefine.ITEM_ADD_BY_SPACE_ACTION: "副本行为",
	csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT: "副本结算",
	csdefine.ITEM_ADD_BY_TONG_STORE: "帮会仓库",
	csdefine.ITEM_ADD_BY_TONG_SALARY: "帮会俸禄",
	csdefine.ITEM_ADD_BY_STORE: "个人仓库取物品",
	csdefine.ITEM_ADD_BY_MAIL: "邮件",
	csdefine.ITEM_ADD_BY_NEW_PLAYER_GIFT: "新手奖励",
	csdefine.ITEM_ADD_BY_SIGN_IN_GIFT: "签到奖励",
	csdefine.ITEM_ADD_BY_SPLIT: "分割物品",
}
ITEM_DEL_REASON_DICT = {
	csdefine.ITEM_REMOVE_BY_USE: "使用后删除",
	csdefine.ITEM_REMOVE_BY_DROP: "玩家主动丢弃",
	csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY: "装备强化",
	csdefine.ITEM_REMOVE_BY_EQUIP_BACKFIRE: "装备回火",
	csdefine.ITEM_REMOVE_BY_INTENSIFY_SAVE: "装备保存",
	csdefine.ITEM_REMOVE_BY_INTENSIFY_RESTORE: "装备还原",
	csdefine.ITEM_REMOVE_BY_QUESTACTION: "任务行为删除",
	csdefine.ITEM_REMOVE_BY_SELL: "出售",
	csdefine.ITEM_REMOVE_BY_ROLETRADE: "交易",
	csdefine.ITEM_REMOVE_BY_RETURN: "退货",
	csdefine.ITEM_REMOVE_BY_SPACE_EVENT: "副本剧情",
	csdefine.ITEM_REMOVE_BY_SORTSTACK: "背包在整理的时候，叠加物品，有时会删除一些",
	csdefine.ITEM_REMOVE_BY_SWAPITEM: "交换由于叠加造成删除物品",
	csdefine.ITEM_REMOVE_BY_SPAR_FAIL: "炼化晶核失败删除",
	csdefine.ITEM_REMOVE_BY_SPELL_BOX: "场景物件交互 移除物品",
	csdefine.ITEM_REMOVE_BY_STORE: "个人仓库存物品",
	csdefine.ITEM_REMOVE_BY_SKILL: "使用技能消耗物品",
	csdefine.ITEM_REMOVE_BY_SHUFFLE: "装备洗练",
	csdefine.ITEM_REMOVE_BY_RECAST: "装备重铸",
	csdefine.ITEM_REMOVE_BY_BIOGRAPHY: "装备传星",
	csdefine.ITEM_REMOVE_BY_MAIL: "邮件",
	csdefine.ITEM_REMOVE_BY_STORE_SORTSTACK: "仓库相关操作，叠加物品",
	csdefine.ITEM_REMOVE_BY_SELL_TO_NPC: "出售给NPC",
	csdefine.ITEM_REMOVE_BY_GM: "GM指令删除物品",
}

#-------------------------------------------------------------------
#角色交易日志类型
#-------------------------------------------------------------------
ITEM_TRADE_TYPE_DICT = {
	LogDefine.LT_TRADE_SWAP_ITEM: "与玩家交易物品",
	LogDefine.LT_TRADE_SWAP_MONEY: "与玩家交易金钱",
	LogDefine.LT_TRADE_SWAP_PET: "与玩家交易幻兽",
	LogDefine.LT_TRADE_NPC_BUY: "在NPC处买东西",
	LogDefine.LT_TRADE_NPC_SELL: "卖东西给NPC",
	LogDefine.LT_TRADE_SHOP_BUY	: "在商城买东西",
	LogDefine.LT_TRADE_BUY_BACK: "回购",
	LogDefine.LT_TRADE_BUY_BACK_HIGH: "高价回购",
	LogDefine.LT_TRADE_RETURN_ITEM: "退货",
	LogDefine.LT_TRADE_GIVING_GOOD: "赠送",
}

#-----------------------------
#角色交易方式
#-----------------------------
ITEM_ROLE_TRADE_TYPE_DICT = {
	LogDefine.LT_TRADE_TYPE_TRANSFER: "直接交易",
	LogDefine.LT_TRADE_TYPE_VEND: "摆摊交易"
}

#-------------------------------------------------------------------
#装备部位分类
#-------------------------------------------------------------------
EQUIP_ORDER_DICT = {
	ItemTypeEnum.EQUIP_HAT: "帽子",
	ItemTypeEnum.EQUIP_COAT: "上衣，衣服",
	ItemTypeEnum.EQUIP_WRIST: "护腕",
	ItemTypeEnum.EQUIP_HAND: "手套",
	ItemTypeEnum.EQUIP_WAIST: "腰带",
	ItemTypeEnum.EQUIP_PANTS: "裤子",
	ItemTypeEnum.EQUIP_SHOES: "鞋子",
	ItemTypeEnum.EQUIP_NECKLACE: "项链",
	ItemTypeEnum.EQUIP_RING: "左手戒指",
	#ItemTypeEnum.EQUIP_RING: "右手戒指（被占用）",
	ItemTypeEnum.EQUIP_WEAPON: "双手武器",
	ItemTypeEnum.EQUIP_LEFT_WEAPON: "左手武器",
	ItemTypeEnum.EQUIP_RIGHT_WEAPON: "右手武器",
	ItemTypeEnum.EQUIP_CLOAK: "披风",
	ItemTypeEnum.EQUIP_FABAO: "法宝",
}

#-------------------------------------------------------------------
#角色属性编号定义
#-------------------------------------------------------------------
ROLE_ATTRIBUTE_NUMBER_DICT = {
	ItemTypeEnum.CORPOREITY: "根骨",
	ItemTypeEnum.STRENGTH: "筋力",
	ItemTypeEnum.INTELLECT: "内力",
	ItemTypeEnum.DISCERN: "洞察",
	ItemTypeEnum.DEXTERITY: "身法",
	ItemTypeEnum.HP: "气血",
	ItemTypeEnum.MP: "内息",
	ItemTypeEnum.DAMAGE: "外攻",
	ItemTypeEnum.MAGICDAMAGE: "内攻",
	ItemTypeEnum.ARMOR: "外防",
	ItemTypeEnum.MAGICARMOR: "内防",
	ItemTypeEnum.CRITICALSTRIKE: "会心",
	ItemTypeEnum.PARRY: "招架",
	ItemTypeEnum.SPEED: "移速",
	ItemTypeEnum.HITRATE: "命中率",
	ItemTypeEnum.DODGERATE: "闪避率",
	ItemTypeEnum.HEALINGRATE: "自愈率",
	ItemTypeEnum.GANGQI_MAX: "罡气",
	ItemTypeEnum.GANGQI_DAMAGE_POINT: "罡气攻击",
	ItemTypeEnum.GANGQI_ARMOR_POINT: "罡气防御",
	ItemTypeEnum.GANGQI_QIJIE_REVIVE: "气竭罡气自愈率",
	ItemTypeEnum.GANGQI_QIYING_REVIVE: "气盈罡气自愈率",
	ItemTypeEnum.TEMPSPEED: "临时速度",
	ItemTypeEnum.CURE: "治疗成效",
	ItemTypeEnum.CRITRATIO: "暴击倍率",
	ItemTypeEnum.PARRYRATIO: "招架倍率",
	ItemTypeEnum.DAMAGECORRECTION: "造成伤害修正",
	ItemTypeEnum.ARMORCORRECTION: "承受伤害修正",
	ItemTypeEnum.ATTACK_DAMAGECORRECTION: "造成物理伤害修正",
	ItemTypeEnum.MAGIC_DAMAGECORRECTION: "造成法术伤害修正",
	ItemTypeEnum.ATTACK_ARMORCORRECTION: "承受物理伤害修正",
	ItemTypeEnum.MAGIC_ARMORCORRECTION: "承受法术伤害修正",
	ItemTypeEnum.ROLE_DAMAGECORRECTION: "造成对玩家伤害修正",
	ItemTypeEnum.PET_DAMAGECORRECTION: "造成对幻兽伤害修正",
	ItemTypeEnum.MONSTER_DAMAGECORRECTION: "造成对怪物伤害修正",
	ItemTypeEnum.ROLE_ARMORCORRECTION: "承受玩家伤害修正",
	ItemTypeEnum.PET_ARMORCORRECTION: "承受幻兽伤害修正",
	ItemTypeEnum.MONSTER_ARMORCORRECTION: "承受怪物伤害修正",
	ItemTypeEnum.CURECORRECTION: "治疗加深",
	ItemTypeEnum.BECURECORRECTION	: "承受治疗加深",
}

#-------------------------------------------------------------------
#装备强化操作定义
#-------------------------------------------------------------------
EQUIP_OPT_TYPE_DICT = {
	LogDefine.LT_EQUIP_INTENSIFY: "装备强化",
	LogDefine.LT_EQUIP_COMPOSE: "装备打造",
	LogDefine.LT_EQUIP_SHUFFLE: "装备洗练",
	LogDefine.LT_EQUIP_SHUFFLE_REPLACE: "装备洗练替换",
	LogDefine.LT_EQUIP_RECAST: "装备重铸",
	LogDefine.LT_EQUIP_REPAIR: "装备修理",
	LogDefine.LT_EQUIP_BACKFIRE: "装备回火",
	LogDefine.LT_EQUIP_RESTORE: "装备还原",
	LogDefine.LT_EQUIP_SAVE: "装备保存",
	LogDefine.LT_EQUIP_TRAN_STAR: "装备传星",
}

#-------------------------------------------------------------------
#装备强化操作定义
#-------------------------------------------------------------------
EQUIP_ATTRIBUTE_TYPE_DICT = {
	"hardiness": "耐久度",
}

#-------------------------------------------------------------------
#幻兽品质
#-------------------------------------------------------------------
PET_QUALITY_DICT = {
	csdefine.VEHICLE_PET_QUALITY_NORMAL: "凡兽",
	csdefine.VEHICLE_PET_QUALITY_SPIRIT: "灵兽",
	csdefine.VEHICLE_PET_QUALITY_HOLY: "圣兽",
	csdefine.VEHICLE_PET_QUALITY_DEITY: "神兽",
}
#-------------------------------------------------------------------
#幻兽操作定义
#-------------------------------------------------------------------
PET_ACTION_DICT = {
	LogDefine.LT_PET_ADD: "获得幻兽",
	LogDefine.LT_PET_LOSE: "失去幻兽",
	LogDefine.LT_PET_SKILL_LEARN: "幻兽学习技能",
	LogDefine.LT_PET_SKILL_UPGRADE: "幻兽升级技能",
	LogDefine.LT_PET_SEAL: "幻兽封印",
	LogDefine.LT_PET_REPLACE_SKILL: "幻兽替换技能",
	LogDefine.LT_PET_COMPOSE: "幻兽合成",
	LogDefine.LT_PET_UP_STEP: "幻兽升阶",
}
#-------------------------------------------------------------------
#幻兽替换技能类型定义
#-------------------------------------------------------------------
LT_PET_REPLACE_SKILL_DICT = {
	LogDefine.LT_PET_REPLACE_SKILL_ACTIVE: "替换主动技能",
	LogDefine.LT_PET_REPLACE_SKILL_PASSIVE: "替换被动技能"
}
#-------------------------------------------------------------------
#幻兽升级技能类型定义
#-------------------------------------------------------------------
PET_SKILL_UPGRADE_DICT = {
	LogDefine.LT_PET_SKILL_UPGRADE_ACTIVE: "升级主动技能",
	LogDefine.LT_PET_SKILL_UPGRADE_PASSIVE: "升级被动技能"
}

#-------------------------------------------------------------------
#获得幻兽原因
#-------------------------------------------------------------------
PET_ADD_REASON_DICT = {
	csdefine.PET_ADD_REASON_DEFAULT: "默认",
	csdefine.PET_ADD_REASON_COMPLETE_QUEST: "完成任务获得",
	csdefine.PET_ADD_REASON_KILL_PETMONSTER: "击杀幻兽怪物获得",
}

#-------------------------------------------------------------------
#失去幻兽原因
#-------------------------------------------------------------------
PET_REMOVE_REASON_DICT = {
	csdefine.PET_REMOVE_REASON_FREE: "放生",
}

#-------------------------------------------------------------------
#任务进度
#-------------------------------------------------------------------
QUEST_STATE_DICT = {
	LogDefine.LT_QUEST_ACCEPT: "接受任务",
	LogDefine.LT_QUEST_COMPLETE: "完成任务",
	LogDefine.LT_QUEST_ABANDON: "放弃任务",
}

#-------------------------------------------------------------------
#充值
#-------------------------------------------------------------------
CHARGE_TYPE_NAME = {
	tooldefine.CHARGE_TYPE_GY_COIN: "光宇币兑换",
	tooldefine.CHARGE_TYPE_SCORE: "积分兑换",
	tooldefine.CHARGE_TYPE_POINT_CARD: "点卡交易",
}