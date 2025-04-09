# -*- coding: utf-8 -*-


#-----------------------利用globalData回调进行全局通信key----------------------------

GLOBAL_CHANNEL_KEY_MEMORY_LEAK				=  'CHANNEL_KEY_MEMORY_LEAK'			# 输出内存泄漏
GLOBAL_CHANNEL_KEY_RECORD_ENTITY_NUM		=  'CHANNEL_KEY_RECORD_ENTITY_NUM'		# 给指定客户端返回当前进程信息
GLOBAL_CHANNEL_KEY_OUTPUT_PROCESS_INFOS		=  'CHANNEL_KEY_OUPUT_PROCESS_INFOS'	# 输出错误到日志文件
GLOBAL_CHANNEL_KEY_FIND_ROLE				=  'CHANNEL_KEY_FIND_ROLE'				# 查找role所在的base和cell
GLOBAL_CHANNEL_KEY_HOT_CONST				=  'CHANNEL_KEY_HOT_CONST'				# 所有进程热更新HotConst文件
GLOBAL_CHANNEL_KEY_CALCULATE_SERVER_INFO	=  'CHANNEL_KEY_CALCULATE_SERVER_INFO'	# 统计服务器运行数据



#-----------------------entity type----------------------------（对应的ENTITY_TYPE_DICT，技能目标类型筛选的参数选项清单，定义在csconst.py中）
ENTITY_FLAG_UNKNOWN						= 0			# 未知，未设置
ENTITY_FLAG_ROLE						= 1			# 角色（Role）
ENTITY_FLAG_SPACE						= 2			# 空间
ENTITY_FLAG_MONSTER						= 3			# 怪物（Monster）
ENTITY_FLAG_NPC							= 4			# NPC
ENTITY_FLAG_DOOR						= 5			# 传送门
ENTITY_FLAG_SPELL						= 6			# 施法箱子（SpellBox）
ENTITY_FLAG_TRAP						= 7			# 陷阱（Trap）
ENTITY_FLAG_PLATFORM					= 8			# 移动平台
ENTITY_FLAG_VEHICLEPET					= 9			# 幻兽（Pet）
ENTITY_FLAG_DROP_BOX					= 10		# 掉落箱子
ENTITY_FLAG_GHOST_RECEIVER				= 11		# 技能ghost受术者（Ghost）
ENTITY_FLAG_TELEPORTSTONE				= 12		# 传送石
ENTITY_FLAG_MGR							= 13		# 管理器
ENTITY_FLAG_ACCOUNT						= 14		# 帐号
ENTITY_FLAG_MAX 						= 15		# 特别注意：这个在输出信息时使用，如果需要加请将这个放到最后（QRN）

#----------------------------entityFlagExt二级标识 (标识具体是哪种类型 如果某种entity需要特别标识 请新增标识) --------------------------
ENTITY_FLAG_EXT_UNKNOWN					= 0			# 未设置
ENTITY_FLAG_EXT_ROLE					= 1			# 角色（Role）
ENTITY_FLAG_EXT_SPACE					= 2			# 空间
ENTITY_FLAG_EXT_MONSTER					= 3			# 怪物（Monster）
ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN		= 4			# 替身怪物
ENTITY_FLAG_EXT_NPC						= 5			# NPC
ENTITY_FLAG_EXT_DOOR					= 6			# 传送门
ENTITY_FLAG_EXT_SPELL					= 7			# 施法箱子（SpellBox）
ENTITY_FLAG_EXT_TRAP					= 8			# 陷阱（Trap）
ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP		= 9			# 客户端陷阱
ENTITY_FLAG_EXT_PLATFORM				= 10		# 移动平台
ENTITY_FLAG_EXT_VEHICLEPET				= 11		# 幻兽（Pet）
ENTITY_FLAG_EXT_DROP_BOX				= 12		# 掉落箱子
ENTITY_FLAG_EXT_GHOST_RECEIVER			= 13		# 技能ghost受术者（Ghost）
ENTITY_FLAG_EXT_TELEPORTSTONE			= 14		# 传送石
ENTITY_FLAG_EXT_MOVE_TRAP				= 15		# 移动陷阱
ENTITY_FLAG_EXT_MONSTER_EXT_YXLMSoldier	= 16		# 英雄联盟 小兵
ENTITY_FLAG_MONSTER_CLIENT_BASE			= 17		# 客户端往服务器同步的Monster
ENTITY_FLAG_EXT_MONSTER_EXT_JUMP		= 18		# 跳跃怪物
ENTITY_FLAG_MONSTER_STEAL_TREASURE		= 19		# 拾取宝物怪物(客户端)
ENTITY_FLAG_EXT_MONSTER_EXT_INTERACTIVE	= 20		# 可交互怪物
ENTITY_FLAG_EXT_MONSTER_EXT_SFMJ		= 21		# 神风秘境 -- F键交互怪物
ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD		= 22		# 勇闯绝命岛 Boss
ENTITY_FLAG_MONSTER_FOLLOW_ROLE			= 23		# 客户端AI测试怪(跟随玩家)
ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT		= 24 		# 客户端控制怪物
ENTITY_FLAG_EXT_MONSTER_EXT_QQRYJ		= 25		# 巧取熔岩晶怪物
ENTITY_FLAG_EXT_MONSTER_EXT_ATTACK_LADDER= 26		# 攻城梯
ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER= 27		# 云梯
ENTITY_FLAG_EXT_MONSTER_EXT_ORIGIN_PET	 = 28		# 原兽
ENTITY_FLAG_EXT_MONSTER_OPTIMIZE			= 29		#优化类型怪物
ENTITY_FLAG_EXT_MONSTER_EXT_COLLISION_CAR= 30 		# 撞车
ENTITY_FLAG_EXT_TRAP_BATTLEFLAG 		= 31 		# 战旗
ENTITY_FLAG_EXT_MONSTER_COMMANDER 		= 32		# 指挥官类型小怪
ENTITY_FLAG_EXT_MONSTER_SOLDIER 		= 33		# 士兵小怪
ENTITY_FLAG_EXT_TRAP_BARRACKS 			= 34		# 兵营
ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND 	= 35		# 练兵场
ENTITY_FLAG_EXT_NPC_POINT			 	= 35		# 据点
ENTITY_FLAG_EXT_MONSTER_EXT_MENU		= 36		# 带菜单怪物
ENTITY_FLAG_EXT_MONSTER_EXT_JDCY		= 37		# 禁地采药怪物
ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY		= 38		# 火炮
ENTITY_FLAG_EXT_MONSTER_EXT_CALL		= 39		# callMonster
ENTITY_FLAG_EXT_MONSTER_EXT_COVER		= 40		# 轮回秘境保护罩
ENTITY_FLAG_EXT_FENSHEN					= 41		# 分身怪物
ENTITY_FLAG_EXT_TONG_DROPBOX			= 42		# 帮会宝箱
ENTITY_FLAG_EXT_TEAM_DROPBOX			= 43		# 队伍宝箱

#带state属性的entity需要加入此集合
ENTITY_FLAG_WITH_STATE                  = [ENTITY_FLAG_ROLE, ENTITY_FLAG_MONSTER, ENTITY_FLAG_TRAP, ENTITY_FLAG_VEHICLEPET]

#---------------------怪物类型---------------------------------
MONSTER_TYPE_MONSTER					= 1			# monster
MONSTER_TYPE_MONSTER_EXT_CALL			= 2			# monsterExtCall

#---------------------陷阱类型---------------------------------
TRAP_TYPE_TRAP							= 1			# trap
TRAP_TYPE_SPACEDOOR						= 2			# SpaceDoor

# 战斗entity flag集合
COMBAT_ENTITY_FLAG_LIST = [ENTITY_FLAG_ROLE, ENTITY_FLAG_MONSTER, ENTITY_FLAG_VEHICLEPET, ENTITY_FLAG_GHOST_RECEIVER]

#-----------------------space-----------------------------------
SPACE_TYPE_NORMAL						= 0					# 缺省值
SPACE_TYPE_MULTILINE					= 1			# 多线地图
SPACE_TYPE_PLANE						= 2			# 位面
SPACE_TYPE_COPY							= 3			# 副本
SPACE_TYPE_POTENTIAL					= 4			# 潜能副本
SPACE_TYPE_CHUAN_CHENG					= 5			# 传承副本
SPACE_TYPE_STORY_COPY					= 6			# 剧情副本
SPACE_TYPE_JAIL							= 7			# 监狱
SPACE_TYPE_TONG							= 8			# 帮会地图
SPACE_TYPE_HOME_BARRACKS 				= 9			# 帮会争霸大本营
SPACE_TYPE_TONG_TIAN_TA					= 10		# 通天塔副本
SPACE_TYPE_DONG_FU						= 11		# 洞府
SPACE_TYPE_JSSLC_CHANCE_COPY			= 12		# 晶石狩猎场机缘副本


SPACE_CHILD_TYPE_SPAR_HUNTING			= 100		# 晶石狩猎场
SPACE_CHILD_TYPE_SFC					= 101		# 至尊争霸第一场 十方成
SPACE_CHILD_TYPE_YZFQ					= 102		# 至尊争霸第二场 血斗凤栖镇
SPACE_CHILD_TYPE_BHZB					= 103		# 帮会争霸
SPACE_CHILD_TYPE_YXLM					= 104		# 英雄王座
SPACE_CHILD_TYPE_JSZZ					= 105		# 金树种子
SPACE_CHILD_TYPE_YCJMD					= 106		# 勇闯绝命岛
SPACE_CHILD_TYPE_GCZ 					= 107		# 攻城战
SPACE_CHILD_TYPE_LBC					= 108		# 练兵场
SPACE_TYPE_CHILD_HOME_BARRACKS 			= 109		# 大本营
SPACE_TYPE_CHILD_STAND_MAP 				= 110 		# 沙盘大地图
SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS 	= 111		# 帮会争霸大本营
SPACE_TYPE_CHILD_BHZB_STAND_MAP 		= 112		# 帮会争霸沙盘大地图
SPACE_TYPE_CHILD_TONG_PLUNDER 		= 113		#帮会掠夺战


#活动集合，用于脱离卡死功能，每加一个新活动需要添加到集合里
SPACE_TYPE_ACTIVITY_LIST = [SPACE_CHILD_TYPE_SPAR_HUNTING,]


#bunch space type
SPACE_BUNCH_TYPE_NORMAL					= 0			# 普通副本串
SPACE_BUNCH_TYPE_POTENTAIL				= 1			# 潜能副本串
SPACE_BUNCH_TYPE_CHUANCHENG				= 2			# 传承副本串

#space belong
SPACE_BELONG_NORMAL						= 0			# 缺省值，不属于任何组人或者玩家
SPACE_BELONG_PERSON						= 1			# 单个玩家
SPACE_BELONG_TEAM						= 2			# 队伍玩家
SPACE_BELONG_TONG						= 3			# 帮会玩家

#-----------------------chat---------------------------------
#chat type
CHAT_TYPE_NEARBY						= 0			# 附近
CHAT_TYPE_SPACE							= 1			# 地图
CHAT_TYPE_WORLD							= 2			# 世界
CHAT_TYPE_WHISPER						= 3			# 密语
CHAT_TYPE_GROUP							= 4			# 讨论组
CHAT_TYPE_TEAM							= 5			# 队伍
CHAT_TYPE_COLLECTIVE					= 6			# 团队
CHAT_TYPE_GANG							= 7			# 帮会
CHAT_TYPE_ALIANCE						= 8			# 联盟
CHAT_TYPE_SCHOOL						= 9			# 门派
CHAT_TYPE_CAMP							= 10		# 阵营
CHAT_TYPE_BATTLESPACE					= 11		# 战场
CHAT_TYPE_TIANYIN						= 12		# 天音
CHAT_TYPE_XIANYIN						= 13		# 仙音
CHAT_TYPE_SYSTEM						= 14		# 系统
CHAT_TYPE_FRIEND						= 15		# 好友

CHAT_SYSTEM_WORLD						= 0
CHAT_SYSTEM_SPACE						= 1
CHAT_SYSTEM_PRIVATE						= 2

CHAT_MONSTER_SPACE						= 0
CHAT_MONSTER_NEARBY						= 1
CHAT_MONSTER_PRIVATE					= 2

CHAT_NEARBY_RANGE						= 50.0

#--------------------禁言原因-----------------------------
CHAT_FORBID_NONE						= 0
CHAT_FORBID_GM							= 1			# 通过GM工具禁言

#-----------------------gossip---------------------------------
#对话选项类型
GOSSIP_TYPE_NORMAL_TALKING				= 0			# 普通对话类型
GOSSIP_TYPE_CAN_ACCEPT_QUEST			= 1			# 可接受任务类型
GOSSIP_TYPE_COMPLETE_QUEST				= 2			# 已完成任务类型
GOSSIP_TYPE_NOT_COMPLETE_QUEST			= 3			# 未完成任务类型
GOSSIP_TYPE_CAN_ACCEPT_TONG_DAILY_QUEST	= 4			# 帮会日常可接受任务类型
GOSSIP_TYPE_COMPLETE_TONG_DAILY_QUEST	= 5			# 帮会日常已完成任务类型
GOSSIP_TYPE_NOT_COMPLETE_TONG_DAILY_QUEST= 6		# 帮会日常未完成任务类型

#---------------------KITBAG--------------------------------------
EQUIP_KITBAG_START_INDEX				= 0			# 装备起始位置
EQUIP_KITBAG_END_INDEX					= 31		# 装备中止位置
COMMON_KITBAG_START_INDEX				= 32		# 普通背包起始位置
COMMON_KITBAG_END_INDEX					= 255		# 普通背包中止位置
QUEST_KITBA_START_INDEX					= 256		# 任务背包起始位置
QUEST_KITBAG_END_INDEX					= 383		# 任务背包中止位置
SPAR_KITBAG_START_INDEX					= 384		# 晶石背包起始位置
SPAR_KITBAG_END_INDEX					= 511		# 晶石背包中止位置

#------------------------relationship-------------------------------
# 关系
ROLE_RELATION_FRIEND					= 0x0001	# 玩家好友关系
ROLE_RELATION_BLACKLIST					= 0x0002	# 玩家黑名单关系
ROLE_RELATION_FOE						= 0x0004	# 玩家仇人关系
ROLE_RELATION_LAST_CHAT					= 0x0008	# 玩家最近联系人

# leave type
LEAVE_GROUP_TYPE_NORMAL					= 0			# 自己申请离开讨论组
LEAVE_GROUP_TYPE_PASSIVE				= 1			# 被请离讨论组

# 好友分组
RELATION_CATALOG_TYPE_FOE_LIST			= -2		# 仇人分组
RELATION_CATALOG_TYPE_BLEACK_LIST		= -1		# 黑名单分组
RELATION_CATALOG_TYPE_LASTTIME_LIST		= 0			# 最近联系人分组
RELATION_CATALOG_TYPE_FRIEND_LIST		= 1			# 好友分组

# 讨论组 延期
GROUP_END_TIME_NONE						= 0			# 无限制
GROUP_END_TIME_ONE_MONTH				= 1			# 30天
GROUP_END_TIME_TWO_MONTH				= 2			# 60天
GROUP_END_TIME_THREE_MONTH				= 3			# 90天

#------------------物品添加，删除，更新原因---------------------
ITEM_ADD_BY_PICKUP						= 0			# 拾取增加物品
ITEM_ADD_BY_SYS							= 1			# 系统赠送
ITEM_ADD_BY_NPCTRADE					= 2			# NPC处购买
ITEM_ADD_BY_ROLETRADE					= 3			# 玩家交易
ITEM_ADD_BY_QUEST						= 4			# 任务奖励获得物品
ITEM_ADD_BY_QUESTACTION					= 5			# 任务行为获得物品
ITEM_ADD_BY_GM_COMMAND					= 6			# GM添加物品
ITEM_ADD_BY_SKILL						= 7			# 技能添加物品
ITEM_ADD_BY_BORN_GAIN					= 8			# 出生赋值
ITEM_ADD_BY_ADDCHECK					= 9			# 添加物品检测，并不会添加物品
ITEM_ADD_BY_STALLTRADE					= 10		# 摆摊
ITEM_ADD_BY_USE_GIFT_ITEM				= 11		# 打开礼包
ITEM_ADD_BY_SHOPMALLTRADE				= 12		# 商城处购买
ITEM_ADD_BY_OPEN_SPELLBOX				= 13		# 打开宝箱
ITEM_ADD_BY_SPELLBOX_KEY				= 14		# 特殊获得宝箱钥匙
ITEM_ADD_BY_SPACE_ACTION				= 15		# 副本行为
ITEM_ADD_BY_SPACE_SENTLEMENT			= 16		# 副本结算
ITEM_ADD_BY_TONG_STORE					= 17		# 帮会仓库
ITEM_ADD_BY_TONG_SALARY					= 18		# 帮会俸禄
ITEM_ADD_BY_STORE						= 19		# 个人仓库取物品
ITEM_ADD_BY_MAIL						= 20		# 邮件
ITEM_ADD_BY_NEW_PLAYER_GIFT				= 21		# 新手奖励
ITEM_ADD_BY_SIGN_IN_GIFT				= 22		# 签到奖励
ITEM_ADD_BY_SPLIT						= 23		# 分割物品
ITEM_ADD_BY_COMPOSE						= 24		# 打造装备
ITEM_ADD_BY_TAKEPRESENT					= 25		# 运营活动奖励，当前包括来自于“custom_ChargePresentUnite”和“custom_ItemAwards”表的奖励。
ITEM_ADD_BY_EVOULATION_PET				= 26		# 原兽进化得幻兽蛋
ITEM_ADD_BY_STORE_TOOL					= 27		# 从轮回秘境储物柜取物品
ITEM_ADD_BY_ADD_JADE					= 28		# 玲珑玉令获得
ITEM_ADD_BY_MONSTER_AI					= 29		# ai添加物品
ITEM_ADD_BY_TALKING						= 30		# 对话添加物品
ITEM_ADD_BY_JADE_UPGRADE				= 29		# 玉玦升级添加

ITEM_REMOVE_BY_USE						= 0			# 使用后删除
ITEM_REMOVE_BY_DROP						= 1			# 玩家主动丢弃
ITEM_REMOVE_BY_EQUIP_INTENSIFY			= 2			# 装备强化
ITEM_REMOVE_BY_EQUIP_BACKFIRE			= 3			# 装备回火
ITEM_REMOVE_BY_INTENSIFY_SAVE			= 4			# 装备保存
ITEM_REMOVE_BY_INTENSIFY_RESTORE		= 5			# 装备还原
ITEM_REMOVE_BY_QUESTACTION				= 6			# 任务行为删除
ITEM_REMOVE_BY_SELL						= 7			# 出售
ITEM_REMOVE_BY_ROLETRADE				= 8			# 交易
ITEM_REMOVE_BY_RETURN					= 9			# 退货
ITEM_REMOVE_BY_SPACE_EVENT				= 10		# 副本剧情
ITEM_REMOVE_BY_SORTSTACK				= 11		# 背包在整理的时候，叠加物品，有时会删除一些
ITEM_REMOVE_BY_SWAPITEM					= 12		# 交换由于叠加造成删除物品
ITEM_REMOVE_BY_SPAR_FAIL				= 13		# 炼化晶核失败删除
ITEM_REMOVE_BY_SPELL_BOX				= 14		# 场景物件交互 移除物品
ITEM_REMOVE_BY_STORE					= 15		# 个人仓库存物品
ITEM_REMOVE_BY_SKILL					= 16		# 使用技能消耗物品
ITEM_REMOVE_BY_SHUFFLE					= 17		# 装备洗练
ITEM_REMOVE_BY_RECAST					= 18		# 装备重铸
ITEM_REMOVE_BY_BIOGRAPHY				= 19		# 装备传星
ITEM_REMOVE_BY_MAIL						= 20		# 邮件
ITEM_REMOVE_BY_STORE_SORTSTACK			= 21		# 仓库相关操作，叠加物品
ITEM_REMOVE_BY_SELL_TO_NPC				= 22		# 出售给NPC
ITEM_REMOVE_BY_COMPOSE					= 23		# 装备打造
ITEM_REMOVE_BY_SYS						= 24		# 系统删除
ITEM_REMOVE_BY_LIMIT_TIME				= 25		# 物品到时间自动销毁
ITEM_REMOVE_BY_CHAT 					= 26		# 聊天(天音和仙音)
ITEM_REMOVE_BY_PLANT					= 27		# 种植
ITEM_REMOVE_BY_UNLOCK_GRID				= 28		# 解锁背包格子
ITEM_REMOVE_BY_JADE_UPGRADE				= 29		# 玉玦升级
ITEM_REMOVE_BY_JADE_DEVOUR				= 30		# 玉玦吞噬
ITEM_REMOVE_BY_GM						= 100		# GM指令删除物品


#使用道具行为类型
PROP_USE_TYPE_DICT = [ITEM_REMOVE_BY_USE, ITEM_REMOVE_BY_EQUIP_INTENSIFY, ITEM_REMOVE_BY_EQUIP_BACKFIRE,  ITEM_REMOVE_BY_INTENSIFY_SAVE,
	ITEM_REMOVE_BY_INTENSIFY_RESTORE, ITEM_REMOVE_BY_SKILL, ITEM_REMOVE_BY_SHUFFLE, ITEM_REMOVE_BY_RECAST, ITEM_REMOVE_BY_BIOGRAPHY,
	ITEM_REMOVE_BY_COMPOSE, ITEM_REMOVE_BY_CHAT, ITEM_REMOVE_BY_PLANT, ITEM_REMOVE_BY_UNLOCK_GRID, ITEM_REMOVE_BY_JADE_UPGRADE,]

# 物品移除与绑定类型相关
ITEM_REMOVE_BY_IS_BIND					= 0			# 优先消耗绑定物品，再消耗无绑定物品
ITEM_REMOVE_BY_NOT_BIND					= 1			# 优先消耗无绑定物品，再消耗绑定物品
ITEM_REMOVE_BY_ONLY_IS_BIND				= 2			# 只消耗绑定物品
ITEM_REMOVE_BY_ONLY_NOT_BIND			= 3			# 只消耗无绑定物品
#----------------------------阵营------------------------------
CMAP_NONE								= 0			# 不区分仙魔
CAMP_TAOSIM								= 1			# 仙道
CAMP_DEMON								= 2			# 魔道
CAMP_NEUTRAL_ENEMY						= 3			# 中立敌对（怪物特有）
CAMP_NEUTRAL_NORMAL						= 4			# 中立友好（怪物特有）

CAMP_LIST = [ CAMP_TAOSIM, CAMP_DEMON, CAMP_NEUTRAL_ENEMY, CAMP_NEUTRAL_NORMAL ]

#----------------------------职业------------------------------
CLASS_UNKNOWN							= 0			# 未知
CLASS_FIGHTER							= 1			# 战士
CLASS_SWORDMAN							= 2			# 剑客
CLASS_ARCHER							= 3			# 射手
CLASS_MAGE								= 4			# 法师
CLASS_PALADIN							= 5			# 强防型战士（NPC专用）

#---------------------------性别-------------------------------
MALE									= 1			# 男性
FEMALE									= 2			# 女性

ENTITY_CREATE_TYPE_UN_KNOE				= 0			# 未知
ENTITY_CREATE_TYPE_DIRECT				= 1			# 直接创建
ENTITY_CREATE_TYPE_SPAWN_POINT			= 2			# 刷新点创建

#---------------------场景中各区域的标志-----------------------------
SCENE_AREA_FLAG_DEFAULT					= 1			# 场景导航框默认
SCENE_AREA_FLAG_DOOR					= 2			# 门
SCENE_AREA_FLAG_WALL					= 3			# 墙
SCENE_AREA_FLAG_DEFAULT_4				= 4			# 待定
SCENE_AREA_FLAG_DEFAULT_5				= 5			# 待定
SCENE_AREA_FLAG_DEFAULT_6				= 6			# 待定
SCENE_AREA_FLAG_DEFAULT_7				= 7			# 待定
SCENE_AREA_FLAG_DEFAULT_8				= 8			# 待定
SCENE_AREA_FLAG_DEFAULT_9				= 9			# 待定
SCENE_AREA_FLAG_DEFAULT_10				= 10		# 待定
SCENE_AREA_FLAG_DEFAULT_11				= 11		# 待定
SCENE_AREA_FLAG_DEFAULT_12				= 12		# 待定
SCENE_AREA_FLAG_DEFAULT_13				= 13		# 待定
SCENE_AREA_FLAG_DEFAULT_14				= 14		# 待定
SCENE_AREA_FLAG_DEFAULT_15				= 15		# 待定
SCENE_AREA_FLAG_DEFAULT_16				= 16		# 待定

#---------------------移动类型------------------------
MOVE_TYPE_STOP							= 0			# 处于没有移动中
MOVE_TYPE_NAVIGATE_POINT				= 1			# 处于向指定点移动
MOVE_TYPE_MOVE_POINT					= 2			# 处于向指定点移动
MOVE_TYPE_CHASE							= 3			# 处于追击目标移动
MOVE_TYPE_PATROL						= 4			# 处于巡逻移动
MOVE_TYPE_RANDOM						= 5			# 处于随机移动
MOVE_TYPE_WANDER						= 6			# 处于游荡移动
MOVE_TYPE_WALK_AROUND					= 7			# 处于游走移动
MOVE_TYPE_CHARGE						= 8			# 处于冲锋移动
MOVE_TYPE_GOBACK						= 9			# 处于回走移动
MOVE_TYPE_LOOP_ROTATOR					= 10		# 转圈
MOVE_TYPE_SKILL_CHASE					= 11		# 处于使用技能跟随移动
MOVE_TYPE_HIT_BACK						= 12		# 被击飞/击退
MOVE_TYPE_RANDOM_CHOICE_FORM_LIST		= 13		# 从列表里随机取点移动
MOVE_TYPE_FIGHT_DISPERSE				= 14		# 小怪物追击及散开表现
MOVE_TYPE_JUMP							= 15		# 跳跃移动
MOVE_TYPE_CHASE_CLIENT					= 16		# 防重叠追击移动
MOVE_TYPE_REVERSE_PATROL				= 17		# 处于反向巡逻移动
MOVE_TYPE_NAVIGATE_POINT_TEST			= 18		# 处于向某个点寻路移动
MOVE_TYPE_SOLDIER_FOLLOW 				= 19 		# 士兵跟随移动
MOVE_TYPE_SOLDIER_RECT 					= 20 		# 士兵矩形列阵移动
MOVE_TYPE_SOLDIER_CIRCLE 				= 21 		# 士兵列阵圆形移动
MOVE_TYPE_RANDOM_IN_SPHERE				= 22		# 在球体里移动
MOVE_TYPE_FLY_TO_POINT					= 23		# 空中移动到某一点
MOVE_TYPE_SKILL_JUMP					= 24		# 跳扑技能移动


PERFORMANCE_PASSIVITY_MOVE				= 0			# 被动表现级别移动
SYSTEM_MOVE								= 1			# 系统级别移动（优先级最高）
PERFORMANCE_INITIATIVE_MOVE				= 2			# 主动表现级别移动
NORMAL_MOVE								= 3			# 普通级别移动（优先级最低）

#小怪物追击及散开表现
MOVING_FIGHT_DISPERSE_STYLE_CHASE		= 1			# 追击
MOVING_FIGHT_DISPERSE_STYLE_WANDER		= 2			# 靠近或游走
MOVING_FIGHT_DISPERSE_STYLE_AWAY		= 3			# 远离

#--------------------巡逻移动模式-----------------------
MOVE_PATROL_MODE_NAVIGATE_POSITION				= 1			# 通过寻路导航巡逻
MOVE_PATROL_MOVE_GOTO_POSITION					= 2			# 通过直接移动到巡逻目标点
MOVE_PATROL_MODE_NAVIGATE_POSITION_NOT_FACE		= 3			# 通过寻路导航巡逻,(无面向)
MOVE_PATROL_MODE_GOTO_POSITION_NOT_FACE			= 4			# 通过直接移动到巡逻目标点(无面向)

#---------------------------幻兽------------------------
# 幻兽品质
VEHICLE_PET_QUALITY_NORMAL				= 1			# 凡兽
VEHICLE_PET_QUALITY_SPIRIT				= 2			# 灵兽
VEHICLE_PET_QUALITY_IMMORTAL			= 3			# 仙兽
VEHICLE_PET_QUALITY_HOLY				= 4			# 圣兽
VEHICLE_PET_QUALITY_DEITY				= 5			# 神兽

#幻兽回收方式
PET_WITHDRAW_COMMON						= 1			# 正常回收
PET_WITHDRAW_DEATH						= 2			# 因血量为零死亡回收
PET_WITHDRAW_CONJURE					= 3			# 激活其他宠物时收回当前宠物
PET_WITHDRAW_MOUNT_PET					= 4			# 骑上宠物收回
PET_WITHDRAW_OWNER_DEATH				= 5			# 所属玩家死亡回收
PET_WITHDRAW_OFFLINE					= 6			# 离线回收
PET_WITHDRAW_FLYTELEPORT				= 7			# 飞翔传送回收
PET_WITHDRAW_GMWATCHER					= 8			# 设置GM观察者回收
PET_WITHDRAW_CHANGE_BODY				= 9			# 变身状态回收
PET_WITHDRAW_STALL						= 10		# 摆摊回收
PET_WITHDRAW_ENTER_FENCE				= 11		# 出战幻兽入栏
PET_WITHDRAW_EXCHANGE_FROM_FENCE		= 12		# 出战幻兽入栏，兽栏幻兽出栏(交换)

#幻兽成长度生成方案
PET_ABILITY_CASE_NORMAL_QUALITY			= 1			# 凡兽蛋
PET_ABILITY_CASE_SPIRIT_QUALITY			= 2			# 灵兽蛋
PET_ABILITY_CASE_HOLY_QUALITY			= 3			# 圣兽蛋
PET_ABILITY_CASE_DEITY_QUALITY			= 4			# 神兽蛋
PET_ABILITY_CASE_NORMAL_RESTORE			= 5			# 凡兽还童
PET_ABILITY_CASE_SPIRIT_RESTORE			= 6			# 灵兽还童
PET_ABILITY_CASE_HOLY_RESTORE			= 7			# 圣兽还童
PET_ABILITY_CASE_DEITY_RESTORE			= 8			# 神兽还童

#幻兽封印符
PET_SEAL_CHARM_ITEMID					= 204020001			# 幻兽封印符物品ID
#仙灵果
PET_COMPOSE_XIANLINGGUO					= 204020002			# 幻兽合成材料ID
#还童丹
PET_ENVOLUTION_ITEMID					= 204020004			# 原兽进化

#获得幻兽原因
PET_ADD_REASON_DEFAULT					= 0			# 默认
PET_ADD_REASON_COMPLETE_QUEST			= 1			# 完成任务获得
PET_ADD_REASON_KILL_PETMONSTER			= 2			# 击杀幻兽怪物获得

#失去幻兽的原因
PET_REMOVE_REASON_FREE					= 1			# 放生

#拾取幻兽原因
PET_DEL_REASON_DEFAULT					= 0			# 默认

#----------------------技能/buff-----------------------
#技能对象entity类型
SKILL_TARGET_OBJECT_NONE				= 0
SKILL_TARGET_OBJECT_ENTITY				= 1
SKILL_TARGET_OBJECT_POSITION			= 2

#技能施展方式
SKILL_CAST_OBJECT_TYPE_NONE				= "TargetNothing"	# 不需要目标和位置;
SKILL_CAST_OBJECT_TYPE_ENTITY			= "TargetLock"		# 对目标Entity施展;
SKILL_CAST_OBJECT_TYPE_POSITION			= "TargetPosition"	# 对位置施展;

#最大施法距离
SKILL_CAST_RANGE_MAX					= 99999999.0	# 修改时请更新客户端对应常量值

#命中类型
SKILL_HIT_TYPE_DIRECT					= "HitDirect"		# 直接命中
SKILL_HIT_TYPE_DODGE					= "HitDodge"		# 判断闪避
#命中结果
SKILL_HIT_SUCCEED						= 0			# 命中成功
SKILL_HIT_FAILED						= 1			# 命中失败
SKILL_HIT_ERROR							= 2			# 命中错误

#技能伤害类型
DAMAGE_TYPE_VOID						= 0x00000001		# 2^0	无类型伤害（此值一般只用于伤害反弹类型和护盾吸收类型）
DAMAGE_TYPE_PHYSICS						= 0x00000002		# 2^1	物理伤害
DAMAGE_TYPE_MAGIC						= 0x00000004		# 2^2	法术伤害
DAMAGE_TYPE_ICE							= 0x00000008		# 2^3	冰元素伤害
DAMAGE_TYPE_FIRE						= 0x00000010		# 2^4	火元素伤害
DAMAGE_TYPE_THUNDER						= 0x00000020		# 2^5	雷元素伤害
DAMAGE_TYPE_XUAN						= 0x00000040		# 2^6	玄元素伤害

# 技能打击范围 单位基准
SKILL_HIT_AREA_UNIT_ABSOLUTE			= 0 		# 绝对坐标(0,0,0) 
SKILL_HIT_AREA_UNIT_CASTER				= 1			# 施法者单位
SKILL_HIT_AREA_UNIT_TARGET				= 2			# 施法目标单位

# 技能打击结果类型
SKILL_HIT_OFFSET_RESULT					= 0 		# 结果偏移
SKILL_HIT_OFFSET_START					= 1			# 起点偏移
SKILL_HIT_OFFSET_END					= 2			# 起点偏移

# 技能打击范围 朝向
SKILL_HIT_AREA_DIRE_ABSOLUTE			= 0			# 绝对方向(0,0,0) 
SKILL_HIT_AREA_DIRE_CASTER				= 1			# 施法者单位（当前朝向）
SKILL_HIT_AREA_DIRE_TARGET				= 2			# 施法目标单位（当前朝向）
SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET	= 3			# 施法者->施法目标（2D朝向）
SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER	= 4			# 施法目标->施法者（2D朝向）
SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET_3D	= 5			# 施法者->施法目标（3D朝向）
SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER_3D	= 6			# 施法目标->施法者（3D朝向）


#buff保存类型
BUFF_OFFLINE_SAVE_TYPE_NULL				= "NotSave"			# 不保存
BUFF_OFFLINE_SAVE_TYPE_CONTINUE			= "ContinueTime"	# 保存继续计时
BUFF_OFFLINE_SAVE_TYPE_NOT_CONTINUE		= "NotContinueTime"	# 保存不继续计时
BUFF_OFFLINE_SAVE_TYPE_AGAIN			= "AgainTime"		# 上线重新计时

#碰撞类型
COLLISION_DEFAULT						= 0			# 默认碰撞
COLLISION_ENEMY							= 1			# 碰撞敌对单位

#技能效果作用类型
SKILL_EFFECT_TYPE_POSITIVE				= 0			# 正作用
SKILL_EFFECT_TYPE_REACTION				= 1			# 反作用
SKILL_EFFECT_TYPE_DIDE					= 2			# 副作用
SKILL_EFFECT_TYPE_CATALYSIS				= 3			# 催化作用

#击退BUFF
#击退类型
BUFF_HIT_TYPE_CASTER_FORWARD			= 0			# 施法者当前方向
BUFF_HIT_TYPE_CASTER_REAR				= 1			# 施法者反方向
BUFF_HIT_TYPE_CATORE_FORWARD			= 2			# 施法者->受术者当前方向
BUFF_HIT_TYPE_CATORE_REAR				= 3			# 施法者->受术者反方向
BUFF_HIT_TYPE_RECEIVER_FORWARD			= 4			# 受术者当前方向
BUFF_HIT_TYPE_RECEIVER_REAR				= 5			# 受术者反方向

#目标朝向类型
BUFF_HIT_TYPE_CASTER_DIRECTION			= 0			# 施法者当前朝向
BUFF_HIT_TYPE_CASTER_RDIRECTION			= 1			# 施法者反朝向
BUFF_HIT_TYPE_CATORE_DIRECTION			= 2			# 施法者->受术者当前朝向
BUFF_HIT_TYPE_CATORE_RDIRECTION			= 3			# 施法者->受术者反朝向
BUFF_HIT_TYPE_RECEIVER_DIRECTION		= 4			# 受术者当前朝向
BUFF_HIT_TYPE_RECEIVER_RDIRECTION		= 5			# 受术者反朝向

#技能学习  技能类型
SKILL_CLASSS_NONE						= 0			# 通用技能
SKILL_CLASSS_CHANGE_POSTURE				= 1			# 切换心法技能
SKILL_CLASSS_POSTURE					= 2			# 心法技能


#心法状态
SKILL_POSTURE_NONE						= 0			# 无心法
SKILL_POSTURE_FIGHTER_ONE				= 101		# 战士1（天怒）
SKILL_POSTURE_FIGHTER_TWO				= 102		# 战士2（神威）
SKILL_POSTURE_SWORDMAN_ONE				= 201		# 剑客1（幻剑）
SKILL_POSTURE_SWORDMAN_TWO				= 202		# 剑客2（天剑）
SKILL_POSTURE_ARCHER_ONE				= 301		# 刺客1（九幽）
SKILL_POSTURE_ARCHER_TWO				= 302		# 刺客2（雷鸣）
SKILL_POSTURE_MAGE_ONE					= 401		# 法师1（寒霜）
SKILL_POSTURE_MAGE_TWO					= 402		# 法师2（神逸）


# 冲突优先级
BUFF_CONFLICT_PRIORITY_NONE 			= 0 		# 无优先级
BUFF_CONFLICT_PRIORITY_PERF 			= 1			# 表现级
BUFF_CONFLICT_PRIORITY_FUC 				= 2			# 功能级
BUFF_CONFLICT_PRIORITY_SCENE 			= 3			# 场景级
BUFF_CONFLICT_PRIORITY_SYS 				= 4			# 系统级


# buff冲突类型
BUFF_CONFLICT_TYPE_NONE					= 0					# 无
BUFF_CONFLICT_TYPE_MODEL				= 0x00000001		# 模型类
BUFF_CONFLICT_TYPE_MODE					= 0x00000002		# 操作模式类
BUFF_CONFLICT_TYPE_BAR					= 0x00000004		# 快捷栏类
BUFF_CONFLICT_TYPE_MATERIAL				= 0x00000008		# 材质特效类



# ------------------------------AI--------------------------------------
# ai类型
AI_TYPE_STATE		= 1
AI_TYPE_EVENT		= 2

#单位事件
#entityevent
ENTITY_EVENT_ENEMY_CHANGED				= 1			# 战斗列表被改变
ENTITY_EVENT_DAMAGE_CHANGED				= 2			# 伤害列表被改变
ENTITY_EVENT_CURE_CHANGED				= 3			# 治疗列表被改变
ENTITY_EVENT_FRIEND_CHANGED				= 4			# 友方列表被改变
ENTITY_EVENT_ATTACKER_REMOVE			= 5			# 当前攻击对象被移出敌人列表时(死亡，不在视野，找不到等)
ENTITY_EVENT_HP_CHANGE					= 6			# 生命值改变
ENTITY_EVENT_MP_CHANGE					= 7			# 魔法值改变
ENTITY_EVENT_ENTER_ATTACK_RANGE			= 8			# 进入主动攻击范围事件
ENTITY_EVENT_COMMAND					= 9			# 接收到命令
ENTITY_EVENT_ENTITY_STATE_CHANGE		= 10		# entity状态改变
ENTITY_EVENT_OUT_OF_TERRITORY			= 11		# 有entity离开主动反应陷阱范围
ENTITY_EVENT_TRIGGER_PROXIMITY			= 12		# 触发主动反应陷阱事件
ENTITY_EVENT_DESTORY_SELF				= 13		# 自身销毁事件
ENTITY_EVENT_SKILL_SUCCESSFUL			= 14		# 技能释放成功
ENTITY_EVENT_SKILL_FAILURE				= 15		# 技能释放失败
ENTITY_EVENT_ON_WITNESSED				= 16		# 自身进入视野
ENTITY_EVENT_ON_LEFT_MOUSE_DOUBLE_CLICK	= 17		# entity被鼠标左键双击事件（MonsterExtClick）
ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER		= 18		# 与怪物对话事件（MonsterExtClick\MonsterExtClickAndModel）
ENTITY_EVENT_ACTIVE_LEAVE_BATTLE		= 19		# 离开区域就自动脱战
ENTITY_EVENT_GANG_QI_CHANGE				= 20		# 罡气状态改变
ENTITY_EVENT_ON_ENTER_FREE				= 21		# 进入自由状态
ENTITY_EVENT_ON_ENTER_FIGHT				= 22		# 进入战斗状态
ENTITY_EVENT_ON_CHANGE_MOVE_TYPE		= 23		# 移动类型改变
ENTITY_EVENT_STOP_PLAY_SOUND			= 24		# 语音/镜头停止播放事件
ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE	= 25		# 特殊属性改变触发事件
ENTITY_EVENT_ON_PLAYER_BEGIN_PUSH		= 26		# 玩家开始推MonsterExtQQRYJ事件
ENTITY_EVENT_ON_PLAYER_END_PUSH			= 27		# 玩家结束推MonsterExtQQRYJ事件
ENTITY_EVENT_ACTION_COMPLETED			= 28		# 士兵列阵指令执行完毕事件
ENTITY_EVENT_MEMBER_SOLDIER_CHANGE		= 29		# 自身带领士兵数量改变
ENTITY_EVENT_BE_KILL 					= 30 		# 被击杀
ENTITY_EVENT_ROLE_TEAM_JOIN 			= 31 		# 玩家加入队伍
ENTITY_EVENT_ROLE_TEAM_LEAVE 			= 32 		# 玩家离队
ENTITY_EVENT_HATRED_CHANGED				= 33		# 仇恨列表被改变

#行为
ENTITY_BEHAVIOR_USE_SKILL				= 1
ENTITY_BEHAVIOR_MOVING					= 2


# ------------------------------------------------------------------------------
# 任务类型
# ------------------------------------------------------------------------------
QUEST_TYPE_MAILLINE						= 1			# 主线任务
QUEST_TYPE_BRANCH						= 2			# 支线任务
QUEST_TYPE_DAILY						= 3			# 日常任务
QUEST_TYPE_LOOP							= 4			# 环任务
QUEST_TYPE_JSZZ							= 5			# 金树种子
QUEST_TYPE_TTD							= 6			# 通天塔
QUEST_TYPE_QIYUAN						= 7			# 奇缘任务

# ------------------------------------------------------------------------------
# 任务奖励类型（添加新类型，需到客户端添加）
# ------------------------------------------------------------------------------
QUEST_REWARD_TYPE_MONEY					= 1			# 金币奖励
QUEST_REWARD_TYPE_EXP					= 2			# 经验奖励
QUEST_REWARD_TYPE_ITEM					= 3			# 物品奖励
QUEST_REWARD_TYPE_SKILL					= 4			# 技能奖励
QUEST_REWARD_TYPE_XIUWEI				= 5			# 修为奖励
QUEST_REWARD_TYPE_POTENTIAL				= 6			# 潜能奖励
QUEST_REWARD_TYPE_ITEM_CHOOSE			= 7			# 多个物品选一个奖励
QUEST_REWARD_TYPE_TITLE					= 8			# 称号奖励
QUEST_REWARD_TYPE_CONTRIBUTE			= 9			# 帮贡奖励
QUEST_REWARD_TYPE_TONG_MONEY			= 10		# 帮会资金奖励
QUEST_REWARD_TYPE_REWARD_ID				= 11		# 根据奖励ID奖励
QUEST_REWARD_TYPE_BARRACKS_EXP			= 12		# 养兵经验奖励

# ------------------------------------------------------------------------------
# 任务状态
# ------------------------------------------------------------------------------
QUEST_NOT_ACCEPT						= 1			# 任务未做过（任务未接受:包含达到接受任务条件但未接受、未达到接受任务条件）
QUEST_DONE								= 2			# 任务已完成（任务已接受且任务目标全部达成）
QUEST_NOT_DONE							= 3			# 任务未完成（任务已接受但任务目标未全部达成）
QUEST_HAD_FINISH						= 4			# 任务已做过（任务已完成并提交了任务）

# ------------------------------------------------------------------------------
# 任务目标状态
# ------------------------------------------------------------------------------
TASK_DONE								= 2			# 任务目标已完成
TASK_NOT_DONE							= 3			# 任务目标未完成

# -----------------------------------------------------------------------------
# NPC头顶任务图标类型
#------------------------------------------------------------------------------
NPC_QUEST_SIGN_NO_ACCEPT				= 0			# 无可接任务
NPC_QUEST_SIGN_NOT_ACCEPT				= 1			# 任务可接
NPC_QUEST_SIGN_IS_DONE					= 2			# 任务可提交
NPC_QUEST_SIGN_NOT_DONE					= 3			# 任务未完成
NPC_LOOPQUEST_SIGN_NOT_ACCEPT			= 4			# 环任务可接
NPC_LOOPQUEST_SIGN_IS_DONE				= 5			# 环任务可提交
NPC_LOOPQUEST_SIGN_NOT_DONE				= 6			# 环任务未完成

QUEST_ACCEPT_FLAG_LIMIT					= 10		# 玩家等级-可接任务的所需等级＞10，将不显示绿色感叹号

#----------entity状态---------------------------------------------------------
ENTITY_STATE_PEAD						= 0			# 未决状态
ENTITY_STATE_FREE						= 1			# 普通状态
ENTITY_STATE_WARN						= 2			# 警戒状态
ENTITY_STATE_FIGHT						= 3			# 战斗状态
ENTITY_STATE_DEAD						= 4			# 死亡状态
ENTITY_STATE_RESET						= 5			# 重置状态（怪物特有）
ENTITY_STATE_SHOW						= 6			# 表演状态（怪物特有）
ENTITY_STATE_STALL						= 7			# 摆摊状态
ENTITY_STATE_STABLE						= 8			# 稳定状态	(不会切换到自由，战斗，重置)
ENTITY_STATE_MAX						= 9			# 状态最大值，高于此值的为无效状态


#----------CMonsterAIStatus----------------------------------------------------
CMONSTER_AI_STATE_DEAD 					= 0 		#死亡
CMONSTER_AI_STATE_NORMAL				= 1 		#普通
CMONSTER_AI_STATE_ESCAPE 				= 2         #逃跑


#-----------MonsterSoldierAIStatus--------------------------------------------
MONSTER_SOLDIER_AI_STATUS_PEND					= 0 		#准备状态
MONSTER_SOLDIER_AI_STATUS_FOLLOW				= 1 		#跟随状态
MONSTER_SOLDIER_AI_STATUS_RECTFORM				= 2 		#矩形列阵状态
MONSTER_SOLDIER_AI_STATUS_CIRCLEFORM			= 3 		#圆形列阵状态
MONSTER_SOLDIER_AI_STATUS_ATTACK				= 4 		#自由攻击状态
MONSTER_SOLDIER_AI_STATUS_DEAD					= 5 		#死亡状态


#-----------玩家申请警戒状态的原因-------------------
ROLE_WARN_REASON_NONE					= 0
ROLE_WARN_REASON_SKILL					= 0x00000001		#技能警戒
ROLE_WARN_REASON_SPACE					= 0x00000002		#空间范围警戒

#-----------行为开关------------------------新增行为开关需添加到 ACTION_FLAG_LIST，修改需要对应修改客户端 GameDefine.ACTION_FLAG----------------------
ACTION_FORBID_NONE = -1 				# 没有限制 
ACTION_FORBID_MOVE						= 0		# 1<<0	禁止主动移动（只禁止主动位移，不会禁止受击被迫位移）
ACTION_FORBID_SPELL						= 1		# 1<<1	禁止施法
ACTION_FORBID_USE_ITEM					= 2		# 1<<2	禁止使用道具
ACTION_FORBID_BE_ATTACK					= 3		# 1<<3	禁止受击
ACTION_FORBID_ATTACK					= 4		# 1<<4	禁止攻击(普通物理攻击)
ACTION_FORBID_JUMP						= 5		# 1<<5	禁止跳跃
ACTION_FORBID_WIELD						= 6		# 1<<6	禁止装备物品
ACTION_FORBID_CHAT						= 7		# 1<<7	禁止聊天
ACTION_FORBID_TALK						= 8		# 1<<8	禁止与NPC、spellBox交互
ACTION_FORBID_TRIGGER_PASSIVE			= 9		# 1<<9	禁止被动技能触发
ACTION_FORBID_BE_HIT_BACK				= 10	# 1<<10	禁止被击退
ACTION_FORBID_CHANGE_BODY				= 11	# 1<<11	禁止变身
ACTION_FORBID_CHANGE_POSTURE			= 12	# 1<<12	禁止变换姿势
ACTION_FORBID_CONJURE_PET				= 13	# 1<<13	禁止召唤幻兽
ACTION_FORBID_TRANSLATE_DIRECTION		= 14	# 1<<14	禁止玩家改变朝向（移动时候的朝向不影响）
ACTION_FORBID_EMERGENCY_EXIT			= 15	# 1<<15	禁止紧急回避
ACTION_FORBID_MOUNT_PET					= 16	# 1<<16	禁止幻兽骑乘
ACTION_FORBID_BE_CONTROL				= 17	# 1<<17	禁止控制
ACTION_FORBID_BE_IMPRESS				= 18	# 1<<18	禁止被良性增益
ACTION_FORBID_BE_DEPRESS				= 19	# 1<<19	禁止被恶性减损
ACTION_FORBID_INSANE					= 20	# 1<<20	禁止心智失常


ACTION_FLAG_LIST = (
	ACTION_FORBID_MOVE, ACTION_FORBID_SPELL, ACTION_FORBID_USE_ITEM, ACTION_FORBID_BE_ATTACK, ACTION_FORBID_ATTACK,
	ACTION_FORBID_JUMP, ACTION_FORBID_WIELD, ACTION_FORBID_CHAT, ACTION_FORBID_TALK, ACTION_FORBID_TRIGGER_PASSIVE,
	ACTION_FORBID_BE_HIT_BACK, ACTION_FORBID_CHANGE_BODY, ACTION_FORBID_CHANGE_POSTURE, ACTION_FORBID_CONJURE_PET,
	ACTION_FORBID_TRANSLATE_DIRECTION, ACTION_FORBID_EMERGENCY_EXIT,ACTION_FORBID_MOUNT_PET, ACTION_FORBID_BE_CONTROL,
	ACTION_FORBID_BE_IMPRESS, ACTION_FORBID_BE_DEPRESS, ACTION_FORBID_INSANE
	)




#-----------效果状态-----------------------新增效果状态需添加到 EFFECT_STATE_LIST-----------------------------------
EFFECT_STATE_DIZZY						= 0		# 1<<0	眩晕效果
EFFECT_STATE_UNCONTROLLABLE				= 1		# 1<<1	霸体效果
EFFECT_STATE_INVINCIBLE					= 2		# 1<<2	无敌效果
EFFECT_STATE_HIT_BACK					= 3		# 1<<3	受击中效果
EFFECT_STATE_FIX						= 4		# 1<<4	定身效果
EFFECT_STATE_SLEEP						= 5		# 1<<5	睡眠效果
EFFECT_STATE_WIND						= 6		# 1<<6	缠绕效果
EFFECT_STATE_PROTECT					= 7		# 1<<7	保护效果
EFFECT_STATE_FOLLOW						= 8		# 1<<8	跟随效果（包括组队跟随和队友跟随）
EFFECT_STATE_CONFUSION					= 9		# 1<<9	混乱效果
EFFECT_STATE_UNYIELDING					= 10	# 1<<10	不屈效果
EFFECT_STATE_FREEZE						= 11	# 1<<11	冻结效果
EFFECT_STATE_SHOW						= 12	# 1<<12	表演效果
EFFECT_STATE_HIDE						= 13	# 1<<13	隐身效果
EFFECT_STATE_LIST = ( EFFECT_STATE_DIZZY, EFFECT_STATE_UNCONTROLLABLE, EFFECT_STATE_INVINCIBLE, EFFECT_STATE_HIT_BACK, EFFECT_STATE_FIX, EFFECT_STATE_SLEEP, EFFECT_STATE_WIND,
					EFFECT_STATE_PROTECT, EFFECT_STATE_FOLLOW, EFFECT_STATE_CONFUSION, EFFECT_STATE_UNYIELDING, EFFECT_STATE_FREEZE, EFFECT_STATE_SHOW, EFFECT_STATE_HIDE )


#----------------------增加玩家经验的原因-----------------------
EXP_ADD_REASON_KILL_MONSTER				= 1			# 杀怪
EXP_ADD_REASON_QUEST_REWARD				= 2			# 任务
EXP_ADD_REASON_USE_GIFT_ITEM			= 3			# 打开礼包
EXP_ADD_REASON_BY_SPELLBOX				= 4			# 打开宝箱
EXP_ADD_REASON_SPACE_SENTLEMENT			= 5			# 副本结算
EXP_ADD_REASON_SPACE_STRATEGYPOINT		= 6			# 副本策略点
EXP_ADD_REASON_YXLM_KILL_REWARD			= 7			# 英雄联盟击杀奖励经验
EXP_ADD_REASON_GM_SET					= 8			# GM指令设置
EXP_ADD_REASON_BHZB_POINT_WAR 			= 9			# 帮会争霸据点争夺
EXP_ADD_REASON_SGMZ_KILL_ROLE 			= 10		# 上古密阵击杀玩家
EXP_ADD_REASON_SGMZ_KILL_BOSS 			= 11		# 上古密阵击杀Boss
EXP_ADD_REASON_ATTR_CORRECT				= 12		# 经验属性修正
EXP_ADD_REASON_SKILL 		 			= 13		# 技能效果
EXP_ADD_REASON_JMZC_KILL_ROLE 			= 14 		# 绝命战场击杀玩家
EXP_ADD_REASON_JMZC_FINAL_EXP 			= 15 		# 绝命战场副本结算经验奖励
EXP_ADD_REASON_YXLM_FINAL_EXP			= 16		# 英雄联盟副本结算经验奖励

#----------------------增加玩家金币的原因-----------------------
MONEY_ADD_REASON_DROP_MONSTER			= 1			# 怪物身上掉落
MONEY_ADD_REASON_QUEST_REWARD			= 2			# 任务奖励
MONEY_ADD_REASON_ROLE_TRADE				= 3			# 玩家交易
MONEY_ADD_REASON_SELL_ITEM				= 4			# 出售物品
MONEY_ADD_REASON_RETURN_ITEM			= 5			# 退回物品
MONEY_ADD_REASON_USE_GIFT_ITEM			= 6			# 打开礼包
MONEY_ADD_REASON_FROM_STORE				= 7			# 从仓库取钱
MONEY_ADD_REASON_LINGSHI_TRADE			= 8			# 灵石寄售
MONEY_ADD_REASON_GM_COMMAND				= 9			# GM命令
MONEY_ADD_REASON_SPACE_SENTLEMENT		= 10		# 副本结算
MONEY_ADD_REASON_SPAR_HUN_TING			= 11		# 晶石狩猎场
MONEY_ADD_REASON_TONGCONTRI_TO_MONEY	= 12		# 帮会解散 帮贡转化为钱
MONEY_ADD_REASON_MAIL					= 13		# 邮件
MONEY_ADD_REASON_MAIL_ATTR_CORRECT		= 14		# 金币属性修正
MONEY_ADD_REASON_SKILL					= 15		# 技能效果

#----------------------减少玩家金币的原因-----------------------
MONEY_SUB_REASON_SPACE_RANDOM			= 1			# 副本随机减少
MONEY_SUB_REASON_NPC_TALK				= 2			# NPC对话消耗
MONEY_SUB_REASON_SHOP_BUY				= 3			# 商店购买物品消费
MONEY_SUB_REASON_EQUIP_REPAIR			= 4			# 装备修理消耗
MONEY_SUB_REASON_UNLOCK_GRID			= 5			# 解锁背包格
MONEY_SUB_REASON_LINGSHI_TRADE			= 6			# 灵石寄售
MONEY_SUB_REASON_PAY_FOR_MAIL_BILL		= 7			# 邮件资费
MONEY_SUB_REASON_COMPOSE_PET			= 8			# 合成幻兽
MONEY_SUB_REASON_REPLACE_PET_SKILL		= 9			# 替换幻兽技能
MONEY_SUB_REASON_UPGRADE_PET_SKILL		= 10		# 升级幻兽技能
MONEY_SUB_REASON_ACTIVATE_CAGE			= 11		# 激活幻兽笼子
MONEY_SUB_REASON_ADD_ENTTIME			= 12		# 添加有效聊天时间
MONEY_SUB_REASON_ROLE_REVIVE			= 13		# 玩家复活
MONEY_SUB_REASON_COMMONUTION_SKILL		= 14		# 精研技能
MONEY_SUB_REASON_TELEPORT				= 15		# 玩家传送消耗
MONEY_SUB_REASON_TONG_DONATE			= 16		# 帮会捐献
MONEY_SUB_REASON_GM_COMMAND				= 17		# GM命令
MONEY_SUB_REASON_ROLE_TRADE				= 18		# 玩家交易
MONEY_SUB_REASON_CREATE_TONG			= 19		# 创建帮会
MONEY_SUB_REASON_LEARN_TONG_SKILL		= 20		# 学习帮会技能
MONEY_SUB_REASON_INTENSIFY_EQUIP		= 21		# 装备强化
MONEY_SUB_REASON_RESET_EQUIP			= 22		# 装备回火
MONEY_SUB_REASON_SAVE_INTENSIFY_EQUIP	= 23		# 装备保存
MONEY_SUB_REASON_RESET_INTENSIFY_EQUIP	= 24		# 装备还原
MONEY_SUB_REASON_SHUFFLE_EQUIP			= 25		# 装备洗练
MONEY_SUB_REASON_RECOST_EQUIP			= 26		# 装备重铸
MONEY_SUB_REASON_TRANSFER_EQUIP			= 27		# 装备传星
MONEY_SUB_REASON_COMPOSE_EQUIP			= 28		# 打造装备
MONEY_SUB_REASON_UNLOCK_PASSIVESKILLBAR	= 29		# 解锁被动技能栏位
MONEY_SUB_REASON_UPGRADE_SKILL			= 30		# 升级技能
MONEY_SUB_REASON_BARRACKS				= 31		# 玩家兵营
MONEY_SUB_REASON_COMPOSE_TOOL			= 32		# 工具打造
MONEY_SUB_REASON_JADE_UPGRADE			= 33		# 玲珑玉令升级消耗
MONEY_SUB_REASON_MELTHING				= 34		# 淬炼
MONEY_SUB_REASON_GET_JADE				= 35		# 获得玲珑玉令
MONEY_SUB_REASON_REFLASH_LHMJ_SHOP		= 36		# 轮回秘境商店刷新
MONEY_SUB_REASON_REFLASH_LHMJ_DONGFU	= 37		# 轮回秘境洞府建造
MONEY_SUB_REASON_REFLASH_LHMJ_BUILD		= 38		# 轮回秘境洞升级消耗
MONEY_SUB_REASON_REFLASH_TG_QUEST		= 40		# 刷新练兵任务
MONEY_SUN_REASON_OCCUPY_TRAIN_GROUND 	= 41		# 占领练兵场
MONEY_SUB_REASON_OPEN_INTENSIFY_SAVE_SLOT =42		# 开启装备强化备份栏位
MONEY_SUB_REASON_FEED_PET				=43			# 喂养幻兽
MONEY_SUB_REASON_UNLOCK_CHUANCHENGSKILLBAR	=44		# 解锁传承技能栏位
MONEY_SUB_REASON_REPLACE_PET_P_SKILL	= 45			# 替换幻兽被动技能
MONEY_SUB_REASON_UPGRADE_PET_P_SKILL	= 46			# 升级幻兽被动技能

#----------------------减少玩家金币的原因-----------------------
TONG_MONEY_ADD_REASON_NORMAL			= 0			# 
TONG_MONEY_ADD_REASON_PERSON			= 1			# 个人因素，添加帮会金币（捐赠等）
TONG_MONEY_ADD_REASON_JOIN_BHZB_FAIL 	= 2			# 未能成功参与帮会争霸

#----------------------增加玩家修为的原因-----------------------
XIUWEI_ADD_REASON_NORMAL				= 0			# 默认方式
XIUWEI_ADD_REASON_QUEST_REWARD			= 1			# 任务奖励
XIUWEI_ADD_REASON_BY_SKILL				= 2			# 技能奖励
XIUWEI_ADD_REASON_DORP_MONSTER			= 3			# 怪物身上掉落
XIUWEI_ADD_REASON_USE_GIFT_ITEM			= 4			# 打开礼包
XIUWEI_ADD_REASON_USE_SPAR_ITEM			= 5			# 使用晶核
XIUWEI_ADD_REASON_SPACE_SENTLEMENT		= 6			# 副本结算
XIUWEI_ADD_REASON_GMCOMMAND				= 7			# 副本结算
XIUWEI_ADD_REASON_ATTR_CORRECT			= 8			# 修为属性修正

#----------------------增加玩家潜能的原因-----------------------
POTENTIAL_ADD_REASON_NORMAL				= 0			# 默认方式
POTENTIAL_ADD_REASON_QUEST_REWARD		= 1			# 任务奖励
POTENTIAL_ADD_REASON_DORP_MONSTER		= 2			# 怪物身上掉落
POTENTIAL_ADD_REASON_USE_GIFT_ITEM		= 3			# 打开礼包
POTENTIAL_ADD_REASON_SPACE_SENTLEMENT	= 4			# 副本结算
POTENTIAL_ADD_REASON_GMCOMMAND			= 5			# GM命令
POTENTIAL_ADD_REASON_STRATEGY_POINT		= 6			# 副本策略点
POTENTIAL_ADD_REASON_ATTR_CORRECT 		= 7			# 潜能属性修正
POTENTIAL_ADD_REASON_SKILL				= 8			# 技能

#----------------------减少玩家潜能的原因-----------------------
POTENTIAL_REMOVE_REASON_NORMAL						= 0			# 默认方式
POTENTIAL_REMOVE_REASON_STUDY_SKILL					= 1			# 技能学习
POTENTIAL_REMOVE_REASON_ADD_JADE					= 2			# 获得玲珑玉令
POTENTIAL_REMOVE_REASON_JADE_UPGRADE				= 3			# 玲珑玉令升级
POTENTIAL_REMOVE_REASON_UNLOCK_CHUANCHENGSKILLBAR	= 4			# 解锁传承技能栏位
#----------------------增加玩家功勋的原因-----------------------
FEATS_ADD_REASON_NORMAL					= 0			# 默认方式
FEATS_ADD_REASON_DROP					= 1			# 掉落方式
FEATS_ADD_REASON_CAMP					= 2			# 阵营击杀方式
FEATS_ADD_REASON_SGMZ_KILL_ROLE 		= 3			# 上古密阵击杀玩家
FEATS_ADD_REASON_JSSLC_KILL_ROLE		= 4			# 晶石狩猎场击杀玩家
FEATS_ADD_REASON_ATTR_CORRECT			= 5			# 属性修正
FEATS_ADD_REASON_SKILL					= 6			# 技能效果方式
FEATS_ADD_REASON_YXWZ 					= 7			# 英雄王座
FEATS_ADD_REASON_JMZC 					= 8 		# 绝命战场


#----------------------减少玩家功勋的原因-----------------------
FEATS_REMOVE_REASON_NORMAL				= 0			# 默认方式
FEATS_REMOVE_REASON_SHOP				= 1			# 商店购买（TRADE_TYPE_NPC_SHOP 与此值相等，不能改）

#----------------------增加玩家技能的原因-----------------------
SKILL_ADD_REASON_NORMAL					= 0			# 默认方式
SKILL_ADD_REASON_QUEST_REWARD			= 1			# 任务奖励
SKILL_ADD_REASON_BORN_GAIN				= 2			# 出生赋值
SKILL_ADD_REASON_LEARN_TONG_SKILL		= 3			# 学习帮会技能

#----------------------删除玩家技能的原因-----------------------
SKILL_REMOVE_REASON_NORMAL				= 0			# 默认方式
SKILL_REMOVE_REASON_LEARN_SKILL			= 1			# 升级技能

#----------------------怪物行为类型-----------------------
BEHAVIOUR_TYPE_RESET_MOVE				= 6			# 回走
BEHAVIOUR_TYPE_CHASE					= 4			# 追击
BEHAVIOUR_TYPE_MOVING					= 1			# 移动
BEHAVIOUR_TYPE_SPELL					= 2			# 使用技能(单个)
BEHAVIOUR_TYPE_WANDER					= 5			# 游荡
BEHAVIOUR_TYPE_SPELL_ONLY				= 3			# 仅仅使用技能，不追踪

MOVE_TYPE_NORMAL						= 0			# 普通移动方式（使用巡逻数据）
MOVE_TYPE_FLY							= 1			# 飞行移动

#----------------------战斗关系-----------------------
COMBAT_RELATION_DEFAULT					= 0			# 未设置
COMBAT_RELATION_NORMAL					= 1			# 友好
COMBAT_RELATION_ENEMY					= 2			# 敌对
COMBAT_RELATION_NEUTRALLY				= 3			# 中立
COMBAT_RELATION_NONE					= 4			# 无任何关系

#------复活方式--------------------------------------------------------------
REVIVE_ON_ORIGIN_BY_COST_ITEM			= 0			# 原地复活(消耗物品)
REVIVE_ON_CITY							= 1			# 回城复活
REVIVE_ON_RETURN_POINT					= 2			# 复活到返回点
REVIVE_ON_REVIVE_SPACE					= 3			# space文件中reviveScriptID配置的地图复活
REVIVE_ON_SPACE_COPY					= 4			# 副本复活（动态区域）
REVIVE_ON_ORIGIN_BY_COST_MONEY			= 5			# 原地复活(消耗金钱)
REVIVE_ON_LING_MAI_COPY					= 6			# 灵脉战场的复活方式
REVIVE_ON_FROZEN_FIGHT_COPY				= 7			# 冰雪之战的复活方式
REVIVE_ON_SECOND_TONG_STARCRAFT			= 8			# 帮会争霸第二场的复活方式
REVIVE_ON_LING_QI						= 9			# 灵气迷宫复活方式
REVIVE_ON_YXLM							= 10		# 英雄王座复活方式
REVIVE_ON_THIRD_TONG_STARCRAFT			= 11		# 帮会争霸第三场的复活方式
REVIVE_ON_JSZZ							= 12		# 金树种子复活方式
REVIVE_ON_YCJMD							= 13		# 勇闯绝命岛复活方式
REVIVE_ON_SGMZ							= 14		# 上古密阵复活方式
REVIVE_ON_FHLT							= 15		# 烽火连天复活方式
REVIVE_ON_GCZ 							= 16		# 攻城战复活方式
REVIVE_ON_HLBCPVP 						= 17		# 高级练兵场PVP
REVIVE_ON_LBCPVP 						= 18		# 练兵场PVP复活方式
REVIVE_ON_LHMJ							= 19		# 轮回秘境复活方式
REVIVE_ON_DF	 						= 20		# 洞府复活方式
REVIVE_ON_TONG_PLUNDER	 				= 21		# 帮会掠夺战复活方式
REVIVE_ON_BHZBPOINTWAR_PVP 				= 22		# 帮会争霸 据点争夺战 PVP 复活

#---------NPC商店-------------------------
NPCSHOP_BUY_RATIO						= 1.0		# 商店购买价格比
NPCSHOP_SELL_RATIO						= 1.0		# 商店出售价格比
NPCSHOP_RETURN_RATIO					= 1.0		# 商店退货价格比

NPCSHOP_BUY_DISTANCE					= 5.0		# 与NPC最大距离

NPCSHOP_BUY_BACK_AMOUNT					= 10		# 商店可记录回购数量
NPCSHOP_HIGH_BUY_BACK_TIME				= 259200.0	# 高级回购限时
NPCSHOP_HIGH_BUY_BACK_AMOUNT			= 30		# 商店可记录高级回购数量

NPCSHOP_ITEM_REFRESH_NULL				= 0			# 不刷新
NPCSHOP_ITEM_REFRESH_WEEK				= 1			# 每周刷新
NPCSHOP_ITEM_REFRESH_DAY				= 2			# 每日刷新
NPCSHOP_ITEM_REFRESH_SELLOUT			= 3			# 售完刷新
NPCSHOP_ITEM_REFRESH_TIME				= 4			# 定点刷新

#--------------------------------------商城-----------------------------------------
STORE_GOODS_REFRESH_NULL				= 0			# 不刷新
STORE_GOODS_REFRESH_DAY					= 1			# 每日刷新
STORE_GOODS_REFRESH_WEEK				= 2			# 每周刷新

STORE_RULE_LIMIT_TIME					= 1			# 购买时间限制
STORE_RULE_DISCOUNT_TIME				= 2			# 折扣时间限制

STORE_GOODS_TYPE_HOME					= 0			# 首页
STORE_GOODS_TYPE_APPEARANCE				= 1			# 外观
STORE_GOODS_TYPE_PET 					= 2			# 坐骑
STORE_GOODS_TYPE_SUNDRIES				= 3			# 天才地宝
STORE_GOODS_TYPE_XUANSHI				= 4			# 玄石专区

STORE_TYPE_XIANSHI						= 1			# 仙石商城
STORE_TYPE_LINGSHI						= 2			# 灵石商城
STORE_TYPE_XUANSHI						= 3			# 玄石商城
STORE_TYPE_JINQIAN						= 4			# 金钱商城

STORE_GOODS_STATE_SOLD_OUT				= 1			# 下架商品
STORE_GOODS_STATE_NEW_PRODUCT			= 2			# 新品商品
STORE_GOODS_STATE_HOT_SELL				= 3			# 热销商品 

#商城物品类型
STORE_ITEM_TYPE_SPECIAL					= 1			# 天材地宝
STORE_ITEM_TYPE_MEDICINE				= 2			# 灵丹妙药
STORE_ITEM_TYPE_GIFT					= 3			# 精品礼包
STORE_ITEM_TYPE_PET						= 4			# 幻兽灵宝

#礼品盒
STORE_GIFT_STATE_NONE					= 0			# 礼品默认状态
STORE_GIFT_STATE_OVERDUE				= 1			# 礼品已过期
STORE_GIFT_STATE_ACCEPT					= 2			# 礼品对方已接受
STORE_GIFT_STATE_REFUSE					= 3			# 礼品对方已拒绝
STORE_GIFT_STATE_RECAPTION				= 4			# 礼品已取回
STORE_GIFT_STATE_SELF_ACCEPT			= 5			# 礼品已接受
STORE_GIFT_STATE_SELF_REFUSE			= 6			# 礼品已拒绝

STORE_CART_CAPACIYT						= 20		# 购物车容量

#-----------------------活动类型--------------------------------
ACTIVITY_TYPE_UNKNOWN					= 0			# 未知
ACTIVITY_TYPE_POTENTAIL_SPACE			= 1			# 潜能副本
ACTIVITY_TYPE_CHUANCHENG_SPACE_1		= 2			# 传承副本(20级)
ACTIVITY_TYPE_MAGIC_MAZE_SPACE_1		= 3			# 幻阵迷宫副本（20级）
ACTIVITY_TYPE_TONG_SPACE_COPY			= 4			# 帮会副本
ACTIVITY_TYPE_CAMP_YXLM					= 5			# 英雄王座
ACTIVITY_TYPE_CAMP_SGMZ					= 6			# 上古密阵
ACTIVITY_TYPE_CAMP_YCJMD				= 7			# 阵营战场“勇闯绝命岛”
ACTIVITY_TYPE_CAMP_LING_MAI				= 8			# 灵脉战场
ACTIVITY_TYPE_CAMP_FIVE_YCJMD			= 9			# 阵营战场“勇闯绝命岛”（5人）
ACTIVITY_TYPE_CAMP_JSSLC 				= 10		# 晶石狩猎场
ACTIVITY_TYPE_CAMP_ZZZB					= 11		# 至尊争霸
ACTIVITY_TYPE_CAMP_SHOOT_YCJMD			= 12		# 勇闯夺命岛（远程）
ACTIVITY_TYPE_CAMP_COPY_YCJMD			= 13		# 勇闯夺命岛（近战）
ACTIVITY_TYPE_COPY_ACCTACK_CITY_WAR		= 14		# 攻城战
ACTIVITY_TYPE_CHUANCHENG_SPACE_2		= 15		# 传承副本(30级)
ACTIVITY_TYPE_MAGIC_MAZE_SPACE_2		= 16		# 幻阵迷宫副本(30级)
ACTIVITY_TYPE_TONG_DAILY_QUEST			= 17		# 帮会日常

#所有活动类型
ACTIVITY_TYPE_LIST = [
	ACTIVITY_TYPE_POTENTAIL_SPACE,
	ACTIVITY_TYPE_CHUANCHENG_SPACE_1,
	ACTIVITY_TYPE_MAGIC_MAZE_SPACE_1,
	ACTIVITY_TYPE_TONG_SPACE_COPY,
	ACTIVITY_TYPE_CAMP_YXLM,
	ACTIVITY_TYPE_CAMP_SGMZ,
	ACTIVITY_TYPE_CAMP_YCJMD,
	ACTIVITY_TYPE_CAMP_LING_MAI,
	ACTIVITY_TYPE_CAMP_FIVE_YCJMD,
	ACTIVITY_TYPE_CAMP_JSSLC,
	ACTIVITY_TYPE_CAMP_ZZZB,
	ACTIVITY_TYPE_CAMP_SHOOT_YCJMD,
	ACTIVITY_TYPE_CAMP_COPY_YCJMD,
	ACTIVITY_TYPE_COPY_ACCTACK_CITY_WAR,
	ACTIVITY_TYPE_CHUANCHENG_SPACE_2,
	ACTIVITY_TYPE_MAGIC_MAZE_SPACE_2,
	ACTIVITY_TYPE_TONG_DAILY_QUEST,
]

#-----------------------玩家游戏记录(publicActRecord)key值--------------------------------
ROLE_ACT_UNKNOW							= 0			# 未知
ROLE_ACT_POTENTAIL_SPACE				= 1			# 潜能副本活动记录
ROLE_ACT_CHUANCHENG_SPACE_1				= 2			# 传承副本活动记录(20级)
ROLE_ACT_MAGIC_MAZE_SPACE_1				= 3			# 幻阵迷宫副本活动记录(20级)
ROLE_ACT_TONG_SPACE_COPY				= 4			# 帮会副本记录
ROLE_ACT_YXLM_CAMP_SPACE				= 5			# 英雄联盟记录
ROLE_ACT_SGMZ_CAMP_SPACE				= 6			# 上古密阵记录
ROLE_ACT_YCJMD_CAMP_SPACE				= 7			# 阵营战场“勇闯绝命岛”记录
ROLE_ACT_LING_MAI_CAMP_SPACE			= 8 		# 灵脉战场记录
ROLE_ACT_YCJMD_CAMP_FIVE_SPACE			= 9 		# 阵营战场“勇闯绝命岛”（5人）
ROLE_ACT_JSSLC_CAMP_SPACE 				= 10		# 晶石狩猎场记录
ROLE_ACT_ZZZB_SPACE 					= 11		# 至尊争霸记录
ROLE_ACT_CAMP_SHOOT_YCJMD				= 12		# 勇闯夺命岛（远程）
ROLE_ACT_CAMP_COPY_YCJMD				= 13		# 勇闯夺命岛（近战）
ROLE_ACT_COPY_ACCTACK_CITY_WAR			= 14		# 攻城战
ROLE_ACT_CHUANCHENG_SPACE_2				= 15			# 传承副本活动记录(30级)
ROLE_ACT_MAGIC_MAZE_SPACE_2				= 16			# 幻阵迷宫副本活动记录(30级)

#-----------------掉落目标类型---------------------------
DROP_OWNER_TYPE_PERSON					= 1			# 个人
DROP_OWNER_TYPE_TEAM					= 2			# 队伍
DROP_OWNER_TYPE_TONG					= 3			# 帮会

#-----------------快捷栏类型---------------------------
QB_ITEM_NONE							= 0			# 空快捷项
QB_ITEM_SKILL							= 1			# 玩家技能快捷项
QB_ITEM_EQUIP							= 2			# 装备中的道具
QB_ITEM_KITBAG							= 3			# 背包中的物品道具快捷项
QB_ITEM_PET_SKILL						= 4			# 幻兽技能快捷项
QB_ITEM_PET_HEAD						= 5			# 幻兽头像快捷项
QB_ITEM_PET_SHENTONG_SKILL				= 6			# 幻兽神通技能快捷项
QB_ITEM_SHENTONG_SKILL					= 7			# 玩家神通技能快捷项

#-----------------物品累加类型---------------------------
ITEM_OVERLYING_TYPE_NONE				= 0			# 无叠加
ITEM_OVERLYING_TYPE_STACK				= 1			# 可叠加
ITEM_OVERLYING_TYPE_TIME				= 2			# 使用次数(使用完销毁)
ITEM_OVERLYING_TYPE_EMPOWER				= 3			# 充能次数(使用完不销毁)
#-----------------------玩家标志位------------------------
ROLE_FLAG_WATCHER						= 1			# 观察者标志位
ROLE_FLAG_TEAMMING						= 2			# 玩家正处于队伍中

#-----------------------怪物或NPC标志位------------------------

FLAG_RELATION_ENEMY_TO_ROLE				= 1			# 怪物和玩家可以互相攻击
FLAG_RELATION_NORMAL_TO_ROLE			= 2			# 怪物和玩家不可以互相攻击
FLAG_RELATION_ENEMY_TO_MONSTER			= 3			# 怪物和怪物可以互相攻击
FLAG_RELATION_NORMAL_TO_MONSTER			= 4			# 怪物和怪物不可以互相攻击

FLAG_AI_TICK							= 7			# 不在玩家AOI范围内也可以开始AI tick
FLAG_UNVISIBLE							= 8			# 对象不可见
FLAG_CAN_FLY							= 9			# 对象可浮空
FLAG_CANT_ROTATE						= 10		# 不能转向
FLAG_CANT_SELECTED						= 11		# 不能被选中
FLAG_OPEN_COLLISION						= 12		# 开启全部模型碰撞
FLAG_HIDE_FLOAT_NAME					= 13		# 屏蔽头顶名字
FLAG_HIDE_FLOAT_HPBAR					= 14		# 屏蔽头顶血条
FLAG_HIDE_FLOAT_LEVEL					= 15		# 屏蔽头顶等级
FLAG_SHOW_FLOAT_NAME					= 16		# 显示头顶名字
FLAG_SHOW_FLOAT_HPBAR					= 17		# 显示头顶血条
FLAG_SHOW_FLOAT_LEVEL					= 18		# 显示头顶等级
FLAG_WANDER								= 19		# 游荡标志位
FLAG_RELATION_EMENY_TO_ROLE				= 20		# 陷阱单向敌对玩家 
FLAG_RELATION_FRIEND_TO_ROLE			= 21		# 陷阱单向优好玩家 
FLAG_USE_SERVER_FLAG					= 22		# 使用服务器追击
FLAG_CLOSE_COLLISION					= 23		# 关闭全部模型碰撞
FLAG_MESH_COLLISION						= 24		# 开启mesh和staticmesh的碰撞
FLAG_STOP_BULLET						= 25		# 防弹标志位（子弹撞上敌对防弹单位，会中断）
FLAG_SHOW_FLOAT_DAMAGEBAR				= 26		# 显示头顶伤害进度条
FLAG_OPEN_CAMERA_COLLISION				= 28		# 开启摄像机碰撞
FLAG_NOT_RESET_SPAWNDIR					= 29		# 回走结束不重置出生点朝向
FLAG_CAN_BE_TREAD						= 30		# 可以被踩踏
FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL= 31	# 开启光线碰撞通道-地面（用来做entity可以站上去表现）

#-------------------------entity状态标志位(程序用来维护状态不提供给策划使用)---------------------------------------
STATE_FLAG_SLIPINTO						= 1			# 潜入状态
STATE_FLAG_XIN_MO						= 2			# 心魔附身状态

#---------------------仙石，灵石，玄石---------------------------
#仙石
CHANGE_XIANSHI_NORMAL					= 0			# 默认方式
CHANGE_XIANSHI_UNLOCKBAGGRID			= 1			# 解锁背包格
CHANGE_XIANSHI_PETCAGES					= 2			# 解锁幻兽格子
CHANGE_XIANSHI_INTENSIFY_SAVESLOT		= 3			# 解锁强化保存栏位
CHANGE_XIANSHI_GM_SET					= 4			# GM指令设置元宝
CHANGE_XIANSHI_AUGMENT_SIGNIN			= 5			# 补签消耗元宝
CHANGE_XIANSHI_COMPOSE_EQUIP			= 6			# 装备打造消耗元宝
CHANGE_XIANSHI_CHARGE					= 7			# 充值兑换
CHANGE_XIANSHI_RECAST_EQUIP				= 8			# 使用元宝重铸
CHANGE_XIANSHI_RESET_EQUIP				= 9			# 使用元宝洗练
CHANGE_XIANSHI_BY_MAILL					= 10		# 邮件
CHANGE_XIANSHI_BY_SHOP_CONSUME			= 11		# 商城消费
CHANGE_XIANSHI_BY_TRADE					= 12		# 灵石急售
CHANGE_XIANSHI_BY_INTENSIFY_EQUIP		= 13		# 装备强化
CHANGE_XIANSHI_BY_RESET_EQUIP			= 14		# 装备回火
CHANGE_XIANSHI_BY_SAVE_INTENSIFY_EQUIP	= 15		# 装备备份
CHANGE_XIANSHI_BY_RESET_INTENSIFY_EQUIP	= 16		# 装备还原
CHANGE_XIANSHI_BY_UNLOCK_PASSIVESKILLBAR= 17		# 解锁被动技能栏位
CHANGE_XIANSHI_PETCOMPOSE				= 18		# 合成幻兽
CHANGE_XIANSHI_ATTR_CORRECT				= 19		# 属性修正

#玄石
CHANGE_XUANSHI_CHARGE					= 1			# 充值兑换
CHANGE_XUANSHI_GM_SET					= 2			# GM指令设置玄石
CHANGE_XUANSHI_SILVERPRESENT			= 3			# 领取玄石奖励
CHANGE_XUANSHI_SHOP_CONUSUME			= 4			# 商城消费
CHANGE_XUANSHI_SHOP_REBATE				= 5			# 商城消费返利
CHANGE_XUANSHI_ATTR_CORRECT				= 6			# 属性修正

#灵石
CHANGE_LINGSHI_NORMAL					= 0			# 默认方式
CHANGE_LINGSHI_BY_STORE					= 1			# 商城购买
CHANGE_LINGSHI_BY_MAILL					= 2			# 邮件
CHANGE_LINGSHI_BY_SHOP_CONUSUME			= 3			# 商城消费
CHANGE_LINGSHI_UNLOCKBAGGRID			= 4			# 解锁背包格
CHANGE_LINGSHI_PETCAGES					= 5			# 解锁幻兽格子
CHANGE_LINGSHI_INTENSIFY_SAVESLOT		= 6			# 解锁强化保存栏位
CHANGE_LINGSHI_GM_SET					= 7			# GM指令设置元宝
CHANGE_LINGSHI_AUGMENT_SIGNIN			= 8			# 补签消耗元宝
CHANGE_LINGSHI_COMPOSE_EQUIP			= 9			# 装备打造消耗元宝
CHANGE_LINGSHI_CHARGE					= 10		# 充值兑换
CHANGE_LINGSHI_RECAST_EQUIP				= 11		# 使用元宝重铸
CHANGE_LINGSHI_RESET_EQUIP				= 12		# 使用元宝洗练
CHANGE_LINGSHI_BY_MAILL					= 13		# 邮件
CHANGE_LINGSHI_BY_SHOP_CONSUME			= 14		# 商城消费
CHANGE_LINGSHI_BY_TRADE					= 15		# 灵石急售
CHANGE_LINGSHI_BY_INTENSIFY_EQUIP		= 16		# 装备强化
CHANGE_LINGSHI_BY_RESET_EQUIP			= 17		# 装备回火
CHANGE_LINGSHI_BY_SAVE_INTENSIFY_EQUIP	= 18		# 装备备份
CHANGE_LINGSHI_BY_RESET_INTENSIFY_EQUIP	= 19		# 装备还原
CHANGE_LINGSHI_BY_UNLOCK_PASSIVESKILLBAR= 20		# 解锁被动技能栏位
CHANGE_LINGSHI_PETCOMPOSE				= 21		# 合成幻兽
CHANGE_LINGSHI_ATTR_CORRECT				= 22		# 属性修正



#角色状态roleState，有刚创建0，激活（1），删除（3），冻结（4）
ROLE_STATE_CREATE						= 0			# 刚创建
ROLE_STATE_ACTIVE						= 1			# 激活，创建完进入游戏就会设置为激活
ROLE_STATE_INACTIVE						= 2			# 不激活，目前没有使用	
ROLE_STATE_DELETE						= 3			# 删除角色
ROLE_STATE_FROZEN						= 4			# 角色已被冻结，无法使用


#------------------------Debug标志位（用于开启某种类型的调试信息）----------------------------------
ENTITY_DEBUG_FLAG_FOR_AI				= 1			# AI调试信息标志

#------------------------陷阱----------------------------------
# 陷阱初始化行为
TRAP_INIT_ACTION_ADD_BUFF				= 0			# 给自身添加buff

# 陷阱普通行为
TRAP_NORMAL_ACTION_ENTER_PLANE				= 0			# 进入位面事件
TRAP_NORMAL_ACTION_LEAVE_PLANE				= 1			# 离开位面事件
TRAP_NORMAL_ACTION_SPELL_TARGET				= 2			# 陷阱对目标施法
TRAP_NORMAL_ACTION_HITBACK					= 3			# 击退行为
TRAP_NORMAL_ACTION_DEAD_SELF				= 4			# 陷阱进入死亡状态
TRAP_NORMAL_ACTION_CONDITIONCHANGE			= 5			# 给副本发送通知
TRAP_NORMAL_ACTION_START_WALK				= 8			# 开始巡逻
TRAP_NORMAL_ACTION_CREATEENTITY				= 9			# 随机创建Entity
TRAP_NORMAL_ACTION_SPACE_DOOR_TELEPORT		= 10		# 大地图传送门的传送行为
TRAP_NORMAL_ACTION_CHANGE_SPACE_LIFE		= 11		# 副本计时 增加\减少
TRAP_NORMAL_ACTION_PLAY_ACTION				= 12		# 陷阱播动作
TRAP_NORMAL_ACTION_GET_REWARD				= 13		# 获得奖励
TRAP_NORMAL_ACTION_SET_DIRECTION			= 14		# 改变进入者朝向
TRAP_NORMAL_ACTION_SET_TEMP					= 15		# 设置temp值
TRAP_NORMAL_ACTION_CREATE_HEHUA				= 16		# 创建荷花
TRAP_NORMAL_ACTION_GET_ITEM					= 17		# 玩家获得物品(怪物则使用技能)
TRAP_NORMAL_ACTION_HQLZ_CREATE_ENTITY		= 18		# 环任务:获取龙珠 创建entity 并记录其位置
TRAP_NORMAL_ACTION_TELEPORT_NEAREST_ENTITY	= 19		# 传送距离最近的同scriptID的entity
TRAP_NORMAL_ACTION_TELEPORT_RANDOM_POSITION	= 20		# 传送到配置的随机位置
TRAP_NORMAL_ACTION_SPELL_SELF				= 21		# 陷阱对自身施法
TRAP_NORMAL_ACTION_REMOVE_BUFF 				= 22		# 移除BUff
TRAP_NORMAL_ACTION_T_SPELL_SELF 			= 23		# 触发者对自身施法


#陷阱周期行为
TRAP_CYCLE_ACTION_NONE					= 0			# 
TRAP_CYCLE_ACTION_USE_SKILL				= 1			# 周期使用技能
TRAP_CYCLE_ACTION_CREATE_ENTITY			= 2			# 周期性创建Entity
TRAP_CYCLE_ACTION_CHECKAROUND			= 3			# 晶石狩猎场周期性检测周围是否有该阵营的玩家
TRAP_CYCLE_ACTION_CHECKHASPLAYER		= 4			# 周期性检测周围是否存在玩家
TRAP_CYCLE_ACTION_BATTLEFLAG_CHECK 		= 5 		# 战旗检测
TRAP_CYCLE_ACTION_BARRACKS_REVIVE_CHECK = 6			# 判断归属方  加Buff

#陷阱持有行为
TRAP_HOLD_ACTION_UNCONTROL				= 0			# 霸体
TRAP_HOLD_ACTION_INVINCIBLE				= 1			# 无敌
TRAP_HOLD_ACTION_SUCK					= 2			# 吸力
TRAP_HOLD_ACTION_BUFF					= 3			# Buff

# 客户端陷阱形状定义
TRAP_SHAPE_RECTANGLE					= 0			# 陷阱方体范围
TRAP_SHAPE_CIRCULAR						= 1			# 陷阱球体范围
TRAP_SHAPE_CYLINDER						= 2			# 陷阱圆柱体范围

#------------------------怪物行为分类----------------------------------
BEHAVIOUR_SYS							= 1
BEHAVIOUR_COMMON						= 2
BEHAVIOUR_LOOP							= 3


MAX_TAKEITEM_AMOUNT						= 999999	#物品最大携带数量


#------------------------添加物品失败或成功的原因---------------------
ADDITEM_NO_DEFINE						= 100		# 未定义，作初始值
ADDITEM_STACK_SUCCESS					= 0			# 叠加添加物品成功
ADDITEM_NEWGRID_SUCCESS					= 1			# 使用新格子添加物品成功
ADDITEM_MULTISTACK_SUCCESS				= 2			# 拆分叠加成功
ADDITEM_MULTISTACK_NEWGRID_SUCCESS		= 3			# 拆分叠加加使用新格子成功
ADDITEM_OTHER_SUCCESS					= 4			# 其它添加成功
ADDITEM_UNIQUE_FAILED					= 10		# 添加唯一物品失败，表现自己已经有一个唯一的物品在背包或仓库中
ADDITEM_MAXTAKELIMIT_FAILED				= 11		# 表示超过最大携带数量，添加失败
ADDITEM_NONEWGRID_FAILED				= 12		# 表示没有新格子来添加物品
ADDITEM_OTHER_FAILED					= 13		# 其它添加失败

#添加成功的原因
ADD_SUCCESS_REASON_LIST = [ADDITEM_STACK_SUCCESS, ADDITEM_NEWGRID_SUCCESS, ADDITEM_MULTISTACK_SUCCESS, ADDITEM_MULTISTACK_NEWGRID_SUCCESS, ADDITEM_OTHER_SUCCESS]

#--------------------------背包锁状态------------------------------------
UNLOCK_KB_WITHOUT_PW					= 0			# 背包无密码背包未锁定
UNLICK_KB_WITH_PW						= 1			# 背包有密码未锁定
LOCK_KB_WITH_PW							= 2			# 背包有密码锁定

UNLOCK_TIMELIMIT_LOGIN					= 2*60				# 角色上线后开始计时，2分钟内不允许解锁
RESET_KB_PW_TIMELIMIT					= 7*24*60*60		# 重置密码7天解锁

RESET_KBPW_NONE							= 0			# 未重置背包密码状态
RESET_KBPW_NOW							= 1			# 重置背包密码状态

#--------------------------背包操作限制的定义
KB_OPRATOR_CAN_GO						= 0			# 可能继续执行操作
KB_OPRATOR_PW_LOCK						= 1			# 由于安全锁，禁止操作
KB_OPRATOR_SYSTEM_LOCK					= 2			# 由于交易过程的系统锁，禁止操作

MAX_HP_FOR_GM							= 999999999			# /full命令的设定值
MAX_MP_FOR_GM							= 999999999			# /full命令的设定值


#-------------------------------奖励类型--------------------------------
REWARD_TYPE_NOTHING						= "nothing"			# 空
REWARD_TYPE_MONEY						= "money"			# 金币奖励
REWARD_TYPE_EXP							= "exp"				# 经验奖励
REWARD_TYPE_ITEM						= "item"			# 物品奖励
REWARD_TYPE_XIUWEI						= "xiuwei"			# 修为奖励
REWARD_TYPE_POTENTIAL					= "potential"		# 潜能奖励 
REWARD_TYPE_BANGGONG					= "tongContribute"	# 帮贡奖励
REWARD_TYPE_TONG_MONEY					= "tongMoney"		# 帮会资金奖励
REWARD_TYPE_FEATS						= "feats"			# 功勋奖励
REWARD_TYPE_MORALE						= "campMorale"		# 气运奖励
REWARD_TYPE_CREWARD						= "child"			# 子奖励表
REWARD_TYPE_EXP_BL						= "exp_bl"			# 1倍基准经验
REWARD_TYPE_POTENTIAL_BL				= "potential_bl"	# 1倍基准潜能
REWARD_TYPE_XIUWEI_BL					= "xiuwei_bl"		# 1倍基准修为
REWARD_TYPE_MONEY_BL					= "money_bl"		# 1倍基准金币
REWARD_TYPE_BINDMONEY_BL				= "bindmoney_bl"	# 1倍基准绑币
REWARD_TYPE_BUFF						= "buff"			# buff奖励
REWARD_TYPE_BARRACKSEXP 				= "barracksExp"		# 养兵经验
REWARD_TYPE_INTEGRAL					= "integral"		# 金精（石狩猎场积分）
REWARD_TYPE_PSIONIC						= "psionic"			# 灵能
REWARD_TYPE_EXPLOIT						= "exploit"			# 军功
REWARD_TYPE_TITLE						= "title"			# 称号
REWARD_TYPE_BINDMONEY					= "bindmoney"		# 绑金
REWARD_TYPE_XIANSHI						= "xianshi"			# 仙石
REWARD_TYPE_LINGSHI						= "lingshi"			# 灵石
REWARD_TYPE_XUANSHI						= "xuanshi"			# 玄石


#-------------------------------奖励集合数据类型--------------------------------
REWARD_DATA_TYPE_NORMAL					= "normal"	# 通用的奖励数据
REWARD_DATA_TYPE_EQUIP					= "equip"	# 装备奖励
REWARD_DATA_TYPE_QUEST					= "quest"	# 任务奖励


#-------------------------------队伍拾取分配方式---------------------------------
TEAM_PICKUP_TYPE_FREEDOM				= 1			# 自由拾取
TEAM_PICKUP_TYPE_TEAM					= 2			# 队伍拾取(掷点分配)
TEAM_PICKUP_TYPE_AUCTION				= 3			# 队伍拍卖
TEAM_PICKUP_TYPE_CAPTAIN				= 4			# 队长分配


#-------------------------------帮会拾取分配方式---------------------------------
TONG_PICKUP_TYPE_FREEDOM				= 1			# 自由拾取
TONG_PICKUP_TYPE_RALLDOM				= 2			# 掷点分配
TONG_PICKUP_TYPE_AUCTION				= 3			# 竞拍分配
TONG_PICKUP_TYPE_LEADER					= 4			# 帮主分配

#------------------------------摆摊--------------------------------
STALL_SELL_ITEM							= 0			# 出售商品
STALL_COLLECTION_ITEM					= 1			# 收购商品

#ShopMall Type
SHOP_TYPE_GIFT							= 0			# 减负礼包
SHOP_TYPE_XIANSHI						= 1			# 仙石商城
SHOP_TYPE_LINGSHI						= 2			# 灵石商城
SHOP_TYPE_XUANSHI						= 3			# 玄石商城

#-----------------------购买商城商品使用货币的类型---------------------
SHOP_MONEY_TYPE_XIANSHI					= 0			# 仙石
SHOP_MONEY_TYPE_LINGSHI					= 1			# 灵石
SHOP_MONEY_TYPE_XUANSHI					= 2			# 玄石

#-----------------------完成商品购买的状态-------------------------------
SHOP_GOODS_NONE							= 0			# 表示未购买
SHOP_GOODS_PERMANENT					= 1			# 表示永久购买
SHOP_GOODS_TEMPORARY					= 2			# 表示临时购买

#---------------------赠送好友物品数据的状态-----------------------
GIVING_GOODSDATA_WAIT_STATE				= 0			# 等待处理的
GIVING_GOODSDATA_OVERDUE_STATE			= 1			# 过期
GIVING_GOODSDATA_RECEIVE_STATE			= 2			# 好友接收
GIVING_GOODSDATA_WITHDRAW_STATE			= 3			# 玩家撤回赠送
GIVING_GOODSDATA_REFUSE_STATE			= 4			# 好友拒绝接收

#--------------------赠送好友物品数据同步人数---------------------
GIVING_GOODSDATA_DATA_SHARED_TO_NULL		= 0			# 两者都没有同步
GIVING_GOODSDATA_DATA_SHARED_TO_GIVING		= 1			# 同步给赠送者
GIVING_GOODSDATA_DATA_SHARED_TO_BY_GIVING	= 2			# 同步给被赠送者
GIVING_GOODSDATA_DATA_SHARED_TO_BOTH		= 3			# 两者都同步

#--------------------赠送好友的物品数据是否清除------------
GIVING_GOODSDATA_CLEAR_NO				= 0
GIVING_GOODSDATA_CLEAR_YES				= 1

AGREE_TO_RECEIVEGIVINGGOODSDATA			= 1			# 同意接收赠送的物品数据
REFUSE_TO_RECEIVEGIVINGGOODSDATA		= 0			# 拒绝接收赠送的物品数据
WITHDRAW_TO_GIVEGOODSDATA				= 2			# 玩家撤回赠送的物品数据

#------------------------灵石寄售--------------------------------------
LINGSHI_TRADE_SELL						= 0			# 出售
LINGSHI_TRADE_COLLECT					= 1			# 收购


#--------------------------技能响应事件------------------------------------
# 技能事件触发类型
SKILL_EVENT_TRIGGER_CASTER_INTERRUPT	= 0			# 施法者触发 中断技能
SKILL_EVENT_TRIGGER_RECEIVER_INTERUPT	= 1			# 受术目标触发 施法者中断技能

# 技能事件类型
SKILL_EVENT_ON_DIE						= 0			# 死亡事件
SKILL_EVENT_STATE_CHANGE				= 1			# 基础状态改变事件
SKILL_EVENT_ACT_WORD_CHANGE				= 2			# 开关状态改变事件
SKILL_EVENT_PLAN_CUSTOM					= 3			# 自定义事件
SKILL_EVENT_STORY_END					= 4			# 镜头结束事件
SKILL_EVENT_BULLET_COLLISION			= 5			# 子弹碰撞事件
SKILL_EVENT_STOP_FLY					= 6			# 飞行传送结束
SKILL_EVENT_ROLE_MOVE_CHANGE			= 7			# 玩家移动模式（主动或被动）改变事件
SKILL_EVENT_NPC_MOVE_CHANGE				= 8			# NPC移动改变事件
SKILL_EVENT_CURE						= 9			# 治疗事件
# SKILL_EVENT_CRITICAL					= 10		# 暴击事件
# SKILL_EVENT_PARRY						= 11		# 招架事件
SKILL_EVENT_HURT						= 12		# 伤害事件
SKILL_EVENT_PROCESS						= 13		# 技能主流程事件
SKILL_EVENT_SPACE_CHANGE				= 14		# 地图改变事件
SKILL_EVENT_SHIELD_BROKEN				= 15		# 护盾破碎事件
SKILL_EVENT_DESTROY						= 16		# 销毁事件
SKILL_EVENT_PER_SECOND_TRIGGER			= 17		# 每秒触发事件
SKILL_EVENT_ADDITEM						= 18		# 玩家物品增加事件
SKILL_EVENT_REMOVEITEM					= 19		# 玩家物品删除事件
SKILL_EVENT_INITIATIVE_STOP_SKIL		= 20		# 玩家主动停止技能事件
SKILL_EVENT_INITIATIVE_STOP_BUFF		= 21		# 玩家主动停止Buff事件
SKILL_EVENT_QTE							= 22		# QTE事件
SKILL_EVENT_BUFFGUEST_END				= 23		# 主从buff之从buff结束事件
BUFF_EVENT_PROCESS						= 24		# Buff流程事件
SKILL_EVENT_SKILL_POSTURE_CHANGE		= 25		# 心法状态改变时
SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL	= 26		# 中断变身类buff事件
SKILL_EVENT_EFFECT_STATE_CHANGE			= 27		# 效果状态改变事件
SKILL_EVENT_REQUEST_ACTION				= 28		# 玩家申请行为事件（移动 使用物品，使用技能，幻兽相关操作，NPC/场景物件交互等）
SKILL_EVENT_ROLE_DROP_GLEDE				= 29		# 玩家掉下老鹰
SKILL_EVENT_PET_ACTIVE					= 30		# 幻兽出战
SKILL_EVENT_ROLE_END_FALL				= 31		# 玩家下落碰到物体
SKILL_EVENT_PROPERTY_PERCENT_CHANGE		= 32		# "资源存量改变时"技能事件
SKILL_EVENT_ROLE_PLMJ_CARRIER			= 33		# CST-6262 蟠龙秘境 玩家上下载具
SKILL_EVENT_ROLE_JUMP_STATE_CHANGE		= 34		# 玩家跳跃模式（主动或被动）改变事件
SKILL_EVENT_ROLE_PARACHUTE				= 35		# 玩家跳伞事件
SKILL_EVENT_YCJMD_RCLICK				= 36		# 勇闯绝命岛进入鼠标右击事件
SKILL_EVENT_ADD_ENERGY					= 37		# 充能事件
SKILL_EVENT_ROLE_YCJMD_CARRIER			= 38		# CST-13454 大荒战场 玩家上下载具



# 技能事件 子事件类型
SKILL_EVENT_CASTER_CURE					= 0			# 施法者治疗事件
SKILL_EVENT_RECEIVER_CURE				= 1			# 受术者被治疗

SKILL_EVENT_CASTER_HURT					= 0			# 伤害事件
SKILL_EVENT_RECEIVER_HURT				= 1			# 被伤害事件

SKILL_EVENT_SKILL_END					= 0			# 施法结束时事件
SKILL_EVENT_SKILL_BEGIN					= 1			# 施法开始时事件
SKILL_EVENT_SKILL_INTERRUPT				= 2			# 施法中断时事件

BUFF_EVENT_BUFF_REMOVE					= 0			# Buff注册事件
BUFF_EVENT_BUFF_ADD						= 1			# Buff注销事件
BUFF_EVENT_BUFF_BEGIN					= 2			# Buff开始事件
BUFF_EVENT_BUFF_INTERRUPT				= 3			# Buff中断事件
BUFF_EVENT_BUFF_END						= 4			# Buff结束事件

SKILL_EVENT_CASTER_DIE					= 0			# 施法者的击杀时事件
SKILL_EVENT_RECEIVER_DIE				= 1			# 受术者的被击杀时事件

# 玩家申请行为事件 子事件类型
SKILL_EVENT_ACTION_TYPE_MOVE			= 1			# 主动移动行为
SKILL_EVENT_ACTION_TYPE_CAST			= 2			# 使用技能行为
SKILL_EVENT_ACTION_TYPE_ITEM			= 3			# 使用物品行为
SKILL_EVENT_ACTION_TYPE_TALK			= 4			# 交互行为
SKILL_EVENT_ACTION_TYPE_PET				= 5			# 幻兽操作行为


#------------------------SpellBox交互条件事件类型--------------------------------------
SPELL_BOX_LISTEN_EVENT_QUEST_CHANGE					= 1
SPELL_BOX_LISTEN_EVENT_ADD_ITEM						= 2
SPELL_BOX_LISTEN_EVENT_KILL_BOSS					= 3
SPELL_BOX_LISTEN_EVENT_SPACE_STAGE_COMPLETE			= 4
SPELL_BOX_LISTEN_EVENT_IS_CAPTAIN					= 5
SPELL_BOX_LISTEN_EVENT_HAS_BUFF						= 6
SPELL_BOX_LISTEN_EVENT_IS_INTERACT					= 7
SPELL_BOX_LISTEN_EVENT_HAS_ENTITY					= 8
SPELL_BOX_LISTEN_EVENT_HAS_CAMP_GOSSIP				= 9
SPELL_BOX_LISTEN_EVENT_IS_THIS_CAMP					= 10
SPELL_BOX_LISTEN_EVENT_NOT_IN_AREA					= 11
SPELL_BOX_LISTEN_EVENT_BXZZ							= 12
SPELL_BOX_LISTEN_EVENT_HAS_NOTIFY					= 13
SPELL_BOX_LISTEN_EVENT_CREATOR						= 14
SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP				= 15
SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP				= 15
SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT				= 16
SPELL_BOX_LISTEN_EVENT_LINGTIAN						= 17
#------------------------SpellBox交互结果类型------------------------------------------
SPELL_BOX_RESULT_GETKEY					= 0			# 获得宝箱钥匙
SPELL_BOX_RESULT_ADDEXP					= 1			# 获得经验
SPELL_BOX_RESULT_ADDBUFF				= 2			# 获得一定时间的buff
SPELL_BOX_RESULT_CREATEMONSTER			= 3			# 小宝箱消失创建怪物
SPELL_BOX_RESULT_ADDITEM				= 4			# 获得物品
SPELL_BOX_RESULT_ADD_INTEGRAL				= 5			# 获得金精（晶石狩猎场）

SPELL_BOX_RESULT_LIST = [SPELL_BOX_RESULT_GETKEY, SPELL_BOX_RESULT_ADDEXP, SPELL_BOX_RESULT_ADDBUFF, SPELL_BOX_RESULT_CREATEMONSTER, SPELL_BOX_RESULT_ADDITEM]
SPELL_BIG_BOX										= 40000001	# 大宝箱
SPELL_BOX_RESULT_AFTER_THE_NUMBER_OF_GETKEY			= 10
SPELL_BOX_NOT_PLAYERS_INTERACTIVE					= 0			# 不能多人交互

RE_TRIGGER_NEAR_TRAP_RANGE				= 80.0		# 重新触发陷阱时，entity的搜索半径

#--------------怪物出场动作------------------------------------------
MONSTER_APPEAR_MOVE_SPEED				= 2000.0	# 怪物出场水平位移速度
MONSTER_APPEAR_MOVE_GRAVITY				= 8000.0	# 怪物出场重力加速度
MONSTER_APPEAR_ACTION_TIME				= 0.5		# 怪物出场起跳动作时间
MONSTER_APPEAR_END_ACTION_TIME			= 1.5		# 怪物出场結束动作时间


#怪物爆尸类型
MONSTER_DEAD_EFFECT_TYPE_NORMAL			= 0			# 不爆尸
MONSTER_DEAD_EFFECT_TYPE_ALWAYS			= 1			# 必然触发型
MONSTER_DEAD_EFFECT_TYPE_DAMAGE			= 2			# 伤害触发型
MONSTER_DEAD_EFFECT_TYPE_MORTUARY		= 3			# 停尸效果型


#--------------------称号--------------------------
TITLE_NONE								= 0			# 无称号
CAMP_TAOISM_VEV_TITLE					= 4			# 仙道尊者
CAMP_FENG_MING_VEV_TITLE				= 5			# 凤鸣之主
CAMP_DEMON_VEV_TITLE					= 7			# 魔道尊者


# 真龙棋局状态
ZHEN_LONG_QI_JU_BLACK_STATE				= 1			# 黑棋状态
ZHEN_LONG_QI_JU_WHITE_STATE				= 2			# 白棋状态

# 组队邀请类型
TEAM_INVITE_TYPE_CREATE_TEAM			= 1			# 邀请新建队伍（双方没有队伍）
TEAM_INVITE_TYPE_JOIN_TEAM				= 2			# 邀请组队（我有队伍，对方没有队伍）

#取消组队跟随原因
TF_CANCEL_REASON_INVALID				= 1			# 不合法（找不到目标或者卡住）
TF_CANCEL_REASON_TO_FAR					= 2			# 离领导者太远
TF_CANCEL_ACTIVE_CANCEL					= 3			# 主动取消
TF_CANCEL_STATE_LIMIT					= 4			# 状态限制（如死亡、被定身等）

#-------------------副本结算评分项相关事件-----------------
SPACE_STMT_SPACE_SUCCESS				= 1			# 通关
SPACE_STMT_RECEIVE_DAMAGE				= 2			# 接受伤害
SPACE_STMT_ROLE_DIE						= 3			# 死亡
SPACE_STMT_TRIGGER_BOX					= 4			# 触发箱子
SPACE_STMT_CHILD_SPACE_FAILURE			= 5			# 子副本失败

#---------玩家之间交易------------------------
TRADE_DISTANCE							= 10.0		# 交易距离
TRADE_OVERTIME_LIMIT					= 15.0		# 交易申请超时限制

TRADE_STATE_NULL						= 0			# 没有交易状态
TRADE_STATE_INVITE						= 1			# 被邀请交易状态
TRADE_STATE_WAIT						= 2			# 等待玩家确认交易状态
TRADE_STATE_BEGIN						= 3			# 交易开始状态
TRADE_STATE_LOCK						= 4			# 物品锁定状态
TRADE_STATE_SURE						= 5			# 交易确定状态

#	交换对象
TRADE_OBJ_MONEY							= 1			# 金钱
TRADE_OBJ_ITEM							= 2			# 物品
TRADE_OBJ_POTENTIAL						= 3			# 潜能
TRADE_OBJ_DAOHENG						= 4			# 道行
TRADE_OBJ_SKILL							= 5			# 技能

#-------------------------帮会----------------------------------------
#帮会权限类型
TONG_GRADE_INVITE			=  0		# 邀请人
TONG_GRADE_REQUEST			=  1		# 管理申请人
TONG_GRADE_KICK				=  2		# 踢人
TONG_GRADE_APPOINT			=  3		# 任免
TONG_GRADE_NOTICE			=  4		# 发布公告
TONG_GRADE_SHUTUP			=  5		# 禁言
TONG_GRADE_QUEST			=  6		# 发任务
TONG_GRADE_DEVELOP			=  7		# 研发
TONG_GRADE_NAGUAL			=  8		# 神兽
TONG_GRADE_BUILDING			=  9		# 建筑
TONG_GRADE_ALLY				= 10		# 结盟
TONG_GRADE_MAIL				= 11		# 邮件
TONG_GRADE_CONVENE			= 12		# 召集帮众
TONG_GRADE_ROB				= 13		# 帮会掠夺
TONG_GRADE_MONEY			= 14		# 帮会资金
TONG_GRADE_STORAGE			= 15		# 帮会仓库
TONG_GRADE_RENAME			= 16		# 更改职位名称
TONG_GRADE_UPGRADE			= 17		# 帮会升级

TONG_SYSTEM_GRADE			= 1			# 系统默认权限
TONG_DEFAULT_GRADE			= 2			# 可操作权限
TONG_FORBID_GRADE			= 3			# 禁止操作权限

TONG_TITLE_1				= 0			# 帮主
TONG_TITLE_2				= 1			# 副帮主
TONG_TITLE_3				= 2			# 军师
TONG_TITLE_4				= 3			# 长老
TONG_TITLE_5				= 4			# 5星帮众
TONG_TITLE_6				= 5			#4星帮众
TONG_TITLE_7				= 6			# 3星帮众
TONG_TITLE_8				= 7			# 2星帮众
TONG_TITLE_9 			= 8			# 1星帮众


# 帮会建筑类别
TONG_BUILDING_TYPE_YSDT		= 0			# 议事大厅
TONG_BUILDING_TYPE_SSD		= 1			# 神兽殿
TONG_BUILDING_TYPE_CK		= 2			# 仓库
TONG_BUILDING_TYPE_TJP		= 3			# 铁匠铺
TONG_BUILDING_TYPE_SD		= 4			# 商店
TONG_BUILDING_TYPE_YJY		= 5			# 研究院

# 帮会神兽类别
TONG_SHENSHOU_TYPE_1		= 1			# 青翼龙王
TONG_SHENSHOU_TYPE_2		= 2			# 白毛虎神
TONG_SHENSHOU_TYPE_3		= 3			# 玄武圣君
TONG_SHENSHOU_TYPE_4		= 4			# 炽焰朱雀

# 帮会技能类型
TONG_SKILL_ROLE				= 1			# 角色技能
TONG_SKILL_PET				= 2			# 幻兽技能

# 帮会玩法类型
TONG_PLAY_TYPE_SIGN			= 1			# 帮会签到
TONG_PLAY_TYPE_DAILY		= 2			# 帮会日常任务
TONG_PLAY_TYPE_ONLINE		= 3			# 日常在线
TONG_PLAY_TYPE_CHAT			= 4			# 帮会聊天
TONG_PLAY_TYPE_COPY			= 5			# 帮会副本

# 帮会事件类型
TONG_EVENT_JOIN					= 0			# 帮会加入事件
TONG_EVENT_CREATE				= 1			# 帮会创建事件
TONG_EVENT_LEAVE				= 2			# 帮会离开事件
TONG_EVENT_TICK					= 3			# 帮会踢人事件
TONG_EVENT_APPOINT				= 4			# 帮会任命事件
TONG_EVENT_RECALL				= 5			# 帮会罢免事件
TONG_EVENT_DONATE				= 6			# 帮会捐献事件
TONG_EVENT_SUB_ACTIVITY			= 7			# 帮会扣除活跃度事件
TONG_EVENT_DOWN_GRADE_NOTICE	= 8			# 帮会降级警告事件
TONG_EVENT_DOWN_GRADE			= 9			# 帮会降级事件
TONG_EVENT_UP_GRADE				= 10		# 帮会升级事件
TONG_EVENT_SAFE_TIME_NOTICE		= 11		# 帮会安全期警告事件
TONG_EVENT_CHANGE_LEADER		= 12		# 帮会禅让帮主事件
TONG_EVENT_UPGRADE_BUILD		= 13		# 帮会建筑升级事件
TONG_EVENT_FORCE_CHANGE_LEADER	= 14		# 帮会系统强制替换帮主事件
TONG_EVENT_REASEARCH_SKILL_BEG	= 15		# 帮会技能研发开始事件
TONG_EVENT_REASEARCH_SKILL_SUC	= 16		# 帮会技能研发成功事件
TONG_EVENT_PROTECT_DAY_OVER_NORMAL=17		# 帮会7天保护期正常结束
TONG_EVENT_PROTECT_DAY_OVER_ADVAN =18		# 帮会7天保护期提前结束
TONG_EVENT_PROTECT_DAY_OVER_ONE	= 19		# 帮会升级后，获得1天保护期结束
TONG_EVENT_PROTECT_DAY_SUB_ONELEVEL = 20	# 一级帮会保护期减少事件

# 帮会仓库存储事件
TONG_STORE_EVENT_STORE		= 0			# 帮会仓库存入
TONG_STORE_EVENT_OBTAIN		= 1			# 帮会仓库取出

TONG_DISMISS_NORMAL			= 0			# 默认解散帮会
TONG_DISMISS_PROTECT_OVER	= 1			# 保护期结束，解散帮会
# ------------罡气状态---------------
GANG_QI_STATE_QI_YING					= 1			# 气盈
GANG_QI_STATE_QI_DUAN					= 2			# 气短
GANG_QI_STATE_QI_JIE					= 3			# 气竭
GANG_QI_STATE_QI_JUE					= 4			# 气绝

#------------------------物品使用限量周期限制--------------------
ITEM_USE_AMOUNT_FOREVER					= 1			# 永久
ITEM_USE_AMOUNT_DAY						= 2			# 每天
ITEM_USE_AMOUNT_WEEK					= 3			# 每周
ITEM_USE_AMOUNT_MONTH					= 4			# 每月

#------------------------Buff结束的原因-----------------------
BUFF_END_RESON_BY_TIME_OVER				= 1			# Buff持续时间结束
BUFF_END_RESON_BY_INTERRUPT				= 2			# Buff打断
BUFF_END_RESON_BY_REPLACE				= 3			# Buff顶替
BUFF_END_RESON_BY_OFFLINE				= 4			# 玩家下线

#----------------陷阱形状-----------------
TRAP_SHAPE_CIRCULAR						= 1			# 圆形
TRAP_SHAPE_SQUARE						= 2			# 方形（引擎陷阱形状：方形、无朝向）
TRAP_SHAPE_SPHERE						= 3			# 球形
TRAP_SHAPE_SECTOR						= 4			# 扇形

TRAP_SHAPE_LIST = [TRAP_SHAPE_CIRCULAR, TRAP_SHAPE_SQUARE, TRAP_SHAPE_SECTOR]

#---------------鱼饵类型------------------
FISH_BAIT_SMALL_TYPE					= 1			# 小型鱼饵
FISH_BAIT_MEDIUM_TYPE					= 2			# 中型鱼饵
FISH_BAIT_BIG_TYPE						= 3			# 大型鱼饵

#---------------活动副本晶石狩猎场 状态--------------------
SHT_ACTIVITY_STATE_FREE					= 1
SHT_ACTIVITY_STATE_SIGNUP				= 2
SHT_ACTIVITY_STATE_START				= 3

#---------------活动副本Key(用于GM命令)---------------------------------------
ACTIVITY_SPAR_HUNTING_SIGNUP			= "晶石狩猎场报名"
ACTIVITY_SPAR_HUNTING					= "晶石狩猎场开始"
ACTIVITY_CAMP_LING_MAI					= "灵脉战场"
ACTIVITY_CAMP_FROZEN_FIGHT				= "冰雪之战"
ACTIVITY_CAMP_YXLM						= "英雄王座"
ACTIVITY_YE_ZHAN_FENG_QI				= "血斗凤栖镇"
ACTIVITY_SHI_FANG_CHENG_SIGN_UP			= "十方城报名"
ACTIVITY_SHI_FANG_CHENG_START			= "十方城开始"
ACTIVITY_FIRST_TONG_STARCRAFT_SIGNUP	= "帮会争霸第一场报名"
ACTIVITY_FIRST_TONG_STARCRAFT_START		= "帮会争霸第一场开始"
ACTIVITY_CAMP_RANDOM_FIT				= "阵营战场随机匹配"
ACTIVITY_BHZB_SIGN_UP 					= "帮会争霸报名"
ACTIVITY_BHZB_START 					= "帮会争霸开始"
ACTIVITY_TONG_PLUNDER_SIGN_UP 		= "帮会掠夺战报名"
ACTIVITY_TONG_PLUNDER_START 		= "帮会掠夺战开始"
ACTIVITY_TONG_PLUNDER_LOCK_SHOP 	= "帮会掠夺战锁定帮会仓库"
ACTIVITY_TONG_PLUNDER_SHOP_SELL	= "帮会掠夺战商店售卖"
ACTIVITY_GCZ_SIGNUP 					= "攻城战报名"
ACTIVITY_GCZ_MATCH 						= "攻城战匹配"
ACTIVITY_GCZ_ENTER 						= "攻城战进入"
ACTIVITY_GCZ_START 						= "攻城战开始"
ACTIVITY_BATTLE 						= "团队竞技"

#---------------玩家pk模式--------------------
PK_MODE_PEACE							= 1			# 和平模式
PK_MODE_CAMP							= 2			# 阵营模式
PK_MODE_RIGHTFUL						= 3			# 正义模式
PK_MODE_SLAUGHTER						= 4			# 恶意模式


#----------------玩家关系规则--------------
ROLE_RELATION_RULE_CAMP					= 1			# 阵营决定PVP关系
ROLE_RELATION_RULE_PKMODE				= 2			# PK模式决定PVP关系
ROLE_RELATION_RULE_PEACE				= 3			# 与其他玩家完全友好
ROLE_RELATION_RULE_ENEMY				= 4			# 用于个人竞技 与其他玩家都是敌对
ROLE_RELATION_RULE_TONG_STARCRAFT		= 5			# 用于帮会之间战斗 不同帮会之间敌对
ROLE_RELATION_RULE_TEAM_STARCRAFT		= 6			# 用于队伍之间战斗 不同队伍之间敌对
ROLE_RELATION_RULE_BLONG_SIDE 			= 7			# 用于攻守战
ROLE_RELATION_RULE_LHMJ					= 8			# 轮回秘境大地图

#----------------持有效果来源类型------------
HOLD_EFFECT_SOURCE_TYPE_SKILL			= 1			# SKILL
HOLD_EFFECT_SOURCE_TYPE_BUFF			= 2			# BUFF
HOLD_EFFECT_SOURCE_TYPE_FIX_ID			= 3			# 固定ID

#---------------与灵箭碰撞的类型--------------
COLLISION_TYPE_PLAYER					= 1			# 玩家
COLLISION_TYPE_SHIELD					= 2			# 化元盾 (其实是碰撞化元盾的光效)
COLLISION_TYPE_UNDERGROUND				= 3			# 地面 (实际是碰撞的是Static Mesh)

# --------------------------------------------------------------------
# 防沉迷
# --------------------------------------------------------------------
# 状态定义
WALLOW_STATE_COMMON						= 0			# 正常状态
WALLOW_STATE_HALF_LUCRE					= 1			# 收益减半
WALLOW_STATE_NO_LUCRE					= 2			# 收益为 0

# ----------------------------脱离卡死功能-------------------------------
#普通地图开启此功能(0:关闭；1：开启)
DISCONNECT_DEATH_SWITCH					= 1
 
#活动串参与返回值
ACTIVITY_BUNCH_RESULT_OK				= 0
ACTIVITY_BUNCH_RESULT_FULL				= 1			#人数已满
ACTIVITY_BUNCH_RESULT_NOT_IN_LIST		= 2			#不在名单


# ----------------------------交易------------------------------
#交易类型
TRADE_TYPE_NULL							= 0			# 无
TRADE_TYPE_NPC_SHOP						= 1			# NPC商店交易
TRADE_TYPE_ROLE							= 2			# 玩家之间交易
TRADE_TYPE_LEARN_SKILL					= 3			# 玩家技能学习
TRADE_TYPE_CREATE_TONG					= 4			# 创建帮会
TRADE_TYPE_ROLE_STALL					= 5			# 玩家摆摊交易
TRADE_TYPE_LEAR_TONG_SKILL				= 7			# 学习帮会技能
TRADE_TYPE_SHUFFLE_EQUIP				= 8			# 装备洗练
TRADE_TYPE_RECOST_EQUIP					= 9			# 装备重铸
TRADE_TYPE_INTENSIFY_EQUIP				= 10		# 装备强化
TRADE_TYPE_RESET_EQUIP					= 11		# 装备回火
TRADE_TYPE_OPEN_INTENSIFY_SAVE_SLOT		= 12		# 开启 装备备份栏位
TRADE_TYPE_SAVE_INTENSIFY_EQUIP			= 13		# 保存装备强化
TRADE_TYPE_RESET_INTENSIFY_EQUIP		= 14		# 还原装备强化
TRADE_TYPE_TRANSFER_EQUIP				= 15		# 装备传星
TRADE_TYPE_COMPOSE_EQUIP				= 16		# 装备打造
TRADE_TYPE_UNLOCK_PASSIVESKILLBAR		= 17		# 解锁被动技能栏栏位
TRADE_TYPE_ROLE_RARRACKS 				= 18		# 玩家兵营交易
TRADE_TYPE_FEED_PET						= 19		# 驯养原兽
TRADE_TYPE_EVOLUTION_PET				= 20		# 原兽进化为原兽
TRADE_TYPE_COMPOSE_TOOL					= 21		# 轮回秘境工具打造
TRADE_TYPE_QUENCHING_EQUIP				= 22		# 轮回秘境半成品淬炼
TRADE_TYPE_GENERATE_ORIGIN_PET			= 23		# 原兽入栏
TRADE_TYPE_JADE_UPGRADE					= 24		# 玲珑玉令升级
TRADE_TYPE_PRAY_EQUIP					= 25		# 祈福消耗
TRADE_TYPE_GET_JADE						= 26		# 获得玲珑玉令
TRADE_TYPE_BUILD_LINGQUAN				= 27		# 建造洞府
TRADE_TYPE_LINGQUAN_UPGRADE				= 28		# 升级灵泉消耗
TRADE_TYPE_ACCEPT_LBC_TASK				= 29		# 接取练兵场任务
TRADE_TYPE_REFRESH_TG_QUEST				= 30		# 刷新练兵场任务
TRADE_TYPE_OPEN_BATTLE_FORMATIONS		= 31		# 开启阵图
TRADE_TYPE_BARRACKS_REVIVE 				= 32 		# 天兵营复活
TRADE_TYPE_LEARN_PASSIVE_SKILL			= 33		# 玩家被动技能学习
TRADE_TYPE_REPAIR_DF_BUILD				= 34		# 修复洞府建筑
TRADE_TYPE_MYSTERIOUS_SHOP				= 35		# 神秘商人
TRADE_TYPE_LEARN_CHUANCHENG_SKILL		= 36		# 玩家传承技能学习


TRADE_PAY_ITEM_MONEY					= 1			# 支付金钱
TRADE_PAY_ITEM_CONTRIBUTE				= 2			# 支付帮贡
TRADE_PAY_ITEM_FEATS					= 3			# 支付功勋
TRADE_PAY_ITEM_POTENTIAL				= 4			# 支付潜能
TRADE_PAY_ITEM_CREATETONG				= 5			# 创建帮会流程
TRADE_PAY_ITEM_LEARNTONGSKILL			= 6			# 学习帮会技能流程
TRADE_PAY_ITEM_BUY_STALLGOODS			= 7			# 摆摊购买物品
TRADE_PAY_ITEM_SELL_STALLGOODS			= 8			# 摆摊出售物品
TRADE_PAY_ITEM_STONE					= 9			# 支付灵石、仙石
TRADE_PAY_ITEM_WASH_STONE				= 10		# 支付洗练石（洗练）
TRADE_PAY_ITEM_BLOOD_SYMBOL				= 11		# 支付血符（洗练）
TRADE_PAY_ITEM_RECAST_STONE				= 12		# 支付重铸宝珠（重铸）
TRADE_PAY_ITEM_RECAST_SYMBOL			= 13		# 支付重铸保护符（重铸）
TRADE_PAY_ITEM_NORMAL_CRYTAL			= 14		# 支付玄晶（强化）
TRADE_PAY_ITEM_MCOLOR_CRYTAL			= 15		# 支付五彩玄晶（强化）
TRADE_PAY_ITEM_SUPPER_CRYTAL			= 16		# 支付超级玄晶（强化）
TRADE_PAY_ITEM_GOODS_BY_ID				= 17		# 支付物品，根据物品ID
TRADE_PAY_ITEM_GOODS_BY_UID				= 18		# 支付物品，根据物品UID
TRADE_PAY_ITEM_BIND_GOODS_BY_ID			= 19		# 支付锁定物品，根据物品ID
TRADE_PAY_ITEM_UNBIND_GOODS_BY_ID		= 20		# 支付非锁定物品，根据物品ID
TRADE_PAY_ITEM_HH_SYMBOL				= 21		# 支付回火符(回火)
TRADE_PAY_ITEM_ZY_SYMBOL				= 22		# 支付正阳符(回火)
TRADE_PAY_ITEM_BD_SYMBOL				= 23		# 支付北斗符(回火)
TRADE_PAY_ITEM_ROLE_TRADE				= 24		# 玩家之间交易
TRADE_PAY_ITEM_MONEY_OR_XIANSHI			= 25		# 支付金钱/仙石
TRADE_PAY_ITEM_BIND_MONEY				= 26		# 支付绑定金钱
TRADE_PAY_ITEM_XIANSHI					= 27		# 支付仙石
TRADE_PAY_ITEM_FEED_PET					= 28		# 驯养原兽(获得经验或者降低原兽野性)
TRADE_PAY_ITEM_EVOLUTION_PET			= 29		# 原兽进化为幻兽
TRADE_PAY_ITEM_COMPOSE_TOOL				= 30		# 工具打造
TRADE_PAY_ITEM_GENERATE_ORIGIN_PET		= 31		# 原兽入栏
TRADE_PAY_ITEM_LING_NENG				= 33		# 消耗灵能
TRADE_PAY_ITEM_LHMJ_SHOP				= 34		# 轮回秘境商店
TRADE_PAY_ITEM_MONEY_AND_BINDMONEY		= 35		# 支付绑金和金钱（绑金优先）

#	交换目标
TRADE_TARGET_SYS						= 0			# 系统
TRADE_TARGET_ROLE						= 1			# 玩家
TRADE_TARGET_NPC						= 2			# NPC

# 交易流程
TRADE_PROCESS_TYPE_LOCK					= 1			# 锁定交易方
TRADE_PROCESS_TYPE_LOCK_TARGET			= 2			# 锁定交易目标
TRADE_PROCESS_TYPE_CHECK				= 3			# 交易条件检查
TRADE_PROCESS_TYPE_VERIFY				= 4			# 交易消耗品验证
TRADE_PROCESS_TYPE_SHOPPING				= 5			# 开始交易
TRADE_PROCESS_TYPE_UNLOCK				= 6			# 解锁交易方
TRADE_PROCESS_TYPE_UNLOCK_TARGET		= 7			# 解锁交易目标
TRADE_PROCESS_TYPE_BLOCK				= 8			# 交易堵塞

#-----------------法阵------------------------------------------------
#interactiveState
INTERACTIVE_STATE_CREATE		= 1			#创建状态
INTERACTIVE_STATE_OPEN			= 2			#开启状态
INTERACTIVE_STATE_INPROGRESS	= 3			#处理状态
INTERACTIVE_STATE_RESOLVED		= 4			#解决状态
INTERACTIVE_STATE_ACCEPT		= 5			#查收状态
INTERACTIVE_STATE_CLOSED		= 6			#关闭状态
INTERACTIVE_STATE_REOPEN		= 7			#重启状态

#EVENT ID
SPELLBOXADVANCED_EVENT_INTERACTIVE = 1

#-----------------游戏排行榜------------------------------------------------
GAME_RANKING_TYPE_LEVEL			= 0			# 等级排行榜
GAME_RANKING_TYPE_COMBAT		= 1			# 战力排行榜
GAME_RANKING_TYPE_MONEY			= 2			# 财富排行旁
GAME_RANKING_TYPE_WEAPON		= 3			# 神器排行榜


#------------------------------------------------------------------------
#邮件
# 信件发送者类型
MAIL_SENDER_TYPE_PLAYER			= 1			# 玩家寄信
MAIL_SENDER_TYPE_SYS			= 2			# 系统寄信
MAIL_SENDER_TYPE_GM				= 3			# GM寄信
MAIL_SENDER_TYPE_RETURN			= 4			# 退信



# 切磋状态
#-----------------------------------------------------------------------
COMPETE_NONE					= 0			# 切磋默认状态
COMPETE_INVITE					= 1			# 切磋邀请状态
COMPETE_BEINVITE				= 2			# 切磋被邀请状态
COMPETE_READY					= 3			# 切磋准备状态
COMPETE_FIRE					= 4			# 切磋进行状态


#帮会争霸第三场
TONG_BELONG_RED_SIDE			= 0			# 帮会属于红方
TONG_BELONG_BLUE_SIDE			= 1			# 帮会属于蓝方
TONG_BELONG_NONE_SIDE			= 2			# 帮会不属于任何一方


#负载均衡相关
GLOBALDATAPREFIX_CELLAPP			= "CELLAPP_"
#技能相关脚本类型
SCRIPT_TYPE_SKILL				= 1			# 技能脚本
SCRIPT_TYPE_BUFF				= 2			# Buff脚本


#英雄王座小兵的分布
YXLM_SOLDIER_UP			= 1		#上路
YXLM_SOLDIER_CENTER		= 2		#中路
YXLM_SOLDIER_DOWN		= 3		#下路

#英雄王座塔的分布
YXLM_TOWER_UP			= 0		# 上路
YXLM_TOWER_CENTER		= 1		# 中路
YXLM_TOWER_DOWN			= 2		# 下路
YXLM_TOWER_BASE			= 3		# 基地


#重新计算战斗力的原因
CALC_COMBAT_POWER_REASON_DEFAULT			= 0			# 默认值
CALC_COMBAT_POWER_REASON_EQUIP				= 1			# 更换装备
CALC_COMBAT_POWER_REASON_PROP				= 2			# 自身属性变化(玩家永久性战力被动提升或降低,被动技能的学习（人物被动技能、帮会被动技能,人物等级提升导致的属性变化（等级包含玩家等级、境界）)
CALC_COMBAT_POWER_REASON_TITLE				= 3			# 称号
CALC_COMBAT_POWER_REASON_UPGRADE			= 4			# 升级

#----------------------------------------------------------------------
#点卡寄售(充值处理)
#-----------------------------------------------------------------------
RECHANGE_OVERTIME_FAILED					= -1		# 超时错误
RECHANGE_SUCCESS							= 0			# 点卡寄售成功
RECHANGE_NO_OR_PWD_FAILED					= 1			# 卡号或密码错误
RECHANGE_USED_FAILED						= 2			# 已使用的卡
RECHANGE_ACCOUNT_NOT_ACTIVITIED_FAILED		= 3			# 帐号未在该区激活
RECHANGE_ACCOUNT_NOT_HAVE_FAILED			= 4			# 帐号不存在
RECHANGE_FAILED								= 5			# 充值失败
RECHANGE_MD5_FAILED							= 6			# MD5校验失败
RECHANGE_PARAMS_FAILED						= 7			# 参数不完整
RECHANGE_SERVER_NAME_FAILED					= 8			# 不存在的服务器名
RECHANGE_OVER_DUPLICATE_FAILED				= 9			# 定单号重复
RECHANGE_TEN_YUAN							= 10		# 10元面值的卡
RECHANGE_IP_FAILED							= 11		# IP错误，服务器中文名和服务器的IP对应不上
RECHANGE_ACCOUNT_MSG_FALIED					= 12		# 获取帐号信息失败
RECHANGE_CARD_LOCKED_CARD					= 13		# 已封号的卡
RECHANGE_LOGGED_FALID						= 14		# 写入充值日志失败
RECHANGE_CARD_NOT_EXIST_CARD				= 15		# 卡不存在 或 卡未激活
RECHANGE_SEND_YUANBAO_FAILED				= 16		# 操作成功，但是发放元宝失败
RECHANGE_THIRTY								= 30		# 30元面值的卡
RECHANGE_CARD_VALUE_FAILED					= 17		# 面值不符

#----------------------------------------------------------------------
#点卡寄售(超时处理)
#----------------------------------------------------------------------
OVERTIME_OVERTIME_FAILED					= -1		# 超时错误
OVERTIME_RECHANGE_SUCCESS					= 0			# 超时检测充值成功
OVERTIME_RECHANGE_FAILED					= 1			# 超时检测充值错误
OVERTIME_NO_ORDER_FAILED					= 2			# 超时没有这个订单


#-----------------------------------------------------------------------
#背包无法承载的奖励类型
#-----------------------------------------------------------------------
REMAIN_ITEM_SPACE_COPY						= 0			#背包已满，副本奖励道具有剩余
REMAIN_ITEM_GIFT							= 1			#背包已满，礼包奖励道具有剩余
REMAIN_ITEM_ACTIVITY						= 2			#背包已满，活动奖励道具有剩余
REMAIN_ITEM_QUEST							= 3			#背包已满，任务奖励道具有剩余
REMAIN_ITEM_DROPBOX							= 4			#背包已满，拾取宝箱道具有剩余
REMAIN_ITEM_TONG_TIAN_TA					= 5			# 通天塔奖励
REMAIN_ITEM_FENGCE_GIFT						= 7			#封测礼包


#---------------------转向原因-------------------------------
REASON_CHANGE_DIR_VOLUNTARY				= 0		#主动转向
REASON_CHANGE_DIR_FORCE					= 1		#被动转向
#----------------------------------------------------------------------
SERVER_INIT_STATE= "SERVER_INIT_STATE"			#服务器初始化状态标识字段


#----------------------jumpState----------------------------
JUMP_SHOW_STATE_STAND					= 0		# 0-非跳跃状态
JUMP_SHOW_STATE_SJUMP					= 1		# 1-原地起跳跃状态
JUMP_SHOW_STATE_MJUMP				= 2			# 2-跑着起跳跃状态
JUMP_SHOW_STATE_TWO_SJUMP			= 3			# 3-二段原地起跳跃状态
JUMP_SHOW_STATE_TWO_MJUMP			= 4			# 4-二段跑着起跳跃状态
JUMP_SHOW_STATE_THREE_SJUMP			= 5			# 5-三段原地起跳跃状态
JUMP_SHOW_STATE_THREE_MJUMP			= 6			# 6-三段跑着起跳跃状态
JUMP_SHOW_STATE_AIR_UP					= 7		# 7-上升状态
JUMP_SHOW_STATE_AIR_DOWN				= 8		# 8-下降状态
JUMP_SHOW_STATE_SLAND					= 9		# 9-原地着陆状态
JUMP_SHOW_STATE_MLAND				= 10		# 10-跑着着陆状态
JUMP_SHOW_STATE_FLOAT					= 11	# 11-浮空状态
JUMP_SHOW_STATE_PASSIVE				= 12		# 12-被动跳跃状态

#--------------------活动提醒类型----------------------------------------
ACTIVITY_NO_REMAIND			= 0			# 不提醒
ACTIVITY_OPENING				= 1			# 开启时
ACTIVITY_BEFORE_FIVE_MINUTES	= 2			# 提前5分钟
ACTIVITY_BEFORE_TEN_MINUTES		= 3			# 提前10分钟
ACTIVITY_BEFORE_HALF_AN_HOUR	= 4			# 提前半个小时

#活动令牌前缀
ACTIVE_KEY_ID		= "ACTIVE_KEY_ID"
ACTIVE_PRE_STR		= "ACTIVE_PRE_STR_"

#--------------------兵临天下  兵营兵种类型-----------------------
BARRACKS_SOLDIER_COMMON_TYPE = 0	#兵种
BARRACKS_SOLDIER_GUARD_TYPE = 1		#亲卫

#-------------------云梯 状态---------------------------------------
AERIAL_LADDER_STATE_FOLLOWER 		= 0 	#跟随
AERIAL_LADDER_STATE_BUILD 	 		= 1 	#搭建中
AERIAL_LADDER_STATE_BUILD_SUCCESS 	= 2 	#搭建成功

#-------------------轮回秘境工具打造-----------------------------------
COMPOSE_TOOL_NORMAL				= 1			# 工具打造
COMPOSE_TOOL_GREEN_EQUIP		= 2			# 绿装打造
COMPOSE_TOOL_TRIPOD				= 3			# 乾坤鼎打造

# 不要修改数值，因为保存到数据库了
SPACE_TYPE_NONE					= 0			# 无
SPACE_TYPE_PRIVATE				= 1			# 洞府（私有）
SPACE_TYPE_PUBLIC				= 2			# 仙府（公有）
SPACE_TYPE_HIGH_DF				= 3			# 高级洞府（私有）

CHANLLENGE_TYPE_NONE			= 0			# 无
CHANLLENGE_TYPE_COMMON			= 1			# 可挑战状态
CHANLLENGE_TYPE_ACCEPT			= 2			# 已接受挑战
CHANLLENGE_TYPE_CANNOT			= 3			# 不可挑战
CHANLLENGE_TYPE_REPAIR			= 4			# 修复中

LHMJ_BUIILD_LING_QUAN			= 1			# 灵泉
LHMJ_BUIILD_GONG_FANG			= 2			# 工坊
LHMJ_BUIILD_QIAN_KU_DING		= 3			# 乾坤鼎
LHMJ_BUIILD_SHOU_LAN			= 4			# 兽栏
LHMJ_BUIILD_LING_TIAN			= 5			# 灵田

LHMJ_BUILD_STATE_NONE		= -1			# 未占领状态
LHMJ_BUILD_STATE_REQUEST	= 0				# 申请状态
LHMJ_BUILD_STATE_OCUPPY		= 1				# 占领状态
LHMJ_BUILD_STATE_IS_BUILD	= 2				# 正在建造
LHMJ_BUILD_STATE_READY		= 3				# 建造完成

CHANLLENGE_REPLY_NONE		= -1			# 没有回应
CHANLLENGE_REPLY_NO			= 0				# 拒绝挑战
CHANLLENGE_REPLY_YES		= 1				# 接受挑战
CHANLLENGE_REPLY_SYS_YES	= 2				# 系统默认应战

LHMJ_PLANT_STATE_NONE		= 0				# 没播种状态
LHMJ_PLANT_STATE_PLANT		= 1				# 种子成长状态
LHMJ_PLANT_STATE_MATURE		= 2				# 成熟状态（可收获）

# 洞府守卫
DONG_FU_GUARD_TYPE_DEFAULT	= 0				# 默认型(防守型)
DONG_FU_GUARD_TYPE_ATTACK	= 1				# 攻击型
DONG_FU_GUARD_TYPE_CONTROL	= 2				# 控制型

#---------------------CMonsterCategory------------------------------
NORMAL 		= 0
SOLDIER 	= 1
LEFT_GUARD 	= 2
RIGHT_GUARD = 3

#-------------------兵营的归属------------------------------
TRAP_BARRACKS_BELONG_NEUTRALLY =2  	# 中立
TRAP_BARRACKS_BELONG_PROTECT = 1	# 防守方
TRAP_BARRACKS_BELONG_ATTACK  = 0	# 进攻方

#----------------------常量--------------------------------
INT_16_MAX = 32767 #int16最大值
INT_32_MAX = 2147483647 #int32最大值
INT_64_MAX = 9223372036854775807	#int64最大值

BELONG_SIDE_ATTACK		= 0 	#归属进攻方
BELONG_SIDE_PROTECT	= 1 	#归属防守方

#---------------------NPC练兵场状态------------------------
NPCTRAINSOLDIERGROUND_STATE_CAN_NOT_BE_DECLARE = 0 # 不可被宣战
NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE = 1	# 可被宣战
NPCTRAINSOLDIERGROUND_STATE_FIGHT 	= 2	# 争夺中


#---------------------练兵场类型---------------------------
NPCTRAINSOLDIERGROUND_TYPE_NONE 		= 0		#默认值
NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL	= 1		#初级练兵场
NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL	= 2		#中级练兵场
NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL 	= 3		#高级练兵场

#---------------------跨服相关------------------------------
#----跨服结果Code------
CROSS_SERVICE_DEFAULT 				= -1	#默认 未知
CROSS_SERVICE_SUCCESS 				= 0		#成功
CROSS_SERVICE_ARGS_ERROR 			= 1		#参数错误
CROSS_SERVICE_SIGN_ERROR			= 2		#签名错误
CROSS_SERVICE_UNKNOW_ERROR		= 3		#系统错误
CROSS_SERVICE_ACCOUNT_NOT_EXISTS 	= 4		#账号不存在或未激活
CROSS_SERVICE_ROLE_NOT_EXISTS 		= 5		#角色不存在
CROSS_SERVICE_SERVER_KEY_ERROR 	= 6		#服务器配置错误
CROSS_SERVICE_OLD_PLAYER_INFO_ERROR 	= 7	#原服务器玩家不存在
CROSS_SERVICE_NOT_CROSS_SERVER_PLAY = 8	#非跨服玩家，不能删除
CROSS_SERVICE_STATUS_ERROR	 = 9	#当前状态不能跨服或者返回原服


#-----------------------------玩家移动类型--------------------------------
MOVE_TYPE_NONE						= 0			# 无移动
MOVE_TYPE_MOUSE						= 1			# 鼠标移动
MOVE_TYPE_CONTROL					= 2			# 自主移动
MOVE_TYPE_TRACE						= 3			# 追踪移动
MOVE_TYPE_FLY						= 4			# 飞行移动
MOVE_TYPE_BACK						= 5			# 受击移动
MOVE_TYPE_NAVIGATE					= 6			# 寻路移动
MOVE_TYPE_TEAM_FOLLOW				= 7			# 组队跟随
MOVE_TYPE_AUTO_NAVIGATE				= 8			# 自动寻路

# 玩家主动移动列表
ACTIVE_MOVE_LIST = [MOVE_TYPE_MOUSE, MOVE_TYPE_CONTROL, MOVE_TYPE_TRACE, MOVE_TYPE_NAVIGATE, 
					MOVE_TYPE_TEAM_FOLLOW, MOVE_TYPE_AUTO_NAVIGATE]

# 玩家被动移动列表
PASSIVE_MOVE_LIST = [MOVE_TYPE_FLY, MOVE_TYPE_BACK]

#帮会争霸据点的相关状态
NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE 	= 0				# 不可被宣战
NPCEXTPOINT_STATE_CAN_BE_DECLARE 		= 1				# 可被宣战
NPCEXTPOINT_STATE_FIGHT 				= 2				# 争夺中
NPCEXTPOINT_STATE_REST 					= 3				# 休整中
NPCEXTPOINT_STATE_DEFENSE 				= 4				# 布防中


#帮会争霸据点的类型
NPCEXTPOINT_TYPE_LOWER_LEVEL			= 1				# 低级据点
NPCEXTPOINT_TYPE_MIDDLE_LEVEL			= 2				# 中级据点


#获得奖励通用原因，用于根据奖励ID奖励，奖励中可能是物品、经验、金钱等
ADD_REWARD_REASON_COMMON_TYPE_QUEST = 110 #任务奖励
ADD_REWARD_REASON_COMMON_TYPE_JZYT  = 111 #金枝玉庭
ADD_REWARD_REASON_COMMON_TYPE_QIANNENG_SPACE  = 112 #潜能副本（CST-11294）
ADD_REWARD_REASON_COMMON_TYPE_ZFZL	= 113		# 逐风之路
ADD_REWARD_REASON_COMMON_TYPE_SPACE_EVENT	= 114		# 副本剧情奖励
ADD_REWARD_REASON_COMMON_TYPE_CAMP_MORALE	= 115		# 阵营气运奖励
ADD_REWARD_REASON_COMMON_TYPE_TRAP_ACTION	= 116		# 触发陷阱给奖励
ADD_REWARD_REASON_COMMON_TYPE_OCCUPY_LBC 	= 117		# 占领练兵场

#定点更新系统
FIXED_UPDATE_KEY = "FIXED_UPDATE_KEY_"
FIXED_UPDATE_TOKEN_ZERO = 0		#零点更新
FIXED_UPDATE_TOKEN_FIVE = 5		#凌晨5点更新

#上面每添加一种类型，需要将其添加到此列表中
FIXED_UPDATE_TOKEN_LIST = [FIXED_UPDATE_TOKEN_ZERO, FIXED_UPDATE_TOKEN_FIVE]

#cst-11490 控制space的开启关闭
CONTROL_SPACE_KEY = "CONTROL_SPACE_KEY_"
CONTROL_SPACE_CLOSE_TIME = 60	#space关闭倒计时

#帮会掠夺战活动状态
TONG_PLUNDER_ACTIVITY_STATUS_FREE 	= 0	#未开启
TONG_PLUNDER_ACTIVITY_STATUS_SIGNUP = 1 #报名
TONG_PLUNDER_ACTIVITY_STATUS_START 	= 2 #开启

#帮会掠夺战活动辅助状态
TONG_PLUNDER_ACTIVITY_STATUS_CAN_NOT_ENTER = 0 #不允许玩家进入
TONG_PLUNDER_ACTIVITY_STATUS_CAN_ENTER = 1 #允许玩家进入

# 跳伞状态
PARACHUTE_STATE_NORMAL			= 0 	# 正常状态
PARACHUTE_STATE_CARRIER			= 1		# 飞行器状态
PARACHUTE_STATE_FALL			= 2		# 自由下落状态
PARACHUTE_STATE_OPEN			= 3		# 开伞状态

# 大荒战场模型使用变色方案
MODEL_COLOR_SCHEME_MS			= 1		# 使用美术替换模型方案
MODEL_COLOR_SCHEME_CX			= 2		# 使用程序的模型材质变色方案
#----------------帮会宝箱奖励 帮会争霸/帮会掠夺 ----------------
TONG_DROPBOX_BHZBFIRST		= "BHZBFIRST"		#帮会争霸冠军
TONG_DROPBOX_BHZBSECOND		= "BHZBSECOND"		#帮会争霸亚军
TONG_DROPBOX_BHZBTHIRD		= "BHZBTHIRD"		#帮会争霸季军
TONG_DROPBOX_BHLD			= "BHLD"			#帮会掠夺

#攻城战活动状态
GCZ_ACTIVITY_STATUS_SIGNUP = 1	# 报名
GCZ_ACTIVITY_STATUS_MATCH = 2	# 匹配
GCZ_ACTIVITY_STATUS_ENTER = 3	# 进入
GCZ_ACTIVITY_STATUS_START = 4	# 开启
