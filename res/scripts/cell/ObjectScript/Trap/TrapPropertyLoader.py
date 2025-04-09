#coding:utf-8

import sys
import KBEDebug
import csdefine
from ObjectScript.ObjectScriptBase.EntityPropertyLoader import EntityPropertyLoader

class TrapPropertyLoader( EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.__init__( self )
		self.delayDeadTime = 0.0
		self.destroyTime = 0.0
		self.deadEffectID = ""
		self.delayStartTime = 0.0

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.initData( self, configData )
			if 'Uname' in configData:
				self.setEntityProperty( "uname", configData["Uname"])
 
#			if 'Title' in configData: 
#				self.setEntityProperty( "title", configData["Title"])

			if 'WalkSpeed' in configData:
				self.setEntityProperty( "moveSpeed", float(configData["WalkSpeed"]) )
 
#			if 'IsBoss' in configData:
#				self.setEntityProperty( "isBoss", configData["IsBoss"] )
#			 
#			if 'Faction' in configData:
#				self.setEntityProperty( "faction", configData["Faction"] )
#			 
#			if 'Camp' in configData: 
#				self.setEntityProperty( "camp", configData["Camp"] )
			
			if 'triggerShape' in configData:
				self.setEntityProperty( "triggerShape", configData["triggerShape"] )
			if 'triggerRadius' in configData:
				self.initTrapShape(configData)
				
			if 'delayDeadTime' in configData:
				self.delayDeadTime = float( configData["delayDeadTime"] )
			if 'deadEffectID' in configData:
				self.deadEffectID = configData["deadEffectID"] 
			if "destroyTime" in configData:
				self.destroyTime = float( configData["destroyTime"] )
				
			if 'patrolList' in configData:
				self.setEntityProperty( "patrolList", int(configData["patrolList"] ))
			if 'patrolPathNode' in configData:
				self.setEntityProperty( "patrolPathNode", int(configData["patrolPathNode"] ))
			if 'patrolMoveMode' in configData:
				self.setEntityProperty( "patrolMoveMode", int(configData["patrolMoveMode"]) )
			if 'accVelocity' in configData:
				self.setEntityProperty( "accVelocity", float(configData["accVelocity"]) )
			if 'InitActionId' in configData:
				self.setEntityProperty( "initActionId", configData["InitActionId"] )
			if 'triggerPosition' in configData:
				self.setEntityProperty( "triggerPosition", configData["triggerPosition"] )
			if 'delayStartTime' in configData:
				self.delayStartTime = float( configData["delayStartTime"] )
		else: 
			KBEDebug.WARNING_MSG("MonsterPropertyLoader::initData() configData is none!!!")
			
	def initTrapShape(self, configData):
		triggerShape = configData["triggerShape"]
		if triggerShape == csdefine.TRAP_SHAPE_RECTANGLE:	#方形
			radius = configData["triggerRadius"].split("|")
			radiusX = radiusY = radiusZ = 0.0
			if len( radius ) >= 3:
				radiusX = float( radius[0] )
				radiusY = float( radius[1] )
				radiusZ = float( radius[2] )
			elif len( radius ) == 1:
				radiusX = radiusY = radiusZ = float( radius[0] )
			self.setEntityProperty( "triggerDepth", radiusX )
			self.setEntityProperty( "triggerWidth", radiusY )
			self.setEntityProperty( "triggerHeight", radiusZ )
			
		elif triggerShape == csdefine.TRAP_SHAPE_CIRCULAR:	#球形
			self.setEntityProperty( "triggerRadius", float(configData["triggerRadius"]) )
			
		elif triggerShape == csdefine.TRAP_SHAPE_CYLINDER:	#圆柱形
			radius = configData["triggerRadius"].split("|")
			radiusXZ = radiusY = 0.0
			if len( radius ) >= 2:
				radiusXZ = float( radius[0] )
				radiusY = float( radius[1] )
			
			self.setEntityProperty( "triggerRadius", radiusXZ )
			self.setEntityProperty( "triggerHeight", radiusY )
		else:
			KBEDebug.ERROR_MSG("UNKNOWN TRAP(scriptID:%s) SHAPE %s" %(configData["scriptID"], triggerShape))
