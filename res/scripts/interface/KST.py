# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *

import KBEIOLoop
from LoginProcesser import g_loginProcesser

def onInterfaceAppReady():
	"""
	KBEngine method.
	interfaceApp已经准备好了
	"""
	INFO_MSG('onInterfaceAppReady: bootstrapGroupIndex=%s, , bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_GROUPID"), os.getenv("KBE_GLOBALID")))
	KBEIOLoop.instance().start()
	g_loginProcesser.start()

def onInterfaceAppShutDown():
	"""
	KBEngine method.
	这个interfaceApp被关闭前的回调函数
	"""
	INFO_MSG('onInterfaceAppShutDown')
	KBEIOLoop.instance().stop()

def onRequestCreateAccount( accountName, password, userDatas ):
	"""
	请求注册账号
	"""
	DEBUG_MSG( "commitName = '{}', password = '{}', userDatas = '{}'".format(accountName, password, userDatas) )
	# un-support
	KBEngine.createAccountResponse( accountName, accountName, b"", KBEngine.SERVER_ERR_OP_FAILED )

def onRequestAccountLogin( accountName, password, userDatas ):
	"""
	请求登录账号
	"""
	DEBUG_MSG( "commitName = '{}', password = '{}', userDatas = '{}'".format(accountName, password, userDatas) )
	#KBEngine.accountLoginResponse( accountName, accountName, b"", KBEngine.SERVER_SUCCESS )
	g_loginProcesser.onRequestAccountLogin(accountName, password, userDatas)

def onRequestCharge( ordersID, dbID, userDatas ):
	"""
	请求充值
	"""
	DEBUG_MSG( "ordersID = '{}', dbID = '{}', userDatas = '{}'".format(ordersID, dbID, userDatas) )
	# un-support
	KBEngine.chargeResponse( orderID, b"", KBEngine.SERVER_ERR_OP_FAILED )





