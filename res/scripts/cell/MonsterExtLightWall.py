# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine

class MonsterExtLightWall( Monster.Monster ):
	"""
	光墙怪物类，CST-3248专用
	"""
	def __init__( self ):
		"""
		配置param1: length，光墙长度
		"""
		Monster.Monster.__init__( self )


