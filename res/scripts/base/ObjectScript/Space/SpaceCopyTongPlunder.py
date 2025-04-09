# -*- coding: utf-8 -*-

import Math
import Functions
import KBEMath
import KBEDebug
import csdefine

from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyTongPlunder( SpaceCopy ):
	"""
	CST-11602 帮会掠夺
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

		self.enterPos = {} #{belongSide: [pos, dir]}
		self._leaveTongSpaceScriptID = ""
		self._leaveTongSpacePos = Math.Vector3(0.0, 0.0, 0.0)
		self._leaveTongSpaceDir = Math.Vector3(0.0, 0.0, 0.0)

	def initData(self, configData):
		SpaceCopy.initData(self, configData)

		attackEnterPosStr = configData["SpaceData"].get( "attackEnterPos", "")
		protectEnterPosStr = configData["SpaceData"].get( "protectEnterPos", "")
		if attackEnterPosStr:
			self.enterPos[csdefine.BELONG_SIDE_ATTACK] = []
			posStr, dirStr = attackEnterPosStr.split("|")
			self.enterPos[csdefine.BELONG_SIDE_ATTACK].append(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr)))
			self.enterPos[csdefine.BELONG_SIDE_ATTACK].append(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr)))
		if protectEnterPosStr:
			self.enterPos[csdefine.BELONG_SIDE_PROTECT] = []
			posStr, dirStr = protectEnterPosStr.split("|")
			self.enterPos[csdefine.BELONG_SIDE_PROTECT].append(KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(posStr)))
			self.enterPos[csdefine.BELONG_SIDE_PROTECT].append(KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(dirStr)))

		if "leaveTongSpaceData" in configData["SpaceData"]:
			self._leaveTongSpaceScriptID = configData["SpaceData"]["leaveTongSpaceData"].get("ScriptID", "")
			posStr = configData["SpaceData"]["leaveTongSpaceData"].get("Position", "")
			pos = Functions.vector3TypeConvert(posStr)
			if pos:
				self._leaveTongSpacePos = KBEMath.Unreal2KBEnginePosition(pos)
			dirStr = configData["SpaceData"]["leaveTongSpaceData"].get("Direction", "")
			dir = Functions.vector3TypeConvert(dirStr)
			if dir:
				self._leaveTongSpaceDir = KBEMath.Unreal2KBEngineDirection(dir)

	def getEnterPos(self, belongSide):
		return self.enterPos.get(belongSide, [])
	
	def getLeaveTongSpaceInfo(self):
		return (self._leaveTongSpaceScriptID, self._leaveTongSpacePos, self._leaveTongSpaceDir)
