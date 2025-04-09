# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time
import KBEMath
import Functions

class SpaceCopyTrainingGroundSave( SpaceCopy ):
	"""
	练兵场 布防
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.hasSaveNPC = {}					# 已经保存的scriptID
		self.isInitNPC = False					# 是否已经初始化了保存的数据
#		self.belongDBID = 0						# 归宿玩家DBID
		
	def onRequestSpaceNPCInfo( self, spaceData ):
		"""
		<define method>
		请求保存的数据回调
		"""
		self.isInitNPC = True
		for data in spaceData:
			if not data["scriptID"] in self.hasSaveNPC:
				self.hasSaveNPC[data["scriptID"]] = 0
			self.hasSaveNPC[data["scriptID"]] += 1
			self.createEntityByScriptID( data["scriptID"], data["position"], data["direction"], data["createArgs"])
		self.getScript().onRequestSpaceNPCInfo( self, spaceData )
	

