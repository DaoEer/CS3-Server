# -*- coding: utf-8 -*-

#存放各种中文字符串
TeleportTitle = '<text fontSize="12" color="#%s">%s</text>'
TeleportStoneLimitLv = "（%d级后开放）"
TeleportStoneMoneyCost = '<text fontSize="12" color="#%s">（%d铜）</text>'

# 帮会默认职称名称
TONG_TITLE_NAME	= [ "帮主", "副帮主", "军师", "长老", "五星帮众", "四星帮众", "三星帮众", "二星帮众", "一星帮众"]

# 帮会日常
TONG_DAILY_QUEST_TITLE = "帮会日常任务"

# 阵营
CAMP_TAOSIM = "仙道"
CAMP_DEMON = "魔道"

CAMP_RED = "红方"
CAMP_BLUE = "蓝方"

#转为语文数字
ChineseNumber = ["十","一","二","三","四","五","六","七","八","九"]

YXLM_TOWER_NAME = { 0: "上路",1:"中路",2:"下路",3:"基地"}


#------------------------------------------------------------------------------------------------------------------------
# text
#------------------------------------------------------------------------------------------------------------------------
MAIL_SEND_SYSTEM				= "系统"

#------------------------------------------------------------------------------------------------------------------------
#点卡寄售
#------------------------------------------------------------------------------------------------------------------------
POINT_CARD_INFO_1							= "寄售点卡成功"
POINT_CARD_INFO_2					= "你寄售的点卡(卡号:%s)已经成功卖出。"
POINT_CARD_INFO_3					= "交易成功"
POINT_CARD_INFO_4					= "元宝将在稍后充值入你的帐户，请及时查看。如果24小时内没有元宝到账，请和GM联系。"
POINT_CARD_INFO_5						= "寄售点卡失败"
POINT_CARD_INFO_6					= "你寄售的点卡(卡号:%s)帐号和密码有误，已经下架，押金没收。"
POINT_CARD_INFO_7							= "交易失败"
POINT_CARD_INFO_8					= "购买的点卡信息有误，已经下架，本邮件包含本次交易费用，请取回。"
POINT_CARD_INFO_9					= "你寄售的点卡(卡号:%s)已经使用，已经下架，押金没收。"
POINT_CARD_INFO_10					= "这次寄售交易出错。本邮件包含本次交易费用，请取回。"
POINT_CARD_INFO_11					= "你寄售的点卡(卡号:%s)之前已被封号，不能使用，押金没收。"
POINT_CARD_INFO_12					= "点卡(卡号:%s)不存在或未激活，押金没收。"
POINT_CARD_INFO_13					= "寄售的点卡信息有误，已经下架，本邮件包含本次交易费用，请取回。"
POINT_CARD_INFO_14					= "你寄售的点卡(卡号:%s)面值不符，请重新寄售，上次寄售的押金没收。"
POINT_CARD_INFO_15					= "点卡寄售"
POINT_CARD_INFO_16					= "你寄售的点卡（卡号：%s）在有效时间内无人购买，该点卡依然有效，押金没收。"

FAST_TEAM_MSG = "@L{t='%s';m=joinTeam:%s;cfc=(0,255,0)}正在召集各路英雄挑战@L{t='%s';m=joinTeam:%s;cfc=(0,255,0)}副本,赶紧加入他们的队伍吧:@L{t='加入';m=joinTeam:%s;cfc=(0,255,0)}"

#帮会争霸报名成功所发送邮件的相关
TONG_STARCRAFT_SIGN_UP_SUCC_MAIL_TITLE = "帮会争霸"
TONG_STARCRAFT_SIGN_UP_SUCC_MAIL_CONTENT = "帮主对你委以重任，请在今晚20:00准时前往凤鸣城帮会管理员肖业处参与帮会争霸淘汰战，为本帮赢取荣耀！"

TONG_DISMISS_CHANGE_CON_TO_MONEY_MAIL_TITLE = "帮会解散--帮贡回奉"
TONG_DISMISS_CHANGE_CON_TO_MONEY_MAIL_CONTENT = "帮会解散，剩余帮贡已兑换成金币，现通过邮件悉数奉上，敬请查收！"

TONG_KICK_MENBER_MAIL_TITLE = "您已被踢出%s"
TONG_KICK_MENBER_MAIL_CONTENT = "您已被%s踢出了%s，自此恩义寸断，天涯飘零。"

TONG_CHANGE_LEADER_MAIL_TITLE = "【{}】帮主转让"
TONG_CHANGE_LEADER_MAIL_CONTENT = "【{}】将【{}】交托于你，让你克勤克俭，带领大家笑傲凤鸣。"

#CST-8727 勇闯夺命岛
YCJMD_BOSS_LEVEL_NAME = {2:"中级",3:"高级"}

# 轮回秘境打造功能 
COMPOSE_TOOL_RESULT_TITLE = "工坊打造"
COMPOSE_TOOL_RESULT_SUCCESS = "您在工坊打造的%s，已打造成功，请您到工坊储物柜处领取道具！"
COMPOSE_TOOL_RESULT_FAIL = "很遗憾，您在工坊打造的%s，打造失败了！"
COMPOSE_TOOL_GREEP_RESULT_FAIL = "很遗憾，您在工坊打造的%s，打造失败；但装备胚子仍然留了下来，装备半成品不能直接使用，需要经过淬炼之后才能使用，装备半成品已放入工坊储物柜中！"
COMPOSE_TRIPOD_RESULT_TITLE = "乾坤鼎炼制"
COMPOSE_TRIPOD_RESULT_SUCCESS = "您在乾坤鼎炼制的%s，已炼制成功，请您到乾坤鼎储物柜处领取道具！"
COMPOSE_TRIPOD_RESULT_FAIL = "很遗憾，您在乾坤鼎炼制的%s，已炼制失败！"

DF_ACTIVE_CHALLENGE_TITLE = "洞府争夺战奖励"
DF_ACTIVE_CHALLENGE_SUCCESS_CONTENT = "恭喜您，获得了洞府争夺战最后的胜利，也许是您走的太匆忙，尚有奖励未曾领取，现特将奖励通过邮件发送给您，请及时查收。"
DF_ACTIVE_CHALLENGE_FAIL_CONTENT = "很遗憾，您未能获得洞府争夺战最后的胜利，也许是您走的太匆忙，尚有奖励未曾领取，现特将奖励通过邮件发送给您，请及时查收。"
DF_ACTIVE_PLUNDER_TITLE = "洞府掠夺战奖励"
DF_ACTIVE_PLUNDER_SUCCESS_CONTENT = "恭喜您，获得了洞府掠夺战最后的胜利，也许是您走的太匆忙，尚有奖励未曾领取，现特将奖励通过邮件发送给您，请及时查收。"
DF_ACTIVE_PLUNDER_FAIL_CONTENT = "很遗憾，您未能获得洞府掠夺战最后的胜利，也许是您走的太匆忙，尚有奖励未曾领取，现特将奖励通过邮件发送给您，请及时查收。"

# 王道神兵
KING_CRAFT_EQUIP = "神兵·"

#年月日
YEAR = "年"
MONTH = "月"
DAY = "日"

#时分秒
HOUR = "时"
MINUTE = "分"
SECOND = "秒"

# 材料
CAI_LIAO = "材料"

TONG = "帮会"

LEVEL_TYPE_NAME = {1:"初级",2:"中级",3:"高级"}

BELONG_SIDE = { 0:"进攻",1:"防守" }
