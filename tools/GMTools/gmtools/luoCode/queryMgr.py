# -*- coding: utf-8 -*-



import pickle
import math
import time

from django.shortcuts import render
from django.http import HttpResponse

from . import login
from common import csstatus, baseConnector, csdefine, SQLConfig, LogDefine, stringRes, tooldefine
from common.DBConnectInterface import g_dbInterfaceInst
from cs3_web_services import settings
from common import Functions, ItemTypeEnum

g_baseappConnector = baseConnector.g_baseappConnector
loginInstannce = login.g_loginInstance


class QueryManager:
	"""
	查询管理器
	"""
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		if QueryManager._instance == None:
			QueryManager._instance = QueryManager()
		return QueryManager._instance
		
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
		return ( index , recordNum )

	def getRoleDaohengLevel(self, level, daoheng):
		"""
		获取玩家对应的道行等级
		"""
		for daohengLevel, daohengData in stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.items():
			if level < daohengData["playerLevel"] or daoheng < daohengData["daoheng"]:
				return max(1, int(daohengLevel) - 1)
		return 1

	def getRoleDaohengLevelCh(self,level, daoheng, camp):
		"""
		获取玩家对应的道行等级的中文
		"""
		daohengLevel = self.getRoleDaohengLevel( level, daoheng )
		return stringRes.ROLE_DAOHENG_LEVEL_CH_DICT.get( str(daohengLevel) ).get("ch").get(camp, level)

	@loginInstannce.login_check
	def query(self, request):
		"""
		查询主页
		"""
		html_template = "gmtools/query/query_base.html"
		return render( request, html_template, {})

	def initContext(self):
		"""
		初始化返回结果信息
		"""
		context={"error": "", "success": ""}
		context["queryText"]=""
		context["page"] = None
		context["totalPage"] = None
		context["datas"] = []
		context["prevPage"] = None
		context["nextPage"] = None
		context["condition"] = ()
		context["roleInfo"] = {}
		context["uid"] = ""
		return context

	def initContext_role_attribute(self):
		"""
		初始化角色属性信息
		"""
		context={"error":""}
		blobParam1Data={'credit': "", 'dexterity': "", 'killingValue': "", 'corporeity': "", 'camp': "", 'xiuwei': "",
		 'money': "", 'intellect': "", 'potential': "", 'moveSpeed': "", 'strength': "", 'combatPower': "",
		 'discern': "", 'level': "", 'profession': ""}
		blobParam2Data={'dodgerate': "", 'healingrate': "", 'gangQiValue_Max': "", 'gangQi_damagePoint': "", 'MP_Max': "",
		 'armor': "", 'gangQi_armorPoint': "", 'magic_damage': "", 'parry': "", 'hitrate': "", 'damage': "",
		 'HP_Max': "", 'magic_armor': "", 'criticalstrike': ""}
		blobParam3Data={'leiKang': "", 'xuanKang': "", 'huoGong': "", 'tiLi': "", 'leiGong': "", 'xuanGong': "", 'huoKang': "", 'bingKang': "",
		 'bingGong': ""}
		blobDatas = {}
		blobDatas.update(blobParam1Data)
		blobDatas.update(blobParam2Data)
		blobDatas.update(blobParam3Data)
		blobDatas["roleName"]=""
		blobDatas["state"]=""
		blobDatas["jingjie"] = ""
		blobDatas["menpai"] = ""
		blobDatas["hitrate"] = ""
		blobDatas["criticalstrike"] = ""
		blobDatas["parry"] = ""
		blobDatas["dodgerate"] = ""
		blobDatas["healingrate"] = ""
		context["roleInfo"] = blobDatas
		context["queryText"] = ""
		return context

	@loginInstannce.login_check
	def query_role_upgrade(self, request):
		"""
		玩家升级信息查询
		"""
		html_template = "gmtools/query/query_role_upgrade.html"
		context=self.initContext()
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_upgrade_result(self, request):
		"""
		玩家升级信息查询结果
		"""
		html_template = "gmtools/query/query_role_upgrade.html"
		context = self.initContext()
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_UPGRADE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		POST = request.POST
		queryType = POST.get("queryType")
		queryText = POST.get("queryText")
		currentPage = request.GET.get("page")
		condition = ""
		if not currentPage:
			currentPage = 1
			index = 0
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
		else:
			index = tooldefine.QUERY_ONCE_NUM_ * ( int(currentPage) - 1 )
			queryCondition = request.GET.get( "condition" )
			queryType, queryText = tuple(eval(queryCondition))
		if queryText == "*":
			pass
		else:
			condition = condition + "and %s = '%s'" % ( queryType, queryText )
		startIndex, endIndex = self.getQueryIndex( index, tooldefine.QUERY_ONCE_NUM_ )
		sql = "select id, roleDBID, roleName, param1, param2, updateTime from Log_Pro where action = %s and roleName = '%s' limit %s, %s"
		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql % ( LogDefine.LT_PRO_LEVEL_UPGRADE, queryText,str( startIndex ), str( endIndex )))
		#totalNumSql 为查询到的记录个数,与分页相关
		totalNumSql = "select count(*) from Log_Pro where action = %s and %s = '%s' " %(LogDefine.LT_PRO_LEVEL_UPGRADE, queryType, queryText )
		countNum = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)

		page = int(currentPage)
		totalNum = countNum[0][0]
		if resultInfos:
			totalPage = int(totalNum / tooldefine.QUERY_ONCE_NUM_)
			if totalPage <= 0:
				totalPage = 1
			context["page"] = page
			context["totalPage"] = totalPage
			context["datas"] = resultInfos
			nextPage = self.getNextPage( page, totalPage )
			prevPage = self.getPrevPage( page )
			context["prevPage"] = prevPage
			context["nextPage"] = nextPage
			context["condition"] = (queryType, queryText)
		else:
			context["error"]= csstatus.ITEM_ISSUE_ALL_ROLE_ERROR
		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_skill_learn(self, request):
		"""
		玩家技能学习
		"""
		html_template = "gmtools/query/query_role_skill_learn.html"
		context = self.initContext()
		POST = request.POST
		queryType = POST.get("queryType")
		queryText = POST.get("queryText")
		send_flag = POST.get("send_flag")
		currentPage = request.GET.get("page")

		if not send_flag and not currentPage:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_SKILL_LEARN]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		condition = ""
		if not currentPage:
			currentPage = 1
			index = 0
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
		else:
			index = tooldefine.QUERY_ONCE_NUM_ * ( int(currentPage) - 1 )
			queryCondition = request.GET.get( "condition" )
			queryType, queryText = tuple(eval(queryCondition))
		if queryText == "*":
			pass
		else:
			condition = condition + "and %s = '%s'" % ( queryType, queryText )
		startIndex, endIndex = self.getQueryIndex( index, tooldefine.QUERY_ONCE_NUM_ )
		
		sql = "select roleDBID, roleName, skillID, param1, updateTime, param2, param3 from Log_Skill where action = %s and roleName ='%s' limit %s, %s"
		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql % ( LogDefine.LT_SKILL_LEARN,queryText,str( startIndex ), str( endIndex ) ))
		#totalNumSql 为查询到的记录个数,与分页相关
		totalNumSql = "select count(*) from Log_Skill where action = %s and %s = '%s' " %(LogDefine.LT_SKILL_LEARN, queryType, queryText )
		countNum = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)
		
		message={}
		message["totalNum"]=countNum[0][0]
		if resultInfos:
			page = int(currentPage)
			totalNum = int(message["totalNum"])
			totalPage = int(totalNum / tooldefine.QUERY_ONCE_NUM_)
			if totalPage <= 0:
				totalPage = 1
			context["page"] = page
			context["totalPage"] = totalPage
			context["datas"] = resultInfos
			nextPage = self.getNextPage( page, totalPage )
			prevPage = self.getPrevPage( page )
			context["prevPage"] = prevPage
			context["nextPage"] = nextPage
			context["condition"] = (queryType, queryText)

		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_mail(self, request):
		"""
		玩家邮件记录
		"""
		html_template = "gmtools/query/query_role_mail.html"
		context = self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		page = request.GET.get("page")                  #当前查询页，点击“查询”时并没有
		condition = ""
		if not send_flag and not page:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_MAIL_RECORD]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:    #如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:#“上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * ( int( page ) - 1 )
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			#而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			#的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get( "condition" )#查询条件
			queryType, queryText = tuple(eval(queryCondition))
		if queryText and queryText.strip() == "*":
			#如果“*”，则不需要查询条件
			pass
		else:
			condition = " where (action = %s  and senderName =  '%s') or ( (action = %s or action = %s or action = %s ) and receiverName = '%s' ) " % (
				csdefine.MAIL_TYPE_SEND, queryText, csdefine.MAIL_TYPE_READ, csdefine.MAIL_TYPE_DEL, csdefine.MAIL_TYPE_EXTRACT, queryText )
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		sql = "select action, param2, mailType, senderName, receiverName, updateTime, title, money, itemData from Log_Mail" + condition + "limit %s, %s"
		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql %(str( startIndex ), str( endIndex )))
		#totalNumSql 为查询到的记录个数,与分页相关
		totalNumSql = "select count(*) from Log_Mail" + condition
		countNum = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)
		message = {}
		message["totalNum"]= countNum[0][0]
		if resultInfos:
			page = int(page)
			totalNum = message["totalNum"]
			totalPage = math.ceil(totalNum / tooldefine.QUERY_ONCE_NUM_)
			if totalPage <= 0:
				totalPage = 1
			context["page"] = page
			context["totalPage"] = totalPage
			nextPage = self.getNextPage( page, totalPage )
			prevPage = self.getPrevPage( page )
			context["prevPage"] = prevPage
			context["nextPage"] = nextPage
			context["condition"] = (queryType, queryText)
			for data in resultInfos:
				itemData = pickle.loads(eval(data[8]))
				data[8]=["","","",""]
				for index in range(0,len(itemData)):
					data[8][index]=itemData[index]["id"]
				if int(data[0]) in stringRes.MAIL_CH_DICT:
					if int(data[0]==3):
						data[0] =stringRes.MAIL_DEL_CH_DICT[int(data[1])]
					else:
						data[0] = stringRes.MAIL_CH_DICT[int(data[0])]
					if data[2]==2:
						data[3]="系统"
			context["datas"] = resultInfos
		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_vend(self, request):
		"""
		玩家摆摊记录
		"""
		html_template = "gmtools/query/query_role_vend.html"
		context = self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		page = request.GET.get("page")                  #当前查询页，点击“查询”时并没有
		condition = ""
		if not send_flag and not page:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_VEND_TRADE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:    #如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:#“上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * ( int( page ) - 1 )
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			#而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			#的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get( "condition" )#查询条件
			queryType, queryText = tuple(eval(queryCondition))
		if queryText and queryText.strip() == "*":
			#如果“*”，则不需要查询条件
			pass
		else:
			condition = " and %s = '%s' " %  (queryType, queryText)
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		sql = SQLConfig.SQL_QUERY_VEND_TRADE + condition + SQLConfig.QUERY_RANGE % ( str( startIndex ), str( endIndex ) )
		if "limit" in sql:
			totalNumSql = "select count(*) " + sql[sql.find("from"): sql.find("limit")]
		else:
			totalNumSql = "select count(*) " + sql[sql.find("from"):]
		totalNum = 0
		totalNumResult = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)
		if len(totalNumResult) > 0:
			totalNum = totalNumResult[0][0]
		else:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		page = int(page)
		totalPage = math.ceil(totalNum / tooldefine.QUERY_ONCE_NUM_)
		if totalPage <= 0:
			totalPage = 1
		context["page"] = page
		context["totalPage"] = totalPage
		context["datas"] = datas
		nextPage = self.getNextPage(page, totalPage)
		prevPage = self.getPrevPage(page)
		context["prevPage"] = prevPage
		context["nextPage"] = nextPage
		context["condition"] = (queryType, queryText)
		context["queryText"] = queryText
		return render( request, html_template, context )

	def query_item_flow(self, request, uid):
		"""
		查询玩家物品流向数据
		"""
		context = self.initContext()
		#查询物品获得途径
		sql_item_access = "select roleName, itemUid, itemName, itemNum, param2, updatetime from %s where action = %s" % (SQLConfig.LOG_TYPE_ITEM, LogDefine.LT_ITEM_ADD)
		if uid:
			sql_item_access += " and itemUid = %s order by updatetime asc limit 1" % uid
		item_access_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_item_access)
		if len(item_access_result) > 0:
			item_access_result = item_access_result[0]
			item_access = {"roleName": item_access_result[0], "itemUid": item_access_result[1], "itemNum": item_access_result[3], "itemName": item_access_result[2], "updatetime": item_access_result[5]}
			item_access["tradeType"] = stringRes.ITEM_ADD_REASON_DICT[int(item_access_result[4])]
			item_access["tradeRole"] = ""
			item_access["type"] = "物品产出信息"
			context["datas"].append(item_access)
		
		#物品删除
		sql_item_del = "select roleName, itemUid, itemName, itemNum, param2, updatetime from %s where action = %s and itemUid = %s order by updatetime desc limit 1" % \
			(SQLConfig.LOG_TYPE_ITEM, LogDefine.LT_ITEM_DEL, uid)
		item_del_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_item_del)
		
		#查询玩家间的物品交易记录
		sql_item_trade = "select roleName, param2, param4, param6, param5, param9, updateTime from %s where action = %s and param4 = '%s' " % (
				SQLConfig.LOG_TYPE_TRADE, LogDefine.LT_TRADE_SWAP_ITEM, uid)
		item_trade_results = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_item_trade)
		if len(item_trade_results) > 0:
			for result in item_trade_results:
				data = {"roleName": result[0], "itemUid": result[2], "itemNum": result[3], "itemName": result[4], "tradeRole": result[1], "updatetime": result[6]}
				data["tradeType"] = stringRes.ITEM_ROLE_TRADE_TYPE_DICT[int(result[5])]
				data["type"] = "玩家间物品交易"
				context["datas"].append(data)

		# 查询玩家与NPC间的物品交易记录
		sql_item_npctrade = "select roleName, param2, param4, param3, action, updateTime, param7 from %s where (action = %s or action = %s or action = %s or action = %s) and param2 = '%s' " % (
			SQLConfig.LOG_TYPE_TRADE, LogDefine.LT_TRADE_NPC_SELL, LogDefine.LT_TRADE_NPC_BUY, LogDefine.LT_TRADE_BUY_BACK, LogDefine.LT_TRADE_BUY_BACK_HIGH, uid)
		item_npctrade_results = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_item_npctrade)
		if len(item_npctrade_results) > 0:
			for result in item_npctrade_results:
				data = {"roleName": result[0], "itemUid": result[1], "itemNum": result[2], "itemName": result[3],"tradeRole": result[6], "updatetime": result[5]}
				data["tradeType"] = stringRes.ITEM_TRADE_TYPE_DICT[int(result[4])]
				data["type"] = "玩家与NPC间物品交易"
				context["datas"].append(data)
		"""
		# 查询物品最终归属信息
		sql_item_belong = "select * from %s where param2 = '%s' or param4 = '%s' order by updatetime desc limit 1" % (SQLConfig.LOG_TYPE_TRADE, uid, uid)
		item_belong_result = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql_item_belong)
		if len(item_belong_result) > 0:
			item_belong_result = item_belong_result[0]
			item_belong = {}
			if item_belong_result[2] == 1:
				item_belong = {"itemUid": item_belong_result[8], "itemNum": item_belong_result[10], "itemName": item_belong_result[9], "updatetime": item_belong_result[1]}
				item_belong["roleName"] = item_belong_result[4]
				item_belong["tradeRole"] = item_belong_result[6]
				item_belong["tradeType"] = stringRes.ITEM_ROLE_TRADE_TYPE_DICT[int(item_belong_result[13])]
				item_belong["type"] = "物品最终归属"
				context["datas"].append(item_belong)
			elif item_belong_result[2] == 5 or item_belong_result[2] == 7:
				item_belong = {"itemUid": item_belong_result[6], "itemNum": item_belong_result[8], "itemName": item_belong_result[7], "updatetime": item_belong_result[1]}
				item_belong["roleName"] = item_belong_result[4]
				item_belong["tradeRole"] = item_belong_result[11]
				item_belong["tradeType"] = stringRes.ITEM_TRADE_TYPE_DICT[item_belong_result[2]]
				item_belong["type"] = "物品最终归属"
				context["datas"].append(item_belong)
		"""
		if len(item_del_result) > 0 and len(context["datas"]) > 0:
			if time.mktime(time.strptime(item_del_result[0][5], "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(context["datas"][-1]["updatetime"], "%Y-%m-%d %H:%M:%S")) > 1: #给以1秒的误差
				item_del_result = item_del_result[0]
				item_del = {"roleName": item_del_result[0], "itemUid": item_del_result[1], "itemNum": item_del_result[3], "itemName": item_del_result[2], "updatetime": item_del_result[5]}
				item_del["tradeType"] = stringRes.ITEM_DEL_REASON_DICT[int(item_del_result[4])]
				item_del["tradeRole"] = ""
				item_del["type"] = ""
				context["datas"].append(item_del)
		
		context["datas"] = sorted(context["datas"], key = lambda data: data["updatetime"])
		return context

	@loginInstannce.login_check
	def query_role_item(self, request):
		"""
		玩家物品流向
		"""
		html_template = "gmtools/query/query_role_item.html"
		context = self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		uid = request.POST.get("uid")       #查询条件的内容
		if not send_flag:                  #初次进入网页
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ITEM_FLOW]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not uid or not uid.strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		else:
			context["uid"] = uid
		context = self.query_item_flow(request, uid)
		if len(context["datas"]) == 0:
			context["error"] = csstatus.QUERY_DATA_FIELD
			return render(request, html_template, context)
		context["uid"] = uid
		return render(request, html_template, context)

	@loginInstannce.login_check
	def query_role_itemRecord(self, request):
		"""
		玩家物品记录查询
		"""
		html_template = "gmtools/query/query_role_itemRecord.html"
		context = {"roleName": "", "itemRecords": [], "coinRecords": [], "error": ""}
		send_flag = request.POST.get("send_flag")
		if not send_flag:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ITEM_RECORD]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		roleName = request.POST.get("roleName", "")
		if not roleName.strip():
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], roleName):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % roleName
			return render(request, html_template, context)
		context["roleName"] = roleName
		#道具获得/消耗记录
		sql = "select updateTime, action, roleName, itemName, itemID, itemUid, itemNum, param1, param2, param3, id from %s " \
			  "where roleName = '%s' and updateTime BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 MONTH) AND CURDATE()" % (SQLConfig.LOG_TYPE_ITEM, roleName)
		resultInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		tempDatas = []
		for data in resultInfos:
			tempDict = {}
			tempDict["roleName"] = data[2]
			tempDict["itemName"] = data[3]
			tempDict["itemID"] = data[4]
			tempDict["itemUid"] = data[5]
			tempDict["itemAmount"] = data[6]
			tempDict["optTime"] = data[0]
			tempDict["optType"] = stringRes.ITEM_ADD_DEL_TYPE_DICT.get(int(data[1]), data[1])
			tempDict["dbid"] = int(data[10])
			if int(data[1]) == LogDefine.LT_ITEM_ADD:
				tempDict["optReason"] = stringRes.ITEM_ADD_REASON_DICT.get(int(data[8]), data[8])
			elif int(data[1]) == LogDefine.LT_ITEM_DEL:
				tempDict["optReason"] = stringRes.ITEM_DEL_REASON_DICT.get(int(data[8]), data[8])
			tempDatas.append(tempDict)
			context["itemRecords"] = tempDatas
		#货币获得/消耗记录
		queryCoinSql = "select roleName, action, oldValue, newValue, reason, updateTime from %s " \
					   "where roleName = '%s' and updateTime BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 MONTH) AND CURDATE()" % (SQLConfig.LOG_TYPE_COIN, roleName)
		queryCoinResults = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], queryCoinSql)
		datas = []
		for result in queryCoinResults:
			data = {"coinType": stringRes.COIN_CH_DICT[result[1]]}
			reasonInt = -1
			try:
				reasonInt = int(result[4])
			except:
				reasonInt = -1
			if result[1] == LogDefine.LT_MONEY_CHANGE:
				data["reason"] = ""
				if (result[2] > result[3]):  # 金钱减少
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]][
						csdefine.MONEY_CHANGE_TYPE_SUB]:
						data["reason"] = result[4]
					else:
						data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_SUB][
							reasonInt]
				elif result[2] < result[3]:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]][
						csdefine.MONEY_CHANGE_TYPE_ADD]:
						data["reason"] = result[4]
					else:
						data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_ADD][
							reasonInt]
			else:
				if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]]:
					data["reason"] = result[4]
				else:
					data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][int(result[4])]
			data["roleName"] = result[0]
			data["oldValue"] = result[2]
			data["newValue"] = result[3]
			data["changeNum"] = int(result[3]) - int(result[2])
			data["updateTime"] = result[5]
			datas.append(data)
		context["coinRecords"] = datas
		return render(request, html_template, context)

	@loginInstannce.login_check
	def query_role_position(self, request):
		"""
		玩家当前位置
		"""
		html_template = "gmtools/query/query_role_position.html"
		context= self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText", "").strip()       #查询条件的内容
		context["queryText"] = queryText
		if not send_flag:                  #初次进入邮件记录网页
			context = self.initContext()
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_POS]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
			
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], queryText):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render( request, html_template, context)
		
		#位置信息
		condition = " where %s = '%s' " % (queryType, queryText.strip())
		sql="select id,sm_playerName, sm_spaceScriptID, sm_0_position, sm_1_position, sm_2_position from tbl_Role"+condition
		tempDatas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(tempDatas)==0:
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render(request, html_template, context)
		datas=[]
		for data in tempDatas:#其实目前仅支持查看指定玩家
			dbid = data[0]
			name = data[1]
			spaceScriptID = data[2]
			positon = "(" + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + ")"
			line = ""
			spaceName = stringRes.SPACE_CH_DICT.get(spaceScriptID, spaceScriptID)
			datas.append([dbid, name, spaceName, line, positon])
		
		#所在分线
		cmd_msg = {}
		cmd_msg["cmd"] = "doActionForPlayer"
		cmd_msg["info"] = {}
		cmd_msg["info"]["cmd_interface"] = "getPlayerLineNumber"
		cmd_msg["info"]["roleName"] = queryText
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, resultInfos = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = resultInfos
			return render( request, html_template, context )
		else:
			datas[0][3] = resultInfos["datas"]["lineNumber"]
		context["datas"] = datas
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_equip(self, request):
		"""
		玩家装备信息
		"""
		html_template = "gmtools/query/query_role_equip.html"
		context= self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText", "")       #查询条件的内容
		context["queryText"] = queryText
		if not send_flag:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_EQUIP]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		sql_queryDBID = "select id from tbl_Role where sm_playerName = '%s'" % queryText.strip()
		results=g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql_queryDBID)
		if len(results) == 0:
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render(request, html_template, context)
		roleDBID = int(results[0][0])
		sql = "select sm_id, sm_uid, sm_order from tbl_Role_itemsBag_items where parentID = %s and (sm_order >= %s and sm_order <= %s)" % (
			roleDBID, ItemTypeEnum.BAG_EQUIPSTART, ItemTypeEnum.BAG_EQUIPEND)
		datas = g_dbInterfaceInst.getGameInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		if len(datas) == 0:
			context["datas"] = []
			return render(request, html_template, context)
		idList = [data[0] for data in datas]
		tempDatas= datas
		cmd_msg = {}
		cmd_msg["cmd"] = "queryItemInfoById"
		cmd_msg["info"] = idList
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		equipDatas=[]
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			equipDatas = message["datas"]
		for i in range(len(tempDatas)):
			equipDatas[i]["id"]=tempDatas[i][0]
			equipDatas[i]["uid"]=tempDatas[i][1]
			equipDatas[i]["quality"] = stringRes.ITEM_QUALITY_CH_DICT.get(int(equipDatas[i]["quality"]), equipDatas[i]["quality"])
		context["datas"] = equipDatas
		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_attribute(self, request):
		"""
		玩家面板属性
		"""
		html_template = "gmtools/query/query_role_attribute.html"
		context= self.initContext_role_attribute()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		condition = ""
		if not send_flag:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_ATTRIBUTE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
			
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], queryText):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render(request, html_template, context)
			
		sql = "select blobParam1, blobParam2, blobParam3 from %s where action = %s and roleName = '%s' ORDER BY id DESC LIMIT 1" % (
			SQLConfig.LOG_TYPE_ROLE, LogDefine.LT_ROLE_PRO_RECORD, queryText)
		tempInfos = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		resultInfos = {}
		resultInfos["datas"] = tempInfos
		datas = resultInfos["datas"]
		if len(datas) == 0:
			context["error"] = csstatus.ROLE_INFO_ERROR % queryText
			return render(request, html_template, context)
			
		blobParam1, blobParam2, blobParam3 = datas[0]
		blobParam1Data = pickle.loads(eval(blobParam1))
		blobParam2Data = pickle.loads(eval(blobParam2))
		blobParam3Data = pickle.loads(eval(blobParam3))
		blobDatas = {}
		blobDatas.update(blobParam1Data)
		blobDatas.update(blobParam2Data)
		blobDatas.update(blobParam3Data)
		blobDatas["roleName"] = queryText
		blobDatas["state"] = ""
		blobDatas["jingjie"] = Functions.getRoleJingjie(blobDatas["level"], blobDatas["xiuwei"], blobDatas["camp"])
		blobDatas["menpai"] = Functions.getRoleMenpai(blobDatas["camp"], blobDatas["profession"])
		blobDatas["hitrate"] = str(blobDatas["hitrate"] / 100) + "%"
		blobDatas["criticalstrike"] = str(blobDatas["criticalstrike"] / 100) + "%"
		blobDatas["parry"] = str(blobDatas["parry"] / 100) + "%"
		blobDatas["dodgerate"] = str(blobDatas["dodgerate"] / 100) + "%"
		blobDatas["healingrate"] = str(blobDatas["healingrate"] / 100) + "%"
		context["roleInfo"] = blobDatas
		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_task(self, request):
		"""
		玩家任务记录
		"""
		html_template = "gmtools/query/query_role_task.html"
		context= self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		page = request.GET.get("page")                  #当前查询页，点击“查询”时并没有
		condition = ""
		if not send_flag and not page:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_TASK]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:    #如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:#“上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * ( int( page ) - 1 )
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			#而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			#的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get( "condition" )#查询条件
			queryType, queryText = tuple(eval(queryCondition))
			
		if queryText != "*":
			if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], queryText):
				context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
				return render(request, html_template, context)
				
		if queryText and queryText.strip() == "*":
			#如果“*”，则不需要查询条件
			pass
		else:
			condition = "%s = '%s'" %  (queryType, queryText)
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		sql = "select id, roleDBID, roleName, roleLevel, questID, questName, action, updateTime from %s" % SQLConfig.LOG_TYPE_QUEST
		totalNumSql = "select count(*) from %s" % SQLConfig.LOG_TYPE_QUEST
		if condition:
			sql = sql + " where " + condition
			totalNumSql = totalNumSql + " where " + condition
		sql += " limit %s, %s" % (startIndex, endIndex)
		totalNum = int(g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)[0][0])
		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		page = int(page)
		totalPage = math.ceil(totalNum / tooldefine.QUERY_ONCE_NUM_)
		if totalPage <= 0:
			totalPage = 1
			
		tempDatas = []
		for data in datas:
			tempData = list(data)
			tempData[6] = stringRes.QUEST_STATE_DICT.get(int(tempData[6]), tempData[6])
			tempDatas.append(tempData)
			
		context["page"] = page
		context["totalPage"] = totalPage
		context["datas"] = tempDatas
		nextPage = self.getNextPage( page, totalPage )
		prevPage = self.getPrevPage( page )
		context["prevPage"] = prevPage
		context["nextPage"] = nextPage
		context["condition"] = (queryType, queryText)
		context["queryText"] = queryText
		return render( request, html_template, context )

	@loginInstannce.login_check
	def query_role_money(self, request):
		"""
		玩家金钱信息
		"""
		html_template = "gmtools/query/query_role_money.html"
		context= {"error": "", "datas": [], "queryText": "", "page": None, "totalPage": None, "prevPage": None, "nextPage": None, "condition": ""}
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		page = request.GET.get("page")
		if not send_flag and not page:                  #初次进入网页
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_COIN]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:    #如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:#“上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * (int(page) - 1)
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			#而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			#的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get( "condition" )#查询条件
			queryType, queryText = tuple(eval(queryCondition))
		if not queryType or not queryText:
			context["error"] = csstatus.QUERY_SELECT_FIELD
			return render(request, html_template, context)
		if not g_dbInterfaceInst.checkRole(request.session[tooldefine.CURR_SERVER], queryText):
			context["error"] = csstatus.ROLE_INFO_NOT_EXIST % queryText
			return render(request, html_template, context)
		condition = "where %s = '%s'" % (queryType, queryText.strip())
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		queryCoinSql = "select roleName, action, oldValue, newValue, reason, updateTime from Log_Coin %s limit %s, %s" % (condition, startIndex, endIndex)
		queryCoinResults = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], queryCoinSql)
		datas=[]
		for result in queryCoinResults:
			data = {"coinType": stringRes.COIN_CH_DICT[result[1]]}
			reasonInt = -1
			try:
				reasonInt = int(result[4])
			except:
				reasonInt = -1
			if result[1] == LogDefine.LT_MONEY_CHANGE:
				data["reason"] = ""
				if(result[2] > result[3]): #金钱减少
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_SUB]:
						data["reason"] = result[4]
					else:
						data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_SUB][reasonInt]
				elif result[2] < result[3]:
					if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_ADD]:
						data["reason"] = result[4]
					else:
						data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][csdefine.MONEY_CHANGE_TYPE_ADD][reasonInt]
			else:
				if reasonInt == -1 or reasonInt not in stringRes.COIN_CHANGE_REASON_DICT[result[1]]:
					data["reason"] = result[4]
				else:
					data["reason"] = stringRes.COIN_CHANGE_REASON_DICT[result[1]][int(result[4])]
			data["roleName"] = result[0]
			data["oldValue"] = result[2]
			data["newValue"] = result[3]
			data["changeNum"] = int(result[3]) - int(result[2])
			data["updateTime"] = result[5]
			datas.append(data)
		context["datas"] = datas
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
		context["queryText"] = queryText
		return render(request, html_template, context)

	@loginInstannce.login_check
	def query_role_recharge(self, request):
		"""
		玩家充值记录
		"""
		html_template = "gmtools/query/query_role_recharge.html"
		context= self.initContext()
		send_flag = request.POST.get("send_flag")       #是否是点击“查询”发送过来的信息
		queryType = request.POST.get("queryType")       #查询类型：DBID，或者玩家名字
		queryText = request.POST.get("queryText")       #查询条件的内容
		page = request.GET.get("page")                  #当前查询页，点击“查询”时并没有
		condition = ""
		if not send_flag and not page:                  #初次进入邮件记录网页
			return render( request, html_template, context )
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ROLE_INFO][tooldefine.ROLE_INFO_QUERY_ROLE_RECHARGE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if not page:    #如果不是选择“上一页”或“下一页”，page为None，表示当前查询页为第一页
			if not queryType or not queryText:
				context["error"] = csstatus.QUERY_SELECT_FIELD
				return render(request, html_template, context)
			page = 1
			index = 0
		else:#“上一页”或“下一页”
			index = tooldefine.QUERY_ONCE_NUM_ * ( int( page ) - 1 )
			# 由于每次查询记录都是查询指定条数，通过选择“上一页”或“下一页”来查询前面或后面的记录，
			#而只有按“查询”时才能通过request.POST.get获取查询类型和查询条件内容，所以需用通过request.GET.get
			#的方式获取查询条件，这个需要在HTML文件那边处理
			queryCondition = request.GET.get( "condition" )#查询条件
			queryType, queryText = tuple(eval(queryCondition))
			
		if queryText != "*":
			if not g_dbInterfaceInst.checkAccount(request.session[tooldefine.CURR_SERVER], queryText):
				context["error"] = csstatus.ACCOUNT_NOT_EXIST % queryText
				return render(request, html_template, context)
				
		if queryText and queryText.strip() == "*":
			#如果“*”，则不需要查询条件
			pass
		else:
			condition = "where %s = '%s'  " %  (queryType, queryText)
		startIndex, endIndex = self.getQueryIndex(index, tooldefine.QUERY_ONCE_NUM_)
		sql = "select accountName,transactionID, updateTime, rechargeType, coinType, value from %s %s limit %s, %s" % (SQLConfig.LOG_TYPE_RECHARGE, 
			condition, startIndex, endIndex)
		totalNumSql = "select count(*) from %s %s" % (SQLConfig.LOG_TYPE_RECHARGE, condition)
		totalNum = int(g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], totalNumSql)[0][0])
		datas = g_dbInterfaceInst.getLogInfoBySql(request.session[tooldefine.CURR_SERVER], sql)
		tempDatas = []
		for data in datas:
			tempData = list(data)
			if int( tempData[-2] ) in stringRes.MONEY_CH_DICT:
				tempData[-2] = stringRes.MONEY_CH_DICT[ int( tempData[-2] ) ]
			tempDatas.append(tempData)
				
		totalPage = math.ceil(totalNum / tooldefine.QUERY_ONCE_NUM_)
		if totalPage <= 0:
			totalPage = 1
		context["page"] = int(page)
		context["totalPage"] = totalPage
		context["datas"] = tempDatas
		context["prevPage"] = self.getPrevPage( page )
		context["nextPage"] = self.getNextPage( page, totalPage )
		context["condition"] = (queryType, queryText)
		context["queryText"] = queryText
		
		return render( request, html_template, context )
		
g_queryInstance = QueryManager.instance()