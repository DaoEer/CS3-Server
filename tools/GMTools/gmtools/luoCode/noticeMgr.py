# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from . import login
from . import GMActionLog
from common import csstatus,baseConnector,csdefine, tooldefine

import hashlib
import time

loginInstannce = login.g_loginInstance
g_baseappConnector = baseConnector.g_baseappConnector
logInstance = GMActionLog.g_logInstance

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


class NoticeManager:
	"""
	公告管理器
	"""
	_instance = None
	def __init__(self):
		pass
	
	@staticmethod
	def instance():
		"""
		NoticeManager实例
		"""
		if NoticeManager._instance == None:
			NoticeManager._instance = NoticeManager()
		return NoticeManager._instance

	@loginInstannce.login_check
	def noticeBase(self, request):
		"""
		公告
		"""
		html_template = "gmtools/notice/notice_base.html"
		context = {}
		return render(request, html_template, context)

	def initContext(self):
		"""
		初始化公告相关数据
		"""
		context = {"error": "", "success": "", "noticeInfo": {}}
		context["noticeInfo"]["sendNumber"] = ""
		context["noticeInfo"]["timeInterval"] = ""
		context["noticeInfo"]["itemInterval"] = ""
		context["noticeInfo"]["groupInterval"] = ""
		context["noticeInfo"]["noticeName"] = ""
		context["noticeInfo"]["noticeContent"] = ""
		context["noticeInfo"]["noticeContents"]=[]
		context["noticeInfo"]["sendDate"] = ""
		context["noticeInfo"]["sendTime"] = ""
		context["noticeProps"] = ""
		context["datas"]=[]
		context["queryflag"] = False
		return context

	@loginInstannce.login_check
	def noticeInstant(self, request):
		"""
		即时公告
		"""
		html_template = "gmtools/notice/notice_instant.html"
		context = {"error": "", "success": "", "noticeInfo": {}}
		sendFlag = request.POST.get("sendFlag", None)
		sendNumber = request.POST.get("sendNumber", 0)
		timeInterval = request.POST.get("timeInterval", 0)
		noticeContent = request.POST.get("noticeContent", "")
		if not sendFlag:
			context=self.initContext()
			return render(request, html_template, context)
			
		context["noticeInfo"]["sendNumber"] = sendNumber 
		context["noticeInfo"]["timeInterval"] = timeInterval
		context["noticeInfo"]["noticeContent"] = noticeContent
		try:
			sendNumber = int(sendNumber)
			timeInterval = int(timeInterval)
		except:
			context["error"] = csstatus.NOTICE_SEND_NUMBER_INTERVAL_FORMAT_ERROR
			return render(request, html_template, context)
		if not noticeContent:
			context["error"] = csstatus.NOTICE_SEND_FIELD
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_NOTICE_MGR][tooldefine.NOTICE_MGR_NOTICE_SEND_INSTANT]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		cmd_msg = {}
		cmd_msg["cmd"] = "noticeInstant"
		cmd_msg["info"] = {}
		cmd_msg["info"]["timeInterval"] = timeInterval
		cmd_msg["info"]["sendNumber"] = sendNumber
		cmd_msg["info"]["noticeContent"] = noticeContent
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.sendInstantNotice(request.session["gm_userid"], request.session["gm_level"], sendNumber, timeInterval, "", noticeContent, currServerkey, request.serverInfos.get(currServerkey, ""))
				
			context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)

	@loginInstannce.login_check
	def noticeTimingQuery(self, request, html_template):
		"""
		查看定时公告
		"""
		cmd_msg = {}
		cmd_msg["cmd"] = "queryNoticeSchemes"
		cmd_msg["info"] = {}
		context = self.initContext()
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			tempData=message["datas"]
			noticeList=[]
			for triggerTime in tempData:
				info=tempData.get(triggerTime)
				noticeID=list(info)[0]
				infos=info.get(noticeID)
				schemeName=infos[0]
				itemInterval=infos[1]
				groupInterval=infos[2]
				sendNumber=infos[3]
				noticeContent=infos[4]
				data = {"cmd": triggerTime, "key": noticeID, "name": schemeName, "itemInterval":itemInterval,
						"groupInterval":groupInterval, "sendNumber":sendNumber, "noticeContent": "|".join(noticeContent)}
				noticeList.append(data)
			context["datas"] = trans_cmd_format(noticeList)
			context["queryflag"] = True
		return render(request, html_template, context)

	@loginInstannce.login_check
	def noticeTiming(self, request):
		"""
		定时公告
		"""
		html_template = "gmtools/notice/notice_timing.html"
		context = {"error": "", "success": "", "noticeInfo": {}}
		sendFlag = request.POST.get("sendFlag", None)
		sendNumber = request.POST.get("sendNumber", 0)
		timeInterval = request.POST.get("timeInterval", 0)
		noticeName = request.POST.get("noticeName", "")
		noticeContent = request.POST.get("noticeContent", "")
		sendDate = request.POST.get("sendDate", "")
		sendTime = request.POST.get("sendTime", "")

		context["noticeInfo"]["sendNumber"] = sendNumber
		context["noticeInfo"]["timeInterval"] = timeInterval
		context["noticeInfo"]["noticeName"] = noticeName
		context["noticeInfo"]["noticeContent"] = noticeContent
		context["noticeInfo"]["sendDate"] = sendDate
		context["noticeInfo"]["sendTime"] = sendTime
		context["queryflag"] = False
		if not sendFlag:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_NOTICE_MGR][tooldefine.NOTICE_MGR_NOTICE_SEND_DELAY]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if "queryTimingNoticeInfoBtn" in request.POST:
			return self.noticeTimingQuery(request,html_template)
		try:
			sendNumber = int(sendNumber)
			timeInterval = int(timeInterval)
		except:
			context["error"] = csstatus.NOTICE_SEND_NUMBER_INTERVAL_FORMAT_ERROR
			return render(request, html_template, context)
		if not sendDate.strip() or not sendTime.strip() or not noticeName.strip() or not noticeContent.strip():
			context["error"] = csstatus.NOTICE_SEND_FIELD
			return render(request, html_template, context)
		sendtime = time.mktime(time.strptime(sendDate+sendTime, "%Y-%m-%d%H:%M:%S"))
		if sendtime < time.mktime(time.localtime()):
			context["error"] = csstatus.NOTICE_SEND_DATE_TIME_ERROR
			return render(request, html_template, context)
		cmd_msg = {}
		cmd_msg["cmd"] = "noticeTiming"
		cmd_msg["info"] = {}
		cmd_msg["info"]["timeInterval"] = timeInterval
		cmd_msg["info"]["sendNumber"] = sendNumber
		cmd_msg["info"]["noticeName"] = noticeName
		cmd_msg["info"]["noticeContent"] = noticeContent
		cmd_msg["info"]["sendDate"] = sendDate
		cmd_msg["info"]["sendTime"] = sendTime
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.sendDelayNotice(request.session["gm_userid"], request.session["gm_level"], sendNumber, timeInterval, noticeName, noticeContent, 
				sendDate + " " + sendTime, currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)
		
	def sendMultipleNotice(self, request, context, html_template):
		"""
		发送多条公告
		"""
		if len(context["noticeInfo"]["noticeContents"]) <= 0:
			context["error"] = csstatus.NOTICE_CONTENT_LEN_ERROR
			return render(request, html_template, context)
		if not context["noticeInfo"]["noticeName"].strip():
			context["error"] = csstatus.NOTICE_SEND_FIELD
			return render(request, html_template, context)
		for notice in context["noticeInfo"]["noticeContents"]:
			if not notice["content"].strip():
				context["error"] = csstatus.NOTICE_SEND_FIELD
				return render(request, html_template, context)
		#日期和时间都不为空时
		if context["noticeInfo"]["sendDate"].strip() and context["noticeInfo"]["sendTime"].strip():
			sendtime = time.mktime(time.strptime(context["noticeInfo"]["sendDate"] + context["noticeInfo"]["sendTime"], "%Y-%m-%d%H:%M:%S"))
			if sendtime < time.mktime(time.localtime()):
				context["error"] = csstatus.NOTICE_SEND_DATE_TIME_ERROR
				return render(request, html_template, context)
		# 日期和时间都为空时
		elif not context["noticeInfo"]["sendDate"].strip() and not context["noticeInfo"]["sendTime"].strip():
			context["noticeInfo"]["sendDate"] = context["noticeInfo"]["sendTime"] = ""
			context["error"] = csstatus.NOTICE_SEND_FIELD
			return render(request, html_template, context)
		# 日期或时间为空时
		elif not context["noticeInfo"]["sendDate"].strip() or not context["noticeInfo"]["sendTime"].strip():
			context["error"] = csstatus.NOTICE_SEND_FIELD
			return render(request, html_template, context)

		try:
			sendNumber = int(context["noticeInfo"]["sendNumber"])
			itemInterval = int(context["noticeInfo"]["itemInterval"])
			groupInterval = int(context["noticeInfo"]["groupInterval"])
		except:
			context["error"] = csstatus.NOTICE_SEND_NUMBER_INTERVAL_FORMAT_ERROR
			return render(request, html_template, context)
		cmd_msg = {}
		cmd_msg["cmd"] = "sendMultipleNotice"
		cmd_msg["info"] = {}
		cmd_msg["info"]["sendNumber"] = sendNumber
		cmd_msg["info"]["itemInterval"] = itemInterval
		cmd_msg["info"]["groupInterval"] = groupInterval
		cmd_msg["info"]["sendDate"] = context["noticeInfo"]["sendDate"]
		cmd_msg["info"]["sendTime"] = context["noticeInfo"]["sendTime"]
		cmd_msg["info"]["noticeName"] = context["noticeInfo"]["noticeName"]
		cmd_msg["info"]["noticeContent"]=context["noticeInfo"]["noticeContents"]

		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.sendMultipleNotice(request.session["gm_userid"], request.session["gm_level"], sendNumber, itemInterval, groupInterval, context["noticeInfo"]["noticeName"], 
				str(context["noticeInfo"]["noticeContents"]), context["noticeInfo"]["sendDate"] + " " + context["noticeInfo"]["sendTime"], currServerkey, request.serverInfos.get(currServerkey, ""))
				
			context["success"] = csstatus.OPERATION_SUCCEED
		return render(request, html_template, context)
		
	@loginInstannce.login_check
	def noticeMultiple(self, request):
		"""
		多条公告
		"""
		html_template = "gmtools/notice/notice_multiple.html"
		context = {"error": "", "success": "", "noticeInfo": {}, "queryflag": False, "noticeProps": ""}
		sendFlag = request.POST.get("sendFlag", None)
		context["noticeInfo"]["sendNumber"] = request.POST.get("sendNumber", 0)
		context["noticeInfo"]["itemInterval"] = request.POST.get("itemInterval", 0)
		context["noticeInfo"]["groupInterval"] = request.POST.get("groupInterval", 0)
		context["noticeInfo"]["sendDate"] = request.POST.get("sendDate", "")
		context["noticeInfo"]["sendTime"] = request.POST.get("sendTime", "")
		context["noticeInfo"]["noticeName"] = request.POST.get("noticeName", "")
		context["noticeInfo"]["noticeContents"] = []
		noticeProps = request.POST.get("noticeProps", "")
		if noticeProps:
			tempData = {}
			for notice in noticeProps.split("*(NOTICE_SEPARATOR)&"):
				context["noticeInfo"]["noticeContents"].append({"content": notice, "index": len(context["noticeInfo"]["noticeContents"])})
		
		if not sendFlag:
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_NOTICE_MGR][tooldefine.NOTICE_MGR_NOTICE_SEND_MULTIPLE]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
			
		if "queryMultipleNoticeInfoBtn" in request.POST:
			return self.noticeTimingQuery(request, html_template)
		elif "sendMultipleNoticeBtn" in request.POST:
			return self.sendMultipleNotice(request, context, html_template)
		return render(request, html_template, context)

	@loginInstannce.login_check
	def notice_delete(self, request):
		"""
		删除定时公告
		"""
		html_template = "gmtools/notice/notice_timing.html"
		returnTemplate=request.GET.get("returnTemplate","")
		if returnTemplate=="multiple":
			html_template = "gmtools/notice/notice_multiple.html"
		cmd = request.GET.get("cmd")
		name=request.GET.get("name")
		context={"success": "", "error": ""}
		try:
			key = int(request.GET.get("key"))
		except:
			context["error"] = csstatus.NOTICE_SEND_NUMBER_INTERVAL_FORMAT_ERROR
			return render(request, html_template, context)
			
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_NOTICE_MGR][tooldefine.NOTICE_MGR_NOTICE_TIMEING_DEL]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.delTimingNotice(request.session["gm_userid"], request.session["gm_level"], request.GET.get("sendNumber"), request.GET.get("itemInterval"), name, 
			request.GET.get("content"), request.GET.get("cmd_str"), currServerkey, request.serverInfos.get(currServerkey, ""), request.GET.get("groupInterval", ""))
		
		cmd_msg = {}
		cmd_msg["cmd"] = "deleteNotice"
		cmd_msg["info"] = {}
		cmd_msg["info"]["schemeName"] = name
		cmd_msg["info"]["triggerTime"] = cmd
		cmd_msg["info"]["timerNoticeID"] = key
		connector = g_baseappConnector.getConnection(request.session[tooldefine.CURR_SERVER])
		result, message = connector.send_msg(cmd_msg)
		if result == tooldefine._MSG_ERROR:
			context["error"] = message
			return render(request, html_template, context)
		else:
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.delTimingNotice(request.session["gm_userid"], request.session["gm_level"], request.GET.get("sendNumber"), request.GET.get("itemInterval"), request.GET.get("name"), name, 
				request.GET.get("content"), request.GET.get("cmd_str"), currServerkey, request.serverInfos.get(currServerkey, ""), request.GET.get("groupInterval", ""))

		return self.noticeTimingQuery(request, html_template)

g_noticeInstance = NoticeManager.instance()