#-*-coding:utf-8-*-
import csdefine
# -------------------------------------------------
# 物品品质定义
# -------------------------------------------------
QUALITY_WHITE							= 1			# 白色
QUALITY_BLUE							= 2			# 蓝色
QUALITY_GOLD							= 3			# 金色
QUALITY_PINK							= 4			# 粉色
QUALITY_GREEN							= 5			# 地阶绿色
QUALITY_GREEN_TIAN						= 6			# 天阶绿色
QUALITY_GREEN_SHENG						= 7			# 圣阶绿色
QUALITY_GREEN_SHEN						= 8			# 神阶绿 


# -------------------------------------------------
# 物品初始化绑定类型定义srcBindType
# -------------------------------------------------
NONE_BIND								= 0			# 无绑定
PICKUP_BIND								= 1			# 拾取绑定
EQUIP_BIND								= 2			# 装备绑定
IS_BIND									= 3			# 默认绑定

#绑定和非绑定区分bindType,运行时绑定类型
BIND_NONT_STATE							= 0			# 装备示绑定
BINDED_STATE							= 1			# 装备绑定


# -------------------------------------------------
# 物品类型定义
# -------------------------------------------------
ITEM_UNKOWN								= 0x000000	# 未知

ITEM_XUANJING							= 1			# 玄晶
ITEM_FIVEXUANJING						= 2			# 五彩玄晶
ITEM_SUPERXUANJING						= 3			# 超级玄晶

ITEM_WHITEBEAD							= 1			# 龙珠
ITEM_FIVEBEAD							= 2			# 五彩龙珠
ITEM_SUPERBEAD							= 3			# 超级龙珠

ITEM_WHITESPAR							= 1			# 晶石
ITEM_FIVESPAR							= 2			# 五彩晶石
ITEM_SUPERSPAR							= 3			# 超级晶石

ITEM_HUIHUO								= 1			# 回火符
ITEM_ZHENGYANG							= 2			# 正阳符
ITEM_BEIDOU								= 3			# 北斗符
ITEM_BLOOD								= 4			# 血符
ITEM_PROTECT							= 5			# 重铸保护符

ITEM_WASH								= 1			# 洗练石
ITEM_RECOIN								= 2			# 重铸宝珠

#强化星级定义
IRONSTAR								= 1			# 铁星
COPPERSTAR								= 2			# 铜星
SILVERSTAR								= 3			# 银星
GOLDSTAR								= 4			# 金星

#强化主属性的取值范围
IRONSTARRANGE							= [0.01, 0.08]		# 铁星主属性取值范围
COPPERSTARRANGE							= [0.08, 0.16]		# 铜星主属性取值范围
SILVERSTARRANGE							= [0.16, 0.24]		# 银星主属性取值范围
GOLDSTARRANGE							= [0.24, 0.36]		# 金星主属性取值范围

#强化主属性取值范围
INTENSIFY_MAINVALUE = {
					IRONSTAR			: IRONSTARRANGE,
					COPPERSTAR			: COPPERSTARRANGE,
					SILVERSTAR			: SILVERSTARRANGE,
					GOLDSTAR			: GOLDSTARRANGE,
	}


ITEM_CHENGYI							= 1			# 成衣
ITEM_WAIZHUANG							= 2			# 外装
ITEM_FACE								= 3			# 易容
ITEM_PENDANT							= 4			# 挂件
ITEM_DECORATION							= 5			# 装饰
ITEM_SPECIAL							= 6			# 珍奇
ITEM_FUN								= 7			# 趣味


# -------------------------------------------------
# 装备部位定义
# -------------------------------------------------
#EQUIP_HEAD								= 0			# 头
#EQUIP_NECK								= 1			# 颈
#EQUIP_BODY								= 2			# 身体
#EQUIP_BREECH							= 3			# 腿部
#EQUIP_VOLA								= 4			# 手掌
#EQUIP_HAUNCH							= 5			# 腰部
#EQUIP_CUFF								= 6			# 腕部
#EQUIP_WEAPON							= 7			# 武器
#EQUIP_LEFTHAND							= 7			# 左手
#EQUIP_RIGHTHAND						= 8			# 右手
#EQUIP_FEET								= 9			# 脚
#EQUIP_FINGER							= 10		# 手指
#EQUIP_LEFTFINGER						= 10		# 左手指
#EQUIP_RIGHTFINGER						= 11		# 右手指
#EQUIP_CIMELIA							= 12		# 魂魄石
#EQUIP_TALISMAN							= 13		# 法宝
#EQUIP_FASHION1							= 14		# 时装1
#EQUIP_POTENTIAL_BOOK					= 15		# 潜能天书
#模型部分
EQUIP_BODY								= 10		# 裸体身体
EQUIP_HEAD								= 11		# 裸体
EQUIP_SUIT								= 12		# 套装（时装）
EQUIP_HAIR								= 13		# 头发
#装备部分
EQUIP_HAT								= 20		# 帽子
EQUIP_COAT								= 21		# 上衣，衣服
EQUIP_WRIST								= 22		# 护腕
EQUIP_HAND								= 23		# 手套
EQUIP_WAIST								= 24		# 腰带
EQUIP_PANTS								= 25		# 裤子
EQUIP_SHOES								= 26		# 鞋子
EQUIP_NECKLACE							= 27		# 项链
EQUIP_RING								= 28		# 左手戒指
#EQUIP_RING								= 29		# 右手戒指（被占用）
EQUIP_WEAPON							= 31		# 双手武器
EQUIP_LEFT_WEAPON						= 32		# 左手武器
EQUIP_RIGHT_WEAPON						= 33		# 右手武器
EQUIP_CLOAK								= 34		# 披风
EQUIP_FABAO								= 35		# 法宝

EQUIP_ARMOR			= [ EQUIP_HAT, EQUIP_COAT, EQUIP_WRIST, EQUIP_HAND, EQUIP_WAIST, EQUIP_PANTS, EQUIP_SHOES, EQUIP_CLOAK, EQUIP_HAIR, EQUIP_SUIT ]
EQUIP_ALL_WEAPON	= [ EQUIP_WEAPON, EQUIP_LEFT_WEAPON, EQUIP_RIGHT_WEAPON ]


#外观部分
FACADE_HAT								= 800		# 帽子
FACADE_COAT								= 801		# 上衣，衣服
FACADE_WRIST							= 802		# 护腕
FACADE_WAIST							= 803		# 腰带
FACADE_SHOES							= 804		# 鞋子

FACADE_HAIR								= 805		# 发型
FACADE_FACE								= 806		# 捏脸
FACADE_WAIST_PENDANT					= 807		# 腰部挂件
FACADE_BACK_PENDANT						= 808		# 背部挂件

FACADE_NECKLACE							= 809		# 项链
FACADE_FOOT_DECORATION					= 900		# 脚饰
FACADE_BRACELET							= 901		# 手环
FACADE_AIRCRAFT							= 902		# 飞行器

#背包整理时装备排序是各装备的顺序
SORTEQUIPINDEXS = {
					EQUIP_WEAPON		: 0,
					EQUIP_LEFT_WEAPON	: 0,
					EQUIP_RIGHT_WEAPON	: 0,
					EQUIP_HAT			: 1,
					EQUIP_COAT			: 2,
					EQUIP_WRIST			: 3,
					EQUIP_HAND			: 4,
					EQUIP_WAIST			: 5,
					EQUIP_PANTS			: 6,
					EQUIP_SHOES			: 7,
					EQUIP_NECKLACE		: 8,
					EQUIP_RING			: 9,
					EQUIP_FABAO			: 10,
	}

#其它装备的序号
SORTEQUIPOTHER = 0


# -------------------------------------------------
# 背包定义，修改此处，还需要修改客户端的RoleKitBagInterface中的GetKitBagByOrder方法
# -------------------------------------------------

COMMONCAPACITY							= 48		# 默认道具背包容量
LOCKCAPACITY							= 72		# 普通背包扩展格数量

QUESTCAPACIRY							= 48		# 任务背包容量
CRYSTALCAPACIRY							= 80		# 晶核背包容量

BAG_EQUIP								= 0			# 装备背包
BAG_EQUIPSTART							= 0			# 装备格起始位0
BAG_EQUIPEND							= 63		# 装备格结束位63

BAG_COMMON								= 1			# 普通背包
BAG_COMMONSTART							= BAG_EQUIPEND + 1											# 普通格起始位64
BAG_COMMONEND							= BAG_COMMONSTART + COMMONCAPACITY + LOCKCAPACITY - 1		# 普通格结束位183

BAG_QUEST								= 2			# 任务背包
BAG_QUESTSTART							= BAG_COMMONEND + 1											# 任务格起始位184
BAG_QUESTEND							= BAG_QUESTSTART + QUESTCAPACIRY - 1						# 任务格结束位231

BAG_SPAR								= 3			# 晶石背包
BAG_SPARSTART							= BAG_QUESTEND + 1											# 晶石格起始位232
BAG_SPAREND								= BAG_SPARSTART + CRYSTALCAPACIRY - 1						# 晶石格结束位311

STORE_CAPACITY							= 100		# 默认仓库容量
STORE_LOCK_CAPACITY						= 100		# 仓库锁定容量

BAG_STORE								= 4			# 仓库
BAG_STORESTART							= BAG_SPAREND + 1											# 仓库起始位312
BAG_STOREEND							= BAG_STORESTART + STORE_CAPACITY + STORE_LOCK_CAPACITY - 1	# 仓库结束位511

TONGCAPACITY							= 480

BAG_TONG_STORE							= 5		# 帮会仓库1
BAG_TONG_STORE_START					= BAG_STOREEND + 1											# 起始位512
BAG_TONG_STORE_END						= BAG_TONG_STORE_START + TONGCAPACITY  - 1					# 结束位991

SPACECOPY_LOCKCECAPACITY				= 24

BAG_SPACE_COPY							= 6		# 玩家副本专用背包
BAG_SPACECOPY_START						= BAG_TONG_STORE_END + 1									# 起始位992
BAG_SPACECOPY_END						= BAG_SPACECOPY_START + SPACECOPY_LOCKCECAPACITY - 1		# 结束位1015

BAG_SPACE_COPY_YXLM1					= 7		# 英雄联盟背包1
BAG_SPACECOPY_YXLM1_START				= BAG_SPACECOPY_END + 1										# 起始位1016
BAG_SPACECOPY_YXLM1_END					= BAG_SPACECOPY_YXLM1_START + 4 -1							# 结束位1019

BAG_SPACE_COPY_YXLM2					= 8		# 英雄联盟背包2
BAG_SPACECOPY_YXLM2_START				= BAG_SPACECOPY_YXLM1_END + 1								# 起始位1020
BAG_SPACECOPY_YXLM2_END					= BAG_SPACECOPY_YXLM2_START + 1 -1							# 结束位1020

BAG_SPACE_COPY_YXLM3					= 9		# 英雄联盟背包3
BAG_SPACECOPY_YXLM3_START				= BAG_SPACECOPY_YXLM2_END + 1								# 起始位1021
BAG_SPACECOPY_YXLM3_END					= BAG_SPACECOPY_YXLM3_START + 1 -1							# 结束位1021

BAG_SPACE_COPY_YXLM4					= 10	# 英雄联盟背包4
BAG_SPACECOPY_YXLM4_START				= BAG_SPACECOPY_YXLM3_END + 1								# 起始位1022
BAG_SPACECOPY_YXLM4_END					= BAG_SPACECOPY_YXLM4_START + 1 -1							# 结束位1022

STORE_LOCKERS_CAPACITY					= 30		# 默认仓库容量
STORE_LOCKERS_LOCK_CAPACITY				= 70		# 仓库锁定容量

BAG_WORK_SHOP_LOCKERS					= 11	# 工坊储物柜
BAG_WORK_SHOP_LOCKERS_START				= BAG_SPACECOPY_YXLM4_END + 1								# 起始位1023
BAG_WORK_SHOP_LOCKERS_END= BAG_WORK_SHOP_LOCKERS_START + STORE_LOCKERS_CAPACITY + STORE_LOCKERS_LOCK_CAPACITY-1# 结束位1122

BAG_ALCHEMIST_LOCKERS					= 12	# 炼金坊储物柜
BAG_ALCHEMIST_LOCKERS_START				= BAG_WORK_SHOP_LOCKERS_END + 1								# 起始位1123
BAG_ALCHEMIST_LOCKERS_END= BAG_ALCHEMIST_LOCKERS_START + STORE_LOCKERS_CAPACITY + STORE_LOCKERS_LOCK_CAPACITY -1# 结束位1222

BAG_APPEARANCE							= 13	# 外观隐藏背包
STORE_APPEARANCE_CAPACITY				= 500		# 外观隐藏背包容量
BAG_APPEARANCES_START				= BAG_ALCHEMIST_LOCKERS_END + 1					# 起始位1223
BAG_APPEARANCES_END= BAG_APPEARANCES_START + STORE_APPEARANCE_CAPACITY -1			# 结束位1722

BAG_TEMP_EQUIP 								= 14 	#CST-12212 阵营竞技“大荒战场50人PVP” 临时装备背包
BAG_TEMP_EQUIP_CAPACITY 						= 50 	#临时装备背包容量
BAG_TEMP_EQUIP_START 						= BAG_APPEARANCES_END+1 					# 起始位1723
BAG_TEMP_EQUIP_END 							= BAG_TEMP_EQUIP_START + BAG_TEMP_EQUIP_CAPACITY - 1  # 结束位1772
EQUIP_WEAPON_YCJMD 						= BAG_TEMP_EQUIP_START 			# CST-12212 吃鸡装备 武器位置
EQUIP_HAT_YCJMD 						= BAG_TEMP_EQUIP_START+1 		# CST-12212 吃鸡装备 帽子位置
EQUIP_COAT_YCJMD 						= BAG_TEMP_EQUIP_START+2 		# CST-12212 吃鸡装备 衣服位置
"""  
目前暂未用到  先注释  避免导致客户端和服务器的数据不一致
FACADE_BAG_CECAPACITY					= 40		# 外观
FACADE_BAG_LOCKCAPACITY					= 40		# 外观背包中扩展格子数量

BAG_WAIST_PENDANT						= 12			# 外观腰部挂件背包
BAG_WAIST_PENDANT_START					= BAG_STOREEND + 1																			# 起始位664
BAG_WAIST_PENDANT_END					= BAG_WAIST_PENDANT_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY -1				# 结束位743

BAG_BACK_PENDANT						= 6			# 外观背部挂件背包
BAG_BACK_PENDANT_START					= BAG_WAIST_PENDANT_END + 1																	# 起始位744
BAG_BACK_PENDANT_END					= BAG_BACK_PENDANT_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY - 1				# 结束位823

BAG_NECKLACE_DECORATION					= 7			# 外观背包项链
BAG_NECKLACE_DECORATION_START			= BAG_BACK_PENDANT_END + 1																	# 起始位824
BAG_NECKLACE_DECORATION_END				= BAG_NECKLACE_DECORATION_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY - 1		# 结束位903

BAG_BRACELET_DECORATION					= 8			# 外观背包手环
BAG_BRACELET_DECORATION_START			= BAG_NECKLACE_DECORATION_END + 1															# 起始位904
BAG_BRACELET_DECORATION_END				= BAG_BRACELET_DECORATION_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY - 1		# 结束位983

BAG_FOOT_DECORATION						= 9			# 外观背包脚饰
BAG_FOOT_DECORATION_START				= BAG_BRACELET_DECORATION_END + 1															# 起始位0984
BAG_FOOT_DECORATION_END					= BAG_FOOT_DECORATION_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY - 1			# 结束位1063

BAG_AIRCRAFT_DECORATION					= 10		# 外观背包飞行器
BAG_AIRCRAFT_DECORATION_START			= BAG_FOOT_DECORATION_END + 1																# 起始位1064
BAG_AIRCRAFT_DECORATION_END				= BAG_AIRCRAFT_DECORATION_START + FACADE_BAG_CECAPACITY + FACADE_BAG_LOCKCAPACITY - 1		# 结束位1143

#外观部分背包
BAG_FACADE								= 11
BAG_FACADE_START						= 1144
BAG_FACADE_END							= 1244
"""


#属性编号定义
CORPOREITY 								= 30001		# 根骨
STRENGTH								= 30002		# 筋力
INTELLECT								= 30003		# 内力
DISCERN 								= 30004		# 洞察
DEXTERITY								= 30005		# 身法
HP										= 30006		# 生命
MP										= 30007		# 法力
DAMAGE									= 30008		# 物攻
MAGICDAMAGE								= 30009		# 法攻
ARMOR									= 30010		# 物防
MAGICARMOR								= 30011		# 法防
CRITICALSTRIKE							= 30012		# 暴击
PARRY									= 30013		# 招架
SPEED									= 30014		# 移速
HITRATE									= 30015		# 命中率
DODGERATE								= 30016		# 闪避率
HEALINGRATE								= 30017		# 脱战生命自愈率
GANGQI_MAX								= 30018		# 罡气最大值
GANGQI_DAMAGE_POINT						= 30019		# 罡气攻击点
GANGQI_ARMOR_POINT						= 30020		# 罡气防御点
GANGQI_QIJIE_REVIVE						= 30021		# 气竭罡气自愈率
GANGQI_QIYING_REVIVE					= 30022		# 气盈罡气自愈率
TEMPSPEED								= 30023		# 临时速度
CURE									= 30024		# 治疗成效
CRITRATIO								= 30025		# 暴击倍率
PARRYRATIO							 	= 30026		# 招架倍率
ICE_DAMAGE								= 30027		# 冰元素攻击
FIRE_DAMAGE								= 30028		# 火元素攻击
THUNDER_DAMAGE							= 30029		# 雷元素攻击
XUAN_DAMAGE								= 30030		# 玄元素攻击
ICE_ARMOR								= 30031		# 冰元素防御
FIRE_ARMOR								= 30032		# 火元素防御
THUNDER_ARMOR							= 30033		# 雷元素防御
XUAN_ARMOR								= 30034		# 玄元素防御
DAMAGE_IGNORE							= 30035		# 物攻忽视
MAGICDAMAGE_IGNORE						= 30036		# 法攻忽视
ARMOR_IGNORE							= 30037		# 物防忽视
MAGICARMOR_IGNORE						= 30038		# 法防忽视
CRITICALSTRIKE_IGNORE					= 30039		# 暴击忽视
PARRY_IGNORE							= 30040		# 招架忽视
HITRATE_IGNORE							= 30041		# 命中率忽视
DODGERATE_IGNORE						= 30042		# 闪避率忽视
ICE_DAMAGE_IGNORE						= 30043		# 冰元素攻击忽视
FIRE_DAMAGE_IGNORE						= 30044		# 火元素攻击忽视
THUNDER_DAMAGE_IGNORE					= 30045		# 雷元素攻击忽视
XUAN_DAMAGE_IGNORE						= 30046		# 玄元素攻击忽视
ICE_ARMOR_IGNORE						= 30047		# 冰元素防御忽视
FIRE_ARMOR_IGNORE						= 30048		# 火元素防御忽视
THUNDER_ARMOR_IGNORE					= 30049		# 雷元素防御忽视
XUAN_ARMOR_IGNORE						= 30050		# 玄元素防御忽视
DEPRESS_RESIST							= 30051		# 减损抵抗率
HITBACK_RESIST							= 30052		# 击退抵抗率
CONTROL_RESIST							= 30053		# 控制抵抗率
INSANE_RESIST							= 30054		# 心智抵抗率
DAMAGECORRECTION						= 40001 	# 造成伤害修正
ARMORCORRECTION							= 40002		# 承受伤害修正
ATTACK_DAMAGECORRECTION					= 40003		# 造成物理伤害修正
MAGIC_DAMAGECORRECTION					= 40004		# 造成法术伤害修正
ATTACK_ARMORCORRECTION					= 40005		# 承受物理伤害修正
MAGIC_ARMORCORRECTION					= 40006		# 承受法术伤害修正
ROLE_DAMAGECORRECTION					= 40007		# 造成对玩家伤害修正
PET_DAMAGECORRECTION					= 40008		# 造成对幻兽伤害修正
MONSTER_DAMAGECORRECTION				= 40009		# 造成对怪物伤害修正
ROLE_ARMORCORRECTION					= 40010		# 承受玩家伤害修正
PET_ARMORCORRECTION						= 40011		# 承受幻兽伤害修正
MONSTER_ARMORCORRECTION					= 40012		# 承受怪物伤害修正
CURECORRECTION							= 40013 	# 治疗加深
BECURECORRECTION						= 40014		# 承受治疗加深
ICE_DAMAGECORRECTION					= 40015		# 造成冰元素伤害修正
FIRE_DAMAGECORRECTION					= 40016		# 造成火元素伤害修正
THUNDER_DAMAGECORRECTION				= 40017		# 造成雷元素伤害修正
XUAN_DAMAGECORRECTION					= 40018		# 造成玄元素伤害修正
ICE_ARMORCORRECTION						= 40019		# 承受冰元素伤害修正
FIRE_ARMORCORRECTION					= 40020		# 承受火元素伤害修正
THUNDER_ARMORCORRECTION					= 40021		# 承受雷元素伤害修正
XUAN_ARMORCORRECTION					= 40022		# 承受玄元素伤害修正
HATRED_CORRECTION						= 40023		# 造成仇恨修正
RELATED_HATRED_CORRECTION				= 40024		# 造成连带仇恨修正
EXPCORRECTION							= 40025		# 经验修正
POTENTIALCORRECTION						= 40026		# 潜能修正
XIUWEICORRECTION						= 40027		# 修为修正
MONEYCORRECTION							= 40028		# 金币修正
BANGGONGCORRECTION						= 40029		# 帮贡修正
FEATSCORRECTION							= 40030		# 功勋修正
MORALECORRECTION						= 40031		# 气运修正
BARRACKSEXPCORRECTION					= 40032		# 养兵经验修正
INTEGRALCORRECTION						= 40033		# 金精修正
PSIONICCORRECTION						= 40034		# 灵能修正
EXPLOITCORRECTION						= 40035		# 军功修正
BINDMONEYCORRECTION						= 40036		# 绑金修正
XIANSHICORRECTION						= 40037		# 仙石修正
LINGSHICORRECTION						= 40038		# 灵石修正
XUANSHICORRECTION 						= 40039		# 玄石修正

# 复合属性，玩家身上没有这些属性，用于装备
ALL_DAMAGE_IGNORE						= 50001 	# 外功＋内功攻击忽视	：外功攻击忽视、内功攻击忽视
ALL_ARMOR_IGNORE						= 50002		# 外功＋内功防御忽视	：外功防御忽视、内功防御忽视
ALL_BASE_PROPERTY						= 50003		# 全基础属性			：根骨、筋力、内力、洞察、身法
ALL_STOCK_PROPERTY						= 50004		# 全存量属性			：生命、法力
ALL_ELEMENT_DAMAGE						= 50005		# 全元素攻击 		：冰元素攻击、火元素攻击、雷元素攻击、玄元素攻击
ALL_ELEMENT_ARMOR						= 50006		# 全元素防御 		：冰元素防御、火元素防御、雷元素防御、玄元素防御
ALL_ELEMENT_DAMAGE_IGNORE				= 50007 	# 全元素攻击忽视		：冰元素攻击忽视、火元素攻击忽视、雷元素攻击忽视、玄元素攻击忽视
ALL_ELEMENT_ARMOR_IGNORE				= 50008		# 全元素防御忽视		：冰元素防御忽视、火元素防御忽视、雷元素防御忽视、玄元素防御忽视


#基础属性对应关系 xxx_base
PROPERTYIDTOSTR = {
					CORPOREITY			: 'corporeity',
					STRENGTH			: 'strength',
					INTELLECT			: 'intellect',
					DISCERN				: 'discern',
					DEXTERITY			: 'dexterity',
					HP					: 'HP_Max',
					MP					: 'MP_Max',
					DAMAGE				: 'damage',
					MAGICDAMAGE			: 'magic_damage',
					ARMOR				: 'armor',
					MAGICARMOR			: 'magic_armor',
					CRITICALSTRIKE		: 'criticalstrike',
					PARRY				: 'parry',
					SPEED				: 'speed',
					HITRATE				: 'hitrate',
					DODGERATE			: 'dodgerate',
					HEALINGRATE			: 'healingrate',
					GANGQI_MAX			: 'gangQiValue_Max',
					GANGQI_DAMAGE_POINT		: 'gangQi_damagePoint',
					GANGQI_ARMOR_POINT		: 'gangQi_armorPoint',
					GANGQI_QIJIE_REVIVE		: 'gangQi_qiJieRevive',
					GANGQI_QIYING_REVIVE	: 'gangQi_qiYingRevive',
					TEMPSPEED				: 'tempSpeed',
					CURE					: 'cure',
					CRITRATIO				: 'critRatio',
					PARRYRATIO				: 'parryRatio',
					DAMAGECORRECTION 		: 'damage_correction',
					ARMORCORRECTION 		: 'armor_correction',
					ATTACK_DAMAGECORRECTION	: 'attack_damage_correction',
					MAGIC_DAMAGECORRECTION	: 'magic_damage_correction',
					ATTACK_ARMORCORRECTION	: 'attack_armor_correction',
					MAGIC_ARMORCORRECTION	: 'magic_armor_correction',
					ROLE_DAMAGECORRECTION	: 'role_damage_correction',
					PET_DAMAGECORRECTION	: 'pet_damage_correction',
					MONSTER_DAMAGECORRECTION: 'monster_damage_correction',
					ROLE_ARMORCORRECTION	: 'role_armor_correction',
					PET_ARMORCORRECTION		: 'pet_armor_correction',
					MONSTER_ARMORCORRECTION	: 'monster_armor_correction',
					CURECORRECTION			: 'curecorrection',
					BECURECORRECTION		: 'becuredcorrection',
					EXPCORRECTION			: 'get_exp_correction',
					POTENTIALCORRECTION		: 'get_potential_correction',
					XIUWEICORRECTION		: 'get_xiuwei_correction',
					MONEYCORRECTION			: 'get_money_correction',
					BANGGONGCORRECTION		: 'get_tongContribute_correction',
					FEATSCORRECTION			: 'get_feats_correction',
					MORALECORRECTION		: 'get_campMorale_correction',
					BARRACKSEXPCORRECTION	: 'get_barracksExp_correction',
					INTEGRALCORRECTION		: 'get_integral_correction',
					PSIONICCORRECTION		: 'get_psionic_correction',
					EXPLOITCORRECTION		: 'get_exploit_correction',
					BINDMONEYCORRECTION		: 'get_bindmoney_correction',
					XIANSHICORRECTION		: 'get_xianshi_correction',
					LINGSHICORRECTION		: 'get_lingshi_correction',
					XUANSHICORRECTION		: 'get_xuanshi_correction',
					ICE_DAMAGE				: 'ice_damage',
					FIRE_DAMAGE				: 'fire_damage',
					THUNDER_DAMAGE			: 'thunder_damage',
					XUAN_DAMAGE				: 'xuan_damage',
					ICE_ARMOR				: 'ice_armor',
					FIRE_ARMOR				: 'fire_armor',
					THUNDER_ARMOR			: 'thunder_armor',
					XUAN_ARMOR				: 'xuan_armor',
					ICE_DAMAGECORRECTION	: 'ice_damage_correction', 
					FIRE_DAMAGECORRECTION	: 'fire_damage_correction',
					THUNDER_DAMAGECORRECTION: 'thunder_damage_correction',
					XUAN_DAMAGECORRECTION	: 'xuan_damage_correction',
					ICE_ARMORCORRECTION		: 'ice_armor_correction',
					FIRE_ARMORCORRECTION	: 'fire_armor_correction',
					THUNDER_ARMORCORRECTION	: 'thunder_armor_correction',
					XUAN_ARMORCORRECTION	: 'xuan_armor_correction',
					HATRED_CORRECTION		: 'hatred_correction',
					RELATED_HATRED_CORRECTION: 'related_hatred_correction',
					DAMAGE_IGNORE			: 'damage_ignore',
					MAGICDAMAGE_IGNORE		: 'magic_damage_ignore',
					ARMOR_IGNORE			: 'armor_ignore',					
					MAGICARMOR_IGNORE		: 'magic_armor_ignore',
					CRITICALSTRIKE_IGNORE	: 'criticalstrike_ignore',
					PARRY_IGNORE			: 'parry_ignore',
					HITRATE_IGNORE			: 'hitrate_ignore',
					DODGERATE_IGNORE		: 'dodgerate_ignore',
					ICE_DAMAGE_IGNORE		: 'ice_damage_ignore',
					FIRE_DAMAGE_IGNORE		: 'fire_damage_ignore',
					THUNDER_DAMAGE_IGNORE	: 'thunder_damage_ignore',
					XUAN_DAMAGE_IGNORE		: 'xuan_damage_ignore',
					ICE_ARMOR_IGNORE		: 'ice_armor_ignore',
					FIRE_ARMOR_IGNORE		: 'fire_armor_ignore',
					THUNDER_ARMOR_IGNORE	: 'thunder_armor_ignore',
					XUAN_ARMOR_IGNORE		: 'xuan_armor_ignore',
					DEPRESS_RESIST			: 'depress_resist',
					HITBACK_RESIST			: 'hitback_resist',
					CONTROL_RESIST			: 'control_resist',
					INSANE_RESIST			: 'insane_resist',
	}

#属性对应战斗力的修正值
PROPERTYIDTOPOWNER = {
					CORPOREITY			: 119.04,
					STRENGTH			: 113.4,
					INTELLECT			: 88.38,
					DISCERN				: 62.58,
					DEXTERITY			: 62.58,
					HP					: 15.83,
					MP					: 5.28,
					DAMAGE				: 34.72,
					MAGICDAMAGE			: 32.21,
					ARMOR				: 104.66,
					MAGICARMOR			: 103.82,
					CRITICALSTRIKE		: 39.27,
					PARRY				: 63.5,
	}

MAXLIMITVALUE							= 99999999			# 目前属性最大值
PRECENTRATIO							= 10000				# 一些百分数用到的比率基准值是一万

BASEPROPERTYRANGE						= (0, MAXLIMITVALUE)						# base属性值范围
EXTRAPROPERTYRANGE						= (0, MAXLIMITVALUE)						# extra属性值范围
PRECENTPROPERTYRANGE					= (-PRECENTRATIO, PRECENTRATIO)			# precent属性值范围，此值需要除以10000,用于实际计算
VALUEPROPERTYRANGE						= (0-MAXLIMITVALUE, MAXLIMITVALUE)			# value属性值范围
RESULTPROPERTYRANGE						= (0, MAXLIMITVALUE)						# 属性值计算结果的范围

#以下属性有4个类似属性，如 strength（玩家本身的属性）， strength_base（装备增加）， strength_extra（buff增加）， strength_percent（百分比增加）
#一级属性
ONEPROPERTIES = [ CORPOREITY, STRENGTH, INTELLECT, DISCERN, DEXTERITY ]

#二级属性，由一级属性计算
TWOPROPETYTIES = [ HP, MP, DAMAGE, MAGICDAMAGE, ARMOR, MAGICARMOR, CRITICALSTRIKE, PARRY, SPEED, HITRATE, DODGERATE, HEALINGRATE, 
GANGQI_MAX, GANGQI_DAMAGE_POINT, GANGQI_ARMOR_POINT, GANGQI_QIJIE_REVIVE, GANGQI_QIYING_REVIVE, DAMAGECORRECTION, ARMORCORRECTION,
ATTACK_DAMAGECORRECTION, MAGIC_DAMAGECORRECTION, ATTACK_ARMORCORRECTION, MAGIC_ARMORCORRECTION, ROLE_DAMAGECORRECTION, PET_DAMAGECORRECTION,
MONSTER_DAMAGECORRECTION, ROLE_ARMORCORRECTION, PET_ARMORCORRECTION, MONSTER_ARMORCORRECTION, CURE, CURECORRECTION, BECURECORRECTION, 
PARRYRATIO, CRITRATIO, ICE_DAMAGE, FIRE_DAMAGE, THUNDER_DAMAGE, XUAN_DAMAGE, ICE_ARMOR, FIRE_ARMOR, THUNDER_ARMOR, XUAN_ARMOR, 
ICE_DAMAGECORRECTION, FIRE_DAMAGECORRECTION, THUNDER_DAMAGECORRECTION, XUAN_DAMAGECORRECTION, ICE_ARMORCORRECTION, FIRE_ARMORCORRECTION,
THUNDER_ARMORCORRECTION, XUAN_ARMORCORRECTION, HATRED_CORRECTION, RELATED_HATRED_CORRECTION, DAMAGE_IGNORE, MAGICDAMAGE_IGNORE,
ARMOR_IGNORE, MAGICARMOR_IGNORE, CRITICALSTRIKE_IGNORE, PARRY_IGNORE, HITRATE_IGNORE, DODGERATE_IGNORE, ICE_DAMAGE_IGNORE,
FIRE_DAMAGE_IGNORE, THUNDER_DAMAGE_IGNORE, XUAN_DAMAGE_IGNORE, ICE_ARMOR_IGNORE, FIRE_ARMOR_IGNORE, THUNDER_ARMOR_IGNORE,
XUAN_ARMOR_IGNORE, DEPRESS_RESIST, HITBACK_RESIST, CONTROL_RESIST, INSANE_RESIST]

#复合类属性
COMPOSITIONPROPERTIES = {
						ALL_DAMAGE_IGNORE : [DAMAGE_IGNORE, MAGICDAMAGE_IGNORE],
						ALL_ARMOR_IGNORE : [ARMOR_IGNORE, MAGICARMOR_IGNORE],
						ALL_BASE_PROPERTY : [ CORPOREITY, STRENGTH, INTELLECT, DISCERN, DEXTERITY ],
						ALL_STOCK_PROPERTY : [HP, MP],
						ALL_ELEMENT_DAMAGE : [ICE_DAMAGE, FIRE_DAMAGE, THUNDER_DAMAGE, XUAN_DAMAGE],
						ALL_ELEMENT_ARMOR : [ICE_ARMOR, FIRE_ARMOR, THUNDER_ARMOR, XUAN_ARMOR],
						ALL_ELEMENT_DAMAGE_IGNORE : [ICE_DAMAGE_IGNORE, FIRE_DAMAGE_IGNORE, THUNDER_DAMAGE_IGNORE, XUAN_DAMAGE_IGNORE],
						ALL_ELEMENT_ARMOR_IGNORE : [ICE_ARMOR_IGNORE, FIRE_ARMOR_IGNORE, THUNDER_ARMOR_IGNORE, XUAN_ARMOR_IGNORE]
						}

#------------------CST-3393 战斗力计算 -----------------
# 价值(系数)
PROPERTY_FACTOR = {
					CORPOREITY 		: 119.04,
					STRENGTH 		: 113.4,
					INTELLECT 		: 88.38,
					DISCERN			: 62.58,
					DEXTERITY 		: 62.58,
					HP 				: 15.83,
					MP 				: 5.28,
					DAMAGE 			: 34.72,
					MAGICDAMAGE		: 32.21,
					ARMOR			: 104.66,
					MAGICARMOR		: 103.82,
					CRITICALSTRIKE 	: 39.27,
					PARRY			: 63.5
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


# 物品大类
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




# 原兽食材类型
ORIGIN_PET_FOOD_TYPE_COMMON			= 0		# 通用食材
ORIGIN_PET_FOOD_TYPE_VEGETARIAN		= 1		# 素食食材
ORIGIN_PET_FOOD_TYPE_CARNIVOROUS	= 2		# 肉食食材