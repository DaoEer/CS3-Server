# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# 服务器热加载模块相关接口
#-----------------------------------------------------------------------------------
import KBEngine
from HotUpdate import ReLoader
from KBEDebug import *


#-----------------------------------------------------------------------------------
# python 类热更新
#-----------------------------------------------------------------------------------
# reloadByInst( KST.g_configLoader, "ConfigLoader" )
def reloadByInst( instance, instName = "" ) :
	"""
	@param instance	:		需要热更新的实例
	@param instance :		instance(如：KST.g_configLoader)
	@param instName :		返回实例的类名
	@param instName :		string
	return instance
	"""
	return ReLoader._reloader( instance, instName )

# reloadByPath( "ConfigObject.ConfigLoader", "ConfigLoader" )
def reloadByPath( modulePath, instName = "" ):
	"""
	@param module	:		需要热更新的模块路径
	@param module :			string(如："ConfigObject.ConfigLoader")
	@param instName :		返回实例的类名
	@param instName :		string
	return instance
	"""
	return ReLoader._reloadByPath( modulePath, instName )

# import ConfigObject.ConfigLoader
# reloadByModule( ConfigObject.ConfigLoader, "ConfigLoader" )
def reloadByModule( module, instName = "" ):
	"""
	@param module	:		需要热更新的模块
	@param module :			module
	@param instName :		返回实例的类名
	@param instName :		string
	return instance
	"""
	return ReLoader._reloadByModule( module, instName )
	
#-----------------------------------------------------------------------------------
# entity 类热更新
#-----------------------------------------------------------------------------------
def reloadEntity():
	KBEngine.reloadScript()