# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from cs3_web_services import settings
from common import baseConnector, csstatus, csdefine, SQLConfig, stringRes, LogDefine, tooldefine
from common.DBConnectInterface import g_dbInterfaceInst
from . import login
from . import GMActionLog

import os
import json
import time
import xlwt
from io import BytesIO
from operator import itemgetter

logInstance = GMActionLog.g_logInstance
loginInstannce = login.g_loginInstance
g_baseappConnector = baseConnector.g_baseappConnector

class AccountManager:
	"""
	游戏账号管理器
	"""
	_instance = None
	def __init__(self):
		pass
	
	@staticmethod
	def instance():
		if AccountManager._instance == None:
			AccountManager._instance = AccountManager()
		return AccountManager._instance
	
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
		
	def getQueryIndex(self, index, recordNum = tooldefine.QUERY_ONCE_NUM_):
		"""
		获得查询记录开始和结尾序号
		:param index: 当前页号
		:param recordNum:查询记录数
		:return:查（起始序号，结尾序号）
		"""
		return ( index * recordNum, recordNum )

	def trusteeship_cancel(self, request, html_template, context):
		"""
		取消托管
		"""
		sql = "select sm_accountName from tbl_GameSeccion where sm_accountName = '%s'" % context["account_name"]
		results=g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(results) <= 0:
			message = {"state": "fault", "message": "the accountName is error"}
			return message
		else:
			sql = "update tbl_GameSeccion set sm_trusteeshipTime = 0 where sm_accountName='%s'" % context["account_name"]
			g_dbInterfaceInst.executeSqlInGameDB(request.session[tooldefine.CURR_SERVER], sql,[])
			
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.cancelTrusteeshipLog(request.session["gm_userid"], request.session["gm_level"], context["account_name"], "", currServerkey, request.serverInfos.get(currServerkey, ""))
			
		return (True, "")

	@loginInstannce.login_check
	def account(self, request):
		"""
		"""
		html_template = "gmtools/account/account.html"
		return render( request, html_template, {})

	@loginInstannce.login_check
	def role_kick(self, request, roleName):
		"""
		踢号
		"""
		cmd_msg = {}
		cmd_msg["cmd"] = "doActionForPlayer"
		cmd_msg["info"] = {}
		cmd_msg["info"]["cmd_interface"] = "kickPlayer"
		cmd_msg["info"]["roleName"] = roleName
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultInfos = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			return(tooldefine._MSG_ERROR, resultInfos)
		else:
			return(tooldefine._MSG_SUCCEED, csstatus.OPERATION_SUCCEED)
	
	@loginInstannce.login_check
	def lock(self, request):
		"""
		封锁账号
		"""
		html_template = "gmtools/account/account_lock.html"
		send_flag = request.POST.get("send_flag")
		name = request.GET.get("name")
		reason = request.POST.get("reason", "")
		accountName = request.POST.get("accountName")
		lockTime = request.POST.get("time", 0)
		if accountName:
			name = accountName
		context = {"error": "", "success": "", "name": name, "lock_time": lockTime, "reason": reason}
		if not send_flag:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_LOCK_ACCOUNT]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)

		if not lockTime:
			context["error"] = csstatus.ACCOUNT_LOCK_NOT_TIME
			return render(request, html_template, context)
		if not g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], accountName):
			context["error"] = csstatus.ACCOUNT_NOT_EXIST % accountName
			return render(request, html_template, context)
		cmd_msg = {}
		cmd_msg["cmd"] = "lockAccount"
		cmd_msg["info"] = {}
		cmd_msg["info"]["account_name"] = name
		cmd_msg["info"]["lock_time"] = int(lockTime) * 60
		cmd_msg["info"]["reason"] = reason
		cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
			return render(request, html_template, context)
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.blockAccountLog(request.session["gm_userid"], request.session["gm_level"], name, int(lockTime), reason, currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.OPERATION_SUCCEED
			return render(request, html_template, context)

	@loginInstannce.login_check
	def lock_batch(self, request):
		"""
		批量封锁账号
		"""
		html_template = "gmtools/account/account_lock_batch.html"
		send_flag = request.POST.get("send_flag")
		name = request.GET.get("name")
		reason = request.POST.get("reason", "")
		accountNameList = request.POST.get("accountNameList")
		lockTime = request.POST.get("time", 0)
		if accountNameList:
			name = accountNameList
		context = {"error": "", "success": "", "name": name, "lock_time": lockTime, "reason": reason}
		if not send_flag:
			return render(request, html_template, context)
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_LOCK_ACCOUNT]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
		if not lockTime:
			context["error"] = csstatus.ACCOUNT_LOCK_NOT_TIME
			return render(request, html_template, context)
		if not accountNameList.strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		accountNameList = accountNameList.split("|")
		for accountName in accountNameList:
			if not g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], accountName):
				context["error"] = csstatus.ACCOUNT_NOT_EXIST % accountName
				return render(request, html_template, context)
			cmd_msg = {}
			cmd_msg["cmd"] = "lockAccount"
			cmd_msg["info"] = {}
			cmd_msg["info"]["account_name"] = accountName
			cmd_msg["info"]["lock_time"] = int(lockTime) * 60
			cmd_msg["info"]["reason"] = reason
			cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
			connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
			result, message = connector.send_msg(cmd_msg)
			if result == tooldefine._MSG_ERROR:
				context["error"] = message
				return render(request, html_template, context)
				
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.blockAccountLog(request.session["gm_userid"], request.session["gm_level"], accountName, int(lockTime), reason, currServerkey, request.serverInfos.get(currServerkey, ""))

		context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)

	@loginInstannce.login_check
	def unlock(self, request):
		"""
		解封账号
		"""
		html_template = "gmtools/account/account_unlock.html"
		name = request.GET.get("name")
		send_flag = request.POST.get("send_flag")
		reason = request.POST.get("reason", "")
		accountName = request.POST.get("accountName")
		if accountName:
			name = accountName
		context = {"error": "", "success": "", "name": name, "reason": reason}
		if not send_flag:
			return render( request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_UNLOCK_ACCOUNT]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
			
		cmd_msg = {}
		cmd_msg["cmd"] = "unLockAccount"
		cmd_msg["info"] = {}
		cmd_msg["info"]["account_name"] = name
		cmd_msg["info"]["reason"] = reason
		cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.unBlockAccountLog(request.session["gm_userid"], request.session["gm_level"], name, reason, currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.OPERATION_SUCCEED
		return render( request, html_template, context)

	@loginInstannce.login_check
	def unlock_batch(self, request):
		"""
		批量解封账号
		"""
		html_template = "gmtools/account/account_unlock_batch.html"
		name = request.GET.get("name")
		send_flag = request.POST.get("send_flag")
		reason = request.POST.get("reason", "")
		accountNameList = request.POST.get("accountNameList", "")
		if accountNameList:
			name = accountNameList
		context = {"error": "", "success": "", "name": name, "reason": reason}
		if not send_flag:
			return render(request, html_template, context)
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_UNLOCK_ACCOUNT]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, html_template, context)
		if not accountNameList.strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		accountNameList = accountNameList.split("|")
		for accountName in accountNameList:
			if not g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], accountName):
				context["error"] = csstatus.ACCOUNT_NOT_EXIST % accountName
				return render(request, html_template, context)
			cmd_msg = {}
			cmd_msg["cmd"] = "unLockAccount"
			cmd_msg["info"] = {}
			cmd_msg["info"]["account_name"] = accountName
			cmd_msg["info"]["reason"] = reason
			cmd_msg["info"]["GMUser"] = request.session["gm_userid"]
			connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
			result, message = connector.send_msg(cmd_msg)
			if result == tooldefine._MSG_ERROR:
				context["error"] = message
			else:	
				currServerkey = request.session[tooldefine.CURR_SERVER]
				logInstance.unBlockAccountLog(request.session["gm_userid"], request.session["gm_level"], accountName, reason, currServerkey, request.serverInfos.get(currServerkey, ""))
			
		context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)

	@loginInstannce.login_check
	def account_query_info(self, request):
		"""
		账号信息查询
		"""
		html_template = "gmtools/account/account_info.html"
		context = self.account_query_info_init()
		send_flag = request.POST.get("send_flag")  # 是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")  # 查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")  # 查询条件的内容
		if not send_flag:  # 初次进入邮件记录网页
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_QUERY]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
			
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		message = g_dbInterfaceInst.queryAccountInfo(request.session[tooldefine.CURR_SERVER], queryType, queryText)
		if message["empty_data"]:
			context["error"] = csstatus.ACCOUNT_NOT_EXIST % queryText
			return render(request, html_template, context)
		datas = message["datas"]
		for data in datas:
			data[1] = data[1]
			data[2] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[2])))
			data[3] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[3])))
		context["datas"] = datas
		context["queryText"] = queryText
		return render(request, html_template, context)

	def account_query_info_init(self):
		return {"roleInfos":{},"accountInfos":"","isQuery":"","success":"","error":"","datas":"","queryText":"","page":None,"nextPage":None,"prevPage":None}
	
	@loginInstannce.login_check
	def account_trusteeship_base(self, request):
		"""
		账号托管
		"""
		html_template = "gmtools/account/account_trusteeship_base.html"
		context = {"error": "", "success":"","nextPage":None,"prevPage":None,"page":None,"account_name":"","datas":""}
		return render( request, html_template, context)
	
	@loginInstannce.login_check
	def account_trusteeship(self, request):
		"""
		进行账号托管
		"""
		html_template = "gmtools/account/account_trusteeship.html"
		context = {"error": "", "success":""}
		account_name = request.POST.get("account_name")
		long_time = request.POST.get("long_time")
		password = request.POST.get("password")
		password_again = request.POST.get("password_again")
		context["account_name"] = account_name
		context["long_time"] = long_time
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
			
		if not long_time.isdigit():
			context["error"] = csstatus.ACCOUNT_TRUSTEESHIP_TIME_ERROR
			return render( request, html_template, context)
		if password != password_again:
			context["error"] = csstatus.ACCOUNT_TRUSTEESHIP_PASSWORD_ERROR
			return render( request, html_template, context)
			
		if not g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], account_name):
			context["error"] = csstatus.ACCOUNT_NOT_EXIST % account_name
			return render( request, html_template, context)
			
		cmd_msg = {}
		cmd_msg["cmd"] = "accountTrusteeship"
		cmd_msg["info"] = {}
		cmd_msg["info"]["account_name"] = account_name
		cmd_msg["info"]["long_time"] = long_time
		cmd_msg["info"]["password"] = password
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
			return render( request, html_template, context )
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.trusteeshipLog(request.session["gm_userid"], request.session["gm_level"], account_name, int(long_time), "", currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.OPERATION_SUCCEED
			return render( request, html_template, context )
	
	def accountTrusteeshipQuery(self, request, accountName, limitCondition):
		"""
		账号托管信息查询
		"""
		if accountName == "*":
			sql = "select count(*) from tbl_GameSeccion where sm_trusteeshipTime > %i" % time.time()
			results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
			totalNum = int(results[0][0])
			sql = "select sm_accountName, sm_trusteeshipTime from tbl_GameSeccion where sm_trusteeshipTime > %i" % time.time()
			if limitCondition:
				sql += " %s" % limitCondition
			results=g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
			datas = []
			for data in results:
				datas.append([data[0], data[1]])
			message = {"datas": datas, "totalNum": totalNum}
			return message
		else:
			sql = "select sm_accountName, sm_trusteeshipTime from tbl_GameSeccion " \
				  "where sm_accountName = '%s' and sm_trusteeshipTime > %i" % (accountName, time.time())
			if limitCondition:
				sql += " %s" % limitCondition
			results=g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
			datas = []
			if len(results) == 0:
				if g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], accountName):
					datas.append([accountName, ""])
					message = {"datas": datas, "totalNum": 1}
					return message
				else:
					return {"datas": [], "totalNum": 0}
			for data in results:
				datas.append([data[0], data[1]])
			message = {"datas": datas, "totalNum": 1}
			return message

	@loginInstannce.login_check
	def account_trusteeship_query(self, request):
		"""
		账号托管查询
		"""
		html_template = "gmtools/account/account_trusteeship_base.html"
		queryText = request.POST.get("queryText")
		currentPage = request.GET.get("page")
		queryAccountName = queryText
		account_name = request.GET.get("account_name")
		context = {"error": "", "success":"","nextPage":None,"prevPage":None,"page":None,"account_name": queryText}
		if account_name:
			context["account_name"] = account_name
			queryAccountName = account_name
		if not currentPage:
			currentPage = 1
			index = 0
		else:
			index = tooldefine.QUERY_ONCE_NUM_ * ( int(currentPage) - 1 )
		startIndex, endIndex = self.getQueryIndex( index, tooldefine.QUERY_ONCE_NUM_ )
		limitCondition = SQLConfig.QUERY_RANGE % (str(startIndex), str(endIndex))
		message=self.accountTrusteeshipQuery(request, queryAccountName,limitCondition)
		page = int(currentPage)
		totalNum = int(message["totalNum"])
		datas = message["datas"]
		totalPage = int(totalNum / tooldefine.QUERY_ONCE_NUM_)
		if totalPage <= 0:
			totalPage = 1
		context["page"] = page
		context["totalPage"] = totalPage
		nextPage = self.getNextPage(page, totalPage)
		prevPage = self.getPrevPage(page)
		context["prevPage"] = prevPage
		context["nextPage"] = nextPage
		if len(datas) == 0 and queryText != "*":
			context["error"] = csstatus.ACCOUNT_NOT_EXIST % queryText
		for data in datas:
			if data[1]:
				data[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[1])))
		context["datas"] = datas
		return render( request, html_template, context )

	@loginInstannce.login_check
	def account_trusteeship_action(self, request):
		"""
		进行账号托管，或者取消账号托管
		"""
		type = request.GET.get("type")
		name = request.GET.get("account_name")
		if int(type) == 1:
			html_template = "gmtools/account/account_trusteeship.html"
			context = {"account_name": name, "error": "", "success": "", "long_time": ""}
			return render( request, html_template, context )
		else:
			html_template = "gmtools/account/account_trusteeship_base.html"
			context = {"account_name": name, "error": "", "success": "", "long_time": ""}
			
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_ACCOUNT_TRUSTEESHIP_CANCEL]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render( request, html_template, context)
			
			self.trusteeship_cancel(request, html_template, context)
			return self.account_trusteeship_query(request)
		
	def getRoleDaohengLevel(self, level, daoheng):
		"""
		获取玩家对应的道行等级
		"""
		for daohengLevel, daohengData in stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.items():
			if level < daohengData["playerLevel"] or daoheng < daohengData["daoheng"]:
				return max(1, int(daohengLevel) - 1)
		return 1

	def getRoleDaohengLevelCh(self, level, daoheng, camp):
		"""
		获取玩家对应的道行等级的中文
		"""
		daohengLevel = self.getRoleDaohengLevel( level, daoheng )
		return stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.get( str(daohengLevel) ).get("ch").get(camp, level)

	def exportRoleInfo(self, request):
		"""
		导出角色信息
		"""
		context = {"error": "", "success": "", "role_name": "", "accountInfos": {"accountName":"","isLock":"","unlockTime":""
		,"lockReason":"","lockUser":""}, "roleInfos": {"isGag":"","gagInfos":"","chat_list":""},"isQuery":None}
		html_template = "gmtools/account/account_state_query.html"
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_EXPORT_ROLE_INFO]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
			
		message = g_dbInterfaceInst.exportAllRoleInfo(request.session[tooldefine.CURR_SERVER], )
		"""
		导出excel表格
		"""
		titleList = [u"账号名", u"角色名", u"性别",u"等级", u"门派", u"境界", u"修为", u"杀气", u"潜能", u"金钱",
					 u"灵石", u"仙石", u"玄石", u"首登时间", u"末登时间", u"在线总时长", u"充值金额（元）"]
		# 创建工作薄
		ws = xlwt.Workbook(encoding='utf-8')
		w = ws.add_sheet(u"角色信息")
		for i in range(len(titleList)):
			w.write(0, i, titleList[i])
		# 写入数据
		excel_row = 1
		# 服务器查询数据顺序accountName, sm_playerName, sm_level, sm_camp, sm_profession, sm_xiuwei, sm_killingValue, sm_potential
		for data in message["datas"]:
			for i in range(len(titleList)):
				if i == 0 or i == 1:
					data[i] = data[i]
				if i==13 or i==14:
					data[i] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[i])))
				if i==15:
					m,s=divmod(data[i],60)
					h,m=divmod(m,60)
					data[i]="%s小时%s分%s秒"%(h,m,s)
				if i==2: #角色性别
					w.write(excel_row, i, stringRes.ROLE_GENDER_DICT[data[2]])
				elif i == 4:  # 门派
					w.write(excel_row, i, stringRes.MENPAI_TYPE_DICT[int(data[4])][int(data[5])])
				elif i == 5:  # 境界
					w.write(excel_row, i, self.getRoleDaohengLevelCh(int(data[3]), int(data[6]), int(data[4])))
				else:
					w.write(excel_row, i, data[i])
			excel_row += 1
		# 检测文件是够存在
		# 方框中代码是保存本地文件使用，如不需要请删除该代码
		###########################
		exist_file = os.path.exists("PlayerInfo.xls")
		if exist_file:
			os.remove(r"PlayerInfo.xls")
		ws.save("PlayerInfo.xls")
		############################
		sio = BytesIO()
		ws.save(sio)
		sio.seek(0)
		response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=PlayerInfo.xls'
		response.write(sio.getvalue())
		return response


	def exportCostInfo(self, request):
		"""
		导出消费排行
		"""
		context = {"error": "", "success": "", "role_name": "", "accountInfos": {"accountName":"","isLock":"","unlockTime":""
		,"lockReason":"","lockUser":""}, "roleInfos": {"isGag":"","gagInfos":"","chat_list":""},"isQuery":None}
		html_template = "gmtools/account/account_state_query.html"
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACCOUNT_MGR][tooldefine.ACCOUNT_MGR_EXPORT_COST_DATA]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context)
			
		roleinfo_sql = "select sm_playerName, sm_level from tbl_Role"
		results = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], roleinfo_sql)
		#金钱变更信息查询
		moneychangeinfo_sql = "select roleName, oldValue, newValue from %s where action = %s and (ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0" % (SQLConfig. LOG_TYPE_COIN,
			LogDefine.LT_MONEY_CHANGE)
		moneychangeinfo = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], moneychangeinfo_sql)
		#灵石变更信息查询
		lingshichangeinfo_sql = "select roleName, oldValue, newValue from %s where action = %s and (ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0" % (SQLConfig.LOG_TYPE_COIN,
			LogDefine.LT_LINGSHI_CHANGE)
		lingshichangeinfo = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], lingshichangeinfo_sql)
		#仙石变更信息查询
		xianshichangeinfo_sql = "select roleName, oldValue, newValue from %s where action = %s and (ifnull(oldValue, 0) - ifnull(newValue, 0)) > 0" % (SQLConfig.LOG_TYPE_COIN,
			LogDefine.LT_XIANSHI_CHANGE)
		xianshichangeinfo = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], xianshichangeinfo_sql)
		datas =	self.sortCostInfo(results, moneychangeinfo, lingshichangeinfo, xianshichangeinfo)
		"""
		导出excel表格
		"""
		titleList = [u"排名",u"角色名",u"角色等级",u"金钱消费",u"灵石消费", u"仙石消费"]
		# 创建工作薄
		ws = xlwt.Workbook(encoding='utf-8')
		w = ws.add_sheet(u"角色信息")
		for i in range(len(titleList)):
			w.write(0, i, titleList[i])
		# 写入数据
		excel_row = 1
		for data in datas:
			w.write(excel_row, 0, excel_row)
			w.write(excel_row, 1, data[0])
			w.write(excel_row, 2, data[1])
			w.write(excel_row, 3, data[2])
			w.write(excel_row, 4, data[3])
			w.write(excel_row, 5, data[4])
			excel_row += 1
		# 检测文件是够存在
		# 方框中代码是保存本地文件使用，如不需要请删除该代码
		###########################
		exist_file = os.path.exists("CostInfo.xls")
		if exist_file:
			os.remove(r"CostInfo.xls")
		ws.save("CostInfo.xls")
		############################
		sio = BytesIO()
		ws.save(sio)
		sio.seek(0)
		response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=CostInfo.xls'
		response.write(sio.getvalue())
		return response
		
	def sortCostInfo(self, roleinfos, moneychangeinfo, lingshichangeinfo, xianshichangeinfo):
		"""
		"""
		for roleinfo in roleinfos:
			moneycost=lingshicost=xianshicost=0
			costList=[moneycost,lingshicost,xianshicost]
			roleinfo.extend(costList)
			for cost in moneychangeinfo:
				if roleinfo[0]==cost[0]:
					roleinfo[2]+=int(cost[1]) - int(cost[2])
			for cost in lingshichangeinfo:
				if roleinfo[0]==cost[0]:
					roleinfo[3]+=int(cost[1]) - int(cost[2])
			for cost in xianshichangeinfo:
				if roleinfo[0]==cost[0]:
					roleinfo[4]+=int(cost[1]) - int(cost[2])
		datas = sorted(roleinfos, key=itemgetter(4,3,2,1),reverse=True)
		return datas
		
	@loginInstannce.login_check
	def account_state_export_data(self, request):
		"""
		导出角色信息或者导出消费排行
		"""
		if "account_export_role_info" in request.POST:
			return self.exportRoleInfo(request)
		elif "account_export_cost_info" in request.POST:
			return self.exportCostInfo(request)
			
	@loginInstannce.login_check
	def account_state_query(self, request):
		"""
		账号状态查询页面
		"""
		context = {"error": "", "success": "", "role_name": "", "accountInfos": {"accountName":"","isLock":"","unlockTime":""
		,"lockReason":"","lockUser":""}, "roleInfos": {"isGag":"","gagInfos":"","chat_list":""},"isQuery":None}
		html_template = "gmtools/account/account_state_query.html"
		return render(request, html_template, context)
	
	@loginInstannce.login_check
	def queryAccountStateInfo(self, request):
		"""
		进行账号状态查询
		"""
		html_template = "gmtools/account/account_state_query.html"
		roleName = request.POST.get("queryText", "")
		context = {"error": "", "success": "", "role_name": roleName, "accountInfos": {}, "roleInfos": []}
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render( request, html_template, context)
		if "btn_roleKick" in request.POST:
			if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_MGR][tooldefine.ROLE_MGR_KICK_ROLE]:
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			else:
				result, resultInfos = self.role_kick(request, roleName)
				if result == tooldefine._MSG_SUCCEED:
					context["success"] = resultInfos
				else:
					context["error"] = resultInfos
		#1.查看玩家境界、是否在线等信息
		result, resultData = self.queryRoleStateInfo(request, roleName)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultData["error"]
			return render( request, html_template, context)
		else:
			datas = resultData["datas"]
			context.update({"menPai": datas["menPai"], "isOnline": datas["isOnline"], "isFrozen": datas["isFrozen"]})
			context["rolePropertyInfors"] = datas
			context["rolePropertyInfors"]["roleName"] = roleName
			#2查看玩家封号信息
			accountInfos = self.queryAccountLockInfo(request, datas["accountName"])
			accountInfos["isOnline"] = datas["isOnline"]
			context["accountInfos"] = accountInfos
			#3.查看玩家禁言信息
			result, message = self.queryRoleGagInfo(request, roleName)
			context["roleInfos"] = message
			context["isQuery"] = True
			return render(request, html_template, context)
			
	def queryRoleStateInfo(self, request, roleName):
		"""
		查询玩家状态信息
		"""
		#检查角色是否存在
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			return (tooldefine._MSG_ERROR, {"error": csstatus.ROLE_INFO_NOT_EXIST % roleName})
		
		#玩家境界、是否在线等信息
		sql = """select tbl_Role.id, kbe_accountinfos.accountName, tbl_Role.sm_camp, tbl_Role.sm_profession, tbl_Role.sm_gender, tbl_Role.sm_level, tbl_Role.sm_money, tbl_Role.sm_potential, tbl_Role.sm_lingshi, tbl_Role.sm_unFreezeTime
		from tbl_Role, kbe_accountinfos where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID and tbl_Role.sm_playerName = '%s'"""
		roleQueryInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql % roleName)
		roleInfos = {"isOnline": False, "accountName": roleQueryInfos[0][1], "level": roleQueryInfos[0][5], "money": roleQueryInfos[0][6], "potential": roleQueryInfos[0][7], "lingshi": roleQueryInfos[0][8], "isFrozen": False}
		roleInfos["menPai"] = stringRes.MENPAI_TYPE_DICT[int(roleQueryInfos[0][2])][int(roleQueryInfos[0][3])]
		sql = """select entityDBID from kbe_entitylog where entityDBID = %s and entityType = %s""" % (int(roleQueryInfos[0][0]), tooldefine.ENTITY_TYPE_ROLE)
		stateQueryInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(stateQueryInfos) > 0:
			roleInfos["isOnline"] = True
		if roleQueryInfos[0][9] > time.time():
			roleInfos["isFrozen"] = True
		
		return (tooldefine._MSG_SUCCEED, {"datas": roleInfos})
		
	def queryAccountLockInfo(self, request, accountName):
		"""
		查看账号是否被封号
		"""
		lockInfo = {"accountName": accountName, "isLock": False, "unlockTime": "", "lockReason": "", "lockUser": ""}
		sql = "select  sm_lockEndTime, sm_lockReason, sm_lockGMUser from tbl_GameSeccion where sm_accountName = '%s'" % accountName
		lockQueryInfos = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(lockQueryInfos) > 0:
			if float(lockQueryInfos[0][0]) > time.time():
				lockInfo["isLock"] = True
				lockInfo["unlockTime"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(lockQueryInfos[0][0])))
				lockInfo["lockReason"] = lockQueryInfos[0][1]
				lockInfo["lockUser"] = lockQueryInfos[0][2]
		return lockInfo
		
	def queryRoleGagInfo(self, request, roleName):
		"""
		查看玩家是否被禁言
		"""
		sql = """select updateTime, action, param1, param2, param3, param4 from %s where ((action = %s and param2 > %s) or (action = %s)) 
			and roleName = '%s'""" % (SQLConfig.LOG_TYPE_ROLE, LogDefine.LT_ROLE_GAG, time.time(), LogDefine.LT_ROLE_UNGAG, roleName)
		gagQueryInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		
		roleInfos = {"isGag": False, "gagInfos": [], "chat_list": ["0"] * len(stringRes.CHAT_TYPE_DICT)}
		if len(gagQueryInfos) > 0:
			recordDatas = sorted(gagQueryInfos, key = lambda data: time.mktime(time.strptime(data[0], "%Y-%m-%d %H:%M:%S")))
			tempDatas = {}
			for recordData in recordDatas:
				if int(recordData[1]) == LogDefine.LT_ROLE_GAG:	#如果是禁言，添加到字典
					if int(recordData[2]) not in tempDatas:
						tempDatas[int(recordData[2])] = {}
					t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(recordData[3])))
					tempDatas[int(recordData[2])]["gagInfo"] = {"gagType": int(recordData[2]), "unGagTime": t, "gagReason": recordData[4], "gagUser": recordData[5]}
				elif int(recordData[1]) == LogDefine.LT_ROLE_UNGAG:
					if int(recordData[2]) in tempDatas:	#如果是解除禁言，将字典中的该频道的禁言信息删除
						tempDatas.pop(int(recordData[2]))
			if tempDatas:
				roleInfos["isGag"] = True
				for key ,value in tempDatas.items():
					gagType = value["gagInfo"]["gagType"]
					roleInfos["gagInfos"].append(value["gagInfo"])
					roleInfos["gagInfos"][-1]["gagType"] = stringRes.CHAT_TYPE_DICT[gagType]
					roleInfos["chat_list"][gagType] = "1"
					
		roleInfos["chat_list"] = "".join(roleInfos["chat_list"])
		return (tooldefine._MSG_SUCCEED, roleInfos)


g_accountInstance = AccountManager.instance()