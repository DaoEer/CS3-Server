# -*- coding: utf-8 -*-


import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from cs3_web_services import settings
from common import baseConnector, csstatus, csdefine,stringRes, tooldefine
from common.DBConnectInterface import g_dbInterfaceInst
from common import toollogdefine
from common import Functions
from . import login
from ..models import GMAwardRecord, GMUser
from . import GMActionLog

itemPath = Functions.getSeverConfigPath() + "/Item/ItemData.json"
ItemData = Functions.loadJsonDataByFile(itemPath)

logInstance = GMActionLog.g_logInstance
srvDB = tooldefine.tool_default_db_key

g_baseappConnector = baseConnector.g_baseappConnector
loginInstannce = login.g_loginInstance

SEND_TARGET_TYPE_SPECIFY = "target_specify" #指定玩家
SEND_TARGET_TYPE_ALL = "target_all" #所有玩家
SEND_TARGET_TYPE_ONLINE = "target_online" #在线玩家玩家

SEND_TARGET_TYPE_DICT = {
	SEND_TARGET_TYPE_SPECIFY: toollogdefine.ITEM_ISSUE_TARGET_SPECIFY,
	SEND_TARGET_TYPE_ALL: toollogdefine.ITEM_ISSUE_TARGET_ALL,
	SEND_TARGET_TYPE_ONLINE: toollogdefine.ITEM_ISSUE_TARGET_ONLINE,
}


class ItemManager:
	"""
	物品管理器
	"""
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		if ItemManager._instance == None:
			ItemManager._instance = ItemManager()
		return ItemManager._instance

	def initContext(self):
		"""
		初始化物品查询相关数据
		"""
		""
		context = {"error": ""}
		context["datas"] = []
		context["queryText"] = ""
		context["page"] = context["prevPage"] =context["nextPage"] = None
		return context

	@loginInstannce.login_check
	def item(self, request):
		"""
		"""
		html_template = "gmtools/item/item_mgr.html"
		return render( request, html_template, {})

	@loginInstannce.login_check
	def item_query(self, request):
		"""
		"""
		html_template = "gmtools/item/item_query.html"
		context = self.item_query_init()
		send_flag = request.POST.get("send_flag")  # 是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")  # 查询类型：道具名称
		queryText = request.POST.get("queryText")  # 查询条件的内容
		if not send_flag:  # 初次进入邮件记录网页
			return render(request, html_template, context)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_QUERY]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)

		itemData = ItemData
		itemLists = []
		if queryText == "":
			for item in itemData:
				data = ItemData.get(item, {})
				itemLists.append(data)
			message = {"datas": itemLists}
		else:
			for item in itemData:
				data = ItemData.get(item, {})
				if data[queryType] == queryText:
					itemLists.append(data)
			message = {"datas": itemLists}
		datas = message["datas"]
		itemList=[]
		NumId=1
		for data in datas:
			ItemID=data.get("ItemID")
			ItemName = data.get("ItemName")
			bindType = data.get("BindType")
			BindType = stringRes.ITEM_ITEM_SRCBindType_CH_DICT.get(int(bindType), bindType)
			quality = data.get("Quality")
			Quality = stringRes.ITEM_QUALITY_CH_DICT.get( int(quality), quality)
			Describe = data.get("Describe")
			if Describe=="":
				Describe="暂无"
			itemList.append({"NumId":NumId,"ItemID":ItemID,"ItemName":ItemName, "BindType":BindType,"Quality":Quality,"Describe":Describe })
			NumId=NumId+1
		context["datas"] = itemList
		context["queryText"] = queryText
		return render(request, html_template, context)
		
	def item_query_init(self):
		return {"error":"","queryText":"","datas":"","prevPage":None,"nextPage":None,"page":None}

	def checkItemInfo(self, request, issue_target, role_infos, item_info):
		"""
		检查物品发放配置数据信息是否正确
		:return: 是：TRUE, 否：FALSE
		"""
		if (len(item_info.split("|")) > 4):
			return (False, csstatus.MAIL_SEND_ITEM_NUM_ERROR)
		if issue_target == SEND_TARGET_TYPE_SPECIFY and not role_infos:
			return (False, csstatus.ITEM_ISSUE_NOT_ROLE_INFO)
		if issue_target == SEND_TARGET_TYPE_SPECIFY:
			for roleName in role_infos.split("|"):
				if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
					return (False, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		if item_info:
			itemInfos = item_info.split("|")
			for itemInfo in itemInfos:
				if ":" in itemInfo:
					itemID, amount = itemInfo.split(":")
				elif itemInfo.strip():
					return (False, csstatus.ITEM_ISSUE_ITEM_INFO_FORMAT_ERROR)
				if not itemID.isdigit() or not amount.isdigit():
					return (False, csstatus.ITEM_ISSUE_ITEM_INFO_NOT_DIGIT)
		else:
			return (False, csstatus.ITEM_ISSUE_NOT_ITME_INFO)
		return (True, "")

	def getAwardRecord(self):
		"""
		查询发奖相关记录
		"""
		record_application = []
		record_back = []
		record_complete = []
		for record in GMAwardRecord.objects.all():
			if record.sendState == 0:
				data = {"pk": record.pk, "id": len(record_application)+1, "applicationTime": record.applicationTime,
						"award_title": record.award_title, "applicant": record.applicant, "award_targetType": record.award_targetType}
				record_application.append(data)
			elif record.sendState == 1:
				data = {"pk": record.pk, "id": len(record_complete)+1, "applicationTime": record.applicationTime,
						"award_title": record.award_title, "applicant": record.applicant, "award_targetType": record.award_targetType}
				record_complete.append(data)
			elif record.sendState == 2:
				data = {"pk": record.pk, "id": len(record_back)+1, "applicationTime": record.applicationTime,
						"award_title": record.award_title, "applicant": record.applicant, "award_targetType": record.award_targetType}
				record_back.append(data)
		return {"record_application": record_application, "record_back": record_back, "record_complete": record_complete}

	@loginInstannce.login_check
	def item_issue(self, request):
		"""
		"""
		html_template = "gmtools/item/item_base.html"
		context= {"error": "", "success": ""}
		context["title"] = ""
		context["content"] = ""
		context["item_info"] = ""
		context["roleList"] = ""
		context["target_type"] = ""
		context["tab_index"] = 0
		if "tab_index" in request.GET:
			context["tab_index"] = int(request.GET.get("tab_index"))
		context.update(self.getAwardRecord())
		return render(request, html_template, context)

	@loginInstannce.login_check
	def item_issue_application(self, request):
		"""
		提交发奖申请
		"""
		html_template = "gmtools/item/item_base.html"
		context = {"error": "", "success": ""}
		context["target_type"] = request.POST.get("target_type", "")  # 发送对象
		context["roleList"] = request.POST.get("roleList", "")  # 玩家数据信息
		context["title"] = request.POST.get("title", "")  # 发放标题
		context["content"] = request.POST.get("content", "")  # 发放理由
		context["item_info"] = request.POST.get("item_info", "")  # 物品数据信息
		context["tab_index"] = int(request.POST.get("tab_index", 0))  # 标签页索引
		checkResult = self.checkItemInfo(request, context["target_type"], context["roleList"], context["item_info"])
		if not checkResult[0]:
			context["error"] = checkResult[1]
			context.update(self.getAwardRecord())
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_ISSUE_APPLICATION]:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)
					
		record = GMAwardRecord()
		record.applicationTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		record.award_targetType = context["target_type"]
		record.award_roleList = context["roleList"]
		record.award_title = context["title"]
		record.award_reason = context["content"]
		record.award_itemList = context["item_info"]
		record.applicant = request.session["gm_username"]
		record.sendState = 0
		record.save()
		context.update(self.getAwardRecord())
		context["success"] = csstatus.AWARD_SUBMIT_SUCCEED
		
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.issueItemApplicationLog(request.session["gm_userid"], request.session["gm_level"], SEND_TARGET_TYPE_DICT.get(context["target_type"], -1), 
			context["roleList"], context["item_info"], context["title"], context["content"], currServerkey, request.serverInfos.get(currServerkey, ""))
			
		return render(request, html_template, context)

	@loginInstannce.login_check
	def item_issue_result(self, request):
		"""
		发奖
		"""
		html_template = "gmtools/item/item_base.html"
		context = {"error": "", "success": "", "tab_index": 2}
		
		if "awardReturn_pk" in request.POST:
			pk = request.POST.get("awardReturn_pk", "")
			if not pk:
				context.update(self.getAwardRecord())
				context["error"] = csstatus.AWARD_SUBMIT_ERROR
				return render(request, html_template, context)
			else:
				if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_ISSUE_RETURN]:
					context.update(self.getAwardRecord())
					context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
					return render(request, html_template, context)
			
				record = GMAwardRecord.objects.get(pk=int(pk))
				record.sendState = 2
				record.save()
				context.update(self.getAwardRecord())
				context["success"] = csstatus.AWARD_RETURN_SUCCEED
				
				user = GMUser.objects.using(srvDB).get(userName=record.applicant)
				currServerkey = request.session[tooldefine.CURR_SERVER]
				logInstance.issueItemReturnLog(request.session["gm_userid"], request.session["gm_level"], user.userID, user.level, SEND_TARGET_TYPE_DICT.get(record.award_targetType, -1), 
					record.award_roleList, record.award_itemList, record.award_title, record.award_reason, currServerkey, request.serverInfos.get(currServerkey, ""))
				
				return render(request, html_template, context)
		record_pk = request.POST.get("record_pk", "")
		if not record_pk:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.AWARD_SUBMIT_ERROR
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_ISSUE_SEND]:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)
			
		record = GMAwardRecord.objects.get(pk=int(record_pk))
		cmd_msg = {}
		item_datas = {}
		item_datas["issue_target"] = record.award_targetType
		item_datas["role_infos"] = record.award_roleList
		item_datas["issue_title"] = record.award_title
		item_datas["issue_reason"] = record.award_reason
		item_datas["item_info"] = record.award_itemList
		item_datas["send_type"] = csdefine.MAIL_SENDER_TYPE_SYS
		cmd_msg["cmd"] = "itemIssue"
		cmd_msg["info"] = {}
		cmd_msg["info"]["item_datas"] = item_datas
		cmd_msg["info"]["senderName"] = "系统"
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultDatas = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultDatas
		else:
			result_datas = resultDatas["result_datas"]
			errorItemList = result_datas["errorItemList"]
			if len(errorItemList) > 0:
				errorItemInfos = ", ".join(errorItemList)
				context["error"] = csstatus.ITEM_ISSUE_ITEM_ID_PART_ERROR % errorItemInfos
				return render(request, html_template, context)
		record.sendState = 1
		record.save()
		context.update(self.getAwardRecord())
		context["success"] = csstatus.ITEM_ISSUE_SUCCESS
		
		user = GMUser.objects.using(srvDB).get(userName=record.applicant)
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.issueItemSendLog(request.session["gm_userid"], request.session["gm_level"], user.userID, user.level, SEND_TARGET_TYPE_DICT.get(item_datas["issue_target"], -1) ,item_datas["role_infos"], item_datas["item_info"], 
			item_datas["issue_title"], item_datas["issue_reason"], currServerkey, request.serverInfos.get(currServerkey, ""))
			
		return render(request, html_template, context)

	@loginInstannce.login_check
	def item_issue_deleteApplication(self, request):
		"""
		删除退回申请
		"""
		html_template = "gmtools/item/item_base.html"
		context = {"error": "", "success": "", "tab_index": 3}
		pk = request.POST.get("awardDelete", "")
		if not pk:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.AWARD_SUBMIT_ERROR
			return render(request, html_template, context)
		else:
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_ISSUE_DEL]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render(request, html_template, context)
			
			record = GMAwardRecord.objects.get(pk=int(pk))
			record.delete()
			context.update(self.getAwardRecord())
			context["success"] = csstatus.AWARD_DELETE_SUCCEED
			
			user = GMUser.objects.using(srvDB).get(userName=record.applicant)
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.issueItemDelLog(request.session["gm_userid"], request.session["gm_level"], user.userID, user.level, SEND_TARGET_TYPE_DICT.get(record.award_targetType, -1), 
				record.award_roleList, record.award_itemList, record.award_title, record.award_reason, currServerkey, request.serverInfos.get(currServerkey, ""))
			
			return render(request, html_template, context)

	@loginInstannce.login_check
	def item_issue_awardRecordEdit(self, request):
		"""
		编辑退回申请
		"""
		context = {"error": "", "success": ""}
		html_template = ""
		if "submit_application" in request.POST:
			context["target_type"] = request.POST.get("target_type", "")  # 发送对象
			context["roleList"] = request.POST.get("roleList", "")  # 玩家数据信息
			context["title"] = request.POST.get("title", "")  # 发放标题
			context["content"] = request.POST.get("content", "")  # 发放理由
			context["item_info"] = request.POST.get("item_info", "")  # 物品数据信息
			context["pk"] = request.POST.get("pk", "")
			if context["target_type"] == "target_all":
				html_template = "gmtools/item/item_recordEdit_targetAll.html"
			elif context["target_type"] == "target_specify":
				html_template = "gmtools/item/item_recordEdit_targetSpecify.html"
			checkResult = self.checkItemInfo(request, context["target_type"], context["roleList"], context["item_info"])
			if not checkResult[0]:
				context["error"] = checkResult[1]
				return render(request, html_template, context)
				
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ITEM_MGR][tooldefine.ITEM_MGR_ITEM_ISSUE_APPLICATION]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render(request, html_template, context)
				
			record = GMAwardRecord.objects.get(pk=int(context["pk"]))
			record.award_targetType = context["target_type"]
			record.award_roleList = context["roleList"]
			record.award_title = context["title"]
			record.award_reason = context["content"]
			record.award_itemList = context["item_info"]
			record.applicant = request.session["gm_user"]
			record.sendState = 0
			record.save()
			context["success"] = csstatus.AWARD_SUBMIT_SUCCEED
			return render(request, html_template, context)

		pk = request.GET.get("pk", "")
		record = GMAwardRecord.objects.get(pk=int(pk))
		if record.award_targetType == "target_all":
			html_template = "gmtools/item/item_recordEdit_targetAll.html"
		elif record.award_targetType == "target_specify":
			html_template = "gmtools/item/item_recordEdit_targetSpecify.html"
		context["title"] = record.award_title
		context["content"] = record.award_reason
		context["roleList"] = record.award_roleList
		context["item_info"] = record.award_itemList
		context["pk"] = pk
		return render(request, html_template, context)

	@loginInstannce.login_check
	def item_issue_queryAwards(self, request):
		"""
		查看奖励列表
		"""
		html_template = "gmtools/item/item_award_info.html"
		context = {"error": ""}
		pk = request.GET.get("pk", "")
		if not pk:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		record = GMAwardRecord.objects.get(pk=int(pk))
		awardList_temp = record.award_itemList.split("|")
		awardList = []
		for award_temp in awardList_temp:
			award = {"itemId": award_temp.split(":")[0], "amount": award_temp.split(":")[1]}
			item = ItemData.get(award["itemId"], {})
			if item:
				award["itemName"] = item["ItemName"]
				award["ReqLevel"] = item["ReqLevel"]
				award["bindType"] = "是" if item["BindType"] == 1 else "否"
				award["Type"] = stringRes.ITEM_TYPE_DICT.get(int(item["Type"]), "")
				award["Describe"] = item["Describe"]
				if item["StackAmount"] == "0":
					award["StackAmount"] = item["StackAmount"].split("|")[0]
				else:
					award["StackAmount"] = item["StackAmount"].split("|")[1]
				award["Price"] = item["Price"]
				awardList.append(award)
		context["awardList"] = awardList
		return render(request, html_template, context)

	def item_issue_queryAwardRoleInfo(self, request):
		"""
		查看发奖名单
		"""
		html_template = "gmtools/item/item_awardRole_info.html"
		context = {"error": ""}
		pk = request.GET.get("pk", "")
		if not pk:
			context.update(self.getAwardRecord())
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		record = GMAwardRecord.objects.get(pk=int(pk))
		awardRoleList = []
		for role in record.award_roleList.split("|"):
			awardRoleList.append({"id": len(awardRoleList)+1, "roleName": role})
		context["awardRoleList"] = awardRoleList
		return render(request, html_template, context)


g_itemInstance = ItemManager.instance()