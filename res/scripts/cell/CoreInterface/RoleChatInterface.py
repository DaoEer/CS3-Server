
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csstatus
import Functions
from ConfigObject.Chat.ChatBase.ChatMgr import g_chatMgr
from ConfigObject.Chat.ChatBase.ChatMgr import g_TYPE_MAPPING
from ChatDataType import ChatData
import time
import datetime
import json
import GMCommand

class RoleChatInterface:
	"""
	玩家发言接口
	"""
	def __init__( self ):
		"""
		初始化
		"""
		if len(self.quickSettings) < 1:
			self.quickSettings = []
			config = g_chatMgr.getChannelConfig()
			for k, v in config.items():
				newDict= { 'channelType':int(v['type']), 'isCanModify':v['isCanModify'], 'shortcutKey':v['shortcutKey'] }
				self.quickSettings.append(newDict)

		if len(self.pageSettings) < 1:
			self.pageSettings = []
			pageConfig = g_chatMgr.getPageConfig()
			for key, value in pageConfig.items():
				makeDic = { 'pageType':int(value['pageType']), 'isDeletable':value['isDeletable'], 'isDraggable':value['isDraggable'], 'pageName':value['pageName'], 'channelList':value['chanelArg'] }
				self.pageSettings.append(makeDic)
		if self.updChatNumTime < self.getTimesTamp():
			self.updateChatNum()

	def getTimesTamp(self):
		#每日七点的时间戳
		a = datetime.datetime.now().strftime("%Y-%m-%d")+" %2d:00:00"%7
		timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
		timeStamp = int(time.mktime(timeArray))
		return timeStamp
	def initChatDatas( self ):
		"""
		通知客户端快捷键以及页签的数据
		"""
		self.client.onReceiveQuickSettings( self.makeDictForQS() )
		self.client.onReceivePageSettings( self.makeDictForPS() )
		
	def makeDictForQS( self ):
		"""
		将快捷键数据打包
		"""
		dataListQS = {"datas":[]}		
		i = 0

		while i < len(self.quickSettings):
			getDict = {  'channelType':self.quickSettings[i]['channelType'], 'isCanModify':self.quickSettings[i]['isCanModify'], 'shortcutKey':self.quickSettings[i]['shortcutKey'] }
			dataListQS["datas"].append(getDict)
			i = i + 1

		return dataListQS

	def makeDictForPS( self ):
		"""
		将页签数据打包
		"""
		dataListPS = {"datas" : []}		
		i = 0

		while i < len(self.pageSettings):
			makeList = []

			for c in self.pageSettings[i]['channelList']:
				makeList.append(c)

			getDict = {  'pageType':self.pageSettings[i]['pageType'], 'isDeletable':self.pageSettings[i]['isDeletable'], 'isDraggable':self.pageSettings[i]['isDraggable'], 'pageName':self.pageSettings[i]['pageName'], 'channelList':makeList }
			dataListPS["datas"].append(getDict)
			i = i + 1

		return dataListPS

	def getAPageData( self, pageType ):
		"""
		获取指定的一条页签数据
		"""
		i =0
		makeDict ={}
		while i < len(self.pageSettings):
			makeList = []

			for c in self.pageSettings[i]['channelList']:
				makeList.append(c)	

			if self.pageSettings[i]["pageType"] == pageType:
				makeDict = { 'pageType':self.pageSettings[i]['pageType'], 'isDeletable':self.pageSettings[i]['isDeletable'], 'isDraggable':self.pageSettings[i]['isDraggable'], 'pageName':self.pageSettings[i]['pageName'], 'channelList':makeList }
			i = i+1
		
		return makeDict

	def receivePageSettings( self, playerID ):
		"""
		<exposed method>
		请求页签数据
		"""
		if not self.validateClientCall( playerID ):
			return

		self.client.onReceivePageSettings( self.makeDictForPS() )				

	def receiveResetPageSettings( self, playerID, pageType ):
		"""
		<exposed method>
		请求重置某个页签设置
		"""
		if not self.validateClientCall( playerID ):
			return

		getPageType = int(pageType)
		pageConfig = g_chatMgr.getPageConfig()

		iPage = 0
		while iPage <len(self.pageSettings):
			if self.pageSettings[iPage]['pageType'] == getPageType:
				if getPageType <5:
					self.pageSettings[iPage]['isDeletable'] = pageConfig[getPageType]['isDeletable']
					self.pageSettings[iPage]['isDraggable'] = pageConfig[getPageType]['isDraggable']
					self.pageSettings[iPage]['pageName'] = pageConfig[getPageType]['pageName']
					self.pageSettings[iPage]['channelList'] = pageConfig[getPageType]['chanelArg']
				else:
					self.pageSettings[iPage]['isDeletable'] = 1
					self.pageSettings[iPage]['isDraggable'] = 1
					self.pageSettings[iPage]['pageName'] = "自定义页签" + str(getPageType -4)
					self.pageSettings[iPage]['channelList'] = []			
			iPage = iPage +1

		self.client.onReceivePageData( self.getAPageData(getPageType))

	def receiveMakeNewPage( self, playerID, pageType, pageName, pageData):
		"""
		<exposed method>

		请求增加一个自定义页签
		@param playerID: 玩家的ID
		@param pageData:  所含频道的信息（Str）	
		"""
		if not self.validateClientCall( playerID ):
			return

		if self.makePageTimes < 1:
			return
		#解析客户端传过来的数据
		pageType = int(pageType)
		#只能创建自定义页签
		if pageType < 5:		
			return
		getPageData = []
		try:
			pageDataList = pageData.split("#")
			for index in pageDataList:
				getPageData.append(int(index))
		except:
			pass

		newPage = { "pageType":pageType, "isDeletable":1, "isDraggable":1, "pageName":pageName, "channelList":getPageData }
		self.pageSettings.append(newPage)
		self.makePageTimes = self.makePageTimes - 1

		#通知玩家新建页签成功,返回新建页签的数据
		self.client.onReceiveNewPageData( self.getAPageData(pageType))

	def receiveDeletePage( self, playerID, pageType ):
		"""
		<exposed method>

		请求删除一个页签
		@param playerID: 玩家的ID
		@param pageType: 自定义页签的类型
		"""
		if not self.validateClientCall( playerID ):
			return

		index = -1
		i = 0
		while i <len(self.pageSettings):
			if self.pageSettings[i]["pageType"] == int(pageType) and self.pageSettings[i]["isDeletable"] > 0:
				index = i
			i =i +1
		if index >-1:
			del self.pageSettings[index]
			self.makePageTimes = self.makePageTimes + 1

		#这里通知玩家删除了某个页签（返回该页签的pageType）
		self.client.onReceiveDeletePage( int(pageType) )

	def receiveChangePageData( self, playerID, pageData ):
		"""
		<exposed method>
		请求更改页签内所含的频道信息

		@param playerID: 玩家的ID	
		@param pageData:  所含频道的信息（Str）		
		"""
		if not self.validateClientCall( playerID ):
			return

		#解析客户端传过来的数据
		
		getPDList = pageData.split("|")
		pageType = int(getPDList[0])
		pageName = getPDList[1]
		getPageData = []
		try:
			pageDataList = getPDList[2].split("#")
			for index in pageDataList:
				getPageData.append(int(index))
		except:
			pass

		i = 0
		while i < len(self.pageSettings):
			if self.pageSettings[i]["pageType"] == pageType:
				if int(self.pageSettings[i]["pageType"]) == 0 and 14 not in getPageData:	#综合页签不能删除系统频道
					return	

				self.pageSettings[i]["pageName"] = pageName
				self.pageSettings[i]["channelList"] = getPageData
			i = i + 1
			
		#只需要告诉玩家修改了的那条页签数据
		self.client.onReceivePageData( self.getAPageData(int(pageType)) )			

	def receiveQuickSettings( self, playerID ):
		"""
		<exposed method>
		请求玩家聊天频道自定义设置
		"""
		if self.id != playerID:
			return

		self.client.onReceiveQuickSettings( self.makeDictForQS() )

	def receiveResetQuickSettings( self, playerID ):
		"""
		<exposed method>
		请求恢复成默认的聊天频道快捷键设置
		"""
		if not self.validateClientCall( playerID ):
			return

		#重置快捷键设置
		self.quickSettings = []
		config = g_chatMgr.getChannelConfig()
		for k, v in config.items():
			newDict= { "channelType":int(v["type"]), "isCanModify":v["isCanModify"], "shortcutKey":v["shortcutKey"] }
			self.quickSettings.append(newDict)

		self.client.onReceiveQuickSettings( self.makeDictForQS() )	#通知客户端最新的快捷键设置		

	def receiveReviseQS( self, playerID, quickSettingDatas ):
		"""
		<exposed method>
		请求修改聊天频道快捷键设置
		"""
		if not self.validateClientCall( playerID ):
			return

		#解析客户端发过来的快捷键设置数据
		getQSList = quickSettingDatas.split("|")
		index = 0
		newQSDatas ={}
		while index < len(getQSList):
			quickSettingdata = getQSList[index].split("#")
			newQSDatas[int(quickSettingdata[0])] = quickSettingdata[1]
			index = index +1

		i = 0
		while i < len(self.quickSettings):
			if self.quickSettings[i]["channelType"] in newQSDatas.keys():
				self.quickSettings[i]["shortcutKey"] = newQSDatas[self.quickSettings[i]["channelType"]]
			i = i + 1
		self.client.onChangeQuickSettings( self.makeDictForQS() )	# 通知客户端更新

	def onRoleSendChatMessage( self, playerID, name, type, message, richText ):
		"""
		<exposed method>
		发送消息
		"""
		if not self.validateClientCall( playerID ):
			return
		chatData = ChatData()
		richText = richText.split("/")
		for x in range( len(richText)-1, -1, -1):
			if richText[x] == '':
				del richText[x]
		chatData.init( self.playerDBID, name, int(type), int(self.getEntityFlag()), message, richText, {} )
		if chatData.type == csdefine.CHAT_TYPE_SYSTEM and chatData.type == csdefine.CHAT_TYPE_MONSTER:
			# 发言类型不符合要求
			KBEDebug.ERROR_MSG( "type error" )
			return	
		g_chatMgr.onSend( self, chatData )

	def onRoleSendGMCommandMessage( self, playerID, dstEntityID, cmd, args ):
		"""
		<Exposed method>
		"""
	
		if not self.validateClientCall( playerID ):
			return
		GMCommand.executeGMCommand(self, int(dstEntityID), cmd, args)

	def onReceiveChatMessage( self, chatData ):
		"""
		<define method>
		接受消息
		"""
		if self.getClient():
			self.client.onReceiveChatMessageCB( chatData )
		
	def onRoleSendGroupMessage( self, playerID, name, type, message, richText, groupUID ):
		"""
		<Exposed method>
		发送讨论组消息
		"""
		if not self.validateClientCall( playerID ):
			return
			
		chatData = ChatData()
		chatData.init( self.playerDBID, name, int(type), message, richText.split("/"), { "groupUID" : groupUID } )
		g_chatMgr.onSend( self, chatData )

	def onReceiveGroupMessage( self, chatData ):
		"""
		<define method>
		接受讨论组消息
		"""
		self.client.onReceiveChatMessageCB( chatData )
	
	def onChatErrorByNoPlayer( self ):
		"""
		<define method>
		回调：玩家不存在
		"""
		KBEDebug.ERROR_MSG( "no player" )

	def onChatErrorByPlayerNoOnline( self ):
		"""
		<define method>
		回调：玩家不在线
		"""
		KBEDebug.ERROR_MSG( "no online player" )

	def onSendChatSuccess( self, chatData ):
		"""
		callback method.
		发送成功
		"""
		pass

	def onSendChatFail( self, chatData ):
		"""
		callback method.
		发送失败
		"""
		pass

	def gagForPlayer( self, type, gagtime, reason = csdefine.CHAT_FORBID_NONE ):
		"""
		禁止玩家在某一频道发言
		"""
		self.gagData[type] = time.time() + gagtime

	def gagAllForPlayer( self, gagtime ):
		"""
		使玩家全频道禁言
		"""
		if self.gagTime == 0:
			self.firstGagTime = time.time()

		if self.firstGagTime + 86400 < time.time():
			self.gagTime = 0

		getGagTime = gagtime
		if self.gagTime+1 >= 10:
			self.gagTime = 0
			getGagTime = 86400
		else:
			self.gagTime = self.gagTime+1

		i = 0
		while i < len(g_TYPE_MAPPING):
		 	self.gagForPlayer(i,gagtime)
		 	i = i + 1

	def unlockAllGag( self ):
		"""
		解除玩家所有禁言
		"""
		i = 0
		while i < len(g_TYPE_MAPPING):
			self.unlockForPlayerGag(i)
			i = i + 1

	def unlockForPlayerGag( self, type ):
		"""
		解除玩家在某一频道的禁言状态
		"""
		if type in self.gagData.keys():
			del self.gagData[type]
			return True
		else:
			return False

	def checkGagState( self, type ):
		"""
		验证玩家是否在某频道被禁言
		"""
		if type in self.gagData.keys():
			if self.gagData[type] >= time.time():
				return False
			else:
				del self.gagData[type]

		return True

	def __splitMessage(self, message, msgInfo ) :
		"""
		萃取指令
		"""
		if message.startswith( "/" ) :
			sps = message[1:].split( None,1)
			if len( sps ) == 0 :
				return False
			msgInfo[0] = sps[0]
			if len( sps ) == 2 :
				msgInfo[1] = sps[1]
			else :
				msgInfo[1] = ""
			return True
		return False

	def updateChatNum(self):
		"""
		刷新所有频道的发言数量
		"""
		i = 0
		while i < len(g_TYPE_MAPPING):
			self.chatNum[i] = 0
			i += 1
		self.updChatNumTime = int(time.time())

	def CELL_chatQueryRoleIsInTable( self , srcEntityID, receiverName):
		"""
		exposed method
		查询私聊的对象是否存在
		"""
		query = "select id from tbl_Role where sm_playerName = '%s'"%receiverName
		KBEngine.executeRawDatabaseCommand(query,Functions.Functor(self.onChatQueryRoleIsInTable) )

	def onChatQueryRoleIsInTable( self , result, rows, insertid, errstr):
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if result:
			self.client.CLINT_onChatQueryRoleExist( True )
		else :
			self.statusMessage(csstatus.CHAT_TARGET_NOT_EXIST,"")
			self.client.CLINT_onChatQueryRoleExist( False )

	def onReceiveChatMessageWithDBID( self, roleDBID, chatData ):
		"""
		"""
		if not self.cellHadBlacklist(roleDBID):
			self.onReceiveChatMessage(chatData)
