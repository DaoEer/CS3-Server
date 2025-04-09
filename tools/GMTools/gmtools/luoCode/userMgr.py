# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from . import login
from ..models import GMUser
from common import csstatus
from common import csdefine
from common import tooldefine
#from common import toollogdefine
from . import GMActionLog
logInstance = GMActionLog.g_logInstance


import hashlib

loginInstannce = login.g_loginInstance

srvConf = tooldefine.tool_default_db_key
srvDB = tooldefine.tool_default_db_key

class UserManager:
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
		if UserManager._instance == None:
			UserManager._instance = UserManager()
		return UserManager._instance
	
	def encryption(self, password ):
		"""
		加密
		"""
		m = hashlib.md5( password.encode("utf-8") )
		return m.hexdigest()

	def user_manage_name_check(self, name):
		"""
		检查新建用户是否已存在
		"""
		for obj in GMUser.objects.using(srvConf):
			if obj.name == name:
				return False
		return True
		
	def user_manage_super_admin_check(self):
		"""
		检查超级管理用户是否已存在
		"""
		num = 0
		for obj in GMUser.objects.using(srvConf):
			if obj.super_admin == 1:
				num += 1
		if num >= tooldefine.SUPER_ADMIN_NUM:
			return False
		return True

	@loginInstannce.login_check
	def user_manage(self, request):
		"""
		功能界面
		"""
		html_template = "gmtools/user_manage.html"
		qs = GMUser.objects.using( srvDB ).all()
		context = {
			"qs": qs,
		}
		return render( request, html_template, context )

	@loginInstannce.login_check
	def user_manage_new(self, request):
		"""
		新建账号
		"""
		datas = {"userInfo": {}}
		datas["userInfo"].update({"userID": "", "userName": ""})
		datas["userInfo"].update({"level": tooldefine.USER_LEVEL_THREE})
		
		html_template = "gmtools/user_manage_new.html"
		context = {"error": "", "success": ""}
		context.update(datas)
		return render( request, html_template, context )

	@loginInstannce.login_check
	def user_manage_new_create(self, request):
		"""
		新建账号
		"""
		html_template = "gmtools/user_manage_new.html"
		
		datas = {"userInfo": {}}
		context = {"error": "", "success": ""}
		context.update(datas)
		
		POST = request.POST
		userID = POST.get("userID", "").strip() 			#用户账号
		userName = POST.get("userName", "").strip()	#用户名
		password = POST.get("password", "").strip()			#密码
		passwordAgain = POST.get("passwordAgain", "").strip()	#确认密码
		level = int(POST.get("userLevelRadio", 0))
		
		datas["userInfo"].update({"userID": userID, "userName": userName})
		datas["userInfo"].update({"level": level})
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_USER_MGR][tooldefine.USER_MGR_ADD]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		
		context.update(datas)
		
		if not userID or not userName:
			context["error"] = csstatus.USER_NAME_ERROR
			return render( request, html_template, context )
		if not password or not passwordAgain:
			context["error"] = csstatus.USER_CREATE_PWD_ERROR
			return render( request, html_template, context )
		if password != passwordAgain:
			context["error"] = csstatus.USER_TWO_PWD_DIFFER
			return render( request, html_template, context )
		if level > tooldefine.USER_LEVEL_THREE or level < tooldefine.USER_LEVEL_ONE:
			context["error"] = csstatus.USER_CHANGE_LEVEl_ERROR
			return render( request, html_template, context )
		
		if GMUser.objects.using(srvConf).filter(userID = userID).exists():
			context["error"] = csstatus.USER_ID_IS_EXISTS % userID
			return render( request, html_template, context )
			
		pwd = self.encryption(password)
		r = GMUser.objects.using(srvConf).create(
				userID = userID,
				userName = userName,
				password = pwd,
				level = level,
			)
		
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.addUserLog(request.session["gm_userid"], request.session["gm_level"], userID, level, currServerkey, request.serverInfos.get(currServerkey, ""))
			
		context["success"] = csstatus.USER_CREATE_SUCCEED
		return render( request, html_template, context )

	@loginInstannce.login_check
	def user_manage_edit(self, request, dbid):
		"""
		账号编辑
		"""
		html_template = "gmtools/user_manage_edit.html"
		POST = request.POST
		send_flag = POST.get("send_flag", "")
		context = {"error": "", "success": ""}
		context.update({"level": 0})
		
		if request.session["gm_level"] > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_USER_MGR][tooldefine.USER_MGR_EDIT] :
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		try:
			user = GMUser.objects.using( srvDB ).get(id=dbid)
		except:
			context["error"] = csstatus.USER_EDIT_USER_INVALID
			return render( request, html_template, context )
		
		"""
		if request.session["super_admin"] != 1 and user.auth == 1: #普通管理员不能编辑其他管理员
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		"""
		
		if not send_flag:	
			context.update({
				"id": dbid,
				"userID": user.userID,
				"userName":user.userName,
				"level":user.level,
			})
			return render( request, html_template, context )

		id = POST.get("id")
		userID = POST.get("userID", "").strip()
		userName = POST.get("userName", "").strip()
		level = int(POST.get("levelRadio", 0))
		
		if not userID or not userName:
			context["error"] = csstatus.USER_NAME_ERROR
			return render( request, html_template, context )
			
		if level < tooldefine.USER_LEVEL_ONE or level > tooldefine.USER_LEVEL_THREE:
			context["error"] = csstatus.USER_CHANGE_LEVEl_ERROR
			return render( request, html_template, context )
			
		user = GMUser.objects.using( srvDB ).get(id=dbid)
		oldLevel = user.level
		GMUser.objects.using( srvDB ).filter(id=dbid).update(
			level = level
			)
			
		user = GMUser.objects.using( srvDB ).get(id=dbid)
		context.update({
			"id": dbid,
			"userID": user.userID,
			"userName":user.userName,
			"level":user.level,
		})
		
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.changeUserLevelLog(request.session["gm_userid"], request.session["gm_level"], user.userID, user.level, oldLevel, currServerkey, request.serverInfos.get(currServerkey, ""))
		
		context["success"] = csstatus.USER_EDIT_SUCCEED % userName
		return render( request, html_template, context )

	@loginInstannce.login_check
	def user_manage_delete(self, request, dbid):
		"""
		用户删除
		"""
		html_template = "gmtools/user_manage.html"
		
		qs = GMUser.objects.using( srvDB ).all()
		context = {"qs": qs,"error": "", "success": ""}
		
		if request.session.get("level", 0) > tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_USER_MGR][tooldefine.USER_MGR_DEL]:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		try:
			userObj = GMUser.objects.using( srvDB ).get(id = dbid )
		except ObjectDoesNotExist:
			context["error"] = csstatus.USER_MANAGE_ID_NOT_EXIST % dbid
			return render( request, html_template, context )
		
		"""
		if request.session["super_admin"] != 1 and userObj.auth == 1: #普通管理员不能删除其他管理员
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )
		"""
		
		currServerkey = request.session[tooldefine.CURR_SERVER]
		logInstance.delUserLog(request.session["gm_userid"], request.session["gm_level"], userObj.userID, userObj.level, currServerkey, request.serverInfos.get(currServerkey, ""))
		
		userObj.delete()
		context["success"] = csstatus.USER_DELETE_SUCCEED % request.session.get("gm_username", "")
		return render( request, html_template, context )

	@loginInstannce.login_check
	def user_manage_password(self, request, dbid):
		"""
		修改密码
		"""
		dbid = int(dbid)
		html_template = "gmtools/user_manage_password.html"
		POST = request.POST
		context = {"userid": dbid, "error": "", "success": ""}
		
		try:
			userObj = GMUser.objects.using( srvDB ).get( id = dbid )
		except ObjectDoesNotExist:
			context["error"] = csstatus.USER_MANAGE_ID_NOT_EXIST
			return render( request, html_template, context )
		
		if request.session.get( "gm_level", "" ) <= tooldefine.GM_USER_ACTION_GRADE_LEVEL_DICT[tooldefine.GM_TOOL_FUNCTION_TYPE_USER_MGR][tooldefine.USER_MGR_MODIFY_PWD] \
			or request.session.get("gm_id") == userObj.id:
			context["name"] = userObj.userName
			if not POST.get( "send_flag", None ):
				return render( request, html_template, context )
				
			"""
			if request.session["gm_id"] != dbid and request.session["super_admin"] != 1 and userObj.auth == 1: #普通管理员不能修改其他管理员密码
				context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
				return render( request, html_template, context )
			"""
			
			old_password = POST.get("password", "")
			new_password = POST.get("new_password", "")
			password_again = POST.get("password_again", "")
			
			if request.session["gm_id"] == dbid:
				pwd = self.encryption( old_password )
				if pwd != userObj.password:
					context["error"] = csstatus.USER_PASSWORD_OLD_PWD_ERROR
					return render( request, html_template, context )
			if new_password != password_again:
				context["error"] = csstatus.USER_TWO_PWD_DIFFER
				return render( request, html_template, context )
			new_pwd = self.encryption( new_password )
			GMUser.objects.using( srvDB ).filter(id = dbid ).update(
				password = new_pwd,
			)
			
			currServerkey = request.session[tooldefine.CURR_SERVER]
			logInstance.delUserLog(request.session["gm_userid"], request.session["gm_level"], userObj.userID, userObj.level, currServerkey, request.serverInfos.get(currServerkey, ""))
			
			context["success"] = csstatus.USER_PASSWORD_MODIFY_SUCCEED
			return render( request, html_template, context )
		else:
			context["error"] = csstatus.USER_GRADE_NOT_ENOUGH
			return render( request, html_template, context )

g_userInstance = UserManager.instance()