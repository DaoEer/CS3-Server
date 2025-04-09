# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine



class SpaceCopyQiJueLing( SpaceCopy ):
	"""
	七绝岭
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )


	def startFirstStage( self ):
		"""
		初赛
		"""
		self.addTimerCallBack(15.0,"showCountDown",(15.0,))
		self.addTimerCallBack(5.0,"showCountDown",(5.0,))

	def showCountDown( self, time ):
		"""
		显示倒计时
		"""
		for player in self._spaceRoles:
			player.ShowCountDown( time )

	def enterFightProcess( self, stageType ):
		"""
		进入战斗阶段
		"""
		#self.getScript().enterFightProcess( self )
		self.addTimerCallBack(180,"releasePoison",(stageType,)) # 3分钟后释放毒物

	def releasePoison( self, stageType ):
		"""
		释放毒物
		"""
		self.spawnGroupEntity( (stageType - 1), "", 0 )  #根据比赛阶段刷某批次的怪
		self.getScript().releasePoison(self,stageType)

	def onPlatFightOver( self, platNumber ):
		"""
		一个平台的战斗结束
		"""
		self.getScript().onPlatFightOver(self,platNumber)
