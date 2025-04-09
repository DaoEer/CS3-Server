# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyStory import SpaceCopyStory
import Math
import KBEMath
import Functions
import csdefine
import KBEDebug

class SpaceCopyStoryExit( SpaceCopyStory ):
	"""
	剧情副本-返回点需要根据职业判断返回点
	"""
	def __init__( self ):
		SpaceCopyStory.__init__( self )
		self.scriptIDList = []	# 战士|剑客|射手|法师
		self.posList = []
		self.dirList = []
	
	def initData( self, configData ):
		SpaceCopyStory.initData( self, configData )
		if "SpaceCopyStoryExit" in configData:
			scriptIDList = configData["SpaceCopyStoryExit"].get("ScriptID", "")
			if scriptIDList:
				_scriptIDList = scriptIDList.split("|")
				if len( _scriptIDList ) == 4:
					self.scriptIDList = [_scriptIDList, _scriptIDList]
				elif len(_scriptIDList) == 8:
					self.scriptIDList = [_scriptIDList[0:4], _scriptIDList[4:8]]
				else:
					KBEDebug.ERROR_MSG(" space%s in SpaceCopyStoryExit ScriptID(len = %i) is error "%( self.scriptID, len(scriptIDList) ))

			posStrList = configData["SpaceCopyStoryExit"].get("Position", "")
			if posStrList:
				_posStrList = posStrList.split("|")
				if len( _posStrList ) == 4:
					posLst = [KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( pos ) ) for pos in _posStrList]
					self.posList = [posLst, posLst]
				elif len( _posStrList ) == 8:
					posLst = [KBEMath.Unreal2KBEnginePosition( Functions.vector3TypeConvert( pos ) ) for pos in _posStrList]
					self.posList = [posLst[0:4], posLst[4:8]]
				else:
					KBEDebug.ERROR_MSG(" space%s in SpaceCopyStoryExit Position(len = %i) is error "%( self.scriptID, len(_posStrList) ))

			dirStrList = configData["SpaceCopyStoryExit"].get("Direction", "")
			if dirStrList:
				_dirStrList = dirStrList.split("|")
				if len( _dirStrList ) == 4:
					dirLst = [KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dir )) for dir in _dirStrList]
					self.dirList = [dirLst, dirLst]
				elif len( _dirStrList ) == 8:
					dirLst = [KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dir )) for dir in _dirStrList]
					self.dirList = [dirLst[0:4], dirLst[4:8]]
				else:
					KBEDebug.ERROR_MSG(" space%s in SpaceCopyStoryExit Direction(len = %i) is error "%( self.scriptID, len(_dirStrList) ))

	def getReviveToExitInfo( self, playerRole ):
		camp = playerRole.getCamp()
		profession = playerRole.getProfession()
		return ( self.scriptIDList[camp - 1][profession - 1], self.posList[camp - 1][profession - 1], self.dirList[camp - 1][profession - 1] )