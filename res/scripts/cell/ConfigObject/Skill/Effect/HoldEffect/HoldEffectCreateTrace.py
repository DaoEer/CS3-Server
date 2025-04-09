# -*- coding: utf-8 -*-


"""
"""


#cell
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect
#common
import csdefine
import KBEDebug



class HoldEffectCreateTrace( HoldEffect ):
	"""
	生成移动轨迹（毒雾）
	"""
	def __init__( self ):
		HoldEffect.__init__( self )
		self.particleID = ""					# 轨迹光效
		self.drawDist = 70.0					# 距离玩家多远，绘制一个轨迹（播放光效,最近距离70,建议配置100或者以上，单位：cm）
		self.singleLifeTime = 10.0				# 单个轨迹光效存活（单位：秒）
		self.width = 0							# 碰撞盒宽度（单位：cm）
		self.hight = 0							# 碰撞盒高度（单位：cm）
		self.skillID = 0						# 技能ID
		
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		HoldEffect.init( self, dictDat, skill )
		self.particleID = dictDat["Param1"]
		self.drawDist = max( float( dictDat["Param2"] ), 70.0 )
		self.singleLifeTime = float( dictDat["Param3"] )
		strData = dictDat["Param4"].split("|")
		if len( strData ) >= 2:
			self.width = int( strData[0] )
			self.hight = int( strData[1] )
		self.skillID = int( dictDat["Param5"] )

	def onBegin( self, effectData, receiver ):
		"""
		效果开始
		"""
		HoldEffect.onBegin( self, effectData, receiver )
		receiver.allClients.OnCreateTrace( receiver.id, self.particleID, self.drawDist, self.singleLifeTime, self.width, self.hight, self.skillID )

	def onEnd( self, effectData, receiver ):
		"""
		效果结束
		"""
		receiver.allClients.OnFinishCreateTrace( receiver.id )
		HoldEffect.onEnd(self, effectData, receiver)

	def onClientActorCreate( self, effectData, receiver, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		HoldEffect.onClientActorCreate( self, effectData, receiver, srcEntityID )
		receiver.allClients.OnCreateTrace( receiver.id, self.particleID, self.drawDist, self.singleLifeTime, self.width, self.hight, self.skillID )

