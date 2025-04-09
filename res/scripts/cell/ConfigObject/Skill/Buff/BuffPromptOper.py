# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""
import KBEngine
import time
#cell
import ItemFactory
import csstatus
import Functions
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop
#common
import KBEDebug
import csdefine
import Functions
import Math
import KBEMath


class BuffPromptOper( BuffLoop ):
	"""
	操作提示
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self._spaceScriptID = ""					# 某地图
		self._spacePos = Math.Vector3( 0,0,0)		# 某地
		self._radius = 0.0							# 搜索半径
		self._promptID = 0							# 技能ID\物品ID
		self._promptTip = ""						# 文字提示
		self._offset = ""							# CST-5274，界面偏移量
		
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		if self._loopTime == 0.0:		# CST-9200提供缺省支持
			self._loopTime = 1.0
		self._spaceScriptID = dictDat["Param1"]
		sPos = Functions.vector3TypeConvert( dictDat["Param2"] )
		if sPos:
			self._spacePos = KBEMath.Unreal2KBEnginePosition( sPos )
		self._radius = float( dictDat["Param3"]) if dictDat["Param3"] else 0.0
		self._promptID = int( dictDat["Param4"]) if dictDat["Param4"] else 0
		temp = dictDat["Param5"].split(";")
		self._promptTip = temp[0]
		if len(temp) >= 2:
			self._offset = temp[1]
		
	def doLoopHit( self, receiver, buffData ):
		"""
		周期打击
		"""
		BuffLoop.doLoopHit( self, receiver, buffData )
		
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			
			isShowPrompt = buffData.getTempData( "isShowPrompt", False )
			if self._spaceScriptID:
				if self._spaceScriptID != receiver.getCurrentSpaceScriptID():
					if isShowPrompt:
						buffData.setTempData( "isShowPrompt", False )
						receiver.hidePrompetOper()
					return
				pos = self._spacePos
				if not self._spacePos:
					pos = self.getCasterPosition(buffData)
				if pos and receiver.position.distTo( pos ) > self._radius:
					if isShowPrompt:
						buffData.setTempData( "isShowPrompt", False )
						receiver.hidePrompetOper()
					return

			if not isShowPrompt:
				# 物品提示可以是物品\技能，物品 需要判断是否在玩家身上
				skill = receiver.getSkill( self._promptID )
				if not skill:
					item = ItemFactory.ItemFactoryInst.createDynamicItem( self._promptID )
					if item:
						itemList = receiver.getItemInstsByID( self._promptID )
						if len(itemList) == 0:
							if not buffData.getTempData("isNoItem", False):
								buffData.setTempData( "isNoItem", True )
								receiver.statusMessage( csstatus.KITBAG_CAN_NOT_FIND_ITEM )
							return
					
				buffData.setTempData( "isShowPrompt", True )
				receiver.showPrompetOper( self._promptID, self._promptTip, self._offset )
	
	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		BuffLoop.doEnd( self, receiver, buffData, reason )
		
		isShowPrompt = buffData.getTempData( "isShowPrompt", False )
		if isShowPrompt:
			receiver.hidePrompetOper()
		buffData.setTempData( "isShowPrompt", False )

	def getCasterPosition(self, buffData):
		caster = KBEngine.entities[ buffData.casterID ]
		if caster:
			return caster.position
		return None
