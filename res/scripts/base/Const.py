# -*- coding: utf-8 -*-
import csdefine
import csconst
import ItemTypeEnum

GLOBAL_BASEDATA_REGISTER_BASEAPP = "GBAE_REGISTER_BASE_APP"

RELATION_UID_SAND_MAX_COUNT			= 100 # 每次给申请玩家关系UID的baseEntity分配的uid个数。

FRIEND_FRIEND_MAX_COUNT		= 200			# 好友数量上限
FRIEND_BLACKLIST_MAX_COUNT	= 100			# 黑名单数量上限
RELATION_FOE_NUM_LIMIT		= 100			# 不友好(仇人)的数量上限
RELATION_LAST_CHAT_LIMIT	= 50			# 最近联系数量上限
RELATION_CATALOG_MAX		= 10			# 分组最大组数

# 关系固定分组
RELATION_FIX_CATALOGS = [ csdefine.RELATION_CATALOG_TYPE_FOE_LIST, 
					csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST,
					csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST,
					csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST]

GROUP_MAX_COUNT 			= 30											# 每个讨论组最多只能拥有30名成员
PLAYER_CAN_JOIN_GROUP_NUM	= 10											# 每个玩家最多加入10个讨论组
GROUP_CAN_USE_TIME			= 30 * 24 *3600 * csconst.TIME_ENLARGE_MULTIPLE	# 讨论组免费使用 30天
GROUP_BLACKLIST_MAX_COUNT	= 50											# 讨论组黑名单最多能添加50位玩家

VPET_SLEEP_TIME				= 5 * 60		# 幻兽休眠时间5分钟

TONG_REQ_JOIN_LIST_MAX 		= 10			# 申请入帮会的最大数量
TONG_MAX_LEVEL				= 5				# 帮会最大等级
TONG_MONEY_TO_CONTRIBUTE	= 1				# 捐献1金获得10帮贡
TONG_MONEY_TO_EXP			= 0.001			# 捐献1金获得10经验
TONG_CREATE_MAX_CAMP_NUM	= 200			# 同一阵营最多能创建200个帮会
TONG_REJOIN_CD_TIME 		= 24 * 3600.0	# 重新加入帮会的CD时间


#帮会职称人数限制
TONG_NUM_LIMIT = { csdefine.TONG_TITLE_1 : 1, csdefine.TONG_TITLE_2 : 2, csdefine.TONG_TITLE_3 : 1, csdefine.TONG_TITLE_4 :4 }

TONG_CREATE_SAFETIME = 7						# 帮会创建安全期时间
TONG_UPGRADE_SAFETIME = 2						# 帮会升级安全期时间
TONG_LEVEL_PROTECTTIME = 4						# 4天保护期，保护期过降级
TONG_DISMISS_PROTECTIME = 30					# 30天保护期，保护期过强制解散帮会
TONG_OFFLINE_DEMISE_LEADER = 2 * 7 * 24 * 3600	# 2周未上线，强制罢免帮主
TONG_RECORD_MAX_NUM = 200						# 帮会记录上限
TONG_ON_LINE_MAX_TIME_REWARD = 10				# 帮会在线奖励最大次数
TONG_DONATE_MONEY_TOTAL	= 10000					# 1万金币

# 阵营活动（灵脉战场）
CAMP_LING_MAI_MATCH_NUM	= 25					# 战场匹配人数
READY_STAGE_TIMER_SECOND= 5						# 5秒自动进入
LMZC_SPACE_SCRIPTID	 = "fu_ben_L_LMZC"			# 灵脉战场space

# 每日签到
SIGN_IN_REWARD_AUGMENT_DAY = 100				# 补签一次，花费100元宝
SIGN_IN_MIN_LEVEL = 10							# 签到最低等级

# 阵营活动（冰雪之战）
CAMP_FROZEN_FIGHT_MATCH_NUM	= 20					# 战场匹配人数
FROZEN_FIGHT_READY_STAGE_TIMER_SECOND= 5			# 5秒自动进入

#帮会争霸 第一场分组
TONG_STARCRAFT_GROUP_MEMBER = 4
#帮会争霸 第一场帮会的通关数
TONG_STARCRAFT_FIRST_PASS_NUMBER = 8
#帮会争霸 第一场最少的通关数
TONG_STARCRAFT_PASS_FIRST_LESS = 5
#帮会争霸 第二场最少报名帮会数
TONG_STARCRAFT_SECOND_SIGN_UP_LESS = 2

#帮会争霸 JIRA-7490 该阵营第一场最少报名的帮会数
TONG_STARCRAFT_FIRST_SIGN_UP_LESS = 5
#帮会争霸 JIRA-7490 该阵营第一场最大报名的帮会数
TONG_STARCRAFT_FIRST_SIGN_UP_MAX = 8

#英雄联盟匹配的最大人数
SPACECOPY_CAMP_YXLM_MATCH_NUMBER		= 5
#上古密阵匹配的最大人数
SPACECOPY_CAMP_SGMZ_MATCH_NUMBER		= 5
#勇闯绝命岛匹配的最大人数
SPACECOPY_CAMP_YCJMD_MATCH_NUMBER		= 25
# 阵营竞技勇闯绝命岛（5人）最大人数
SPACECOPY_CAMP_FIVE_YCJMD_MATCH_NUMBER		= 5

# 排行榜
GAME_RANK_MIN_UPDATE_TIME = 600					# 排行榜最低更新频率
GAME_RANK_MAX_RANKING	  = 100					# 排行榜最大名次

LOGIN_CALCULATE_TIME_INTERVAL			= 180.0		# 秒，登录等待计算等待时间的有效期限

#玩家account entity状态
ACCOUNT_INITIAL_STATE					= 0		# 初始状态
ACCOUNT_WAITTING_STATE					= 1		# 等待状态
ACCOUNT_LOGIN_STATE						= 2		# 正在登录中
ACCOUNT_GAMMING_STATE					= 3		# 游戏中

#帮会阵营战 一个帮会参加的最大人数
TONG_CAMP_WAR_TONG_MAX_JOIN_MEMBER = 20

# 阵营活动（烽火连天）
CAMP_FHLT_MATCH_NUM	= 20					# 战场匹配人数
CAMP_FHLT_READY_STAGE_TIMER_SECOND = 5		# 5秒自动进入
FHLT_SPACE_SCRIPTID = "fu_ben_L_FHLT"		# 烽火连天space

#活动提醒
CROND_NO_REMIND 				= 0		# 活动不提醒
CROND_BEFORE_OPENING_REMIND 	= 1		# 活动开启时提醒
CROND_BEFORE_FIVEMINUTE_REMIND 	= 2		# 活动开启前5分钟提醒
CROND_BEFORE_TENMINUTE_REMIND 	= 3		# 活动开启前10分钟提醒
CROND_BEFORE_HALFHOUR_REMIND 	= 4		# 活动开启前30分钟提醒

# 轮回秘境刷新时间
LHMJ_SHOP_REFLASH_TIME			= 3600	# 1小时刷新
LHMJ_SHOP_REFLASH_NUM			= 10	# 刷新数量
LHMJ_DONG_FU_SHOW_ENTRY			= 10	# 界面显示洞府的条目
LHMJ_CHALLENGE_LEVEL			= 3		# 洞府挑战等级分界线
LHMJ_DEFAULT_REPLY				= 3 * 3600	# 3小时没应战，默认应战
LHMJ_GUARD_REVIVE_TIME			= 48 * 3600	# 守卫死亡，48小时复活
LHMJ_FIRST_STAGE_TIME			= 10 * 60	# 掠夺战\争夺战第一阶段10分钟
LHMJ_SECONED_STAGE_TIME			= 5 * 60	# 掠夺战\争夺战第二阶段5分钟

#帮会争霸参加活动帮会数
BHZB_JOIN_TONG_NUMBER 			= 15


#-------------------帮会掠夺战----------------
#活动参加人数
TONG_PLUNDER_JOIN_MEMBER_NUM = 10
#帮会商店物品比例
TONG_PLUNDER_SHOP_RATIO = 0.5

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

#------------------------------ 宝箱竞拍/掷点 --------------------------------------------
ROLLDOM_COUNTDOWN_TIME = 2 * 60	#宝箱掷点倒计时
AUCTION_COUNTDOWN_TIME = 30		#宝箱第一次竞拍倒计时
AUCTION_BASE_PRICE = 1000		#宝箱竞拍底价

#-------------------帮会争霸宝箱声音 ------------------------------------
#第一层字典的key值为名次，第二层为分配方式（对应csdefine中帮会拾取分配方式）
BHZB_VOICE_DICT = {		
	1	: {
		2	: "C001754",		#冠军 + 掷点分配
		3	: "C001753",		#冠军 + 竞拍分配
		4	: "C001752",		#冠军 + 帮主分配
	},
	2	: {
		2	: "C001757",		#亚军 + 掷点分配
		3	: "C001756",		#亚军 + 竞拍分配
		4	: "C001755",		#亚军 + 帮主分配
	},
	3	: {
		2	: "C001760",		#季军 + 掷点分配
		3	: "C001759",		#季军 + 竞拍分配
		4	: "C001758",		#季军 + 帮主分配
	}
}

BHZB_DROPBOX_OPEN_VOICE = "C001761"				#宝箱开启倒计时


#-------------------日志相关 ------------------------------------
MSG_TPYE_ONLINE_RECORD = 5.0 * 60 #在线数据记录相隔时间