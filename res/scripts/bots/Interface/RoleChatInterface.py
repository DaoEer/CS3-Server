# -*- coding: utf-8 -*-
import KBEngine
class RoleChatInterface:
	
	def __init__(self):
		pass
		
	def onRoleSendChatMessage( self, type, message, richText ):
		self.cell.onRoleSendChatMessage(self.playerName, type, message, richText )
		self.outputMsg("onRoleSendChatMessage {}".format(message))
		
	def onReceiveChatMessageCB(self, chatData):
		pass
		
	def onStatusMessage(self, state, params):
		"""
		used for receiving states message from server
		<Arg> UINT16 </Arg>	<!-- 状态码, see also common/GloballyStatus.py -->
		<Arg> UNICODE </Arg>	<!-- 额外参数 -->
		"""
		args = None
		if params.strip() != '':
			args = json.loads(params)
			
		errorConfig = g_errorConfig[state]
		serverVar = errorConfig['serverVar']
		try:
			func = getattr(self, 'onStatusMessage_' + serverVar)
		except:
			#ERROR_MSG( "%s: state = '%s', params = '%s'" % (self.id, errorConfig['errorDescription'], params) )
			return
		
		if args != None:
			func(errorConfig, *args)	
		else:
			func(errorConfig)
		
	def onReceiveQuickSettings(self, params):
		pass
		
	def onChangeQuickSettings(self, params):
		pass
		
	def onReceivePageSettings(self, params):
		pass
		
	def onReceiveDeletePage(self, pageType):
		pass
		
	def onReceivePageData(self, params):
		pass
		
	def onReceiveNewPageData(self, params):
		pass
		
		
	def CLINT_onChatQueryRoleExist( self, p1 ):
		pass
