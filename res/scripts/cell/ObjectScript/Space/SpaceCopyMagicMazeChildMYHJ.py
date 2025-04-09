# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import random
import Math
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild

class SpaceCopyMagicMazeChildMYHJ( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 梦魇画卷
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		originPos = configData["SpaceData"].get( "originPos", "" )
		if originPos:
			originPos = originPos.split("|")
			self.originPos = tuple( [ float(i) for i in originPos ] )
		self.unitLength = float(configData["SpaceData"].get( "unitLength", 0.0) )
		if configData["SpaceData"].get("damageSkillID") != "":
			self.damageSkillID = int(configData["SpaceData"].get( "damageSkillID") )
		self.clubID = configData["SpaceData"].get( "clubID", "" )			# 梅
		self.orchidID = configData["SpaceData"].get( "orchidID", "" )		# 兰
		self.banbooID = configData["SpaceData"].get( "banbooID", "" )		# 竹
		self.chryID = configData["SpaceData"].get( "chryID", "" )			# 菊
		self.meiBossID = configData["SpaceData"].get( "meiBossID", "" )		# 梅·画卷
		self.lanBossID = configData["SpaceData"].get( "lanBossID", "" )		# 兰·画卷
		self.zhuBossID = configData["SpaceData"].get( "zhuBossID", "" )		# 竹·画卷
		self.juBossID = configData["SpaceData"].get( "juBossID", "" )		# 菊·画卷
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyMagicMazeChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.originPos, self.unitLength, self.damageSkillID, self.clubID, self.orchidID,\
			self.banbooID, self.chryID, self.meiBossID, self.lanBossID, self.zhuBossID, self.juBossID )
