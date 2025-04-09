# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine


class SpaceCopyQiJueLing( SpaceCopy ):
	"""
	七绝岭
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.positionList = []		# 需进入七座山峰的位置

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		posList = configData["SpaceData"].get("positionList","").split("|")
		for pos in posList:
			pos = Functions.vector3TypeConvert(pos)
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self.positionList.append(pos)

	def getPositionList( self ):
		"""
		获得七座山峰位置
		"""
		return self.positionList