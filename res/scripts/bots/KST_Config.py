# -*- coding: utf-8 -*-


#ai切换概率(需进行哪项测试，请将对应的测试项的值设为100，其他项值设为0)
aiPer = {
	"OldAI"				: 0,				#旧AI
	
	"LoginAI"			: 10,				#玩家登录&喊话
	"TeleportSpaceAI"	: 0,				#玩家传送（地图切换）
	"RoleFightRoleAI"	: 0,				#玩家竞技
	"SpaceAI"			: 10,				#新手村/位面/副本
	"SpaceCampAI"		: 0,				#阵营副本
	"QuestAI"			: 70,				#主线任务
	"ShopAI"			: 10,				#商城	
	
	"PetAI"				: 0,				#宠物
	"QuestTestAI"		: 0,				#测试任务
	"TongAI"			: 0,				#帮会
	"TeamAI"			: 0,				#队伍
	"SkillAI"			: 0,				#技能
	"RandWalkAI"		: 0,				#移动
	"RoleFightMonsterAI": 0,				#战斗
	"StandAI"			: 0,				#站立
	"FollowWalkAI"		: 0,				#跟随移动
}

#注意：如果选择的是“SpaceCampAI”，这里设置是无效的，会在Account.py中强制平均分配阵营
#阵营(0:随机 1:仙道 2:魔道)
camp = 0

#职业(0:随机 1， 2， 3， 4)
profession = 0
#性别(0:随机 1:男, 2:女)
gender = 0

#是否携带宠物开关
pet= False
#是否关闭技能释放
close_skill = False
#默认地图
default_map = ("bigmap_1", "26473 -60183 -1297")


"""
登陆&喊话测试配置 ------------------------------ 
"""
Login_talk_tick = 5		#间隔5个tick，每个tick为60S


"""
传送测试配置  ----------------------------------
"""
teleport_with_item = True	#是否携带物品进行跳转
teleport_tick = 2			#间隔2个tick，每个tick为60S
teleport_map_random = False	#True：各主城+副本间随机切换 False：teleport_maps配置的地图间进行切换
#如果是在下面地图间跳转的话，至少要配置两个地图才能进行跳转
teleport_maps = {
#	 						地图				坐标								   	是否参与测试
"bigmap_1"				: ["bigmap_1", 			"26473 -60183 -1297", 					True],
"L_FightDemo"			: ["L_FightDemo", 		"6407.623047 -6630.79248 199.998657", 	False],
"L_FMC"					: ["L_FMC", 			"23614.0 21573.0 12230.0", 				False],
"fu_ben_JSSLC"			: ["fu_ben_JSSLC", 		"15600.0 39190.0 -90.0", 				False],
"fu_ben_L_BHMY"			: ["fu_ben_L_BHMY", 	"-14400.0 13670.0 1543.437134", 		False],
"fu_ben_L_CBK"			: ["fu_ben_L_CBK", 		"14180.0 27025.0 190.0", 				False],
"fu_ben_L_HKY"			: ["fu_ben_L_HKY", 		"40874.04 -1258.4 -60.9", 				False],
"fu_ben_L_HKY_1"		: ["fu_ben_L_HKY_1", 	"47560.2 -8324.8 1109.8", 				False],
"fu_ben_L_HKY_Boss"		: ["fu_ben_L_HKY_Boss", "-57250.0 90.0 3920.0", 				False],
"fu_ben_L_HLG"			: ["fu_ben_L_HLG", 		"-43629.9 4760.0 260.0", 				False],
"fu_ben_L_HYZY"			: ["fu_ben_L_HYZY", 	"-37466.0 -22980.0 -609.37", 			False],
"fu_ben_L_HYZY_1"		: ["fu_ben_L_HYZY_1", 	"-37466.0 -22980.0 -609.37", 			False],
"fu_ben_L_HZMG"			: ["fu_ben_L_HZMG", 	"-89510.0 7390.0 5691.5", 				False],
"L_JYHD"				: ["L_JYHD", 			"11252.49 13760.15 129.25", 			True],
"L_JYDT"				: ["L_JYDT", 			"46093.0 29674.2 -16539.3", 			False],
"L_JX"					: ["L_JX", 				"13544.8 -362.4 172.0", 				False],
}

"""
玩家战斗测试配置  -------------------------------
"""
rolevsrole_fight_radius = 50	#战斗半径
rolevsrole_fight_skill = 0		#攻击使用的技能 -1：随机使用技能  0：顺序释放技能 其他：使用指定技能
#测试地图
rolevsrole_fight_map = {
#							地图											是否参与测试
"bigmap_1"				: [("bigmap_1", 		"26473 -60183 -1297"),			False],
"L_FMC"					: [("L_FMC", 	"23614.0 21573.0 12230.0"), 			False],
"L_FightDemo"			: [("L_FightDemo", 	"6407.623047 -6630.79248 199.998657"), 	True],
}

"""
新手村/位面/副本测试配置 -------------------------
"""
space_first_belongType = 1	#如果副本属于可单人/组队等情况，优先选择其中一种
space_maps = {
#序号		位面/副本  			  是否参与测试 		
1		: ("fu_ben_L_HKY_Boss",		True),
2		: ("fu_ben_L_HKY",			True),
3		: ("L_YXG",					True),
4		: ("L_FMC",					True),
}

"""
阵营副本测试配置 -------------------------------
"""
spaceCamp_maps = {
#副本			  			 副本AI脚本名字	 是否参与测试 		
"fu_ben_L_YXWZ"	:			("CSpace_YXWZ",		False),		#英雄王座
"fu_ben_L_LMZC" :			("CSpace_LMZC",		False),		#灵脉战场
"fu_ben_JSSLC" 	:			("CSpace_JSSLC",	True),		#晶石狩猎场
}

"""
主线任务测试配置 -------------------------------
"""
startQuestID = 0		#起始任务ID
isLoopQuest = True		#是否循环刷任务
task_done_goto_space_maps = {
#序号		地图  			  	是否参与测试 		
1		: ("L_FMC",					True),
}

"""
任务测试配置 ------------------------------------
"""
#任务ID
loopQuestID = [20101142, 20101007, 20101202, 20101143, 20101114, 20101022, 20101103] 		

"""
技能测试配置  -----------------------------------  
"""
skill_test_space = ("bigmap_1", "26473 -60183 -1297")
skill_use_skill = ""			#测试技能
skill_stand_distance = 5		#站位间隔


"""
移动测试配置  ----------------------------------- 
"""
walk_watch_flag = True	#设置机器人watch
walk_radius = 50		#移动半径
walk_map = ("bigmap_1", "26473 -60183 -1297")
walk_create_team = False
#是否一直随机移动(如需进入地图后，机器人随机分布在一定范围内后站立请设置这里)
walk_loop = True


"""
玩家怪物战斗测试配置  -----------------------------
"""
rolevsmonster_fight_radius = 50		#战斗半径
rolevsmonster_fight_map = ("bigmap_1", "26473 -60183 -1297")
#攻击使用的技能 -1：随机使用技能  0：顺序释放技能(哪个能用用哪个) 其他：使用指定技能
relevsmonster_fight_skill = 0


"""
帮会系统测试配置  -----------------------------
"""
tong_clear = True				#帮会清理标识


"""
机器人站立地图位置(基准)
"""
stand_map = ("bigmap_1", "26473 -60183 -1297")


"""
跟随移动
"""
follow_auto_sync_server = False		#是否自动同步怪物坐标朝向到服务器
follow_sync_frequency	= 5			#手动同步坐标时间间隔
follow_radius = 50					#移动半径
follow_enter_default_map = False	#进入big_map进行测试
follow_map = "fu_ben_bigmap"
