# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import Math
import KBEngine
import csdefine
import Functions
import KBEMath

class SpaceCopyMQRSG( SpaceCopyRingTask ):
	"""
	冥气人参果副本
	"""
	def __init__( self ) :
		SpaceCopyRingTask.__init__( self )
	
	def initSpaceData( self, cikuCoordList, cikuCoordList1, monsterScriptIDList ):
		"""
		初始化数据
		"""	
		self.cikuCoordList = cikuCoordList
		self.monsterScriptIDList = monsterScriptIDList
		for coord in cikuCoordList:
			posStr = Functions.vector3TypeConvert( coord )
			self.cikuCoordXList.append( int(posStr[0]) )
			self.cikuCoordYList.append( int(posStr[1]) )
			self.cikuCoordZList.append( int(posStr[2]) )

		for coord1 in cikuCoordList1:
			posStr1 = Functions.vector3TypeConvert( coord1 )
			self.cikuCoordXList1.append( int(posStr1[0]) )
			self.cikuCoordYList1.append( int(posStr1[1]) )
			self.cikuCoordZList1.append( int(posStr1[2]) )

	def creatHitRightCikuMonster( self, ciKuPos ):
		"""
		击中正确的人参果创建对应的怪物
		"""
		self.createEntityByScriptID( self.monsterScriptIDList[0], KBEMath.Unreal2KBEnginePosition(ciKuPos), Math.Vector3(0,0,0), {} )

	def creatHitErrorCikuMonster( self, ciKuPos ):
		"""
		击中错误的人参果创建对应的怪物
		"""
		self.createEntityByScriptID( self.monsterScriptIDList[1], KBEMath.Unreal2KBEnginePosition(ciKuPos), Math.Vector3(0,0,0), {} )