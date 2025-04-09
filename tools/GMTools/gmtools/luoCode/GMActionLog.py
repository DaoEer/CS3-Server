# -*- coding: utf-8 -*-

from datetime import datetime

from .. import models
from common import csdefine
from common import tooldefine
from common import toollogdefine

srvConf = tooldefine.tool_default_db_key

class GMActionLog:
	"""
	GM日志
	"""
	_instance = None
	def __init__(self):
		pass
	
	@staticmethod
	def instance():
		if GMActionLog._instance == None:
			GMActionLog._instance = GMActionLog()
		return GMActionLog._instance
		
		
	#-----------------------GM用户管理-------------------------
	def userLog(self, action, id, level, targetID, targetLevel, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		models.GMUserLog.objects.using(srvConf).create(
			actionType = action, userID = id, userLevel = level, targetUserID = targetID, targetUserLevel = targetLevel, serverKey = serverKey, serverName = serverName,
			param1 = param1, param2 = param2, param3 = param3,
		)
	
	def addUserLog(self, userID, userLevel, newUserID, newUserLevel, serverKey, serverName):
		"""
		#添加GM用户
		@Parmas: userID，userLevel，新用户userID，新用户userLevel，服务器key，服务器名字
		"""
		self.userLog(tooldefine.USER_MGR_ADD, userID, userLevel, newUserID, newUserLevel, serverKey, serverName)
		
	def delUserLog(self, userID, userLevel, targetUserID, targetUserLevel, serverKey, serverName):
		"""
		#删除GM用户
		@Parmas: userID，userLevel，被删除用户userID，被删除用户userLevel，服务器key，服务器名字
		"""
		self.userLog(tooldefine.USER_MGR_DEL, userID, userLevel, targetUserID, targetUserLevel, serverKey, serverName)
		
	def editUserLog(self, userID, userLevel, targetUserID, targetUserLevel, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		self.userLog(tooldefine.USER_MGR_EDIT, userID, userLevel, targetUserID, targetUserLevel, serverKey, serverName, param1, param2, param3)
		
	def changeUserLevelLog(self, userID, userLevel, targetUserID, targetUserLevel, targetUserOldLevel, serverKey, serverName):
		"""
		#修改GM用户等级
		@Parmas: userID，userLevel，被修改用户userID，被修改用户userLevel，修改用户原userLevel，服务器key，服务器名字
		"""
		self.editUserLog(userID, userLevel, targetUserID, targetUserLevel, serverKey, serverName, targetUserOldLevel, toollogdefine.USER_MGR_EDIT_TYPE_LEVEL_MODIFY)
	
	def changeUserPasswordLog(self, userID, targetUserID, userLevel, targetUserLevel, serverKey, serverName):
		"""
		#修改GM用户密码
		@Parmas: userID，userLevel，被修改用户userID，被修改用户userLevel，服务器key，服务器名字
		"""
		self.userLog(tooldefine.USER_MGR_MODIFY_PWD, userID, targetUserID, userLevel, targetUserLevel, serverKey, serverName)
		
		
	#-----------------------游戏账号管理-------------------------
	def accountLog(self, action, id, level, targetAccount, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		models.GMAccountMgrLog.objects.using(srvConf).create(
			actionType = action, userID = id, userLevel = level, targetAccount = targetAccount, serverKey = serverKey, serverName = serverName, 
			param1 = param1, param2 = param2, param3 = param3,
		)
		
	def blockAccountLog(self, userID, userLevel, targetAccount, blockTime, reason, serverKey, serverName):
		"""
		#封锁账号
		@Parmas: 操作者userID，userLevel，被封锁账号，封锁时长，封锁原因，服务器key，服务器名字
		"""
		self.accountLog(tooldefine.ACCOUNT_MGR_LOCK_ACCOUNT, userID, userLevel, targetAccount, serverKey, serverName, blockTime, reason)
		
	def unBlockAccountLog(self, userID, userLevel, targetAccount, reason, serverKey, serverName):
		"""
		#解封账号
		@Parmas: 操作者userID，userLevel，被解封账号，解封原因，服务器key，服务器名字
		"""
		self.accountLog(tooldefine.ACCOUNT_MGR_UNLOCK_ACCOUNT, userID, userLevel, targetAccount, serverKey, serverName, reason)
		
	def trusteeshipLog(self, userID, userLevel, targetAccount, trusteeshipTime, reason, serverKey, serverName):
		"""
		#账号托管
		@Parmas: 操作者userID，userLevel，被托管账号，托管时长，托管原因，服务器key，服务器名字
		"""
		self.accountLog(tooldefine.ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP, userID, userLevel, targetAccount, serverKey, serverName, trusteeshipTime, reason)
		
	def cancelTrusteeshipLog(self, userID, userLevel, targetAccount, reason, serverKey, serverName):
		"""
		#取消账号托管
		@Parmas: 操作者userID，userLevel，取消托管账号，取消托管原因，服务器key，服务器名字
		"""
		self.accountLog(tooldefine.ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP_CANCEL, userID, userLevel, targetAccount, serverKey, serverName, reason)
		
		
	#-----------------------角色管理-------------------------
	def roleLog(self, action, id, level, targetRole, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		models.GMRoleMgrLog.objects.using(srvConf).create(
			actionType = action, userID = id, userLevel = level, targetRole = targetRole, serverKey = serverKey, serverName = serverName, 
			param1 = param1, param2 = param2, param3 = param3,
		)
		
	def kickRoleLog(self, userID, userLevel, targetRole, reason, serverKey, serverName):
		"""
		#踢人
		@Parmas: 操作者userID，userLevel，被踢玩家名，被踢原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_KICK_ROLE, userID, userLevel, targetRole, serverKey, serverName, reason)
		
	def gagRoleLog(self, userID, userLevel, targetRole, gagList, gagTime, reason, serverKey, serverName):
		"""
		#禁言
		@Parmas: 操作者userID，userLevel，被禁言玩家名，禁言频道列表，禁言时长，禁言原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_GAG, userID, userLevel, targetRole, serverKey, serverName, gagList, gagTime, reason)
		
	def unGagRoleLog(self, userID, userLevel, targetRole, unGagList, reason, serverKey, serverName):
		"""
		#解除禁言
		@Parmas: 操作者userID，userLevel，解除禁言玩家名，解除禁言频道列表，解除禁言原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_UNGAG, userID, userLevel, targetRole, serverKey, serverName, unGagList, reason)
		
	def freezeRoleLog(self, userID, userLevel, targetRole, reason, serverKey, serverName):
		"""
		#冻结角色
		@Parmas: 操作者userID，userLevel，冻结玩家名，冻结原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_FREEZE_ROLE, userID, userLevel, targetRole, serverKey, serverName, reason)
		
	def unFreezeRoleLog(self, userID, userLevel, targetRole, reason, serverKey, serverName):
		"""
		#解除冻结角色
		@Parmas: 操作者userID，userLevel，解冻玩家名，解冻原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_UNFREEZE_ROLE, userID, userLevel, targetRole, serverKey, serverName, reason)

	def tranToRevivePosRoleLog(self, userID, userLevel, targetRole, serverKey, serverName):
		"""
		#解除冻结角色
		@Parmas: 操作者userID，userLevel，解冻玩家名，解冻原因，服务器key，服务器名字
		"""
		self.roleLog(tooldefine.ROLE_MGR_TRAN_TO_REVIVE_POS, userID, userLevel, targetRole, serverKey, serverName)

		
	#-----------------------活动管理-------------------------
	def activityLog(self, action, userID, userLevel, activityKey, activityName, serverKey, serverName, param1 = ""):
		models.GMActivityMgrInfo.objects.using(srvConf).create(
			actionType = action, userID = userID, userLevel = userLevel, activityKey = activityKey, activityName = activityName, serverKey = serverKey, serverName = serverName, 
			param1 = param1,
		)
		
	def openActivityLog(self, userID, userLevel, activityKey, activityName, serverKey, serverName):
		"""
		#开启活动
		@Parmas: 操作者userID，userLevel，活动key，活动名字，服务器key，服务器名字
		"""
		self.activityLog(tooldefine.ACTIVITY_MGR_ACTITY_OPEN, userID, userLevel, activityKey, activityName, serverKey, serverName)
		
	def closeActivityLog(self, userID, userLevel, activityKey, activityName, serverKey, serverName):
		"""
		#关闭活动
		@Parmas: 操作者userID，userLevel，活动key，活动名字，服务器key，服务器名字
		"""
		self.activityLog(tooldefine.ACTIVITY_MGR_ACTITY_CLOSE, userID, userLevel, activityKey, activityName, serverKey, serverName)
		
	def addDelayActivity(self, userID, userLevel, activityKey, activityName, openTime, serverKey, serverName):
		"""
		#添加定时活动计划
		@Parmas: 操作者userID，userLevel，活动key，活动名字，活动开启时间，服务器key，服务器名字
		"""
		self.activityLog(tooldefine.ACTIVITY_MGR_ACTITY_DELAY_ADD, userID, userLevel, activityKey, activityName, serverKey, serverName, openTime)
		
	def cancelDelayActivity(self, userID, userLevel, activityKey, activityName, openTime, serverKey, serverName):
		"""
		#取消定时活动计划
		@Parmas: 操作者userID，userLevel，活动key，活动名字，活动开启时间，服务器key，服务器名字
		"""
		self.activityLog(tooldefine.ACTIVITY_MGR_ACTITY_DELAY_DEL, userID, userLevel, activityKey, activityName, serverKey, serverName, openTime)
		
		
	#-----------------------物品管理-------------------------
	def itemLog(self, action, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		models.GMItemMgrLog.objects.using(srvConf).create(
			actionType = action, userID = userID, userLevel = userLevel, targetType = targetType, roleList = roleList, itemList = itemList, title = title, 
			content = content, serverKey = serverKey, serverName = serverName, param1 = param1, param2 = param2, param3 = param3,
		)
		
	def issueItemApplicationLog(self, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName):
		"""
		#申请发奖
		@Parmas: 申请人UserID，申请人Level，发奖对象类型（所有玩家，在线玩家，指定玩家），发奖玩家列表，物品信息列表，标题，内容，服务器key，服务器名字
		"""
		self.itemLog(tooldefine.ITEM_MGR_ITEM_ISSUE_APPLICATION, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName)
		
	def issueItemSendLog(self, userID, userLevel, appUserID, appUserLevel, targetType, roleList, itemList, title, content, serverKey, serverName):
		"""
		#审核通过发奖
		@Parmas: 审核人UserID，审核人Level，申请人UserID，申请人Level，发奖对象类型（所有玩家，在线玩家，指定玩家），发奖玩家列表，物品信息列表，标题，内容，服务器key，服务器名字
		"""
		self.itemLog(tooldefine.ITEM_MGR_ITEM_ISSUE_SEND, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName, appUserID, appUserLevel)
		
	def issueItemReturnLog(self, userID, userLevel, appUserID, appUserLevel, targetType, roleList, itemList, title, content, serverKey, serverName):
		"""
		#退回发奖申请
		@Parmas: 退回人UserID，退回人Level，申请人UserID，申请人Level，发奖对象类型（所有玩家，在线玩家，指定玩家），发奖玩家列表，物品信息列表，标题，内容，服务器key，服务器名字
		"""
		self.itemLog(tooldefine.ITEM_MGR_ITEM_ISSUE_RETURN, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName, appUserID, appUserLevel)
		
	def issueItemDelLog(self, userID, userLevel, appUserID, appUserLevel, targetType, roleList, itemList, title, content, serverKey, serverName):
		"""
		#删除被退回的发奖申请
		@Parmas: 删除人UserID，删除人Level，申请人UserID，申请人Level，发奖对象类型（所有玩家，在线玩家，指定玩家），发奖玩家列表，物品信息列表，标题，内容，服务器key，服务器名字
		"""
		self.itemLog(tooldefine.ITEM_MGR_ITEM_ISSUE_DEL, userID, userLevel, targetType, roleList, itemList, title, content, serverKey, serverName, appUserID, appUserLevel)
		
		
	#-----------------------邮件管理-------------------------
	def mailLog(self, action, userID, userLevel, targetType, roleList, itemList, title, content, moneyAmount, serverKey, serverName):
		models.GMMailMgrLog.objects.using(srvConf).create(
			actionType = action, userID = userID, userLevel = userLevel, targetType = targetType, roleList = roleList, itemList = itemList, title = title, 
			content = content, moneyAmount = moneyAmount, serverKey = serverKey, serverName = serverName,
		)
		
	def sendMail(self, userID, userLevel, targetType, roleList, itemList, title, content, moneyAmount, serverKey, serverName):
		"""
		#发送邮件
		@Parmas: 发送者userID，发送者Level，发送对象类型（所有玩家，在线玩家，指定玩家），发送玩家列表，物品信息列表，标题，内容，金钱数，服务器key，服务器名字
		"""
		self.mailLog(tooldefine.MAIL_MGR_MAIL_SEND, userID, userLevel, targetType, roleList, itemList, title, content, moneyAmount, serverKey, serverName)
		
		
	#-----------------------公告管理-------------------------
	def noticeLog(self, action, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName, param1 = "", param2 = "", param3 = ""):
		models.GMNoticeMgrLog.objects.using(srvConf).create(
			actionType = action, userID = userID, userLevel = userLevel, noticeTimes = noticeTimes, intervalTime = intervalTime, title = title, 
			content = content, serverKey = serverKey, serverName = serverName, param1 = param1, param2 = param2, param3 = param3,
		)
		
	def sendInstantNotice(self, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName):
		"""
		#发送即时公告
		@Parmas: 发送者userID，发送者Level，公告发送次数，每次公告时间间隔，标题，内容，服务器key，服务器名字
		"""
		self.noticeLog(tooldefine.NOTICE_MGR_NOTICE_SEND_INSTANT, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName)
		
	def sendDelayNotice(self, userID, userLevel, noticeTimes, intervalTime, title, content, sendTime, serverKey, serverName):
		"""
		#发送定时公告
		@Parmas: 发送者userID，发送者Level，公告发送次数，每次公告时间间隔，标题，内容，公告发送时间，服务器key，服务器名字
		"""
		self.noticeLog(tooldefine.NOTICE_MGR_NOTICE_SEND_DELAY, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName, sendTime)
		
	def sendMultipleNotice(self, userID, userLevel, noticeTimes, intervalTime, groupIntervalTime, title, content, sendTime, serverKey, serverName):
		"""
		#发送多条公告
		@Parmas: 发送者userID，发送者Level，公告发送次数，每次公告时间间隔，每组功能时间间隔，标题，内容，公告发送时间，服务器key，服务器名字
		"""
		self.noticeLog(tooldefine.NOTICE_MGR_NOTICE_SEND_MULTIPLE, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName, sendTime, groupIntervalTime)
		
	def delTimingNotice(self, userID, userLevel, noticeTimes, intervalTime, title, content, sendTime, serverKey, serverName, groupIntervalTime = ""):
		"""
		#删除定时公告（包括定时公告和多条公告）
		@Parmas: 删除者userID，删除者Level，公告发送次数，每次公告时间间隔，标题，内容，公告发送时间，服务器key，服务器名字，每组功能时间间隔
		"""
		self.noticeLog(tooldefine.NOTICE_MGR_NOTICE_TIMEING_DEL, userID, userLevel, noticeTimes, intervalTime, title, content, serverKey, serverName, sendTime, groupIntervalTime)
		
		
	def queryLog(self, name = "", userName = "", actionType = 0, updateTime = {}):
		conditionDict = {}
		if name:
			conditionDict["name"] = name
		if userName:
			conditionDict["userName"] = userName
		if actionType != 0:
			conditionDict["actionType"] = actionType
		if updateTime:
			startTime = updateTime.get("startTime", datetime(2020, 0, 0, 0, 0, 0))
			endTime = updateTime.get("endTime", datetime.now())
			conditionDict["updateTime__range"] = (startTime, endTime)
		
		return GMLogInfo.objects.using(srvConf).filter(**conditionDict)
		
		
g_logInstance = GMActionLog.instance()