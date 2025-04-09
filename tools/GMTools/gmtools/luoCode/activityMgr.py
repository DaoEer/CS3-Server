# -*- coding: utf-8 -*-


import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets
from django import forms

from cs3_web_services import settings
from common import baseConnector, csdefine, stringRes,csstatus, tooldefine, Functions
from . import login
from . import GMActionLog
logInstance = GMActionLog.g_logInstance

g_baseappConnector = baseConnector.g_baseappConnector
loginInstance = login.g_loginInstance

def get_cmd_china_str(cmd, china_str):
	if cmd == "*":  # 正确的配置,"分"不会"*"
		cmd_str = "每%s" % china_str
	else:
		if "|" in cmd:
			cmd_list = cmd.split("|")
			cmd_list_str = ""
			for min in cmd_list:
				cmd_list_str = cmd_list_str + min + china_str + "、"
			cmd_list_str = cmd_list_str[:-1]
		elif "-" in cmd:
			cmd_list = cmd.split("-")
			min_start = cmd_list[0]
			min_end = cmd_list[1]
			cmd_list_str = min_start + "%s至" % china_str + min_end + china_str
		else:
			cmd_list_str = cmd + china_str
		cmd_str = cmd_list_str
	return cmd_str

def trans_cmd_format(datas):
	""""""
	#cmd_china_str = {0:"分"，1: "时", 2: "日", 3: "月", 4: "周"}
	for data in datas:
		minute, hour, day, month, wday = data["cmd"].split(" ")
		minute_str = get_cmd_china_str(minute, "分")
		hour_str = get_cmd_china_str(hour, "点")
		day_str = get_cmd_china_str(day, "日")
		month_str = get_cmd_china_str(month, "月")
		wday_str = get_cmd_china_str(wday, "周")
		data["cmd_str"] = ""
		if day != "*" or (day == "*" and wday == "*"):
			data["cmd_str"] = month_str + day_str + hour_str + minute_str
		elif day == "*" and wday != "*" :
			data["cmd_str"] = month_str + wday_str + hour_str + minute_str
		#1.day != "*" and wday != "*"的配置错误
	return datas
	
	

class ActivityManage(object):
	_instance = None
	def __init__(self, datas = {}):
		self.html_template = "gmtools/activity/activity_manage.html"
	
	@staticmethod
	def instance():
		if not ActivityManage._instance:
			ActivityManage._instance = ActivityManage()
		return ActivityManage._instance
		
	def getActivityBaseInfo(self, request):
		"""
		获取基础数据
		"""
		context = {}
		context["actnameselect"] = request.POST.get("act_name_select", "")
		context["sendflag"] = request.POST.get("send_flag", "")
		context["startdate"] = request.POST.get("start_date", "")
		context["starttime"] = request.POST.get("start_time", "")
		context["error"] = ""
		context["success"] = ""
		context["queryflag"] = False
		activeDatas = Functions.getActivityDatas()
		activitylist = []
		for key in sorted(activeDatas.keys()):
			name = activeDatas[key]["Name"]
			activitylist.append((key, name))
		context.update({"actlist": activitylist})
		return context
		
	def getActivityNameByKey(self, key):
		for actKey, name in stringRes.ACTIVITY_NAME_FOR_KEY_DICT.items():
			if actKey.lower() == key:
				return name
			return ""
		
	def setActivityName(self, datas):
		for data in datas:
			data["name"] = self.getActivityNameByKey(data["name"])
			data["startTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["startTime"]))
			
	def siftingSchemeActivityData(self, datas):
		tempDatas = []
		for data in datas:
			if data["key"] in stringRes.ACTIVITY_NAME_FOR_KEY_DICT:
				tempDatas.append(data)
		return tempDatas
		
	def startActivityImmediate(self, request):
		"""
		即时开启活动
		"""
		context = self.getActivityBaseInfo(request)
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACTIVITY_MGR][tooldefine.ACTIVITY_MGR_ACTITY_OPEN]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, self.html_template, context )
			
		activeDatas = Functions.getActivityDatas()
		cmd_msg = {}
		cmd_msg["cmd"] = "startActivity"
		cmd_msg["info"] = {}
		cmd_msg["info"]["actMgr"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["ClassName"]
		cmd_msg["info"]["startMethod"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["StartMethod"]
		cmd_msg["info"]["hasActivityMgr"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["HasActivityMgr"]
		cmd_msg["info"]["callbackArgs"] = str(activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["CallbackArgs"])
		cmd_msg["info"]["type"] = 1
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)

		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.openActivityLog(request.session["gm_userid"], request.session["gm_level"], context["actnameselect"], activeDatas[context["actnameselect"]]["Name"], 
				currServerkey, request.serverInfos.get(currServerkey, ""))
			context["success"] = csstatus.OPERATION_SUCCEED + "," + csstatus.ACTIVITY_START_SUCCEED_NOW
		return render(request, self.html_template, context)
		
	def startActivityImmediate_init(self):
		context={"startdate":"","starttime":"","actnameselect":"","error":"","success":""}
		
	def startActivityTiming(self, request):
		"""
		定时开启活动
		"""
		self.startActivityImmediate_init()
		context = self.getActivityBaseInfo(request)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACTIVITY_MGR][tooldefine.ACTIVITY_MGR_ACTITY_DELAY_ADD]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, self.html_template, context )

		cmd_msg = {}
		cmd_msg["info"] = {}
		cmd_msg["cmd"] = "startActivity"

		timeStr = context["startdate"] + " " + context["starttime"]
		if not context["startdate"] or not context["starttime"]:
			context["error"] = csstatus.ACTIVITY_START_TIME_NOT_INPUT
			return render(request, self.html_template, context)
		timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
		t = int(time.mktime(timeArray))
		if t < time.time():
			context["error"] = csstatus.ACTIVITY_START_SUCCEED_DELAY_TIME_ERROR
			return render(request, self.html_template, context)
			
		activeDatas = Functions.getActivityDatas()
		
		cmd_msg["info"]["time"] = t
		cmd_msg["info"]["key"] = context["actnameselect"]
		cmd_msg["info"]["actMgr"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["ClassName"]
		cmd_msg["info"]["startMethod"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["StartMethod"]
		cmd_msg["info"]["hasActivityMgr"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["HasActivityMgr"]
		cmd_msg["info"]["callbackArgs"] = str(activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["CallbackArgs"])
		cmd_msg["info"]["type"] = 2

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)

		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.addDelayActivity(request.session["gm_userid"], request.session["gm_level"], cmd_msg["info"]["key"], activeDatas[context["actnameselect"]]["Name"], 
			timeStr, currServerkey, request.serverInfos.get(currServerkey, ""))

			context["success"] = csstatus.OPERATION_SUCCEED + "," + csstatus.ACTIVITY_START_SUCCEED_DELAY % timeStr

		return render( request, self.html_template, context )
		
	def endActivityImmediate(self, request):
		"""
		关闭活动
		"""
		self.startActivityImmediate_init()
		context = self.getActivityBaseInfo(request)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACTIVITY_MGR][tooldefine.ACTIVITY_MGR_ACTITY_CLOSE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, self.html_template, context )
		
		activeDatas = Functions.getActivityDatas()
		
		endMethod = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["EndMethod"]
		if not endMethod:
			context["error"] = csstatus.ACTIVITY_NO_END_METHOD
			return render( request, self.html_template, context )
		
		cmd_msg = {}
		cmd_msg["cmd"] = "endActivity"
		cmd_msg["info"] = {}
		cmd_msg["info"]["actMgr"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["ClassName"]
		cmd_msg["info"]["endMethod"] = activeDatas[context["actnameselect"]]["ActivityMgrInfo"]["EndMethod"]

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)

		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.closeActivityLog(request.session["gm_userid"], request.session["gm_level"], context["actnameselect"], activeDatas[context["actnameselect"]]["Name"], 
				currServerkey, request.serverInfos.get(currServerkey, ""))

			context["success"] = csstatus.OPERATION_SUCCEED + ",【%s】" % activeDatas[context["actnameselect"]]["Name"] + csstatus.ACTIVITY_END_SUCCEED

		return render( request, self.html_template, context )
		
	def activityQuery(self, request, agrs = {}):
		"""
		查看定时活动
		"""
		context ={}
		self.activityQuery_init()
		context = self.getActivityBaseInfo(request)
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACTIVITY_MGR][tooldefine.ACTIVITY_MGR_ACTITY_DELAY_QUERY]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, self.html_template, context )

		if agrs:
			context.update(agrs)
			if context["error"]:
				return render(request, self.html_template, context)
		cmd_msg = {}
		cmd_msg["cmd"] = "queryActivityScheme"
		cmd_msg["info"] = {}

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			activeDatas = Functions.getActivityDatas()
			for data in message["datas"]:
				data["name"] = activeDatas.get(data["key"], {"Name": ""})["Name"]
				data["startTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["startTime"]))
			context["datas"] = message["datas"]
			context["queryflag"] = True
		return render( request, self.html_template, context )
	
	def activityQuery_init(self):
		context = {"error":"","datas":"","queryflag":""}
		
	@loginInstance.login_check
	def activity_manage(self, request):
		"""
		活动管理主页面
		"""
		context = self.getActivityBaseInfo(request)
		return render(request, self.html_template, context)

	@loginInstance.login_check
	def activity_action(self, request):
		"""
		执行某行为，开启活动、关闭活动、或者查看定时活动
		"""
		if "start_activity_immediate" in request.POST:
			return self.startActivityImmediate(request)
		elif "end_activity_immediate" in request.POST:
			return self.endActivityImmediate(request)
		elif "start_activity_timing" in request.POST:
			return self.startActivityTiming(request)
		elif "activity_query" in request.POST:
			return self.activityQuery(request)
			
		context = self.getActivityBaseInfo(request)
		return render(request, self.html_template, context)
		
	@loginInstance.login_check
	def activity_delete(self, request):
		"""
		删除定时活动
		"""
		context = self.getActivityBaseInfo(request)

		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_ACTIVITY_MGR][tooldefine.ACTIVITY_MGR_ACTITY_DELAY_DEL]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render(request, self.html_template, context)

		key = request.GET.get("key")
		schemeString = request.GET.get("schemeString")
		callbackName = request.GET.get("callbackName")
		activeDatas = Functions.getActivityDatas()
		actMgr = activeDatas.get(key, {}).get("ActivityMgrInfo", {}).get("ClassName", "")
		cmd_msg = {}
		cmd_msg["cmd"] = "cancelActivity"
		cmd_msg["info"] = {}
		cmd_msg["info"]["key"] = key
		cmd_msg["info"]["schemeString"] = schemeString
		cmd_msg["info"]["callbackName"] = callbackName
		cmd_msg["info"]["actMgr"] = actMgr

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)

		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			context["success"] = csstatus.OPERATION_SUCCEED
			currServerkey = request.session[tooldefine.CURR_SERVER]
			#logInstance.cancelDelayActivity(request.session["gm_userid"], request.session["gm_level"], tooldefine.ACTIVITY_KEY_AND_METHOD_DICT[int(context["actnameselect"])][3],
			#	stringRes.ACTIVITY_NAME_DICT.get(int(context["actnameselect"]), 	context["actnameselect"]), currServerkey, request.serverInfos.get(currServerkey, ""))

		return self.activityQuery(request, context)
		
	def activity_delete_init(self):
		context = {"error":""}
		
g_activityInstance = ActivityManage.instance()