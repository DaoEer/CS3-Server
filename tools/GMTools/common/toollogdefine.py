# -*- coding: utf-8 -*-
#*****toollogdefine******

from . import csdefine



#------------------------------
#GM工具账号管理
#------------------------------
"""
USER_MGR_ADD = 1 #新建账号
USER_MGR_DEL = 2 #删除账号
USER_MGR_EDIT = 3 #编辑账号
USER_MGR_MODIFY_PWD = 4 #修改密码
"""
#编辑账号类型
USER_MGR_EDIT_TYPE_LEVEL_MODIFY = 1 #修改等级

#------------------------------
#游戏账号管理
#------------------------------
"""
ACCOUNT_MGR_QUERY = 1 #查看账号信息
ACCOUNT_MGR_EXPORT_ROLE_INFO = 2 #导出角色信息
ACCOUNT_MGR_EXPORT_COST_DATA = 3 #导出消费排行
ACCOUNT_MGR_LOCK_ACCOUNT = 4 #封锁账号
ACCOUNT_MGR_UNLOCK_ACCOUNT = 5 #解封账号
ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP = 6 #账号托管
ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP_CANCEL = 7 #取消账号托管
"""

#------------------------------
#游戏角色管理
#------------------------------
"""
ROLE_MGR_KICK_ROLE = 1 #踢人
ROLE_MGR_QUERY_INFO = 2 #角色信息查询
ROLE_MGR_QUERY_ACTIVITY_PART = 3 #活动参与查询
ROLE_MGR_QUERY_COIN = 4 #货币查询
ROLE_MGR_QUERY_PET = 5 #幻兽查询
ROLE_MGR_QUERY_ITEM = 6 #道具查询
ROLE_MGR_FREEZE_ROLE = 7 #冻结角色
ROLE_MGR_UNFREEZE_ROLE = 8 #解冻角色
ROLE_MGR_GAG = 9 #禁言
ROLE_MGR_UNGAG = 10 #解除禁言
"""
#------------------------------
#活动管理
#------------------------------
"""
ACTIVITY_MGR_ACTITY_OPEN = 1 #开启活动
ACTIVITY_MGR_ACTITY_CLOSE = 2 #关闭活动
ACTIVITY_MGR_ACTITY_DELAY_ADD = 3 #添加预约活动
ACTIVITY_MGR_ACTITY_DELAY_DEL = 4 #取消预约活动
ACTIVITY_MGR_ACTITY_DELAY_QUERY = 5 #查看预约活动
"""

#------------------------------
#物品管理
#------------------------------
"""
ITEM_MGR_ITEM_QUERY = 1 #物品查询（数据支持）
ITEM_MGR_ITEM_ISSUE_APPLICATION = 2 #申请物品发放
ITEM_MGR_ITEM_ISSUE_SEND = 3 #审核通过发奖
ITEM_MGR_ITEM_ISSUE_RETURN = 4 #退回发奖申请
ITEM_MGR_ITEM_ISSUE_DEL = 5 #删除被退回的发奖申请
"""
#物品发放对象类型
ITEM_ISSUE_TARGET_ONLINE = 1 #所有在线玩家
ITEM_ISSUE_TARGET_ALL = 2 #所有玩家
ITEM_ISSUE_TARGET_SPECIFY = 3 #所有在线玩家

#------------------------------
#邮件管理
#------------------------------
"""
MAIL_MGR_MAIL_SEND = 1 #发送邮件
"""
#发送邮件对象类型
MAIL_SEND_TARGET_ONLINE = 1 #所有在线玩家
MAIL_SEND_TARGET_ALL = 2 #所有玩家
MAIL_SEND_TARGET_SPECIFY = 3 #所有在线玩家

#------------------------------
#公告管理
#------------------------------
"""
NOTICE_MGR_NOTICE_SEND_INSTANT = 1 #发送即时公告
NOTICE_MGR_NOTICE_SEND_DELAY = 2 #发送定时公告
NOTICE_MGR_NOTICE_SEND_MULTIPLE = 3 #发送多条公告
NOTICE_MGR_NOTICE_TIMEING_DEL = 4 #删除定时功告（包括定时公告和多条公告）
"""

#------------------------------
#角色查询
#------------------------------
"""
ROLE_INFO_QUERY_ROLE_UPGRADE = 1 #升级信息
ROLE_INFO_QUERY_SKILL_LEARN = 2 #技能学习信息
ROLE_INFO_QUERY_MAIL_RECORD = 3 #邮件记录信息
ROLE_INFO_QUERY_VEND_TRADE = 4 #摆摊交易信息
ROLE_INFO_QUERY_ITEM_FLOW = 5 #物品流向信息
ROLE_INFO_QUERY_ITEM_RECORD = 6 #物品记录信息
ROLE_INFO_QUERY_ROLE_POS = 7 #玩家当前位置信息
ROLE_INFO_QUERY_ROLE_EQUIP = 8 #玩家装备信息
ROLE_INFO_QUERY_ROLE_ATTRIBUTE = 9 #玩家属性信息
ROLE_INFO_QUERY_ROLE_TASK = 10 #玩家任务信息
ROLE_INFO_QUERY_ROLE_COIN = 11 #玩家金钱（货币）信息
ROLE_INFO_QUERY_ROLE_RECHARGE = 12 #玩家充值记录信息
"""

#------------------------------
#数据监控
#------------------------------
"""
DATA_MONITOR_ONLINE_DATA = 1 #在线数据监控
DATA_MONITOR_ROLE_COST_DATA = 2 #消费数据监控
DATA_MONITOR_RECHARGE_DATA = 3 #充值数据监控
DATA_MONITOR_ROLE_COIN_ADD = 4 #货币收入监控
"""

#玩家消费查询类型
DATA_MONITOR_ROLE_COST_DATA_TYPE_TOTAL = 1 #汇总查询
DATA_MONITOR_ROLE_COST_DATA_TYPE_SINGLE = 2 #详细查询
#玩家消费详细查询类型
ROLE_COST_DATA_QUERY_TYPE_ACCOUNT = 1 #账号查询
ROLE_COST_DATA_QUERY_TYPE_ROLE = 2 #角色查询
#玩家消费详细查询货币类型
ROLE_COST_DATA_QUERY_COIN_XIANSHI = 1 #仙石
ROLE_COST_DATA_QUERY_COIN_LINGSHI = 2 #灵石
ROLE_COST_DATA_QUERY_COIN_XUANSHI = 3 #玄石

#玩家充值查询类型
DATA_MONITOR_RECHARGE_DATA_TYPE_TOTAL = 1 #汇总查询
DATA_MONITOR_RECHARGE_DATA_TYPE_ORDER = 2 #订单查询
#充值订单查询方式
RECHARGE_DATA_QUERY_TYPE_ACCOUNT = 1 #账号查询
RECHARGE_DATA_QUERY_TYPE_TOTAL_VALUE = 2 #总充值查询
RECHARGE_DATA_QUERY_TYPE_SINGLE = 3 #单笔充值查询