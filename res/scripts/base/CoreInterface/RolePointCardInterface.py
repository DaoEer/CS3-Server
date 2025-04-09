# -*- coding: utf-8 -*-
import KBEngine
import csconst
import csdefine
import KST
import KBEDebug

class RolePointCardInterface:
	def __init__( self ):
		pass
	
	def sellPointCard( self, cardNo, pwd, serverName, cardPrice ):
		"""
		define method
		玩家寄售点卡
		"""
		cardInfo = PointCardInfo()
		cardInfo.cardNo 	= cardNo.lower()
		cardInfo.passWord 	= pwd
		cardInfo.serverName = serverName
		cardInfo.salesName  = self.playerName
		cardInfo.salesAccount = self.accountEntity.playerName
		cardInfo.price		= cardPrice
		cardInfo.salesIP	= self.clientAddr[0]

		KBEngine.globalData["PointCardMgr"].sellPointCard( cardInfo, self )


	def buyPointCard( self, cardNo, money ):
		"""
		define method
		"""
		KBEngine.globalData["PointCardMgr"].buyPointCard( cardNo, money, self, self.playerName, self.accountEntity.playerName )


	def queryPointCards( self, page ):
		"""
		exposed method
		"""
		KBEngine.globalData["PointCardMgr"].queryPointCards( self, page )