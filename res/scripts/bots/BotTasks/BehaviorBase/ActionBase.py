# -*- coding: utf-8 -*-

import Functions
import KBEngine

class ActionBase( object ):
	_ACTION_CLASS = {}
	def __init__( self, config ):
		self.keyID="0"
		if "keyid" in config.keys():
			self.keyID= config[ "keyid" ]
		self.navigateData = config["navigateData"]
		self.targetPosition = {"SpaceID":"","Position":(0,0,0)}
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._ACTION_CLASS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, config ):
		scriptName = config[ "Script" ]
		return SELF._ACTION_CLASS[ scriptName ]( config )
	
	def doAction( self, roleEntity ):
		roleEntity.behOver()
		
	def checkIsCompleted( self, roleEntity ):
		roleEntity.outputMsg("%s is completed!"%self.__class__)
		return True
	
	def isArrived(self, roleEntity):
		"""
		检查机器人是否到达目标位置
		"""
		return( roleEntity.spaceScriptID== self.targetPosition["SpaceID"] and roleEntity.position.distTo( self.targetPosition["Position"] )<=5.0 )
		
	def arrive(self,roleEntity):
		#先到达目的地
		if self.navigateData and "#" in self.navigateData:
			naviData = self.navigateData.split("#")
			if "(" in naviData[0]:
				self.targetPosition["Position"],self.targetPosition["SpaceID"] = list(map(eval,naviData[0].replace("(","").replace(")","").split(" "))), naviData[1]
				monsterScriptIDs = []
			else:
				monsterScriptIDs, spaceScriptID = naviData[0].split( "|" ),naviData[1]
				self.targetPosition["SpaceID"], self.targetPosition["Position"] = roleEntity.findNPC( monsterScriptIDs, spaceScriptID )
		else:
			self.doAction( roleEntity )
				
		if self.targetPosition["SpaceID"] and self.targetPosition["Position"]:
			needTime = roleEntity.goto( self.targetPosition["SpaceID"], self.targetPosition["Position"] )
			KBEngine.callback( needTime, Functions.Functor( self.doAction, roleEntity ))
			roleEntity.onRoleSendChatMessage( "2", "quest:%s goto position: %s %s find: %s;"%(self.keyID,self.targetPosition["SpaceID"],self.targetPosition["Position"], monsterScriptIDs) , "" )

		