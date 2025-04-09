# -*- coding: utf-8 -*-

"""
下面的是游戏中的csdefine.py文件中定义的，这里是直接拷贝过来的
"""




#-----------------------------------
#玩家聊天频道
#-----------------------------------
CHAT_TYPE_NEARBY = 0			# 附近
CHAT_TYPE_SPACE = 1				# 地图
CHAT_TYPE_WORLD = 2				# 世界
CHAT_TYPE_WHISPER = 3			# 密语
CHAT_TYPE_GROUP = 4				# 讨论组
CHAT_TYPE_TEAM = 5				# 队伍
CHAT_TYPE_COLLECTIVE = 6			# 团队
CHAT_TYPE_GANG = 7				# 帮会
CHAT_TYPE_ALIANCE = 8			# 联盟
CHAT_TYPE_SCHOOL = 9			# 门派
CHAT_TYPE_CAMP = 10				# 阵营
CHAT_TYPE_BATTLESPACE = 11		# 战场
CHAT_TYPE_TIANYIN = 12			# 天音
CHAT_TYPE_XIANYIN = 13			# 仙音
CHAT_TYPE_SYSTEM = 14			# 系统
CHAT_TYPE_FRIEND = 15			# 好友

#----------------------------------------------
#金钱类型
#----------------------------------------------
COIN_TYPE_GOLD        = 1
COIN_TYPE_SILVER  	= 2
COIN_TYPE_MONEY      = 3     #金币

MONEY_CHANGE_TYPE_ADD = 1	#金钱曾加
MONEY_CHANGE_TYPE_SUB = 2	#金钱减少

#----------------------------------------------
#增加玩家金币的原因
#----------------------------------------------
MONEY_ADD_REASON_DROP_MONSTER		= 1			# 怪物身上掉落
MONEY_ADD_REASON_QUEST_REWARD			= 2			# 任务奖励
MONEY_ADD_REASON_ROLE_TRADE			= 3			# 玩家交易
MONEY_ADD_REASON_SELL_ITEM				= 4			# 出售物品
MONEY_ADD_REASON_RETURN_ITEM			= 5			# 退回物品
MONEY_ADD_REASON_USE_GIFT_ITEM			= 6			# 打开礼包
MONEY_ADD_REASON_FROM_STORE			= 7			# 从仓库取钱
MONEY_ADD_REASON_LINGSHI_TRADE			= 8			# 灵石寄售
MONEY_ADD_REASON_GM_COMMAND			= 9			# GM命令
MONEY_ADD_REASON_SPACE_SENTLEMENT		= 10		# 副本结算
MONEY_ADD_REASON_SPAR_HUN_TING			= 11		# 晶石狩猎场
MONEY_ADD_REASON_TONGCONTRI_TO_MONEY	= 12	# 帮会解散 帮贡转化为钱
MONEY_ADD_REASON_MAIL					= 13		# 邮件

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
MONEY_SUB_REASON_ROLE_REVIVE				= 13		# 玩家复活
MONEY_SUB_REASON_COMMONUTION_SKILL	= 14		# 精研技能
MONEY_SUB_REASON_TELEPORT				= 15		# 玩家传送消耗
MONEY_SUB_REASON_TONG_DONATE			= 16		# 帮会捐献
MONEY_SUB_REASON_GM_COMMAND			= 17		# GM命令
MONEY_SUB_REASON_ROLE_TRADE				= 18		# 玩家交易
MONEY_SUB_REASON_CREATE_TONG			= 19		# 创建帮会
MONEY_SUB_REASON_LEARN_TONG_SKILL		= 20		# 学习帮会技能
MONEY_SUB_REASON_INTENSIFY_EQUIP			= 21		# 装备强化
MONEY_SUB_REASON_RESET_EQUIP				= 22		# 装备回火
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

#----------------------------------------------
#仙石，灵石，玄石变更原因日志分类
#----------------------------------------------
#仙石
CHANGE_XIANSHI_NORMAL					= 0			# 默认方式
CHANGE_XIANSHI_UNLOCKBAGGRID		= 1			# 解锁背包格
CHANGE_XIANSHI_PETCAGES				= 2			# 解锁幻兽格子
CHANGE_XIANSHI_INTENSIFY_SAVESLOT		= 3			# 解锁强化保存栏位
CHANGE_XIANSHI_GM_SET					= 4			# GM指令设置元宝
CHANGE_XIANSHI_AUGMENT_SIGNIN		= 5			# 补签消耗元宝
CHANGE_XIANSHI_COMPOSE_EQUIP			= 6			# 装备打造消耗元宝
CHANGE_XIANSHI_CHARGE					= 7			# 充值兑换
CHANGE_XIANSHI_RECAST_EQUIP			= 8			# 使用元宝重铸
CHANGE_XIANSHI_RESET_EQUIP				= 9			# 使用元宝洗练
CHANGE_XIANSHI_BY_MAILL				= 10 		# 邮件
CHANGE_XIANSHI_BY_SHOP_CONSUME		= 11		# 商城消费
CHANGE_XIANSHI_BY_TRADE				= 12		# 灵石急售
CHANGE_XIANSHI_BY_INTENSIFY_EQUIP		= 13		# 装备强化
CHANGE_XIANSHI_BY_RESET_EQUIP			= 14		# 装备回火
CHANGE_XIANSHI_BY_SAVE_INTENSIFY_EQUIP	= 15		# 装备备份
CHANGE_XIANSHI_BY_RESET_INTENSIFY_EQUIP	= 16		# 装备还原
CHANGE_XIANSHI_BY_UNLOCK_PASSIVESKILLBAR= 17		# 解锁被动技能
CHANGE_XIANSHI_PETCOMPOSE				= 18		# 合成幻兽
#玄石
CHANGE_XUANSHI_CHARGE					= 1			# 充值兑换
CHANGE_XUANSHI_GM_SET					= 2			# GM指令设置玄石
CHANGE_XUANSHI_SILVERPRESENT			= 3			# 领取玄石奖励
CHANGE_XUANSHI_SHOP_CONUSUME		= 4			# 商城消费
CHANGE_XUANSHI_SHOP_REBATE			= 5			# 商城消费返利
#灵石
CHANGE_LINGSHI_BY_STORE 				= 1			# 商城购买
CHANGE_LINGSHI_BY_MAILL 				= 2			# 邮件
CHANGE_LINGSHI_BY_SHOP_CONUSUME	= 3			# 商城消费


#----------------------------------------------
#物品品质
#----------------------------------------------
QUALITY_WHITE					= 1		# 白色
QUALITY_BLUE					= 2		# 蓝色
QUALITY_GOLD					= 3		# 金色
QUALITY_PINK					= 4		# 粉色
QUALITY_GREEN				= 5		# 地阶绿色
QUALITY_GREEN_TIAN				= 6		# 天阶绿色
QUALITY_GREEN_SHENG				= 7		# 圣阶绿色

#----------------------------------------------
#物品初始化绑定类型定义
#----------------------------------------------
ITEM_SRCBINDTYPE_NONE_BIND				= 0			# 无绑定
ITEM_SRCBINDTYPE_PICKUP_BIND			= 1			# 拾取绑定
ITEM_SRCBINDTYPE_EQUIP_BIND				= 2			# 装备绑定
ITEM_SRCBINDTYPE_IS_BIND				= 3			# 默认绑定




#----------------------------------------------
#邮件操作类型
#----------------------------------------------
MAIL_TYPE_SEND		= 1	#发送邮件
MAIL_TYPE_READ		= 2	#阅读邮件
MAIL_TYPE_DEL		= 3	#删除邮件
MAIL_TYPE_EXTRACT	= 4	#提取邮件
#删除邮件分类
LT_MAIL_DEL_TYPE_ACTIVE			= 1 #主动删除
LT_MAIL_DEL_TYPE_TIME_ARRIVE	= 2 #时间达到
LT_MAIL_DEL_TYPE_BEREPLACED		= 3 #被其他新邮件顶替
#邮件
# 信件发送者类型
MAIL_SENDER_TYPE_PLAYER				= 1		# 玩家寄信
MAIL_SENDER_TYPE_SYS				= 2		# 系统寄信
MAIL_SENDER_TYPE_GM					= 3		# GM寄信
MAIL_SENDER_TYPE_RETURN				= 4		# 退信


#----------------------------------------------
#职业
#----------------------------------------------
CLASS_FIGHTER							= 1			# 战士
CLASS_SWORDMAN							= 2			# 剑客
CLASS_ARCHER							= 3			# 射手
CLASS_MAGE								= 4			# 法师

#----------------------------------------------
#角色性别
#----------------------------------------------
MALE									= 1			# 男性
FEMALE									= 2			# 女性



#----------------------------------------------
#阵营
#----------------------------------------------
CMAP_NONE								= 0			# 不区分仙魔
CAMP_TAOSIM								= 1			# 仙道
CAMP_DEMON								= 2			# 魔道

#----------------------------------------------
#物品位置
#----------------------------------------------
ITEM_ORDER_BAG		= 1 #包裹
ITEM_ORDER_STORE	= 2 #仓库
ITEM_ORDER_WEAR		= 3 #穿戴

#----------------------------------------------
#物品大类
#----------------------------------------------
ITEM_TYPE_DEFAULT = 0			# 默认
ITEM_TYPE_WEAPON = 10001		# 武器
ITEM_TYPE_HAT = 10002			# 帽子
ITEM_TYPE_COAT = 10003			# 衣服
ITEM_TYPE_PANTS = 10004			# 裤子
ITEM_TYPE_BELT = 10005			# 腰带
TEM_TYPE_WRIST = 10006			# 护腕
ITEM_TYPE_GLOVES = 10007		# 手套
ITEM_TYPE_SHOES = 10008			# 鞋子
ITEM_TYPE_NECKLACE = 10009		# 项链
ITEM_TYPE_RING = 10010			# 戒指
ITEM_TYPE_FASHION = 10011		# 时装
ITEM_TYPE_VARIA = 20001			# 杂物
ITEM_TYPE_BDRUG = 20002			# 气血药
ITEM_TYPE_EDRUG = 20003			# 内息药
ITEM_TYPE_PBDRUG = 20004		# 幻兽气血药
ITEM_TYPE_PEDRUG = 20005		# 幻兽内息药
ITEM_TYPE_PETEGG = 20006		# 幻兽蛋
ITEM_TYPE_SYSTEM = 20007		# 系统功能
ITEM_TYPE_SPAR = 20008			# 晶核
ITEM_TYPE_MATERIAL = 20009		# 材料
ITEM_TYPE_SCROLL = 20010		# 卷轴
ITEM_TYPE_CHARM = 20011			# 符咒
ITEM_TYPE_GIFT = 20012			# 礼包
ITEM_TYPE_PPSKILL = 20013		# 幻兽被动技能书
ITEM_TYPE_QUEST = 30001			# 任务物品
ITEM_TYPE_ACTIVE = 30002		# 活动物品
ITEM_TYPE_COPY = 30003			# 副本物品
ITEM_TYPE_COPY_YXWZ1 = 30004	# 英雄王座战魂
ITEM_TYPE_COPY_YXWZ2 = 30005	# 英雄王座红药
ITEM_TYPE_COPY_YXWZ3 = 30006	# 英雄王座蓝药
ITEM_TYPE_COPY_YXWZ4 = 30007	# 英雄王座固定物品
ITEM_TYPE_PART_EQUIP = 30010	# 半成品装备
ITEM_TYPE_BPRINT	 = 30011	# 图纸
ITEM_TYPE_JADE		 = 30012	# 玲珑玉令


#----------------------------------------------
#物品添加，删除，更新原因
#----------------------------------------------
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
ITEM_REMOVE_BY_SKILL					= 16 		# 使用技能消耗物品
ITEM_REMOVE_BY_SHUFFLE					= 17		# 装备洗练
ITEM_REMOVE_BY_RECAST					= 18		# 装备重铸
ITEM_REMOVE_BY_BIOGRAPHY				= 19		# 装备传星
ITEM_REMOVE_BY_MAIL						= 20		# 邮件
ITEM_REMOVE_BY_STORE_SORTSTACK			= 21		# 仓库相关操作，叠加物品
ITEM_REMOVE_BY_SELL_TO_NPC				= 22		# 出售给NPC
ITEM_REMOVE_BY_GM						= 100		# GM指令删除物品

#----------------------------------------------
#幻兽品质
#----------------------------------------------
VEHICLE_PET_QUALITY_NORMAL				= 1			# 凡兽
VEHICLE_PET_QUALITY_SPIRIT				= 2			# 灵兽
VEHICLE_PET_QUALITY_HOLY				= 3			# 圣兽
VEHICLE_PET_QUALITY_DEITY				= 4			# 神兽

#----------------------------------------------
#获得幻兽原因
#----------------------------------------------
PET_ADD_REASON_DEFAULT					= 0	# 默认
PET_ADD_REASON_COMPLETE_QUEST			= 1 # 完成任务获得
PET_ADD_REASON_KILL_PETMONSTER			= 2 # 击杀幻兽怪物获得
#----------------------------------------------
#失去幻兽原因
#----------------------------------------------
PET_REMOVE_REASON_FREE					= 1 # 放生



