# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *

import LogTables
from LogProcesser import LogProcesserManager, LogAccountLogin, EnterDistLog, EnterSceneLog, OnlineLog, LevelLog, CreditLog, CostLog, PlayLog
from LogProcesser import g_logProcesser
from GMToolsLogInterfaces import Acceptor

LogTables.init()

acceptorInstance = Acceptor()
acceptorInstance.start()

# 日志处理器初始化
#LogAccountLogin( g_logProcesser )
#EnterDistLog( g_logProcesser )
#EnterSceneLog( g_logProcesser )
#OnlineLog( g_logProcesser )
#LevelLog( g_logProcesser )
#CreditLog( g_logProcesser )
#CostLog( g_logProcesser )
#PlayLog( g_logProcesser )

"""
logger进程主要处理KBEngine服务端的日志保存工作。
"""


def onLoggerAppReady():
	"""
	KBEngine method.
	logger已经准备好了
	"""
	INFO_MSG('onLoggerAppReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
	 (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

def onLoggerAppShutDown():
	"""
	KBEngine method.
	这个logger被关闭前的回调函数
	"""
	INFO_MSG('onLoggerAppShutDown()')

def onReadyForShutDown():
	"""
	KBEngine method.
	logger询问脚本层：我要shutdown了，你（脚本）是否准备好了？
	如果返回True，则logger会进入shutdown的流程，其它值会使得logger在过一段时间后再次询问。
	用户可以在收到消息时进行脚本层的数据清理工作，以让脚本层的工作成果不会因为shutdown而丢失。
	"""
	INFO_MSG('onReadyForShutDown()')
	return g_logProcesser.mtIsReadyForShutDown()

def onLogWrote(logData):
	"""
	KBEngine method.
	logger写入了一条日志后的回调，
	有需要的用户可以在此处把日志写入到其它的地方（如数据库）
	@param logData: bytes
	"""
	#INFO_MSG('onLogWrote() logData = "%s"' % logData)
	g_logProcesser.mtOnReceiveLog( logData )

