# -*- coding: utf-8 -*-

#------------------
#怪物随机移动脚本
#------------------
import random
import KBEMath
import Functions
import KBEDebug
import ObjectScript.Monster.Monster as Monster

class MonsterRandomChoiceMove( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.posList = []

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		posStrList = configData["Param1"].split("|")
		for posStr in posStrList:
			pos = Functions.vector3TypeConvert( posStr )
			try:
				self.posList.append(KBEMath.Unreal2KBEnginePosition( pos ))
			except:
				KBEDebug.ERROR_MSG("ID : %s pos is error"%configData["scriptID"])

	def getRandomPosFromPosList(self, selfEntity ):
		"""
		从位置列表里随机选择一个坐标
		"""
		random.shuffle( self.posList )
		tempPos = ( 0.0, 0.0, 0.0 )
		for pos in self.posList:
			 if selfEntity.position.distTo( pos  ) > 6:
				 tempPos = pos
				 break
			 
		return tempPos

