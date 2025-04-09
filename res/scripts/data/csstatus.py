
# -*- coding: utf-8 -*-



# 技能施展状态（1-99）
DEFAULT_STATUS_MESSAGE				= 1		# 没有找到ID={0}的提示信息，确认输入
SKILL_GO_ON							= 2		# 释放成功
SKILL_CAST_ENTITY_ONLY          	= 3		# (SC):无效的目标
SKILL_NOT_EXIST						= 4		# (SC):指定的技能不存在
SKILL_UNKNOWN						= 5		# (SC):你无法执行该操作
SKILL_NOT_READY						= 6		# (SC):技能冷却中
SKILL_IN_DEAD                  		= 7		# (SC):您已经死亡,无法进行该操作
SKILL_CANT_CAST						= 8		# (SC):您现在无法使用技能
SKILL_OUTOF_MP	                	= 9		# (SC):法力值不足
SKILL_MISS_POSITION             	= 10		# (SC):请选择一个施法位置
SKILL_CAST_POSITION_ONLY        	= 11		# (SY,SC):只能对一个位置施放
SKILL_TOO_FAR                   	= 12		# (SC):目标距离过远，请靠近后使用
SKILL_TOO_NEAR                  	= 13		# (SC):距离目标太近
SKILL_MISS_TARGET               	= 14		# (SC):没有找到施法目标
SKILL_NOT_ENEMY_ENTITY          	= 15		# (SC):只能对可攻击敌人施展
SKILL_OUTOF_HP	                	= 16		# (SC):血量不足
SKILL_STATE_CANT_CAST             	= 17		# (SC):当前状态下,无法进行该操作
SKILL_CAST_FAILED        		   	= 18		# (SC):释放失败
SKILL_IS_CASTING					= 19		# (SC):正在施法中，请稍后再试！
SKILL_AI_INTERRUPT					= 20		# (SC):AI中断当前释放技能
SKILL_CAST_SUCCESS					= 23		# (SC):技能[{0}]施展成功！
SKILL_CAST_POS_FAIL					= 24		# (SC):指定位置无效，请重新选择。
SKILL_OUTOF_GANGQI					= 25 		# (SC):罡气值不足
SKILL_SPACE_FORBID					= 26		# 该地图不允许释放该技能
SKILL_OUTOF_ITEM					= 27		# 物品不足
SKILL_TARGET_OUTOF_MP	            = 29		# (SC):目标的法力值不足
SKILL_TARGET_OUTOF_HP	            = 30		# (SC):目标的血量不足
SKILL_TARGET_OUTOF_GANGQI			= 31 		# (SC):目标的罡气值不足
SKILL_TARGET_OUTOF_ITEM				= 32		# 目标的物品不足
SKILL_TARGET_STATE_CANT_CAST        = 33		# (SC):目标在当前状态下,无法进行该操作
SKILL_TARGET_NOT_READY				= 34		# (SC):目标的技能冷却中
SKILL_OUT_RATE_FAIL					= 35		# (SC):未中目标

# 传送（100-119）
CANNOT_FLY_WHILE_FIGHTING				= 100		# (MB):您正在战斗中，无法传送。
CANNOT_FLY_WHILE_DEAD					= 101		# (MB):您处于死亡状态，无法传送。
CANNOT_TRANSPORT_IN_SPACE_COPY			= 102		# (MB):您正在副本中，无法传送。
CANNOT_TRANSPORT_IN_JAIL				= 103		# (MB):在监狱中不能传送。
CANNOT_TRANSPORT_IN_FLY					= 104		# (MB):您正处于飞行中，无法传送。
YOU_HAVE_COME_IN						= 105		# (SY):你已经进入 {0}
YOU_HAVE_COME_IN_COPY					= 106		# (SY,PD):你已经进入 {0}
YOU_HAVE_COME_IN_COPY_1					= 106		# 你已经进入 {0}
YOU_HAVE_COME_IN_COPY_2					= 107		# 你已经进入 {0}
SPACE_ENTER_OR_LEAVE_OK					= 108		# 可以进入/离开
KILLING_VALUE_TO_MUCH					= 109		# 你的杀气值大于0，还需要继续反省！


# GameMgr（120-129）
QUIT_GAME_DIALOG				= 120		# (MB):"你确实要退出游戏吗？"


# 角色选择（130-139）
DELETE_ROLE_DIALOG				= 130		# (MB):"输入错误，删除取消"
ENTERGAME_DIALOG				= 131		# "您还未建立任何角色"


# 位面（140-199）
QUIT_PLANE_PANEL_DIALOG				= 140		# (MB):"返回位面入口会使剧情重置，是否继续？"
QUIT_COPY_PANEL_DIALOG				= 141 		# (MB):"确认返回复活点？"
IS_LEAVE_SPACECOPY					= 142		# (MB):"是否离开副本?（消耗一次副本次数）"


#GM命令提示（200-500）
GM_CANNOT_FIND_TARGET				= 200		#GM命令操作目标ID={0}不存在
GM_CANNOT_FIND_COMMAND				= 201		#GM命令找不到
GM_COMMAND_GRADE_NOT_ENOUGH			= 202		#当前GM命令的执行权限为{0},你的的权限等级为{1},权限不够
GM_FORMAT_TIPS						= 203		#指令格式：{0}
GM_ARGS_SPACE_VALUE_ERROR			= 204		#输入的spaceKey错误，目标地图不存在
GM_COMMAND_SUCCESS					= 205		#操作成功
GM_SCRIPTID_DONT_EXIST 				= 206		#输入的scriptID不存在
GM_ARGS_MUST_INT	 				= 207		#输入的参数必须是整型
GM_ARGS_TYPE_ERROR		 			= 208		#输入的参数类型有误
GM_QUERY_RESULT			 		= 209		#输出查询属性
GM_ATTR_NOT_EXIST		 			= 210		#查询属性不存在
GM_CONFIG_RELOAD_SUCCESS 		= 211		#配置热更新成功！
GM_CONFIG_RELOAD_FAIL	 			= 212		#配置热更新失败！请查看{0}！
GM_GOTO_BUNCHSPACE				= 213		#此副本是副本串子副本，不能用此指令进入
GM_REQUESTID_SIGN_REMOVE			= 214		#任务questID标记已清除
GM_ALL_REQUEST_SIGN_REMOVE		= 215		#所有任务标记已清除
GM_ITEMID_DONT_EXIST 				= 216		#输入的ITEMID不存在
GM_DROP_BOX_FAIL					= 217		#创建掉落箱子失败！
GM_DROP_BOX_ITEM_LIST_NONE		= 218		#物品列表为空，请检查输入参数！
GM_SET_ATTR_SUCCESS				= 219		#设置成功！
GM_SET_ATTR_FAIL						= 220		#设置失败！
GM_SET_ENTITY_ERROR					= 221		#GM指令的设置对象不是玩家！
GM_NO_USE_1							= 222		#闲置1
GM_RELOAD_FILE_FORMAT_ERROR		= 223		#配置热更新失败！配置{0}格式错误！
GM_RELOAD_SUCCEED					= 224		#热更新{0}：{1}成功！
GM_RELOAD_FAILED					= 225		#热更新{0}：{1}失败！
GM_SETMODELSCALE_SUCCEED			= 226 		#设置模型大小成功！
GM_CMMAND_FAILED					= 227		#GM操作失败，请查看服务器报错
GM_ADD_BUFF_SUCCEED				= 228		#GM添加buff{0}成功!
GM_ADD_BUFF_FAILED					= 229		#GM添加buff{0}失败!
GM_REMOVE_BUFF_SUCCEED			= 230 		#GM移除buff{0}成功！
GM_REMOVE_BUFF_FAILED				= 232 		#GM移除buff{0}失败！
GM_QUERY_BUFF						= 231 		#GM查询buff结果{0}
GM_CLONE_NEM_ERR					= 233 		#clone的数量必须小于50！
GM_CLEAR_EQUIPBAG_INFO				= 234		#已清空装备包裹
GM_CLEAR_COMMONBAG_INFO			= 235		#已清空普通包裹
GM_CLEAR_QUESTBAG_INFO				= 236		#已清空任务包裹
GM_CLEAR_SPARBAG_INFO					= 237		#已清空晶核包裹
GM_CLEAR_STORE_INFO					= 238		#已清空仓库
GM_RELOADSCRIPT_SUCCEED			= 239		#热更新脚本{0}成功！
GM_RELOADSCRIPT_FAILED				= 240		#热更新失败，无法查找到{0}脚本！
GM_RELOADENTITY_SUCCEED			= 242		#热更新Entity成功！
GM_CANT_ENTER_TARGET_SPACE			= 241		#目标地图无法传送
GM_MODEL_NUMBER_IS_INVALID          = 243       #模型{0}无效
GM_TARGET_TYPE_CAN_NOT_BE_ROLE		= 244 		#目标不能是玩家
GM_QUERY_RELATION					= 245 		#查询结果：[{0} {1}][{2} {3}]
GM_CANT_FIND_NPCID_POSDATA			= 246       #找不到指定NPCID{0}位置数据
GM_REMOVE_CD_SUCCEED				= 247		#清除CD成功
GM_QUEST_TASK_USE_FAILURE			= 248		#使用任务目标命令失败
GM_QUEST_TASK_USE_SUCCESS			= 249		#使用任务目标命令成功
GM_QUEST_TASK_STAGE_USE_FAILURE		= 250		#使用阶段目标命令失败
GM_QUEST_TASK_STAGE_USE_SUCCESS		= 251		#使用阶段目标命令成功
GM_SHOW_BASEAPP_ROLE				= 252		# {0}中当前人数为{1}人!
GM_ADD_EFFECT_SUCCEED				= 253		#GM添加effect{0}成功!
GM_ADD_EFFECT_FAILED				= 254		#GM添加effect{0}失败!
GM_CHECK_INFO						= 255		#{0}
GM_CLEAR_ACTIVITY_DEGREE 			= 302		#活动次数已清空


# 创建人物时base返回状态（501-512）
ACCOUNT_STATE_NAME_NONE 			= 501		# 角色名不能为空,请至少键入一个字符
ACCOUNT_STATE_NAME_TOOFAR       	= 502		# 角色名字长度不得超过7个汉字或14个英文字母
ACCOUNT_STATE_NAME_EXIST        	= 503		# 该名称已被使用,请换一个名称
ACCOUNT_STATE_ROLE_NOT_EXIST		= 504		# 该角色不存在
ACCOUNT_STATE_ROLE_LIST_NOT_READY   = 505		# 正在加载角色列表,请稍侯
ACCOUNT_STATE_ROLE_ALREADY_LOGIN    = 506		# 该角色已登陆
ACCOUNT_STATE_ID_ALREADY_LOGIN 		= 507		# 该帐号已登陆
ACCOUNT_STATE_CREATE_FULL			= 508		# 最多只能创建 5 个角色
ACCOUNT_STATE_SERVER_BUSY			= 509		# 服务器忙,请稍后再试
ACCOUNT_STATE_SERVER_FREQUENTLY 	= 510		# 操作过于频繁，请稍后再试


# 对话（513-548）
TALK_CANNOT_FIND_DIALOG				= 513		# 该NPC未配置对话内容
QUEST_CANNOT_ABANDON				= 514		# 该任务不能放弃
LEVEL_CANNOT_SATISFY				= 515		# 等级不足，至少{0}级才能进行此操作
TALK_FORBID_DEAD_STATE				= 516		# 您已经死亡，NPC不敢和你说话！
TALK_FORBID_PEAD_STATE				= 517		# 当前处于传送保护中，无法与其对话！
TALK_FORBID_BY_STATE				= 518		# 您目前不能和NPC对话！
TALK_FORBID_TOO_NEAR				= 519		# 您离得太近了。
TALK_FORBID_TOO_FAR					= 520		# 您离得太远了。
TALK_HAS_ACCEPT_LOOP_QUEST			= 522		# 您已经接取环任务
TALK_SET_REVIVE_POS 				= 523       # 你已成功绑定复活点：{0}
TALK_HAS_FINISH_LOOP_QUEST			= 524		# 已完成3轮环任务，无法再次领取。
TALK_FORBID_CANT_NOW				= 525 		# 您目前无法进行这个操作
TALK_GET_REWARD_ITEM				= 526		# 已领取奖励，不能重复领取！

# 技能学习（549-591）
NEW_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH	= 549	# 您的潜能点不足，无法学习该技能
CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH = 550	# 您的潜能点不足，无法升级该技能
CAN_NOT_LEARN_SKILL_AS_LEVEL_NOT_ENOUGH 	= 551	# 您的等级不够，无法学习该技能
ADD_SKILL_SUCESS							= 552	# 你成功学习了该技能
ADD_SKILL_FAIL_AS_HAS_LEAR					= 553	# 你已学习了该技能
ADD_SKILL_NOT_SAVE							= 554	# 技能加点未保存，是否保存
IS_CONSUME_POTENTIAL_UPGRADE_SKILL			= 555	# 确定消耗{0}点潜能升级{1}？
CAN_NOT_LEVEL_UPGRADE_SKILL					= 556	# 等级过低，无法升级该技能
CAN_NOT_MATERIAL_UPGRADE_SKILL				= 557	# 技能书不足，无法升级该技能
CAN_NOT_MONEY_UPGRADE_SKILL					= 558	# 您的金钱不足，无法升级该技能
LEARN_SKILL_SUCESS							= 5925	# 你学习了技能{}

# 物品使用（592-）
ITEM_USE_GO_ON_MSG					= 592			# 物品能正常使用
ITEM_NOT_EXIST_MSG					= 593			# 物品不存在
BAG_NOT_ENOUGHSPACE					= 594			# 背包没有空闲的位置
ITEM_ISBUSY							= 595			# 物品正处于操作中，请稍候再试
ITEM_USE_LV_LESS_MSG				= 596			# 你的等级太低，不能使用此物品
USE_ITEM_FORBID_BY_STATE			= 597			# 您暂时不能使用该物品！
MONEY_NOT_ENOUGH					= 598			# 您的金币不够！
ITEM_USING_NOW						= 599			# 您正在使用其它物品。
ITEM_CANNOT_USED					= 600			# 您不能使用该道具。
NOT_ENOUGH_MONEY_UNLOCK_GRID		= 601			# 金钱不足，无法扩展包裹
UNLOCK_GRID_COST					= 602			# 是否花费{0}金钱扩展包裹？
ITEM_USE_CLASS_NOTMATCH				= 603			# 你的职业不适合使用此物品
ITEMBAG_LOCKED						= 604			# 背包锁了，暂不能卸载装备
ITEM_DESTROY						= 605			# 确定将{0}摧毁吗？它将无法恢复！
ITEM_LIMITDESTORY					= 606			# 此物品不允许销毁
ITEM_INCD							= 607			# 此物品正在CD中，请稍候
ITEM_CANSELL						= 608			# 此物品不能被销售
ITEM_SWAPITEM_TIPS					= 609			# 该操作将会使道具变为绑定道具，是否继续？
ITEM_SPACE_LESS						= 610			# 背包空间不足
ITEM_CAN_NOT_STORE					= 611			# 该物品不能被放入仓库
UNLOCK_GRID_SUCCESS					= 612 			# 包裹扩展成功
KITBAG_CAN_NOT_FIND_ITEM			= 613			# 背包中没有此物品
ITEM_USE_AMOUNT_LIMIT				= 614			# 该物品已达到使用限量
ITEM_USE_NUMBER_LIMIT				= 615			# 您的使用次数不够
ITEM_USE_HARDINESS_ZERO				= 616			#该装备耐久度为0，无法使用
ITEM_UPPER_NOT_CARRIED				= 617			#你的{0}已达上限，无法携带更多的{0}
ITEM_WEAR_EQUIP_PART_ERROR			= 618			#请放入正确的装备部位
ITEM_WEAR_ISNOT_EQUIP				= 619			#请放入装备
ITEM_IS_TRADING						= 620			#交易过程中，不能使用物品
ITEM_IS_MOUNT_NOT_USE				= 621			#在骑乘状态下，不能使用该物品
ITEM_GO_ON							= 622			#可以添加该物品
ITEM_IS_REACH_MAX_TAKE_LIMIT		= 623			#你携带该物品的数量已上限
UNLOCK_MULTI_GRID_COST				= 624			# 是否花费{0}扩展{1}个格子？
ITEM_TARGET_SPACE_LESS				= 625			# 对方背包已满！
UNLOCK_GRID_ITEM_MONEY_COST			= 627			# 是否花费{0}金钱{1}乾坤囊扩展{2}个格子
NOT_ITEM_UNLOCK_GRID                = 628			# 乾坤囊不足，无法扩展包裹 
ITEM_OVER_TIME						= 629			# 物品已经过期！
ITEM_USE_JJLV_LESS_MSG              = 631           # 您的境界等级太低，不能使用此物品！
UNLOCK_GRID_OR_STORE_SUCCESS		= 5580			# 您的{0}第几个{1}栏位已解锁

# 副本相关提示（769-）
SPACE_CLOSE_NOTIFY					= 769		# 副本{0}秒后关闭！
SPACE_TELEPORT_ON_LEAVE_TEAM		= 770		# 您已离开队伍，{0}秒后传送出副本。
SPACE_ENTER_NOT_CAPTAIN				= 771		# 我只接受队长的请求。
SPACE_ENTER_LEVEL_LACK				= 772		# 等级不够，无法进入。
SPACE_ENTER_EXCEED_JOIN_DEGREE		= 773		# 今天进入次数已用完，请明天再来。
SPACE_ENTER_MEM_EXCEED_RANGE		= 774		# 队伍中有人距离过远，无法进入。
SPACE_ENTER_MEM_LEVEL_LACK			= 775		# 队伍中有人等级不够，无法进入。
SPACE_ENTER_MEM_EXCEED_JOIN_DEGREE	= 776		# 队伍中有人进入次数已用完，无法进入。
SPACE_EVENT_ADD_ITEM 				= 777		# 玩家[{0}]已成功找到{1}！
SPACE_SUCCESS_TELEPORT				= 778		# 副本通关成功，副本将在{0}秒后关闭。
SPACE_FAILUER_TELEPORT				= 779		# 副本通关失败，副本将在{0}秒后关闭。
SPACE_LOOPQUEST_TASK_END 			= 780		# 任务{0}秒后结束
SPACE__NOT_QUEST_CONDITION			= 790		# 任务条件不满足
SPACE_PLANE_CLOSE_NOTIFY			= 791		# 剧情将在{0}秒后结束，请尽快完成剧情内容。
SPACE_QUEST_END_NOTIFY				= 792		# 剧情限时剩余{0}秒
SPACE_CLOSE_NOTIFY_MINS 			= 793 		# @F{fc=c3}副本剩余{0}分钟
SPACE_ENTER_MEM_NUM_MANY			= 4961		# 此副本为{0}人副本，您的队伍人数超过{1}人，无法进入。

# 装备系统（1025-1099）
EQUIP_INTENSIFY_INPUT_EQUIP			= 1025		# 装备回火之后除了锁定属性会保留，其他属性都会消失，是否继续？
EQUIP_INTENSIFY_NEED_LEVEL			= 1026		# 大于20级的装备才能强化
EQUIP_INTENSIFY_NO_SUPPORT			= 1027		# 该装备无法强化
EQUIP_INTENSIFY_MAX_LEVEL			= 1028		# 该装备已强化至最高等级
EQUIP_INTENSIFY_AMATIRAL_IS_WRONG	= 1029		# 强化附加材料错误
EQUIP_INTENSIFY_NOT_ENOUGH_MONEY	= 1030		# 强化所需金钱不足
EQUIP_INTENSIFY_SUCCEED				= 1031		# 装备强化成功
EQUIP_BACKFIRE_INPUT_EQUIP			= 1032		# 请放入需要回火的装备
EQUIP_BACKFIRE_NEED_LEVEL			= 1033		# 未强化的装备不能回火
EQUIP_BACKFIRE_NOT_ENOUGH_MONEY		= 1034		# 回火所需金钱不足
EQUIP_BACKFIRE_SUCCEED				= 1035		# 装备回火成功
EQUIP_INTENSIFY_SAVE_INPUT_EQUIP	= 1036		# 请放入需要备份的装备
EQUIP_INTENSIFY_SAVE_NEED_LEVEL		= 1037		# 装备未强化到最高级，无法备份
EQUIP_INTENSIFY_SAVE_NOT_ENOUGH_MONEY= 1038		# 金钱不足，无法备份
EQUIP_INTENSIFY_SAVE_SUCCEED		= 1039		# 装备备份成功
EQUIP_INTENSIFY_RESTORE_INPUT_EQUIP	= 1040		# 装备未备份过，无法还原
EQUIP_INTENSIFY_RESTORE_EQUIP_WRONG	= 1041		# 备份有误，请选择正确的备份属性进行还原
EQUIP_INTENSIFY_RESTORE_NOT_ENOUGH_MONEY= 1042	# 金钱不足，无法还原
EQUIP_INTENSIFY_RESTORE_SUCCEED		= 1043		# 装备还原成功
EQUIP_FORBID_WIELD_BY_STATE			= 1044		# 当前状态不允许进行该操作
EQUIP_INTENSIFY_MONEY_NOT_ENOUGH	= 1045		# 您的金钱不足，无法继续强化
EQUIP_INTENSIFY_XUANJING_NOT_ENOUGH	= 1046		# 您的材料不足，无法继续强化
EQUIP_INTENSIFY_ATTACHMATERIAL_NOT_ENOUGH = 1047# 您的附加材料不足，无法继续强化
EQUIP_BACK_FU_NOT_ENOUGH			= 1048		# 您的材料不足，无法回火
EQUIP_BACK_MONEY_NOT_ENOUGH			= 1049		# 您的金钱不足，无法回火
EQUIP_SAVE_MATERIAL_NOT_ENOUGH		= 1050		# 您的材料不足，无法备份
EQUIP_INTENSIFY_SAVE_NOT_ENOUGH		= 1051		# 你的仙石不足，无法开启新备份栏
EQUIP_SHUFFLE_QUALITY_BLUE			= 1052		# 蓝色品质以上装备才能洗练
EQUIP_SHUFFLE_NEED_LEVEL			= 1053		# 大于30级的装备才能洗练
EQUIP_RECAST_QUALITY_BLUE			= 1054		# 蓝色品质以上装备才能重铸
EQUIP_RECAST_NEED_LEVEL				= 1055		# 大于30级的装备才能重铸
EQUIP_BIOGRAPHY_NO_SAMPLE_PART		= 1056		# 相同部位的装备才能传星
EQUIP_BIOGRAPHY_NO_SAMPLE_QUALITY	= 1057		# 相同品质的装备才能传星
EQUIP_BIOGRAPHY_LEVEL_NOT_MATCH		= 1058		# 传星装备等级不匹配无法传星
EQUIP_SLOT_IS_NULL					= 1059		# 您还未放入装备，无法{0}
EQUIP_SHUFFLE_PANEL_IS_NOT_CLOSE 	= 1060		# 关闭面板后，将删除洗练后的属性，是否关闭
EQUIP_SHUFFLE_REPLACE_STONE_BY_XIANSHI	= 1061	# 洗练石不足，是否用仙石代替
EQUIP_SHUFFLE_REPLACE_XUEFU_BY_XIANSHI	= 1062	# 血符不足，是否用仙石代替
EQUIP_SHUFFLE_XUEFU_NOT_ENOUGH			= 1063	# 您的血符不足，无法洗练
EQUIP_SHUFFLE_STONE_NOT_ENOUGH			= 1064	# 您的洗练石不足，无法洗练
NOT_ENOUGH_XIANSHI						= 1065	# 仙石不足，是否充值
EQUIP_COMPOSE_USE_XIANSHI				= 1066	# 金钱不足，是否使用{0}个仙石代替？
EQUIP_RECAST_REPLACE_BAOZHU_BY_XIANSHI	= 1067	# 重铸宝珠不足，是否使用仙石代替
EQUIP_RECAST_REPLACE_BAOHUFU_BY_XIANSHI	= 1068	# 重铸保护符不足，是否使用仙石代替
EQUIP_RECAST_BAOZHU_NOT_ENOUGH			= 1069	# 您的重铸宝珠不足，无法重铸
EQUIP_RECAST_FU_NOT_ENOUGH				= 1070	# 您的重铸保护符不足，无法重铸
EQUIP_BIOGRAPHY_NOT_SELECT_STAR_LEVEL	= 1071	# 您还未选择需要传星的强化星级，无法传星
EQUIP_BIOGRAPHY_OLD_SLOT_IS_NULL		= 1072	# 您还未放入需要传星的旧装备，无法传星
EQUIP_BIOGRAPHY_NEW_SLOT_IS_NULL		= 1073	# 您还未放入需要传星的新装备，无法传星
EQUIP_BIOGRAPHY_NOT_ENOUGH_MATERIAL		= 1074	# 您的传星材料不足，无法传星
EQUIP_BUILD_NOT_ENOUGH_MATERIAL			= 1075	# 装备打造的材料不足，无法打造装备
EQUIP_INTENSIFY_BACKUP_SLOT_OPEN_CONSUME= 1076	#开放第{0}个强化备份栏目消耗:{1}
EQUIP_INTENSIFY_OPEN_SLOT__MONEY_NOT_ENOUGH = 5568	#金钱不足，无法开启栏位
EQUIP_BACKUP_CONFIRM_REPLACE_PROPERTY	= 1077	# 当前装备已备份，请替换原备份属性
EQUIP_BACKUP_IS_NOT_REPLACE_PROPERTY	= 1078	# 是否确认替换当前属性，替换后原属性将消失
EQUIP_RESTORE_MATERIAL_NOT_ENOUGH		= 1079	# 您的材料不足，无法还原
EQUIP_IS_NOT_CONFIRM_RESTORE			= 1080	# 是否确认还原，还原后备份属性将消失
EQUIP_SHUFFLE_BIND_CONFIRM        	    = 1083  #洗练之后装备将变为@F{fc=c43}绑定@D，是否洗练？
EQUIP_IS_NOT_XIAN_SHI					= 1085	# 您的仙石不足，无法继续强化！
EQUIP_BIOGRAPHY_HAS_INTENSIFY_SAVED     = 1086  #装备强化属性已备份，无法传星
EQUIP_COMPOSE_PRINT_HAS_LEARNED         = 1087  #已学会打造{0}
EQUIP_BIOGRAPHY_BIND_CONFIRM            = 1089  #传星之后的新装备将变为@F{fc=c43}绑定@D，是否传星？
EQUIP_INTENSIFY_BIND_CONFIRM            = 1090  #强化之后，装备将变为@F{fc=c43}绑定@D，是否强化？
EQUIP_RECAST_BIND_CONFIRM               = 1091  #装备重铸之后，装备将变为@F{fc=c43}绑定@D，是否重铸？
EQUIP_BIOGRAPHY_NOT_ENOUGH_MONEY        = 1094  #您的金钱不足，无法传星
EQUIP_INTENSIFY_QUALITY_BLUE			= 5449	# 蓝色品质以上装备才能强化

# 好友系统（1100-1149）
RELATION_MSG_FRIEND_LIST_FULL			= 1100		# 您的好友列表已满。
RELATION_MSG_TARGET_FRIEND_LIST_FULL	= 1101		# [{0}]的好友列表已满。
RELATION_MSG_CANOT_MAKE_FRIEND_YOURSELF	= 1102		# 您不能添加自己为好友！
RELATION_MSG_REPEAT_MAKE_FRIEND			= 1103		# [{0}]已经存在于列表中！
RELATION_MSG_FRIEND_TARGET_REMOVE		= 1104		# [{0}]将您从好友中删除。
RELATION_MSG_IN_BLACK_CANOT_MAKE_FRI	= 1105		# [{0}]在黑名单中，不能添加为好友！
RELATION_MSG_PLAYER_IS_OFFLINE			= 1106		# 对方不存在或目前不在线，不能添加！
RELATION_MSG_REFUSE_INVITATION			= 1107		# 对方拒绝了您的邀请。
RELATION_MSG_I_REFUSE_OHTERS_INVITE     = 5581      # 您拒绝了[{0}]的好友申请
RELATION_MSG_CATALOG_IS_LIMIT			= 1108		# 好友分组已达上限！
RELATION_MSG_REMOVE_FRIEND				= 1109		# 确定要删除好友[{0}]吗？
RELATION_MSG_BLACK_LIST_FULL			= 1110		# 您的黑名单已满！
RELATION_MSG_CANOT_MAKE_BLACK_YOURSELF	= 1111		# 您不能添加自己到黑名单！
RELATION_MSG_NOT_FRIEND_LIST_FULL		= 1112		# 您的不友好名单已满！
RELATION_MSG_CANOT_MAKE_NFRIEND_YOURSELF= 1113		# 您不能添加自己为不友好目标。
RELATION_MSG_GROUP_IS_LIMIT				= 1114		# 可加入的讨论组已达上限！
RELATION_MSG_GROUP_NEM_IS_LIMIT			= 1115		# 讨论组人数已达上限！
RELATION_MSG_CANOT_JOIN_GROUP			= 1116		# 无法加入该组。
RELATION_MSG_GROUP_PASSWORD_ERR			= 1117		# 密码错误。
RELATION_MSG_IN_BLACK_CANOT_JOIN_GROUP	= 1118		# [{0}]在黑名单中，无法加入讨论群！
RELATION_MSG_GROUP_BLACK_IS_FULL		= 1119		# 该组频道黑名单已满，无法继续添加。
RELATION_MSG_TARGET_LEAVE_GROUP			= 1120		# [{0}]离开了[{1}]。
RELATION_MSG_LEAVE_GROUP				= 1121		# 你离开了[{0}]。
RELATION_MSG_LEAVE_GROUP_PASSIVE		= 1122		# 你被请离了[{0}]。
RELATION_MSG_PLAYER_IN_GROUP_AREADY		= 1123		# [{0}]已在讨论组中。
RELATION_MSG_PLAYER_GROUP_IS_LIMIT		= 1124		# 你最多能加入10个讨论组。
RELATION_MSG_GROUP_BLACK_REPEAT			= 1125		# 请勿重复添加。
RELATION_MSG_GROUP_JOIN_FREEDOM			= 1126		# 该组设置了不允许任何人申请加入。
RELATION_MSG_GROUP_TIME_NOT_ENOUGH		= 1127		# 讨论群有效使用时期已过，请先延期使用！
RELATION_MSG_MAKE_FRIEND_SUCESS			= 1128		# 添加好友成功！
RELATION_MSG_REMOVE_FRIEND_SUCESS		= 1129		# 删除好友成功！
RELATION_MSG_MAKE_BLACK_SUCESS			= 1130		# 黑名单添加成功！
RELATION_MSG_MAKE_UFRIEND_SUCESS		= 1131		# 成功将[{0}]添加至不友好列表！
RELATION_MSG_IN_BLACKLIST				= 1132		# [{0}]已经在您的黑名单中了！
RELATION_MSG_REQUEST_ADD_FRIEND			= 1133		# [{0}]添加你为好友，是否同意？
RELATION_MSG_REQUEST_ADD_GROUP			= 1134		# [{0}]邀请你进入[ {1} ]讨论组，是否同意？
RELATION_MSG_ADDTIME_NOT_ENOUGH_MONEY	= 1139		# 黄金不足。
RELATION_MSG_CREATE_GROUP				= 1140		# 成功创建[{0}]
RELATION_MSG_ENTER_GROUP				= 1141		# [{0}]加入[{1}]
RELATION_MSG_GROUP_ALREADY_DISBAND		= 1142		# [{0}]已解散。
RELATION_MSG_SEND_MSG_AS_PALYER_OFFLINE	= 1143		# 该玩家已下线，无法进行聊天。
RELATION_MSG_FRIEND_ONLINE				= 1144		# 你的好友{0}，已上线。
RELATION_MSG_FOD_ONLINE					= 1145		# 你的不友好{0}，已上线。
RELATION_MSG_IN_MY_BLACK_LIST			= 1146		# 该玩家在黑名单中，无法聊天
RELATION_MSG_IN_OTHER_BLACK_LIST		= 1147		# 你被拉入黑名单中，无法聊天
RELATION_MSG_CAN_REC_MSG				= 1148		# 已在{0}的黑名单中，对方无法接受您的信息

# 行为状态限制（1150-1199）
CHAT_MSG_FORBID_BY_STATE				= 1150		# 该状态下无法进行聊天
TELEPORT_PROTECT_STATE					= 1151 		# 当前处于传送保护中，无法使用技能/道具，移动可取消保护
RELATION_MSG_ADD_FRIEND_AS_FOE			= 1152		# {0}存在敌人列表中，添加好友后将解除不友好关系，是否确定？ 
RELATION_MSG_ADD_FRIEND_AS_BLACK_LIST	= 1153		# {0}存在黑名单列表中，添加好友后将解除黑名单关系，是否确定？ 
RELATION_MSG_ADD_FRIEND_IN_BLACK_LIST	= 1154		# 您已被{0}拉入黑名单，无法向对方发起添加好友请求。
RELATION_MSG_FORBID_TRADE_BLACK_LIST	= 1155		# 您已被{0}拉入黑名单，无法向对方发起交易请求。
RELATION_MSG_FORBID_JOIN_TEAM_BLACK_LIST	= 1156		# 您已被{0}拉入黑名单，无法向对方发起组队请求。
RELATION_MSG_FORBID_INVITE_JOIN_TONG_BLACK_LIST	= 1157		# 您已被{0}拉入黑名单，无法邀请对方加入帮会。

# 潜能（1200-1219）
ACCOUNT_CANT_GAIN_POTENTIAL				= 1200		# 您的潜能已经达到上限！
ACCOUNT_STATE_GAIN_POTENTIAL			= 1201		# 您获得 {0} 点潜能
ACCOUNT_STATE_SUB_POTENTIAL				= 1202		# 您消耗 {0} 点潜能
ACCOUNT_GET_BARRACKS_EXP 				= 1203		# 获得养兵经验
ACCOUNT_LOSE_BARRACKS_EXP 				= 1204		# 失去养兵经验

ADD_EXPLOIT_SUCCESS 					= 1206		# 获得军功{0}
EXPLOIT_IS_MAX_FIRST_TIME				= 1207		# 获得军功 0.（已达到每日击杀军功上限：600）
EXPLOIT_IS_MAX							= 1208		# 获得军功 0.


# 修为（1220-1229）
ACCOUNT_STATE_GAIN_XIUWEI			= 1220		# 您获得 {0} 点修为
ACCOUNT_STATE_CAN_NOT_GAIN_XIUWEI	= 5566		# 您的境界已提升至当前等级限制下最高等级，无法获得修为！

# 金钱（1230-1239）
ACCOUNT_CANT_GAIN_MONEY				= 1230		# 您的金钱携带数量已达上限
ACCOUNT_STATE_GAIN_MONEY			= 1231		#您获得 {0} 个铜板
ACCOUNT_STATE_LOSE_MONEY			= 1232		#您失去 {0} 个铜板
ACCOUNT_CANT_GAIN_BIND_MONEY        = 1233      # 您的绑定金钱携带数量已达上限
ACCOUNT_STATE_GAIN_BIND_MONEY       = 1234      # 您获得绑定金钱{0}
ACCOUNT_STATE_LOSE_BIND_MONEY       = 1235      # 您失去绑定金钱{0}

# 经验（1240）
ACCOUNT_STATE_GAIN_EXP				= 1240		# 您获得经验:{0}

# 等级
ACCOUNT_CHANGE_LEVEL					= 1241		# 您已达到 {0} 级

# 称号
ACCOUNT_CHANGE_TITLE					= 1242		# 您已经装备了该称号，无法替换

#脱离卡死功能
DISCONNECT_DEATH_TO_DEAD				= 1243		# 您已死亡，无法使用此功能
DISCONNECT_DEATH_TO_WAIT				= 1244		# 还需要10分钟后才能再次使用脱离卡死功能

# 元宝
ACCOUNT_ADD_XIAN_SHI					= 1250		# 您获得{0}仙石
ACCOUNT_DEL_XIAN_SHI					= 1251		# 您失去{0}仙石
ACCOUNT_ADD_LING_SHI					= 1252		# 您获得{0}灵石
ACCOUNT_DEL_LING_SHI					= 1253		# 您失去{0}灵石
ACCOUNT_ADD_XUAN_SHI					= 1254		# 您获得{0}玄石
ACCOUNT_DEL_XUAN_SHI					= 1255		# 您失去{0}玄石

# NPC商店（1300-1399）
NPCSHOP_SHOP_AMOUNT_ERROR				= 1300		# 物品数量不足
NPCSHOP_ROLE_MONEY_ERROR				= 1301		# 玩家金币不足
NPCSHOP_ROLE_BUY_SUCCESS				= 1302		# 购买成功
NPCSHOP_SELL_MONEY_MAX					= 1303		# 金币到达上限
NPCSHOP_SHOP_AMOUNTLIMIT				= 1304		# 您无法再拥有更多的该道具
NPCSHOP_SHOP_BUYLIMIT					= 1305  	# 您无法再购买更多的该道具
NPCSHOP_SHOP_NOT_REPAIR					= 1306		# 该物品不需要修理。
NPCSHOP_SHOP_NOT_REPAIR_STORE_EQUIP		= 1307 		# 不能修理仓库中的装备。
NPCSHOP_SHOP_REPAIR_FAILURE				= 1308		# 您的金钱不足，无法对装备进行修理
NPCSHOP_SHOP_REPAIR_SUCCESS				= 1309 		# 修理成功：本次修理共花费 {0}
NPCSHOP_SHOP_REPAIR_APART_SUCCESS		= 1310		# 本次修理共花费 {0}。部分装备因金钱不足，无法修理
NPCSHOP_SHOP_RETURN_ITEM_QUALITY_LIMIT  = 1311		# 粉色品质及以上的装备才拥有退货功能
NPCSHOP_SHOP_RETURN_ITEM_TIME_LIMIT		= 1312		# 已超过退货时间
NPCSHOP_SHOP_ITEM_RETURN_LIMIT			= 1313 		# 物品不能出售
NPCSHOP_ROLE_DEAD						= 1314		# 您已经死亡
NPCSHOP_BAG_ENOUGH						= 1315		# 背包已满
NPCSHOP_SELL_SUCCESS					= 1316		# 出售成功
NPCSHOP_SHOP_REPAIR_COST				= 1317		# 本次装备修理花费：{0}，是否确定修理？
NPCSHOP_SHOP_NOT_ITEM_REPAIR			= 1318		# 当前没有需要修理的装备
NPCSHOP_CANNOT_MULTI_BUY				= 1319		# 该商品不支持批量购买
NPCSHOP_CANNOT_BUY_LIMIT				= 1320		# 您无法再购买更多的该道具
NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY    = 1321      #您的绑定金钱不足以购买道具，是否使用{0}代付？
NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY   = 1322      #您的绑定金钱不足以支付本次费用，是否使用{0}代付？

# 玩家交易（1400-1500）
PLAYERTRADE_REQUEST_TRADE				= 1400		# 玩家{0}请求与您交易
PLAYERTRADE_TRADE_FAIL					= 1401 		# 交易失败
PLAYERTRADE_CANCEL_REQUEST_TRADE		= 1402		# 你拒绝了[{0}]的交易申请。
PLAYERTRADE_ANTHOR_CANCEL_REQUERT_TRADE	= 1403		# [{0}]拒绝了您的交易申请。
PLAYERTRADE_TRADE_SUCCESS				= 1404		# 交易成功
PLAYERTRADE_TRADE_OVER_TIME				= 1405		# 交易申请超时
PLAYERTRADE_CANCEL_TRADE  				= 1406		# 你取消了交易。
PLAYERTRADE_ANTHOR_CANCEL_TRADE 		= 1407		# 对方取消了交易。
PLAYERTRADE_MONEY_CANT_GAIN 			= 1408		# 你的金钱携带数量已达上限，交易失败
PLAYERTRADE_ANTHOR_MONEY_CANT_GAIN 		= 1409		# 对方金钱携带数量已达上限，交易失败
PLAYERTRADE_KITBAG_NOT_ENOUGH			= 1410		# 你的背包不足，交易失败
PLAYERTRADE_ANTHOR_KITBAG_NOT_ENOUGH	= 1411		# 对方的背包不足，交易失败
PLAYERTRADE_ITEM_ISBIND					= 1412		# 该物品已绑定,无法交易
PLAYERTRADE_ANTHOR_TRADE_OVER_TIME		= 1413		# [{0}]发起的交易申请已超时。
PLAYERTRADE_REQUEST_REFUSE				= 1414		# 玩家拒绝与您交易
PLAYERTRADE_IS_TRADEING					= 1415		# 正在交易中！
PLAYERTRADE_IS_FARAWAY					= 1416		# 超出交易范围，交易自动取消
PLAYERTRADE_IS_BUSYNESS					= 1418		# 对方正忙！
PLAYERTRADE_CANT_THE_UI 				= 1420 		# 该界面下，无法进行交易
PLAYERTRADE_NOT_OPEN_UI 				= 1421 		# 交易状态下，无法打开该界面


#背包（1501-1599）
CIB_MSG_GAIN_ITEMS                       = 1501		# 您获得 {0}
CIB_MSG_UNLOCK_LOGIN					 = 1502		# 上线2分钟内不允许解锁背包
CIB_MSG_UNLOCK_WRONGPW					 = 1503		# 您输入的旧密码有误,无法更新密码
CIB_MSG_RELIEVE_RESET_KBPW				 = 1504		# 您已经成功解除重置密码
CIB_MSG_IN_RESET_KBPW					 = 1505		# 已经在重置密码过程中，请勿重复重置
CIB_MSG_RESET_KBPW_SUCCESS				 = 1506		# 背包密码已成功清除
CIB_MSG_RESET_KBPW_LEFTTIME				 = 1507		# 您正在重置密码，{0}天{1}时{2}分{3}秒后，密码将被重置
CIB_MSG_KBPW_NOT_SAME					 = 1508		# 两次输入的密码不一致
CIB_MSG_KBPW_LEN_TOO_LONG				 = 1509		# 您输入的密码太长，请重新输入
CIB_MSG_REQUEST_RESET_KBPW				 = 1510		# 你申请重置密码，密码在7天后会自动清除。
CIB_MSG_RESET_KBPW_CANCEL				 = 1511		# 重置密码申请已被取消
CIB_MSG_FULL							 = 1512		# 背包已满！
CIB_MSG_KBPW_WRONG				 = 1513		# 您输入的密码有误，请重新输入！
CIB_MSG_ENTER_NEW_KBPW					 = 1514		# 请输入新密码
CIB_MSG_KBPW_CONTAIN_FORBIDDEN_CHAR		 = 1515		# 您输入的密码含有非法字符，请重新输入
CIB_MSG_CAN_REMOVE_ITEM_AS_USING		 = 1516		# 物品正在使用，无法丢弃！
CIB_MSG_SPLIT_COUNT_IS_ONE				 = 1517		# 拆分目标的数量必须多于1个
CIB_MSG_ITEM_LOST 						 = 1518		# 您失去了{0}
CIB_MSG_ITEM_LOST_AMOUNT 				 = 1519		# 您失去了{0}个{1}
CIB_MSG_KITBAG_LOCKED					 = 1520		# 包裹已处于锁定状态,无法对其进行操作,请先解锁。
CIB_MSG_CANNOT_SPLIT_ITEM				 = 1521		# 无法对任务、晶核类道具进行拆分。
CIB_MSG_REFIX_PASSWORLD					 = 1522		# 安全锁密码已修改
CIB_MSG_IS_STACK_LIMITTIME_ITEM			 = 1523		# 该您将要堆叠的道具是限时道具，堆叠将向下取最少时限，是否确认？

#仓库（1600-1699）
STORE_MSG_LIMIT_MONEY					= 1600		# 仓库可存放金钱已达上限
STORE_MSG_FULL							= 1601		# 仓库已满！
STORE_NO_STOREMONEY						= 1602		# 无法提取更多的金钱
STORE_NO_ENOUGHMONEY					= 1603		# 您的金钱不足
STORE_NO_QUEST_ITEM						= 1604		# 任务道具，无法存入仓库
STORE_CRYSTAL_ITEM_TO_CRYSTAL_BAG		= 1605		# 晶核背包，只能存放晶核物品！
STORE_NORMAL_ITEM_TO_NORMAL_BAG			= 1606		# 道具背包，只能存放道具物品！
STORE_QUESAT_ITEM_TO_QUEST_BAG			= 1607		# 任务背包，只能存放任务物品！
STORE_ERROR								= 1608		# 无法操作！
STORE_MONEY								= 1609		# 已存入金钱{0}
STORE_MULTI_COST_XIANSHI				= 1610		# 您将花费{0}仙石扩展{1}个格子，是否确认？

#掉落（1700-1799）
PICK_UP_ITEM_ONLY_CAPTAIN		= 5337		#物品{0}只能由队长拾取
PICK_UP_ITEM_GET_ITEM			= 1701		#{0}通过队长分配获得了{1} x {2}
PICK_UP_ITEM_ROLL_ABANDON		= 1702		#{0}放弃了{1}
PICK_UP_ITEM_ROLL_POINT			= 1703		#{0}对{1}掷出了{2}点
PICK_UP_ITEM_ROLL_MAX_POINT		= 1704		#{0}掷出了最高点{1}，获得了{2} x {3}
PICK_UP_ITEM_ALLOCATION_FAILED	= 1705		#该玩家距离过远，无法分配
PICK_UP_ITEM_ROLE_GET_ITEM		= 1706		#{0}获得了{1} x {2}


#摆摊（1800-1900）
STALL_ITEM_FULL 						= 1800		# 当前可上架的商品已满
STALL_ITEM_NULL							= 1801		# 没有可交易的项目
STALL_SELL_MONEY_NOTENOUGH				= 1802 		# 金币剩余携带量不足					
STALL_ALREADY_SOMEONE					= 1803		# 当前位置已有其他玩家摆摊
STALL_FORBIDDEN_STATE					= 1804		# 当前状态无法摆摊
STALL_MONEY_NONE 						= 1805 		# 上架的商品还没有价格，请标好价后在上架
STALL_ITEM_AMOUNT_NOT_ENOUGH			= 1806		# 商品剩余数量不足！
STALL_ITEM_SOLD_OUT						= 1807		# 该商品已下架！
STALL_SELL_MONEY_LIMIT					= 1808		# 金币数量超过上限
STALL_SELL_SETTLEMENT					= 1809		# 您在摊位{0}购买了{1}个{2}。该次交易共支出了金币{3}。
STALL_COLLECTION_SETTLEMENT				= 1810		# 您向摊位{0}出让了{1}个{2}。该次交易共获得了金币{3}。
STALL_OPEN_TOO_FAR						= 1811 		# 目标距离太远,请靠近后在操作。
STALL_POINT_IS_FULL						= 1812		# 摆摊位置已满。
STALL_POINT_ALREAD_HAS_ONE				= 1813		# 该摆摊位置已有人。
STALL_NAME_TOO_LONG						= 1814		# 摆摊名字太长。
STALL_POINT_IS_ERROR					= 1815		# 摊位不存在。
STALL_END  								= 1816		# 对方已结束摆摊。
STALL_FORBIDDEN_AREA					= 1817		# 不在摆摊区域内。
STALL_BUY_TIPS							= 1818		# 您是否要花费{0}购买{1}个{2}？
STALL_SELL_TIPS							= 1819		# 您是否要以{0}的价格出让{1}个{2}？
STALL_SCRIPTID_NO_POINT					= 1820		# 该地图没有摆摊点
STALL_UPDATA_SUCCESSFUL					= 1821		#出售物品信息更新成功
STALL_ISBIND_NOSELL						= 1822		#绑定的物品不能出售
STALL_REMOVE_ALL_ITEM					= 1823		#确定要下架所有商品吗？
STALL_TOTAL_CALCULATE					= 1824		#本次摆摊时长：{0}<br/>本次收益：出售商品共获得金钱{1}<br/>本次支出：收购商品共花费金钱{2}
STALL_CANCEL_STALL						= 1825		#是否放弃摆摊？
STALL_MUST_BE_UNLOCK					= 1827		#解除安全锁后，方可摆摊
STALL_CAN_NOT_SELL						= 1828		# 该道具不可收购！
STALL_HAS_STOP_NAVIGATE					= 1829		# 摆摊寻路已终止！
STALL_FAIL_FULL_MONEY					= 1830		#已上架的物品总售价，超过当前携带的金钱上限，无法继续摆摊

#灵石寄售（1901-1949）
LINGSHI_TRADE_NOT_ADD					 = 1901		# 不能再上架更多的商品了
LINGSHI_TRADE_PRICE_ERROR				 = 1902		# 请输入有效单价
LINGSHI_TRADE_AMOUNT_ERROR				 = 1903		# 请输入有效的出售数量
LINGSHI_TRADE_XIANSHI_NOT_POUNDAGE		 = 1904 	# 您的仙石不足以支付手续费
LINGSHI_TRADE_MONEY_NOT_ENOUGH			 = 1905		# 您的金币不足！
LINGSHI_TRADE_MONEY_NOT_POUNDAGE		 = 1906		# 您的金币不足以支付手续费!
LINGSHI_TRADE_ORDER_AMOUNT_ERROR		 = 1907		# 当前剩余仙石数量不足。
LINGSHI_TRADE_ORDER_XIANSHI_NOT_ENOUGH	 = 1908		# 仙石不足！
LINGSHI_TRADE_SELL_ORDER_SUCCESS		 = 1909		# 您寄售的仙石成功出售[{0}]个，获得[{1}]，收益寄存于“我的收售”界面，请前往领取。
LINGSHI_TRADE_COLLECT_ORDER_SUCCESS		 = 1910	    # 成功收购灵石[{0}]个，消费[{1}]，灵石寄存于“我的收售”界面，请前往领取。
LINGSHI_TRADE_MONEY_MAX					 = 1911		# 金币携带已达上限
LINGSHI_TRADE_LINGSHI_MAX				 = 1912		# 灵石达到上限
LINGSHI_TRADE_SELL_SUCCESS 				 = 5225 	# 寄售交易成功，货币已添加至背包内
LINGSHI_TRADE_COLLECT_SUCCESS 			 = 5226 	# 寄售交易成功，货币已发放至邮件中，请及时查收！
LINGSHI_TRADE_CANT_BUY_SELF		 		 = 5227 	# 不可以购买自己寄售的货币

#幻兽（1950-2014）
PET_CANNOT_HATCH_AS_STATE				 = 1950		# 该状态下无法召唤幻兽
PET_HATCH_SUCCESS						 = 1951		# 孵化幻兽成功,您获得{0}幻兽
PET_HATCH_FAIL							 = 1952		# 孵化幻兽失败！
PET_FREE_OR_NOT							 = 1953		# 幻兽放生后，将无法还原，是否放生？
PET_FREE_FAIL_AS_BATTLE					 = 1954		# 正在出战状态的幻兽无法放生
PET_FREE_IS_SUCCESS						 = 1955		# 幻兽[{0}]已被放生
GB_OPERATE_FREQUENTLY					 = 1956		# 你的操作过于频繁
PET_TAKE_LEVEL_NO_ENOUGH				 = 1957		# 您还未达到该幻兽的携带等级
PET_IS_IN_DORMANT_CANOT_CONJURE			 = 1958		# 幻兽正处于休眠中，无法出战
PET_IS_ACTIVE							 = 1959		# 幻兽正处于出战状态，无法执行其他操作
PET_IS_IN_DORMANT_CANOT_OPERATE			 = 1960		# 幻兽正处于休眠状态，无法执行其他操作
PET_CANNOT_UPDATE_STEP_NOT_ENOUGH_LEVEL	 = 1961		# 角色等级未达到{0}级，幻兽无法升阶
PET_CANNOT_UPDATE_STEP_NOT_ENOUGH_POTENTIAL= 1962	# 您的潜能不足，幻兽无法升阶
PET_NAME_HAS_ILEGAL_STRING				 = 1963		# 名字含有非法字符，请重新输入
PET_NAME_THE_SAME_TO_ROLE_NAME			 = 1964		# 幻兽不能与角色同名，请重新输入
PET_MODIFY_NAME_SUCCESS					 = 1965		# 幻兽名修改成功。
PET_COMPOSE_INPUT_VPET					 = 1966		# 请放入想要合成的幻兽
PET_COMPOSE_FAIL_VPET_STEP_NOT_ENOUGH	 = 1967		# 幻兽未达到6阶，无法进行幻兽合成
PET_ACTIVATE_CAGE_CONST_MONEY			 = 1968		# 是否花费{0}金钱解锁该栏位
PET_ACTIVATE_CAGE_CONST_GOLD			 = 1969		# 是否花费{0}元宝解锁该栏位
PET_ACTIVATE_CAGE_NO_ENOUGH_LEVEL		 = 1970		# 需要{0}等级，才能解锁该栏位
PET_ACTIVATE_CAGE_NO_ENOUGH_MONEY		 = 1971		# 金钱不足，无法解锁该幻兽栏位
PET_ACTIVATE_CAGE_NO_ENOUGH_GOLD		 = 1972		# 元宝不足，无法解锁该幻兽栏位
PET_NAME_LONG_NO_SUITABLE				 = 1973		# 幻兽名需在2~7个汉字或4~14个字节之间，请重新输入
PET_CANNOT_GET_MORE						 = 1974		# 无法孵化更多的幻兽！
PET_NAME_SAVE_OR_NOT					 = 1975		# 是否保存当前幻兽名字？
PET_CAN_NOT_MOUNT_PET_BY_FIGHT_STATE	 = 1976		# 战斗状态下，无法骑乘
PET_SEAL_CHARM_CAN_NOT_CONSUME			 = 1977		# 您是否要消耗{0}个封印符，对幻兽进行封印？ 确定 取消
PET_SEAL_CHARM_NOT_ENOUGN				 = 1978		# 您的封印符不足，无法进行封印
PET_COMPOSE_NO_ENOUGH_MATERIALS			 = 1979		# 仙灵果不够，是否直接消耗仙石进行幻兽合成？ 确认 取消
PET_COMPOSE_NO_ENOUGH_MONEY				 = 1980		# 金钱不足，无法合成
PET_COMPOSE_NO_ENOUGH_GOLD				 = 5308		# 仙石不足，无法合成
PET_PASSIVE_SKILL_NO_SKILL_BOOK			 = 1981		# 您还未放入被动技能书，无法替换技能
PET_PASSIVE_SKILL_NOT_ENOUGH_QUALITY	 = 1982		# 幻兽品质太低，无法学习该技能
PET_PASSIVE_SKILL_IS_SAME				 = 1983		# 被动技能书与被替换技能相同，无法替换
PET_PASSIVE_SKILL_NO_BOOKS				 = 1984		# 被动技能残卷不足，无法升级被动技能
PET_PASSIVE_SKILL_WRONG_BOOKS			 = 1985 	# 请放入正确的被动技能残卷
PET_PASSIVE_SKILL_NO_ENOUGH_MONEY		 = 1986 	# 金钱不足，无法升级
PET_SKILL_NO_SKILL_BOOK 				 = 1987		# 请放入主动技能书
PET_SKILL_NOT_SAME_RACES				 = 1988		# 种族不符，幻兽无法学习该主动技能
PET_SKILL_NOT_SAME_QUALITY				 = 1989		# 被替换技能品质较高，替换后将无法还原，是否替换？  确认，取消
PET_SKILL_NOT_SAME_LEVEL				 = 1990 	# 被替换技能等级较高，替换后将无法还原，是否替换？  确认，取消
PET_SKILL_NO_ENOUGH_MATERIALS			 = 1991 	# 启化丹不足，无法替换
PET_SKILL_NO_ENOUGH_MONEY 				 = 1992		# 金钱不足，无法替换
PET_SKILL_NO_ENOUGH_STEP				 = 1993 	# 幻兽主动技能等级不能超过幻兽的阶位
PET_SKILL_NO_ENOUGH_POTENTIAL			 = 1994 	# 潜能不足，无法升级
PET_INITIATIVE_SKILL_UPGRADE			 = 1995 	# 是否消耗{0}点潜能将{1}技能提升到{2}级？  是，否
PET_CAN_NOT_MOUNT_AS_STATE_NOT_ALLOW	 = 1996 	# 该状态无法上坐骑！
PUT_CONJURE_PET_INITIATIVE_SKILL		 = 1997 	# 请放入出战的幻兽主动技能
PET_COMPOSE_QUALITY_IS_NOT_SAME			 = 1998 	# 不同品质的幻兽，无法合成
PET_NO_TARGET_FOR_ATTACK				 = 1999		# 请为幻兽选中可供攻击的目标
PET_TARGET_IS_TOO_FAR_NOT_ATTACK		 = 2000		# 目标太远了，无法攻击
PET_CAN_NOT_MOUNT_PET_BY_ACTFORBID		 = 2001		# 当前状态下，无法骑乘
PET_NO_CONJURED_CANNOT_USE_ITEM			 = 2002		# 必须召唤一个幻兽后才能使用。
PET_BATTLE_UNABLE_RENAME				 = 2003		# 幻兽在出战状态下，无法改名
PET_DETERMIN_POTRNTIAL_CONSUMPTION		 = 2004		# 确定消耗{0}潜能对幻兽进行升阶吗 
PET_REACHED_HIGHEST_ORDER				 = 2005		# 幻兽已达到最高阶
PET_IS_ACTIVE_SKILL_TYPE				 = 2006		# 技能书不匹配，无法替换
PET_HPSLOT_AND_MPSLOT_IS_NONE			 = 2007		# 气血/内息槽存放的气血/内息值为0，请及时补充
PET_HPSLOT_IS_FULL						 = 2008		# 幻兽气血槽已满，无法继续添加
PET_MPSLOT_IS_FULL						 = 2009		# 幻兽内息槽已满，无法继续添加
PET_CANT_CATCH 							 = 2010 	# 该幻兽当前拥有权非您所有，可静候5分钟后再行拾取
PET_CANT_FOOD_WILDNESS					 = 2012		# 原兽处理野性难驯状态，不能喂食
PET_EXCHAGE_EACH_OTHER					 = 2014		# 幻兽出栏，当前出战幻兽会入栏，是否确定？
PET_GET_EXP								 = 2018		# 幻兽{0}获得{1}点经验
PET_CANNOT_OUTSIDE_CD_TIME				 = 2019		# CD时间不能出栏
PET_SKILL_LEARN_LEVEL					 = 5902		# 只能使用@F{fc=c4}1@D级的技能书替换当前技能
PET_SKILL_LEARN_USE_BOOK				 = 5903		# 使用@F{fc=c4}{0}@D替换后，@F{fc=c4}{1}@D将会消失，是否确认替换？

# 稀有怪物刷新
MONSTER_REFRESH_NOTICE					= 2011		# {0}已在{1}现身，请速来挑战，击败后可获得丰厚奖励

# 商城（2015-2100）
SPECIALSHOP_ITEM_NOT_ENOUGH				= 2015		# 物品没有足够的数量。
SPECIALSHOP_FAIRYSTONE_NOT_ENOUGH		= 2016		# 您当前仙石数额不足以支付货款。
SPECIALSHOP_IS_NOT_OPEN					= 2017		# 商城还没开业。
SPECIALSHOP_XUANSTONE_NOT_ENOUGH		= 2018		# 您当前玄石数额不足以支付货款。
SPECIALSHOP_ITEM_NOT_FOUND				= 2019		# 没有找到此类物品
SPECIALSHOP_QUICKSTONE_NOT_ENOUGH		= 2020		# 您当前灵石数额不足以支付货款。


# 队伍（2101-2180）
TEAM_REQUEST_FORBID						= 2101		# (SY,SC):"对方婉拒了您的申请。",
TEAM_CAPTAIN_REFUSE_INVITE				= 2102		# (SY,SC):"队长拒绝让[{0}]加入队伍。",
TEAM_INVITE_PLAYER						= 2103		# (SY,SC):你已向[{0}]发出组队邀请。
TEAM_PLAYER_REFUSE_INVITE				= 2104		# (SY,SC):[{0}]婉拒了你的邀请。
TEAM_NOT_FIND_INVITER					= 2105		# (SY,SC):对方不在线。
TEAM_PLAYER_IN_TEAM_INVITE				= 2106		# (SY,SC):目标正在被邀请,请稍候。
TEAM_PLAYER_ALREADY_INVITE				= 2107		# (MB):您已经邀请了一个玩家,请稍候。
TEAM_NOT_INVITE_SELF					= 2108		# (MB):不能邀请自己！
TEAM_PLAYER_IN_TEAM						= 2109		# (MB):对方已有队伍。
TEAM_SELF_IN_TEAM						= 2110		# (MB):您已经在队伍中。
TEAM_FULL								= 2111		# (MB):队伍已满。
TEAM_FULL_REFUSE_JOIN					= 2112		# (MB):该队伍人数已满
TEAM_JOIN_TEAM_SUCCESS					= 2113		# (SY):你加入了[{0}]的队伍。
TEAM_MEMBER_JOIN						= 2114		# (SY,SC):[{0}]加入了队伍。
TEAM_AUCTION_PICK						= 2115		# (SY,SC):队伍的拾取模式改为竞拍拾取
TEAM_ORDER_PICK							= 2116		# (SY,SC):队伍的拾取模式改为队伍拾取
TEAM_LEADER_PICK						= 2117		# (SY,SC):队伍的拾取模式改为队长分配
TEAM_INVITE_FOLLOW_OTHER_PLAYER			= 2118		# (MB):"[{0}]邀请你跟随他，你是否接受？"
TEAM_CAPTAIN_LEAD_TEAM					= 2119		# (SY):您向队员发出了组队跟随邀请。
TEAMATE_FOLLOW_SUCCESS					= 2120		# (SY):[{0}] 已经跟随您。
TEAMATE_FOLLOW_REPLY_FALSE				= 2121		# (SY,SC):[{0}]拒绝了您的跟随邀请。
TEAMATE_WHETHER_FOLLOW_CAPTAIN			= 2122		# (MB):是否要跟随队长行动？
TEAM_DISBAND_CONFIRM					= 2123		# (MB):是否确认解散该队伍？
TEAM_NOT_CAPTAIN						= 2124		# (SY,SC):你不是队长。
TEAM_IS_NOT_MEMBER						= 2125		# (SY,SC):玩家不是队伍成员！
TEAM_MEMBER_NOT_ON_LINE					= 2126		# (SY,SC):该队员不在线
TEAM_NOT_IN_TEAM						= 2127		# (SY,SC):玩家不在队伍中！
TEAMATE_INVITE_SEND_TO_CAPTAIN			= 2128		# (MB):组队邀请已转交队长，请等候答复！
TEAM_CREATE_TEAM						= 2129		# (SY,SC):你成功创建了队伍。
TEAM_REFUSE_JOIN						= 2130		# (SY,SC):您拒绝了[{0}]的组队邀请。
TEAM_JOIN_FAILURE						= 2131		# (SY,SC):加入队伍失败。
TEAM_SEND_JOIN_REQUEST					= 2132		# (SY,SC):您申请加入[{0}]的队伍。
TEAM_MEMBER_LEAVE_TEAM					= 2133		# (SY,SC):[{0}]离开了队伍。
TEAM_LEAVE								= 2134		# (MB):你离开了队伍。
TEAM_MEMBER_CHANGE_CANPTAIN				= 2135		# (SY,SC):当前队长为：[{0}]。
TEAM_DISBAND							= 2136		# (SY,SC):队伍已解散。
TEAM_CAPTAIN_AGREE_INVITE				= 2137		# (SY,SC):队长已向[{0}]发出组队邀请。
TEAM_PLAYER_FORBID_INVITE				= 2138		# (MB):对方拒绝与您组队。
TEAM_CANCEL_TEAM_FOLLOW					= 2139		# (SY,SC):您取消了队伍跟随。
TEAM_LEADER_CANCEL_TEAM_FOLLOW			= 2140		# (SY,SC):队长[{0}]取消了队伍跟随。
TEAM_MEM_CANCEL_TEAM_FOLLOW				= 2141		# (SY,SC):队员[{0}]取消了队伍跟随。
TEAM_TO_FAR_TO_FOLLOW					= 2142		# (MB):距离太远，跟随队长失败。
TEAM_MEM_TO_FAR_TO_FOLLOW				= 2143		# (SY,SC):队员[{0}]由于距离太远，跟随失败。
TEAM_FOLLOW_FORBID_DIZZY				= 2144		# (MB):眩晕状态下无法跟随。
TEAM_FOLLOW_FORBID_FIX					= 2145		# (MB):定身状态下无法跟随。
TEAM_FOLLOW_FORBID_SLEEP				= 2146		# (MB):睡眠状态下无法跟随。
TEAM_FOLLOW_FORBID_WIND					= 2147		# (MB):缠绕状态下无法跟随。
IS_STOP_TEAM_FOLLOW						= 2148		# (MB):正在组队跟随中，是否停止？
IS_STOP_TEAM_NORMAL_FOLLOW				= 2149		# (MB):正在跟随中，是否停止？
TEAM_TO_FOLLOW_FAILD					= 2150		# (MB):目标已离开当前地图或者已下线。
TELEPORT_TO_TARGET						= 2151		# (MB):即将被传送到{0}身边
TEAM_PICK_QUALITY_BLUE					= 2152		# (SY,SC):队伍的分配品质改为蓝色
TEAM_PICK_QUALITY_GOLD					= 2153		# (SY,SC):队伍的分配品质改为黄色
TEAM_PICK_QUALITY_PINK					= 2154		# (SY,SC):队伍的分配品质改为粉色
TEAM_PICK_QUALITY_GREEN					= 2155		# (SY,SC):队伍的分配品质改为绿色
ITEM_INVITE_TARGET_OFF_LINE				= 5564		#对方已离线
TEAM_FORBID_DIFF_CAMP_INVITE_EACH_OHER  = 5916      #当前地图不同阵营玩家禁止组队
#普通跟随
COMMON_FOLLOW_TO_FAW_AWAY				= 2156		# 距离太远，无法跟随
COMMON_FOLLOW_PLAYER_DEAD				= 2157		# 该玩家已死亡，无法跟随
COMMON_FOLLOW_THE_SUCCESSFUL			= 2158		# 跟随成功
COMMON_FoOLLOW_TO_BEING					= 2159		# [{0}]正在跟随你
COMMON_FOLLOW_TO_CANCEL					= 2160		# 取消跟随
COMMON_FoOLLOW_TO_STOP					= 2161		# [{0}]已取消跟随你
TEAM_INVITED_IS_SEAD					= 2162		# 您已向该队伍发送过入队申请，请耐心等待!
TEAM_REQUEST_IS_SEAD					= 2163		# 您已向该玩家发送过组队邀请，请耐心等待!
TEAM_NOT_FIND_PLAYER					= 2164		# 对方不在线

#快速组队
FAST_TEAM_FORBID_LEVEL 					= 2165		# 该队伍只有{0}级到{1}级的玩家才能加入
FAST_TEAM_FORBID_PROFESSION 			= 2166		# 您的职业与要求不符，无法加入该队伍
FAST_TEAM_JOIN_OTHER 					= 2168		# 您已在队伍中，无法发送求组信息
TEAM_NOT_JOIN_SELF						= 2169		# 不能加入自己快速组队
SELF_IS_IN_TEAM_NOT_JOIN 				= 2170		# 你在队伍中无法加入快速组队
SENDER_IS_LOGIN_OFF						= 2171		# 发起者已不在线
TEAM_PLAYER_IN_TEAM_APPLY				= 2172		# 你已申请，请稍等
TEAM_PLAYER_REFUSE_JOIN					= 2173		# [{0}]婉拒了你的申请。
FAST_TEAM_IS_ALREADY_REQ 				= 2174		# 您正在搜索{0}副本的队伍，是否停止搜索并开启{1}活动的队伍搜索
FAST_TEAM_IS_FULL 						= 2175		# 您的队伍已满员
FAST_TEAM_IS_IN_TEAM_LIMIT				= 2176		# 您已在队伍中，无法发送求组信息
FAST_TEAM_REQ_TEAM_FAILURE 			= 2177		# 没有搜索到合适的玩家
FAST_TEAM_REQ_PRESON_FAILURE 			= 2178		# 没有搜索到适合的队伍
FAST_TEAM_IS_MATCH_FAST_TEAM			= 5887		#正在快速组队，无法进入副本

SPACE_NOT_ALLOW_JOIN_TEAM				= 2183		# 当前地图无法组队
ROLE_IN_NOT_ALLOW_JOIN_TEAM_SPACE 		= 2184		# 该玩家位于不可组队的地图中
FAST_TEAM_FORBID_MEMBER 				= 2185		# 该副本只能3名玩家参与，您的队伍人数不符合。
COMMON_FOLLOW_FAIL		 				= 2186		# 当前状态下，无法跟随
SPACE_CANT_ENTER_IN_TEAM	 			= 5545 		# 当前地图不能组队进入

#复活（2181-2199）
RIVIVE_ITEM_NOT_ENOUGN					= 2181		#原地复活需要使用归命符箓，您可以在道具商城购买到归命符箓

#SpellBox（2200-2280）
SPELL_BOX_RESULT_ADD_BUFF 				 = 2200		# 获得Buff: {0}
SPELL_BOX_RESULT_ADD_EXP				 = 2201		# 获得经验: {0}
SPELL_BOX_RESULT_ADD_ITEM				 = 2202		# 获得物品:	{0}


#仙化
SPAR_FAIRY_SUCCESS_RESULT		 = 2300		# 盘古大神护佑，激发“仙化”状态获得额外修为。

CHALLENGE_CHANGE_BODY = 2350				# 准备好与我比赛变身了吗？

#寻路（2400-2449）
NO_NAVIGATE_DATA_IN_DST_POS = 2400		#寻路失败，目标点无法到达。
CANNOT_NAVIGATE_FROM_CURRENT_SPACE_TO_DST_SPACE = 2401		#寻路失败，请完成当前剧情内容。
ONLY_NAVIGATE_IN_PLAYER_MAP = 2410		#只能在角色所在地图寻路
IS_CROSS_MAP_NAVIGATE = 2411		#是否要传送到 "{0}" 传送点？
CURRSTATR_CAN_NOT_NAVIGATE = 2412		#当前状态无法寻路

#传送石（2450-2499）
CANNOT_OPEN_TELEPORTSTONE_WITHLIMITLV = 2450	#	还未达到XX级，无法激活传送石
CANNOT_TELEPORT_WITHMONEYCOST		  = 2451	#	您的金钱不足以支付传送费用
CANNOT_TELEPORT_WITHCAMPLIMIT		  = 2452	#	您的阵营不符合此传送目的地
CANNOT_TELEPORT_WITHOUT_STONE		  = 2453	#	您还未获得神行石，无法进行传送
TELEPORT_BY_TELEPORTSTONE			  = 2454	#	神行石已就绪，是否进行传送？
TELEPORT_BY_MONEY					  = 2455	#	神行石正在休整中，是否启用付费传送？付费传送将消耗{0}
TELEPORT_POINT_NOT_OPEN				  = 2456	#	传送点还未激活
CANT_TELEPORT_STONE_DEAD_STATE 		  = 2457 	#	当前为死亡状态，无法使用神行石进行传送！
TELEPORT_STONE_HAS_ACTIVATE 		  = 2458 	#	{0}神行点已激活！

#称号（2500-2529）
ROLE_MSG_GAIN_TITLE					= 2500		#	你获得称号[%s]

#输入（2530-2539）
INPUT_CONTAIN_SENSITIVE_CHAR		= 2530		#	您输入的内容中包含敏感词汇，请重新输入
ROLE_NAME_CONTAIN_FORBIDDEN_CHAR	= 2531		#	角色命名仅支持中文，不能使用字母数字或符号
INPUT_CONTAIN_FORBIDDEN_CHAR		= 2532		#	您输入的内容含有非法字符，请重新输入
IS_SAVE_INPUT_CONTENT				= 2533		#	是否保存当前输入内容？

#环任务钓鱼
CATCH_FISH_MISS						= 2701		#鱼挣脱逃走了
CATCH_FISH_SUCCESS					= 2702		#钓上一条鱼
#环任务猜大小
DICE_GUESS_CHARGE_BIG				= 2703		#确定押大？
DICE_GUESS_CHARGE_SAMLL				= 2704		#确定押小？
#环任务奖励确认
LOOP_QUEST_REWARDS_CONFIRM_THREE_PARAMS			= 2705		#{0},获得经验:{1}获得金钱:{2} 确认
LOOP_QUEST_REWARDS_CONFIRM_FIVE_PARAMS			= 2706		#{0},获得经验:{1}获得金钱:{2}获得额外经验:{3}获得额外金钱:{4} 确认
LOOP_QUEST_REWARDS_CONFIRM_TWO_PARAMS			= 2707		#{0},获得经验:{1}确认
LOOP_QUEST_REWARDS_CONFIRM_FOUR_PARAMS			= 2708		#{0},获得经验:{1}获得额外经验:{2}获得额外金钱:{3}确认

#晶石狩猎场(2750 - 2799)
SPARHUNTING_ACTIVITY_SIGN_UP_ALREADY 	 = 2750		#已成功报名，请勿重复报名！
SPARHUNTING_ACTIVITY_SIGN_UP_LEVEL_ERROR = 2751		#只有30级及以上的玩家才能参与活动!
SPARHUNTING_ACTIVITY_SIGN_UP_SUCCESS	 = 2752 	#报名成功！
SPARHUNTING_ACTIVITY_NOT_SIGN_UP		 = 2753		#您没报名活动，不能进入战场！
SPARHUNTING_ACTIVITY_SIGN_UP_TIME_ERROR	 = 2754	 	#现在不是报名时间!
SPARHUNTING_ACTIVITY_NOT_START			 = 2755 	#对不起，活动暂未开放，请留意活动开放时间。
SPARHUNTING_ACTIVITY_SIGN_UP_TIME		 = 2756		#活动即将开始，请稍后进入。
SPARHUNTING_INTEGRAL_MAX				 = 2757		#已超过携带上限，无法获得更多金晶，请前往炼化炉处炼化转换为金钱。
SPARHUNTING_TOTAL_REWARD_MONEY			 = 2759		#本次点金石共带来了多少金钱收益
SPARHUNTING_SIGN_UP 					 = 2760		#金满仓正在征召勇敢的修士前往神秘的晶石狩猎场试炼，请30级及以上玩家前往凤鸣城金满仓处报名！
SPARHUNTING_SIGN_UP_FIFTEEN 			 = 2761		#（15分钟）金满仓正在征召勇敢的修士前往神秘的晶石狩猎场试炼，请30级及以上玩家前往凤鸣城金满仓处报名！
SPARHUNTING_SIGN_UP_TWENTY_FIVE			 = 2762		#（25分钟）神秘的晶石狩猎场试炼即将开启，请30级及以上玩家前往凤鸣城金满仓处报名参与！
SPARHUNTING_SIGN_UP_END					 = 2763		#晶石狩猎场试炼报名已结束，已报名的玩家可前往金满仓处开启活动
SPARHUNTING_KILL_FIRST					 = 2764		#{0}英雄{1}开启杀戮序幕，一骑当先！
SPARHUNTING_GOD_LIKE					 = 2765		#{0}英雄{1}已超越了神的杀戮，但求一败！
SPARHUNTING_KILL_GOD_PLAYER				 = 2766		#{0}英雄{1}挤高一筹，终结了{2}超越神的杀戮！
SPARHUNTING_FIVE_BKILL					 = 2767		#你已连续被击败，获得晶石精灵赐予力量，抓紧时间复仇吧！
SPARHUNTING_ACTIVITY_END 				 = 2768		#本次晶石狩猎场活动已经结束，恭喜{0}获得金钱榜{1}。
SPARHUNTING_NOBODY_COMBAT				 = 2769		#{0}英雄{1}气势如虹，已经无人能挡！
SPARHUNTING_CRAZY_KILL					 = 2770		#{0}英雄{1}一刀一个小盆友，正在疯狂杀戮！
SPARHUNTING_ROLE_GET_LUCKY				 = 5437		#{0}遇到天赐机缘，将获得一番大造化。
SPARHUNTING_GET_LUCKY					 = 5438		#您遇到天赐机缘，是否进入机缘玩法
SPARHUNTING_GET_MANAY_GIFT				 = 5569		#{0}已从机缘副本中满载而归，金光外露羡煞旁人。


#自动战斗（2800-2849）
AUTO_FIGHT_ADD_SKILL					= 2800		#	请放入一个可攻击技能
AUTO_FIGHT_ADD_HP_ITEM					= 2801		#	请放入恢复气血的药品
AUTO_FIGHT_ADD_MP_ITEM					= 2802		#	请放入恢复内息的药品
AUTO_FIGHT_SAVE_TIPS					= 2803		#	您修改的数据还未保存，点击确定后将自动保存当前数据。
AUTO_FIGHT_OPEN							= 2804		#	您已开启自动战斗
AUTO_FIGHT_CLOSE						= 2805		#	自动战斗已关闭

#真龙棋局副本（2850-2860）
SPACE_ZLQJ_STATE_TIPS					= 2850		#	10秒钟后BOSS将会切换状态
SPACE_ZLQJ_CHANGED_STATE				= 2851		#	BOSS已经切换状态

# 防沉迷系统相关(2861-2900)
ANTI_WALLOW_COMMON                       = 2861		# "(SY,SC):您累计在线时间已满{0}小时，为了您的健康，请做适当身体活动，合理安排学习生活。"
ANTI_WALLOW_ENTER_HALF_LUCRE             = 2862		# "(SY,SC):您累计在线时间已满{0}小时,请您下线休息,做适当身体活动，合理安排学习生活。",
ANTI_WALLOW_HALF_LUCRE                   = 2863		# "(SY,SC):您已经进入疲劳游戏时间,您的游戏收益将降为正常值的 50％,为了您的健康,请尽快下线休息,做适当身体活动,合理安排学习生活。",
ANTI_WALLOW_NO_LUCRE                     = 2864		# "(MB):    您已进入不健康游戏时间，为了您的健康，请您立即下线休息。如不下线，您的身体将受到损害，您的收益已降为零，直到您的累计下线时间满 5 小时后，才能恢复正常。"


#系统功能栏
FUNCTION_TEMPOR_DONOTOPEN			= 2901		#功能暂不开放

#邮件(3000-3100)
MAIL_SEND_SUCCESS                        = 3000		# 邮件发送成功
MAIL_TITLE_TOO_LONG                      = 3001		# 邮件标题太长
MAIL_CONTENT_TOO_LONG                    = 3002		# 邮件内容太长
MAIL_RECEIVER_NOT_FOUND                  = 3003		# 收件人不存在，请输入正确的收件人
MAIL_ITEM_NOT_ALLOW_TRADE                = 3004		# 不能邮寄不能出售的物品。
MAIL_ITEM_NOT_BINDED                     = 3005		# 不能邮寄绑定的物品。
MAIL_RECEIVER_NAME_EMPTY				 = 3006		# 请输入收件人的名字
MAIL_RECEIVER_IS_SENDER					 = 3007		# 收件人填写错误，请填写正确的收件人
MAIL_TITLE_IS_EMPTY						 = 3008		# 邮件还没有主题
MAIL_SEND_HAS_NOT_ENOUGH_MONEY			 = 3009		# 金钱不足，无法发送邮件。
MAIL_DELETE_HAS_NOT_CHOICE				 = 3010		# 请选中想要删除的邮件
MAIL_DELETE_HAS_ATTACHMENT				 = 3011		# 是否删除选中的所有邮件（含有附件的邮件无法删除）
MAIL_FULL 								 = 3012		# 您的邮箱已满，将无法及时收到新的邮件，请及时清理
MAIL_DELETE_HAS_NOT_READ				 = 3013		# 邮件未阅读，确定要删除邮件吗？
MAIL_DELETE 							 = 3014		# 确定是否删除邮件
MAIL_RECEIVER 							 = 3015		# 您收到了新的邮件，请注意查收
MAIL_HAS_NO_ITEM_EXTRACT 				 = 3016		# 已无可提取附件
MAIL_EXTRACT_SUCCESS 					 = 3017		# 附件提取成功
MAIL_DELETE_FORBID_ATTACHMENT			 = 3018		# 邮件中有附件未领取，不能删除


#帮会（3100-3199）
TONG_CANOT_JOIN_MAX_NUM					= 3100		# 你发送的申请过多
TONG_CANOT_JOIN_NOT_ENOUGH_LEVEL		= 3101		# 20级以上玩家才能加入帮会
TONG_CANOT_JOIN_HAS_TONG				= 3102		# 您已拥有帮会，无法加入新的帮会
TONG_CANOT_JOIN_MAX_MEMBER				= 3103		# 该帮会人员已达上限，无法申请
TONG_CANOT_JOIN_REFUSE					= 3104		# {0}帮会拒绝了您的申请
TONG_CANOT_JOIN_DIFFER_CAMP				= 3105		# 阵营不同，无法加入
TONG_JOIN_SUCCESS_OTHER					= 3106		# 欢迎{0}加入帮会
TONG_JOIN_SUCCESS_SELF					= 3107		# 欢迎加入{0}帮会，与我们一起并肩携手终结洪荒乱世
TONG_CANOT_INVITE_NOT_ENOUGH_GRADE		= 3108		# 您没有邀请玩家入帮的权限
TONG_CANOT_INVITE_MAX_MEMBER			= 3109		# 帮会人员已达上限，无法邀请更多玩家加入
TONG_CANOT_INVITE_REFUSE				= 3110		# {0}拒绝了你的邀请
TONG_CANOT_INVITE_CAMP					= 3111		# 不能邀请敌对阵营玩家加入帮会
TONG_CANOT_INVITE_HAS_TONG				= 3112		# 该玩家已加入其它帮会
TONG_INVITE_TO_TONG						= 3113		# {0}邀请你加入{1}帮会
TONG_NOT_ENOUGH_GRADE					= 3114		# 你的权限不够！
TONG_KICK_OUT_TONG						= 3115		# 你将{0}踢出了帮会
TONG_BEKICK_OUT_TONG					= 3116		# {0}将你踢出了帮会
TONG_CANOT_LEAVE_TITLE_1				= 3117		# 您需要将帮主之位转让给其他成员之后，才能退出帮会
TONG_CANNOT_UPGRADE_NOT_ENOUGH_MONEY	= 3118		# 帮会资金不足，无法升级
TONG_CANNOT_UPGRADE_NOT_ENOUGH_ACTIVITY	= 3119		# 帮会活跃度不足，无法升级
TONG_CANNOT_RENAME_NAME_IS_EXIT			= 3120		# 该职位已存在，请输入新的职位名称
TONG_STORAGE_CANT_STORE					= 3121		# 已绑定物品不能放入帮会仓库!
TONG_STORAGE_IS_FULL					= 3122		# 帮会仓库已满，无法存放更多的道具！
TONG_RESEARCH_SAME_TIME_MUL_SKILLID		= 3123		# 同一时间只能研发一个帮会技能
TONG_RESEARCH_NO_ENOUGHT_MONEY			= 3124		# 帮会资金不足，技能无法研发
TONG_RESEARCH_NO_ENOUGHT_BUILD_LEVEL	= 3125		# 研究院需要达到{0}等级，才能研发该技能
TONG_KICK_ONE_OUT_TONG					= 3126		# {0}将{1}踢出了帮会
TONG_LEADER_QUIT_TONG_CONFIRM			= 3127		# 您已决定解散帮会了吗？
TONG_DISBAND_NOTIFY						= 3128		# (MB)您的帮会{0}已被解散
TONG_DISBAND_NOTIFY_LOW_ACTIVITY_1		= 3129		# (MB)帮会活跃度持续低迷，若在没有起色，7日之后，凤鸣城将收回贵帮的帮会领地，并解散贵帮会。
TONG_DISBAND_NOTIFY_LOW_ACTIVITY_2		= 3130		# (MB)贵帮活跃度持续低迷，已引起凤鸣城高层震怒，1日之后，就将收回贵帮的帮会领地，并强制解散贵帮会。
TONG_FORCE_DISBAND_NOTIFY				= 3131		# (SY){0}帮会已被强制解散。
TONG_DISBAND_CONFIRM					= 3132		# 建帮不易，是否确认解散帮会
TONG_MEMBER_LEAVE_TONG					= 3133		# {0}退出了帮会
TONG_AMOUNT_REACH_MAX					= 3134		# 服务器帮会数量已达上限，无法创建更多帮会
TONG_CREATE_NO_ENOUGH_DAOHENG			= 3135		# 您的道行太低，等达到仙师/魔师，再来吧
TONG_NAME_CONTAIN_FORBIDDEN_CHAR		= 3136		# 帮会名字含有非法字符，请重新输入
TONG_NAME_REACH_MAX						= 3137		# 帮会名字超过上限，请重新输入
TONG_HAS_ALREADY_EXISTED				= 3138		# 该帮会已存在
TONG_CREATE_NO_ENOUGH_MONEY				= 3139		# 金钱不足，无法创建帮会
TONG_CREATE_CANNOT_REACH_LEVEL			= 3140		# 等级必须达到30级及以上才能创建帮会
TONG_IS_CREATEING_CANNOT_APPLY			= 3141		# 您正在筹建{0}帮会，无法加入其他帮会
TONG_CREATE_SUCCESS_XIAN				= 3142		# 恭喜您创建{0}，从此除魔洪荒，并肩携手
TONG_CREATE_SUCCESS_MO					= 3143		# 恭喜您创建{0}，纵横四海，与尔同仇
TONG_JOIN_SUCCESS						= 3144		# 恭喜您加入{0}帮会
TONG_QUERY_CANNOT_FIND					= 3145		# 未搜索到该帮会
TONG_JOIN_NOT_SELECTED_TONG				= 3146		# 请选中想要加入的帮会
TONG_DONATE_INPUT_AMOUNT				= 3147		# 捐款金额不足，最少捐款1金
TONG_CHAT_FORBID_SPEAK					= 3148		# 您已被帮中高层禁言，无法再帮会聊天频道发言
IS_LEAVE_TONG							= 3149		# 您确定要退出帮会吗，退出帮会后帮贡将全部清零。
TONG_UPGROW_FAIL_NOT_EMOUGH_MONEY		= 3150		# 帮会资金不足，无法提升帮会建筑等级
TONG_UPGROW_FAIL_NOT_EMOUGH_GROW		= 3151		# 帮会成长度不足，无法提升帮会建筑等级
TONG_UPGROW_FAIL_NOT_EMOUGH_LEVEL		= 3152		# 帮会等级不满足，无法提升帮会建筑等级
TONH_UPGROW_SWCCESS						= 3153		# {0}已成功提升到{1}级
TONG_STUDY_SKILL_NO_ENOUGH_MONEY		= 3154		# 金钱不足，无法学习该技能
TONG_STUDY_SKILL_NO_ENOUGH_CONTRIBUYION	= 3155		# 帮贡不足，无法学习该技能
TONG_STUDY_SKILL_NO_ENOUGH_XIUWEI		= 3156		# 修为不足，无法学习该技能
TONG_SKILL_DEVELOP_IS_STOP				= 3157		# (MB):是否暂停【{0}】的研发。
TONG_MONEY_IS_FULL						= 3158		# 帮会金库已满，所以只收纳了您所捐献的{0}！
TONG_MONEY_IS_FULL_ALREADY				= 3159		# 帮会的资金已经到达上限，请提升仓库等级！
TONG_DONATE_MONEY_SELF_RESULT			= 3160		# 您为帮会捐献了{0}，获得{1}点帮贡和帮会{2}点经验
TONG_DONATE_MONEY_OTHER_RESULT			= 3161		# {0}为帮会捐献了{1}，获得{2}点帮贡和帮会{3}点经验
TONG_OPEN_LEVEL							= 3162		# (SY,SC):帮会系统20级开放
TONG_SKILL_BEGIN_RESEARCH				= 3163		# (TG):{0}技能已开始研发，踊跃完成帮会日常会提升帮会研发进度
TONG_DEMISE_LEADER_FOR_YOU				= 3164		# {0}将帮主之位转让于你，望你带领本帮问鼎凤鸣。
TONG_DEMISE_FAIL_NO_ENOUGH_EXP			= 3165		# 该帮众的对帮会贡献太低，无法转让帮主
TONG_CHAT_IS_GAG						= 3166		# 您已被帮中高层禁言，无法再帮会聊天频道发言
TONG_LEVEL_CANNOT_BUY_GOODS				= 3167		# (MB)您的帮众等级太低，无法购买该商品
TONG_STORAGE_LEVEL_UPGRADE_CAN_OPEN_BAG	= 3168		# (MB) 提升帮会仓库等级，可以开启更多的格子
TONG_MEMBER_TITLE_ONLINE				= 3169		# 【{0}】{1}上线了
TONG_MEMBER_TITLE_OFFLINE				= 3170		# 【{0}】{1}下线了
TONG_CANOT_JOIN_AS_MAX_MEMBER			= 3171		# 帮会人员已达上限，无法加入该帮会
TONG_IS_SET_PLAYER_MANAGER				= 3172		# (MB):您确定提升【{0}】为帮会管理层
TONG_IS_RELIEVE_MEMBER_DUTY				= 3173		# (MB):您确定解除【{0}】的职位
TONG_IS_KICK_PLAYER						= 3174		# (MB):您确定将【{0}】踢出帮会
TONG_DUTY_SET_SUCCESS					= 3175		# (SY):职位任命成功
YOU_DISMISS_MEMBER_TONG_DUTY			= 3176		# (SY):你罢免了【{0}】的职位
IS_SAVE_TONG_GRADE_MODIFY				= 3177		# (MB):权限发生了变动，是否保存修改。
IS_SAVE_TONG_EVENT_SET_MODIFY			= 3178		# (MB):帮会事件设置发生了变动，是否保存修改。
TONG_SPACE_COPY_NOT_ENOUGHT_TIME		= 3179		# 今天帮会副本次数已用完!
TONG_SPACE_COPY_ENTER_DELAY				= 3180		# {0}秒后进入{1}副本
TONG_SPACE_COPY_NOT_IN_TONG				= 3181		# 你还没加入帮会
TONG_MEMBER_GET_CONTRIBUTION			= 3182		# 获得了{0}帮贡
TONG_DONATE_MONEY_IS_FULL				= 3183		# 今天捐献的帮贡已到达上限！
TONG_DONATE_MONEY_IS_FULL_ALREADY		= 3184		# 今天捐献的帮贡已到达上限,所以只收纳了您所捐献的{0}！
IS_SURE_CHANGE_TONG_LEADER_TO_TARGET	= 3185		# (MB):你确定转让【{0}】为帮主
YOU_TONG_DUTY_BE_SET_SUCCESS			= 3186		# 您被【{0}】{1}任命为{2}
YOU_BE_DISMISS_MEMBER_TONG_DUTY			= 3187		# 您的【{0}】职位已被【{1}】{2}罢免
TONG_REJOIN_FORBID_CD_TIME 				= 3188		# 您刚刚离开帮会，必须{}后才能申请加入新的帮会
TONG_INVITE_FORBID_CD_TIME 				= 3189		# 该玩家刚刚离开帮会，必须{}后才能邀请他进入帮会
TONG_CREATE_WORLD_NOTICE				= 3190		# 恭喜{0}建立{1}帮会
TONG_TITLE_MEMBER_HAS_ENOUGH			= 3191		# 无法任命，该职位任命人数已达上限
TONG_MEMBER_COST_CONTRIBUTION			= 3192		# 消耗了{0}帮贡
TONG_HAS_JOING							= 5464		# 您已加入其它帮会。
TONG_CANOT_DESTROY_PUBLIC_ITEM			= 5450		# 您不能销毁帮会公共道具。

#荷花法阵（3200 -- 3210）
HEHUAFAZHEN_NOT_CAN_MOVE				= 3200		# 当前方向因障碍或者所处边界无法移动，请尝试其他方向移动

# 3994-4053 被客户端用了

#至尊争霸（3220-3240）
ZHIZUNZHENBA_ACTIVITY_START             = 3220      #至尊争霸活动于19.30开启报名，请等级在30级以上的玩家前往柳晴儿报名参加比赛！
ZHIZUNZHENBA_SURE_REFUSE_GAME			= 3221		#你确定是否放弃比赛？
ZHIZUNZHENBA_LIMIT_LEVEL				= 3222		#当前活动需要等级≥30级，请勇士提升实力之后再来参加。
ZHIZUNZHENBA_SIHN_UP_LIMIT_TEAM			= 3223		#此次活动是单人比赛，请您离开队伍再来参加。
ZHIZUNZHENBA_NOT_SIGN_UP_START			= 3224		#活动报名将在每周三和周六晚19:30开启，请在勇士在规定时间内前来报名。
ZHIZUNZHENBA_SIGN_UP_LIMIT_NUMBER		= 3225		#此次活动人数已满，请您等待下一次活动时间。
ZHIZUNZHENBA_ENTER_LIMIT_TEAM			= 3226		#此活动为单人活动，请勇士离开队伍之后再来进入活动场地。

#幻阵迷宫（3240~3260）
HUAN_ZHEN_MI_GONG_SUCCESS_MSG = 3240			#挑战成功，即将传送回幻阵迷宫
HUAN_ZHEN_MI_GONG_FAILURE_MSG = 3241			#挑战失败，即将传送回幻阵迷宫
HUAN_ZHEN_MI_GONG_ANSWER_QUESTION_GOOD_PLAYER_MSG = 3242	#玩家{0}天资聪颖，当获嘉奖，获得10%的额外奖励
HUAN_ZHEN_MI_GONG_ANSWER_QUESTION_TEAM_PERFECT_MSG = 3243	#诸位惊才绝艳，特备厚礼以表钦佩。
HUAN_ZHEN_MI_GONG_ANSWER_QUESTION_TEAM_GOOD_MSG = 3244	#诸位才高八斗，略备薄礼聊表吾心。


#PK模式提示（4054~4057）
PK_MODE_PEAD_MSG = 4054			#该状态无法切换PK模式
PK_MODE_PEAD_MSG = 4055		    #战斗状态无法切换PK模式
PK_MODE_PEAD_MSG = 4056			#死亡状态无法切换PK模式
PK_MODE_PEAD_MSG = 4057			#等级低于30级无法切换PK模式


#CST-3740 法宝碎片提示信息
FBSP_GET_FA_BAO	 = 4080			#成功收集法宝碎片*1 


#阵营竞技-----英雄王座 （4085-4119）
SPACECOPY_CAMP_YXLM_BUILIDING_UPGRADE			= 4085			#我方{0}路防御塔的到冰封强化
SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_UPGRADE 	= 4086			#敌方{0}路防御塔得到冰封强化，请注意
SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_ROLE			= 4087			#{0}的{1}已被{2}的{3}击杀！
SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_BUILIDING	= 4088			#{0}的{1}已被{2}的防御力量击杀！
SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_CREEPS  		= 4089			#{0}的{1}在野区遇到不测，被野怪击杀！
SPACECOPY_CAMP_YXLM_NOT_CAPTAIN_SIGNUP			= 4090			#请退出队伍或由队长报名
SPACECOPY_CAMP_YXLM_NOT_START					= 4091			#活动暂未开启，报名失败！
SPACECOPY_CAMP_YXLM_SIGN_UP_ALREADY				= 4092			#已成功报名，请勿重复报名！
SPACECOPY_CAMP_YXLM_CANCEL_SIGNUP				= 4093			#报名已取消，退出匹配
SPACECOPY_CAMP_YXLM_CANCEL_AFFIRM				= 4094 			#战队成员{0}取消确认，你已重新排队。
SPACECOPY_CAMP_YXLM_TEAMMEMBER_CANCEL_AFFIRM 	= 4095			#队友{0}取消确认，你已退出排队。
SPACECOPY_CAMP_YXLM_TEAM_CHANGE					= 4096			#战队人员发生改变，你已重新排队。
SPACECOPY_CAMP_YXLM_ENEMY_TEAM_CHANGE			= 4097			#敌方战队人员发生改变，你已重新排队。
SPACECOPY_CAMP_YXLM_MATCH_ITEM_CHANGE			= 4098			#战队人员发生改变，你已退出排队。
SPACECOPY_CAMP_YXLM_ENEMY_MATCH_ITEM_CHANGE		= 4099			#敌方战队人员发生改变，你已退出排队。
SPACECOPY_CAMP_YXLM_MEM_CONFIRM_FAILURE			= 4100			#队伍中有人没有确认，你已退出排队。
SPACECOPY_CAMP_YXLM_ACTIVITY_IS_JOIN			= 4101			#您已经参加过本次活动，请下次再来。
SPACECOPY_CAMP_YXLM_MEMBER_IS_JOIN				= 4102			#队伍中有人已参加过本次活动，请下次再来。
SPACECOPY_CAMP_YXLM_MEMBER_LEVEL_NOTIN_DIFFLEVEL= 4103			#队员与队长不在同一等级段内，匹配失败。
SPACECOPY_CAMP_YXLM_NOTIFY						= 4104			#阵营英雄王座活动将于20:00开启，请参与活动的道友前往各自阵营活动NPC处准备报名。
SPACECOPY_CAMP_YXLM_START 						= 4105			#阵营英雄王座活动已经开始了，请参与活动的勇士在各自阵营活动NPC处参加活动。
SPACECOPY_CAMP_YXLM_END  						= 4106			#阵营英雄王座活动已经结束，感谢大家参与，请留意下次活动时间。
SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_CHANGE	= 4107			#基地正遭受敌方攻击，请速来支援！
SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_FIVITY	= 4108			#基地生命不足50%，请速来支援！
SPACECOPY_CAMP_YXLM_BASE_BUILIDING_HP_THRTY		= 4109			#基地生命不足30%，十分危险，请速来支援！
SPACECOPY_CAMP_YXLM_BASE_BUILIDING_DESTROY		= 4110			#基地已经被摧毁，请下次多多努力！
SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_DESTROY		= 4111			#敌人已经被打败！恭喜获得最终胜利！
SPACECOPY_CAMP_YXLM_DESTROY_BUILDING_LESS_WIN	= 4112			#剩余的防御塔更多，恭喜获得胜利！
SPACECOPY_CAMP_YXLM_TIME_KILL_FAILURE			= 4113			#未能击杀更多敌人，请下次多努力！
SPACECOPY_CAMP_YXLM_TIME_JADE_MOVE_WIN			= 4114			#获得魂玉更多，恭喜获得胜利！
SPACECOPY_CAMP_YXLM_TIME_JADE_FAILURE			= 4115			#未能获得更多魂玉，请下次多努力！
SPACECOPY_CAMP_YXLM_ENEMY_LEVEL_SPACE			= 4116			#敌方溃败脱逃，恭喜获得最终胜利！
SPACECOPY_CAMP_YXLM_BUILIDING_KILL				= 4117			#我军一个防御塔被摧毁！
SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_KILL		= 4118			#敌人一个防御塔被摧毁！
SPACECOPY_CAMP_YXLM_SOLDIERS_CREATE				= 4119			#{0}兵已加入我方{1}路进行战斗




# 至尊争霸-----十方城 （4120-4140）
SHI_FANG_CHENG_COMPLETESTAGE 			= 4120		#恭喜你,成功通过区域{0}，耗时{1}。此次竞赛第{2}名通过区域{3}。
SHI_FANG_CHENG_COMPLETESTAGE_FIRST		= 4121		#{0}实力超群,以一骑绝尘的速度率先通过了{1}区域。尚未通过的勇士们，需要继续努力。
SHI_FANG_CHENG_COMPLETESTAGE_SECOND		= 4122		#{0}实力超群，在 第一名 之后顺利通过{1}区域。尚未通过的勇士们，需要继续努力。
SHI_FANG_CHENG_COMPLETESTAGE_THREE		= 4123		#{0}实力超群，紧随 第一名跟第二名 的脚步，顺利通过{1}区域。尚未通过的勇士们，需要继续努力。
SHI_FANG_CHENG_COMPLETESTAGE_BEHIND_THREE=4124		#已经有{0}名玩家顺利通过{1}区域。尚未通过的勇士们，需要继续努力。
SHI_FANG_CHENG_SPACE_SUCCESS_FIRST		= 4125		#{0}实力超群，以一骑绝尘的速度率先通关副本。尚未通关的勇士们，需要继续努力。
SHI_FANG_CHENG_SPACE_SUCCESS_SECOND 	= 4126		#{0}实力超群，在 第一名 之后顺利通关副本。尚未通关的勇士们，需要继续努力。
SHI_FANG_CHENG_SPACE_SUCCESS_THREE		= 4127		#{0}实力超群，紧随 第一名跟第二名 的脚步，顺利通关副本。尚未通关的勇士们，需要继续努力。
SHI_FANG_CHENG_SPACE_SUCCESS_BEHIND_THREE=4128		#已经有{0}名玩家顺利通关副本。尚未通关的勇士们，需要继续努力。
SHI_FANG_CHENG_SPACE_SUCCESS   			= 4129		#恭喜你通关副本，耗时{0}。此次竞赛排名{1}名.
SHI_FANG_CHENG_SIGN_UP_END              = 4130      #活动报名时间已经结束，请勇士下次早点前来报名。
SHI_FANG_CHENG_SIGN_UP_AREADY           = 4131      #勇士已经报名成功，无需再次报名。
SHI_FANG_CHENG_SIGN_UP_SUCCESS          = 4132      #勇士已经成功报名了活动，请在活动开启时前来进入活动场地
SHI_FANG_CHENG_NOT_SIGN_UP              = 4133      #勇士尚未报名活动，无法进入活动场地。
SHI_FANG_CHENG_ACTIVITY_SIGN_UP         = 4134      #至尊争霸活动已接受报名，请等级在30级以上的玩家前往柳晴儿报名参加比赛！
SHI_FANG_CHENG_ACTIVITY_SIGN_UP_END     = 4135      #至尊争霸活动已结束，请已报名的玩家前往柳晴儿准备参加比赛！
SHI_FANG_CHENG_ACTIVITY_START           = 4136      #至尊争霸活动已开启，请已报名的玩家前往柳晴儿参加比赛！
SHI_FANG_CHENG_LIMIT_TEAM				= 4137		#此活动为单人活动，不可以组队。


#阵营竞技-----灵脉战场 （4140-4160）
ACTIVITY_CAMP_READY_ENTER						= 4140			# 匹配成功，是否已准备好进入战场
ACTIVITY_CAMP_ENTER_FAIL						= 4141			# 有玩家未准备充足，继续匹配，请耐心等候
ACTIVITY_CAMP_LING_MAI_GRAB_GOURD				= 4143			# {0}玩家{1}成功从对方营地中夺得一枚灵能宝葫！
ACTIVITY_CAMP_OCCUPY_LINGMAI					= 4144			# {0}占领了{1}部灵脉
ACTIVITY_CAMP_OCCUPY_PAGODA						= 4145			# {0}占领了{1}灵塔
ACTIVITY_CAMP_FIX_TIME							= 4146			# 战场将在{0}s后开启...
ACTIVITY_CAMP_COUNT_DOWN_TIME					= 4147			# 战场将在{0}s后开启...
ACTIVITY_CAMP_CANNOT_SIGNIN_AFTER_MATCHING		= 4148			# 战场匹配中，请勿重复报名。
ACTIVITY_CAMP_LING_MAI_NOTICE					= 4149			# 阵营竞技@F{fc=c8}灵脉战场@D将在五分钟后开启，请30级及以上的玩家做好准备。
ACTIVITY_CAMP_LING_MAI_START					= 4150			# 阵营竞技@F{fc=c8}灵脉战场@D已经开启，请30级及以上的玩家前往@F{fc=c7}@L{t='凤鸣城陆玄';m=goto:10000201#L_FMC} @D处报名参加。
ACTIVITY_CAMP_LING_MAI_END						= 4151			# 阵营竞技@F{fc=c8}灵脉战场@D已经结束。
ACTIVITY_CLOSE_NOTIFY							= 4152			# 战场{0}秒后关闭！
ACTIVITY_CAMP_XIAN_CREATE_CRYSTAL				= 4153			# 仙道大本营中出现一枚灵能宝葫！
ACTIVITY_CAMP_MO_CREATE_CRYSTAL					= 4154			# 魔道大本营中出现一枚灵能宝葫！

#帮会争霸 （4170-4230）
TONG_STARCRAFT_SIGNUP_HASNOT_GRADE				= 4170			# 你的权限不足，报名失败！
TONG_STARCRAFT_SIGNUP_LEVEL_TONG				= 4171			# {0}已离开帮会，请重新选择参赛人员。
TONG_STARCRAFT_SIGNUP_SUCCESS					= 4172			# 报名成功！
TONG_STARCRAFT_JOIN_NOTIFY						= 4173			# 帮主已选定你参加帮会争霸序幕战！
TONG_STARCRAFT_FIRST_SIGN_UP					= 4174			# 帮会争霸序幕战已开启报名，截止至晚18点，有意角逐本阵营第一帮会的帮主不要犹豫，速去凤鸣城帮会管理员肖业出报名吧！
TONG_STARCRAFT_FIRST_START_NOTICE				= 4175			# 帮会争霸序幕战10分钟后开始，已报名的帮会请组织人员准时参加。
TONG_STARCRAFT_FIRST_START 						= 4176			# 帮会争霸序幕战已开启，请各个帮会参赛选手尽快前往肖业处参加比赛
TONG_STARCRAFT_FIRST_END						= 4177			# 本次帮会序幕战挑战时间已结束，正在进行挑战的帮会请继续完成挑战，还未进行挑战的帮会算作挑战失败，欢迎各帮会前往肖业处查看战绩。
TONG_STARCRAFT_SECOND_SIGN_UP					= 4178			# 帮会争霸淘汰赛即将举行，获得参赛资格的帮会不要忘记报名参战哦！
TONG_STARCRAFT_SECOND_START_NOTICE 				= 4179			# 帮会争霸淘汰战10分钟后开始，这次谁将脱颖而出，成为阵营第一大帮，让我们拭目以待！
TONG_STARCRAFT_FIRST_TEAM_CANNOT_EMPTY			= 4180			# 队伍成员不能为空！
TONG_STARCRAFT_FIRST_CANOT_CHANGE_MEMBER		= 4181			# 参赛人员选定后将不可更改，确定选择？
TONG_STARCRAFT_SECOND_FIRST_TONG				= 4182			# 本场淘汰战胜负已见分晓，{0}帮会计胜一筹，即将展开最后的争霸战！
TONG_STARCRAFT_THIRD_FIRST_TONG					= 4183			# 本次帮会争霸赛最终胜负已分，恭喜{0}帮会成为我{1}霸主！
TONG_STARCRAFT_FIRST_SIGN_UP_NOTICE				= 4184			# 帮会争霸淘汰赛即将举行，获得参赛资格的帮会不要忘记报名参战哦！



#阵营竞技------冰雪之战 （4231-4270）
ACTIVITY_CAMP_FROZEN_FIGHT_OCCUPY_RIVIVE_POS	= 4231			# {0}占领了{1}复活点
ACTIVITY_CAMP_FROZEN_FIGHT_OCCUPY_TOWER			= 4232			# {0}占领了{1}哨塔
ACTIVITY_CAMP_FROZEN_FIGHT_NOTICE				= 4233			# 阵营竞技@F{fc=c8}冰雪之战@D将在30分钟后开启，请需要参战的玩家准时前往@F{fc=c7}@L{t='凤鸣城陆玄';m=goto:10000201#L_FMC} @D处报名。
ACTIVITY_CAMP_FROZEN_FIGHT_START				= 4234			# 阵营竞技@F{fc=c8}冰雪之战@D正在火热进行，请需要参战的玩家准时前往@F{fc=c7}@L{t='凤鸣城陆玄';m=goto:10000201#L_FMC} @D处报名。
ACTIVITY_CAMP_FROZEN_FIGHT_END					= 4235			# 阵营竞技@F{fc=c8}冰雪之战@D已经结束。
ACTIVITY_CAMP_FROZEN_FIGHT_XIAN_KILL_BOSS  		= 4236 			# 仙道阵营击杀了魔道大将
ACTIVITY_CAMP_FROZEN_FIGHT_MO_KILL_BOSS   		= 4237 			# 魔道阵营击杀了仙道大将
ACTIVITY_CAMP_FROZEN_FIGHT_MO_DESTROY_TOWER 	= 4238 			# 魔道摧毁了南侧哨塔
ACTIVITY_CAMP_FROZEN_FIGHT_XIAN_DESTROY_TOWER 	= 4239 			# 仙道摧毁了北侧哨塔


#切磋(4271-4320)
COMPETE_SELF_IN_COMPETING 						= 4271				#您正处于切磋中
COMPETE_TARGET_IN_COMPETING 					= 4272				#对方正在切磋中，无法接受您的邀请
COMPETE_TARGET_NOT_IN_FREE  					= 4273				#对方当前状态无法接受您的邀请
COMPETE_SELF_LEAVE_AREA 						= 4274				#你已超出切磋范围，切磋取消
COMPETE_TARGET_LEAVE_AREA 						= 4275				#{0}超出切磋范围，切磋取消
COMPETE_TARGET_DEAD 							= 4276				#对方已死亡，切磋取消
COMPETE_TARGET_REFUSE 							= 4277				#{0}拒绝了你的切磋邀请
COMPETE_COUNTDOWN 								= 4278				#@F{n=/Game/Miscs/Fonts/FZJinLing;fc=c6; fs=20;ft=Bold}@F{fc=c3}{0}
COMPETE_WIN 									= 4279				#您战胜了{0}
COMPETE_LOSE 									= 4280				#您被{0}击败
COMPETE_BE_INVITED 								= 4281				#{0}向你发起来切磋请求，是否接受他的挑战?
COMPETE_SPACE_CAN_NOT 							= 4282 				#当前地图不允许切磋
COMPETE_TARGET_SO_FAR 							= 4283 				#目标过远无法发起切磋
COMPETE_SELF_LEAVE_AREA_WARNING 				= 4284 				#你已离开切磋区域！请在{0}秒内返回
COMPETE_SELF_NOT_IN_FREE  						= 4285				#您当前状态无法发送切磋邀请
COMPETE_MSG_1_0 								= 4286 				#{0}：仙道，魔道，皆为我道，神道，鬼道，不如证道，{1}，可愿与我一战，互证己道.
COMPETE_MSG_1_1 								= 4287 				#{0}：与君一战，不负所学，请赐教。
COMPETE_MSG_2_0 								= 4288 				#{0}：天机浩渺，唯争一线，世情沉沦，难脱真我，{1}，可愿与我一战，脱却尘芥。
COMPETE_MSG_2_1 								= 4289 				#{0}：也罢，那边放下一切，战个痛快吧，请赐教！
COMPETE_MSG_3_0 								= 4290 				#{0}：天人还是蝼蚁，一战而决，{1}，可敢迎接我的挑战。
COMPETE_MSG_3_1 								= 4291 				#{0}：那就看看谁才是真正的蝼蚁吧！
COMPETE_TARGET_ACCEPT 							= 4292 				#{0}接受了你的挑战
COMPETE_END 									= 4293 				#强大的{0}在与{1}的巅峰对决中获胜，再一次向世人证明了自己的力量
COMPETE_TARGET_DEAD 							= 4294 				#对方已死亡，切磋取消
COMPETE_COUNTDOWN_END 							= 4295 				#切磋将在{0}秒后结束
COMPETE_INVALID_SO_FAR 							= 5459 				#目标距离过远，无法切磋

CANT_TELEPORT_POINT_FIGHT_STATE                 = 4298 				#当前为战斗状态，无法使用传送点进行寻路！
CANT_TELEPORT_STONE_FIGHT_STATE                 = 4299 				#当前为战斗状态，无法使用神行石进行寻路！

CAN_NOT_EQUIP_IN_COMBAT							= 4300				# 战斗中不可换装


# 场景分线
SPACE_LINENUMBER_IS_CLOSE 				= 4304		# 该分线已关闭，无法进入
TEAM_MEMBER_NOT_IS_NEAR 				= 4305		# {0},不在附近，无法进入副本
TEAM_CAPTAIN_CALL_YOU					= 4306		# 队长召唤你去与他相同的线，是否同意!
TEAM_CAPTAIN_LINENUMBER_IS_FULL			= 4307		# 本分线分成拥挤，无法召唤更多玩家
TEAM_LINENUMBER_IS_FULL  				= 4308		# 该分线非常拥挤，请选择其它分线
TEAM_CAN_NOT_SIGN_NUMBER 				= 4309		# 无法标记目标
SPACE_DIFF_LINENUMBER_NOT_COMPETE 		= 4310		# 无法与不同分线玩家切磋
STALL_STATE_NOT_CHANGE_LINE 			= 4312		# 摆摊状态下无法切换线路
STATE_NOT_ALLOW_TEAM_CALL 				= 4313		# 该状态下，无法接受队长召唤
ROLE_IN_NOT_ALLOW_CALL_STATE 			= 4314		# {0}处于不可召唤的状态
ROLE_NOT_IN_SPACE_LINENUMBER_CAN_NOT_CALL=4315		# {0}当前不在分线地图上，无法召唤
TEAM_CAPTAIN_STATE_NOT_ALLOW_CALL 		= 4316		# 该状态下无法召唤队友

SPACE_LINENUMBER_IS_FULL 				= 5307		# 该分线非常拥挤,请选择其他分线


TEAM_CAPTAIN_LIMIT_CALL 				= 4315		# 玩家当前不在分线地图上无法召唤

#聊天频道 (4400 - 4415)
COMBAT_BE_DAMAGE								= 4400		#{0}（玩家或怪物）对你使用{1}（技能、道具）造成了{2}（数值）伤害
COMBAT_BE_DAMAGE_MISS							= 4401		#{0}（玩家或怪物）的{1}（技能、道具）未命中你
COMBAT_BE_TREATMENT								= 4402		#{0}（玩家或怪物）对你使用{1}（技能、道具）恢复了{2}（数值）气血
COMBAT_CAUSE_DAMAGE								= 4403		#你使用{0}（技能、道具）对{1}造成了{2}（数值）伤害
COMBAT_CAUSE_DAMAGE_MISS						= 4404		#你的{0}（技能）未命中{1}（玩家或怪物）
COMBAT_CAUSE_TREATMENT							= 4405		#你使用{0}（技能、道具）对{1}恢复了{2}（数值）生命值气血
COMBAT_KIll_TARGET								= 4406		#你击败了{0}（玩家）
COMBAT_BY_KIll									= 4407		#你被{0}（玩家）击败
COMBAT_BY_BUFF									= 4408		#你获得了效果{0}（各类增益buff名称）
COMBAT_LOST_BUFF								= 4409		#{0}（效果名称）已从你身上移除 
CHAT_SPEAK_FREQUENTLY							= 4410		#你的发言过于频繁，请稍后再试！
CHAT_OUTOF_NUMBER								= 4411		#你本日在此频道发言次数已用完
CHAT_LEVEL_CANNOT_SATISFY						= 4412		#需要{0}级，才可以使用此频道
CHAT_TARGET_NOT_EXIST							= 4415		#目标不存在

# 在线奖励(4731-4750)
ONLINE_REWARD_LING_SHI_NOT_ENOUGH				= 4731			# 你的灵石不足，无法操作


#血斗凤栖镇 (4761-4780)
ZHIZUNZHENBA_THE_FIRST					= 4761		#{0}在凤栖镇中，力压群雄，获得了本次至尊大会霸主称号！
YE_ZHAN_FENG_QI_END_MESSAGE				= 4762		#是否离开活动场地
YE_ZHAN_FENG_QI_MEMBER_OUT 				= 4763		#已经被淘汰
YE_ZHAN_FENG_QI_MEMBER_BE_KILL 			= 4765		#{0}玩家被{1}玩家一招毙命淘汰出局。
GET_JOIN_YE_ZHAN_FENG_QI 				= 4766		#恭喜你，获得进入凤栖镇资格。
LOSE_JOIN_YE_ZHAN_FENG_QI				= 4767		#很遗憾，此次未能获得进入凤栖镇资格。请下次努力。
YE_ZHAN_FENG_START_NOTICE				= 4768		#凤栖镇 活动将在20点开启，请获得参赛资格的玩家前往 凤鸣城柳晴儿 准备参加比赛!
YE_ZHAN_FENG_START 						= 4769		#凤栖镇 活动已开启，请获得参赛资格的玩家前往 凤鸣城柳晴儿 参加比赛!
YE_ZHAN_FENG_QI_CAN_NOT_JOIN 			= 4770		#勇士在十方城的比试成绩靠后，没有获得进入凤栖镇，无法进入活动场地。
YE_ZHAN_FENG_START_TO_JOIN 				= 5845		# 凤栖镇已开启，是否立刻进入？


#福袋活动 (4781 - 4800)
ZHEN_BAO_NANG_USE 						= 4781 		#开启将获得玲珑珠，是否开启 
ZHEN_BAO_NANG_USE_END					= 4782		#恭喜，您已获得玲珑珠，您可以前往灵气浓郁之地种植
LING_LONG_ZHU_MONEY						= 4783		#玩家获得{0}金钱
LING_LONG_ZHU_ITEM						= 4784		#玩家获得{0}
ZHEN_BAO_HE_USE							= 4785		#开启将获得金种子，是否开启
ZHEN_BAO_HE_USE_END						= 4786 		#恭喜，您已获得金种子，您可以前往灵气浓郁之地种植金树！

#GM工具添加自定义公告
GMTOOLS_ADD_CUSTOM_NOTICE 			    = 4800      #{0}


#阵营系统 (4801 - 4900)
CAMP_TAOISM_MORALE_EFFECT_ONE 					= 4801		#仙道阵营气运碾压魔道，所有仙道玩家获得气运加成，蒸蒸日上
CAMP_TAOISM_MORALE_EFFECT_TWO 					= 4802		#仙道阵营气运碾压魔道，所有仙道玩家获得气运加成，紫气东来
CAMP_TAOISM_MORALE_EFFECT_THREE 				= 4803		#仙道阵营气运碾压魔道，所有仙道玩家获得气运加成，气冲斗牛
CAMP_TAOISM_MORALE_EFFECT_FOUR 					= 4804		#仙道阵营气运碾压魔道，所有仙道玩家获得气运加成，气势如虹
CAMP_TAOISM_MORALE_EFFECT_FIVE 					= 4805		#仙道阵营气运碾压魔道，所有仙道玩家获得气运加成，浩气冲霄
CAMP_DEMON_MORALE_EFFECT_ONE 					= 4806		#魔道阵营气运碾压仙道，所有魔道玩家获得气运加成，蒸蒸日上
CAMP_DEMON_MORALE_EFFECT_TWO 					= 4807		#魔道阵营气运碾压仙道，所有魔道玩家获得气运加成，紫气东来
CAMP_DEMON_MORALE_EFFECT_THREE 					= 4808		#魔道阵营气运碾压仙道，所有魔道玩家获得气运加成，气冲斗牛
CAMP_DEMON_MORALE_EFFECT_FOUR 					= 4809		#魔道阵营气运碾压仙道，所有魔道玩家获得气运加成，气势如虹
CAMP_DEMON_MORALE_EFFECT_FIVE 					= 4810		#魔道阵营气运碾压仙道，所有魔道玩家获得气运加成，浩气冲霄
CAMP_MORALE_REWARD_LEVEL						= 4811 		#必须30级以上玩家，才能领取阵营气运奖励
CAMP_MORALE_ROLE_LIMIT							= 4812 		#今日获得气运已达上限
CAMP_MORALE_ADD									= 1205 		#获得气运{0}
CAMP_MORALE_KILL_TAOISM 						= 4813 		#您击杀了仙道阵营的{0}，魔道获得{1}点气运
CAMP_MORALE_KILL_DEMON 							= 4814 		#您击杀了魔道阵营的{0}，仙道获得{1}点气运
CAMP_MORALE_KILL_TAOISM_LIMIT 					= 4815		#多次击杀仙道阵营的{0}，已无法获得更多的气运
CAMP_MORALE_KILL_DEMON_LIMIT 					= 4816		#多次击杀魔道阵营的{0}，已无法获得更多的气运
CAMP_FEATS_KILL_TAOISM_LIMIT  					= 4817		#多次击杀仙道阵营的{0}，已无法获得更多的功勋
CAMP_FEATS_KILL_DEMON_LIMIT 					= 4818		#多次击杀魔道阵营的{0}，已无法获得更多的功勋
CAMP_FEATS_TEAM_KILL_TAOISM						= 4819 		#协助队友{0}击杀了仙道阵营的{1}，获得1点功勋值
CAMP_FEATS_TEAM_KILL_DEMON						= 4820 		#协助队友{0}击杀了魔道阵营的{1}，获得1点功勋值
CAMP_FEATS_ADD									= 1257 		#获得功勋{0}
CAMP_TAOISM_VEV_ONLINE							= 4821 		#仙道尊者{0}已上线
CAMP_DEMON_VEV_ONLINE							= 4822 		#魔道尊者{0}已上线
CAMP_FENG_MING_VEV_ONLINE						= 4823 		#凤鸣之主{0}已上线
CAMP_FEATS_IS_MAX_FIRST_TIME					= 4824		#获得功勋 0.（已达到每日击杀功勋上限：600）
CAMP_FEATS_IS_MAX								= 4825		#获得功勋 0

# 领取奖励和充值相关(4901 - 5000)
PCU_NOT_ENOUGH_GRID                      = 4951		# (MB):背包空间不足，无法获得物品。
PCU_CAN_NOT_ADD_XUANSHI 	             = 4952		# (MB):该操作将导致玄石超过上限，无法获得玄石。
PCU_CAN_NOT_ADD_XIANSHI                  = 4953		# (MB):该操作将导致仙石超过上限，无法获得仙石。
PCU_YOU_ARE_BUSY                         = 4954		# (MB):领取请求正在处理中，请稍候。
PCU_HAVE_NO_PRESENT                      = 4955		# (MB):您尚未达到领取该奖励的资格。
PCU_CHARGE_SUCCESS                       = 4956		# (SY,SC):充值已到账！

# 神通技能(5001 - 5100)
SHEN_TONG_NOT_ENOUGH_ITEM				 = 5001 	# (MB):请放入可吞噬的神通材料
SHEN_TONG_IS_COMMINUTION				 = 5002 	# (MB):吞噬材料中含有精品神通，精研后将无法恢复，是否精研！ 确定，取消
SHEN_TONG_HAS_SUCCEED					 = 5003 	# (MB):神通已精研成功，无法再次精研
SHEN_TONG_NOT_ENOUGH_POTENTIAL			 = 5004 	# (MB):潜能不足，无法精研
SHEN_TONG_NOT_ENOUGH_MONEY				 = 5005 	# (MB):金钱不足，无法精研
SHEN_TONG_TIMES_FULL					 = 5573 	# (MB):该神通技能蓄能已达上限，无法继续蓄能
SHEN_TONG_TIMES_WILL_FULL				 = 5574 	# (MB):使用后改神通技能将达到上限，超出部分将被抹去，是否确认蓄能？
SHEN_TONG_SKILL_LEARN					 = 5641 	# (MB):成功增加{神通技能名}{使用次数}次使用次数
SHEN_TONG_MAX							 = 5917		# 您无法拥有更多的神通技能
PET_SHEN_TONG_CANT_USE		 			 = 5473		# 暂时无法使用该道具
PET_SHEN_TONG_MAX		 				 = 5474		# 该幻兽无法拥有更多的神通技能
PET_SHEN_TONG_TIMES_MAX		 			 = 5855		# {0}可学习次数已达上限
PET_SHEN_TONG_REMOVE					 = 5475		# 移除后@F{fc=c4}{0}@D将会消失，无法还原，是否确定移除？
PET_SHEN_TONG_FREE						 = 5476		# 幻兽 @F{fc=c19}{0}@D已装备了神通技能，是否还要继续放生？
PET_SHEN_TONG_CANT_LEARN				 = 5926		# 幻兽无法学习该技能！
PET_SHEN_TONG_PROFESSION				 = 5928		# 种族不符，幻兽无法学习该神通技能！


# 帮会争霸第三场
THIRD_TONG_STARCRAFT_FIRST_KILL 		 = 5101 	#{0}帮会的{1}开启杀戮序幕，一骑当先!
THIRD_TONG_STARCRAFT_GOD_LIKE 			 = 5102		#{0}帮会的{1}已超越了神的杀戮，但求一败!
THIRD_TONG_STARCRAFT_KILL_GOD_PLAYER 	 = 5103		#{0}帮会的{1}技高一筹，终结了{2}超越神的杀戮！
THIRD_TONG_STARCRAFT_FIVE_KILL 			 = 5104		#{0}帮会的{1}气势如虹，已经无人能挡！
THIRD_TONG_STARCRAFT_EIGHT_KILL 		 = 5105		#{0}帮会的{1}一刀一个小盆友，正在疯狂杀戮！
THIRD_TONG_STARCRAFT_OCCUPY_SPAR 		 = 5106		#{0}帮会已占领一枚水晶
THIRD_TONG_STARCRAFT_BEOCCUPY_SPAR 		 = 5107		#{0}帮会已夺取敌方水晶


# 商城系统(5200 - 5299)
STORE_NO_ENOUGH_XIANSHI 				 = 5204 	#您的仙石不足，无法购买该商品，若想继续购买商品，请点击<text color="#FFFF00">充值</text>按钮，即可完成购买。
STORE_NO_ENOUGH_XIANSHI_REPALCE_LINGSHI	 = 5205 	#您的灵石不足，将以{0}仙石替代{1}灵石进行差额补充，是否同意？
STORE_NO_ENOUGH_XIANSHI_AND_LINGSHII 	 = 5206 	#您的仙石不足，无法补足灵石购买商品所需的差额。点击<text color=""#FFFF00"">充值</text>按钮进行充值，可获得更多仙石。
STORE_NO_ENOUGH_XUANSHI 				 = 5207 	#您的玄石不足，无法购买该商品，消费仙石可获得更多玄石。
STORE_NO_ENOUGH_XIANSHI_REPALCE_MONEY 	 = 5208 	#您的金钱不足，将以{0}仙石替代{1}金钱进行差额补充，是否同意？
STORE_NO_ENOUGH_XIANSHI_AND_MONEY 		 = 5209 	#您的仙石不足，无法补足金钱购买商品所需的差额。点击<text color=""#FFFF00"">充值</text>按钮进行充值，可获得更多仙石。
STORE_NO_ENOUGH_ROOM					 = 5214 	#背包空位不足，无法后买商品，请先清理背包
STORE_BUY_SUCCESS						 = 5213 	#购买成功
STORE_BUY_REBATE_XUANSHI				 = 1254 	#获得{0}玄石
STORE_GOODS_SOLD_OUT 					 = 5211		#该商品已下架，无法选购
STORE_GOODS_CANT_BUY_MORE 				 = 1305		#您无法再购买更多的该道具。
STORE_BALANCE_FAILED					 = 5215		#结算失败，请重新结算
STORE_BAG_HAS_ENOUGH					 = 5218 	#您的背包已满，请先清理背包
STORE_PRESENT_SUCCESS					 = 5210     #礼品成功发送
STORE_RECEIVE_GIFT						 = 5217 	#收到新的礼物，请去礼品盒中查收
STORE_CART_REMOVE_SOLD_OUT				 = 5212 	#购物车中含有已下架的商品，点击确定按钮，即可移出购物车
STORE_ROLE_NOT_EXIST 					 = 5202 	#该玩家不存在，请重新输入
STORE_ROLE_NOT_FRIEND					 = 5451		#该玩家不是您的好友，请先添加好友再赠送

STORE_CART_HAS_ENOUGH					 = 5221 	# 已超过购物车承载上限，无法再进行添加
STORE_CART_NOT_LIMIT_TIME				 = 5224 	#
STORE_GIFT_DEFAULT_MESSAGE				 = 5222 	#
STORE_GIFT_CUSTOM_MESSAGE				 = 5223 	#
STORE_GIFT_BE_REFUSE 					 = 5228 	# {0}已拒绝您的礼物，请在礼品盒赠送礼品页面进行查收
STORE_STORE_APPEARANCE_GENDER 			 = 5851 	# 性别不符

#被动技能栏
PASSIVESKILLBAR_BEFORE_NOT_UNLOCK		= 5300		# 前一个栏位还未解锁
PASSIVESKILLBAR_LEVEL_LOW				= 5301		# 等级不够，无法解锁
PASSIVESKILLBAR_MONEY_LOW				= 5302		# 金钱不够，无法解锁
PASSIVESKILLBAR_XIANSHI_LOW				= 5303		# 仙石不够，无法解锁
PASSIVESKILLBAR_WUPIN_LOW				= 5304		# 缺少道具，无法解锁

#CST-8727 勇闯夺命岛
YCJMD_BOSS_UP_LEVEL 					= 5305		# BOSS{0}进阶至{1}形态！

ZSYG_GET_NOTHING 						= 5306		#你什么都没有发现!

EQUIP_WIELD_FORBID_BY_SPACE				= 5310		# 该地图不能替换装备
ITEM_FORBID_BY_SPACE 					= 5311		# 该地图不能使用该道具
CHAT_XIANYIN_FORBID_BY_ITEM 			= 5312		# 您没有足够的仙音喇叭
CHAT_TIANYIN_FORBID_BY_ITEM 			= 5313		# 您没有足够的天音喇叭

#环任务副本 焚火金牛
LOOP_QUEST_FHJN_NEAR					= 5314		# 不要靠的太近，避免灼伤
LOOP_QUEST_FHJN_FAR						= 5315		# 不要离得太远，以免金牛挣脱捆仙绳

CANOT_BUY_GOODS_AS_LEVEL				= 5342		# 您的等级太低，无法购买该商品
CANOT_BUY_GOODS_AS_JINGJIELEVEL			= 5343		# 您的境界太低，无法购买该商品
CANOT_BUY_GOODS_AS_TONGCONTRIBUTE		= 5344		# 您的帮贡不足，无法购买该商品
CANOT_BUY_GOODS_AS_FEATS				= 5345		# 您的功勋不足，无法购买该商品


CANOT_FEED_PET_AS_CD_COOL				= 5347
PLAYER_IN_TONG_SPACE					= 5351


#CST-9960 阵营战场“勇闯绝命岛”
CAMP_YCJMD_KILL 						= 5349		# {0}玩家{1}淘汰了{2}玩家{3}
ROLE_DEAD_OUT	 						= 5412		# 死亡出局
ROLE_LEAVE_TREASURE_BOX	 				= 5425		# {0}玩家{1}被淘汰时留下了一个幸存者奖励宝箱！
ROLE_GET_TREASURE_BOX		 			= 5426		# {0}玩家{1}开启幸存者奖励宝箱后，意外的获得了{3}

#上古密阵  （5400-5499）
MI_ZHEN_KILL_BOSS							= 5316		#{0}队伍击杀{1}阶段{2}BOSS，获得{3}经验，用时{4}秒
MI_ZHEN_LAST_BOSS_ENTER_BATTLE				= 5317		#@{0}@F{fc=c0}队伍抵达@F{fc=c3}四臂魔猿@F{fc=c0}的巢穴！
MI_ZHEN_LAST_BOSS_BE_DAMAGE					= 5318		#{0}队伍已对BOSS造成{1}点伤害，{2}队伍已对BOSS造成{3}点伤害
MI_ZHEN_KILL_LAST_BOSS						= 5319		#{0}玩家击杀BOSS，{1}队伍将获得额外奖励
MI_ZHEN_BOSS_OUTOF_HP						= 5320		#{0}队伍与{1}阶段{2}BOSS激烈战斗,{3}BOSS剩余50%血量

#帮会阵营战 (5500-5700)
TONG_CAMP_WAR_NOTICE						= 5500		#帮会阵营战已开启报名，截止至19.50，有意角逐本阵营第一帮会的帮主不要犹豫，速去凤鸣城帮会管理员肖业出报名吧！
TONG_CAMP_WAR_IS_NOT_LEADER					= 5501		#你的权限不足，报名失败！
TONG_CAMP_WAR_SGIN_UP_END					= 5502		#帮会阵营战报名已经结束，请各帮会准备拖到，活动马上开启
TONG_CAMP_WAR_START 						= 5503		#帮会阵营战正式开启

PLUNDER_ACTIVITY_NOTICE_BEGIN				= 5479		# 开始 掠夺战报名通知
PLUNDER_ACTIVITY_NOTICE_END					= 5480		# 结束 掠夺战报名通知
CHALLENGE_ACTIVITY_NOTICE_BEGIN				= 5481		# 开始 争夺战报名通知
CHALLENGE_ACTIVITY_NOTICE_END				= 5482		# 结束 争夺战报名通知
PLUNDER_ACTIVITY_BEFORE_BEGIN				= 5483		# 掠夺战开启前5分钟公告
PLUNDER_ACTIVITY_BEGIN						= 5484		# 掠夺战 开始 通知
CHALLENGE_ACTIVITY_BEFORE_BEGIN				= 5485		# 争夺战开启前5分钟公告
CHALLENGE_ACTIVITY_BEGIN					= 5486		# 争夺战 开始 通知
NO_DONG_FU_OR_JADE							= 5487		# 没有洞府\玲珑玉令
CHALLENGE_HAS_INVITE						= 5488		# 已经点击了挑战（没回应）
CHALLENGE_HAS_REFUSE_INVITE					= 5489		# 您已发起过洞府争夺战，不能再次发起
CHALLENGE_PEOPLE_TOO_MUSH					= 5490		# 挑战的玩家人太多
CHALLENGE_NO_AS_LEVEL						= 5491		# 对方等级过低，无法挑战
CHALLENGE_IS_ACCEPT							= 5492		# 您向**发起挑战成功
CHALLENGE_IS_ACCEPT_OTHER					= 5493		# **同意了您发起的洞府掠夺战请求
PLUNDER_IS_ACCEPT_OTHER						= 5494		# **同意了您发起的洞府争夺战请求
CHALLENGE_IS_ACCEPT_MY						= 5495		# 您同意了**发起的洞府掠夺战请求
PLUNDER_IS_ACCEPT_MY						= 5496		# 您同意了**发起的洞府争夺战请求
CHALLENGE_IS_REFUSE_OTHER					= 5497		# **拒绝了您发起的洞府掠夺战请求
PLUNDER_IS_REFUSE_OTHER						= 5498		# **拒绝了您发起的洞府争夺战请求
CHALLENGE_IS_REFUSE_MY						= 5499		# 您拒绝了**发起的洞府掠夺战请求
PLUNDER_IS_REFUSE_MY						= 5500		# 您拒绝了**发起的洞府争夺战请求

LHMJ_PLAYER_VIT_POINT_IS_FULL				= 5801		#不能在吃更多食物了(功能废弃)
LUMJ_ON_START_REFRESH_PET					= 5501		#轮回秘境中灵气大盛，平时隐藏起来的原兽也即将出外活动，勇士/斗士赶紧前往轮回秘境，捕捉原兽吧!
TTD_SHI_LIAN_END							= 5502		#通天塔试炼结束
TTD_PLAYER_IS_IN_TEAM						= 5503		#通天塔只允许单人进入
TTE_NEED_PLAYER_LEVEL						= 5504		#等级不足，无法进入通天塔
LHMJ_CAN_NOT_ENTER							= 5666		#轮回秘境第二层尚未开启，暂时无法进入

#阵营竞技-----烽火连天 （5701-5800）
ACTIVITY_CAMP_FHLT_NOTICE					= 5701		#阵营竞技@F{fc=c8}烽火连天@D将在五分钟后开启，请30级及以上的玩家做好准备。
ACTIVITY_CAMP_FHLT_START					= 5702		#阵营竞技@F{fc=c8}烽火连天@D已经开启，请30级及以上的玩家前往@F{fc=c7}@L{t='凤鸣城陆玄';m=goto:10000201#L_FMC} @D处报名参加。
ACTIVITY_CAMP_FHLT_END						= 5703		#阵营竞技@F{fc=c8}烽火连天@D已经结束。
ACTIVITY_CAMP_FHLT_LEVEL_NOTIN_DIFFLEVEL	= 5704		#参加阵营烽火连天活动需要35级。
ACTIVITY_CAMP_FHLT_PUNISH_TIME				= 5705		#处于逃离战场惩罚期间。
ACTIVITY_CAMP_FHLT_SIGNIN_AFTER_MATCHING	= 5706		#匹配中，请勿重复报名。
ACTIVITY_CAMP_FHLT_OCCUPY_WARFLAG			= 5707		#战旗已被仙道/魔道的xxx占领
ACTIVITY_CAMP_FHLT_CREATE_DROP				= 5708		#新宝箱已刷新，开启宝箱可以获得积分或资材，请速度前往抢占宝箱
ACTIVITY_CAMP_FHLT_BARTIZAN_DESTROY			= 5709		#仙道/魔道的一座箭塔已被仙道/魔道的xxx摧毁
ACTIVITY_CAMP_FHLT_ALTAR_DESTROY			= 5710		#仙道/魔道的一座祭坛已被仙道/魔道的xxx摧毁



EVOLUTION_PET_FAIL_NO_ITEM					= 5348		# 还童丹不足
COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_ITEM			= 5352		# 道具不足，无法打造该道具
COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_MONEY		= 5353		# 金钱不足，无法打造该道具
COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_LINGNENG		= 5354		# 灵能不足，无法打造该道具
OPEN_GRID_NUM								= 5355		# 成功开启{0}个背包格子
OPEN_ALL_GRID_NUM							= 5356		# 背包格子已全部开启
SHOP_ONlY_COMPOSE_ONE_ITEM					= 5357		# 工坊同一时间只能打造一件道具
TRIPOD_IS_FULL_SHOULD_CLEAN					= 5358		# 储物柜已满，请先清理背包
COMPOSE_TOOL_SUCCESS						= 5359		# 您打造的{0}已经打造成功，请回到洞府储物柜取出打造好的道具。
COMPOSE_TOOL_FAIL							= 5360		# 您打造的{0}已经打造失败，请回到洞府储物柜取出打造好的道具。
CAN_NOT_PRAY_AGAIN							= 5361		# 超过10次祈福，无法再祈福
QUENCHING_EQUIP_SUCCESS						= 5363		# 淬炼成功
QUENCHING_FAIL_AS_NOEMOUGHT_ITEM			= 5364		# 材料不足，无法淬炼
QUENCHING_EQUIP_FINISH						= 5365		# 装备已经淬炼成功，可以正常使用
CAN_PUT_IT_DOWN								= 5366		# 放置成功
CAN_NOT_PUT_IT_DOWN							= 5367		# 该区域不可放置该道具
CAN_NOT_USE_KUILEI_IN_SPACE					= 5368		# 该地图无法放置傀儡
CAN_NOT_USE_KUILEI_IN_SELF_DONGFU			= 5369		# 您无法在自己的洞府中放置傀儡

#捕捉原兽
CATCH_TARGET_NOT_ORIGINPET					= 5376		#目标非原兽，无法捕捉
CATCH_TARGET_NOT_BELONG_TO_PLAYER			= 5377		#该原兽归属与他人，你无权捕捉
JADE_UPGRADE_COST							= 5379		# 是否消耗{0}金钱和{1}潜能将玲珑玉令提升到{3}级

# 阵营活动随机匹配（5380 - 5400）
CAMP_RANDOM_FIT_NOTIFY						= 5380			# 随机阵营战场将于20:00开启，请30级及以上的玩家做好准备。
CAMP_RANDOM_FIT_START 						= 5381			# 随机阵营战场已开启，请30级及以上的玩家前往凤鸣城萧炎处报名参加。
CAMP_RANDOM_FIT_END  						= 5382			# 随机阵营战场已关闭，感谢大家参与，请留意下次活动时间。
CAMP_RANDOM_FIT_NOT_DEGREE					= 5383			# 本周战场次数已满，无法匹配。
CAMP_RANDOM_FIT_NOT_CAPTAIN					= 5384			# 请退出队伍或由队长报名。
CAMP_RANDOM_FIT_NOT_CAMP					= 5385			# 队伍中有非本阵营玩家，无法匹配。
CAMP_RANDOM_FIT_DIFF_DEGREE					= 5386			# 队伍成员相同战场次数不足，无法匹配。
CAMP_RANDOM_FIT_OFFLINE						= 5387			# 队伍中有离线成员，无法匹配。
CAMP_RANDOM_FIT_LEVEL						= 5388			# 队伍中有成员不在同一等级段，无法匹配。
CAMP_RANDOM_FIT_DIE							= 5389			# 队伍中有成员处于死亡状态，无法匹配。
CAMP_RANDOM_FIT_FAR							= 5390			# 本队伍中有成员距离过远，无法匹配。
CAMP_RANDOM_FIT_LEAVE						= 5391			# 队伍中有成员离队，取消匹配。
CAMP_RANDOM_FIT_MEB_OFFLINE					= 5392			# 队伍中有成员离线，取消匹配
CAMP_RANDOM_FIT_CANCEL						= 5393			# 匹配终止。	

JADE_UP_GRADE								= 5394			# 玲珑玉令升级{0}级
CANOT_ENTER_PET_FENCE						= 5395			# 兽栏已满，无法入栏
CANNOT_PRAY_AS_NO_ITEM						= 5396			# 无法祈福，祈福香不够
CANNOT_GETSALARY_AS_CD_TIME					= 5397			# 今日已领取过俸禄了，无法再次领取
COST_MONEY_POTENTIAL_GET_JADE				= 5398			# 是否消耗{0}金钱与{1}潜能领取一块玲珑玉令
CANNOT_UPGRADE_JADE_MAX_LEVEL				= 5399			# 玲珑玉令已提升到最高级，无法继续升级
POTENTIAL_NO_EMOUGHT						= 5400			# 潜能不足
CANOT_BUY_ITEM_JADE_LEVEL_DOWN				= 5401			# 您的玲珑玉令等级太低，无法购买该商品
COST_MONEY_REFLASH_LHMJ_SHOP				= 5402			# 是否消耗{0}金钱刷新一次商店中的货物
OCCUPY_BUILD_FAILURE						= 5432			# 该地基已被其他玩家占领，请重新探索

COMPOSE_TRIPOD_SUCCESS						= 5408			# 乾坤鼎中炼制的{0}已炼制成功，请回到洞府储物柜取出炼制好的道具
COMPOSE_TRIPOD_FAIL							= 5409			# 乾坤鼎中炼制的{0}已经打造失败。
PLAYER_GET_LING_NENG						= 5410			# 获得灵能{0}
PLAYER_COST_LING_NENG						= 5411			# 失去灵能{0}
DONG_FU_NOT_BELONG_TO_PLAYER				= 5439			# 该洞府不属于你
DONG_FU_OTHER_BUILD_LEVEL_LOW				= 5440			# 洞府中部分建筑等级过低，无法升级灵泉 
DONG_FU_LINGQUAN_LEVEL_LOW					= 5441			# 灵泉等级过低， 无法升级
DONG_FU_BUILD_IS_UPGRADING					= 5442			# 有建筑正在升级中
LING_TIAN_LEVEL_LOW_NOT_PLANT				= 5461			# 灵田等级过低，该灵田尚未开发
LING_TIAN_PLANT_SUCCESS						= 5462			# 种植成功
LING_TIAN_COLLECTION_SUCCESS				= 5463			# 采集成功
BUILD_NEED_PSIONIC_NOT_ENOUGH_LN			= 5434			# 灵能不足
CHECK_POTENTIAL_NO_EMOUGHT					= 5400			# 潜能不足
BUILD_DONGFU_NOT_ENOUGH_DATA				= 5443			# {0}不足，无法建造
BUILD_UPGRADE_NOT_ENOUGH_DATA				= 5444			# {0}不足，无法升级
DONG_FU_IS_IN_PROGRESS						= 5445			# 洞府正在建造中

# 练兵场争夺战
TRAIN_SOLDIER_GROUND_DECLARWAR_MSG 		 	= 5420			# 宣战提示
TRAIN_SOLDIER_GROUND_DECLARWAR_SURE 		= 5421			# 争夺确认提示

# 天兵营兵升级提示
BARRACKS_UP_LEVEL_MSG 						= 5428			# 兵种只能升至{0}!其他士兵可继续分配经验
BARRACKS_UP_MAX_LEVEL_MSG 					= 5429			# 兵种最高升至6级，其他士兵可继续分配经验！

OPEN_BF_FAIL_AS_NOT_ENOUGH_LN				= 5430			# 灵能不足，无法开启阵图

LHMJ_CALL_MAX_GHOST							= 5431			# 同时最多可以召唤出{0}个傀儡
LHMJ_CANNOT_CALL_GHOST_IN_SELF_SPACE		= 5433			# 您不能在自己的洞府中召唤傀儡作战

LHMJ_SYMBOL_JADE_ONLY_USE_SELF_SPACE		= 5435			# 符玉只能用于防守自己的洞府，此处无法使用
LHMJ_SYMBOL_JADE_HAS_EMOUGH					= 5436			# 可放置符玉已达上限，无法放置更多符玉

TRAIN_SOLDIER_GROUND_NO_OCCUPY				= 5452			# 练兵场为被占领
TRAIN_SOLDIER_GROUND_NO_BELONGTO			= 5453			# 练兵场不归宿玩家
TRAIN_SOLDIER_GROUND_NO_LOWER				= 5454			# 低级练兵场不能领取
TRAIN_SOLDIER_GROUND_HAS_GET				= 5455			# 已经领取了物品
TRAIN_SOLDIER_GROUND_QUEST_FULL				= 5456			# 一天练兵任务不超过20个
TRAIN_SOLDIER_GROUND_NO_ITEM				= 5457			# 没有练兵令，解不了任务



LHMJ_BUILD_IS_FULL							= 5466			# 灵气罗盘检测到，本场景内，所有洞府福地均被占领，已无法搜索到洞府。

ACTIVATION_KEY_ERROR						= 5467			# 输入的礼包码有误，请重新输入
ACTIVATION_KEY_HAS_USED						= 5468			# 礼包码已经激活过
ACTIVATION_KEY_USE_SUCCESS					= 5469			# 礼包码激活成功。
ACTIVATION_KEY_ACCOUNT_HAS_USED				= 5470			# 您已激活过礼包码
ACTIVATION_KEY_NO_ROLE						= 5972			# 请创建好角色后，再来领取礼包



LHMJ_HAS_NOT_DONGFU							= 5471			# 你已没有洞府，无法返回洞府
PET_GET_EXT									= 5472			# 幻兽获得经验

BUILD_LEVEL_NO_ENOUGH						= 5506			# 工坊等级不足，无法打造此装备
CANNOT_COMPOSE_OTHER_PROFESSION				= 5507			# 您无法打造其他职业的装备

TTT_HAS_CHALLENGE_TODAY						= 5509			# 每日只能挑战一次通天塔

ACTIVITY_COPY_SPACE_FAIL_TIMES				= 5543			# 副本次数不足，无法进入。
ACTIVITY_COPY_SPACE_FAIL_SOMEONE_TIMES		= 5544			# 队伍成员xxx、xxx、xxx副本次数不足，无法进入。
ACTIVITY_COPY_SPACE_CLOSE					= 5527 			# 活动未开启，无法进入

#CST-11386 帮会争霸消息
BHZB_TONG_SIGN_UP_NOTICE 					= 5511 			# 帮会争霸已开启报名，请各帮帮主前往帮会领地报名参加，报名截止时间为周五晚24:00，正式活动将于周日20：00开启
BHZB_TONG_SIGN_END_NOTICE					= 5512 			# 帮会争霸报名已截止，请等待周六早上8:00公布最终获得参赛资格的帮会名单。
BHZB_TONG_JOIN_SUCCESS						= 5513			# 恭喜{0}{1}最终获得帮会争霸赛资格，请参赛帮会于周六24:00前提交最终参赛人员名单，并于周日20:00准时参加！
BHZB_TONG_START_FAIL						= 5514			# 很遗憾，由于没有帮派报名，本周帮会争霸取消开启
BHZB_TONG_START_NOTICE 						= 5515			# 帮会争霸将于20:00正式开启，请参赛的各帮会成员做好准备！活动入口：凤鸣城柳南
BHZB_TONG_START 							= 5516			# 帮会争霸已经正式开启，请参赛的各帮会成员尽快进入活动，开始争夺据点！活动入口：凤鸣城柳南。
BHZB_TONG_SUCCESS_FIRST 					= 5517			# 恭喜{0}{1}帮会荣获本周帮会争霸冠军，帮主{2}获得“{3}盟盟主”称号！
BHZB_TONG_SUCCESS_SECOND 					= 5518			# 恭喜{0}{1}帮会荣获本周帮会争霸冠军，帮主{2}获得“{3}盟副盟主”称号！
BHZB_TONG_SUCCESS_THIRD 					= 5967			# 恭喜{0}{1}最终荣获本周帮会争霸季军！

BHZB_TONG_CALL_TO_ATTACK_POINT 				= 5521			# 指挥官有令：命你队前往进攻{0}据点
BHZB_TONG_CALL_TO_PROTECT_POINT 			= 5522			# 指挥官有令：命你队前往防守{0}据点
BHZB_TONG_SIGN_UP_SUCCESS 					= 5523			# 报名成功!
BHZB_TONG_SIGN_UP_FORBID_TITLE 				= 5524			# 不是帮主或军师报名时：请帮主或军师前来报名。
BHZB_TONG_SIGN_UP_FORBID_TIME 				= 5525			# 不在报名时间段内时：现在不是报名时间
BHZB_TONG_SIGN_UP_FORBID_ALREADY 			= 5526			# 已报名时：已报名，请勿重复报名。
BHZB_TONG_NOT_START 						= 5527			# 不在活动时间内时：活动未开启，无法进入
BHZB_TONG_SIGN_UP_FORBID_LEVEL 				= 5529 			# 帮会等级不足2级时：帮会等级未达2级以上，无法报名
BHZB_TONG_SIGN_UP_FORBID_MONEY 				= 5530			# 帮会资金不足时：帮会资金不足，无法报名。
BHZB_TONG_SIGN_UP_FORBID_MEM_AMOUNT  		= 5531			# 名单成员数量不足时：争霸活动人员不足，无法报名。
BHZB_TONG_SIGN_UP_FORBID_MEMBER 			= 5536			# 你不是参赛人员，无法进入

BHZB_TONG_OCCUPY_POINT 						= 5519 			# @F{fc=c3}{0}@D帮会成功占领据点：@F{fc=c3}{1}@D！
BHZB_TONG_BE_OCCUPY_POINT 					= 5520			# @D本帮据点@F{fc=c3}{0}@D已被@F{fc=c3}{1}@D帮会攻占！
BHZB_TONG_POINT_BE_DECLARE 					= 5532			# @D本帮据点@F{fc=c3}{0}@D被敌方宣战，请军师迅速指挥人员回防！
BHZB_PLAYER_FORBID_IS_DECLARE				= 5537 			# 无法同时宣战多个据点。
BHZB_TONG_POINT_ENEMY_CANCEL 				= 5538			# 敌方已取消宣战。

BHZB_ATTACK_PVEPOINT 						= 5679			# {0}（帮派A）对{1}（据点名）发起进攻
BHZB_ATTACK_PVEPOINT_SUCCESS 				= 5680			# 恭喜{0}（帮派A）成功占领{1}（据点名）
BHZB_ATTACK_PVEPOINT_FAIL 					= 5681			# 很遗憾未能成功占领{1}（据点名)
BHZB_ATTACK_PVPPOINT  						= 5682			# {0}（帮派A）对{1}（帮派B）的{2}（据点名）发起进攻
BHZB_ATTACK_PVPPOINT_PROTECT_SUCCESS 		= 5683 			# 恭喜{0}（帮派A）成功守住{1}（据点名）
BHZB_ATTACK_PVPPOINT_PROTECT_FAIL  			= 5684			# 很遗憾未能成功守住{1}（据点名）

BHZB_POINT_STATE_DECLARE 					= 5685			# 该据点已被宣战
BHZB_POINT_FORBID_JOINATTACK				= 5686			# 参战人数已满
BHZB_POINT_FORBID_JOINPROTECT  				= 5687			# 回防人数已满
BHZB_POINT_STATE_DEFENSE 					= 5688			# 该据点正在布防中

BHZB_POINT_JOIN_ATTACK_OTHER_POINT 			= 5691			# 无法同时参战多个据点
BHZB_POINT_JOIN_PROTECT_OTHER_POINT 		= 5692			# 无法同时回防多个据点
BHZB_POINT_ALREADY_TO_JOIN_ATTACK 			= 5693			# 该据点争夺中，无法宣战
BHZB_POINT_ALREADY_TO_JOIN_PROTECT  		= 5694			# 该据点休整中，无法宣战
BHZB_POINT_DEFENSE_FORBID_JOIN_ATTACK 		= 5695			# 该据点未被宣战，无需回防
BHZB_POINT_DEFENSE_FORBID_JOIN_PROTECT 		= 5828			# 已回防，无法布防

BHZB_TEAM_OCCUPY_POINT_SUCCESS 				= 5888			# 队伍{0}成功占领据点{1}
BHZB_TEAM_OCCUPY_POINT_FAIL 				= 5889			# 很遗憾，队伍{0}未能成功占领据点{1}
BHZB_TEAM_PROTECT_POINT_SUCCESS 			= 5890			# 队伍{0}成功守住据点{1}
BHZB_TEAM_PROTECT_POINT_FAIL 				= 5891			# 很遗憾，队伍{0}未能成功守住据点{1}
BHZB_POINT_BE_DECLARE_BY_OTHER_TONG 		= 5892			# 本帮据点{0}已被{1}帮会宣战
BHZB_TEAM_ALL_MEMBER_OFF_LINE 				= 5894 			# 该队伍成员均不在线，派遣失败
BHZB_POINT_WAR_CALL_NOT_TEAM 				= 5895			# 当前地图此操作无效
BHZB_JUN_SHI_CANCEL_ORDER 					= 5898			# 军师已撤销指令
BHZB_NOT_JOIN_CANNOT_CHANGE_TEAM 			= 5899			# 非参赛人员无法编入队伍

LEAVE_BHZB_PVP_SPACE 						= 5830			# 离开帮会争霸PVPspace

BHZB_END_GLOBALWOLD_RANK					= 5965			# 恭喜{0}帮会在本月的帮会争霸中累计积分暂列{1}第一，总积分为{2}
BHZB_END_GLOBALWOLD_TO_JOIN_CAMP_WAR 		= 5966			# 本月帮会争霸已结束。恭喜{0}{1}帮会最终累计积分位列仙道第一，成为{2}最强帮会！将代表{3}阵营参加本月阵营争霸，与{4}最强帮会争夺天下第一帮的荣耀！ 

GROUND_ATTACK_SUCCESS						= 5548			# 恭喜xxx成功占领***
GROUND_DEFENSE_FAIL							= 5549			# 很遗憾未能成功守住***
GROUND_DEFENSE_SUCCESS						= 5558			# 恭喜xxx成功守住***
GROUND_ATTACK_FAIL							= 5559			# 很遗憾未能成功占领***

TONG_GET_MONEY_BY_SELF						= 5551			# 获得帮会资金
BHLD_TONG_WAR_SUCCESS						= 5552			# XXX帮会成功抢下XXX帮会的战旗，获得此次争夺战的胜利。
TONG_BUILD_UPGRADE							= 5553			# 帮会建筑升级

DF_BUILD_IS_DESTROY							= 5556			# 建筑已损坏，无法升级

TRAIN_SOLDIER_GROUND_DECLAR_FORBIG_TRAINTYPE= 5560 			# 未占领初级练兵场，无法宣战更高级练兵场
TRAIN_SOLDIER_GROUND_DECLAR_FORBIG_MONEY 	= 5561			# 金钱不足xxx，无法宣战更高级练兵场
TRAIN_SOLDIER_GROUND_DECLAR_WAR 			= 5562 			# xxx对xxx的xxx发动进攻

LHMJ_JYWF_NOTICE_ALL 						= 5570  		#@F{fc=c4}{0}@D红星高照，在@F{fc=c19}{1}@D中触发机缘，有缘进入@F{fc=c19}{2}@D中探索。
LHMJ_JYWF_BACK 								= 5571 			#@F{fc=c4}{0}@D已从@F{fc=c19}{1}@D中满载而归，金光外露羡煞旁人。
LHMJ_JYWF_NOTICE_SELF						= 5572 			#恭喜您触发了仙缘，有缘进入@F{fc=c19}{0}@D中，机缘难得，请君珍惜。

MILITARY_RANK_LEVEL_NO_ENOUGH				= 5577			# 您的军衔等级太低，无法购买该道具

#好东西触发提示
ITEM_ADD_IN_SPACE_WIN_BOSS					= 5582			#恭喜@F{fc=c4}{0}@D在挑战@F{fc=c19}{1}@D的@F{fc=c8}{2}@D时获得了极品道具@F{fc=c4}{3}@D，有此臂助，前路可期
ITEM_ADD_IN_SPACE							= 5583			#恭喜@F{fc=c4}{0}@D在挑战@F{fc=c19}{1}@D时获得了极品道具@F{fc=c4}{2}@D，有此臂助，前路可期。
ITEM_ADD_IN_SPACE_WIN_BOSS_IN_TONGTIANTA	= 5584			#恭喜@F{fc=c4}{0}@D在挑战通天塔中突破极限，在挑战超过自身等级@F{fc=c8}{1}@D级的@F{fc=c8}{2}@D时，成功击败@F{fc=c19}{3}@D，并获得了极品道具@F{fc=c4}{4}@D，有此臂助，前路可期。
ITEM_ADD_IN_SPACE_OPEN_BOX					= 5585			#恭喜@F{fc=c4}{0}@D在开启@F{fc=c8}{1}@D，获得了极品道具@F{fc=c4}{2}@D，有此臂助，前路可期。
ITEM_ADD_IN_SPACE_WIN_NO_ONE				= 5586			#恭喜@F{fc=c4}{0}@D在至尊争霸战中傲视群雄，获得了极品道具奖励@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_IN_SPACE_WIN_NO_TWO				= 5587			#恭喜@F{fc=c4}{0}@D在至尊争霸战中屈居亚席，获得了极品道具奖励@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_IN_SPACE_WIN_NO_THREE				= 5588			#恭喜@F{fc=c4}{0}@D在至尊争霸战中位列第三，获得了极品道具奖励@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_BUY_JIYUAN							= 5589			#恭喜@F{fc=c4}{0}@D机缘巧合之下在凤鸣城@F{fc=c19}{1}@D，购买了极品道具@F{fc=c4}{2}@D，有此臂助，前路可期。
ITEM_ADD_BUY_MYSTERIOUS						= 5590			#恭喜@F{fc=c4}{0}@D，巧遇神秘商人，并在神秘商人处购买了极品道具@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_DAZAO								= 5591			#恭喜@F{fc=c4}{0}@D，历经千锤百炼，终于打造出了圣阶道具@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_LIANZHI							= 5592			#恭喜@F{fc=c4}{0}@D，历经千辛万苦，终于炼制出了圣阶道具@F{fc=c4}{1}@D，有此臂助，前路可期。
ITEM_ADD_BY_LUNHUIMIJING					= 5593			#恭喜@F{fc=c4}{0}@D，在轮回秘境中捕捉到了极品道具@F{fc=c4}{1}@D，有此臂助，前路可期。

#游戏付费时间提示
GAME_TIME_HAS_USED							= 5594			# 您的游戏时间已用完，请及时续费
GAME_TIME_BLAN_HALF_HOUR					= 5595			# 游戏时间只剩30分钟，请及时续费
GAME_TIME_TEN_MINUTES						= 5596			# 游戏时间只剩10分钟，请及时续费
GAME_TIME_TEN_SECONDS						= 5597			# 游戏时间只剩余1分钟，若不及时续费，会影响到后续使用。
GAME_TIME_ALL_HAS_USED						= 5598			# 游戏时间已全部用完，请先续费后才能继续游戏
GAME_TIME_START_BILLING_LEVEL				= 5834			# 您已达到{0}级，若要继续体验后续内容，请及时充值游戏时间。
GAME_TIME_ADD_TIME							= 5854			# 恭喜，您已获得{0}分钟游戏时间，祝您游戏愉快，早日问鼎洪荒。

MYSTERIOUS_SHOP_ZHAOHUAN_NPC				= 5599			# 恭喜@F{fc=c4}{0}@D在打开神秘宝盒的时候，天降奇缘，成功召唤出了携带无数珍宝的@F{fc=c4}东方聚宝道人@D。
MYSTERIOUS_SHOP_SELL_ALL					= 5600			# 神秘商人已出售完所有宝物，并返回虚空之中，等待有缘人下一次的召唤
MYSTERIOUS_SHOP_TIMES_UP					= 5927			# 时间已到，我也该走了，若有缘下次再见。

CAN_NOT_SET_BATTERY_CUR_STATE				= 5601			# 当前状态下，无法放置洞府防御器械
CAN_NOT_SET_BATTLE_CUR_STATE				= 5602			# 当前状态下，无法更换阵图
HAS_NOT_ENOUGHT_LING_NENG_CLOSE_BATTLE		= 5607			# 您的灵能不足，已无法维持阵图运转，阵法已关闭。

LHMJ_CHANGELLENGE_NOT_OPEN					= 5642			# 洞府战尚未开启，无法进入对方洞府
LHMJ_PLUNDER_NOT_OPEN						= 5643			# 洞府掠夺战尚未开启，无法进入对方洞府

#练兵场
LBC_GOTO_LBC_LOW 							= 5644 			#未被占领的初级练兵场无需宣战即可立刻前往争夺。你的已有练兵场将视为放弃占领。是否确定前往争夺！
LBC_NOT_DECLARE_TIME 						= 5645 			#已被占领的练兵场需要在周二或者周五20:00-21:00时间段内发起宣战。目前不在时间段内，不可宣战！
LBC_IS_DECLARE								= 5646 			#是否对当前练兵场发起宣战？宣战后XX月XX日20:00正式开启争夺！
LBC_DECLARE_SUCCEED 						= 5647 			#你对XXX练兵场发起的宣战生效 XX月XX日20:00正式开启争夺！
LBC_BE_DECLARED 							= 5648 			#你的练兵场已被他人宣战 XX月XX日20:00正式开启争夺！	
LBC_START_FIGHT 							= 5649 			#练兵场争夺战正式开启 勇士是否前往争夺练兵场！	
LBC_ENTER_FIGHT 							= 5650 			#你的练兵场正在争夺中，是否立即前往？
LBC_LOST_ON_LOGOFF 							= 5651 			#练兵场争夺期间你不在线，你的练兵场已被他人占领！
LBC_DEFENCE_SUCCEED    						= 5652 			#练兵场进攻方未能抢夺你的练兵场，你继续拥有该练兵场！
LBC_CONDITION_NO_LBC	 					= 5655 			#你未占领xx级练兵场
LBC_CONDITION_NO_MONEY 						= 5656 			#你的金钱不足XXX
LBC_CONDITION_NO_SOLDIER 					= 5657 			#你xx级以上的士兵不足xx个
LBC_CONDITION_MEMBER_AMOUNT 				= 5660 			#争夺中级和高级练兵场需要组成三人队伍！
LBC_OCCUPY_SUCCEED 							= 5661 			#恭喜你，成功占领XXX练兵场！
LBC_OCCUPIED_BY_OTHERS 						= 5662 			#该练兵场已被他人抢先占领！

#练兵场任务
LBC_TASK_PROCESS_LIMITED 					= 5554 			#每日只能练兵两次，你的当前练兵次数不足！

#帮会掠夺战
TONG_PLUNDER_IS_NOT_LEADER					= 5623			# 您不是帮主，无法对其他帮会发起掠夺。
TONG_PLUNDER_LEVEL_NOT_ENOUGH				= 5624			# 您的帮会等级不足2级，无法参加帮会掠夺，请提升帮会等级再来参加。
TONG_PLUNDER_MONEY_NOT_ENOUGH				= 5625			# 您的帮会资金低于维持帮会最低资金数,无法参加帮会掠夺,请补充帮会资金再来
TONG_PLUNDER_ACTIVITY_NOT_ENOUGH			= 5626			# 您的帮会活跃度不足，无法参加帮会掠夺，请补充帮会活动度再来参加。
TONG_PLUNDER_LOCKED_BY_OTHER				= 5627			# 您的帮会已经被其他帮会锁定掠夺，无法参加帮会掠夺。
TONG_PLUNDER_TARGET_LEVEL_NOT_ENOUGH		= 5628			# 该帮会的帮会等级不足2级，无法对该帮会发起掠夺。请选择其他帮会进行掠夺。
TONG_PLUNDER_TARGET_MONEY_NOT_ENOUGH		= 5629			# 该帮会的帮会资金不足，无法对该帮会发起掠夺。请选择其他帮会进行掠夺。
TONG_PLUNDER_TARGET_ACTIVITY_NOT_ENOUGH		= 5630			# 该帮会的活跃度不足，无法对该帮会发起掠夺。请选择其他帮会进行掠夺。
TONG_PLUNDER_LEVEL_DIFF_TOO_BIG				= 5631			# 本帮会与该帮会的等会等级差大于2级，无法对该帮会发起掠夺。请选择其他帮会进行掠夺。
TONG_PLUNDER_TARGET_LOCKED_BY_OTHER			= 5632			# 该帮会已经被其他帮会锁定掠夺，无法对该帮会发起掠夺。请选择其他帮会进行掠夺。
TONG_PLUNDER_CAN_NOT_ENTER					= 5633			# 很遗憾，你没有被帮主选做此次掠夺战的参加人员，不能进入活动场地
TONG_PLUNDER_BE_PLUNDER_CHALLENGE_NOTIFY	= 5634			# {0}帮会对我帮发起了掠夺，即将于{1}年{2}月{3}日{4}正式开战
TONG_PLUNDER_CHALLENGE_NOTIFY				= 5635			# 我帮已对{0}帮会发起掠夺，即将于{1}年{2}月{3}日{4}正式开战
TONG_PLUNDER_CHALLENGE_NOTIFY_TO_LEADER	= 5636			# 您对{0}帮会发起了掠夺战斗
TONG_PLUNDER_NEED_SELECT_TONG				= 5836			# 请您选择一个帮会发起掠夺
TONG_PLUNDER_TONG_NOT_SIGN_UP_ACTIVE		= 5837			# 您的帮会没有报名参加此次掠夺战，无法进入活动场地。
TONG_PLUNDER_CAN_NOT_CHANGE_MEMBER		= 5838			# 掠夺战已经开始，您无法更改参加帮会掠夺的成员
TONG_PLUNDER_MEMBER_NUM_IS_FULL			= 5839			# 参加掠夺战人员数量已满，无法添加新人员。
TONG_PLUNDER_HAS_OPENED_BOX					= 5840			# 您已经开启过一个奖励宝箱了，请将宝箱留给其他人。
TONG_PLUNDER_CAN_NOT_OPEN_BOX				= 5841			# 您的帮会没有获得此次掠夺战的胜利，无法开启宝箱。
TONG_PLUNDER_ADD_MEMBER_SUCCESS			= 5842			# 成功设置{0}为帮会掠夺战斗成员。
TONG_PLUNDER_REMOVE_MEMBER_SUCCESS		= 5843			# 将{0}移出帮会掠夺战斗成员。
TONG_PLUNDER_MEMBER_ALREADY_ADD			= 5844			# {0}已经在帮会掠夺战斗成员中，无需再次设置出战。
TONG_PLUNDER_REVIVE_NUM_USE_UP				= 5850 			# 你的死亡次数超过{0}次，无法继续参战，即将离开活动场地！
TONG_PLUNDER_ENTER_NUM_USE_UP				= 5948			#您的出战次数已经用完，无法再次进入战场。
TONG_PLUNDER_ENTER_TIME_OUT					= 5949			#您错过了进入战场的时间，无法进入战场。
TONG_PLUNDER_CAN_NOT_ADD_MEMBER			= 5970			#帮会没有参与掠夺活动，无法添加活动人员
TONG_PLUNDER_ACTIVITY_END						= 5971			#本场战斗胜负已分晓，无法进入战场


#招募士兵
BARRACKS_ADD_SUCCESS	= 5637	#您成功招募了一个{0}级{1}
ITEM_ADD_BARRACKS_AMOUNT_TOO_MAX	= 5638	#您天兵营的{0}人数已达上限，无法使用道具招募{1}
BARRACKS_SOLDIER_ALL_DIE			= 5950	#你已经没有可以出战的部队了！

TONG_MONEY_GET_MONEY						= 5696			# 帮会

# 洞府
DONG_FU_COVER_BEING_ATTACK					= 5815			# {0}正在进攻我方保护罩
DONG_FU_COVER_DESTROY_PROTECT				= 5816			# 攻方把罩子 攻破
DONG_FU_COVER_DESTROY_ATTACK				= 5817			# 把守方罩子 攻破
DONG_FU_ENTER_BY_ATTACK						= 5818			# {0}已进入我方洞府
DONG_FU_BUILD_BEING_ATTACK					= 5823			# 我方{0}建筑被攻击
DONG_FU_OCCUPY_BY_HASDF						= 5824			# 恭喜您占领了{0}的洞府
DONG_FU_OCCUPY_BY_JADE						= 5825			# 恭喜您占领了{0}的洞府，背包的玲珑玉令无效

#传承技能
CC_SKILL_BAR_MONEY_NOT_ENOUGH 				= 5806			# 您的金钱不足，无法开启该栏位
CC_SKILL_BAR_POTENTIAL_NOT_ENOUGH			= 5807			# 您的潜能不足，无法开启该栏位
CC_SKILL_BAR_IS_OPEN						= 5808			# 是否消耗{}点的潜能与{}金钱开启该栏位
CC_SKILL_BAR_IS_NOT_FENG_MING				= 5809			# 您未获得凤鸣之主称号，无法开启该栏位
CC_SKILL_FULL_LEVEL							= 5833			# 传承技能已满级，无法吞噬玉玦
CC_SKILL_IS_DEVOUR							= 5835			# 吞噬玉玦包含一块{0}完整玉玦{1}级，是否确定吞噬

# 神兵王道
PLAYER_GET_KIND_EQUIP						= 5859			# 恭喜您，经过不懈努力，终于获得神介装备{0}
GLOBAL_PLAYER_GET_KIND_EQUIP				= 5960			# 天道酬勤，{0}经过不懈努力，成功蕴养出神介装备{1}

# 攻城战
GCZ_SIGN_UP_FORBID_LEVEL 					= 5866			# 报名攻城战需达到{0}级，无法报名
GCZ_SIGN_UP_FORBID_SOLDIER_AMOUNT 			= 5867			# 您的士兵数量不足{0}个，无法报名
GCZ_SIGN_UP_SUCCESS 						= 5868			# 您已经成功报名 {0}点{1}分 场次的攻城战副本，请准时参加
GCZ_SIGN_UP_FORBID_NUMBER_PERSON 			= 5869			# 当前场次人数已满，您无法报名参加 {0}点{1}分场次的攻城战副本。
GCZ_ALREADY_SIGN_UP							= 5870			# 您已经报名了一场攻城战，无需再次报名。
GCZ_TEAMCAPTAIN_CANCEL_MATCH 				= 5872			# 队长取消攻城战组队匹配。
IS_JOIN_GCZ_MATCH 							= 5873  		# 是否进入攻城战队伍匹配
GCZ_ENTER_SPACE_FORBID_CLOSE 				= 5874			# 当前副本已关闭，无法进入副本。
GCZ_MATCH_SUCCESS_IS_TO_ENTER 				= 5875			# 是否立即进入攻城战副本？
GCZ_ENTER_SPACE_IS_GIVE_UP 					= 5876			# 是否放弃进入攻城战副本资格？
IS_KICK_OUT_NOT_JOIN_GCZ_TO_MATCH 			= 5877			# 是否将没有资格的队员移除队伍，进行攻城战组队匹配？
IS_LEAVE_TEAM_TO_MATCH 						= 5878			# 队长没有参加本场攻城战资格，是否离开队伍进行攻城战组队匹配？
GCZ_MATCH_FORBID_TEAM_MEMBER_CHANGE 		= 5879			# 队伍成员发生变化，取消匹配。
GCZ_MATCH_FORBID_TEAM_MEMBER_OFFLINE 		= 5880			# 队伍存在离线队员，无法匹配。
GCZ_MATCH_CANCEL_BY_OFFLINE_MEMBER 			= 5881			# 队伍成员{0}处于离线状态，取消匹配。
GCZ_ENTER_FORBID_NOT_MATCH					= 5882			# 提示队伍没通过匹配，无法进入副本
GCZ_MATCH_FORBID_SIGNUP 					= 5883			# 你没有报名当前场次的攻城战，无法匹配
GCZ_ENTER_FORBID_SIGNUP 					= 5884			# 你没有报名当前场次的攻城战，无法进入副本。
GCZ_IS_ALREADY_TO_MATCH 					= 5885			# 正在匹配中，无需再次操作。
GCZ_MATCH_FORBID_MATCH_SUCCESS 				= 5938			# 已匹配成功无需再匹配


#帮会宝箱分配
DROPBOX_ALLOCATION_FORBID					= 5893			#帮会争霸期间无法修改宝箱分配方式
DROPBOX_AUCTION_ABANDOM						= 5904			#是否放弃竞拍@F{fc=c4}{0}@D？
DROPBOX_AUCTION_NO_ENOUGH_MONEY				= 5905			#您的出价高出您背包中携带的金币。
DROPBOX_AUCTION_LOW_MONEY					= 5906			#您的出价低于最低出价，无法竞拍。
DROPBOX_AUCTION_ABANDOM_ALL					= 5907			#是否放弃所有拍品的竞拍资格？
DROPBOX_TONG_GET_ITEM						= 5910			#@F{fc=c4}{0}@D获得了{1} ×{2} 
DROPBOX_AUCTION_MAX_ROLE					= 5913			#您已是最高出价者，无法再次出价
TONG_DROPBOX_LEADER_ALLOCATION				= 5918 			#@F{fc=c4}{0}@D通过帮会分配获得了{1} ×{2}
DROPBOX_AUCTION_GET_ITEM					= 5919 			#@F{fc=c4}{0}@D花费@F{fc=c39}{1}@D金币拍得了{2}

ONLY_HIGH_DF_CAN_ENTER						= 5924			# 只有高级洞府的兽栏才能驯养神兽与圣兽

#多人载具
VEHICLE_INVITE_TO_MOUNT					= 5929			#邀请你共同骑乘，是否接受？
VEHICLE_TO_REFUSE_INVITE					= 5930			#拒绝了你的邀请
VEHICLE_APPLY_TO_MOUNT					= 5931			#申请共同骑乘，是否接受？
VEHICLE_TO_REFUSE_APPLY						= 5932			#拒绝了你的申请
VEHICLE_TO_MOUNT_CANNOT_GOSSIP			= 5933			#骑乘状态无法交互
VEHICLE_TO_MOUNT_CANNOT_INVITE			= 5934			#对方处于骑乘状态，邀请失败
NO_VEHICLE_CANNOT_APPLY					= 5935			#对方没有多人坐骑，申请失败
VEHICLE_NUM_TO_REACH_FULL					= 5936			#共同骑乘人数已满，申请失败
VEHICLE_BEYOND_INTERACTIVE_DISTANCE		= 5952			#距离过远

DF_BUILD_IS_REPAIRING					= 5953			# 有建筑正在修改中

LHMJ_DF_BEING_OCCUPY					= 5955			# 洞府被**占领

CANNOT_ENTER_MAGICMAZESPACE_FORBIG_PLAYEAMOUNT = 5957	# 由于人数限制禁止进入幻阵迷宫

LHMJ_SYS_AGAIN_PLUNDER					= 5958			# 系统已默认同意了@F{fc=c44}{0}@D向您发起的洞府掠夺战挑战申请，因为该申请已超过@F{fc=c8}3@D小时或洞府掠夺战报名已截止。
LHMJ_SYS_AGAIN_CHALLENGE				= 5959			# 系统已默认同意了@F{fc=c44}{0}@D向您发起的洞府争夺战挑战申请，因为该申请已超过@F{fc=c8}3@D小时或洞府争夺战报名已截止。