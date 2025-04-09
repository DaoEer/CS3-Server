# -*- coding: utf-8 -*-

import KBEngine
import KST
from KBEDebug import *
from CoreObject import MgrPersistentObject
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class CrondTestMgr( MgrPersistentObject.MgrPersistentObject ):
	
	def __init__( self ):

		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self.onCompleteInit()
		
	
	def register( self ):
		
		taskEvents = {"QuizGameMgr_notice": "onQuizGameMgr_notice",
				  "QuizGameMgr_start": "onQuizGameMgr_start"
		}
		
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName )

	def onQuizGameMgr_notice( self, cmd, *callbackArgs):
		
		INFO_MSG("========================================onQuizGameMgr_notice is callbacked")
		
	def onQuizGameMgr_start( self, cmd, *callbackArgs ):
		
		INFO_MSG("==========================================onQuizGameMgr_start is callbacked")

	def onQuizGameMgr_end( self, *callbackArgs):
		
		INFO_MSG("========================================onQuizGameMgr_end is callbacked")
		