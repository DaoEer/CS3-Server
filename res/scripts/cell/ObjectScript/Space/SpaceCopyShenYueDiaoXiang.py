# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import copy
import Functions
import KBEMath


class SpaceCopyShenYueDiaoXiang( SpaceCopyRingTaskChild):
	"""
	神乐雕像
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		self.shentanPos = []															#神坛刷灵球的坐标
		shentanPos = configData["SpaceData"].get( "shentanPos", [] )
		for info in shentanPos:
			position = Functions.vector3TypeConvert(info["pos"])
			if position:
				info["pos"] = KBEMath.Unreal2KBEnginePosition( position )
				self.shentanPos.append(info)
		self.lingqiuNum = configData["SpaceData"].get( "lingqiuNum", 15 )				#灵球的数量，默认为15个
		self.lingqiuScriptID = configData["SpaceData"].get("lingqiuScriptID", "")
		self.submitInfoDict = configData["SpaceData"].get("submitInfoDict", {})
		self.statueNum = configData["SpaceData"].get("statueNum", len(self.submitInfoDict.keys()))


	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyRingTaskChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( copy.deepcopy(self.shentanPos), self.lingqiuNum, self.lingqiuScriptID, copy.deepcopy(self.submitInfoDict), self.statueNum )
