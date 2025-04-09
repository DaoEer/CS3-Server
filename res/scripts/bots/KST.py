# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import KST_Config

roles = {}
tempData = {}

CALLBACK_SPACE_TIME = 5 * 60
def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	@param isReload: 是否是被重写加载脚本后触发的
	@type isReload: bool
	"""
	DEBUG_MSG('onInit::isReload:%s' % isReload)
	KBEngine.callback(CALLBACK_SPACE_TIME, onCallBack)
	
def onStart():
	"""
	KBEngine method.
	在onInitialize调用之后， 准备开始游戏时引擎调用这个接口.
	"""
	#我去，这函数竟然不会调用
	pass
	
def onFinish():
	"""
	KBEngine method.
	客户端将要关闭时， 引擎调用这个接口
	可以在此做一些游戏资源清理工作
	"""
	pass

def startBehaviour( behaviourKey ): 
	"""
	所有机器人客户端执行行为
	"""
	pass

def startAction( key, param ):
	"""
	机器人执行指令
	"""
	global roles
	for role in roles.values():
		role[0].startAction(key, param)
		
def onCallBack():
	"""
	"""
	global roles
	global CALLBACK_SPACE_TIME

	dct = {}
	t = int(time.time())
	for role in roles.values():
		role[0].onTickCallBack(CALLBACK_SPACE_TIME)
		
		classname = role[0].ai.__class__.__name__
		if classname not in dct:
			dct[classname] = [0, 0]
		dct[classname][0] += 1
		
		#如果时间差在30分钟内，则认为机器人是正常的。
		if role[2] + 30 * 60 >= t:
			dct[classname][1] += 1
	
	for k, v in dct.items():
		msg = "BOTAI:{}#{}#{}#{}".format(k, v[0], v[1], len(roles))
		DEBUG_BOT_MSG(msg)
		
	KBEngine.callback(CALLBACK_SPACE_TIME, onCallBack)