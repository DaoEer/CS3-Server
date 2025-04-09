# -*- coding: utf-8 -*-

#-------------------------------------------------------------------
#日志类型
#-------------------------------------------------------------------
LOG_TYPE_QUEST		= 1	#任务
LOG_TYPE_ITEM		= 2	#物品
LOG_TYPE_COIN		= 3	#货币
LOG_TYPE_PRO			= 4	#属性
LOG_TYPE_EQUIP		= 5	#装备
LOG_TYPE_RELATION	= 6	#人物关系
LOG_TYPE_PET			= 7	#幻兽
LOG_TYPE_TRADE		= 8	#交易
LOG_TYPE_MAIL		= 9	#邮件
LOG_TYPE_TONG		= 10	#帮会
LOG_TYPE_SKILL		= 11	#技能
LOG_TYPE_RECHARGE	= 12	#充值
LOG_TYPE_ACCOUNT	= 13	#账号
LOG_TYPE_ROLE		= 14	#角色
LOG_TYPE_VEND		= 15	#摆摊
LOG_TYPE_ACT_COPY		= 16	#活动、副本



#-----------------------------------
#任务日志分类
#-----------------------------------
LT_QUEST_ACCEPT		= 1	#接受任务
LT_QUEST_COMPLETE	= 2	#完成任务
LT_QUEST_ABANDON	= 3	#放弃任务

#-----------------------------------
#物品日志分类
#-----------------------------------
LT_ITEM_ADD			= 1	#添加物品
LT_ITEM_DEL			= 2	#删除物品
LT_ITEM_SET_AMOUNT	= 3	#设置数值
LT_ITEM_TRAN_STORE	= 4	#转入仓库
LT_ITEM_TALK_STORE	= 5	#取出仓库

#-----------------------------------
#货币日志分类
#-----------------------------------
LT_MONEY_CHANGE	= 1	#金钱改变
LT_XIANSHI_CHANGE	= 2	#仙石改变
LT_LINGSHI_CHANGE	= 3	#灵石改变
LT_XUANSHI_CHANGE	= 4	#玄石改变
LT_BINDMONEY_CHANGE	= 5	#绑定金钱改变

#-----------------------------------
#角色属性改变日志分类
#-----------------------------------
LT_PRO_EXP_CHANGE			= 1	#经验改变
LT_PRO_POTENTIAL_CHANGE	= 2	#潜能改变
LT_PRO_XIUWEI_ADD		= 3	#修为增长
LT_PRO_LEVEL_UPGRADE		= 4	#升级
LT_PRO_KILLING_CHANGE		= 5	#杀气改变
LT_PRO_CREDIT_CHANGE		= 6	#功勋值改变

#-----------------------------------
#角色装备日志分类
#-----------------------------------
LT_EQUIP_INTENSIFY	= 1	#装备强化
LT_EQUIP_COMPOSE	= 2	#装备打造
LT_EQUIP_SHUFFLE		= 3	#装备洗练
LT_EQUIP_SHUFFLE_REPLACE	= 4	#装备洗练替换
LT_EQUIP_RECAST		= 5	#装备重铸
LT_EQUIP_REPAIR		= 6	#装备修理
LT_EQUIP_BACKFIRE		= 7	#装备回火
LT_EQUIP_RESTORE		= 8	#装备还原
LT_EQUIP_SAVE			= 9	#装备保存
LT_EQUIP_TRAN_STAR	= 10	#装备传星
LT_EQUIP_OPEN_SAVE_SLOT		= 11 #开启强化保存栏位

#-----------------------------------
#角色装备日志分类
#-----------------------------------
LT_RELATION_TEACHER_BUILD		= 1	#建立师徒关系
LT_RELATION_TEACHER_REMOVE	= 2	#解除师徒关系

#-----------------------------------
#角色幻兽日志分类
#-----------------------------------
LT_PET_ADD			= 1	#获得幻兽
LT_PET_LOSE			= 2	#失去幻兽
LT_PET_SKILL_LEARN		= 3	#幻兽学习技能
LT_PET_SKILL_UPGRADE	= 4	#幻兽升级技能
LT_PET_SEAL			= 5	#幻兽封印
LT_PET_REPLACE_SKILL	= 6	#幻兽替换技能
LT_PET_COMPOSE		= 7	#幻兽合成
LT_PET_UP_STEP			= 8	#幻兽升阶

#打书技能类型
LT_PET_REPLACE_SKILL_ACTIVE	= 1 #主动技能
LT_PET_REPLACE_SKILL_PASSIVE	= 2 #被动技能

#升级技能类型
LT_PET_SKILL_UPGRADE_ACTIVE	= 1 #升级主动技能
LT_PET_SKILL_UPGRADE_PASSIVE	= 2 #升级被动技能

#-----------------------------------
#角色交易日志分类
#-----------------------------------
LT_TRADE_SWAP_ITEM		= 1	#与玩家交易物品
LT_TRADE_SWAP_MONEY	= 2	#与玩家交易金钱
LT_TRADE_SWAP_PET		= 3	#与玩家交易幻兽
LT_TRADE_NPC_BUY		= 4	#在NPC处买东西
LT_TRADE_NPC_SELL		= 5	#卖东西给NPC
LT_TRADE_SHOP_BUY		= 6	#在商城买东西
LT_TRADE_BUY_BACK		= 7	#回购
LT_TRADE_BUY_BACK_HIGH	= 8	#高价回购
LT_TRADE_RETURN_ITEM	= 9	#退货
LT_TRADE_GIVING_GOOD	= 10 #赠送

#-----------------------------
#角色交易方式
#-----------------------------
LT_TRADE_TYPE_TRANSFER		= 1	#直接交易
LT_TRADE_TYPE_VEND			= 2	#摆摊

#-----------------------------------
#邮件日志分类
#-----------------------------------
LT_MAIL_SEND		= 1	#发送邮件
LT_MAIL_READ		= 2	#阅读邮件
LT_MAIL_DEL		= 3	#删除邮件
LT_MAIL_EXTRACT	= 4	#提取邮件

#删除邮件分类
LT_MAIL_DEL_TYPE_ACTIVE			= 1 #主动删除
LT_MAIL_DEL_TYPE_TIME_ARRIVE	= 2 #时间达到
LT_MAIL_DEL_TYPE_BEREPLACED		= 3 #被其他新邮件顶替

#-----------------------------------
#帮会日志分类
#-----------------------------------
LT_TONG_CREATE				= 1	#帮会创建
LT_TONG_DISMISS				= 2	#帮会解散
LT_TONG_MEMBER_ADD		= 3	#成员加入
LT_TONG_MEMBER_LEAVE		= 4	#成员离开
LT_TONG_MONEY_CHANGE		= 5	#帮会资金改变
LT_TONG_LEVEl_CHANGE		= 6	#帮会等级改变
LT_TONG_GRADE_CHANGE		= 7	#帮会权限改变
LT_TONG_LEADER_CHANGE		= 8	#帮会帮主改变
LT_TONG_CONTRIBUTE_CHANGE  = 9	#帮会成员帮贡改变
LT_TONG_ITEM_ADD			= 10	#帮会物品添加
LT_TONG_ITEM_REMOVE		= 11	#帮会物品删除

#-----------------------------------
#技能日志分类
#-----------------------------------
LT_SKILL_LEARN		= 1	#学习技能
LT_SKILL_UPGRADE		= 2	#升级技能

#-----------------------------------
#账号日志分类
#-----------------------------------
LT_ACCOUNT_LOGON		= 1	#账号登录
LT_ACCOUNT_LOGOUT		= 2	#账号下线
LT_ACCOUNT_ROLE_ADD	= 3	#添加角色
LT_ACCOUNT_ROLE_DEL		= 4	#删除角色
LT_ACCOUNT_LOCK			= 5	#封锁账号
LT_ACCOUNT_UNLOCK		= 6	#解封账号


#-----------------------------------
#角色日志分类
#-----------------------------------
LT_ROLE_LOGON		= 1	#角色登录
LT_ROLE_LOGOUT		= 2	#角色下线
LT_ROLE_GAG			= 3	#角色禁言
LT_ROLE_UNGAG		= 4	#角色解除禁言
LT_ROLE_PRO_RECORD	= 5	#角色属性记录

#-----------------------------------
#充值类型日志分类
#-----------------------------------
LT_RECHARGE_GOLD	= 1
LT_RECHARGE_SILVER	= 2

#-----------------------------------
#活动、副本日志分类
#-----------------------------------
LT_ACT_COPY_TYPE_JOIN	= 1 #活动、副本参与
