# -*- coding: utf-8 -*-

#-------------------------------------------------------------------
#日志类型
#-------------------------------------------------------------------
LOG_TYPE_QUEST		= 1	#任务
LOG_TYPE_ITEM		= 2	#物品
LOG_TYPE_COIN		= 3	#金钱
LOG_TYPE_PRO			= 4	#属性
LOG_TYPE_EQUIP		= 5	#装备
LOG_TYPE_RELATION	= 6	#人物关系
LOG_TYPE_PET			= 7	#宠物
LOG_TYPE_TRADE		= 8	#交易
LOG_TYPE_MAIL		= 9	#邮件
LOG_TYPE_TONG		= 10	#帮会
LOG_TYPE_SKILL		= 11	#技能
LOG_TYPE_RECHARGE	= 12	#充值
LOG_TYPE_ACCOUNT	= 13	#账号
LOG_TYPE_ROLE		= 14	#角色
LOG_TYPE_VEND		= 15	#摆摊
LOG_TYPE_ACT_COPY		= 16	#活动、副本
LOG_TYPE_ONLINE		= 17	#玩家在线数据
LOG_TYPE_COST		= 18	#消费表
LOG_TYPE_PROP		= 19	#道具
LOG_TYPE_ROLE_UP_LEVEL		= 20	#道具
LOG_TYPE_ACTIVE_RECORD		= 21	#活动记录
LOG_TYPE_ITEM_LOAD		= 22	#物品加载日志




_LOG_TABLES = {
	LOG_TYPE_QUEST:		"Log_Quest",
	LOG_TYPE_ITEM:		"Log_Item",
	LOG_TYPE_COIN:		"Log_Coin",
	LOG_TYPE_PRO:		"Log_Pro",
	LOG_TYPE_EQUIP:		"Log_Equip",
	LOG_TYPE_RELATION:	"Log_Relation",
	LOG_TYPE_PET:			"Log_Pet",
	LOG_TYPE_TRADE:		"Log_Trade",
	LOG_TYPE_MAIL:		"Log_Mail",
	LOG_TYPE_TONG:		"Log_Tong",
	LOG_TYPE_SKILL:		"Log_Skill",
	LOG_TYPE_RECHARGE:	"Log_Recharge",
	LOG_TYPE_ACCOUNT:	"Log_Account",
	LOG_TYPE_ROLE:		"Log_Role",
	LOG_TYPE_VEND:		"Log_Vend",
	LOG_TYPE_ACT_COPY:	"Log_ActCopy",
	LOG_TYPE_ONLINE:		"Log_Online",
	LOG_TYPE_COST:		"Log_Cost",
	LOG_TYPE_PROP:		"Log_Prop",
	LOG_TYPE_ROLE_UP_LEVEL:		"Log_RoleUpLevel",
	LOG_TYPE_ACTIVE_RECORD:		"Log_ActRecord",
	LOG_TYPE_ITEM_LOAD:		"Log_ItemLoad",
	}
	
	
_LOG_FIELD_ = {
	LOG_TYPE_QUEST:		"updatetime, action, roleDBID, roleName, questID, questName, roleLevel, roleGrade, useTime",
	LOG_TYPE_ITEM:		"updatetime, action, roleDBID, roleName, itemID, itemUid, itemName, itemNum, param1, param2, param3, itemData",
	LOG_TYPE_COIN:		"updatetime, action, accountDBID, roleDBID, roleName, oldValue, newValue, reason, orders",
	LOG_TYPE_PRO:		"updatetime, action, roleDBID, roleName, param1, param2, param3, param4, param5",
	LOG_TYPE_EQUIP:		"updatetime, action, roleDBID, roleName, itemID, itemUid, itemName, itemNum, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, equipData",
	LOG_TYPE_RELATION:	"updatetime, action, roleDBID, roleName, tRoleDBID, tRoleName, param1, param2 , param3",
	LOG_TYPE_PET:		"updatetime, action, roleDBID, roleName, petName,petUname, petUid, petQuality, petLevel, petData, param1, param2, param3, param4, param5, param6,param7,param8, param9, param10",
	LOG_TYPE_TRADE:		"updatetime, action, roleDBID, roleName, param1, param2, param3, param4, param5, param6, param7, param8, param9, itemData",
	LOG_TYPE_MAIL:		"updatetime, action, senderName, receiverName, mailType, title, money, itemData, param1, param2",
	LOG_TYPE_TONG:		"updatetime, action, tongDBID, tongName, param1, param2, param3, param4, param5, param6, param7",
	LOG_TYPE_SKILL:		"updatetime, action, roleDBID, roleName, skillID, param1, param2, param3, param4, param5, param6",
	LOG_TYPE_RECHARGE:	"updatetime, accountDBID, accountName, rechargeType, coinType, value, transactionID",
	LOG_TYPE_ACCOUNT:	"updatetime, action, accountDBID, accountName, param1, param2, param3",
	LOG_TYPE_ROLE:		"updatetime, action, roleDBID, roleName, accountDBID, accountName, param1, param2, param3, param4, param5, blobParam1, blobParam2, blobParam3",
	LOG_TYPE_VEND:		"updatetime, roleDBID, roleName",
	LOG_TYPE_ACT_COPY:	"updatetime, action, actCopyType, actCopyName, roleDBID, roleName, param1, param2, param3",
	LOG_TYPE_ONLINE:		"update_time, lineNum, onlineRoleNum, onlineMacNum",
	LOG_TYPE_COST:		"update_time, account_id, gid, buy_item_id, buy_item_name, item_price, buy_item_amount, gold_coin_cost, gold_coin_left, bind_coin_cost, bind_coin_left, level",
	LOG_TYPE_PROP:		"update_time, line, account_id, gid, level, iid, item_name, memo",
	LOG_TYPE_ROLE_UP_LEVEL:		"update_time, account_id, gid, level, time_used, last_lv_up",
	LOG_TYPE_ACTIVE_RECORD:		"update_time, line, action, account_id, gid, level, bonus_type, bonus_name, start_time, time_used, action_status",
	LOG_TYPE_ITEM_LOAD:		"update_time, itemID",
}


