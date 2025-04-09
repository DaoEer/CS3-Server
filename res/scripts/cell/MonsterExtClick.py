# -*- coding: utf-8 -*-


"""
usage:
	怪物基类

attribute:
	modelNumber

member function:
	getModelNumber
	setModelNumber

callback:
	pass

"""


#python
#engine
import KBEngine
import KBEDebug
#script
import Monster
import time
import csarithmetic
import csdefine
import Const


class MonsterExtClick( Monster.Monster ):
	"""
	可点击怪物
	AI有左键双击事件响应
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def CELL_gossipWith(self, srcEntityID):
		"""
		<exposed method>
		客户端左键双击事件
		"""
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ON_LEFT_MOUSE_DOUBLE_CLICK, [], triggerEntity )


