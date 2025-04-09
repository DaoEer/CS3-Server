# -*- coding: utf-8 -*-
import csdefine
import csstatus
import KBEDebug

class RoleRelationInterface:
	"""
	玩家关系
	"""
	def __init__( self ):
		pass
			
	def addFoeRequest( self, playerBase ):
		"""
		<define method>
		仇人 数据请求
		"""
		playerBase.addFoeReply( self.base, self.playerDBID, self.getName(),\
		self.getProfession(), self.getLevel(), self.getCamp(), self.tongName, self.spaceScriptID )

	def addBlacklistRequest( self, playerBase ):
		"""
		<Define method>
		黑名单 数据请求
		"""
		playerBase.addBlacklistReply( self.base, self.playerDBID, self.getName(),\
		self.getProfession(), self.getLevel(), self.getCamp(), self.tongName, self.spaceScriptID )

	def addRecentContactsRequest( self, playerBase ):
		"""
		<define method>
		最近联系人 数据请求
		"""
		playerBase.addRecentContactsReply( self.base, self.playerDBID, self.getName(),\
		self.getProfession(), self.getLevel(), self.getCamp(), self.tongName, self.spaceScriptID )
	
	def addEndTimePayMoney( self, money, uid, endType ):
		"""
		<define method>
		添加有效聊天时间
		"""
		if self.subBindMoney( money, csdefine.MONEY_SUB_REASON_ADD_ENTTIME ):
			self.addEndTimeSuccess( uid, endType )
		else:
			self.statusMessage( csstatus.RELATION_MSG_ADDTIME_NOT_ENOUGH_MONEY, "" )

	def updateBlacklist( self, blackList):
		self.blackDbidList = blackList

	def cellHadBlacklist( self, playerBDID ):
		"""
		是否已经存在黑名单
		"""
		if playerBDID in self.blackDbidList:
			return True
		return False