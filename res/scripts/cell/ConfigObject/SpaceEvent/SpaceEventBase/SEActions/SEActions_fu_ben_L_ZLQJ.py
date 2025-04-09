# -*- coding: utf-8 -*-

# 副本事件行为
import random
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction35( SEActionBase ):
	"""
	真龙棋局：副本初始化随机刷出param1~param2颗棋子,其中不能出现连续5个同样的相邻且相连的棋子。
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self.param1 = int( section["param1"] )
		self.param2 = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		number = random.randint( self.param1, self.param2 )
		if spaceEntity:
			spaceEntity.initGobang( number )

class SEAction36( SEActionBase ):
	"""
	真龙棋局：销毁所有棋子
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.destroyAllPieces()

class SEAction37( SEActionBase ):
	"""
	真龙棋局：开启定时器并通知界面显示特殊血条
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.openChangeTimeID()

class SEAction38( SEActionBase ):
	"""
	真龙棋局：客户端清空相关数据
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if trigger:
			trigger.client.ZhenLongQiju_ClearData()

class SEAction39( SEActionBase ):
	"""
	真龙棋局：销毁至少5个连续的棋子,并重新刷新
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			for coord,entityID in spaceEntity.pointHasEntity.items():
				if entityID == triggerID:
					links = spaceEntity.checkGobangLink([coord])
					if len(links) > 0:
						spaceEntity.refreshGobangLink(links)

class SEAction40( SEActionBase ):
	"""
	真龙棋局：发送副本Boss的状态和血量到客户端
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get( triggerID )
		if spaceEntity and trigger:
			for player in spaceEntity._spaceRoles:
				player.client.ZhenLongQiJu_OnBossHPChange( eventParams["HP_Max"], eventParams["newValue"] )

class SEAction41( SEActionBase ):
	"""
	真龙棋局：清除副本状态切换定时器并关闭界面特殊血条
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.clearChangeTimeID()

SEActionBase.setActionClass("SEAction35", SEAction35)
SEActionBase.setActionClass("SEAction36", SEAction36)
SEActionBase.setActionClass("SEAction37", SEAction37)
SEActionBase.setActionClass("SEAction38", SEAction38)
SEActionBase.setActionClass("SEAction39", SEAction39)
SEActionBase.setActionClass("SEAction40", SEAction40)
SEActionBase.setActionClass("SEAction41", SEAction41)
