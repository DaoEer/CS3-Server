# -*- coding: utf-8 -*-
import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import Math
import KBEngine
import random
import Functions
import KBEMath

class SpaceCopyFenHuoJinNiu( SpaceCopyRingTask ):
	"""
	环任务副本 焚火金牛
	"""
	def __init__( self ) :
		SpaceCopyRingTask.__init__( self )

	def initSpaceData( self, taurusScriptID, destPos, centerPos, runSpeed, speedLimit, accSpeed, buffID ):
		"""
		初始化数据
		"""
		self.taurusScriptID = taurusScriptID	# 金牛的ScriptID
		self.destPos = destPos				    # 三个灵池的位置坐标
		self.centerPos = centerPos				# 祭坛位置坐标
		self.runSpeed = runSpeed 				# 金牛行走速度
		self.speedLimit = speedLimit			# 金牛的速度上限
		self.accSpeed = accSpeed				# 金牛的加速度
		self.buffID = buffID

	def getRunSpeed( self ):
		"""
		获取速度
		"""
		return self.runSpeed

	def getMaxSpeed( self ):
		"""
		获取速度上限
		"""
		return self.speedLimit

	def getAccSpeed( self ):
		"""
		获取加速度
		"""
		return self.accSpeed

	def getBuffID( self ):
		"""
		获取buffID
		"""
		return int(self.buffID)

	def getCenterPos( self ):
		"""
		获取祭坛位置坐标
		"""
		centerPos = Functions.vector3TypeConvert( self.centerPos )
		return KBEMath.Unreal2KBEnginePosition( centerPos )

	def randomSelectChannel( self ):
		"""
		随机选择一条通道
		"""
		destPos = random.choice( self.destPos )
		destPosStr = Functions.vector3TypeConvert( destPos )
		idList = self.getEntityRecord( self.taurusScriptID )
		if not idList or len(idList) > 1:
			return
		entity = KBEngine.entities.get(idList[0], None)
		entity.moveStartFHJN( KBEMath.Unreal2KBEnginePosition( destPosStr ) )