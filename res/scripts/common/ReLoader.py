# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# 功能说明：服务器热加载模块
# 文件作者：chendongyong
# 创建时间：2016-11-17
#-----------------------------------------------------------------------------------

import sys
from imp import reload


def _reloader( instance, instName = "" ) :
	"""
	@param instance	:		需要热更新的实例
	@param instance :		instance
	@param instName :		需要热更新实例的类名
	@param instName :		string
	"""
	modulePath = instance.__module__
	return _reloadByPath( modulePath, instName )
	
def _reloadByPath( modulePath, instName = "" ):
	"""
	@param modulePath	:	需要热更新的模块路径
	@param modulePath :		string
	@param instName :		需要热更新实例的类名
	@param instName :		string
	"""
	module = sys.modules[modulePath]
	return _reloadByModule( module, instName )
	
def _reloadByModule( module, instName = "" ):
	"""
	@param module	:		需要热更新的模块
	@param module :			module
	@param instName :		需要热更新实例的类名
	@param instName :		string
	"""
	new = reload( module )
	if instName:
		new = getattr( new, instName )()
	return new
	

