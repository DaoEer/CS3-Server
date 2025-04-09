import json

from django.shortcuts import render
from django.conf import settings
from CS3App.models import GameSeccion
from django.http import HttpResponse

from Common import Utils
from Common.Define import SUCCESS, FAIL, LOGINCODE

import logging
logger = logging.getLogger("default")

def test(request):
	"""
	"""
	return HttpResponse("This is Test")

def checklogin(request):
	"""
	"""
	if settings.CS_OPEN_ACCOUNT_VERIFY == False:
		return Utils.HttpResponseJson({ "result" : SUCCESS, "return_code" : LOGINCODE.CHECK_LOGIN_SUCCESS })
	try:
		datas = request.GET
		#logger.error(datas)
		
		accName = datas.get("AccountName", None)
		passwd = datas.get("PassWord", None)
		sign = datas.get("Sign", None)
		
		#参数错误
		if not accName or not passwd or not sign:
			return Utils.HttpResponseJson({ "result" : FAIL, "return_code" : LOGINCODE.CHECK_LOGIN_ARGS_ERROR })
		
		#签名错误
		csSign = Utils.CS_Sign(("AccountName", accName), ("PassWord", passwd))
		if csSign != sign:
			return Utils.HttpResponseJson({ "result" : FAIL, "return_code" : LOGINCODE.CHECK_LOGIN_SIGN_ERROR })
		
		#账号不存在
		acc = GameSeccion.query_account(accName)
		if not acc:			
			return Utils.HttpResponseJson({ "result" : FAIL, "return_code" : LOGINCODE.CHECK_LOGIN_ACCOUNT_NOT_EXISTS })
		
		#密码不对
		pwd = ""
		if isinstance(acc.password, bytearray):
			pwd = acc.password.decode("utf-8")
		else: 
			pwd = acc.password
		if pwd != passwd:		
			return Utils.HttpResponseJson({ "result" : FAIL, "return_code" : LOGINCODE.CHECK_LOGIN_PASSWD_ERROR })
	except:
		return Utils.HttpResponseJson({ "result" : FAIL, "return_code" : LOGINCODE.CHECK_LOGIN_UNKNOW_ERROR })
	
	return Utils.HttpResponseJson({ "result" : SUCCESS, "return_code" : LOGINCODE.CHECK_LOGIN_SUCCESS })