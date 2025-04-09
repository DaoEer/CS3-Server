# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from SmartImport import smartImport
from ObjectScript.SpellBox import SpellScriptBase
import csstatus

class MultiAreaSpellBox( SpellScriptBase.SpellScriptBase ):
	def __init__( self ):
		SpellScriptBase.SpellScriptBase.__init__( self )
		self.gossipConditions = {}
		self.gossipResults = {}
		self.listenEvents = 0	#需要监听的影响自身交互状态的事件，这是采用int64类型是因为all_clients属性不支持列表
		self.holdAction = {}	#持有动作
		self.holdEffectID = {}	#持有光效
		self.effectID = {}		#可交互光效
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellScriptBase.SpellScriptBase.initData( self, data )
		if "Uname" in data:
			self.setEntityProperty( "uname", data["Uname"] )
		if "Area" in data:
			for index, conData in data["Area"].items():
				if "holdAction" in conData:
					self.holdAction[int(index)] = conData["holdAction"]
				if "holdEffectID" in conData:
					self.holdEffectID[int(index)] = conData["holdEffectID"]
				if "effectID" in conData:
					self.effectID[int(index)] = conData["effectID"]

				if "gossipCondition" in conData:
					gossipCondition = []
					for conDict in conData["gossipCondition"]:
						scriptName = conDict[ "scriptName" ]
						scriptObj = smartImport( "ConfigObject.SpellBoxGossip.SpellGossipCondition" + ":" + scriptName )()
						scriptObj.init( conDict )
						gossipCondition.append( scriptObj )
						if not self.hasListenEvent( scriptObj.eventType ):
							self.addListenEvent( scriptObj.eventType )
					self.gossipConditions[int(index)] = gossipCondition

				if "gossipResult" in conData:
					gossipResult = []
					for conDict in conData["gossipResult"]:
						scriptName = conDict[ "scriptName" ]
						scriptObj = smartImport( "ConfigObject.SpellBoxGossip.SpellGossipResult" + ":" + scriptName )()
						scriptObj.init( conDict )
						gossipResult.append( scriptObj )
					self.gossipResults[int(index)] = gossipResult
	
	def hasListenEvent( self, eventType ):
		eventType = 1 << eventType
		return ( self.listenEvents & eventType ) == eventType
	
	def addListenEvent( self, eventType ):
		eventType = 1 << eventType
		self.listenEvents |= eventType
	
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化entity
		"""
		SpellScriptBase.SpellScriptBase.initEntity( self, selfEntity )
		selfEntity.listenEvents = self.listenEvents

	def onClientActorReady( self, selfEntity ):
		"""
		客户端Character Actor已经准备好
		"""
		pass

	def requestRefreshAreaStatus( self, selfCell, playerEntity ):
		"""
		请求刷新某区域状态
		"""
		if selfCell.isInArea:
			selfCell.isInArea = False
		else:
			selfCell.isInArea = True
		self.RefreshAreaStatus( selfCell, playerEntity )

	def RefreshAreaStatus( self, selfCell, playerEntity ):
		"""
		是否在区域中
		"""
		if selfCell.isInArea and self.__checkGossipConditions( selfCell, playerEntity ):
			if selfCell.currentArea in selfCell.isExecuted and not selfCell.isExecuted[selfCell.currentArea]:
				selfCell.isExecuted[selfCell.currentArea] = True
				selfCell.stopHoldActionAndEffect()
				self.__handleGossipResults( selfCell, playerEntity )

	def refreshGossipCondition( self, selfCell, playerEntity ):
		"""
		是否满足条件显示光效
		"""
		if self.__checkGossipConditions( selfCell, playerEntity) and selfCell.currentArea in self.effectID:
			selfCell.playParticles( self.effectID[selfCell.currentArea] )

	def __checkGossipConditions( self, selfCell, playerEntity):
		"""
		检测交互条件
		"""
		if selfCell.currentArea in self.gossipConditions:
			gossipConditions = self.gossipConditions[selfCell.currentArea]
			for obj in gossipConditions:
				if not obj.check( selfCell, playerEntity ):
					return False
		return True
	
	def __handleGossipResults( self, selfCell, playerCell ):
		"""
		执行交互效果脚本
		"""
		if selfCell.currentArea in self.gossipResults:
			gossipResults = self.gossipResults[selfCell.currentArea]
			for obj in gossipResults:
				obj.do( selfCell, playerCell )
	
	
	