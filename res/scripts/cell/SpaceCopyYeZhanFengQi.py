# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine

class SpaceCopyYeZhanFengQi( SpaceCopy ):
	"""
	血斗凤栖镇
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def getDynamicReviverInfo( self, camp = csdefine.CMAP_NONE ):
		"""
		<Define method>
		获取副本动态复活点
		"""
		return self.getScript().getEnterInfo()

	def addYeZhanFengQiMemberData( self, roleMB, initIntegral ):
		"""
		增加血斗凤栖镇成员数据
		"""
		self.memberDatas.add(roleMB,initIntegral)

	def removeYeZhanFengQiMemberData( self, roleMB ):
		"""
		减少副本玩家数据
		"""
		self.memberDatas.remove( roleMB )

	def addPlayerIntegral( self, roleMB, integral ):
		"""
		增加积分
		"""
		self.memberDatas.addIntegral( roleMB.id, integral )

	def reducePlayerIntegral( self, roleMB, integral ):
		"""
		减少积分
		"""
		self.memberDatas.decIntegral( roleMB.id, integral )

#--------------设置安全区域起点坐标-------------------------------------
	def setUpLeftOriginPos( self, upLeftOriginPos ):
		"""
		"""
		self.upLeftOriginPos = upLeftOriginPos

	def setUpRightOriginPos( self, upRightOriginPos ):
		"""
		"""
		self.upRightOriginPos = upRightOriginPos

	def setDownLeftOriginPos( self, downLeftOriginPos ):
		"""
		"""
		self.downLeftOriginPos = downLeftOriginPos

	def setDownRightOriginPos( self, downRightOriginPos ):
		"""
		"""
		self.downRightOriginPos = downRightOriginPos

#---------------设置缩小安全区域终点坐标-----------------------------------------
	def setUpLeftEndPos( self, upLeftEndPos ):
		"""
		"""
		self.upLeftEndPos = upLeftEndPos

	def setUpRightEndPos( self, upRightEndPos ):
		"""
		"""
		self.upRightEndPos = upRightEndPos

	def setDownLeftEndPos( self, downLeftEndPos ):
		"""
		"""
		self.downLeftEndPos = downLeftEndPos

	def setDownRightEndPos( self, downRightEndPos ):
		"""
		"""
		self.downRightEndPos = downRightEndPos

#-----------------获得安全区域起点坐标---------------------------------------
	def getUpLeftOriginPos( self ):
		"""
		"""
		return self.upLeftOriginPos

	def getUpRightOriginPos( self ):
		"""
		"""
		return self.upRightOriginPos

	def getDownLeftOriginPos( self ):
		"""
		"""
		return self.downLeftOriginPos

	def getDownRightOriginPos( self ):
		"""
		"""
		return self.downRightOriginPos

#--------------------获得缩小安全区域终点坐标----------------------------------------
	def getUpLeftEndPos( self ):
		"""
		"""
		return self.upLeftEndPos

	def getUpRightEndPos( self ):
		"""
		"""
		return self.upRightEndPos

	def getDownLeftEndPos( self ):
		"""
		"""
		return self.downLeftEndPos

	def getDownRightEndPos( self ):
		"""
		"""
		return self.downRightEndPos


	def CLIENT_StartReduceArea( self, totalUseTime ):
		"""
		开始缩小安全区域
		"""
		tickTime = 1.0
		totalUseTime = totalUseTime / tickTime #缩小的总时间
		upLeftVector = self.upLeftEndPos - self.upLeftOriginPos
		upLeftVector.normalise() #单位向量
		
		uprightVector = self.upRightEndPos - self.upRightOriginPos
		uprightVector.normalise()

		downLeftVector = self.downLeftEndPos - self.downLeftOriginPos
		downLeftVector.normalise()

		downRightVector = self.downRightEndPos - self.downRightOriginPos
		downRightVector.normalise()

		upLeftLength = self.upLeftEndPos.flatDistTo( self.upLeftOriginPos ) #距离
		upLeftSpeed = upLeftLength / totalUseTime #速度

		upRightLength = self.upRightEndPos.flatDistTo( self.upRightOriginPos )
		upRightSpeed = upRightLength / totalUseTime

		downLeftLength = self.downLeftEndPos.flatDistTo( self.downLeftOriginPos )
		downLeftSpeed = downLeftLength / totalUseTime

		downRightLength = self.downRightEndPos.flatDistTo( self.downRightOriginPos )
		downRightSpeed = downRightLength / totalUseTime

		self.reduceAreaTimer = self.addTimerRepeat( tickTime, "onStartReduceArea",(upLeftVector,uprightVector,downLeftVector,downRightVector,upLeftSpeed,upRightSpeed,downLeftSpeed,downRightSpeed) )
		self.addTimerCallBack( totalUseTime, "removeAreaTimer",() )

	def onStartReduceArea( self,upLeftVector,uprightVector,downLeftVector,downRightVector,upLeftSpeed,upRightSpeed,downLeftSpeed,downRightSpeed ):
		"""
		"""
		self.upLeftOriginPos = self.upLeftOriginPos + upLeftVector * upLeftSpeed
		self.upRightOriginPos = self.upRightOriginPos + uprightVector * upRightSpeed
		self.downLeftOriginPos = self.downLeftOriginPos + downLeftVector * downLeftSpeed
		self.downRightOriginPos = self.downRightOriginPos + downRightVector * downRightSpeed

	def removeAreaTimer( self ):
		"""
		清除缩毒timer
		"""
		if self.reduceAreaTimer:
			self.popTimer( self.reduceAreaTimer )
			self.reduceAreaTimer = 0

	def checkPlayerIsInSaveArea( self, buffID ):
		"""
		"""
		self.addTimerRepeat(0.1, "onCheckPlayerIsInSaveArea",(buffID,) )

	def onCheckPlayerIsInSaveArea( self, buffID ):
		"""
		检查玩家是否在安全区域里 原理：判断这个点发送射线与几条边相交 奇数在安全区域里，否则不在
		"""
		XList = [ self.upLeftOriginPos.x, self.upRightOriginPos.x, self.downRightOriginPos.x,self.downLeftOriginPos.x ]
		ZList = [ self.upLeftOriginPos.z, self.upRightOriginPos.z,self.downRightOriginPos.z , self.downLeftOriginPos.z ]
		posList = [self.upLeftOriginPos, self.upRightOriginPos,self.downRightOriginPos,self.downLeftOriginPos ]
		lastIndex = len(posList) -1
		MaxX = max(XList)
		MaxZ = max(ZList)
		MinX = min(XList)
		MinZ = min(ZList)
		for player in self._spaceRoles:
			if player.position.x > MaxX or player.position.x < MinX or player.position.z > MaxZ or player.position.z < MinZ:
				if len(player.findBuffsByBuffID(buffID)) > 0:
					return
				player.addBuff(player,buffID)
				return
			isInSaveArea = False
			for pos in posList:
				beValue = ( posList[lastIndex].z - pos.z )
				if beValue == 0:
					value = 0
				else:
					value = (posList[lastIndex].x - pos.x) * ( player.position.z - pos.z ) / beValue
				boolY1 = pos.z > player.position.z
				boolY2 = posList[lastIndex].z > player.position.z
				if player.position.x < (pos.x + value) and (boolY1 != boolY2):
					isInSaveArea = not isInSaveArea
				lastIndex = posList.index(pos)
			if not isInSaveArea:
				if len(player.findBuffsByBuffID(buffID)) > 0:
					return
				player.addBuff(player,buffID)
			else:
				player.removeBuffByID(buffID)


