# -*- coding: utf-8 -*-

from BotTasks.BehaviorBase import TargetBase

#kill monster
class Target1( TargetBase.TargetBase ):
	def __init__( self, config ):
		TargetBase.TargetBase.__init__( self, config )
		self.killMonsterScriptIDs = []
		self.killMonsterNumber = 0
		self.killMonsterScriptIDs = config[ "Param1" ].split( "|" )
		self.killMonsterNumber = int( config[ "Param2" ] )

	def checkIsCompleted( self, roleEntity ):
		return roleEntity.getKillMonstersCounter( self.killMonsterScriptIDs ) >= self.killMonsterNumber

TargetBase.TargetBase.setClass( "Target1", Target1 )