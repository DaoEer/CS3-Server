# -*- coding: utf-8 -*-

import KBEngine


"""
usage:
	非玩家控制对象script基类

attribute:
	objectType

member function:
	getObjectType
	getName

callback:
	pass

"""


#python
#engine
import KBEngine
#script
import ObjectScript.ObjectScriptBase.GameScript as GameScript


class NPCBaseScript( GameScript.GameScript ):
	"""
	非玩家控制对象script基类
	"""
	def __init__( self ):
		GameScript.GameScript.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param data: dict
		"""
		GameScript.GameScript.initData( self, configData )
	
	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		pass


