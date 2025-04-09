# -*- coding: utf-8 -*-


"""
usage:
	怪物基类

attribute:
	modelNumber

member function:
	getModelNumber
	setModelNumber

callback:
	pass

"""


#python
#engine
import KBEngine
import KBEDebug
#script
import Monster
import time


class MonsterExtShowTopCountDown( Monster.Monster ):
	"""
	头顶显示倒计时怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.lifeTime = float(self.getScript().param1)
		self.createTime = time.time()
		if self.lifeTime > 0:
			self.addTimerCallBack(self.lifeTime,"destroySelf",() )
	
	def getRemainLifeTime( self ):
		"""
		获取剩余生命时长
		"""
		if self.lifeTime <= 0 :
			return -1
		return float( self.createTime + self.lifeTime - time.time() )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		if self.lifeTime > 0:
			self.allClients.CLIENT_ShowRemainLifeTime( self.getRemainLifeTime() )

