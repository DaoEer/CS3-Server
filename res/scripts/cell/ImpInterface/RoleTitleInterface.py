# -*- coding: utf-8 -*-



import KBEDebug
import csdefine
import  TitleLoader 
import time
import ConfigObject.Skill.EffectLoader as EffectLoader
import Const
import csstatus
import CoreInterface.CombatInterface as CombatInterface
import QuestEventDefine

g_titleLoader = TitleLoader.g_titleLoader
g_titleRewardLoader = TitleLoader.g_titleRewardLoader

class RoleTitleInterface:
	"""
	玩家称号接口
	"""
	def __init__( self ):
		self.addTitleHoldEffects()
		self.availableTitles = []           #可获得的所有称号列表，后续如果加上阵营职业性别限制，则需要从总表中筛选一遍，目前暂时没有这个限制
		self.initAvailableTitles()

		

	def rewardTitle(self):
		"""
		通过等级,境界，充值，消费等方式(提升时)获取称号
		"""

		#筛出已拥有的称号
		titleIDList = [ i for i in self.availableTitles if i not in self.titles ]
		
		for titleID in titleIDList:
			if self.canRewardTitleCheck(titleID):
				self.addTitle(titleID)


	def canRewardTitleCheck(self, titleID):
		"""
		判断当前能否获取称号奖励(等级,境界，充值，消费等方式获取)
		"""
		titleRewardDatas = g_titleRewardLoader.getAllData()
		if titleID not in titleRewardDatas.keys():
			return False
		datas = titleRewardDatas[titleID]
		for data in datas:
			#阵营
			if data["camp"]!=self.getCamp() and data["camp"]!=0:	continue
			#职业
			if data["profession"]!=self.getProfession() and data["profession"]!=0:	continue
			#性别
			if data["sex"]!=self.getGender() and data["sex"]!=0:	continue
			#等级条件
			if data["level"]>self.getLevel() and data["level"]!=0:	continue
			#境界条件
			if  data["xiuweiLevel"]>self.getXiuweiLevel() and data["xiuweiLevel"]!=0:	continue

			return True
		return False
		


	def sendTitleData(self):
		"""
		初始化客户端的称号数据,发送玩家已拥有称号数据
		"""
		for title in self.titles:
			self.setTitleData(title) 
			
	def checkAvailableTitle(self, titleID):
		"""
		检查可获得称号，目前仅检查阵营和职业
		"""
		titleRewardDatas = g_titleRewardLoader.getAllData()
		if titleID not in titleRewardDatas.keys():
			return False
		datas = titleRewardDatas[titleID]
		for data in datas:
			#阵营
			if data["camp"]!=self.getCamp() and data["camp"]!=0:	continue
			#职业
			if data["profession"]!=self.getProfession() and data["profession"]!=0:	continue
			
			return True
		return False
		
	def initAvailableTitles(self):
		"""
		初始化"可获得称号"
		"""
		data = g_titleLoader.getAllData()
		for key in data:
			if self.checkAvailableTitle(int(key)):
				self.availableTitles.append(int(key))


	def sendAvailableTitleData(self):
		"""
		初始化客户端的称号数据，发送玩家可获得的称号数据
		"""
		for title in self.availableTitles:
			self.setAvailableTitleData(title)

	
	def addTitle( self, titleID ):
		"""
		define method
		给玩家增加一个称号
		@param titleID : 称号的ID
		@type titleID : INT32
		"""
		if titleID == csdefine.TITLE_NONE : return  #不在最开始进行titleID in self.titles的判断。要保留最新的称号。
		titleData = g_titleLoader.getData( titleID )
		if not titleData:
			return
		if titleID in self.titles:
			self.removeTitle( titleID )
		self.titles.append( titleID )
		self.base.addTitle( titleID )
		if g_titleLoader.isTimeLimit( titleID ):	# 如果是个有时限的称号，开始计时
			tempTime = titleData[ "LimitTime" ] + time.time()
			timerID = self.addTimerCallBack( titleData[ "LimitTime" ], "onTitleAddTimer", () )
			self.titleLimitTime.append( { "titleID":titleID, "time":tempTime, "timerID":timerID } )
		titleUname = Const.MSG_FORMAT_COLOR_STRING%("(255, 0, 255, 255)", "[%s]"%titleData["TitleName"] )
		self.statusMessage( csstatus.ROLE_MSG_GAIN_TITLE,titleUname)
		self.setTitleData(titleID)
		self.client.CLIENT_OnTitleAdded(titleID)
		

	def removeTitle( self, titleID ):
		"""
		移除玩家的一个称号
		define method
		@param titleID : 称号的ID
		@type titleID : INT32
		"""
		if not titleID in self.titles:
			KBEDebug.ERROR_MSG( "Could not remove such title id %i because it does not exist in player( %s )'s titles!" % ( titleID, self.getName() ) )
			return
		
		self.titles.remove( titleID )
		self.base.removeTitle( titleID )
		self.client.CLIENT_OnTitleRemoved( titleID )
		if self.title == titleID:
			self._changeTitle( csdefine.TITLE_NONE )
		for temp in self.titleLimitTime:
			if temp[ "titleID" ] == titleID:
				self.popTimer( temp[ "timerID" ] )
				self.titleLimitTime.remove( temp )
				break


	def _changeTitle( self, titleID ):
		"""
		改变称号，所有改变称号的入口。

		对于一些需要base数据才能生成的称号，可以避免异步问题

		@param oldTitle : 旧称号的ID
		@type oldTitle : INT32
		@param titleID : 称号的ID
		@type titleID : INT32
		"""
		oldTitle = self.title
		self.title = titleID
		self.oldCombatPower = self.combatPower
		#称号改变后重新计算战斗属性
		self.removeTitleHoldEffects()
		self.addTitleHoldEffects()
		self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_TITLE)
		self.onCombatPowerChange(self.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_TITLE)
		self.triggerQuestEvent( QuestEventDefine.EVENT_EVENT_TRIGGER, self.title )
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onPlayerUseTitle( spaceEntity, self, self.title )

	def CELL_selectTitle( self, srcEntityID, titleID ):
		"""
		Exposed method.
		玩家选择一个称号
		@param titleID : 称号的ID
		@type titleID : UINT8
		"""		
		if not self.validateClientCall( srcEntityID ):
			KBEDebug.ERROR_MSG( "self.id != srcEntityID" )
			return
		if titleID == self.title:
			return
		if titleID not in self.titles and titleID!=csdefine.TITLE_NONE:	# 判断titleID参数是否合法,选择0为卸下称号
			return

		self._changeTitle( titleID )


	def onTitleAddTimer( self ):
		"""
		添加有时间限制的称号的回调
		"""
		for temp in self.titleLimitTime:
			if temp[ "time" ] - time.time() < 1.0:		# 考虑误差在1秒以内
				self.removeTitle( temp[ "titleID" ] )
				break		
#---------------------称号加持--------------------------------


	def addTitleHoldEffects( self ):
		"""
		添加称号的持有效果
		"""
		holdEffectIDs = g_titleLoader.getHoldEffectIDs(self.title)
		for effectID in holdEffectIDs:
			index = self.addFixIDHoldEffect( effectID, self )
			if index != -1:
				self.titleHoldEffectIndexs.append( index )

	def removeTitleHoldEffects( self ):
		"""
		移除称号持有效果
		"""
		for index in self.titleHoldEffectIndexs:
			self.removeFixIDHoldEffect( index )
		self.titleHoldEffectIndexs = []

	def getEquipAttachProperties(self):
		"""
		获取装备的附加属性统计
		"""
		attackPropertiesStr = g_titleLoader.getAttackPropertiesStr(self.title)

		return {"_extra" : attackPropertiesStr}




#-----------------------发送数据给客户端----------------------------------
		
	def parseAttackPropertiesByID(self, titleID):
		"""
		解析属性,发送给界面显示 格式如："30008#239|30010#239|30012#184|30013#1017|30006#15350"
		"""
		attackPropertiesStr = g_titleLoader.getAttackPropertiesStr(titleID)
		result = ""
		for key, value in attackPropertiesStr.items():
			result += str(key)+"#"+str(value)+"|"
		#除去最后一个"|"
		if len(result):
			result = result[:len(result)-1]
		#KBEDebug.ERROR_MSG("result = %s"%(result))
		return result

		

	def getLimitTimeByID(self, titleID):
		"""
		剩余时间
		"""
		limitTime = -1.0
		for temp in self.titleLimitTime:
			if temp[ "titleID" ] == titleID:
				limitTime = temp["time"] - time.time()
				break
		return limitTime
		
	def setTitleData( self, titleID ):
		"""
		发送称号数据
		"""
		attackPropertiesStr = self.parseAttackPropertiesByID(titleID)
		limitTime = self.getLimitTimeByID(titleID)
		self.client.CLIENT_OnSetTitleData(titleID, attackPropertiesStr, limitTime)


	def setAvailableTitleData( self, titleID ):
		"""
		发送可获得称号数据
		"""
		attackPropertiesStr = self.parseAttackPropertiesByID(titleID)
		limitTime = self.getLimitTimeByID(titleID)
		self.client.CLIENT_OnSetAvailableTitleData(titleID, attackPropertiesStr, limitTime)