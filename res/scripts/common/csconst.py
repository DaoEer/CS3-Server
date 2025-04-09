#-*-coding:utf-8-*-

import csdefine
import csstatus
import ItemTypeEnum

CONFIG_PATCH = "res/scripts/data/"

# --------------------------------------------------------------------
# about login
# --------------------------------------------------------------------
LOGIN_ROLE_UPPER_LIMIT					= 5			# 最多可以创建多少个角色
ROLE_NAME_LENGTH_UPPER_LIMIT			= 14		# 角色名字长度上限
TONG_NAME_LENGTH_UPPER_LIMIT			= 12		# 帮会名字长度上限

# --------------------------------------------------------------------
# object paths
# --------------------------------------------------------------------
SPACE_OBJECT_CONFIG_PATH				= "data/SpaceObject"

SPAWN_POSITION_X						= (-61.38, 157.43, 100.49)
SPAWN_DIRECTION_X						= (0, 0, 2.97)
SPAWN_SPACE_X							= "L_YXG"

SPAWN_POSITION_M						= (-122.80, 159.65, 520.2)
SPAWN_DIRECTION_M						= (0.0, 0.0, 1.57)
SPAWN_SPACE_M							= "L_XYM"

REVIVE_SPACE_SCRIPTID 					= "L_FMC"
REVIVE_POSITION 						= (215.73,122.3,236.14)
REVIVE_DIRECTION 						= (0.0,0.0,-1.5)

SPAWN_ROUTE								= -1		# 如果值为-1，则不设置出生点

# 单方关系列表
SINGLE_RELATION_LIST = [ csdefine.ROLE_RELATION_BLACKLIST, csdefine.ROLE_RELATION_FOE, csdefine.ROLE_RELATION_LAST_CHAT ]
# 双发关系列表
MULTI_RELATION_LIST = [ csdefine.ROLE_RELATION_FRIEND ]

#------------------------金币----------------------------------
MONEY_MAX_AMOUNT						= 10000000000		# 金币最大数量
#---------仓库------------------------------------------
LIMIT_STORE_MONEY						= 100000000000		# 仓库最大存储金币数(1000万金币)

#---------skill------------------------------------------
ATTACK_RANGE_BIAS						= 1.5		# 表示由于客户端和服务器EntityPosition不一致允许的攻击距离计算偏差
BUFF_SOURCE_INDEX_MAX					= 100		# buffSourceIndex，最大值
BUFF_AMOUNT_MAX							= 25		# buff警告最大数量

#---------entity状态、行为-----------------------------------------------
EFFECT_STATE_TO_ACTION_FLAGS = {
			csdefine.EFFECT_STATE_DIZZY				: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_SPELL,
													  csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_TALK],
			
			csdefine.EFFECT_STATE_UNCONTROLLABLE	: [csdefine.ACTION_FORBID_BE_HIT_BACK, csdefine.ACTION_FORBID_BE_CONTROL],
			
			csdefine.EFFECT_STATE_INVINCIBLE		: [csdefine.ACTION_FORBID_BE_ATTACK, csdefine.ACTION_FORBID_BE_HIT_BACK, csdefine.ACTION_FORBID_BE_CONTROL, csdefine.ACTION_FORBID_BE_DEPRESS,
														csdefine.ACTION_FORBID_INSANE],
			
			csdefine.EFFECT_STATE_HIT_BACK			: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_SPELL,
													  csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_TALK],
			
			csdefine.EFFECT_STATE_FIX				: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP],
			
			csdefine.EFFECT_STATE_SLEEP				: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_SPELL,
													  csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_TALK],
			
			csdefine.EFFECT_STATE_WIND				: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_JUMP , csdefine.ACTION_FORBID_TRANSLATE_DIRECTION],
			csdefine.EFFECT_STATE_PROTECT			: [csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_WIELD , csdefine.ACTION_FORBID_ATTACK,
													   csdefine.ACTION_FORBID_SPELL , csdefine.ACTION_FORBID_TALK , csdefine.ACTION_FORBID_BE_ATTACK , csdefine.ACTION_FORBID_TRIGGER_PASSIVE ,csdefine.ACTION_FORBID_BE_HIT_BACK],
			csdefine.EFFECT_STATE_FOLLOW			: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_SPELL],
			csdefine.EFFECT_STATE_CONFUSION			: [csdefine.ACTION_FORBID_TALK],
			csdefine.EFFECT_STATE_UNYIELDING		: [],
			csdefine.EFFECT_STATE_FREEZE			: [csdefine.ACTION_FORBID_MOVE , csdefine.ACTION_FORBID_SPELL , csdefine.ACTION_FORBID_JUMP,
													  csdefine.ACTION_FORBID_EMERGENCY_EXIT, csdefine.ACTION_FORBID_USE_ITEM , csdefine.ACTION_FORBID_TRANSLATE_DIRECTION , csdefine.ACTION_FORBID_TALK],
			csdefine.EFFECT_STATE_SHOW 				: [csdefine.ACTION_FORBID_BE_CONTROL,csdefine.ACTION_FORBID_BE_HIT_BACK,csdefine.ACTION_FORBID_BE_ATTACK],
			csdefine.EFFECT_STATE_HIDE				: [],
	}

#属性
FLOAT_ZIP_PERCENT						= 10000.0

# Time
TIME_ENLARGE_MULTIPLE					= 10000000

ROLE_EXP_MAX_LEVEL						= 150		# 玩家经验对应最大等级，用在common/LevelEXP.py中
ROLE_LEVEL_UPPER_LIMIT					= 40		# 玩家等级上限


ROLE_POTENTIAL_UPPER					= 100000000			# 玩家潜能点上限

ROLE_XIANSHI_UPPER_LIMIT				= 900000000			# 玩家拥有仙石上限
ROLE_LINGSHI_UPPER_LIMIT				= 900000000			# 玩家拥有灵石上限
ROLE_XUANSHI_UPPER_LIMIT				= 900000000			# 玩家拥有玄石上限


#移动行为中跑与走的速度比率
WalkRatio			= 0.25
RunRatio			= 1.0
SpeedRunRatio		= 2.0


#是否使用旧版本AI
AI_USING_OLD_FLAG						= 0
STALL_ITEM_MAX_COUNT					= 30		# 摆摊出售商品上限
STALL_NAME_MAX_LENGTH					= 20		# 摆摊名称的最大字节数

TELEPORT_PROTECT_BUFFID					= 12345607			# 传送保护buffID



# Group
GROUP_ENDTIME_MAPPING = {
					csdefine.GROUP_END_TIME_NONE			: [0, 0],
					csdefine.GROUP_END_TIME_ONE_MONTH		: [30*24*3600*TIME_ENLARGE_MULTIPLE, 0],
					csdefine.GROUP_END_TIME_TWO_MONTH		: [60*24*3600*TIME_ENLARGE_MULTIPLE, 0],
					csdefine.GROUP_END_TIME_THREE_MONTH		: [90*24*3600*TIME_ENLARGE_MULTIPLE, 0],
	}

ROLE_GIVINGGOODSDATA_UPPER_LIMIT		= 50		# 玩家赠送物品的上限
ROLE_CARRYGOODS_UPPER_LIMIT				= 20		# 玩家可携带数量上限的商品

#摆摊的摊税
ROLE_STALL_PRICE = 0.01

#阵营关系
CAMP_RALETION = {
					(csdefine.CAMP_TAOSIM, csdefine.CAMP_DEMON)					: csdefine.COMBAT_RELATION_ENEMY,		# 仙&魔
					(csdefine.CAMP_TAOSIM, csdefine.CAMP_NEUTRAL_ENEMY)			: csdefine.COMBAT_RELATION_ENEMY,		# 仙&中立敌对
					(csdefine.CAMP_TAOSIM, csdefine.CAMP_NEUTRAL_NORMAL)		: csdefine.COMBAT_RELATION_NORMAL,		# 仙&中立友好
					(csdefine.CAMP_DEMON, csdefine.CAMP_NEUTRAL_ENEMY)			: csdefine.COMBAT_RELATION_ENEMY,		# 魔&中立敌对
					(csdefine.CAMP_DEMON, csdefine.CAMP_NEUTRAL_NORMAL)			: csdefine.COMBAT_RELATION_NORMAL,		# 魔&中立友好
					(csdefine.CAMP_NEUTRAL_ENEMY, csdefine.CAMP_NEUTRAL_NORMAL)	: csdefine.COMBAT_RELATION_NORMAL,		# 中立敌对&中立友好
	}

#灵石寄售
LINGSHI_TRADE_QTY_UNIT 					= 100 		# 灵石寄售数量单位
LINGSHI_TRADE_UPPER_LIMIT				= 5			# 灵石寄售的最大条目数
LINGSHI_TRADE_PRICE						= 0.02		# 灵石寄售的手续费
LINGSHI_TRADE_SUCCESS_LIMIT				= 50		# 灵石寄售成交单数

#不能战斗的状态
NOT_FIGHT_STATES  = [
					csdefine.ENTITY_STATE_RESET,
					csdefine.ENTITY_STATE_DEAD,
					csdefine.ENTITY_STATE_PEAD,
					csdefine.ENTITY_STATE_STALL,
	]

#不能被怪物攻击状态
NOT_ATTACK_STATES = [
					csdefine.ENTITY_STATE_RESET,
					csdefine.ENTITY_STATE_DEAD,
					csdefine.ENTITY_STATE_PEAD,
	]

#队伍
TEAM_MEMBER_MAX							= 5			# 定义队伍最大成员数
TEAM_SURVIVAL_TIME						= 600		# 定义队伍在全员离线时的最大存活时间
TEAM_FOLLOW_REQUEST_DISTANCE			= 20		# 多远内的队员能收到组队跟随邀请
TEAM_FOLLOW_TRANSPORT_DISTANCE			= 20		# 过地图时，多远内的队员能跟过去
#禁止仙魔组队的地方
FORBID_XIAN_MO_INVITE_EACE_OTHER 		= [ "fu_ben_L_YCJMD_zhenyingPVP_wuren1",
											"fu_ben_L_YXWZ",
											"fu_ben_L_SGMZ",
											"fu_ben_JSSLC1"]
#禁止不同阵营组队的地方（设置了临时阵营）
FORBID_DIFF_CAMP_INVITE_EACH_OTHER 		= [ "fu_ben_L_YCJMD_zhenyingPVP",
											"fu_ben_L_LMZC"
]

# 有这些效果时，不能跟随
TEAM_FOLLOW_FORBID_EFFECT = [csdefine.EFFECT_STATE_DIZZY, csdefine.EFFECT_STATE_FIX, csdefine.EFFECT_STATE_SLEEP, csdefine.EFFECT_STATE_WIND]


# 幻兽成长度修正值
correctBase			= 0.0
correctDivisor		= 100.0
correctSquare		= 1.0

# 幻兽栏开启
ACTIVATE_PET_CAGES	= {
					3 : {"needLevel":30, "needMoney":50000},
					4 : {"needLevel":40, "needMoney":200000},
					5 : {"needLevel":50, "needMoney":500000},
					6 : {"needLevel":60, "needGold":100},
	}

# 幻兽技能栏开启 品质:技能栏位
PET_SKILL_CAGES	= {
					1 : 2,
					2 : 2,
					3 : 3,
					4 : 5,
					5 : 5,
	}

# 幻兽开始使用血槽恢复血量的BUFF
PET_USE_BLOOD_SLOT_BUFF = 15003401

# 幻兽开始使用蓝槽恢复蓝量的BUFF
PET_USE_BLUE_CHANNEL_BUFF = 15003402

# 原兽喂养CD时间
ORIGIN_PET_FEED_TIME = 60				# 原兽喂养cd时间1分钟

# 技能目标类型筛选的参数选项清单（对应的ENTITY_TYPE定义在csdefine.py中）
ENTITY_TYPE_DICT = {
					1 : "Role",
					3 : "Monster",
					6 : "SpellBox",
					7 : "Trap",
					9 : "Pet"
	}


MOVE_TYPE_DICT = {					
					csdefine.MOVE_TYPE_HIT_BACK					: csdefine.PERFORMANCE_PASSIVITY_MOVE,
					csdefine.MOVE_TYPE_NAVIGATE_POINT_TEST		: csdefine.PERFORMANCE_PASSIVITY_MOVE,
					csdefine.MOVE_TYPE_SKILL_JUMP				: csdefine.PERFORMANCE_PASSIVITY_MOVE,
					csdefine.MOVE_TYPE_FLY_TO_POINT				: csdefine.PERFORMANCE_PASSIVITY_MOVE,
					csdefine.MOVE_TYPE_SKILL_CHASE				: csdefine.PERFORMANCE_PASSIVITY_MOVE,
					csdefine.MOVE_TYPE_CHARGE					: csdefine.PERFORMANCE_PASSIVITY_MOVE,

					csdefine.MOVE_TYPE_GOBACK					: csdefine.SYSTEM_MOVE,
					
					csdefine.MOVE_TYPE_STOP						: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_RANDOM					: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_WANDER					: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_WALK_AROUND				: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_NAVIGATE_POINT			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_MOVE_POINT				: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_CHASE					: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_PATROL					: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_LOOP_ROTATOR				: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_RANDOM_CHOICE_FORM_LIST	: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_FIGHT_DISPERSE			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_CHASE_CLIENT 			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_REVERSE_PATROL			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_SOLDIER_FOLLOW			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_SOLDIER_RECT				: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_SOLDIER_CIRCLE			: csdefine.NORMAL_MOVE,
					csdefine.MOVE_TYPE_RANDOM_IN_SPHERE			: csdefine.NORMAL_MOVE,
	}


#---------------------------战斗关系相关-----------------------------------
#玩家关系规则与关系判断类的对应关系
ROLE_RELATION_RULE_TO_REL_CLS = {
									csdefine.ROLE_RELATION_RULE_CAMP	: "RelRole_Camp",
									csdefine.ROLE_RELATION_RULE_PKMODE	: "RelRole_PKMode",
									csdefine.ROLE_RELATION_RULE_PEACE	: "RelRole_Peace",
									csdefine.ROLE_RELATION_RULE_ENEMY	: "RelRole_Enemy",
									csdefine.ROLE_RELATION_RULE_TONG_STARCRAFT: "RelRole_TongStarcraft",
									csdefine.ROLE_RELATION_RULE_TEAM_STARCRAFT: "RelRole_TeamStarcraft",
									csdefine.ROLE_RELATION_RULE_BLONG_SIDE:"RelRoleEntityRelationGCZ",
									csdefine.ROLE_RELATION_RULE_LHMJ: "RelEntityRelationLHMJ",
								}

KV_ORANGE_NAME		= 1		#橙名杀气值
KV_RED_NAME			= 40	#红名杀气值
KV_MORE_GO_JAIL		= 150	#进监狱杀气值

HARDINESS_VALUE_ORANGE_NAME = 0.03	#橙名掉耐久比例
HARDINESS_VALUE_RED_NAME = 0.06		#红名掉耐久比例
KV_REDUCE_TICK = 60.0					#杀气值衰减tick（秒）
PK_PROTECT_LEVEL = 30				#pk保护等级

JAIL_SCRIPTID = "L_JAIL"			#监狱地图名
JAIL_ENTER_POS = (24540.84, -67901.30, -1297.84)	#监狱进入坐标
JAIL_ENTER_DIR = (0,0,0)			#监狱进入朝向


#-------------------邮件-----------------------
MAIL_TITLE_LENGTH_MAX 				= 10			# 邮件标题最大长度（字节)
MAIL_CONTENT_LENGTH_MAX				= 255			# 邮件内容最大长度（字节)

MAIL_OUTTIMED						= 2592000		# 未读邮件删除时间，单位：秒； 2592000 = 3600*24*30 秒；表示邮件多长时间没有阅读就会被删除

MAIL_SEND_COST						= 0				# 发送邮件的收费 目前暂时未加 先留着
MAIL_UPPER_LIMIT					= 100			# 收件人可存在的邮件数量
MAIL_RECORD_RECEIVE_NAME_MAX 		= 5				# 记录收信人的最大人数


#---------------帮会--------------
#帮众经验划分等级
TONG_RANK_EXP_1	= 400
TONG_RANK_EXP_2	= 300
TONG_RANK_EXP_3	= 200
TONG_RANK_EXP_4	= 100
TONG_RANK_EXP_5	= 0

TONG_JOIN_MIX_LEVEL = 20					# 加入帮会最低等级
TONG_STORE_BAG_CAPACITY = 80				# 帮会仓库每个包袱的容量
TONG_DAILY_TREE_MIN = 3						# 帮会日常任务每层最小枝点
TONG_DAILY_TREE_MAX = 4						# 帮会日常任务每层最大枝点

#交易条件
TRADE_CONDITION_TYPE_LEVEL			= "level"
TRADE_CONDITION_TYPE_JINGJIELEVEL	= "jingjieLevel"
TRADE_CONDITION_TYPE_TONGSHOPLEVEL	= "tongShopLevel"
TRADE_CONDITION_TYPE_TONGTITLE		= "tongTitle"
TRADE_CONDITION_TYPE_RESEARCHSKILLID= "researchSkillID"
TRADE_CONDITION_TYPE_TONGSMITHYLEVEL= "tongSmithyLevel"

ITEM_XUANJING_CLASS					= "ItemIntensifyCrystal"	# 玄晶物品脚本
ITEM_SYMBOL_CLASS					= "ItemIntensifySymbol"		# 回火符物品脚本(回火符、北斗符、血符、重铸保护符)
ITEM_SPAR_CLASS						= "ItemIntensifySpar"		# 晶石物品脚本
ITEM_DRAGON_CLASS					= "ItemIntensifyDragon"		# 龙珠物品脚本
ITEM_RESET_CLASS					= "ItemShuffle"				# 洗练石（重铸宝珠）

PAY_TRADETYPE_TO_REASON_XIAN_SHI = {							# 交易类型与仙石消耗映射关系
	csdefine.TRADE_TYPE_SHUFFLE_EQUIP : csdefine.CHANGE_XIANSHI_RECAST_EQUIP,
	csdefine.TRADE_TYPE_RECOST_EQUIP : csdefine.CHANGE_XIANSHI_RESET_EQUIP,
	csdefine.TRADE_TYPE_OPEN_INTENSIFY_SAVE_SLOT : csdefine.CHANGE_XIANSHI_INTENSIFY_SAVESLOT,
	csdefine.TRADE_TYPE_COMPOSE_EQUIP : csdefine.CHANGE_XIANSHI_COMPOSE_EQUIP,
	 }

PAY_XIANSHI_USE_LINGSHI = {
	csdefine.CHANGE_XIANSHI_NORMAL 						: csdefine.CHANGE_LINGSHI_NORMAL,
	csdefine.CHANGE_XIANSHI_UNLOCKBAGGRID				: csdefine.CHANGE_LINGSHI_UNLOCKBAGGRID,
	csdefine.CHANGE_XIANSHI_PETCAGES 					: csdefine.CHANGE_LINGSHI_PETCAGES,
	csdefine.CHANGE_XIANSHI_INTENSIFY_SAVESLOT			: csdefine.CHANGE_LINGSHI_INTENSIFY_SAVESLOT,
	csdefine.CHANGE_XIANSHI_GM_SET 						: csdefine.CHANGE_LINGSHI_GM_SET,
	csdefine.CHANGE_XIANSHI_AUGMENT_SIGNIN 				: csdefine.CHANGE_LINGSHI_AUGMENT_SIGNIN,
	csdefine.CHANGE_XIANSHI_COMPOSE_EQUIP 				: csdefine.CHANGE_LINGSHI_COMPOSE_EQUIP,
	csdefine.CHANGE_XIANSHI_CHARGE 						: csdefine.CHANGE_LINGSHI_CHARGE,
	csdefine.CHANGE_XIANSHI_RECAST_EQUIP 				: csdefine.CHANGE_LINGSHI_RECAST_EQUIP,
	csdefine.CHANGE_XIANSHI_RESET_EQUIP 				: csdefine.CHANGE_LINGSHI_RESET_EQUIP,
	csdefine.CHANGE_XIANSHI_BY_MAILL 					: csdefine.CHANGE_LINGSHI_BY_MAILL,
	csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME 			: csdefine.CHANGE_LINGSHI_BY_SHOP_CONSUME,
	csdefine.CHANGE_XIANSHI_BY_TRADE 					: csdefine.CHANGE_LINGSHI_BY_TRADE,
	csdefine.CHANGE_XIANSHI_BY_INTENSIFY_EQUIP 			: csdefine.CHANGE_LINGSHI_BY_INTENSIFY_EQUIP,
	csdefine.CHANGE_XIANSHI_BY_RESET_EQUIP 				: csdefine.CHANGE_LINGSHI_BY_RESET_EQUIP,
	csdefine.CHANGE_XIANSHI_BY_SAVE_INTENSIFY_EQUIP 	: csdefine.CHANGE_LINGSHI_BY_SAVE_INTENSIFY_EQUIP,
	csdefine.CHANGE_XIANSHI_BY_RESET_INTENSIFY_EQUIP 	: csdefine.CHANGE_LINGSHI_BY_RESET_INTENSIFY_EQUIP,
	csdefine.CHANGE_XIANSHI_BY_UNLOCK_PASSIVESKILLBAR 	: csdefine.CHANGE_LINGSHI_BY_UNLOCK_PASSIVESKILLBAR,
	csdefine.CHANGE_XIANSHI_PETCOMPOSE 					: csdefine.CHANGE_LINGSHI_PETCOMPOSE,
}

# 防沉迷
WALLOW_STATES = set( [
	csdefine.WALLOW_STATE_COMMON,
	csdefine.WALLOW_STATE_HALF_LUCRE,
	csdefine.WALLOW_STATE_NO_LUCRE
	] )										# 所有收益状态
ANTIWALLOWTICK = 1.0 						#防沉迷检测频率时间

#英雄联盟匹配取消确定时间
SPACECOPY_CAMP_YXLM_AFFIRM_TIME			= 300.0
MONSTERYXLM_MAX_LEVEL = 3 #英雄联盟最大等级

#上古密阵匹配取消确定时间
SPACECOPY_CAMP_SGMZ_AFFIRM_TIME			= 300.0
SPACECOPY_CAMP_SGMZ_MATCH_TIME			= 150.0

#------------------CST-3393 战斗力计算 -----------------
# 价值(系数)

PROPERTY_FACTOR = {
					ItemTypeEnum.CORPOREITY 	: 119.04,		
					ItemTypeEnum.STRENGTH 		: 113.4, 		
					ItemTypeEnum.INTELLECT 		: 88.38, 		
					ItemTypeEnum.DISCERN		: 62.58,		
					ItemTypeEnum.DEXTERITY 		: 62.58,			
					ItemTypeEnum.HP 			: 15.83,			
					ItemTypeEnum.MP 			: 5.28, 			
					ItemTypeEnum.DAMAGE 		: 34.72, 		
					ItemTypeEnum.MAGICDAMAGE	: 32.21, 		
					ItemTypeEnum.ARMOR			: 104.66, 		
					ItemTypeEnum.MAGICARMOR		: 103.82, 		
					ItemTypeEnum.CRITICALSTRIKE : 39.27, 		
					ItemTypeEnum.PARRY			: 63.5 	
}	

# 职业修正价值(系数)
PROFESSION_CORRECTION_FACTOR = {
	csdefine.CLASS_FIGHTER:{
							'corporeity'	:	136.676,
							'strength'		:	103.0808,
							'intellect'		:	50.5575,
							'discern'		:	58.905,
							'dexterity'		:	12.7
							},
	csdefine.CLASS_SWORDMAN:{
							'corporeity'	:	120.846,
							'strength'		:	113.1496,
							'intellect'		:	68.273,
							'discern'		:	58.905,
							'dexterity'		:	12.7
							},
	csdefine.CLASS_ARCHER:	{
							'corporeity'	:	120.846,
							'strength'		:	115.58,
							'intellect'		:	70.5277,
							'discern'		:	58.905,
							'dexterity'		:	12.7
							},
	csdefine.CLASS_MAGE:	{
							'corporeity'	:	105.016,
							'strength'		:	89.54,
							'intellect'		:	74.715,
							'discern'		:	58.905,
							'dexterity'		:	12.7
							}
}

#------------------------排行榜----------------------
GAME_LEVEL_RANK_LOWER_LEVEL = 10			# 等级排行榜最低等级
GAME_COMBAT_RANK_LOWER_LEVEL= 30			# 战斗力排行榜最低等级
GAME_MONEY_RANK_LOWER_MONEY	= 1000000		# 财富排行榜最低财富
GAME_RANKING_NUM_PER_PAGE	= 10			# 排行榜每页显示条目
GAME_RANKING_NUM_MAX_PAGE	= 10			# 排行榜最大页数


#---------------------------切磋-----------------------------------
COMPETE_PREP_COUNTDOWN 				= 10 			#切磋准备10s倒计时
COMPETE_TIME 						= 300 			#5分钟切磋时间
COMPETE_LAST_COUNTDOWN 				= 10  	 		#切磋最后剩余10s倒计时
COMPETE_FLAG_SCRIPTID 				= "20008154" 	#棋子ScriptID
COMPETE_MIN_LEVEL 					= 30 			#发起最小切磋等级
COMPETE_MAX_DIST 					= 20.0 			#发起切磋最大距离
COMPETE_AREA_DIST 					= 24.0			#切磋范围
COMPETE_COME_BACK_AREA_TIME 		= 5 			#返回切磋范围时间
COMPETE_RAND_MSG 					= [csstatus.COMPETE_MSG_1_0, csstatus.COMPETE_MSG_2_0, csstatus.COMPETE_MSG_3_0] #邀请方随机骚话
COMPETE_VOICEID 					= "other010106" #开始切磋时的铜锣声
COMPETE_EFFECTID                    = "101588" 		#切磋范围光效ID
COMPETE_ACTION_START 				= 1
COMPETE_ACTION_WIN 					= 2
COMPETE_ACTION_LOSE 				= 3
COMPETE_ACTIONS_BUFF = {
	COMPETE_ACTION_START: {
							csdefine.CLASS_FIGHTER: 14026801,
							csdefine.CLASS_SWORDMAN: 14026804,
							csdefine.CLASS_ARCHER: 14026807,
							csdefine.CLASS_MAGE: 14026810
						},
	COMPETE_ACTION_WIN: {
							csdefine.CLASS_FIGHTER: 14026802,
							csdefine.CLASS_SWORDMAN: 14026805,
							csdefine.CLASS_ARCHER: 14026808,
							csdefine.CLASS_MAGE: 14026811	
						},		
	COMPETE_ACTION_LOSE: {
							csdefine.CLASS_FIGHTER: 14026803,
							csdefine.CLASS_SWORDMAN: 14026806,
							csdefine.CLASS_ARCHER: 14026809,
							csdefine.CLASS_MAGE: 14026812	
						}			
}


AI_ENTITIES_IN_RANGE_HEIGHT = 20 #AI搜索的有效高度


COMBAT_POWER_CHANGE_REASONS = [csdefine.CALC_COMBAT_POWER_REASON_EQUIP, csdefine.CALC_COMBAT_POWER_REASON_PROP, csdefine.CALC_COMBAT_POWER_REASON_TITLE]


#---------------- 奖励领取 -------------------------------
PCU_TAKEPRESENTWITHOUTID		= 0			#不带订单号的奖品领取类型
PCU_TAKESILVERCOINS				= 1			#银元宝领取类型
PCU_TAKEPRESENT					= 2			#带订单号的奖品领取类型
PCU_TAKECHARGE					= 3			#充值领取类型
PCU_TAKECHARGEUNITE				= 4			#领取奖品(带订单和不带订单)
PCU_TAKEPRESENTUNITE			= 5			#所有奖品的领取(除充值外)
PCU_TAKECHARGEUNITE_SINGLE		= 6			#一次领取一个物品的（带/不带订单）奖励

#----------------连击---------------------------------------
#连击次数对应连击状态
DOUBLE_HIT_STATE = {			#连击奖励次数要求
	30			: 1,
	100			: 2,
	300			: 3,
	600			: 4,
	999			: 5
}
#连击状态对应持有效果
DOUBLE_HIT_EFFECT = {			#连击奖励持有效果ID（唯一的）
	1			: 101010101,
	2			: 101010102,
	3			: 101010103,
	4			: 101010104,
	5			: 101010105
}

#连击次数重置时间
DOUBLE_HIT_TIME = {
	1			: 5.0,
	2			: 4.0,
	3			: 3.5,
	4			: 3.0,
	5			: 2.0
}

#被连击状态对应持有效果
DOUBLE_BE_HIT_EFFECT = {
	1			: 0,
	2			: 0,
	3			: 0,
	4			: 0,
	5			: 0
}

#技能消耗消息提示
SKILL_REQUIRE_MESSAGE = {
	csstatus.SKILL_OUTOF_MP 	: csstatus.SKILL_TARGET_OUTOF_MP,
	csstatus.SKILL_OUTOF_HP 	: csstatus.SKILL_TARGET_OUTOF_HP,
	csstatus.SKILL_OUTOF_GANGQI : csstatus.SKILL_TARGET_OUTOF_GANGQI,
	csstatus.SKILL_OUTOF_ITEM 	: csstatus.SKILL_TARGET_OUTOF_ITEM
}

#技能条件判断消息提示
SKILL_CONDITION_MESSAGE = {
	"SKILL_PROPERTY_COUNT_FAIL"					: [],
	"SKILL_NOT_PROPERTY_COUNT_FAIL"				: [],
	"SKILL_PROPERTY_PERCENT_FAIL"				: [],
	"SKILL_NOT_PROPERTY_PERCENT_FAIL"			: [],
	"SKILL_DISTANCE_FAIL"						: [],
	"SKILL_PROPERTY_SUBTRACT_FAIL"				: [],
	"SKILL_NOT_PROPERTY_SUBTRACT_FAIL"			: [],
	"SKILL_TARGET_NOT_PROPERTY_SUBTRACT_FAIL"	: [],
	"SKILL_TARGET_NPC_BUFF_COUNT_FAIL"			: [],
	"SKILL_BUFF_COUNT_FAIL"						: [],
	"SKILL_BUFF_LAYER_FAIL"						: [],
	"SKILL_TARGET_NPC_BUFF_LAYER_FAIL"			: [],
	"SKILL_ASSEMBLE_FAIL"						: [],
	"SKILL_NOT_PROPERTY_ASSEMBLE_FAIL"			: [],
	"SKILL_ENEMY_FAIL"							: [],
	"SKILL_NOT_ENEMYLIST_FAIL"					: [],
	"SKILL_NOT_TEAMMEMBERS_FAIL"				: [],
	"SKILL_NOT_CALLMONSTERMBLIST_FAIL"			: [],
	"SKILL_RELATION_ASSEMBLE_FAIL"				: [],
	"SKILL_TYPE_FAIL"							: [],
	"SKILL_ROLE_SCRIPTID_FAIL"					: [],
	"SKILL_NOT_SCRIPTID_FAIL"					: [],
	"SKILL_SCRIPTID_FAIL"						: [],
	"SKILL_COOLDOWN_TIME_FAIL"					: [],
	"SKILL_ROLE_SKILL_POSTURE_FAIL"				: [],
	"SKILL_SKILL_POSTURE_FAIL"					: [],
	"SKILL_DIRECTION_FAIL"						: [],
	"SKILL_BUFF_REPLACE_FAIL"					: [],
	"SKILL_BUFF_EXTRA_FAIL"						: [],
	"SKILL_BUFF_ENERGY_FAIL"					: [],
}

# 角色模型初始化数据
ROLE_INIT_MODULE = {
	1:{
		1:"Long",			# 男战士
		2:"Sword",			# 男剑客
		3:"Whip",			# 男射手
		4:"Fan",			# 男法师
	},
	2:{
		1:"LongFamale",		# 女战士
		2:"SwordFamale",	# 女剑客
		3:"WhipFamale",		# 女射手
		4:"FanFamale",		# 女法师
	}

}

#------------------轮回秘境---------------------------------------
LUN_HUI_MI_JIN_SCRIPTID 	= "L_LHMJ_1"	# 轮回秘境大地图scriptID
DONGFU_MAP_SPACESCRIPTID = {csdefine.SPACE_TYPE_PRIVATE : "L_LHMJDF",
							csdefine.SPACE_TYPE_HIGH_DF : "L_LHMJDF2" }	#洞府\高级洞府对应的scriptID

REFLASH_PROY_TIME			= 15 * 60		# 祈福时间表刷新时间15分钟
REFLASH_PROY_NUM			= 1*24*60*60	# 祈福刷新时间1天
PROY_MAX_NUM				= 10			# 一天只能祈福10次
QUENCHING_EQUIP_MAX_NUM		= 10			# 半成品只能淬炼10次
QUENCHING_EQUIP_COST_ITEMS	= []			# 淬炼消耗物品ID
QUENCHING_EQUIP_COST_ITEM	= 203010017		# 漓泉水 淬炼必要材料
QUENCHING_EQUIP_COST_WEAPON	= 203010018		# 淬炼武器
QUENCHING_EQUIP_COST_ARMOR	= 203010019		# 淬炼防具
QUENCHING_EQUIP_COST_ORNA	= 203010020		# 淬炼饰品
QUENCHING_EQUIP_COST_MONEY	= 10000			# 淬炼消耗金钱
PART_EQUIP_BASE_PROPERTY_RATE = 20			# 半成品基础属性只有原有的20%
PART_EQUIP_QUENCHING_MIN_RATE = 70			# 半成品淬炼一次最低可以提高7%
PART_EQUIP_QUENCHING_MAX_RATE = 90			# 半成品淬炼一次最低可以提高9%

LUN_HUI_MI_JING_SOUME_TIME 	= 60.0			# 阵图 每60秒 消耗一次
LHMJ_CHALLENGE_REFUSE		= 2				# 每周可以拒绝2次挑战
LHMJ_BUILD_OCCUPY_TIME		= 3600			# 轮回秘境有效占领时间
ADD_GUARD_LEVEL				= [3,5]			# 洞府3级、5级分别增加守卫
LHMJ_LUN_PAN_ITEMID			= 303020008		# 轮盘物品ID
KILL_LINGFUXIAOYAO_QUESTID	= { csdefine.SPACE_TYPE_PRIVATE : 71100001,
								csdefine.SPACE_TYPE_HIGH_DF : 71100006 } 		# 建造洞府杀怪任务
BUILD_DONG_FU_QUESTID		= 71100002		# 建造洞府任务
LHMJ_LING_TIAN_INIT_SCRIPT	= ["40000938","40000939","40000940","40000941"]	# 初始灵田scriptID
LHMJ_LING_TIAN_LEVEL_NUM_MAP= {1:4,2:6,3:8,4:10,5:12}	# 灵田等级对应开放的灵田数量
LHMJ_LING_TIAN_SCRIPTS = ["40000938","40000939","40000940","40000941","40000942","40000943",
"40000944","40000945","40000946","40000947","40000948","40000949"]	# 所有的灵田scriptID

DF_PLUNDER_BUILDS = [csdefine.LHMJ_BUIILD_GONG_FANG, 
csdefine.LHMJ_BUIILD_QIAN_KU_DING, csdefine.LHMJ_BUIILD_SHOU_LAN]	# 洞府掠夺战可被掠夺的建筑

#--------------------------练兵场------------------------------------
LBC_LINE_NUM = 10 	#练兵场分线数量
LBC_STATUS_NORMAL = 1 #练兵场未被占领
LBC_STATUS_DELCARED = 2#练兵场被宣战
LBC_STATUS_FIGHT = 3 #练兵场争夺中
LBC_STATUS_OCCUPIED = 4 #练兵场被占领

LBC_MID_COST_MONEY = 50000 #占领中级练兵场需要消耗的金币
LBC_MID_COST_SOLDIER = (4,10) #占领中级练兵场需要消耗的士兵 4：等级 10：数量
LBC_HIGH_COST_MONEY = 100000 #占领高级练兵场需要消耗的金币
LBC_HIGH_COST_SOLDIER = (6, 20) #占领高级练兵场需要消耗的士兵 20个 6级士兵

LBC_DECLARE_TIME_WEEK = [2,5] #周二和周五
LBC_DECLARE_TIME_HOUR = [20] #20点到21点

LBC_SPACE = {
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:["fu_ben_L_LBCZDZPVP", "fu_ben_L_LBCZDZ"],
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL:"fu_ben_L_ZJLBC",
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL:"fu_ben_L_LBCPVP"
}

LBC_FIGHT_REASON_OFFENCE  = 0 #进攻
LBC_FIGHT_REASON_DEFENCE  = 1 #防守
LBC_FIGHT_COUNT_DOWN = 30 #练兵场争夺战倒计时提示
#-------------------------练兵场任务---------------------------------
#各种类型练兵场对应的地图
LBC_TASK_SPACE = {
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:["fu_ben_L_LBCTask1", "fu_ben_L_LBCTask2", "fu_ben_L_LBCTask3"],
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL:["fu_ben_L_LBCTask4", "fu_ben_L_LBCTask5", "fu_ben_L_LBCTask6"],
	csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL:["fu_ben_L_LBCTask7", "fu_ben_L_LBCTask8", "fu_ben_L_LBCTask9"]
	}

LBC_TASK_PROCESSES = 2 #练兵场任务剩余次数

# 帮会争霸报名成功的邮件ID
BHZB_SIGN_UP_SUCCESS_MAIL_ID 	= "100000012"
# 帮会争霸人员参与的邮件ID
BHZB_SIGN_UP_MEB_MAIL_ID 		= "100000013"
#帮会争霸大本营
BHZB_HOME_BARRACKS_SPACE = ["fu_ben_L_BHZB_DBY"]
#帮会争霸报名需要资金
BHZB_SIGN_UP_COST_MONEY	 = 50000
#帮会争霸未能参与的帮会邮件ID
BHZB_NOT_TO_JOIN_TONG_MAIL_ID = "300601013"
# 有资格参加阵营争霸的邮件ID
BHZB_TO_JOIN_CAMP_WAR_MAIL_ID = "300301012"

# 帮会掠夺战即将开始邮件ID
TONG_PLUNDER_START_MAIL_ID	= "100000014"
# 帮会掠夺战人员奖励的邮件ID
TONG_PLUNDER_REWARD_MAIL_ID	= "100000015"

#------------------------CST-11583 手写装备不同心法附加属性----------------------------
# {职业:{心法:[属性1，属性2，...]...}...}
CUSTOM_EQUIP_POSTURE_PROPERTY = {
	0:{	11:{30002, 30008, 30012, 30004, 30001},12:{30001, 30006, 30008, 30010, 30011},
		21:{30003, 30009, 30012, 30004, 30001},22:{30001, 30006, 30003, 30009, 30013},
		31:{30005, 30002, 30008, 30012, 30004},32:{30005, 30002, 30008, 30012, 30004},
		41:{30003, 30009, 30012, 30004, 30001},42:{30003, 30024, 30001, 30006, 30007},
	},
	1:{1:{30002, 30008, 30012, 30004, 30001},2:{30001, 30006, 30008, 30010, 30011}},
	2:{1:{30003, 30009, 30012, 30004, 30001},2:{30001, 30006, 30003, 30009, 30013}},
	3:{1:{30005, 30002, 30008, 30012, 30004},2:{30005, 30002, 30008, 30012, 30004}},
	4:{1:{30003, 30009, 30012, 30004, 30001},2:{30003, 30024, 30001, 30006, 30007}},
}

# 被动技能激活的最大数
ACT_PASSIVE_SKILL_MAX = 5

#------------------------帮会掠夺战----------------------------
#帮会掠夺战参与活动最低等级
TONG_PLUNDER_MIN_TONG_LEVEL = 2
#帮会掠夺战参与活动最大相差等级
TONG_PLUNDER_BOTH_MAX_DIFF_LEVEL = 2


# 随机物品商店刷新时间
RANDOM_REFLASH_TIME_BEGIN		= 10				# 刷新开始时间段
RANDOM_REFLASH_TIME_END			= 22				# 刷新结束时间段
RANDOM_REFLASH_TIME_LAST		= 900				# 持续半小时

#-----------------------大荒战场--------------------------------

DHZC_BOX_REVIVER_TIME_MIN = 180 				#大荒战场宝箱随机刷新时间 最小值
DHZC_BOX_REVIVER_TIME_MAX = 300 				#大荒战场宝箱随机刷新时间 最大值

#-----------------------神通技能--------------------------------
SHENTONG_SKILL_MAX_TIMES = 1000					#PC及幻兽神通技能充能次数上限

#-----------------------5v5阵营竞技-----------------------------

ZYJJ_REWARD_CONTRIBUTION = {3:300, 4:400, 5:500} #帮贡奖励

#---------------------- 每日最大功勋上限-----------------------
FEAT_MAX_AMOUNT = 600
#---------------------- 每日最大军功上限
EXPLOIT_MAX_AMOUNT = 600