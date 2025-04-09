# -*- coding: utf-8 -*-
#
import KBEngine
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface
import NPC


class NPCGinsengFruit(NPC.NPC,NPCAmbulantInterface.NPCAmbulantInterface ):
	"""
	人参果NPC 详情请见JIRA ： CST-2150
	"""
	def __init__(self):
		NPC.NPC.__init__( self )
		NPCAmbulantInterface.NPCAmbulantInterface.__init__(self)

	def startMove( self, dstPos ):
		"""
		开始移动
		"""
		self.moveToPosition( dstPos, True, True, 0.1 )

	def onCollisionBegin( self, exposedID ):
		"""
		碰撞开始
		"""
		self.destroySelf()
		

