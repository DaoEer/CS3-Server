# -*- coding: utf-8 -*-


import json
import time, datetime
import pickle
import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from common.DBConnectInterface import g_dbInterfaceInst
from cs3_web_services import settings
from common import baseConnector, csstatus, csdefine, stringRes, LogDefine, Functions, SQLConfig, ItemTypeEnum, \
	DBConnectInterface
from common import tooldefine
from common import Functions
from . import login
from . import GMActionLog
logInstance = GMActionLog.g_logInstance

g_baseappConnector = baseConnector.g_baseappConnector
loginInstannce = login.g_loginInstance

itemPath = Functions.getSeverConfigPath() + "/Item/ItemData.json"
ItemData = Functions.loadJsonDataByFile(itemPath)

ITEM_TYPE_ADD_DEL = 1  # 添加、删除物品
ITEM_TYPE_TRADE = 2  # 交易
ITEM_TYPE_EQUIP = 3  # 装备记录

PET_QUERY_TYPE_NAME = 1  # 幻兽名字
PET_QUERY_TYPE_UID = 2  # 幻兽UID
PET_QUERY_TYPE_DICT = {
	"petName": PET_QUERY_TYPE_NAME,
	"petUid": PET_QUERY_TYPE_UID,
}

def intensifyDataToDict(data):
	tempData = {}
	for key, value in data.items():
		propertyList = value[1].split(":")
		for propertyStr in propertyList:
			for property in propertyStr.split("|"):
				propertyData = property.split("#")
				if int(propertyData[0]) not in tempData:
					tempData[int(propertyData[0])] = 0
				tempData[int(propertyData[0])] += int(propertyData[1])
				
	return tempData


class RolePet:
	"""
	幻兽
	"""
	_instance = None

	def __init__(self):
		self.petChangeRecord = []

	@staticmethod
	def instance():
		if RolePet._instance == None:
			RolePet._instance = RolePet()
		return RolePet._instance

	def getPetHtmlBaseData(self, request):
		"""
		"""
		context = {"error": "", "roleInfo": {}, "rolePetBaseInfos": {}, "petChangeInfos": [], "petBookInfos": {},	"petComposeInfos": {}, "petChangeQueryInfo": {},
			"petBookQueryInfo": {}, "petComposeQueryInfo": {}, "petBaseInfo": {}, "attrSkillInfo": [], "passiveSkillInfo": []}
		context["sendFlag"] = request.POST.get("send_flag", None)
		context["roleInfo"]["roleName"] = request.POST.get("roleName", "")
		# 变更
		context["petChangeQueryInfo"]["queryType"] = PET_QUERY_TYPE_DICT.get(request.POST.get("changeQueryType", ""),
			PET_QUERY_TYPE_NAME)
		context["petChangeQueryInfo"]["queryText"] = request.POST.get("changeQueryText", "")
		# 打书
		context["petBookQueryInfo"]["queryType"] = PET_QUERY_TYPE_DICT.get(request.POST.get("bookQueryType", ""), PET_QUERY_TYPE_NAME)
		context["petBookQueryInfo"]["queryText"] = request.POST.get("bookQueryText", "")
		context["petBookQueryInfo"]["startDate"] = request.POST.get("bookStartDate", "")
		context["petBookQueryInfo"]["startTime"] = request.POST.get("bookStartTime", "")
		context["petBookQueryInfo"]["endDate"] = request.POST.get("bookEndDate", "")
		context["petBookQueryInfo"]["endTime"] = request.POST.get("bookEndTime", "")
		# 合成
		context["petComposeQueryInfo"]["queryType"] = PET_QUERY_TYPE_DICT.get(request.POST.get("composeQueryType", ""),
			PET_QUERY_TYPE_NAME)
		context["petComposeQueryInfo"]["queryText"] = request.POST.get("composeQueryText", "")
		context["petComposeQueryInfo"]["startDate"] = request.POST.get("composeStartDate", "")
		context["petComposeQueryInfo"]["startTime"] = request.POST.get("composeStartTime", "")
		context["petComposeQueryInfo"]["endDate"] = request.POST.get("composeEndDate", "")
		context["petComposeQueryInfo"]["endTime"] = request.POST.get("composeEndTime", "")

		return context

	def arraRolePetInfos(self, datas):
		"""
		整理玩家现有幻兽信息
		"""
		tempDatas = []
		for data in datas:
			tempDict = {}
			tempDict["name"] = data["name"]
			tempDict["uname"] = data["uname"]
			tempDict["uid"] = data["uid"]
			tempDict["level"] = data["level"]
			tempDict["quality"] = stringRes.PET_QUALITY_DICT.get(int(data["quality"]), data["quality"])
			tempDict["state"] = "出战" if data["isActive"] else "休息"
			tempDict["position"] = ""
			tempDatas.append(tempDict)
		return tempDatas

	def arraRolePetChangeRecord(self, datas, result_queryActivePetUID):
		"""
		整理幻兽变更记录信息
		"""
		tempDatas = []
		for data in datas:
			tempDict = {}
			if not data[2].strip():
				tempDict["name"] = data[3]
			else:
				tempDict["name"] = data[2]
			tempDict["uname"] = data[3]
			tempDict["uid"] = data[4]
			if int(tempDict["uid"]) == result_queryActivePetUID:
				tempDict["state"] = True
			else:
				tempDict["state"] = False
			tempDict["quality"] = stringRes.PET_QUALITY_DICT.get(data[5], 0)
			tempDict["level"] = data[6]
			tempDict["optTime"] = data[7]
			if data[8] == 1:
				tempDict["getReason"] = stringRes.PET_ADD_REASON_DICT.get(int(data[9]))
			else:
				tempDict["getReason"] = ""
			tempDict["optContent"] = stringRes.PET_ACTION_DICT.get(data[8])
			tempDict["index"] = len(tempDatas)
			tempDict["petData"] = pickle.loads(eval(data[10]))
			tempDatas.append(tempDict)
		return tempDatas

	def getRolePetInfos(self, request, roleName):
		"""
		获取玩家现有幻兽信息
		"""
		cmd_msg = {}
		cmd_msg["info"] = {}
		cmd_msg["info"]["roleName"] = roleName
		# 现有幻兽
		cmd_msg["cmd"] = "queryRolePetInfos"
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultInfos = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			return (tooldefine._MSG_ERROR, resultInfos)
		return(tooldefine._MSG_SUCCEED,  self.arraRolePetInfos(resultInfos["datas"]))

	def queryRolePetInfos(self, context, html_template, request):
		"""
		查看玩家现有幻兽信息
		"""
		datas = []
		roleName = request.POST.get("roleName", "")
		if not roleName:
			context["error"] = csstatus.MAIL_SEND_NOT_ROLE_INFO
			return render(request, html_template, context)
		result, resultInfos = self.getRolePetInfos(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["rolePetBaseInfos"] = resultInfos
		return render(request, html_template, context)

	def queryRolePetChangeRecord(self, context, html_template, request):
		"""
		查看幻兽变更记录
		"""
		if not context["roleInfo"]["roleName"].strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		sql = "select roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, updatetime, action, param1, petData from %s" % SQLConfig.LOG_TYPE_PET
		sql += " where (action = 1 or action = 2 or action = 5) and roleName = '%s'" % context["roleInfo"]["roleName"]
		if context["petChangeQueryInfo"]["queryText"]:
			if context["petChangeQueryInfo"]["queryType"] == PET_QUERY_TYPE_NAME:
				sql += " and petUname = '%s'" % context["petChangeQueryInfo"]["queryText"]
			elif context["petChangeQueryInfo"]["queryType"] == PET_QUERY_TYPE_UID:
				sql += " and petUid = '%s'" % context["petChangeQueryInfo"]["queryText"]
		results = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(results) == 0:
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		sql_queryActivePetUID = "select sm__activePetUID from tbl_Role where sm_playerName = '%s'" % context["roleInfo"]["roleName"]
		result_queryActivePetUID = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryActivePetUID)
		datas = self.arraRolePetChangeRecord(results, result_queryActivePetUID[0][0])
		self.petChangeRecord = datas
		context["petChangeInfos"] = datas
		return render(request, html_template, context)

	def queryRolePetBookRecord(self, context, html_template, request):
		"""
		查看玩家幻兽打书记录
		"""
		if not context["roleInfo"]["roleName"].strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		sql = "select action, roleDBID, roleName, petName, petUname, petUid, param1, param2, param3, param4, param5, param6, param7, updateTime from %s" % SQLConfig.LOG_TYPE_PET
		sql += " where (action = %s or action = %s) and roleName = '%s'" % (LogDefine.LT_PET_REPLACE_SKILL, LogDefine.LT_PET_SKILL_UPGRADE, context["roleInfo"]["roleName"])
		queryType = context["petBookQueryInfo"]["queryType"]
		queryText = context["petBookQueryInfo"]["queryText"]
		if queryText:
			if queryType == PET_QUERY_TYPE_NAME:
				sql += " and petUname = '%s'" % queryText
			elif queryType == PET_QUERY_TYPE_UID:
				sql += " and petUid = '%s'" % queryText
		startDate = context["petBookQueryInfo"]["startDate"]
		startTime = context["petBookQueryInfo"]["startTime"]
		endDate = context["petBookQueryInfo"]["endDate"]
		endTime = context["petBookQueryInfo"]["endTime"]
		if (not startDate and startTime) or (not endDate and endTime):
			context["error"] = csstatus.QUERY_TIME_FORMAT_ERROR
			return render(request, html_template, context)
		if startDate and not startTime:
			sql += " and updatetime >= '%s'" % (startDate + " 00:00:00")
		elif startDate and startTime:
			sql += " and updatetime >= '%s'" % (startDate + " " + startTime)
		if endDate and not endTime:
			sql += " and updatetime <= '%s'" % (endDate + " 00:00:00")
		elif endDate and endTime:
			sql += " and updatetime <= '%s'" % (endDate + " " + endTime)
		results = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(results) == 0:
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		context["petBookInfos"] = []
		skillTablePath = Functions.getSeverConfigPath() + '/Skill/SkillConfigs/SkillTable.json'
		with open(skillTablePath, encoding='utf-16') as skillTempleData:
			skillData = json.load(skillTempleData)
		for result in results:
			petBookInfo = {}
			if not result[3].strip():
				petBookInfo["name"] = result[3]
			else:
				petBookInfo["name"] = result[4]
			petBookInfo["uid"] = result[5]
			petBookInfo["newSkillName"] = petBookInfo["oldSkillName"] = ""
			for skill in skillData:
				if int(skill["Name"]) == int(result[7]):
					petBookInfo["newSkillName"] = skill["SkillName"]
				elif int(skill["Name"]) == int(result[8]):
					petBookInfo["oldSkillName"] = skill["SkillName"]
				if petBookInfo["newSkillName"] and petBookInfo["oldSkillName"]:
					break
			if int(result[0]) == LogDefine.LT_PET_REPLACE_SKILL:
				petBookInfo["actionType"] = stringRes.LT_PET_REPLACE_SKILL_DICT[int(result[6])]
				petBookInfo["useQiHuaDan"] = result[11]
				petBookInfo["useMoney"] = result[12]
				petBookInfo["usePotential"] = ""
				petBookInfo["useBook"] = ""
				petBookInfo["useSoulbead"] = ""
				if int(result[6]) == LogDefine.LT_PET_REPLACE_SKILL_ACTIVE:
					itemData = ItemData.get(str(result[10]), {})
					if itemData:
						petBookInfo["activeBook"] = itemData["ItemName"]
						petBookInfo["passiveBook"] = ""
						petBookInfo["activeSkillNum"] = result[9]
						petBookInfo["passiveSkillNum"] = ""
				else:
					itemData = ItemData.get(str(result[10]), {})
					if itemData:
						petBookInfo["activeBook"] = ""
						petBookInfo["passiveBook"] = itemData["ItemName"]
						petBookInfo["activeSkillNum"] = ""
						petBookInfo["passiveSkillNum"] = result[9]
			elif int(result[0]) == LogDefine.LT_PET_SKILL_UPGRADE:
				petBookInfo["actionType"] = stringRes.PET_SKILL_UPGRADE_DICT[int(result[6])]
				petBookInfo["useQiHuaDan"] = ""
				petBookInfo["useMoney"] = result[10]
				petBookInfo["usePotential"] = result[9]
				petBookInfo["useBook"] = result[11]
				petBookInfo["useSoulbead"] = result[12]
				petBookInfo["activeBook"] = petBookInfo["passiveBook"] = petBookInfo["activeSkillNum"] = petBookInfo["passiveSkillNum"] = ""
			petBookInfo["optTime"] = result[13]
			context["petBookInfos"].append(petBookInfo)
		return render(request, html_template, context)

	def queryRolePetComposeRecord(self, context, html_template, request):
		"""
		查看玩家幻兽合成记录
		"""
		if not context["roleInfo"]["roleName"].strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		sql = "select roleDBID, roleName, petName, petUname, petUid, param1, param2, param3, param6, param7, param8, param9, updateTime from %s" % SQLConfig.LOG_TYPE_PET
		sql += " where action = %s and roleName = '%s'" % (LogDefine.LT_PET_COMPOSE, context["roleInfo"]["roleName"])
		queryType = context["petComposeQueryInfo"]["queryType"]
		queryText = context["petComposeQueryInfo"]["queryText"]
		if queryText:
			if queryType == PET_QUERY_TYPE_NAME:
				sql += " and petUname = '%s'" % queryText
			elif queryType == PET_QUERY_TYPE_UID:
				sql += " and petUid = '%s'" % queryText
		startDate = context["petComposeQueryInfo"]["startDate"]
		startTime = context["petComposeQueryInfo"]["startTime"]
		endDate = context["petComposeQueryInfo"]["endDate"]
		endTime = context["petComposeQueryInfo"]["endTime"]
		if (not startDate and startTime) or (not endDate and endTime):
			context["error"] = csstatus.QUERY_TIME_FORMAT_ERROR
			return render(request, html_template, context)
		if startDate and not startTime:
			sql += " and updatetime >= '%s'" % (startDate + " 00:00:00")
		elif startDate and startTime:
			sql += " and updatetime >= '%s'" % (startDate + " " + startTime)
		if endDate and not endTime:
			sql += " and updatetime <= '%s'" % (endDate + " 00:00:00")
		elif endDate and endTime:
			sql += " and updatetime <= '%s'" % (endDate + " " + endTime)
		results = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(results) == 0:
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		context["petComposeInfos"] = []
		for result in results:
			composeInfo={}
			if not result[2].strip():
				composeInfo["onePetName"] = result[3]
			else:
				composeInfo["onePetName"] = result[2]
			composeInfo["onePetUid"] = result[4]
			if not result[5].strip():
				composeInfo["twoPetName"] = result[6]
			else:
				composeInfo["twoPetName"] = result[5]
			composeInfo["twoPetUid"] = result[7]
			composeInfo["useXianshi"] = result[11]
			composeInfo["useMoney"] = result[10]
			composeInfo["abilityChangeValue"] = int(result[8]) - int(result[9])
			composeInfo["optTime"] = result[12]
			context["petComposeInfos"].append(composeInfo)
		return render(request, html_template, context)

	def queryPetAttributeInfo(self, context, html_template, request):
		"""
		查看幻兽的详细信息
		"""
		petInfoIndex = request.GET.get("petInfoIndex", "")
		context["petChangeInfos"] = self.petChangeRecord
		attrSkillBox = passiveSkillBox = []
		for data in self.petChangeRecord:
			if int(petInfoIndex) == int(data["index"]):
				context["petBaseInfo"] = data["petData"]
				context["petBaseInfo"].update(data)
				attrSkillBox = context["petBaseInfo"]["attrSkillBox"]
				passiveSkillBox = context["petBaseInfo"]["passiveSkillBox"]
				break
		skillTablePath = Functions.getSeverConfigPath()+'/Skill/SkillConfigs/SkillTable.json'
		with open(skillTablePath, encoding='utf-16') as skillTempleData:
			skillData = json.load(skillTempleData)
		attrSkillInfo = passiveSkillInfo = ["", "", "", "", ""]
		i = j = 0
		for data in skillData:
			for attrSkill in attrSkillBox:
				if int(attrSkill) == int(data["Name"]):
					attrSkill = data["SkillName"]
					attrSkillInfo[i] = attrSkill
					i = i + 1
			for passiveSkill in passiveSkillBox:
				if int(passiveSkill) == int(data["Name"]):
					passiveSkill = data["SkillName"]
					passiveSkillInfo[j] = passiveSkill
					j = j + 1
		context["attrSkillInfo"] = attrSkillInfo
		context["passiveSkillInfo"] = passiveSkillInfo
		return render(request, html_template, context)

	def query(self, request):
		html_template = "gmtools/role/role_query_pet.html"
		context = self.getPetHtmlBaseData(request)
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_QUERY_PET]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if "rolePetQueryBtn" in request.POST:
			return self.queryRolePetInfos(context, html_template, request)
		elif "petChangeQueryBtn" in request.POST:
			return self.queryRolePetChangeRecord(context, html_template, request)
		elif "petBookQueryBtn" in request.POST:
			return self.queryRolePetBookRecord(context, html_template, request)
		elif "petComposeQueryBtn" in request.POST:
			return self.queryRolePetComposeRecord(context, html_template, request)
		elif "petInfoIndex" in request.GET:
			return self.queryPetAttributeInfo(context, html_template, request)
		return render(request, html_template, context)


class RoleItem:
	"""
	道具（物品）
	"""
	_instance = None

	def __init__(self):
		pass

	@staticmethod
	def instance():
		if RoleItem._instance == None:
			RoleItem._instance = RoleItem()
		return RoleItem._instance

	def getItemHtmlBaseData(self, request):
		"""
		"""
		context = {"roleInfo": {}, "roleItemBaseInfos": {}, "itemAddDelInfos": {}, "itemChangeQueryData": {}, "itemTradeInfos": {},"equipChangeInfos": {}, "error": ""}
		context["sendFlag"] = request.POST.get("send_flag")
		context["roleInfo"]["roleName"] = request.POST.get("roleName", "")
		context["itemChangeQueryData"]["itemChangeQueryText"] = request.POST.get("itemChangeQueryText", "")
		return context

	def arraRoleItemInfos(self, datas):
		"""
		"""
		tempDatas = []
		for data in datas:
			tempDict = {}
			tempDict["name"] = data["itemName"]
			tempDict["quality"] = stringRes.ITEM_QUALITY_CH_DICT[data["quality"]]
			tempDict["amount"] = data["itemAmount"]
			tempDict["position"] = data["order"]
			order = data["order"]
			if order >= ItemTypeEnum.BAG_EQUIPSTART and order <= ItemTypeEnum.BAG_EQUIPEND:
				tempDict["position"] = stringRes.ITEM_ORDER_DICT[csdefine.ITEM_ORDER_WEAR]
			elif order >= ItemTypeEnum.BAG_COMMONSTART and order <= ItemTypeEnum.BAG_SPAREND:
				tempDict["position"] = stringRes.ITEM_ORDER_DICT[csdefine.ITEM_ORDER_BAG]
			elif order >= ItemTypeEnum.BAG_STORESTART and order <= ItemTypeEnum.BAG_STOREEND:
				tempDict["position"] = stringRes.ITEM_ORDER_DICT[csdefine.ITEM_ORDER_STORE]
			tempDatas.append(tempDict)
		return tempDatas

	def getRoleItemInfos(self, request, roleName):
		"""
		获取玩家现有物品信息
		"""
		datas = []
		sqlRoleName = "select id,sm__activePetUID from tbl_Role where sm_playerName = '%s'" % roleName
		resultDBID = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sqlRoleName)
		if not resultDBID:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		sqlRoleDBID = "select sm_id, sm_amount, sm_order from tbl_Role_itemsBag_items where parentID = %s" % \
					  resultDBID[0][0]
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sqlRoleDBID)
		itemList = []
		for data in results:
			itemID, amount, order = data
			itemData = ItemData.get(str(itemID), {})
			if itemData:
				itemList.append(
					{"itemName": itemData["ItemName"], "itemAmount": int(amount), "quality": itemData["Quality"],
					 "order": int(order)})
		resultInfos = {"datas": itemList}
		datas.extend(resultInfos["datas"])
		# 仓库物品
		sqlRoleDBID = "select sm_item_id, sm_item_amount, sm_item_order from tbl_Role_storeItems_bag where parentID = %s" % \
					  resultDBID[0][0]
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sqlRoleDBID)
		itemList = []
		for data in results:
			itemID, amount, order = data
			itemData = ItemData.get(str(itemID), {})
			if itemData:
				itemList.append(
					{"itemName": itemData["ItemName"], "itemAmount": int(amount), "quality": itemData["Quality"],
					 "order": int(order)})
		resultInfos = {"datas": itemList}
		datas.extend(resultInfos["datas"])
		return(tooldefine._MSG_SUCCEED, self.arraRoleItemInfos(datas))

	def queryRoleItemInfos(self, context, html_template, request):
		"""
		查询玩家现有物品信息
		"""
		datas = []
		roleName = request.POST.get("roleName", "")
		if not roleName:
			context["error"] = csstatus.MAIL_SEND_NOT_ROLE_INFO
			return render(request, html_template, context)
		result, resultInfos = self.getRoleItemInfos(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleItemBaseInfos"] = resultInfos
		return render(request, html_template, context)

	def arraItemAddDelRecord(self, datas):
		"""
		整理添加、删除物品记录
		"""
		tempDatas = []
		for data in datas:
			tempDict = {}
			tempDict["roleName"] = data[2]
			tempDict["itemName"] = data[3]
			tempDict["itemID"] = data[4]
			tempDict["itemUid"] = data[5]
			tempDict["itemAmount"] = data[6]
			tempDict["optTime"] = data[0]
			tempDict["optType"] = stringRes.ITEM_ADD_DEL_TYPE_DICT.get(int(data[1]), data[1])
			tempDict["dataType"] = ITEM_TYPE_ADD_DEL
			packData = pickle.loads(eval(data[10]))
			tempDict["dbid"] = int(data[11])
			if int(data[1]) == LogDefine.LT_ITEM_ADD:
				tempDict["optReason"] = stringRes.ITEM_ADD_REASON_DICT.get(int(data[8]), data[8])
			elif int(data[1]) == LogDefine.LT_ITEM_DEL:
				tempDict["optReason"] = stringRes.ITEM_DEL_REASON_DICT.get(int(data[8]), data[8])
			if packData:
				tempDict["isEquip"] = True
			else:
				tempDict["isEquip"] = False
			tempDatas.append(tempDict)
		return tempDatas

	def arraItemTradeRecord(self, datas):
		"""
		整理交易记录
		"""
		tempDatas = []
		for data in datas:
			tradeType = int(data[1])
			tempDict = {"money": 0, "xianshi": 0, "lingshi": 0, "xuanshi": 0, "tRoleName": ""}
			tempDict["roleName"] = data[2]
			tempDict["tradeTime"] = data[0]
			tempDict["tradeType"] = stringRes.ITEM_TRADE_TYPE_DICT.get(tradeType, tradeType)
			tempDict["dataType"] = ITEM_TYPE_TRADE
			packData = pickle.loads(eval(data[12]))
			tempDict["dbid"] = int(data[13])
			if packData:
				tempDict["isEquip"] = True
			else:
				tempDict["isEquip"] = False
			if tradeType == LogDefine.LT_TRADE_SWAP_ITEM:
				tempDict["tRoleName"] = data[4]
				tempDict["itemName"] = data[7]
				tempDict["itemID"] = data[5]
				tempDict["itemUid"] = data[6]
				tempDict["itemAmount"] = data[8]
				tempDict["money"] = int(data[9]) - int(data[10])
			elif tradeType == LogDefine.LT_TRADE_NPC_BUY or tradeType == LogDefine.LT_TRADE_BUY_BACK or tradeType == LogDefine.LT_TRADE_BUY_BACK_HIGH:
				tempDict["itemName"] = data[5]
				tempDict["itemID"] = data[3]
				tempDict["itemUid"] = data[4]
				tempDict["itemAmount"] = data[6]
				tempDict["money"] = 0 - int(data[7])  # 付钱
			elif tradeType == LogDefine.LT_TRADE_NPC_SELL or tradeType == LogDefine.LT_TRADE_RETURN_ITEM:
				tempDict["itemName"] = data[5]
				tempDict["itemID"] = data[3]
				tempDict["itemUid"] = data[4]
				tempDict["itemAmount"] = data[6]
				tempDict["money"] = int(data[7])
			elif tradeType == LogDefine.LT_TRADE_SHOP_BUY:
				tempDict["itemName"] = data[5]
				tempDict["itemID"] = data[3]
				tempDict["itemUid"] = data[4]
				tempDict["itemAmount"] = data[6]
				tempDict["xianshi"] = 0 - int(data[7])
				tempDict["lingshi"] = 0 - int(data[8])
				tempDict["xuanshi"] = 0 - int(data[9])
			elif tradeType == LogDefine.LT_TRADE_GIVING_GOOD:
				tempDict["itemName"] = data[6]
				tempDict["itemID"] = data[5]
				tempDict["itemUid"] = ""
				tempDict["itemAmount"] = data[7]
				tempDict["xianshi"] = 0 - int(data[8])
				tempDict["lingshi"] = 0 - int(data[10])
				tempDict["xuanshi"] = 0 - int(data[9])
				tempDict["money"] = 0 - int(data[11])
			tempDatas.append(tempDict)
		return tempDatas

	def arraItemEquipRecord(self, datas):
		"""
		整理装备操作记录
		"""
		tempDatas = []
		for data in datas:
			tempDict = {}
			tempDict["roleName"] = data[2]
			tempDict["itemID"] = data[3]
			tempDict["itemUid"] = data[4]
			tempDict["itemName"] = data[5]
			tempDict["itemAmount"] = data[6]
			tempDict["optTime"] = data[0]
			tempDict["dataType"] = ITEM_TYPE_EQUIP
			tempDict["dbid"] = int(data[17])
			action = int(data[1])
			tempDict["optType"] = stringRes.EQUIP_OPT_TYPE_DICT.get(action, action)
			tempDict["isEquip"] = True
			if action == LogDefine.LT_EQUIP_INTENSIFY or action == LogDefine.LT_EQUIP_BACKFIRE:	#强化，回火
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr(pickle.loads(eval(data[15])), pickle.loads(eval(data[16])))
			elif action == LogDefine.LT_EQUIP_COMPOSE:	#打造
				tempDict["attributeChange"] = ""
			elif action == LogDefine.LT_EQUIP_SHUFFLE_REPLACE:	#洗练替换
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr(pickle.loads(eval(data[15])), pickle.loads(eval(data[16])))
			elif action == LogDefine.LT_EQUIP_RECAST:	#重铸
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr({}, pickle.loads(eval(data[15])))
			elif action == LogDefine.LT_EQUIP_REPAIR:	#修理
				tempDict["attributeChange"] = stringRes.EQUIP_ATTRIBUTE_TYPE_DICT.get("hardiness") + "+"+ str(int((int(data[8]) - int(data[7])) / 10000))
			elif action == LogDefine.LT_EQUIP_RESTORE:	#还原
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr(pickle.loads(eval(data[14])), pickle.loads(eval(data[15])))
			elif action == LogDefine.LT_EQUIP_TRAN_STAR:	#传星
				changeData = intensifyDataToDict(pickle.loads(eval(data[15])))
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr({}, changeData)
			elif action == LogDefine.LT_EQUIP_SAVE:	#保存
				changeData = intensifyDataToDict(pickle.loads(eval(data[15])))
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr({}, changeData)
			elif action == LogDefine.LT_EQUIP_SHUFFLE:	#洗练
				tempDict["attributeChange"] = Functions.equipAttributeChangeStr(pickle.loads(eval(data[15])), pickle.loads(eval(data[16])))
			tempDatas.append(tempDict)
			
		return tempDatas

	def getItemAddDelRecord(self, context, request):
		"""
		获取添加、删除物品记录
		"""
		sql = "select updateTime, action, roleName, itemName, itemID, itemUid, itemNum, param1, param2, param3, itemData, id from %s" % SQLConfig.LOG_TYPE_ITEM

		if context["roleInfo"]["roleName"]:
			sql += " where roleName = '%s'" % context["roleInfo"]["roleName"]
		if context["itemChangeQueryData"]["itemChangeQueryText"]:
			if context["roleInfo"]["roleName"]:
				sql += " and itemName = '%s'" % context["itemChangeQueryData"]["itemChangeQueryText"]
			else:
				sql += " where itemName = '%s'" % context["itemChangeQueryData"]["itemChangeQueryText"]

		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		datas = self.arraItemAddDelRecord(resultInfos)
		return datas

	def getItemTradeRecord(self, context, request):
		"""
		获取物品交易记录
		"""
		sql = "select updateTime, action, roleName, param1, param2, param3, param4, param5, param6, param7, param8, param9, itemData, id from %s" \
			  % SQLConfig.LOG_TYPE_TRADE
		changeQueryText = context["itemChangeQueryData"]["itemChangeQueryText"]
		if changeQueryText:
			# 和玩家交易、赠送
			sql += " where ((action = %s and param5 = '%s') or (action = %s and param4 = '%s'))" % (
			LogDefine.LT_TRADE_SWAP_ITEM, changeQueryText, LogDefine.LT_TRADE_GIVING_GOOD, changeQueryText)
			# 在NPC处买东西、回购、高价回购、卖东西给NPC、退货、在商城买东西
			sql += " or ((action = %s or action = %s or action = %s or action = %s or action = %s or action = %s) and param3 = '%s')" % (
			LogDefine.LT_TRADE_NPC_BUY,
			LogDefine.LT_TRADE_BUY_BACK, LogDefine.LT_TRADE_BUY_BACK_HIGH, LogDefine.LT_TRADE_NPC_SELL,
			LogDefine.LT_TRADE_RETURN_ITEM,
			LogDefine.LT_TRADE_SHOP_BUY, changeQueryText)
		else:
			# 和玩家交易、赠送、#在NPC处买东西、回购、高价回购、卖东西给NPC、退货、在商城买东西
			sql += " where (action = %s or action = %s or action = %s or action = %s or action = %s or action = %s or action = %s or action = %s)" % \
				(LogDefine.LT_TRADE_SWAP_ITEM, LogDefine.LT_TRADE_GIVING_GOOD, LogDefine.LT_TRADE_NPC_BUY,
					LogDefine.LT_TRADE_BUY_BACK, LogDefine.LT_TRADE_BUY_BACK_HIGH, LogDefine.LT_TRADE_NPC_SELL, 
					LogDefine.LT_TRADE_RETURN_ITEM, LogDefine.LT_TRADE_SHOP_BUY)
		if context["roleInfo"]["roleName"]:
			sql += " and roleName = '%s'" % context["roleInfo"]["roleName"]
		
		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		datas = self.arraItemTradeRecord(resultInfos)
		return datas

	def getItemEquipRecord(self, context, request):
		"""
		获取装备操作记录
		"""  # action, roleDBID, roleName, param1, param2 , param3, param4, param5, param6, param7, param8, param9, equipData
		sql = "select updatetime, action, roleName, itemID, itemUid, itemName, itemNum, param1, param2, param3, param4, param5, param6, \
			param7, param8, param9, param10, id from %s" % SQLConfig.LOG_TYPE_EQUIP
		#conditon = "(action != %s and action != %s)" % (LogDefine.LT_EQUIP_SHUFFLE, LogDefine.LT_EQUIP_SAVE)#不包括装备洗练和装备保存
		#sql += " where %s" % conditon
		if context["itemChangeQueryData"]["itemChangeQueryText"]:
			#和玩家交易、赠送
			sql += " where itemName = '%s'" % context["itemChangeQueryData"]["itemChangeQueryText"]
		if context["roleInfo"]["roleName"]:
			if context["itemChangeQueryData"]["itemChangeQueryText"]:
				sql += " and roleName = '%s'" % context["roleInfo"]["roleName"]
			else:
				sql += " where roleName = '%s'" % context["roleInfo"]["roleName"]
		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		datas = self.arraItemEquipRecord(datas)
		return datas

	def queryRoleItemChangeRecord(self, context, html_template, request):
		"""
		查看玩家物品变更记录
		"""
		# 1添加、删除物品 2.物品交易 3.装备操作
		datas = []
		# 添加、删除物品，包括转入/转出仓库
		addDelResultInfos = self.getItemAddDelRecord(context, request)
		context["itemAddDelInfos"] = addDelResultInfos
		context["itemAddDelType"] = ITEM_TYPE_ADD_DEL
		# 物品交易
		tradeResultInfos = self.getItemTradeRecord(context, request)
		context["itemTradeInfos"] = tradeResultInfos
		context["itemTradeType"] = ITEM_TYPE_TRADE
		# 包括转入/转出仓库
		equipResultInfos = self.getItemEquipRecord(context, request)
		context["equipChangeInfos"] = equipResultInfos
		context["equipChangeType"] = ITEM_TYPE_EQUIP
		return render(request, html_template, context)

	def queryEquipInfosxxx(self, request):
		"""
		查看装备的详细信息
		"""

		dataType = request.GET.get("dataType")
		index = request.GET.get("index")
		equipInfo = self._itemChangeRecords[int(dataType)][int(index)]
		equipData = {}
		packData = equipInfo["packData"]
		equipData["itemName"] = equipInfo["itemName"]
		equipData["itemID"] = equipInfo["itemID"]
		equipData["itemUid"] = equipInfo["itemUid"]
		equipData["level"] = packData["level"]
		equipData["quality"] = packData["quality"]
		equipData["combatPower"] = packData["combatPower"]
		equipData["hardiness"] = packData["hardiness"]
		equipData["classes"] = Functions.getEquipClasses(int(packData["classes"]))
		equipData["order"] = stringRes.EQUIP_ORDER_DICT.get(int(packData["order"]), packData["order"])
		equipData["price"] = packData["price"]
		equipData["bindType"] = packData["bindType"]
		equipData["attributeAddition"] = ""
		for key, value in packData["extra"].items():
			equipData["attributeAddition"] += stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(int(key), str(key)) + "+" + str(value) + " "
	
		html_template = "gmtools/role/role_query_item_equip.html"
		context = {"equipData": equipData}
		return render(request, html_template, context)

	def queryEquipInfos(self, request):
		"""
		查看装备的详细信息
		"""
		html_template = "gmtools/role/role_query_item_equip.html"
		context = {"equipData": {}}
		dataType = request.GET.get("dataType")
		itemName = request.GET.get("itemName")
		itemID = request.GET.get("itemID")
		itemUid = request.GET.get("itemUid")
		dbid = request.GET.get("dbid")
		if int(dataType) == ITEM_TYPE_ADD_DEL:
			sql = "select itemData from %s where id = %i " % (SQLConfig.LOG_TYPE_ITEM, int(dbid))
		elif int(dataType) == ITEM_TYPE_EQUIP:
			sql = "select equipData from %s where id = %i " % (SQLConfig.LOG_TYPE_EQUIP, int(dbid))
		elif int(dataType) == ITEM_TYPE_TRADE:
			sql = "select itemData from %s where id = %i " % (SQLConfig.LOG_TYPE_TRADE, int(dbid))

		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(datas) <= 0:
			return render(request, html_template, context)
		equipData = {}
		packData = pickle.loads(eval(datas[0][0]))
		equipData["itemName"] = itemName
		equipData["itemID"] = itemID
		equipData["itemUid"] = itemUid
		equipData["level"] = packData["level"]
		equipData["quality"] = packData["quality"]
		equipData["combatPower"] = packData["combatPower"]
		equipData["hardiness"] = packData["hardiness"]
		equipData["classes"] = Functions.getEquipClasses(int(packData["classes"]))
		equipData["order"] = stringRes.EQUIP_ORDER_DICT.get(int(packData["order"]), packData["order"])
		equipData["price"] = packData["price"]
		equipData["bindType"] = packData["bindType"]
		equipData["attributeAddition"] = ""
		for key, value in packData["extra"].items():
			equipData["attributeAddition"] += stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(int(key), str(key)) + "+" + str(
				value) + " "

		html_template = "gmtools/role/role_query_item_equip.html"
		context = {"equipData": equipData}
		return render(request, html_template, context)

	def query(self, request):
		html_template = "gmtools/role/role_query_item.html"
		context = self.getItemHtmlBaseData(request)
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_QUERY_ITEM]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if "queryEquipInfoFlag" in request.GET:
			return self.queryEquipInfos(request)
		if not context["sendFlag"]:
			return render(request, html_template, context)
		if "roleItemQueryBtn" in request.POST:
			return self.queryRoleItemInfos(context, html_template, request)
		elif "itemChangeQueryBtn" in request.POST:
			return self.queryRoleItemChangeRecord(context, html_template, request)

		return render(request, html_template, context)


class RoleManager:
	"""
	角色管理器
	"""
	_instance = None

	def __init__(self):
		pass

	@staticmethod
	def instance():
		if RoleManager._instance == None:
			RoleManager._instance = RoleManager()
		return RoleManager._instance

	def getNextPage(self, page, totalPage):
		"""
		检测是否有“下一页”标签
		:param page: 当前页
		:param totalPage: 总页数
		:return: 有返回下一页，没有返回-1
		"""
		if page == totalPage:
			return -1
		return page + 1

	def getPrevPage(self, page):
		"""
		检测是否有“上一页”标签
		:param page: 当前页
		:param totalPage: 总页数
		:return: 有返回1，没有返回0
		"""
		if page == 1:
			return -1
		return page - 1

	def getQueryIndex(self, index, recordNum=tooldefine.QUERY_ONCE_NUM_):
		"""
		获得查询记录开始和结尾序号
		:param index: 当前页号
		:param recordNum:查询记录数
		:return:查（起始序号，结尾序号）
		"""
		return (index, recordNum)

	@loginInstannce.login_check
	def role(self, request):
		"""
		"""
		html_template = "gmtools/role/role.html"
		return render(request, html_template, {})

	@loginInstannce.login_check
	def role_kick(self, request):
		"""
		踢人
		"""
		html_template = "gmtools/role/role_kick.html"
		context = self.role_kick_init()
		sendFlag = request.POST.get("send_flag")
		roleName = request.POST.get("roleName", "")
		if not sendFlag:
			return render(request, html_template, context)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_KICK_ROLE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		cmd_msg = {}
		cmd_msg["cmd"] = "doActionForPlayer"
		cmd_msg["info"] = {}
		cmd_msg["info"]["cmd_interface"] = "kickPlayer"
		cmd_msg["info"]["roleName"] = roleName
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultInfos = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.kickRoleLog(request.session["gm_userid"], request.session["gm_level"], roleName, "", currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.OPERATION_SUCCEED
		context["roleName"] = roleName
		return render(request, html_template, context)

	def role_kick_init(self):
		return {"error": "", "success": "", "roleName": ""}

	@loginInstannce.login_check
	def role_freeze(self, request):
		"""
		冻结角色
		"""
		html_template = "gmtools/role/role_freeze.html"
		send_flag = request.POST.get("send_flag")
		roleName = request.GET.get("roleName", "")
		time = float(request.POST.get("time", 0))
		reason = request.POST.get("reason", "")
		name = request.POST.get("roleName", "")
		if name.strip():
			roleName = name
		context = {"error": "", "success": "", "roleName": roleName, "reason": reason, "lock_time": time}
		if not send_flag:
			return render(request, html_template, context)

		if time <= 0:
			context["error"] = csstatus.ROLE_FREEZE_TIME_ERROR
			return render(request, html_template, context)

		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render(request, html_template, context)

		cmd_msg = {}
		cmd_msg["cmd"] = "freezeRole"
		cmd_msg["info"] = {}
		cmd_msg["info"]["roleName"] = roleName
		cmd_msg["info"]["time"] = int(time*60*60)
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
			return render(request, html_template, context)
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.freezeRoleLog(request.session["gm_userid"], request.session["gm_level"], roleName, reason, currServerkey,  request.serverInfos.get(currServerkey, ""))
			context["success"] = csstatus.OPERATION_SUCCEED
			return render(request, html_template, context)

	@loginInstannce.login_check
	def role_unfreeze(self, request):
		"""
		角色解除冻结
		"""
		html_template = "gmtools/role/role_unfreeze.html"
		roleName = request.GET.get("roleName", "")
		send_flag = request.POST.get("send_flag")
		reason = request.POST.get("reason", "")
		name = request.POST.get("roleName", "")
		if name.strip():
			roleName = name
		context = {"error": "", "success": "", "roleName": roleName, "reason": reason}
		if not send_flag:
			return render(request, html_template, context)
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render(request, html_template, context)

		cmd_msg = {}
		cmd_msg["cmd"] = "unFreezeRole"
		cmd_msg["info"] = {}
		cmd_msg["info"]["roleName"] = roleName
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.unFreezeRoleLog(request.session["gm_userid"], request.session["gm_level"], roleName, reason, currServerkey, request.serverInfos.get(currServerkey, ""))
			context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)

	@loginInstannce.login_check
	def role_chat_unLockGag(self, request):
		"""
		解除禁言
		"""
		html_template = "gmtools/role/role_chat_unLockGag.html"
		POST = request.POST
		send_flag = POST.get("send_flag", "")
		context = {"error": "", "success": ""}
		name = request.GET.get("name")
		chatList = request.GET.get("chat_list")
		reason = POST.get("reason", "")
		context["name"] = name
		context["chat_list"] = chatList
		context["reason"] = reason
		gagData = ""
		if chatList:
			for i in range(len(chatList)):
				if int(chatList[i]) == 1:
					gagData += "[" + stringRes.CHAT_TYPE_DICT.get(i) + "]"
		if not gagData:
			gagData = "该玩家没有被禁言的聊天频道"
		context["gagData"] = gagData
		if not send_flag:
			return render(request, html_template, context)
		else:
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ROLE_MGR_UNGAG]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render( request, html_template, context )
				
			chat_nearby = request.POST.get("chat_nearby")
			chat_space = request.POST.get("chat_space")
			chat_world = request.POST.get("chat_world")
			chat_whisper = request.POST.get("chat_whisper")
			chat_group = request.POST.get("chat_group")
			chat_team = request.POST.get("chat_team")
			chat_collective = request.POST.get("chat_collective")
			chat_gang = request.POST.get("chat_gang")
			chat_alience = request.POST.get("chat_alience")
			chat_school = request.POST.get("chat_school")
			chat_camp = request.POST.get("chat_camp")
			chat_battilespace = request.POST.get("chat_battilespace")
			chat_tianyin = request.POST.get("chat_tianyin")
			chat_xianyin = request.POST.get("chat_xianyin")
			chat_system = request.POST.get("chat_system")
			chat_friend = request.POST.get("chat_friend")
			chatGagList = (chat_nearby, chat_space, chat_world, chat_whisper, chat_group,
				chat_team, chat_collective, chat_gang, chat_alience, chat_school,
				chat_camp, chat_battilespace, chat_tianyin, chat_xianyin,
				chat_system, chat_friend)
			gagList = []
			for i in range(len(chatGagList)):
				if chatGagList[i]:
					gagList.append(i)
			if not gagList:
				context["error"] = csstatus.CHAT_NEED_SELECT
				return render(request, html_template, context)
			connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
			cmd_msg = {}
			cmd_msg["cmd"] = "unGag"
			cmd_msg["info"] = {}
			cmd_msg["info"]["cmd_interface"] = "unLockGagForPlayer"
			cmd_msg["info"]["roleName"] = name
			cmd_msg["info"]["gag_list"] = gagList
			cmd_msg["info"]["reason"] = reason
			cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
			result, resultInfos = connector.send_msg(cmd_msg)
			if result == tooldefine._MSG_ERROR:
				context["error"] = resultInfos
				return render(request, html_template, context)
			else:
				tempGagList = [str(i) for i in gagList]
				currServerkey = request.session[tooldefine.CURR_SERVER]
				logInstance.unGagRoleLog(request.session["gm_userid"], request.session["gm_level"], name, "|".join(tempGagList), reason, currServerkey, request.serverInfos.get(currServerkey, ""))
				
				context["success"] = csstatus.OPERATION_SUCCEED
				return render(request, html_template, context)

	@loginInstannce.login_check
	def role_chat_gag(self, request):
		"""
		进行禁言
		"""
		html_template = "gmtools/role/role_chat_gag.html"
		POST = request.POST
		send_flag = POST.get("send_flag", "")
		reason = POST.get("reason", "")
		context = {"error": "", "success": ""}
		name = request.GET.get("name")
		chatList = request.GET.get("chat_list")
		context["name"] = name
		context["chat_list"] = chatList
		context["reason"] = reason
		gagData = ""
		if chatList:
			for i in range(len(chatList)):
				if int(chatList[i]) == 1:
					gagData += "[" + stringRes.CHAT_TYPE_DICT.get(i) + "]"
		context["gagData"] = gagData
		if not send_flag:
			return render(request, html_template, context)
		else:
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ROLE_MGR_GAG]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render( request, html_template, context )
				
			gagTime = POST.get("gagTime", "")
			if not gagTime:
				context["error"] = csstatus.CHAT_INPUT_TIME
				return render(request, html_template, context)
			chat_nearby = request.POST.get("chat_nearby")
			chat_space = request.POST.get("chat_space")
			chat_world = request.POST.get("chat_world")
			chat_whisper = request.POST.get("chat_whisper")
			chat_group = request.POST.get("chat_group")
			chat_team = request.POST.get("chat_team")
			chat_collective = request.POST.get("chat_collective")
			chat_gang = request.POST.get("chat_gang")
			chat_alience = request.POST.get("chat_alience")
			chat_school = request.POST.get("chat_school")
			chat_camp = request.POST.get("chat_camp")
			chat_battilespace = request.POST.get("chat_battilespace")
			chat_tianyin = request.POST.get("chat_tianyin")
			chat_xianyin = request.POST.get("chat_xianyin")
			chat_system = request.POST.get("chat_system")
			chat_friend = request.POST.get("chat_friend")
			chatGagList = (chat_nearby, chat_space, chat_world, chat_whisper, chat_group,
				chat_team, chat_collective, chat_gang, chat_alience, chat_school,
				chat_camp, chat_battilespace, chat_tianyin, chat_xianyin,
				chat_system, chat_friend)
			gagList = []
			for i in range(len(chatGagList)):
				if chatGagList[i]:
					gagList.append(i)
			if not gagList:
				context["error"] = csstatus.CHAT_NEED_SELECT
				return render(request, html_template, context)
			connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
			cmd_msg = {}
			cmd_msg["cmd"] = "gag"
			cmd_msg["info"] = {}
			cmd_msg["info"]["cmd_interface"] = "gagForPlayer"
			cmd_msg["info"]["roleName"] = name
			cmd_msg["info"]["gag_list"] = gagList
			cmd_msg["info"]["long_time"] = int(gagTime)
			cmd_msg["info"]["reason"] = reason
			cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
			result, resultInfos = connector.send_msg(cmd_msg)
			if result == tooldefine._MSG_ERROR:
				context["error"] = resultInfos
				return render(request, html_template, context)
			else:
				tempGagList = [str(i) for i in gagList]
				currServerkey = request.session[tooldefine.CURR_SERVER]
				logInstance.gagRoleLog(request.session["gm_userid"], request.session["gm_level"], name, "|".join(tempGagList), int(gagTime), reason, currServerkey, request.serverInfos.get(currServerkey, ""))
				
				context["success"] = csstatus.OPERATION_SUCCEED
				return render(request, html_template, context)

	@loginInstannce.login_check
	def role_query_info(self, request):
		"""
		角色信息查询
		"""
		html_template = "gmtools/role/role_query_info.html"
		context = self.role_query_info_init()
		roleName = ''
		send_flag = request.POST.get("send_flag", "")
		query_account_flag = request.POST.get("query_account_flag", "")
		if not send_flag:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_QUERY_INFO]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
				
		if "queryPetInfos" in request.POST:
			petUid = request.POST.get("queryPetInfos", "")
			context = eval(request.POST.get("context", "{}"))
			result, resultInfos = self.getPetInfoDetail(request, petUid)
			if result == tooldefine._MSG_ERROR:
				context["error"] = resultInfos
				return render(request, html_template, context)
			context["roleInfo"].update(resultInfos)
			context["context"] = context
			return render(request, html_template, context)

		queryType = request.POST.get("queryType", "")

		if "queryAccount" in request.POST:
			accountName = request.POST.get("queryValue", "")
			if not accountName:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			result, resultInfos = self.getRoleListInfo(request, accountName, "", "")
			if result == tooldefine._MSG_ERROR:
				context["error"] = resultInfos
				return render(request, html_template, context)
			context["queryType"] = "accountName"
			context["roleInfo"]["accountName"] = accountName
			context["roleList"] = resultInfos
			roleName = context["roleSelected"] = context["roleInfo"]["roleName"] = resultInfos[0]["playerName"]
		elif "roleSelected" in request.POST:
			context["queryType"] = "accountName"
			context["roleInfo"]["accountName"] = request.POST.get("accountName", "")
			context["roleList"] = eval(request.POST.get("roleList", ""))
			context["roleSelected"] = request.POST.get("roleSelected", "")
			roleName = context["roleSelected"]
			context["roleInfo"]["roleName"] = roleName

		nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		startDate = request.POST.get("date", "")
		startTime = request.POST.get("time", "")
		if not startDate:
			startDate = "2018-01-01"
		if not startTime:
			startTime = "00:00:00"
		updateTime = startDate + " " + startTime
		context.update({"date": startDate, "time": startTime})

		endDate = request.POST.get("endDate", "")
		endTime = request.POST.get("endTime", "")
		if not endDate:
			endDate = nowtime.split(" ")[0]
		if not endTime:
			endTime = nowtime.split(" ")[1]
		endUpdateTime = endDate + " " + endTime
		context.update({"endDate": endDate, "endTime": endTime})

		if endUpdateTime < updateTime:
			context["roleList"] = []
			context["roleInfo"]["roleName"] = ""
			context["error"] = csstatus.QUERY_TIME_FORMAT_ERROR
			return render(request, html_template, context)

		#获取角色ID
		result, resultInfos = self.getRoleIdByRoleName(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		roleId = int(resultInfos)

		# 玩家状态
		resultInfos = self.getRoleStateInfo(request, roleName)
		datas = resultInfos["datas"]
		if not datas:
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render(request, html_template, context)

		context["roleInfo"]["state"] = stringRes.STATE_DICT[datas["isOnline"]]
		# 玩家属性
		result, resultInfos = self.getRolePropertyInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)
		context["blobdata"] = resultInfos
		if context["roleList"]:
			for role in context["roleList"]:
				if role["playerName"] == roleName:
					context["roleInfo"]["gender"] = role["gender"]
					if role["tongName"]:
						context["roleInfo"]["tongName"] = role["tongName"]
					else:
						context["roleInfo"]["tongName"] = "无"
		#角色装备信息
		result, resultInfos = self.getRoleEquipInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 角色背包道具信息
		result, resultInfos = self.getRoleBagItemsInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 角色仓库道具信息
		result, resultInfos = self.getRoleStoreItemsInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 玩家金钱信息
		result, resultInfos = self.getRoleMoneyInfo(request, roleName, updateTime, endUpdateTime)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 角色幻兽信息
		result, resultInfos = RolePet.instance().getRolePetInfos(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"]["petListInfos"] = resultInfos

		# 角色技能信息
		result, resultInfos = self.getRoleSkillInfo(request, roleId)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		#角色称号信息
		result, resultInfos = self.getRoleTitleInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 角色任务信息
		result, resultInfos = self.getRoleQuestInfo(request, roleId)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 角色军衔信息
		result, resultInfos = self.getRoleMilitaryRankInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)

		# 玩家登录信息
		result, resultInfos = self.getRoleLoginInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render(request, html_template, context)
		context["roleInfo"].update(resultInfos)
		context["context"] = context
		return render(request, html_template, context)

	def role_query_info_init(self):
		return {"roleList": [], "queryType": "", "queryValue": "", "roleSelected": ""
			, "roleInfo": {"state": "", "accountName": "", "roleName": "", "menpai": "", "level": "", "combatPower": ""
			, "jingjie": "", "tongName": "", "gender": "", "camp": "", "exp": "",  "xiuwei": "", "killingValue": "", "credit": "", "potential": ""
			, "corporeity": "", "intellect": "", "discern": "", "moveSpeed": "", "dexterity": "", "strength": "",
							 "HP_Max": "", "MP_Max": "", "gangQiValue_Max": "", "tiLi": ""
			, "damage": "", "magic_damage": "", "armor": "", "magic_armor": "", "gangQi_damagePoint": "",
							 "gangQi_armorPoint": "", "hitrate": "", "criticalstrike": "", "parry": ""
			, "dodgerate": "", "healingrate": "", "recharge_amount": "", "xianshi": "", "lingshi": "", "xuanshi": "",
							 "money": "", "bindMoney": "", "feats": "", "psionic": ""
			,  "equipDatas": [], "ItemInfos":[], "petInfos": {}, "bagItems_equip": [], "bagItems_item": []
			,"storeItems_equip": [], "storeItems_item": [], "storeMoney": 0, "petListInfos": [], "skillInfos": [], "title": "", "titles": [],
						   "militaryRankInfo": "", "questInfos": []
			, "bingGong": "", "bingKang": "", "leiGong": "", "leiKang": "", "huoGong": "",
							 "huoKang": "", "xuanGong": "", "xuanKang": "", "firstLoginTime": ""
			, "lastLoginTime": "", "loginSpaceName": "", "loginPosition": ""}, "error": "", "date": "", "time": "", "endDate": "", "endTime": "", "context": {}}

	@loginInstannce.login_check
	def role_query_activity(self, request):
		"""
		"""
		html_template = "gmtools/role/role_query_activity.html"
		context = self.role_query_activity_init()
		send_flag = request.POST.get("send_flag", "")
		if not send_flag:
			return render(request, html_template, context)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_QUERY_ACTIVITY_PART]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		roleName = request.POST.get("roleName", "")
		context["roleInfo"] = {"roleName": roleName}
		sql = "select actCopyName, count(actCopyType) as c from %s where roleName = '%s' group by actCopyType" % \
			  (SQLConfig.LOG_TYPE_ACT_COPY, roleName)
		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		context["actCopyList"] = datas
		return render(request, html_template, context)

	def role_query_activity_init(self):
		return {"roleInfo": {"roleName": ""}, "error": "", "actCopyList": "", "roleName": ""}

	@loginInstannce.login_check
	def role_query_coin(self, request):
		"""
		货币查询
		"""
		html_template = "gmtools/role/role_query_coin.html"
		send_flag = request.POST.get("send_flag", "")
		queryType = request.POST.get("queryType")
		queryText = request.POST.get("queryText")
		date = request.POST.get("date","")
		coinType = request.POST.get("coinType", "")
		page = request.GET.get("page")
		context = {"error": "", "roleName": "", "date": "", "coinType": "", "datas": [], "page": None,
			"totalPage": None, "prevPage": None, "nextPage": None, "condition": "", "selected": 0}
		if not send_flag and not page:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_QUERY_COIN]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:  # 如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:  # “上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * (int(page) - 1)
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			# 而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			# 的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get("condition")  # 查询条件
			coinType = request.GET.get("coinType")
			date = request.GET.get("date")
			queryType, queryText = tuple(eval(queryCondition))
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], queryText):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render(request, html_template, context)
		condition = "where %s = '%s'" % (queryType, queryText.strip())
		if coinType and coinType.strip():
			condition += " and action = %s" % int(coinType)
		else:
			condition += " and action <> 1"
		if date:
			startDate = datetime.datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
			endDate = startDate + datetime.timedelta(days=1)
			startDate = startDate.strftime("%Y-%m-%d %H:%M:%S")
			endDate = endDate.strftime("%Y-%m-%d %H:%M:%S")
			condition += " and updateTime>'%s' and updateTime<'%s'" % (startDate, endDate)
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		queryCoinSql = "select action, oldValue, newValue, reason, updateTime from Log_Coin %s limit %s, %s" % (condition, startIndex, endIndex)
		queryCoinResults = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], queryCoinSql)
		datas = []
		for result in queryCoinResults:
			data = {"coinType": stringRes.COIN_CH_DICT[result[0]]}
			reasonInt = -1
			try:
				reasonInt = int(result[3])
			except:
				reasonInt = -1
			if result[1] < result[2]:
				if result[0] == LogDefine.LT_MONEY_CHANGE or result[0] == LogDefine.LT_BINDMONEY_CHANGE:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[0]][csdefine.MONEY_CHANGE_TYPE_ADD]:
						data["getReason"] = result[3]
					else:
						data["getReason"] = stringRes.COIN_CHANGE_REASON_DICT[result[0]][csdefine.MONEY_CHANGE_TYPE_ADD][int(result[3])]
				else:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[0]]:
						data["getReason"] = result[3]
					else:
						data["getReason"] = stringRes.COIN_CHANGE_REASON_DICT[result[0]][int(result[3])]
				data["get_oldValue"] = result[1]
				data["get_newValue"] = result[2]
				data["get_Num"] = result[2] - result[1]
				data["get_updateTime"] = result[4]
				data["costReason"] = data["cost_oldValue"] = data["cost_newValue"] = data["cost_Num"] = data["cost_updateTime"] = ""
			else:
				if result[0] == LogDefine.LT_MONEY_CHANGE or result[0] == LogDefine.LT_BINDMONEY_CHANGE:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[0]][csdefine.MONEY_CHANGE_TYPE_SUB]:
						data["costReason"] = result[3]
					else:
						data["costReason"] = stringRes.COIN_CHANGE_REASON_DICT[result[0]][csdefine.MONEY_CHANGE_TYPE_SUB][int(result[3])]
				else:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[0]]:
						data["costReason"] = result[3]
					else:
						data["costReason"] = stringRes.COIN_CHANGE_REASON_DICT[result[0]][int(result[3])]
				data["cost_oldValue"] = result[1]
				data["cost_newValue"] = result[2]
				data["cost_Num"] = result[1] - result[2]
				data["cost_updateTime"] = result[4]
				data["getReason"] = data["get_oldValue"] = data["get_newValue"] = data["get_Num"] = data["get_updateTime"] = ""
					
			datas.append(data)
		totalNumSql = "select count(*) from Log_Coin %s" % condition
		totalNum = int(g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)[0][0])
		totalPage = math.ceil(totalNum / tooldefine.QUERY_ONCE_NUM_)
		if totalPage <= 0:
			totalPage = 1
		context["page"] = int(page)
		context["totalPage"] = totalPage
		context["prevPage"] = self.getPrevPage(int(page))
		context["nextPage"] = self.getNextPage(int(page), totalPage)
		context["condition"] = (queryType, queryText)
		context["roleName"] = queryText
		context["date"] = date
		context["coinType"] = coinType
		if coinType == "":
			context["selected"] = 0
		else:
			context["selected"] = int(coinType)-1
		context["datas"] = datas
		return render(request, html_template, context)


	def getRoleIdByRoleName(self, request, roleName):
		"""
		通过角色名获取ID
		"""
		sql_queryDBID = "select id from tbl_Role where sm_playerName = '%s'" % roleName
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryDBID)
		if len(results) == 0:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		return (tooldefine._MSG_SUCCEED, results[0][0])

	def getRoleStateInfo(self, request, roleName):
		"""
		查询玩家状态信息
		"""
		context = {"error": "", "datas": ""}
		sql = "select tbl_Role.id, kbe_accountinfos.accountName from tbl_Role, kbe_accountinfos where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID and tbl_Role.sm_playerName = '%s'"
		roleQueryInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql % roleName)
		roleInfos = {"isOnline": False}
		sql = "select entityDBID from kbe_entitylog where entityDBID = %s and entityType = %s"
		if roleQueryInfos:
			stateQueryInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql % (
			int(roleQueryInfos[0][0]), tooldefine.ENTITY_TYPE_ROLE))
			if len(stateQueryInfos) > 0:
				roleInfos["isOnline"] = True
			return ({"datas": roleInfos})
		else:
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return (context)

	def getRoleListInfo(self, request, accountName, startTime, endTime):
		"""
		获取角色列表信息
		"""
		sql = """select tbl_Role.sm_playerName, tbl_Role.sm_level, tbl_Role.sm_gender,  tbl_Role.sm_camp, tbl_Role.sm_profession, tbl_Role.sm_tongName from tbl_Role, kbe_accountinfos 
		where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID and tbl_Role.sm_roleState = 1 and kbe_accountinfos.accountName = '%s'"""
		resultInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql % accountName)
		if not resultInfos:
			return (tooldefine._MSG_ERROR, csstatus.ACCOUNT_NOT_EXIST % accountName)
		roleList = []
		for role in resultInfos:
			data = {}
			data["playerName"] = role[0]
			data["level"] = role[1]
			data["gender"] = stringRes.ROLE_GENDER_DICT[role[2]]
			data["camp"] = "仙道" if role[3] == 1 else "魔道"
			data["menpai"] = Functions.getRoleMenpai(role[3], role[4])
			data["tongName"] = role[5]
			roleList.append(data)
		return(tooldefine._MSG_SUCCEED, roleList)

	def getRolePropertyInfo(self, request, roleName):
		"""
		得到玩家的属性
		"""
		sql = "select blobParam1, blobParam2, blobParam3 from Log_Role where action = %s and roleName = '%s' ORDER BY id DESC LIMIT 1"
		tempInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER],
													  sql % (LogDefine.LT_ROLE_PRO_RECORD, roleName))
		resultInfos = {}
		resultInfos["datas"] = tempInfos
		datas = resultInfos["datas"]
		if len(datas) == 0:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_ERROR % roleName)
		blobParam1, blobParam2, blobParam3 = datas[0]
		blobParam1Data = pickle.loads(eval(blobParam1))
		blobParam2Data = pickle.loads(eval(blobParam2))
		blobParam3Data = pickle.loads(eval(blobParam3))
		blobDatas = {}
		blobDatas.update(blobParam1Data)
		blobDatas.update(blobParam2Data)
		blobDatas.update(blobParam3Data)
		blobDatas["jingjie"] = Functions.getRoleJingjie(blobDatas["level"], blobDatas["xiuwei"], blobDatas["camp"])
		blobDatas["menpai"] = Functions.getRoleMenpai(blobDatas["camp"], blobDatas["profession"])
		blobDatas["hitrate"] = str(blobDatas["hitrate"] / 100) + "%"
		blobDatas["criticalstrike"] = str(blobDatas["criticalstrike"] / 100) + "%"
		blobDatas["parry"] = str(blobDatas["parry"] / 100) + "%"
		blobDatas["dodgerate"] = str(blobDatas["dodgerate"] / 100) + "%"
		blobDatas["healingrate"] = str(blobDatas["healingrate"] / 100) + "%"
		blobDatas["camp"] = "仙道" if blobDatas["camp"] == 1 else "魔道"

		return (tooldefine._MSG_SUCCEED, blobDatas)

	def getRoleEquipInfo(self, request, roleName):
		"""
		获取角色装备信息
		"""
		sql_queryDBID = "select id from tbl_Role where sm_playerName = '%s'" % roleName
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryDBID)
		if len(results) == 0:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		roleDBID = int(results[0][0])
		sql = "select sm_uid from tbl_Role_itemsBag_items where parentID = %s and (sm_order >= %s and sm_order <= %s)" % (
			roleDBID, ItemTypeEnum.BAG_EQUIPSTART, ItemTypeEnum.BAG_EQUIPEND)
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, [])
		uidList = [data[0] for data in datas]
		equipDatas_temp = []
		for uid in uidList:
			sql_equipData = "select itemName, equipData from %s where itemUid = %i order by id desc limit 1" % (SQLConfig.LOG_TYPE_EQUIP, int(uid))
			equipData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_equipData)
			if equipData_result:
				equipDatas_temp.append({"itemName": equipData_result[0][0], "data": pickle.loads(eval(equipData_result[0][1]))})
			else:
				sql_itemData = "select itemName, itemData from %s where itemUid = %i and action = 1 order by id desc limit 1" % (SQLConfig.LOG_TYPE_ITEM, int(uid))
				itemData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_itemData)
				if itemData_result:
					equipDatas_temp.append({"itemName": itemData_result[0][0], "data": pickle.loads(eval(itemData_result[0][1]))})
		equipDatas = []
		for equip in equipDatas_temp:
			equipData = {"equipName": equip["itemName"]}
			equipData["level"] = equip["data"]["level"]
			equipData["quality"] = stringRes.ITEM_QUALITY_CH_DICT[equip["data"]["quality"]]
			equipData["combatPower"] = equip["data"]["combatPower"]
			equipData["hardiness"] = equip["data"]["hardiness"]
			equipData["classes"] = Functions.getEquipClasses(int(equip["data"]["classes"]))
			equipData["order"] = stringRes.EQUIP_ORDER_DICT.get(int(equip["data"]["order"]), equip["data"]["order"])
			equipData["price"] = equip["data"]["price"]
			equipData["bindType"] = "是" if equip["data"]["bindType"] == 1 else "否"
			equipData["attributeAddition"] = ""
			for key, value in equip["data"]["extra"].items():
				equipData["attributeAddition"] += stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(int(key), str(key)) + "+" + str(
					value) + " "
			equipDatas.append(equipData)
		return(tooldefine._MSG_SUCCEED, {"equipDatas": equipDatas})

	def getRoleBagItemsInfo(self, request, roleName):
		"""
		获取角色背包物品信息
		"""
		sql_queryDBID = "select id from tbl_Role where sm_playerName = '%s'" % roleName
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryDBID)
		if len(results) == 0:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		roleDBID = int(results[0][0])
		sql = "select sm_id, sm_uid, sm_amount, sm_bindType from tbl_Role_itemsBag_items where parentID = %s and (sm_order >= %s and sm_order <= %s)" % (
			roleDBID, ItemTypeEnum.BAG_COMMONSTART, ItemTypeEnum.BAG_SPAREND)
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, [])
		itemDatas_temp = []
		equipDatas_temp = []
		for data in datas:
			itemData = ItemData.get(str(data[0]), {})
			if not itemData:
				continue
			if str(itemData["Type"]).startswith("100"):
				sql_equipData = "select itemName, equipData from %s where itemUid = %i order by id desc limit 1" % (SQLConfig.LOG_TYPE_EQUIP, int(data[1]))
				equipData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER],sql_equipData)
				if equipData_result:
					equipDatas_temp.append({"itemName": equipData_result[0][0], "data": pickle.loads(eval(equipData_result[0][1]))})
				else:
					sql_itemData = "select itemName, itemData from %s where itemUid = %i and action = 1 order by id desc limit 1" % (SQLConfig.LOG_TYPE_ITEM, int(data[1]))
					itemData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_itemData)
					if itemData_result:
						equipDatas_temp.append({"itemName": itemData_result[0][0], "data": pickle.loads(eval(itemData_result[0][1]))})
					else:
						itemData = ItemData.get(str(data[0]), {})
						if itemData:
							equipDatas_temp.append({"itemName": itemData["ItemName"], "data": itemData})
			else:
				itemData = ItemData.get(str(data[0]), {})
				if itemData:
					itemDatas_temp.append({"itemName": itemData["ItemName"], "data": itemData, "amount": data[2], "bindType": data[3]})
		equipDatas = []
		for equip in equipDatas_temp:
			equipData = {"equipName": equip["itemName"]}
			equipData["level"] = equip["data"]["level"]
			equipData["quality"] = stringRes.ITEM_QUALITY_CH_DICT[equip["data"]["quality"]]
			equipData["combatPower"] = equip["data"]["combatPower"]
			equipData["hardiness"] = equip["data"]["hardiness"]
			equipData["classes"] = Functions.getEquipClasses(int(equip["data"]["classes"]))
			equipData["order"] = stringRes.EQUIP_ORDER_DICT.get(int(equip["data"]["order"]), equip["data"]["order"])
			equipData["price"] = equip["data"]["price"]
			equipData["bindType"] = "是" if equip["data"]["bindType"] == 1 else "否"
			equipData["attributeAddition"] = ""
			for key, value in equip["data"]["extra"].items():
				equipData["attributeAddition"] += stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(int(key), str(key)) + "+" + str(
					value) + " "
			equipDatas.append(equipData)
		itemDatas = []
		for item in itemDatas_temp:
			itemData = {"itemName": item["itemName"]}
			itemData["ReqLevel"] = item["data"]["ReqLevel"]
			itemData["bindType"] = "是" if item["bindType"] == 1 else "否"
			itemData["Type"] = stringRes.ITEM_TYPE_DICT.get(int(item["data"]["Type"]), "")
			itemData["Describe"] = item["data"]["Describe"]
			if item["data"]["StackAmount"] == "0":
				itemData["StackAmount"] = item["data"]["StackAmount"].split("|")[0]
			else:
				itemData["StackAmount"] = item["data"]["StackAmount"].split("|")[1]
			itemData["amount"] = item["amount"]
			itemData["Price"] = item["data"]["Price"]
			itemDatas.append(itemData)
		return(tooldefine._MSG_SUCCEED, {"bagItems_equip": equipDatas, "bagItems_item": itemDatas})

	def getRoleStoreItemsInfo(self, request, roleName):
		"""
		获取角色仓库物品信息
		"""
		sql_queryDBID = "select id, sm_storeMoney from tbl_Role where sm_playerName = '%s'" % roleName
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryDBID)
		if len(results) == 0:
			return (tooldefine._MSG_ERROR, csstatus.ROLE_INFO_NOT_EXIST % roleName)
		roleDBID = int(results[0][0])
		sql = "select sm_item_id, sm_item_uid, sm_item_amount, sm_item_bindType from tbl_Role_storeItems_bag where parentID = %s" % roleDBID
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, [])
		itemDatas_temp = []
		equipDatas_temp = []
		for data in datas:
			if str(ItemData.get(str(data[0]), {})["Type"]).startswith("100"):
				sql_equipData = "select itemName, equipData from %s where itemUid = %i order by id desc limit 1" % (SQLConfig.LOG_TYPE_EQUIP, int(data[1]))
				equipData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER],sql_equipData)
				if equipData_result:
					equipDatas_temp.append({"itemName": equipData_result[0][0], "data": pickle.loads(eval(equipData_result[0][1]))})
				else:
					sql_itemData = "select itemName, itemData from %s where itemUid = %i and action = 1 order by id desc limit 1" % (SQLConfig.LOG_TYPE_ITEM, int(data[1]))
					itemData_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_itemData)
					if itemData_result:
						equipDatas_temp.append({"itemName": itemData_result[0][0], "data": pickle.loads(eval(itemData_result[0][1]))})
					else:
						itemData = ItemData.get(str(data[0]), {})
						if itemData:
							equipDatas_temp.append({"itemName": itemData["ItemName"], "data": itemData})
			else:
				itemData = ItemData.get(str(data[0]), {})
				if itemData:
					itemDatas_temp.append({"itemName": itemData["ItemName"], "data": itemData, "amount": data[2], "bindType": data[3]})
		equipDatas = []
		for equip in equipDatas_temp:
			equipData = {"equipName": equip["itemName"]}
			equipData["level"] = equip["data"]["level"]
			equipData["quality"] = stringRes.ITEM_QUALITY_CH_DICT[equip["data"]["quality"]]
			equipData["combatPower"] = equip["data"]["combatPower"]
			equipData["hardiness"] = equip["data"]["hardiness"]
			equipData["classes"] = Functions.getEquipClasses(int(equip["data"]["classes"]))
			equipData["order"] = stringRes.EQUIP_ORDER_DICT.get(int(equip["data"]["order"]), equip["data"]["order"])
			equipData["price"] = equip["data"]["price"]
			equipData["bindType"] = "是" if equip["data"]["bindType"] == 1 else "否"
			equipData["attributeAddition"] = ""
			for key, value in equip["data"]["extra"].items():
				equipData["attributeAddition"] += stringRes.ROLE_ATTRIBUTE_NUMBER_DICT.get(int(key), str(key)) + "+" + str(
					value) + " "
			equipDatas.append(equipData)
		itemDatas = []
		for item in itemDatas_temp:
			itemData = {"itemName": item["itemName"]}
			itemData["ReqLevel"] = item["data"]["ReqLevel"]
			itemData["bindType"] = "是" if item["bindType"] == 1 else "否"
			itemData["Type"] = stringRes.ITEM_TYPE_DICT.get(int(item["data"]["Type"]), "")
			itemData["Describe"] = item["data"]["Describe"]
			if item["data"]["StackAmount"] == "0":
				itemData["StackAmount"] = item["data"]["StackAmount"].split("|")[0]
			else:
				itemData["StackAmount"] = item["data"]["StackAmount"].split("|")[1]
			itemData["amount"] = item["amount"]
			itemData["Price"] = item["data"]["Price"]
			itemDatas.append(itemData)
		return(tooldefine._MSG_SUCCEED, {"storeItems_equip": equipDatas, "storeItems_item": itemDatas, "storeMoney": int(results[0][1])})

	def getPetInfoDetail(self, request, petUid):
		"""
		获取幻兽详细信息
		"""
		sql = "select petName, petUname, petUid, petQuality, petLevel, updatetime, action, param1, petData from %s where action != 2 and petUid = %i order by id desc limit 1" \
			  % (SQLConfig.LOG_TYPE_PET, int(petUid))
		data = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		petInfos = {}
		if data:
			petInfos.update(pickle.loads(eval(data[0][8])))
			petInfos["uname"] = data[0][1]
			petInfos["quality"] = stringRes.PET_QUALITY_DICT.get(int(data[0][3]), data[0][3])
			petInfos["level"] = data[0][4]
			petInfos["name"] = data[0][0] if data[0][0].strip() else data[0][1]
		else:
			return (tooldefine._MSG_SUCCEED, {})
		attrSkillBox = petInfos["attrSkillBox"]
		passiveSkillBox = petInfos["passiveSkillBox"]
		attrSkillInfo = ["", "", "", "", ""]
		passiveSkillInfo = ["", "", "", "", ""]
		skillTablePath = Functions.getSeverConfigPath() + '/Skill/SkillConfigs/SkillTable.json'
		with open(skillTablePath, encoding='utf-16') as skillTempleData:
			skillData = json.load(skillTempleData)
		i = j = 0
		for data in skillData:
			for attrSkill in attrSkillBox:
				if int(attrSkill) == int(data["Name"]):
					attrSkill = data["SkillName"]
					attrSkillInfo[i] = attrSkill
					i = i + 1
		passiveSkillTablePath = Functions.getSeverConfigPath() + '/Skill/SkillConfigs/PassiveSkillTable.json'
		with open(passiveSkillTablePath, encoding='utf-16') as passiveSkillTempleData:
			passiveSkillData = json.load(passiveSkillTempleData)
		for data in passiveSkillData:
			for passiveSkill in passiveSkillBox:
				if int(passiveSkill) == int(data["Name"]):
					passiveSkill = data["SkillName"]
					passiveSkillInfo[j] = passiveSkill
					j = j + 1
		petInfos["attrSkillInfo"] = attrSkillInfo
		petInfos["passiveSkillInfo"] = passiveSkillInfo
		return (tooldefine._MSG_SUCCEED, {"petInfos" :petInfos})

	def getRoleSkillInfo(self, request, roleId):
		"""
		获取角色技能信息
		"""
		sql = "select sm_value from tbl_Role_attrSkills where parentID = %i" % roleId
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, [])
		qbItem_sql = "select sm_id from tbl_Role_qbItems where parentID = %i" % roleId
		qbItem_result = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], qbItem_sql)
		qbItemLsit = [data[0] for data in qbItem_result]
		skillInfos = []
		skillTablePath = Functions.getSeverConfigPath() + '/Skill/SkillConfigs/skillLearnConfig.json'
		with open(skillTablePath, encoding='utf-8-sig') as skillTempleData:
			skillDatas = json.load(skillTempleData)
		for skill in skillDatas:
			for data in datas:
				if data[0] == int(skill["Name"]):
					skillInfos.append({"name": skill["UName"], "type": "主动技能", "level": skill["ReqLevel"], "state": "是" if data[0] in qbItemLsit else "否"})
		PassiveSkillTablePath = Functions.getSeverConfigPath() + '/Skill/SkillConfigs/PassiveSkillTable.json'
		with open(PassiveSkillTablePath, encoding='utf-16') as PassiveSkillTempleData:
			PassiveSkillDatas = json.load(PassiveSkillTempleData)
		for skill in PassiveSkillDatas:
			for data in datas:
				if data[0] == int(skill["Name"]):
					skillInfos.append({"name": skill["SkillName"], "type": "被动技能", "level": skill["SkillLevel"], "state": "是" if data[0] in qbItemLsit else "否"})
		return (tooldefine._MSG_SUCCEED, {"skillInfos": skillInfos})

	def getRoleMoneyInfo(self, request, roleName, startTime, endTime):
		"""
		得到玩家金钱相关信息
		"""
		# 查询玩家的金钱数、绑金、灵石、潜能、功勋、灵能和账号dbid
		sql = "select sm_money, sm_bindMoney, sm_lingshi, sm_feats, sm_psionic, sm_parentDBID from tbl_Role where sm_playerName = '%s'" % roleName
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		money, bindMoney, lingshi, feats, psionic, dbid = [int(data) for data in results[0]]
		# 查询账号仙石、玄石
		sql = "select sm_xianshi, sm_xuanshi from tbl_Account where id = %s" % dbid
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		xianshi, xuanshi = int(results[0][0]), int(results[0][1])
		# 查询充值金额
		rechargeInfo_sql = "select value from %s where accountDBID = %s and updateTime >= '%s' and updateTime <= '%s' " % (SQLConfig.LOG_TYPE_RECHARGE, dbid, startTime, endTime)
		rechargeInfo_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], rechargeInfo_sql)
		recharge_amount = 0
		for amount in rechargeInfo_result:
			recharge_amount += int(amount[0])
		datas = {"xianshi": xianshi, "xuanshi": xuanshi, "lingshi": lingshi, "money": money, "bindMoney": bindMoney,
				 "feats": feats, "psionic": psionic, "recharge_amount": recharge_amount}
		return (tooldefine._MSG_SUCCEED, datas)

	def getRoleTitleInfo(self, request, roleName):
		"""
		获取角色称号信息
		"""
		sql = "select tbl_Role.sm_title, tbl_Role_titles.sm_value from tbl_Role, tbl_Role_titles where tbl_Role_titles.parentID = tbl_Role.id and tbl_Role.sm_playerName = '%s'" % roleName
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, {"titleInfos": {"title": "", "titles": []}})
		titleTablePath = Functions.getSeverConfigPath() + '/TitleData/titleData.json'
		with open(titleTablePath,  encoding='utf-8') as titleTempleData:
			titleData = json.load(titleTempleData)
		titleInfos = {"title": "", "titles": []}
		for title in titleData:
			if datas[0][0] == title["TitleID"]:
				titleInfos["title"] = title["TitleName"]
			for data in datas:
				if data[1] == title["TitleID"]:
					titleInfos["titles"].append(title["TitleName"])
		return (tooldefine._MSG_SUCCEED, titleInfos)

	def getRoleQuestInfo(self, request, roleId):
		"""
		获取角色任务信息
		"""
		sql = "select sm_id from tbl_Role_questTable_quests where parentID = %i" % roleId
		questId_datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not questId_datas:
			return (tooldefine._MSG_SUCCEED, {"questInfos": []})
		questInfos = []
		for questId in questId_datas:
			questDataPath = Functions.getSeverConfigPath() + '/Quest/%i.json' % questId[0]
			with open(questDataPath, encoding='utf-8') as questTempleData:
				questData = json.load(questTempleData).get(str(questId[0]), "")
			if questData:
				questInfos.append({"id": questData["id"], "title": questData["title"], "QuestClass": questData["QuestClass"], "level": questData["level"]})
		for quest in questInfos:
			if quest["QuestClass"] == "QuestNormal":
				quest["QuestClass"] = "主线任务"
			elif quest["QuestClass"] == "QuestLoop":
				quest["QuestClass"] = "环任务"
			elif quest["QuestClass"] == "QuestTongDaily":
				quest["QuestClass"] = "帮会任务"
		return (tooldefine._MSG_SUCCEED, {"questInfos": questInfos})

	def getRoleMilitaryRankInfo(self, request, roleName):
		"""
		获取角色军衔信息
		"""
		sql = "select sm_maxMilitaryRank from tbl_Role where sm_playerName = '%s'" % roleName
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if not datas:
			return (tooldefine._MSG_SUCCEED, {"militaryRankInfo": ""})
		militaryRankTablePath = Functions.getSeverConfigPath() + '/MilitaryRank/MilitaryRankCfg.json'
		with open(militaryRankTablePath, encoding='utf-8') as militaryRankTempleData:
			militaryRankData = json.load(militaryRankTempleData)
		militaryRankInfo = militaryRankData.get(str(datas[0][0]), "")
		if militaryRankInfo:
			militaryRankInfo = militaryRankInfo["title"]
		return (tooldefine._MSG_SUCCEED, {"militaryRankInfo": militaryRankInfo})

	def getRoleLoginInfo(self, request, roleName):
		"""
		得到玩家其他信息(时间,空间,坐标)
		"""
		loginData = {}
		sql = "select sm_spaceScriptID,sm_0_position,sm_1_position,sm_2_position from tbl_Role where sm_playerName = '%s'"
		tempInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql % roleName)
		resultInfos = {}
		resultInfos["space"] = tempInfos[0][0]
		resultInfos["position"] = tempInfos[0][1:]
		datas = resultInfos["position"]
		loginData["loginSpaceName"] = stringRes.MAP_NAME_DICT.get(resultInfos["space"], resultInfos["space"])
		loginData["loginPosition"] = resultInfos["position"]

		loginData.update({"firstLoginTime": "", "lastLoginTime": ""})
		sql = "select updateTime from Log_Role where action = %s and roleName = '%s' ORDER BY id ASC LIMIT 1"
		tempInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER],
													  sql % (LogDefine.LT_ROLE_LOGON, roleName))
		resultInfos = {}
		resultInfos["datas"] = tempInfos
		datas = resultInfos["datas"]
		if len(datas) > 0:
			loginData["firstLoginTime"] = datas[0][0]

		sql = "select updateTime from Log_Role where action = %s and roleName = '%s' ORDER BY id DESC LIMIT  1"
		tempInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER],
													  sql % (LogDefine.LT_ROLE_LOGON, roleName))
		resultInfos = {}
		resultInfos["datas"] = tempInfos
		datas = resultInfos["datas"]
		if len(datas) > 0:
			loginData["lastLoginTime"] = datas[0][0]

		return (tooldefine._MSG_SUCCEED, loginData)

	@loginInstannce.login_check
	def role_query_pet(self, request):
		"""
		角色幻兽查询
		"""
		return RolePet.instance().query(request)

	@loginInstannce.login_check
	def role_query_item(self, request):
		"""
		角色道具查询
		"""
		return RoleItem.instance().query(request)

	@loginInstannce.login_check
	def role_tranToRevivePosition(self, request):
		"""
		传送到复活点
		"""
		html_template = "gmtools/role/role_tranToRevivePos.html"
		sendFlag = request.GET.get("send_flag")
		roleName = request.GET.get("roleName", "")

		context = {"error": "", "success": "", "roleName": roleName}
		if not sendFlag:
			return render(request, html_template, context)

		if not roleName:
			context["error"] = csstatus.ROLE_INFO_NOT_NAME_INPUT
			return render(request, html_template, context)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_TRAN_TO_REVIVE_POS]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)


		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render(request, html_template, context)

		cmd_msg = {}
		cmd_msg["cmd"] = "tranToRevivePos"
		cmd_msg["info"] = {}
		cmd_msg["info"]["roleName"] = roleName

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultInfos = connector.send_msg(cmd_msg)

		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
		else:
			context["success"] = csstatus.OPERATION_SUCCEED

			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.tranToRevivePosRoleLog(request.session["gm_userid"], request.session["gm_level"], roleName, currServerkey, request.serverInfos.get(currServerkey, ""))
			


		return render(request, html_template, context)


g_roleInstance = RoleManager.instance()