# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import KBEMath
import Math
import math

class SpaceCopyClientEffect( SpaceCopy ):
	"""
	客户端效果demon
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.allFuDaiScriptIDList = []
		self.addTimerCallBack(2.0,"callBossMonster",())
	
	def callBossMonster( self ):
		"""
		刷Boss
		"""
		ue4Pos = (2400.0,5000.0,100.0)
		spawnPos = Math.Vector3(KBEMath.Unreal2KBEnginePosition( ue4Pos ))
		self.createEntityByScriptID("29900127",spawnPos,Math.Vector3(0,0,0),{"spawnPos":spawnPos})
		
		ue4Pos1 = (3200.0,7000.0,300.0)
		spawnPos1 = Math.Vector3(KBEMath.Unreal2KBEnginePosition( ue4Pos1 ))
		self.createEntityByScriptID("29900126",spawnPos1,Math.Vector3(0,0,-math.pi/4),{})
		#刷大摆锤
		spawnPos2 = Math.Vector3(KBEMath.Unreal2KBEnginePosition( (2730.0,13800.0,200.0) ))
		self.createEntityByScriptID("20007868",spawnPos2,Math.Vector3(0,0,math.pi/2),{})
		spawnPos3 = Math.Vector3(KBEMath.Unreal2KBEnginePosition( (2730.0,14800.0,200.0) ))
		self.createEntityByScriptID("20007868",spawnPos3,Math.Vector3(0,0,math.pi/2),{})
		spawnPos4 = Math.Vector3(KBEMath.Unreal2KBEnginePosition( (2730.0,15800.0,200.0) ))
		self.createEntityByScriptID("20007868",spawnPos4,Math.Vector3(0,0,math.pi/2),{})
		
	def setOriginCenterPos( self, originCenterPos ):
		"""
		设置起始中心点
		"""
		self.originCenterPos = originCenterPos

	def setOriginRadius( self, originRadius ):
		"""
		设置起始半径
		"""
		self.originRadius = originRadius

	def setEndCenterPos( self, endCenterPos ):
		"""
		设置终点圆心
		"""
		self.endCenterPos = endCenterPos

	def setEndRadius( self, endRadius ):
		"""
		设置终点半径
		"""
		self.endRadius = endRadius

	def getOriginCenterPos( self ):
		"""
		获得起始中心点
		"""
		return self.originCenterPos

	def getOriginRadius( self ):
		"""
		获得起始中心点
		"""
		return self.originRadius

	def getEndCenterPos( self ):
		"""
		获得终点圆心
		"""
		return self.endCenterPos

	def getEndRadius( self ):
		"""
		获得终点圆的半径
		"""
		return self.endRadius
		
	def StartReduceYeZhanFengQiArea( self, totalUseTime ):
		"""
		开始缩小安全区域
		"""
		pass
		
	