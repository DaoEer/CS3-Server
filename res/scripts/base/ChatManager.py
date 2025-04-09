import KBEngine
import KST
import csstatus
from KBEDebug import *
from csdefine import *
from CoreObject.MgrPersistentObject import MgrPersistentObject
from ChatDataType import ChatData
from Functions import Functor
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class ChatManager( MgrPersistentObject ):
	"""
	聊天管理类
	接收cell发送聊天请求
	"""
	def __init__( self ):
		MgrPersistentObject.__init__( self )
		self.onCompleteInit()
		self.register()

	def register(self ):
		taskEvents = {"ChatManager_start": "onChatManager_start"
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1, () )
				
	def onChatManager_start(self, cmd, *callbackArgs):
		KST.g_baseAppEntity.globalUpdateChatNum()
		
	def onBroadcastChat( self, chatData ):
		"""
		<define method>
		世界广播消息
		"""
		KST.g_baseAppEntity.globalChat( chatData )
#		KST.g_baseAppEntity.broadcastChat( chatData )

	def onBroadcastChatCamp(self,chatData, camp, playerName):
		"""
		<define method>
		世界广播消息(阵营)
		"""
		KST.g_baseAppEntity.globalChatCamp( chatData , camp , playerName)

	def onBroadcastChatSchool(self,chatData, camp, profession, playerName):
		"""
		<define method>
		世界广播消息(门派)
		"""
		KST.g_baseAppEntity.globalChatSchool( chatData , camp, profession , playerName)

	def onDesignatedChat( self, avatar, name, chatData, srcPlayerName ):
		"""
		<define method>
		查找玩家给予聊天消息
		"""

		KST.g_baseAppEntity.lookupRoleBaseByName( name, Functor( self.onDesignatedChatCallback, avatar, name, chatData, srcPlayerName ))
		#KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor(self.onDesignatedChatCallback, avatar, chatData)  )

	def onDesignatedChatCallback( self, avatar, name, chatData, srcPlayerName, target ):
		"""
		callback method.
		先查询目标是否在线 不在线则去数据库查找有无该玩家
		"""
		if target:
			if chatData.type == CHAT_TYPE_WHISPER:  # 密语
				target.onFriendChatCB( avatar, chatData, srcPlayerName )
			else:
				target.cell.onReceiveChatMessage( chatData )
		else:
			self.chatQueryRoleIsInTable( avatar, name)
			#avatar.client.statusMessage( csstatus.CHAT_TARGET_NOT_EXIST, "" )
		
#		if target is False:
#			if avatar != None:
#				avatar.onChatErrorByNoPlayer()
#
#		if target is True:
#			if avatar != None:
#				avatar.onChatErrorByPlayerNoOnline()
#
#		target.cell.onReceiveChatMessage( chatData )

	def chatQueryRoleIsInTable( self , avatar, name ):
		"""
		exposed method
		查询对象是否存在
		"""
		query = "select id from tbl_Role where sm_playerName = '%s'"%name
		KBEngine.executeRawDatabaseCommand(query,Functor(self.onChatQueryRoleIsInTable , avatar , name) )

	def onChatQueryRoleIsInTable( self , avatar, name,  result, rows, insertid, errstr):
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if result:
			avatar.statusMessage(csstatus.RELATION_MSG_SEND_MSG_AS_PALYER_OFFLINE,"")	#存在就说明不在线
		else :
			avatar.statusMessage(csstatus.CHAT_TARGET_NOT_EXIST,"")
			#self.client.CLINT_onChatQueryRoleExist( False )


	def onSendPlayerMessage( self, playerDBID, message, rictText ):
		"""
		<define method>
		发送玩家系统消息
		"""
		chatData = ChatData()
		parms = [ { "key":"type", "value":CHAT_SYSTEM_PRIVATE }, { "key":"playerDBID", "value":playerDBID }]
		chatData.init( 0, "系统消息", CHAT_TYPE_SYSTEM, ENTITY_FLAG_UNKNOWN, message, rictText, parms )
		self.onDesignatedChat( None, playerDBID, chatData )

	def onSendSpaceMessage( self, spaceID, message, rictText ):
		"""
		<define method>
		发送地图广播消息
		"""
		chatData = ChatData()
		parms = [ { "key":"type", "value":CHAT_SYSTEM_SPACE }, { "key":"spaceID", "value":spaceID } ]
		chatData.init( 0, "系统消息", CHAT_TYPE_SYSTEM, ENTITY_FLAG_UNKNOWN, message, rictText, parms )
		#g_chatMgr.send( self, chatData )

	def onSendWorldMessage( self, message, rictText ):
		"""
		<define method>
		发送世界广播消息
		"""
		chatData = ChatData()
		parms = [ { "key":"type", "value":CHAT_SYSTEM_WORLD } ]
		chatData.init( 0, "系统消息", CHAT_TYPE_SYSTEM, ENTITY_FLAG_UNKNOWN, message, rictText, parms )
		self.onBroadcastChat( chatData )

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