import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction371( SEActionBase ):
	"""
	帮会日常任务 天之幻境--通知客户端开始掉落法宝
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if not self.scriptIDList:
			KBEDebug.ERROR_MSG("scriptIDList is None")
			return
		for player in spaceEntity._spaceRoles:
			if player and player.getClient():
				player.client.StartFallTZHJFabao( self.scriptIDList )

class SEAction372( SEActionBase ):
	"""
	帮会日常任务 天之幻境--通知客户端停止掉落法宝
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player and player.getClient():
				player.client.StopFallTZHJFabao()

SEActionBase.setActionClass("SEAction371", SEAction371)
SEActionBase.setActionClass("SEAction372", SEAction372)