# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
import csstatus
import KST

class RareMonsterMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	稀有怪物刷新 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.recordBossData = {}
		self.onCompleteInit()
		
	def onStartRefreshNotice( self, monsterName, spaceName, spaceScriptID ):
		"""
		世界公告
		"""
		msg = monsterName + "|" + spaceName
		KST.g_baseAppEntity.globalWold( csstatus.MONSTER_REFRESH_NOTICE, msg )
		if spaceScriptID not in self.recordBossData:
			self.recordBossData[spaceScriptID] = 1
		else:
			self.recordBossData[spaceScriptID] += 1

	def onSpaceInitOver( self, spaceMB ):
		"""
		Space初始化完成
		"""
		spaceMB.cell.onCreateWorldBoss()

	def onBossOnEnterDead( self, spaceMB, spaceScriptID ):
		"""
		Boss死亡
		"""
		if spaceScriptID in self.recordBossData:
			self.recordBossData[spaceScriptID] -= 1
		# 判断该地图所有Boss是不是都死了
		if self.recordBossData[spaceScriptID] <= 0:
			spaceMB.cell.onCountDpwnRefreshTime()
