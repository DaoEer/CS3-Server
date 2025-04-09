#-*-coding:utf-8-*-

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
ITEM_BLOOD								= 5			# 重铸保护符

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

SPACECOPY_LOCKCECAPACITY				= 8

BAG_SPACE_COPY							= 6		# 玩家副本专用背包
BAG_SPACECOPY_START						= BAG_TONG_STORE_END + 1								# 起始位992
BAG_SPACECOPY_END						= BAG_SPACECOPY_START + SPACECOPY_LOCKCECAPACITY - 1		# 结束位999


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
PRECENTPROPERTYRANGE					= (-PRECENTRATIO/2.0, PRECENTRATIO)			# precent属性值范围，此值需要除以10000,用于实际计算
VALUEPROPERTYRANGE						= (0-MAXLIMITVALUE, MAXLIMITVALUE)			# value属性值范围
RESULTPROPERTYRANGE						= (0, MAXLIMITVALUE)						# 属性值计算结果的范围

#以下属性有4个类似属性，如 strength（玩家本身的属性）， strength_base（装备增加）， strength_extra（buff增加）， strength_percent（百分比增加）
#一级属性
ONEPROPERTIES = [ CORPOREITY, STRENGTH, INTELLECT, DISCERN, DEXTERITY ]

#二级属性，由一级属性计算
TWOPROPETYTIES = [ HP, MP, DAMAGE, MAGICDAMAGE, ARMOR, MAGICARMOR, CRITICALSTRIKE, PARRY, SPEED, HITRATE, DODGERATE, HEALINGRATE, 
GANGQI_MAX, GANGQI_DAMAGE_POINT, GANGQI_ARMOR_POINT, GANGQI_QIJIE_REVIVE, GANGQI_QIYING_REVIVE, DAMAGECORRECTION, ARMORCORRECTION,
ATTACK_DAMAGECORRECTION, MAGIC_DAMAGECORRECTION, ATTACK_ARMORCORRECTION, MAGIC_ARMORCORRECTION, ROLE_DAMAGECORRECTION, PET_DAMAGECORRECTION,
MONSTER_DAMAGECORRECTION, ROLE_ARMORCORRECTION, PET_ARMORCORRECTION, MONSTER_ARMORCORRECTION]


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

