# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from cs3_web_services import settings
from common import baseConnector, csstatus, csdefine, tooldefine, toollogdefine
from common.DBConnectInterface import g_dbInterfaceInst
from . import login
from . import GMActionLog

import json

g_baseappConnector = baseConnector.g_baseappConnector
loginInstannce = login.g_loginInstance
logInstance = GMActionLog.g_logInstance

SEND_TARGET_TYPE_SPECIFY = "target_specify" #指定玩家
SEND_TARGET_TYPE_ALL = "target_all" #所有玩家
SEND_TARGET_TYPE_ONLINE = "target_online" #在线玩家玩家

SEND_TARGET_TYPE_DICT = {
	SEND_TARGET_TYPE_SPECIFY: toollogdefine.ITEM_ISSUE_TARGET_SPECIFY,
	SEND_TARGET_TYPE_ALL: toollogdefine.ITEM_ISSUE_TARGET_ALL,
	SEND_TARGET_TYPE_ONLINE: toollogdefine.ITEM_ISSUE_TARGET_ONLINE,
}

class MailManager:
	"""
	邮件管理器
	"""
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		if MailManager._instance == None:
			MailManager._instance = MailManager()
		return MailManager._instance
		
	def getBaseInfo(self,request):
		"""
		"""
		context= {"error": "", "success": ""}
		context["send_target"] = request.POST.get("send_target", "") 
		context["role_type"] = request.POST.get("role_type", "")
		context["mail_role_infos"] = request.POST.get("mail_role_infos", "")
		context["mail_title"] = request.POST.get("mail_title", "")
		context["mail_content"] = request.POST.get("mail_content", "")
		context["mail_item_infos"] = request.POST.get("mail_item_infos", "")
		context["mail_money"] = request.POST.get("mail_money", 0)
		context["target_type"] = request.POST.get("send_target", "")
		return context
		
	def checkMailInfo(self, request):
		"""
		检查邮件信息是否合法
		"""
		send_target = request.POST.get("send_target").strip()       #发送对象
		mail_role_infos = request.POST.get("mail_role_infos").strip()       #玩家信息
		mail_item_infos = request.POST.get("mail_item_infos").strip()       #物品数据信息
		mail_money = request.POST.get("mail_money").strip()       #金钱数
		#检查角色
		if send_target and send_target == 'target_specify':
			if not mail_role_infos:
				return (False, csstatus.MAIL_SEND_NOT_ROLE_INFO)
			for roleName in mail_role_infos.split("|"):
				if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
					return (False, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		#检查物品
		if mail_item_infos:
			itemInfos = mail_item_infos.split("|")
			for itemInfo in itemInfos:
				bindType = "-1"
				if ":" in itemInfo:
					itemStr = itemInfo.split(":")
					if len(itemStr) == 2:
						itemID, amount = itemStr
					elif len(itemStr) == 3:
						itemID, amount, bindType = itemStr
					else:
						return (False, csstatus.MAIL_SEND_ITEM_INFO_FORMAT_ERROR)
				elif itemInfo.strip():
					return (False, csstatus.MAIL_SEND_ITEM_INFO_FORMAT_ERROR)
				if not itemID.isdigit() or not amount.isdigit():
					return (False, csstatus.MAIL_SEND_ITEM_INFO_NOT_DIGIT)
				if bindType != "-1" and bindType != "0" and bindType != "1":
					return (False, csstatus.MAIL_SEND_BIND_TYPE_ERROR)
		#检查金钱
		if mail_money:
			if not mail_money.isdigit():
				return (False, csstatus.MAIL_SEND_MONEY_NOT_DIGIT)
		
		return (True, "")	

	@loginInstannce.login_check
	def mail(self, request):
		""""""
		html_template = "gmtools/mail/mail_base.html"
		return render(request, html_template, {})

	@loginInstannce.login_check
	def mail_send(self, request):
		"""
		发送邮件
		:param request:
		:return:
		"""
		html_template = "gmtools/mail/mail_send.html"
		context = self.getBaseInfo(request)
		return render(request, html_template, context)

	@loginInstannce.login_check
	def mail_send_result(self, request):
		"""
		发送邮件处理结果
		"""
		html_template = "gmtools/mail/mail_send.html"
		context= self.getBaseInfo(request)
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_MAIL_MGR][tooldefine.MAIL_MGR_MAIL_SEND]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		checkResult = self.checkMailInfo(request)
		if not checkResult[0]:
			context["error"] = checkResult[1]
			return render(request, html_template, context)
		
		cmd_msg = {}
		cmd_msg["cmd"] = "sendMail"
		cmd_msg["info"] = {}
		cmd_msg["info"]["send_target"] = context.get("send_target")       #发送对象：指定玩家，所以玩家或者所以在线玩家
		cmd_msg["info"]["role_type"] = context.get("role_type")       #查询类型：DBID，或者玩家名字
		cmd_msg["info"]["mail_role_infos"] = context.get("mail_role_infos")       #玩家信息
		cmd_msg["info"]["mail_title"] = context.get("mail_title")       #邮件标题
		cmd_msg["info"]["mail_content"] = context.get("mail_content")       #邮件内容
		cmd_msg["info"]["mail_item_infos"] = context.get("mail_item_infos")       #物品数据信息
		cmd_msg["info"]["send_type"] = csdefine.MAIL_SENDER_TYPE_SYS
		cmd_msg["info"]["senderName"] = "系统"
		mail_money = context.get("mail_money")       #金钱数
		if not mail_money:
			cmd_msg["info"]["mail_money"] = 0
		else:
			cmd_msg["info"]["mail_money"] = int(mail_money)

		if(len(cmd_msg["info"]["mail_item_infos"].split("|"))>4):
			context["error"] = csstatus.MAIL_SEND_ITEM_NUM_ERROR
			return render(request, html_template, context)
		
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultDatas = connector.send_msg(cmd_msg)
		
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultDatas
		else:
			result_datas = resultDatas["result_datas"]
			errorItemList = result_datas["errorItemList"]
			if len(errorItemList) > 0:
				errorItemInfos = ", ".join(errorItemList)
				context["error"] = csstatus.MAIL_SEND_ITEM_ID_PART_ERROR % errorItemInfos
				return render(request, html_template, context)
			context["success"] = csstatus.MAIL_SEND_SUCCESS
			
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.sendMail(request.session["gm_userid"], request.session["gm_level"], SEND_TARGET_TYPE_DICT.get(context["send_target"], -1), context["mail_role_infos"], 
				context["mail_item_infos"], context["mail_title"], context["mail_content"], int(mail_money), currServerkey, request.serverInfos.get(currServerkey, ""))
				
		return render( request, html_template, context)

g_mailInstance = MailManager.instance()