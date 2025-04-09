# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.conf import settings

from CS3App.models import GameSeccion
from api.models import ChargeOrders

from Common import Utils
from Common.Define import CHARGERESULTCODE, CHARGERESULTINFO
from .baseConnector import g_baseappConnector

import time

import logging
logger = logging.getLogger("default")


def charge(request):
	"""
	充值
	"""
	datas = request.GET
	try:
		requestIP = ""
		if request.META.get("HTTP_X_FORWARDED_FOR"):
			requestIP = request.META.get("HTTP_X_FORWARDED_FOR")
		elif request.META.get("REMOTE_ADDR"):
			requestIP = request.META.get("REMOTE_ADDR")
			
		if requestIP not in settings.CHARGE_SERVER_REQUEST_HOSTS:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_GRADE_NOT_ENOUGH}
			return Utils.HttpResponseJson(result)
			
		account = datas.get("account", "")
		amount = int(datas.get("amount", "0"))
		goodtype = datas.get("goodtype", "")
		orderid = datas.get("orderid", "")
		timestamp = int(datas.get("timestamp", "0"))
		sign = datas.get("sign", "")
		signtype = datas.get("signtype", "")

		if not account or not amount or not goodtype or not orderid or not timestamp or not sign or not signtype:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_INFO_INCOMPLETE, "description": CHARGERESULTINFO.RESULT_INFO_INFO_INCOMPLETE}
			return Utils.HttpResponseJson(result)

		#如果amount小于0
		if amount <= 0:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_INFO_INCOMPLETE, "description": CHARGERESULTINFO.RESULT_INFO_AMOUNT_VALUE_ERROR}
			return Utils.HttpResponseJson(result)

		#账号不存在
		if not GameSeccion.query_account(account):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_ACCOUNT_NOT_EXIST, "description": CHARGERESULTINFO.RESULT_INFO_ACCOUNT_NOT_EXIST}
			return Utils.HttpResponseJson(result)

		#订单号已存在，默认已经执行成功
		if ChargeOrders.query_orderid(orderid):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_ORDER_IS_EXECUTED, "description": CHARGERESULTINFO.RESULT_INFO_ORDER_ALREADY_EXIST}
			return Utils.HttpResponseJson(result)

		#有效时间
		if abs(time.time() - timestamp) > settings.CHARGE_VALID_TIME:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_VALID_TIME_OVER}
			return Utils.HttpResponseJson(result)

		#签名
		if signtype != settings.CHARGE_SIGN_TYPE:
			logger.error("charge signtype error: %s: %s" % (signtype, settings.CHARGE_SIGN_TYPE))
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SIGN_ERROR, "description": CHARGERESULTINFO.RESULT_INFO_SIGN_TYPE_ERROR}
			return Utils.HttpResponseJson(result)
		signInfo = (("account", account), ("amount", amount), ("goodtype", goodtype), ("orderid", orderid), ("timestamp", timestamp))
		if sign != Utils.charge_sign("/api/charge?", *signInfo):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SIGN_ERROR, "description": CHARGERESULTINFO.RESULT_INFO_SIGN_ERROR}
			return Utils.HttpResponseJson(result)

		#执行充值操作
		if not ChargeOrders.charge(orderid, account, goodtype, amount):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_FAILD}
			return Utils.HttpResponseJson(result)

		#充值完后在查询一遍
		if not ChargeOrders.query_orderid(orderid):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_FAILD}
			return Utils.HttpResponseJson(result)

		g_baseappConnector.init(settings.CHARGE_SERVER_GM_HOSTS, settings.CHARGE_SERVER_GM_PORT)
		message = {"cmd": "chargeOrder", "info": {"accountName": "%s" % account}}
		if not g_baseappConnector.send_msg(message):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SUCCESS, "description": CHARGERESULTINFO.RESULT_INFO_NOTICE_SERVER_ERROR}
			return Utils.HttpResponseJson(result)
		g_baseappConnector.close()

		result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SUCCESS, "description": CHARGERESULTINFO.RESULT_INFO_SUCCESS}
		return Utils.HttpResponseJson(result)

	except Exception as err:
		logger.error("charge error: %s" % err)
		result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": err}
		return Utils.HttpResponseJson(result)
		

def queryOrder(request):
	"""
	查询订单号
	"""
	datas = request.GET
	try:
		requestIP = ""
		if request.META.get("HTTP_X_FORWARDED_FOR"):
			requestIP = request.META.get("HTTP_X_FORWARDED_FOR")
		elif request.META.get("REMOTE_ADDR"):
			requestIP = request.META.get("REMOTE_ADDR")			
		if requestIP not in settings.CHARGE_SERVER_REQUEST_HOSTS:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_GRADE_NOT_ENOUGH}
			return Utils.HttpResponseJson(result)
		
		orderid = datas.get("orderid", "")
		timestamp = int(datas.get("timestamp", "0"))
		sign = datas.get("sign", "")
		signtype = datas.get("signtype", "")
		
		if  not orderid or not timestamp or not sign or not signtype:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_INFO_INCOMPLETE, "description": CHARGERESULTINFO.RESULT_INFO_INFO_INCOMPLETE}
			return Utils.HttpResponseJson(result)

		#有效时间
		if abs(time.time() - timestamp) > settings.CHARGE_VALID_TIME:
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": CHARGERESULTINFO.RESULT_INFO_VALID_TIME_OVER}
			return Utils.HttpResponseJson(result)

		#签名
		if signtype != settings.CHARGE_SIGN_TYPE:
			logger.error("queryOrder signtype error: %s: %s" % (signtype, settings.CHARGE_SIGN_TYPE))
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SIGN_ERROR, "description": CHARGERESULTINFO.RESULT_INFO_SIGN_TYPE_ERROR}
			return Utils.HttpResponseJson(result)
		signInfo = (("orderid", orderid), ("timestamp", timestamp))
		if sign != Utils.charge_sign("/api/query/order?", *signInfo):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_SIGN_ERROR, "description": CHARGERESULTINFO.RESULT_INFO_SIGN_ERROR}
			return Utils.HttpResponseJson(result)
			logger.error("queryOrder signtype error: %s: %s" % (signtype, settings.CHARGE_SIGN_TYPE))

		if not ChargeOrders.query_orderid(orderid):
			result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_ORDER_NOT_EXIST, "description": CHARGERESULTINFO.RESULT_INFO_ORDER_NOT_EXIST}
			return Utils.HttpResponseJson(result)

		result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_ORDER_IS_EXECUTED, "description": CHARGERESULTINFO.RESULT_INFO_ORDER_IS_EXECUTED}
		return Utils.HttpResponseJson(result)		

	except Exception as err:
		logger.error("queryOrder error: %s" % err)
		result = {"errorcode": CHARGERESULTCODE.RESULT_TYPE_FAILD, "description": err}
		return Utils.HttpResponseJson(result)