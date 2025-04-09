# -*- coding: utf-8 -*-
import csdefine
import ItemTypeEnum

#----------------------space cellapp data key----------------
CELLAPP_DATA_SPACE_KEY = "SPACE_BASE.%s"
GET_SPACE_CELLAPP_KEY = lambda spaceID:CELLAPP_DATA_SPACE_KEY%spaceID
CELLAPP_DATA_SPACE_KEY_1 = "SPACE_CELL.%s"
GET_SPACE_CELLAPP_KEY_1 = lambda spaceID:CELLAPP_DATA_SPACE_KEY_1%spaceID


#----------------------space data----------------------
SPACE_DATA_SCRIPT_ID 	= "SPACE_SCRIPT_ID"
SPACE_DATA_SPACE_ID		= "SPACE_ID"
SPACE_DATA_BELONG_TYPE	= "SPACE_DATA_BELONG_TYPE"
SPACE_DATA_REVIVE_TYPE	= "SPACE_REVIVE_TYPE"
SPACE_DATA_SPACE_TYPE	= "SPACE_TYPE"
SPACE_DATA_RELATION_MODE= "SPACE_RELATION_MODE"
SPACE_DATA_LINE_NUMBER	= "SPACE_DATA_LINE_NUMBER"
SPACE_DATA_MAX_LINE_NUMBER = "SPACE_DATA_MAX_LINE_NUMBER"

SPACE_LIFE_NOTIFY_TIME = 10.0		# 副本时限剩余多少秒时给予提示

BUNCH_SPACE_TELEPORT_BOX_ID = "40000011"	#副本串传送物件ID
BUNCH_RECORD_SPACE_STR = "recordSpace"		#出副本标识

FIGHT_CHECK_TIMER			= 8				# 战斗检测时间

TEAM_ENTER_SPACE_RANGE = 20		# 进副本队伍距离

#----------------------equip data----------------------
EQUIP_INTENSIFY_NEED_LEVEL = 20			# 可强化装备等级
EQUIP_INTENSIFY_NEED_QUALITY = 2		# 可强化装备品质
EQUIP_INTENSIFY_MAX_LEVEL_MAPS = {2:5, 3:5, 4:7, 5:9, 6:12, 7:15}	# 装备强化等级上限表
EQUIP_SHUFFLE_NEED_LEVEL = 30			# 可洗练装备等级
EQUIP_DIOGRAPHY_BW_LEVEL = 10			# 装备传星之间的最大等级
EQUIP_RECAST_NEED_LEVEL = 30			# 可重铸装备等级
EQUIP_COMPOSE_MONEY_TO_XIANSHI = 164	# 1仙石=164金币

#----------------------state data--------------------
FIGHT_START_TIME = 1.0
FIGHT_INTERVAL_TIME = 3.0

FREE_START_TIME = 1.0

NPC_DESTORY_SELF = 8.0										#monster/npc销毁默认时间

#--------------------unfinishDes---------------------
UNFINISH_QUEST_DESCRIPT = "Q010199"							# 默认未完成语音

#--------------------move----------------------------
WANDER_RADIUS = (2, 10)										# 游荡范围
WANDER_TIMES = 4.0											# 游荡间隔时间
WANDER_CHANGE_YAW_TIMES = 0.5								# 游荡转向间隔时间
WANDER_YAW_DICT = {"front":0.0, "back": -180.0, "left":-90.0, "right":90.0}

CHASE_ENTITY_RANGE = ( 0.8, 1.95 )							# 追击靠近范围

#--------------------gm data---------------------
CLONE_MONSTER_MAX_COUNT = 50

#--------------------skill data------------------
SKILL_MIN_HIT_TIME = 0.01	#技能打击点打击时间小于等于此值则马上打击，不加延时timer

#-------------------falling data-----------------
ROLE_DROP_DAMAGE_HEIGHT				= 15.0										# 跌落伤害的高度
ROLE_DROP_DAMAGE_SPEED				= 24.0										# 开始跌落伤害的速度
ROLE_DROP_DEAD_SPEED				= 48.0										# 致死跌落伤害的速度

#------------------refine-------------------------
BUFF_REFINE_AREA = 16019201				# 炼化池buffID

#------------------loopQuest-------------------------
REWARD_MONEY_BY_ROLL = { 1:0.15, 2:0.4, 3:0.7 }			# 环任务根据任务难度，获得金钱奖励的概率
QUEST_OF_NUM_LOOP	= 18								# 每轮的任务数量
MUST_LOOP_QUEST_TYPE				= [ 1 , 2 ]			# 环任务必须的任务( ( 传话,拜访)、送宝)
ORDINARY_LOOP_QUEST_TYPE			= 3					# 普通环任务类型
LOOP_QUEST_RING_NUM					= 3					# 环任务的环数

#------------------VehiclePet-------------------------
VPET_CAGE_MAX = 6						# 可携带幻兽最大个数
VPET_DELAY_DEAD_TIME = 2				# 幻兽死亡销毁时间
MOUNT_ON_PET_SKILLID = 240004001		# 上坐骑的技能ID
PET_DIST_ROLE = 1						# 幻兽与玩家之间的距离
CAN_FREE_PET_LEVEL = 20					# 20级才能放生
MOUNT_PET_ACT_FORBID = [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_USE_ITEM,
	csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_EMERGENCY_EXIT]
	
STAND_ONE_SECTION_JUMP_SKILLID = 240000001;			# 站立一段跳技能ID
MOVE_ONE_SECTION_JUMP_SKILLID = 240001001;			# 前进一段跳技能ID
TWO_SECTION_JUMP_SKILLID = 240002001;				# 二段跳技能ID
THREE_SECTION_JUMP_SKILLID = 240003001;				# 三段跳技能ID
#------------------岩浆伤害BuffID-----------
MAGMA_DAMAGE_BUFFID = 12008701

#------------------仙化倍率-----------、
SPAR_ITEM_RATE = 1.5

#------------------ghostReceiver默认生命周期----------
GHOST_RECEIVER_DEAD_TIME = 1.0
GHOST_RECEIVER_DELAY_SPELL = 0.2

DEFAULT_AOI_RADIUS = 80.0	# 默认AIO范围
DEFAULT_AOI_EXTRA_RADIUS = 5.0	# 引擎默认的：超过AOI区域的滞后区域

MIN_SCOUT_HEIGHT = 5.0		# 最小侦测高度

#--------------------猜大小 定义------------------------------
SIZE_DEFINE = { 0:[1,2,3], 1:[4,5,6] }


SKILL_FILTER_ENTITYS = [
	csdefine.ENTITY_FLAG_UNKNOWN,
	csdefine.ENTITY_FLAG_NPC,
	csdefine.ENTITY_FLAG_DOOR,
	csdefine.ENTITY_FLAG_PLATFORM,
	csdefine.ENTITY_FLAG_DROP_BOX,
	csdefine.ENTITY_FLAG_GHOST_RECEIVER,
	csdefine.ENTITY_FLAG_SPACE,
	csdefine.ENTITY_FLAG_TRAP,
]

ACRION_FORBID_OTHER_ACTION = [ csdefine.ACTION_FORBID_SPELL,csdefine.ACTION_FORBID_EMERGENCY_EXIT ]

#----------------------------变身NPC------------------------------------
BEGIN_CHANGE_BODY_TIME = 10.0			# NPC创建好后开始变身时间
CHANGE_BODY_TIME = 4.0					# 变身准备时间，（播放即将要变啥语音时间）
CHANGE_BODY_ROLL = 0.4 					# 变身NPC语音正确的概率
CHECK_CHANGE_BODY_TIME = 6.0			# 变身某一次时间和检测是否变身正确的时间
CHANGE_BODY_NUM = 12					# 可允许变身的次数
CHANGE_BODY_CHECK_ROLE_RANGE = 20.0		# 检测附近玩家的范围
CHANGE_BODY_DATAS = { "SK_GW0034_Mon" : { "buffID": 23000001, "voice": "Cy000110" },
					"SK_GW2423_Mon" : { "buffID": 23000002, "voice": "Cy000106" },
					"SK_GW0072_Mon" : { "buffID": 23000003, "voice": "Cy000108" },
					"SK_GW0344_Mon" : { "buffID": 23000004, "voice": "Cy000107" },
					"SK_GW0042_C_Mon" : { "buffID": 23000005, "voice": "Cy000105" },
					"SK_GW0121_Mon" : { "buffID": 23000006, "voice": "Cy000109" },
					"SK_GW0365_Mon" : { "buffID": 23000007, "voice": "Cy000104" },
					"SK_GW0028_Mon" : { "buffID": 23000008, "voice": "Cy000103" },
}

BUFF_GANG_QI_BLOCK = 90000201			#罡气格挡表现buff
BUFF_GANG_QI_QI_JIE = 90000202	#罡气气竭破绽buff

#----------------------------trap data------------------------------------
PERMISSIBLE_MAX_RANGE = 20 	#客户端陷阱触发，在服务器有效性验证最大允许范围

#----------------------------妖魔化身------------------------------------
DEMON_PART_MODEL = {"modelNumber": {"SK_NPCM2000_Mon":"Cy000143","SK_NPCM2001_Mon":"Cy000142"}}
SEX_TO_MODEL = {
	"SK_NPCM2000_Mon":{"coatModel": {"SK_NPCM2000_Dx":"Cy000148","SK_NPCM2000_Cx":"Cy000149"}, \
		"hatModel": {"SK_NPCM2000_Ts":"Cy000146","":"Cy000147"}, \
		"handModel": {"SK_NPCM2000_St":"Cy000145","":"Cy000144"}, \
		"waistModel": {"SK_NPCM2000_Ps":"Cy000150","":"Cy000151"}\
		},
	"SK_NPCM2001_Mon":{"pantsModel": {"SK_NPCM2001_Dq":"Cy000152","SK_NPCM2001_Cq":"Cy000153"}, \
		"cloakModel": {"SK_NPCM2001_Pf":"Cy000154","":"Cy000155"}, \
		"waistModel": {"SK_NPCM2001_Ps":"Cy000156","":"Cy000157"}, \
		"handModel":{"SK_NPCM2001_St":"Cy000158","":"Cy000159"}
		}
	}
	
#----------------------------雷域试炼------------------------------------
LEI_SCRIPTID_TO_BUFFID = {"20004031":14002301,  "20004032":14002302,  "20004033":14002303,  "20004034":14002304, \
	"20004035":14002305,  "20004036":14002306,  "20004037":14002307,  "20004038":14002308,  "20004039":14002309, \
	"20004040":14002310,  "20004041":14002311,  "20004042":14002312,  "20004043":14002313,  "20004044":14002314, \
	"20004045":14002315,  "20004046":14002316,  "20004047":14002317,  "20004048":14002318}
#---------------------------------------------物品名称颜色品质映射表-------------------------
ITEM_NAME_QUALITY_COLORS = {
		ItemTypeEnum.QUALITY_WHITE:"(255, 255, 255, 255)",
		ItemTypeEnum.QUALITY_BLUE:"(51, 204, 255, 255)",
		ItemTypeEnum.QUALITY_GOLD:"(255, 224, 54, 255)",
		ItemTypeEnum.QUALITY_PINK:"(255, 128, 128,  255)",
		ItemTypeEnum.QUALITY_GREEN:"(99, 255, 158, 255)",
		ItemTypeEnum.QUALITY_GREEN_TIAN:"(99, 255, 158, 255)",
		ItemTypeEnum.QUALITY_GREEN_SHENG:"(99, 255, 158, 255)",
}
MSG_FORMAT_COLOR_STRING = "@F{fc=%s}%s"
#----------------------------幻阵迷宫------------------------------------
MAZE_SPACE_SCRIPTID = ["fu_ben_L_HZMG1", "fu_ben_L_HZMG2", "fu_ben_L_HZMG3", "fu_ben_L_HZMG4", "fu_ben_L_HZMG5", "fu_ben_L_HZMG6", "fu_ben_L_HZMG7", "fu_ben_L_HZMG8", "fu_ben_L_HZMG9","fu_ben_L_HZMG10"]
MAZE_SPACE_MAIN_SCENE = "mainSpace"	#幻阵迷宫主场景
MAZE_DELAY_MOVE_TIME = 1.0			# 延迟移动
FLY_SPEED = 4000										
MAGIC_MAZE_ANSWER_GOOD_RATE = 0.5
MAGIC_MAZE_ANSWER_OPTION_LIST = ["a","b","c","d"]
MAGIC_MAZE_SHANG_CHI_BANG = 1
MAGIC_MAZE_XIA_CI_BANG = 2
MAGIC_MAZE_XUAN_WU = 3
MAGIC_MAZE_WEN_HAO = 4
MGGIC_MAZE_WEN_HAO_FU_BEN = 1
MGGIC_MAZE_WEN_HAO_QI_YU = 2
MGGIC_MAZE_WEN_HAO_BAO_XIANG = 3
MGGIC_MAZE_WEN_HAO_WEN_DA = 4
#气运副本：天地玄黄空日月（第三版）
MAGIC_MAZE_LUCK_COPY_TIAN	= 1
MAGIC_MAZE_LUCK_COPY_DI		= 2
MAGIC_MAZE_LUCK_COPY_XUAN	= 3
MAGIC_MAZE_LUCK_COPY_HUAN1	= 4
MAGIC_MAZE_LUCK_COPY_KONG	= 5
MAGIC_MAZE_LUCK_COPY_DAY	= 6
MAGIC_MAZE_LUCK_COPY_MONTH	= 7
MAGIC_MAZE_LUCK_COPY_HUAN2	= 8
#四组幻阵迷宫飞到第一点设置位置(第二版)
MAZE_SPACE_SCRIPTID_ONE 	= "fu_ben_L_HZMG1"
MAZE_SPACE_SCRIPTID_TWO 	= "fu_ben_L_HZMG2"
MAZE_SPACE_SCRIPTID_THREE 	= "fu_ben_L_HZMG3"
MAZE_SPACE_SCRIPTID_FOUR	= "fu_ben_L_HZMG4"
MAZE_SPACE_DIRECTION_ONE 	= ( 0, 0, 0 )
MAZE_SPACE_DIRECTION_TWO 	= ( 0, 0, -52 )
MAZE_SPACE_DIRECTION_THREE 	= ( 0, 0, -35 )
MAZE_SPACE_DIRECTION_FOUR 	= ( 0, 0, -43 )
#迷幻丛书玩法：答案字数
MAGIC_MAZE_THREE = 3
MAGIC_MAZE_FOUR	 = 4

#-----------------CST-2149 灵箭华元-------------------
BUFF_SHIELD_FIGHTER		=  15001201	#战士举盾状态下的BuffID
BUFF_SHIELD_SWORDMAN	=  15001202	#剑客举盾状态下的BuffID
BUFF_SHIELD_ARCHER		=  15001203	#链刃举盾状态下的BuffID
BUFF_SHIELD_MAGE		=  15001204	#法师举盾状态下的BuffID

#-----------------CST-3660 荷花法阵-------------------
BUFF_HHFZ_MALE_FIGHTER		=  11017205	#战士上荷花姿势的BuffID
BUFF_HHFZ_MALE_SWORDMAN		=  11017206	#剑客上荷花姿势的BuffID
BUFF_HHFZ_MALE_ARCHER		=  11017207	#链刃上荷花姿势的BuffID
BUFF_HHFZ_MALE_MAGE			=  11017208	#链刃上荷花姿势的BuffID
BUFF_HHFZ_FEMALE_FIGHTER		=  11017209	#战士上荷花姿势的BuffID
BUFF_HHFZ_FEMALE_SWORDMAN		=  11017210	#剑客上荷花姿势的BuffID
BUFF_HHFZ_FEMALE_ARCHER		=  11017211	#链刃上荷花姿势的BuffID
BUFF_HHFZ_FEMALE_MAGE			=  11017212	#链刃上荷花姿势的BuffID


#-----------------CST-4564 拷问玩法 -------------------
SKILL_KWWF_ROLE			=  110331002 #玩家切换武器姿势

#-----------------CST-6526 冥域缉凶----------------------
MYJX_MACHINE_TRAP_SCRIPTID = "30000681" # 机关陷阱scriptID

#-----------------帮会--------------------------
TONG_CREATE_NEED_MONEY		= 10000			# 创建帮会需要消耗10000金币
TONG_CREATE_MIX_LEVEL		= 20			# 创建帮会最低等级
TONG_CREATE_MIX_JINJIELEVEL = 4				# 创建帮会玩家境界等级必须达到4级
TONG_JOIN_MIX_LEVEL			= 20			# 加入帮会最低等级

TONG_SPACE_SCRIPTID			= "L_BHLD"
TONG_SPACE_POSITION			= ( -1.9, 2.25, -183.60 )
TONG_SPACE_DIRECTION		= ( 0, 0, 0 )

TONG_ANSWER_OPTION_LIST = ["a","b","c","d"]


#九字真言副本(配置为UE4坐标)
TONG_SPACECOPY_JIUZIZHENYAN_SCRIPT = ""
TONG_SPACECOPY_JIUZIZHENYAN_POSITION = ()
TONG_SPACECOPY_JIUZIZHENYAN_DIRECTION = ()

#-----------------日常任务--------------------------
QUEST_ACEEPT_TWICE_ODDS			= 0.1			# 10%概率接第二个任务
ACCEPT_DAILY_QUEST_TWICE_SOUND	= "other010050 "# 接取第二个任务语音ID
#-----------------晶石狩猎场--------------------------
INTEGRAL_DOUBLE_BUFF_LIST =	[12058709,12058710]
KILL_VOICE	= "C000287"  # 超神和首杀的语音ID

#----------------------------附身技能施法成功提示id-----------------------
SKILL_POSSESS_SUCC_TIPS_ID = 1


#---------------------------装备强化--------------------------------------
INTENSIFY_SAVE_SLOT_MAX_NUM = 5				# 装备强化备份最大数目
INTENSIFY_SAVE_ONE_SLOT_COST = 50000			# 开放第一个强化备份栏目消耗 50000金币
INTENSIFY_SAVE_TWO_SLOT_COST = 200000			# 开放第二个强化备份栏目消耗 200000金币

#----------------------------晶石狩猎场前三-----------------------
SPAR_HUNTING_MONEY_RANK_FIRST = "第一"
SPAR_HUNTING_MONEY_RANK_SECOND = "前二"
SPAR_HUNTING_MONEY_RANK_THIRD = "前三"


#---------传送石相关---------------------------------------
TELEPORTSTONE_ITEMID = 205010002

#-------------------------重置原地复活消耗的时间----------------------
RECOVER_REVIVE_DATA_TIME = 3600

#---------------------------脱离卡死消耗时间-------------------------
DISCONNECT_CD_TIME = 600

#-------------------------灵脉战场-------------
LMZC_SPACE_SCRIPTID				 = "fu_ben_L_LMZC"	# 灵脉战场space
LMZC_CREATE_ENTITY_BY_POWERPOINT = 300				# 灵能点每300点，刷出一个葫芦
LMZC_POWER_POINT_WINNER			 = 2000				# 优先获得2000点灵能点数的一方获胜
LMZC_CREATE_TAOSIM_CENTER_POS	 = ( 59.26, -66.89, 220.98 ) # 仙道葫芦中心位置
LMZC_CREATE_DEMON_CENTER_POS	 = (-30.17, -61.66, -180.25) # 魔道葫芦中心位置
# 仙道葫芦刷新位置
LMZC_CREATE_TAOSIM_CRYSTAL_POS	 = [( 59.32, -66.89, 220.36), ( 40.19, -66.97, 222.10), ( 78.93, -66.97,221.15),
	( 58.79, -66.97,240.77), ( 40.50, -66.97,237.27), ( 78.26, -66.97,238.78), ( 60.02, -66.97,202.02),
	( 44.96, -66.40,199.09), ( 75.22, -66.78,201.51), ( 60.18, -66.97,190.35)]
# 魔道葫芦刷新位置
LMZC_CREATE_DEMON_CRYSTAL_POS	 = [( -30.31, -61.66, -179.47), ( -14.67, -61.76, -179.01), ( -48.92, -61.36, -186.16),
	( -11.92, -61.36, -196.45), ( -27.23, -61.80, -197.01), ( -54.46, -61.36, -202.20), ( -35.71, -61.74, -168.80),
	( -23.44, -61.80, -162.32), ( -44.60, -61.80, -163.19 ), ( -33.16 ,-61.80, -156.24)]

LMZC_POWER_POINT_CRYSTAL_SCRIPTID= "40000143"			# 葫芦scriptID
#-------------------------复活道具ID-------------------------
REVIVE_ITEMID	= 205010001	

FENG_MING_CHENG_SCRIPTID = "L_FMC"					# 凤鸣城ScriptID

#------------------------冰雪之战----------------------
FROZEN_FIGHT_SPACE_SCRIPTID    	= "fu_ben_L_BXZZ" 			   #冰雪之战space

#------------------------英雄联盟----------------------
NOTDUPLICATE_MONSTER_SCRIPTID = "20008025"			# 不可重复的怪物

#------------------------CST-7419 金树种子 任务ID----------------------
JSZZ_QUEST_ID = 80135054

#-----------------------帮会争霸 第二场----------------
TONG_STARCRAFT_DOUBLE_INTEGRAL_BUFF = [12166601,12166701]
TONG_STARCRAFT_WATCH_BUFF = 1111111

#帮会争霸 每个参加的人数
TONG_STARCRAFT_JOIN_MEMBER = 20

#环任务
LOOP_QUEST_CAN_ACCEPT_NUM			= 54						# 环任务一天可以完成3轮


#角色水上漂时buff
ENTER_WATER_BUFF = 24000501

#摆摊
SPACE_TELEPORT_POSITION = ( 215.73, 122.29, 236.14 )			# 传送到凤鸣城的坐标点

#幻兽AI：服务器 = False 客户端 = True
VEHICLEPET_IS_SERVER_OR_CLIENT = True

 #怪物跳跃
MONSTER_JUMP_SPEED	 	= 10.0 		# 怪物跳跃速度

#玩家属性变化写日志时间
ROLE_PROPERTIES_ADDLOG_TIME = 5.0 * 60

#解锁包裹格子物品ID
UnlockGrid_ITEMID = 205010011

# Wind Tick time
BLOW_WIND_TICK_TIME = 0.08

#-------------------------烽火连天-------------
FHLT_SPACE_SCRIPTID				 = "fu_ben_L_FHLT"	# 烽火连天space
FHLT_INTEGRAL_WINNER			 = 2500				# 优先获得2500积分的一方获胜
FHLT_PUNISH_BUFF				 = 24000501			# 惩罚Buff

#-------------------------灵兽圈-------------
LXQ_AIM_SKILLID					 = 140148001		#瞄准模式下技能ID

#-------------------------通天塔---------------------
TTD_JUMP_LAYER_PROBABILITY		 = 15				#通天塔跳层挑战概率15% 


#-------------------------轮回秘境---------------------
LHMJ_HOUSE_PARTICLE = 102932				# 轮回秘境建筑光效
SAVE_TRAP_MORE_TIME	= 20					# 陷阱生命周期低于20秒，不保存
NPC_FORWARD_DISTANCE = 5					# 用于计算洞府建筑偏移位置
DONG_FU_GUARD_TYPE = {
	csdefine.DONG_FU_GUARD_TYPE_DEFAULT : "mDefaultID",
	csdefine.DONG_FU_GUARD_TYPE_ATTACK	: "mAttackID",
	csdefine.DONG_FU_GUARD_TYPE_CONTROL : "mControlID"	}
LHMJ_ENTER_POS = (264.7, 2.7, -406.8)		# 轮回秘境入口
LHMJ_JADE_ITEM_ID = "303020004"				# 玲珑玉令ID
LHMJ_CAVE_TIPS_PARTICLE = "103012_12"		# 洞府建筑tips
DONG_FU_BUILD_MAP_MONSTER = {
	csdefine.LHMJ_BUIILD_LING_QUAN : "20014315",
	csdefine.LHMJ_BUIILD_GONG_FANG : "20014181",
	csdefine.LHMJ_BUIILD_QIAN_KU_DING : "20014182",
}
#------------------------开放练兵场等级---------------
OPEN_TRAIN_SOLDIER_GROUND_LEVEL	 = 30

TRAIN_GROUND_QUEST_NUM = 5					# 练兵场任务随机出任务数量
TRAIN_GROUND_REFRESH_TIME = [11, 16, 20]	# 11、16、20点分别刷新
TRAIN_GROUND_REFRESH_MONEY = 10				# 刷新消耗金钱
TRAIN_GROUND_QUEST_SRC_SCRIPTID = "20013989"# 派遣做 练兵场任务的scriptID
TRAIN_GROUND_QUEST_FIGHT_TIME = 61 			# 练兵任务，战斗时间
TRAIN_GROUND_QUEST_MIN_RATE_NUM = 0.45		# 实力比，成功率最小值
TRAIN_GROUND_QUEST_MAX_RATE_NUM = 1.5		# 实力比，成功率最大值
TRAIN_GROUND_QUEST_MAX_NUM		= 20		# 1天可以接的最大任务数量
TRAIN_GROUND_QUEST_UST_ITEM		= 201010029	# 领取任务消耗 练兵令物品ID
TRAIN_GROUND_QUEST_DOU_BUFF		= 12243102	# 添加双倍经验的buffID
TRAIN_GROUND_QUEST_POiNT_FIVE_BUFF = 12243101# 添加1.5倍经验的buffID

#-------------------------------传承技能---------------------------------------
#残缺空白玉玦的进度上限概率
BROKENJADE_PROGRESS_MAX = {5:1000, 6:1300, 7:1500, 8:1800, 9:2100, 10:2300}
BROKENJADE_PROGRESS = {1:3090, 2:2160, 3:1510, 4:1060, 5:740, 6:520, 7:360, 8:255, 9:180, 9:125}

#-------------------------------掉落宝箱出现时表现效果 ------------------------
DROPBOX_MOVE_SPEED = 500.0					#宝箱出现时动画中飞行速度
DROPBOX_START_SCALE = 0.01					#宝箱初始缩放比例
DROPBOX_END_SCALE = 0.2						#宝箱最终缩放比例
GREEN_DROPBOX_XUANFU_HIGHT = 1.0			#绿色品质道具的宝箱浮空的高度
GREEN_DROPBOX_GET_EFFECTID = "102695_1"		#绿色品质道具获取后玩家身上的光效
DROPBOX_GRAVITY = 980.0						#控制弧度大小
GREEN_DROPBOX_DRAG_ACTION	= "Idle_Free"	#绿色品质宝箱拖曳动作
GREEN_DROPBOX_LEVITATE_ACTION = "Idle_Fight"#绿色品质宝箱浮空时的动作
GREEN_DROPBOX_START_SCALE = 1.0				#宝箱初始缩放比例
GREEN_DROPBOX_END_SCALE = 2.0				#宝箱最终缩放比例


#------------------------------圣阶物品相关内容----------------------------------
SHENGJIE_ITEM_GET_SOUND = "C001653"				#圣阶物品获取后播放的语音
SHENGJIE_ITEM_GET_EFFECTID = "102695_1"			#圣阶物品获取后播放的光效

#-----------------------------帮会宝箱-------------------------------------------
TONG_DROPBOX_OPEN_TIME = 10 * 60 			#帮会宝箱自动开启时间（从宝箱创建开始算）
TONG_DROPBOX_RALLDOM_TIME = 2 * 60			#掷点倒计时
TONG_DROPBOX_AUCTION_TIME = 2 * 60			#竞拍倒计时
TONG_DROPBOX_OPEN_RANGE = 20				#宝箱开启时，多大范围内的玩家有权领取

TONG_SPACE_COPY_XIUWEI_RATE = 0.5			# 帮会副本第二次进入击杀怪物获得1.5倍奖励
TONG_SPACE_COPY_TOTAL_RATE = 1.5			# 帮会副本第二次进入副本结算奖励1.5倍

# 大荒战场 变色模型ID {临时阵营 ：性别： {职业 ：modelID}}
COLOR_SCHEME_MODEL_COLOR = { csdefine.CAMP_DEMON : 
								{ csdefine.MALE : 
									{ csdefine.CLASS_FIGHTER : "SK_M_Long_Body_Red",
									  csdefine.CLASS_SWORDMAN : "SK_M_Sword_Body_Red",
									  csdefine.CLASS_ARCHER : "SK_M_Whip_Body_Red",
									  csdefine.CLASS_MAGE : "SK_M_Fan_Body_Red" },
								 csdefine.FEMALE :
								 	{ csdefine.CLASS_FIGHTER : "SK_F_Long_Body_Red",
									  csdefine.CLASS_SWORDMAN : "SK_F_Sword_Body_Red",
									  csdefine.CLASS_ARCHER : "SK_F_Whip_Body_Red",
									  csdefine.CLASS_MAGE : "SK_F_Fan_Body_Red" }, 
								},
							csdefine.CAMP_TAOSIM : 
								{ csdefine.MALE : 
									{ csdefine.CLASS_FIGHTER : "SK_M_Long_Body_Blue",
									  csdefine.CLASS_SWORDMAN : "SK_M_Sword_Body_Blue",
									  csdefine.CLASS_ARCHER : "SK_M_Whip_Body_Blue",
									  csdefine.CLASS_MAGE : "SK_M_Fan_Body_Blue" },
								 csdefine.FEMALE :
								 	{ csdefine.CLASS_FIGHTER : "SK_F_Long_Body_Blue",
									  csdefine.CLASS_SWORDMAN : "SK_F_Sword_Body_Blue",
									  csdefine.CLASS_ARCHER : "SK_F_Whip_Body_Blue",
									  csdefine.CLASS_MAGE : "SK_F_Fan_Body_Blue" }, 
								},
							}