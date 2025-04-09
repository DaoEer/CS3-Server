# -*- coding: utf-8 -*-
from .LogDefine import *

LOG_TYPE_QUEST = "Log_Quest"
LOG_TYPE_ITEM = "Log_Item"
LOG_TYPE_COIN = "Log_Coin"
LOG_TYPE_PRO = "Log_Pro"
LOG_TYPE_EQUIP = "Log_Equip"
LOG_TYPE_RELATION = "Log_Relation"
LOG_TYPE_PET = "Log_Pet"
LOG_TYPE_TRADE = "Log_Trade"
LOG_TYPE_MAIL = "Log_Mail"
LOG_TYPE_TONG = "Log_Tong"
LOG_TYPE_SKILL = "Log_Skill"
LOG_TYPE_RECHARGE = "Log_Recharge"
LOG_TYPE_ACCOUNT = "Log_Account"
LOG_TYPE_ROLE = "Log_Role"
LOG_TYPE_VEND = "Log_Vend"
LOG_TYPE_ACT_COPY = "Log_ActCopy"

QUERY_CONDITION = " where %s "
QUERY_RANGE = " limit %s, %s "

SQL_QUERY_ROLE_SKILL_LEAEN = "select id, roleDBID, roleName, skillID, param1, updateTime, param2, param3, param4, param5 from %s where action = %s " \
	% (LOG_TYPE_SKILL, LT_SKILL_LEARN)
SQL_QUERY_ROLE_UPGRADE = "select id, roleDBID, roleName, param1, param2, param3 from %s where action = %s " % (LOG_TYPE_PRO, LT_PRO_LEVEL_UPGRADE)
SQL_QUERY_MAIL_RECORD = "select id, action, senderName, receiverName, updateTime, title, param1, param2, param3 from %s " % LOG_TYPE_MAIL
SQL_QUERY_VEND_TRADE = "select id, roleDBID, roleName, updateTime, param6, param5, param7, param1, param2 from %s where param9 = %s and param7>0" \
	% (LOG_TYPE_TRADE, LT_TRADE_TYPE_VEND)
SQL_QUERY_TASK = "select id, roleDBID, roleName, roleLevel, questID, questName, action from %s " % LOG_TYPE_QUEST
SQL_QUERY_RECHARGE = "select id, accountDBID, accountName,transactionID, updateTime, rechargeType, coinType, value from %s " % LOG_TYPE_RECHARGE
SQL_QUERY_COST = "select roleName, oldValue, newValue from %s where action = %s and (ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0" % \
	(LOG_TYPE_COIN, LT_XIANSHI_CHANGE)
SQL_QUERY_ACCOUNT_LOCK_INFO = "select updateTime, action, param1, param2, param3 from %s where ((action = %s and param1 > %s) or (action = %s)) \
	and accountName = '%s'"
SQL_QUERY_ROLE_GAG_INFO = "select updateTime, action, param1, param2, param3, param4 from %s where ((action = %s and param2 > %s) \
	or (action = %s)) and roleName = '%s'"
