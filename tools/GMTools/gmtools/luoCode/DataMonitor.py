# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from . import login
from common import csstatus
from common import csdefine
from common import stringRes
from common import LogDefine
from common import tooldefine
from common.DBConnectInterface import g_dbInterfaceInst
from common.ServerConfigMgr import g_srvCfgMgrInstance
import time

loginInstannce = login.g_loginInstance

class DataMonitor:
	"""
	用户管理器
	"""
	_instance = None
	def __init__(self):
		pass
	
	@staticmethod
	def instance():
		"""
		UserManager实例
		"""
		if DataMonitor._instance == None:
			DataMonitor._instance = DataMonitor()
		return DataMonitor._instance
	
	def getOnlineData(self, request):
		"""
		获取当前在线数据
		"""
		serverConfig = g_srvCfgMgrInstance.getConfig()
		serverName = serverConfig[request.session[tooldefine.CURR_SERVER]]["name"]
		onlineSql = "select count(*) from kbe_entitylog where entityType = %s" % tooldefine.ENTITY_TYPE_ROLE
		onlineData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], onlineSql)
		accountSql = "select count(*) from tbl_Account"
		accountData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], accountSql)
		
		data = {"serverName": serverName, "totalAmount": int(accountData[0][0]), "onlineAmount": int(onlineData[0][0])}
		return [data]
		
	def getChargeBaseData(self):
		datas = {}
		datas.update({"error": ""})
		datas.update({"totalChargeQueryInfo": {"startDate": "", "endDate": ""}})
		datas.update({"totalChargeInfo": {"totalChargeValue": "", "singleHighestValue": "", "sumHighestValue": "", "accountName": ""}})
		datas.update({"orderQueryInfo": {"accountQuery": 0, "totalChargeQuery": 0, "singleChargeQuery": 0, "accountName": "", "totalChargeValue": "", "singleChargeValue": ""}})
		datas.update({"orderQueryDatas": []})
		
		return datas
		
	def getChargeTotalData(self, request):
		datas = {"totalChargeValue": 0, "singleHighestValue": 0, "sumHighestValue": 0, "accountName": ""}
		
		startTime = ""
		endTime = int(time.time())
		
		startDate = request.POST.get("startDate", "")
		endDate = request.POST.get("endDate", "")
		
		if startDate:
			startTimeStr = "%s 00:00:00" % startDate
			startTime = int(time.mktime(time.strptime(startTimeStr, "%Y-%m-%d %H:%M:%S")))
		if endDate:
			endTimeStr = "%s 24:00:00" % endDate
			endTime = int(time.mktime(time.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S")))
			
		totalChargeSql = "select sum(sm_gold), max(sm_gold) from tbl_ChargeOrders where sm_orders_time <= %s" % endTime
		if startTime:
			totalChargeSql += " and sm_orders_time >= %s" % startTime
		totalChargeData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], totalChargeSql)
		if len(totalChargeData) > 0: #有可能查到的结果为[[None, None]]
			try:
				datas["totalChargeValue"] = int(totalChargeData[0][0])
				datas["singleHighestValue"] = int(totalChargeData[0][1])
			except:
				pass
		
		if startTime:
			singleHighestSql = "select sm_account, sum(sm_gold) as sumgold from csol3.tbl_ChargeOrders where sm_orders_time >= %s and sm_orders_time <= %s \
			 group by sm_account order by sumgold desc limit 0, 1" % (startTime, endTime)
		else:
			singleHighestSql = "select sm_account, sum(sm_gold) as sumgold from csol3.tbl_ChargeOrders where sm_orders_time <= %s \
			 group by sm_account order by sumgold desc limit 0, 1" % endTime
			 
		singleHighestSqlData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], singleHighestSql)
		if len(singleHighestSqlData) > 0  and singleHighestSqlData[0][0] != "None":
			try:
				datas["accountName"] = singleHighestSqlData[0][0]
				datas["sumHighestValue"] = int(singleHighestSqlData[0][1])
			except:
				pass
		
		return datas
		
	def getChargeOrdersData(self, request, type):
		chargeOrderData = []
		
		if type == tooldefine.CHARGE_ORDER_QUERY_TYPE_ACCOUNT:
			accountName = request.POST.get("accountName")
			sql = "select sm_gy_orderId, sm_account, sm_gold, sm_chargeType, sm_orders_time from tbl_ChargeOrders where sm_account = '%s'" % accountName
		elif type == tooldefine.CHARGE_ORDER_QUERY_TYPE_TOTALCHARGE:
			totalChargeValue = request.POST.get("totalChargeValue")
			sql = "select sm_gy_orderId, sm_account, sm_gold, sm_chargeType, sm_orders_time from tbl_ChargeOrders where sm_account in \
				( select sm_account from tbl_ChargeOrders group by sm_account  having sum(sm_gold )> %s ) " % totalChargeValue
		else:
			singleChargeValue = request.POST.get("singleChargeValue")
			sql = "select sm_gy_orderId, sm_account, sm_gold, sm_chargeType, sm_orders_time from tbl_ChargeOrders where sm_gold > %s" % singleChargeValue
			
		orderSqlData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		
		for orderData in orderSqlData:
			orderData[3] = stringRes.CHARGE_TYPE_NAME[int(orderData[3])]
			orderData[4] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(orderData[4])))
			chargeOrderData.append(orderData)
			
		balanceData = {}
		accountList = set([d[1] for d in chargeOrderData])
		for accountName in accountList:
			sql = "select sm_xianshi from tbl_Account where sm_playerName = '%s'" % accountName
			queryData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
			if len(queryData) > 0:
				balanceData[accountName] = int(queryData[0][0])
				
		for orderData in chargeOrderData:
			orderData.append(balanceData.get(orderData[1], 0))
		
		return chargeOrderData
		
	def getCoinBaseData(self):
		datas = {}
		datas.update({"error": ""})
		datas.update({"gameCoinQueryInfo": {"startDate": "", "endDate": "", "roleName": ""}})
		datas.update({"gameCoinQueryData": []})
		
		return datas
		
	def getCoinAddData(self, request):
		coinData = []
		startDate = request.POST.get("startDate", "")
		endDate = request.POST.get("endDate", "")
		roleName = request.POST.get("roleName", "")
		sql = "select roleName, action, (ifnull(newValue, 0) - ifnull(oldValue, 0)), newValue, reason, updateTime from Log_Coin where (action = %s or action = %s)and \
			(ifnull(newValue, 0) - ifnull(oldValue, 0)) > 0" % (LogDefine.LT_BINDMONEY_CHANGE, LogDefine.LT_MONEY_CHANGE)
		
		if startDate:
			sql = sql + " and updateTime > '%s 00:00:00'" % startDate
		if endDate:
			sql = sql + " and updateTime < '%s 24:00:00'" % endDate
			
		if roleName:
			sql = sql + " and roleName = '%s'" % roleName
			
		coinSqlData = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		
		for data in coinSqlData:
			try:
				changeType = int(data[4])
			except:
				pass
			data[1] = stringRes.COIN_CH_DICT.get(int(data[1]), data[1])
			data[4] = stringRes.MONEY_ADD_REASON_CH_DICT.get(changeType, data[4])
			coinData.append(data)
			
		return coinData
		
	def getCostBaseData(self):
		datas = {}
		datas.update({"error": ""})
		datas.update({"totalCostQueryInfo": {"startDate": "", "endDate": ""}})
		datas.update({"totalCostInfo": {"xianshiTotalCost": "", "xianshiMaxCost": "", "xianshiCostNumber": "", "xianshiCostTimes": ""}})
		datas["totalCostInfo"].update({"lingshiTotalCost": "", "lingshiMaxCost": "", "lingshiCostNumber": "", "lingshiCostTimes": ""})
		datas["totalCostInfo"].update({"xuanshiTotalCost": "", "xuanshiMaxCost": "", "xuanshiCostNumber": "", "xuanshiCostTimes": ""})
		datas.update({"singleQueryInfo": {"accountQuery": 1, "roleQuery": 0}})
		datas["singleQueryInfo"].update({"xianshiQuery": 1, "lingshiQuery": 0, "xuanshiQuery": 0})
		datas["singleQueryInfo"].update({"startDate": "", "endDate": ""})
		datas["singleQueryInfo"].update({"queryText": ""})
		datas.update({"singleQueryDatas": []})
		
		return datas
		
	def getCostTotalData(self, request):
		costTotalData = {}
		costTotalData.update({"xianshiTotalCost": 0, "xianshiCostNumber": 0, "xianshiMaxCost": 0, "xianshiCostTimes": 0})
		costTotalData.update({"lingshiTotalCost": 0, "lingshiCostNumber": 0, "lingshiMaxCost": 0, "lingshiCostTimes": 0})
		costTotalData.update({"xuanshiTotalCost": 0, "xuanshiMaxCost": 0, "xuanshiCostNumber": 0, "xuanshiCostTimes": 0})
		
		startDate = request.POST.get("startDate", "")
		endDate = request.POST.get("endDate", "")
		condition = "(ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0 and (action = %s or action = %s or action = %s)" % (LogDefine.LT_XIANSHI_CHANGE, LogDefine.LT_LINGSHI_CHANGE, LogDefine.LT_XUANSHI_CHANGE)
		if startDate:
			startTime = "%s 00:00:00" % startDate
			condition = condition + " and updateTime >= '%s'" % startTime
		if endDate:
			endTime = "%s 24:00:00" % endDate
			condition = condition + " and updateTime <= '%s'" % endTime
		
		costRoleNumSql = "select DISTINCT action, roleName from Log_Coin where %s" % condition
		costRoleNumData = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], costRoleNumSql)
		
		tempData = {}
		for data in costRoleNumData:
			if int(data[0]) not in tempData:
				tempData[int(data[0])] = 0
			tempData[int(data[0])] += 1
		
		costSql = "select action, sum((ifnull(oldValue, 0) - ifnull(newValue, 0))), count(*), max((ifnull(oldValue, 0) - ifnull(newValue, 0))) from Log_Coin where %s group by action" % condition		
		costSqlData = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], costSql)
		
		for data in costSqlData:
			if int(data[0]) == LogDefine.LT_XIANSHI_CHANGE:
				costTotalData.update({"xianshiTotalCost": int(data[1]), "xianshiCostNumber": tempData.get(int(data[0]), 0), "xianshiMaxCost": int(data[3]), "xianshiCostTimes": int(data[2])})
			if int(data[0]) == LogDefine.LT_LINGSHI_CHANGE:
				costTotalData.update({"lingshiTotalCost": int(data[1]), "lingshiCostNumber": tempData.get(int(data[0]), 0), "lingshiMaxCost": int(data[3]), "lingshiCostTimes": int(data[2])})
			if int(data[0]) == LogDefine.LT_XUANSHI_CHANGE:
				costTotalData.update({"xuanshiTotalCost": int(data[1]), "xuanshiCostNumber": tempData.get(int(data[0]), 0), "xuanshiMaxCost": int(data[3]), "xuanshiCostTimes": int(data[2])})
			
		return costTotalData
		
	def getCostSingleData(self, request):
		singleCostData = []
		
		startDate = request.POST.get("singleStartDate", "")
		endDate = request.POST.get("singleEndDate", "")
		playerQuery = request.POST.get("playerQuery", "")
		queryText = request.POST.get("queryText", "")
		xianshiQuery = request.POST.get("xianshiQuery", 0)
		lingshiQuery = request.POST.get("lingshiQuery", 0)
		xuanshiQuery = request.POST.get("xuanshiQuery", 0)
		
		valueCondition = "(ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0"
		
		timeCondition = ""
		if startDate:
			timeCondition = "updateTime >= '%s 00:00:00'" % startDate
		if endDate:
			if timeCondition:
				timeCondition += "and updateTime <= '%s 24:00:00'" % endDate
			else:
				timeCondition = "updateTime <= '%s 24:00:00'" % endDate
		
		shitouCondition =""
		if xianshiQuery:
			shitouCondition = "action = %s" % LogDefine.LT_XIANSHI_CHANGE
		if lingshiQuery:
			if shitouCondition:
				shitouCondition += " or action = %s" % LogDefine.LT_LINGSHI_CHANGE
			else:
				shitouCondition = "action = %s" % LogDefine.LT_LINGSHI_CHANGE
		if xuanshiQuery:
			if shitouCondition:
				shitouCondition += " or action = %s" % LogDefine.LT_XUANSHI_CHANGE
			else:
				shitouCondition = "action = %s" % LogDefine.LT_XUANSHI_CHANGE
		
		if playerQuery == "account":
			accountSql = "select DISTINCT id from tbl_Account where sm_playerName = '%s'" % queryText
			accountData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], accountSql)
			
			if len(accountData) > 0:
				accountDBID = int(accountData[0][0])
				if timeCondition:
					costSql = "select roleName, action, (ifnull(oldValue, 0) - ifnull(newValue, 0)), newValue, reason, updateTime from Log_Coin where (%s) and (%s) and (%s) and accountDBID = %s" \
					% (shitouCondition, timeCondition, valueCondition, accountDBID)
				else:
					costSql = "select roleName, action, (ifnull(oldValue, 0) - ifnull(newValue, 0)), newValue, reason, updateTime from Log_Coin where (%s) and (%s) and accountDBID = %s" \
					% (shitouCondition, valueCondition, accountDBID)
					
				costSqlData = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], costSql)
				for data in costSqlData:
					if int(data[1]) == LogDefine.LT_XIANSHI_CHANGE:
						data[4] = stringRes.COIN_XIANSHI_CHANGE_CH_DICT.get(int(data[4]), data[4])
					elif int(data[1]) == LogDefine.LT_LINGSHI_CHANGE:
						data[4] = stringRes.COIN_LINGSHI_CHANGE_CH_DICT.get(int(data[4]), data[4])
					elif int(data[1]) == LogDefine.LT_XUANSHI_CHANGE:
						data[4] = stringRes.COIN_XUANSHI_CHANGE_CH_DICT.get(int(data[4]), data[4])
					data[1] = stringRes.COIN_CH_DICT.get(int(data[1]), data[1])
					data.insert(0, queryText)
					singleCostData.append(data)
		elif playerQuery == "role":
			accountSql = "select tbl_Account.sm_playerName from tbl_Account, tbl_Role where tbl_Account.id = tbl_Role.sm_parentDBID and tbl_Role.sm_playerName = '%s'" % queryText
			accountData = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], accountSql)
			if len(accountData) > 0:
				accountName = accountData[0][0]
				if timeCondition:
					costSql = "select roleName, action, (ifnull(oldValue, 0) - ifnull(newValue, 0)), newValue, reason, updateTime from Log_Coin where (%s) and (%s) and (%s) and roleName = '%s'" % \
					(shitouCondition, timeCondition, valueCondition, queryText)
				else:
					costSql = "select roleName, action, (ifnull(oldValue, 0) - ifnull(newValue, 0)), newValue, reason, updateTime from Log_Coin where (%s) and (%s) and roleName = '%s'" % \
					(shitouCondition, valueCondition, queryText)
					
				costSqlData = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], costSql)
				for data in costSqlData:
					data[1] = stringRes.COIN_CH_DICT.get(int(data[1]), data[1])
					if int(data[2]) == LogDefine.LT_XIANSHI_CHANGE:
						data[4] = stringRes.COIN_XIANSHI_CHANGE_CH_DICT.get(int(data[3]), data[3])
					elif int(data[2]) == LogDefine.LT_LINGSHI_CHANGE:
						data[4] = stringRes.COIN_LINGSHI_CHANGE_CH_DICT.get(int(data[3]), data[3])
					elif int(data[2]) == LogDefine.LT_XUANSHI_CHANGE:
						data[4] = stringRes.COIN_XUANSHI_CHANGE_CH_DICT.get(int(data[3]), data[3])
					data.insert(0, accountName)
					singleCostData.append(data)
		
		return singleCostData
		
	@loginInstannce.login_check
	def dataMonitorBase(self, request):
		"""
		数据监控主界面
		"""
		html_template = "gmtools/DataMonitor/DataMonitorBase.html"
		
		context = {}
		return render( request, html_template, context )

	@loginInstannce.login_check
	def onLineData(self, request):
		"""
		在线数据监控
		"""
		html_template = "gmtools/DataMonitor/OnLineData.html"
		
		context = {"datas": [], "error": ""}
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def onLineDataQuery(self, request):
		"""
		在线数据查询
		"""
		html_template = "gmtools/DataMonitor/OnLineData.html"
		context = {"datas": [], "error": ""}
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_ONLINE_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		datas = self.getOnlineData(request)
		context["datas"] = datas
		return render( request, html_template, context )

	@loginInstannce.login_check
	def chargeData(self, request):
		"""
		消费数据监控
		"""
		html_template = "gmtools/DataMonitor/ChargeData.html"
		
		datas = self.getChargeBaseData()
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def chargeDataTotalquery(self, request):
		"""
		充值数据汇总查询
		"""
		html_template = "gmtools/DataMonitor/ChargeData.html"
		datas = self.getChargeBaseData()
		context = {}
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_RECHARGE_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		totalChargeData = self.getChargeTotalData(request)
		datas["totalChargeInfo"].update(totalChargeData)
		
		datas["totalChargeQueryInfo"]["startDate"] = request.POST.get("startDate", "")
		datas["totalChargeQueryInfo"]["endDate"] = request.POST.get("endDate", "")
		
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def chargeDataOrdersQuery(self, request):
		"""
		充值数据订单查询
		"""
		html_template = "gmtools/DataMonitor/ChargeData.html"
		datas = self.getChargeBaseData()
		context = {}
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_RECHARGE_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		chargeOrderData = datas["orderQueryDatas"]
		
		accountQuery = request.POST.get("accountQuery", 0)
		totalChargeQuery = request.POST.get("totalChargeQuery", 0)
		singleChargeQuery = request.POST.get("singleChargeQuery", 0)
		
		datas["orderQueryInfo"].update({"accountQuery": int(accountQuery), "totalChargeQuery": int(totalChargeQuery), "singleChargeQuery": int(singleChargeQuery)})
		
		if not accountQuery and not totalChargeQuery and not singleChargeQuery:
			datas["error"] = csstatus.CHARGE_ORDER_QUERY_TYPE_ERROR
		else:
			if accountQuery:#账号查询
				accountName = request.POST.get("accountName", "")
				if not accountName:
					datas["error"] = csstatus.CHARGE_ORDER_QUERY_ACCOUNT_NONE_ERROR
				else:
					datas["orderQueryInfo"].update({"accountName": accountName})
					condition = "sm_account = %s" % accountName
					chargeOrderData = self.getChargeOrdersData(request, tooldefine.CHARGE_ORDER_QUERY_TYPE_ACCOUNT)
			elif totalChargeQuery:#总消费查询
				totalChargeValue = request.POST.get("totalChargeValue", "")
				if not totalChargeValue:
					datas["error"] = csstatus.CHARGE_ORDER_QUERY_TOTALCHARGE_NONE_ERROR
				else:
					datas["orderQueryInfo"].update({"totalChargeValue": totalChargeValue})
					chargeOrderData = self.getChargeOrdersData(request, tooldefine.CHARGE_ORDER_QUERY_TYPE_TOTALCHARGE)
			elif singleChargeQuery:
				singleChargeValue = request.POST.get("singleChargeValue", "")
				if not singleChargeValue:
					datas["error"] = csstatus.CHARGE_ORDER_QUERY_TOTALCHARGE_NONE_ERROR
				else:
					datas["orderQueryInfo"].update({"singleChargeValue": singleChargeValue})
					chargeOrderData = self.getChargeOrdersData(request, tooldefine.CHARGE_ORDER_QUERY_TYPE_SINGLECHARGE)
					
			datas["orderQueryDatas"] = chargeOrderData
		context = datas
		return render( request, html_template, context )

	@loginInstannce.login_check
	def coinData(self, request):
		"""
		货币收入监控
		"""
		html_template = "gmtools/DataMonitor/CoinData.html"
		
		datas = self.getCoinBaseData()
		
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def coinDataQuery(self, request):
		"""
		货币收入监控
		"""
		html_template = "gmtools/DataMonitor/CoinData.html"
		
		datas = self.getCoinBaseData()
		context = {}
	
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_ROLE_COIN_ADD]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		startDate = request.POST.get("startDate", "")
		endDate = request.POST.get("endDate", "")
		roleName = request.POST.get("roleName", "")
		
		datas.update({"gameCoinQueryInfo": {"startDate": startDate, "endDate": endDate, "roleName": roleName}})
		
		coinData = self.getCoinAddData(request)
		
		datas["gameCoinQueryData"] = coinData
		
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def costData(self, request):
		html_template = "gmtools/DataMonitor/CostData.html"
		
		datas = self.getCostBaseData()
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def costDataTotalQuery(self, request):
		html_template = "gmtools/DataMonitor/CostData.html"
		
		datas = self.getCostBaseData()	
		datas["totalCostQueryInfo"]["startDate"] = request.POST.get("startDate", "")
		datas["totalCostQueryInfo"]["endDate"] = request.POST.get("endDate", "")
		
		context = {}
	
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_ROLE_COST_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		costTotalData = self.getCostTotalData(request)
		datas.update({"totalCostInfo": costTotalData})
		
		context = datas
		return render( request, html_template, context )
		
	@loginInstannce.login_check
	def costDataSingleQuery(self, request):
		html_template = "gmtools/DataMonitor/CostData.html"
		
		datas = self.getCostBaseData()
		
		datas["singleQueryInfo"]["xianshiQuery"] = int(request.POST.get("xianshiQuery", 0))
		datas["singleQueryInfo"]["lingshiQuery"] = int(request.POST.get("lingshiQuery", 0))
		datas["singleQueryInfo"]["xuanshiQuery"] = int(request.POST.get("xuanshiQuery", 0))
		
		datas["singleQueryInfo"]["startDate"] = request.POST.get("singleStartDate", "")
		datas["singleQueryInfo"]["endDate"] = request.POST.get("singleEndDate", "")
		datas["singleQueryInfo"]["queryText"] = request.POST.get("queryText", "")
		
		context = {}
	
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_DATA_MONITOR][tooldefine.DATA_MONITOR_ROLE_COST_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		playerQuery = request.POST.get("playerQuery", "")
		if playerQuery:
			if playerQuery == "account":
				datas["singleQueryInfo"]["accountQuery"] = 1
				datas["singleQueryInfo"]["roleQuery"] = 0
			elif playerQuery == "role":
				datas["singleQueryInfo"]["accountQuery"] = 0
				datas["singleQueryInfo"]["roleQuery"] = 1
		else:
			datas["error"] = csstatus.COST_SINGLE_QUERY_COIN_NONE_ERROR
			context = datas
			return render( request, html_template, context )
			
		if not datas["singleQueryInfo"]["xianshiQuery"] and not datas["singleQueryInfo"]["lingshiQuery"] and not datas["singleQueryInfo"]["xuanshiQuery"]:
			datas["error"] = csstatus.COST_SINGLE_QUERY_TEXT_COND_ERROR
			context = datas
			return render( request, html_template, context )
		if not datas["singleQueryInfo"]["queryText"]:
			datas["error"] = csstatus.COST_SINGLE_QUERY_TEXT_NONE_ERROR
			context = datas
			return render( request, html_template, context )
			
		singleCostData = self.getCostSingleData(request)
		datas["singleQueryDatas"] = singleCostData
		
		context = datas
		return render( request, html_template, context )


g_dataMonitorInstance = DataMonitor.instance()