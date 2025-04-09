# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import csstatus
import csconst
import KST
import Functions
import KBEngine
import time
import json
from MailDataInfo import g_mailDataInfo
from MsgLogger import g_logger
import LogDefine

class RoleMailInterface:
	"""
	玩家邮件接口
	"""
	def __init__( self ):
		"""
		"""
		self.mail_allInfo = {}
		self.mail_sending = False		# 临时标记，用于阻止连续发送多封邮件而导致邮件数据的不正确
		self.mail_sendInfo = {}			# 临时存储要发送的邮件的信息

#----------------------------------玩家发送邮件--------------------------------
	def BASE_mail_send(self, receiverName, title, content):
		"""
		exposed method
		玩家寄信
		receiverName：收信人名称
		title: 邮件标题
		content:邮件内容
		"""
		#不允许同时发送多封信件，以避免出现后来的信件内容覆盖前面的信件内容
		if not self.validateClientCall():
			return
			
		if self.mail_sending:
			return
			
		if receiverName == "":
			self.statusMessage( csstatus.MAIL_RECEIVER_NAME_EMPTY,"" )
			return
			
		if self.hadBlacklist(receiverName):
			self.statusMessage( csstatus.RELATION_MSG_FORBID_SEND_MAIL_BLACK_LIST )
			return

		if receiverName == self.getName():
			self.statusMessage( csstatus.MAIL_RECEIVER_IS_SENDER,"" )
			return

		if title == "":
			self.statusMessage( csstatus.MAIL_TITLE_IS_EMPTY,"" )
			return

		if len(title) > csconst.MAIL_TITLE_LENGTH_MAX:
			self.statusMessage( csstatus.MAIL_TITLE_TOO_LONG,"" )
			return
		if len(content) > csconst.MAIL_CONTENT_LENGTH_MAX:
			self.statusMessage( csstatus.MAIL_CONTENT_TOO_LONG,"" )
			return
		
		query = "select id from tbl_Role where sm_playerName = '%s'"%receiverName

		KBEngine.executeRawDatabaseCommand(query,Functions.Functor(self._mail_queryRoleIsInTable, receiverName, title, content) )

	def _mail_queryRoleIsInTable( self, receiverName, title, content,result, rows, insertid, errstr ):
		"""
		查询数据库中是否存在改玩家
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if not result:
			self.statusMessage(csstatus.MAIL_RECEIVER_NOT_FOUND,"")
			return
		query = """SELECT cr.sm_relationStatus from kbe_Relation as cr WHERE cr.sm_playerDBID1 = %i and cr.sm_playerDBID2 = %i union
		SELECT cr.sm_relationStatus from kbe_Relation as cr WHERE cr.sm_playerDBID2 = %i and cr.sm_playerDBID1 = %i"""% (self.databaseID,int(result[0][0]),int(result[0][0]),self.databaseID )
		
		KBEngine.executeRawDatabaseCommand( query, Functions.Functor(self._mail_queryRelationForCheckCb, receiverName, title, content) )

	def _mail_queryRelationForCheckCb( self, receiverName, title, content,result, rows, insertid, errstr  ):
		"""
		"""
		if result:
			if int(result[0][0]) & csdefine.ROLE_RELATION_BLACKLIST or int(result[0][0]) & (csdefine.ROLE_RELATION_BLACKLIST << 16 ):
				self.statusMessage( csstatus.RELATION_MSG_FORBID_SEND_MAIL_IN_ROLE_BLACK_LIST, receiverName )
				return

		if self.isDestroyed:
			return

		self.mail_sendInfo = {	"receiverName" 	: receiverName,
								"title" 		: title,
								"content" 		: content,
							}

		self.mail_sending = True

		KST.g_baseAppEntity.lookupRoleBaseByName( receiverName,Functions.Functor(self._mail_getPlayerMailboxCb ) )

	def _mail_getPlayerMailboxCb( self,target ):
		"""
		寄信过程中通过收信人名字查找收信人是否存在，以及在线情况的回调函数
		"""
		self.mail_sending = False
		if target:
			playerBase = target
		else:
			playerBase = None
			
		self.cell.mail_send(	self.mail_sendInfo["receiverName"], \
								self.mail_sendInfo["title"], \
								self.mail_sendInfo["content"], \
								playerBase )		

	def mail_newNotify( self, senderName, timeFlag ):
		"""
		通知有新邮件。这是当有人给当前玩家寄信的时候被调用。一般由MailManager调用。
		接到新邮件通知的时候,当前玩家到数据库中去查找新的邮件。
		senderName: 发信者的名称，用于查找过滤
		timeFlag: 发信时间标记，用于查找过滤
		"""
		# 搜索属于我的邮件，且发送且是senderName而发送时间为timeFlag的信件，
		# 虽然这样搜索在极短的情况下有可能会有多条，但在回调用会进行处理。
		query = "select id, sm_title, sm_content, sm_item0, sm_item1, sm_item2, sm_item3,sm_money, sm_senderName, sm_receiverName, sm_senderType, UNIX_TIMESTAMP(sm_receiveTime), sm_isRead,sm_isUpper, sm_lingshi, sm_xianshi, sm_bindMoney from custom_MailTable where sm_receiverName = '%s' and sm_senderName = '%s' and sm_timeFlag = %i;" % (self.getName(), senderName ,timeFlag)
		KBEngine.executeRawDatabaseCommand( query, self._mail_newNotifyCb )

	def _mail_newNotifyCb( self,result, rows, insertid, errstr):
		"""
		通知有新邮件回调函数.
		这个回调函数把从数据库读取到的新邮件放入到base的邮件信息中。
		同时还把新邮件部分数据发送到客户端。
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if self.isDestroyed:
			return
		for m in result:
			id = int(m[0])
			if id in self.mail_allInfo:
				continue	# 对于已经存在于列表中的邮件，我们采取忽略态度（这种情况在极端的状态是会发生的）
			mailItemDatas = [m[3].decode("utf-8"), m[4].decode("utf-8"), m[5].decode("utf-8"), m[6].decode("utf-8")]
			itemDatas = []
			for mailItemData in mailItemDatas:
				if mailItemData:
					itemDict = json.loads( mailItemData )
					itemDatas.append(itemDict)
			mailDict = {
				"id":id,	
				"title"			: m[1].decode("utf-8"),
				"content"		: m[2].decode("utf-8"),
				"itemList": itemDatas,
				"money"			: int( m[7] ),
				"senderName"	: m[8].decode("utf-8"),
				"receiverName"	: m[9].decode("utf-8"),
				"senderType"	: int( m[10] ),
				"receiveTime"	: int( m[11] ),
				"remainTime":int(int(m[11]) + csconst.MAIL_OUTTIMED - time.time()),
				"isRead": int(m[12]),
				"isUpper":int(m[13]),
				"lingshi":int(m[14]),
				"xianshi":int(m[15]),
				"isTaken"		: 0,				# 用于临时记录当前是否正在拿取邮件
				"bindMoney"		: int( m[16] ),
			}
			mailData = g_mailDataInfo.createObjFromDict(mailDict)
			if mailData.isUpper:
				#新规则，当玩家邮件已满，只提示csstatus.MAIL_FULL，不再是删除邮件（CST-11659），此处不再调用checkHasNoItemsMail
				#self.checkHasNoItemsMail( mailData ) 
				self.statusMessage(csstatus.MAIL_FULL, "")
			else:
				self.mail_allInfo[mailData.id] = mailData
				self.client.ReceiveMail( mailData )
				self.statusMessage( csstatus.MAIL_RECEIVER )

#----------------------------查询玩家身上有所邮件-----------------------------------
	def initClientData( self ):
		"""
		"""
		self.initAllMailToClient()

	def initAllMailToClient( self ):
		"""
		查询邮件，主要用于玩家登陆上线时，一次性查询所有邮件所用。
		查询所有收信者是玩家
		"""
		self.mail_allInfo = {}
		query = "select id, sm_title, sm_content, sm_item0, sm_item1, sm_item2, sm_item3, sm_money, sm_senderName, sm_receiverName, sm_senderType,UNIX_TIMESTAMP(sm_receiveTime), sm_isRead,sm_isUpper, sm_lingshi, sm_xianshi, sm_bindMoney from custom_MailTable where sm_receiverName = '%s'" % self.getName()
		KBEngine.executeRawDatabaseCommand( query, self._mail_queryAllCb )

	def _mail_queryAllCb( self, result, rows, insertid, errstr):
		"""
		查询所有邮件数据的回调函数。获得所有邮件数据之后，本地保留一份。同时把每封邮件的部分数据发送到客户端。
		所有邮件数据包括： 邮件DBID， 邮件标题， 邮件内容， 邮件包含物品， 邮件包含金钱， 寄信人的名字， 收信人的名字。
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if self.isDestroyed:
			return

		for m in result:
			mailItemDatas = [ m[3].decode("utf-8"), m[4].decode("utf-8"), m[5].decode("utf-8"), m[6].decode("utf-8") ]
			itemDatas = []
			for mailItemData in mailItemDatas:
				if mailItemData:
					itemDatas.append( json.loads( mailItemData ) )

			mailDict = {
				"id":int(m[0]),
				"title"		: m[1].decode("utf-8"),
				"content"	: m[2].decode("utf-8"),
				"itemList"	: itemDatas,
				"money"	: int( m[7] ),
				"senderName"	: m[8].decode("utf-8"),
				"receiverName"	: m[9].decode("utf-8"),
				"senderType"	: int( m[10] ),
				"receiveTime"	: int( m[11] ),
				"remainTime"	: int(int(m[11]) + csconst.MAIL_OUTTIMED - time.time()),
				"isRead"			: int(m[12]),
				"isUpper"		: int(m[13]), 				#是否为达到邮件上限的邮件标识
				"lingshi"			: int(m[14]),
				"xianshi"		: int(m[15]),
				"isTaken"		: 0,				# 用于临时记录当前是否正在拿取邮件
				"bindMoney"		: int(m[16])
			}
			mailData = g_mailDataInfo.createObjFromDict(mailDict)
			self.mail_allInfo[mailData.id] = mailData
		
		if self.checkAllMail():
			if len( self.mail_allInfo ):
				self.client.ReceiveAllMail( self.recordReceiverNames, list( self.mail_allInfo.values() )  )

	def checkAllMail( self ):
		"""
		检查所有邮件
		"""
		#超出邮件上限了
		#先删除过期邮件
		needDelMailIDs = []
		needToChangeUpperValueIDs = []
		overdueMail = [ i for i in self.mail_allInfo.values() if i.remainTime <= 0 ]
		for mail in overdueMail:
			del self.mail_allInfo[mail.id]
			needDelMailIDs.append(mail.id)
			
			#添加日志
			itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
			g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_TIME_ARRIVE)
			
		#再判断当前邮件数量
		if len( self.mail_allInfo ) <= csconst.MAIL_UPPER_LIMIT:
			for mailInfo in self.mail_allInfo.values():
				if mailInfo.isUpper:
					mailInfo.isUpper = 0
					needToChangeUpperValueIDs.append(mailInfo.id)

			#通知数据库删除邮件
			needDelMailIDStr = ", ".join([str(i) for i in needDelMailIDs])
			if needDelMailIDStr:
				query = "delete from custom_MailTable where id IN (%s)"%needDelMailIDStr
				KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
			#通知数据库修改邮件值
			changValueStr = ", ".join([str(i) for i in needToChangeUpperValueIDs])
			if changValueStr:
				mailQuery = "update custom_MailTable set sm_isUpper = 0 where id IN (%s)"%changValueStr
				KBEngine.executeRawDatabaseCommand( mailQuery, self.updateIsUpperValueCB )
			return True
		#如果还大于邮件上限值
		#分开  1.玩家没有超上限的邮件列表
		#	   2.玩家超过上限的邮件列表
		#
		mailList = [ i for i in self.mail_allInfo.values() if i.isUpper == 0 ]
		upperMailList = [ i for i in self.mail_allInfo.values() if i.isUpper > 0 ]
		upperMailList = sorted( upperMailList ,key = lambda m : m.receiveTime, reverse = False )
		mailList = sorted( mailList ,key = lambda m : m.receiveTime, reverse = False )
		for upperMail in upperMailList:
			if len(mailList) < csconst.MAIL_UPPER_LIMIT:
				mailList.append( upperMail )
				needToChangeUpperValueIDs.append(upperMail.id)
			elif len( mailList) > csconst.MAIL_UPPER_LIMIT:
				tempAmount = len( mailList )
				for mail in mailList:
					if len(mail.itemList) == 0 and mail.money == 0:
						mailList.remove(mail)
						needDelMailIDs.append( mail.id )
						if mail.id in needToChangeUpperValueIDs:
							needToChangeUpperValueIDs.remove(mail.id)
						
						#添加日志
						itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
						g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_BEREPLACED)
			
						break
				if tempAmount == len( mailList ):
					break
				else:
					mailList.append( upperMail )
					needToChangeUpperValueIDs.append(upperMail.id)
		
		self.mail_allInfo.clear()
		for mail in mailList:
			self.mail_allInfo[mail.id] = mail

		#通知数据库删除邮件
		needDelMailIDStr = ", ".join([str(i) for i in needDelMailIDs])
		if needDelMailIDStr:
			query = "delete from custom_MailTable where id IN (%s)"%needDelMailIDStr
			KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
		#通知数据库修改邮件值
		changValueStr = ", ".join([str(i) for i in needToChangeUpperValueIDs])
		if changValueStr:
			mailQuery = "update custom_MailTable set sm_isUpper = 0 where id IN (%s)"%changValueStr
			KBEngine.executeRawDatabaseCommand( mailQuery, self.updateIsUpperValueCB )
		return True

#----------------------------删除某邮件-------------------------------------------
	def mail_delete( self, mailIDs ):
		"""
		exposed method
		删除某封邮件邮件

		删除邮件除了到数据库中去删除之外，还要删除base里面的该封邮件信息。
		"""
		if not self.validateClientCall():
			return
		if len(mailIDs) == 0:
			self.statusMessage( csstatus.MAIL_DELETE_HAS_NOT_CHOICE,"" )
			return
		if len(mailIDs) == 1:
			self.deleteOneMail( int(mailIDs[0]) ) # 删除一封邮件
			return
		#删除多封邮件
		isHasAttachment = False  #是否有附件
		for mailID in mailIDs:
			if mailID not in self.mail_allInfo:
				continue
			mailInfo = self.mail_allInfo[mailID]
			if mailInfo.money or len(mailInfo.itemList):
				isHasAttachment = True
				break
		if isHasAttachment:
			self.inquireMessage( csstatus.MAIL_DELETE_HAS_ATTACHMENT,"","replyMail_delete",mailIDs )
		else:
			self.inquireMessage( csstatus.MAIL_DELETE,"","replyMail_delete",mailIDs )

	def deleteOneMail( self, mailID ):
		"""
		删除一封邮件
		"""
		if mailID not in self.mail_allInfo:
			KBEDebug.ERROR_MSG(" Delete One mail(ID = %i) is error"%mailID)
			return
		mailInfo = self.mail_allInfo[mailID]
		if not mailInfo.isRead: #该封邮件未阅读
			self.inquireMessage( csstatus.MAIL_DELETE_HAS_NOT_READ,"","replyOneMail_delete",mailID )
		else:
			if mailInfo.money or len( mailInfo.itemList ):# 已阅读但是含有附件
				self.statusMessage( csstatus.MAIL_DELETE_FORBID_ATTACHMENT,"" )
			else:
				self.replyOneMail_delete(1,mailID)

	def replyOneMail_delete( self, reply, mailID ):
		"""
		确定删除一封邮件
		"""
		if reply:
			if mailID not in self.mail_allInfo:
				return
			mail = self.mail_allInfo[mailID]
			del self.mail_allInfo[mailID]
			#添加日志
			itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
			g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_ACTIVE)

			query = "delete from custom_MailTable where id = %i"%mailID
			KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
			# 通知客户端删除数据
			self.client.OnMailDeleted( [mailID] )
			self.sendUpperMailToClient( 1 )

	def replyMail_delete( self, reply, mailIDs ):
		"""
		确定删除多封邮件
		"""
		if reply:
			tempArray = []
			for mailID in mailIDs:
				if mailID not in self.mail_allInfo:
					tempArray.append(mailID)
					continue
				mail = self.mail_allInfo[mailID]
				if mail.money or len(mail.itemList): #有附件的不删除
					tempArray.append(mailID)
					continue
				del self.mail_allInfo[mailID]
				
				#添加日志
				itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
				g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_ACTIVE)
				
			for mailID in tempArray:
				mailIDs.remove(mailID)
			if len(mailIDs) <= 0:
				return
			mailIDStr = ", ".join([str( i ) for i in mailIDs])
			query = "delete from custom_MailTable where id IN (%s)"%mailIDStr
			KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
			# 通知客户端删除数据
			self.client.OnMailDeleted(mailIDs)
			self.sendUpperMailToClient( len(mailIDs) )

	def _mail_deleteCb( self,  result, rows, insertid, errstr ):
		"""
		删除某封邮件回调函数
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)

#-----------------------------------------提取邮件--------------------------------
	def extractOneMail( self, mailID ):
		"""
		提取一封邮件
		"""
		if mailID not in self.mail_allInfo:
			KBEDebug.ERROR_MSG( "No such mailID! the id is: %i " % ( mailID ))
			return
		mailInfo = self.mail_allInfo[mailID]
		if mailInfo.money == 0 and len( mailInfo.itemList) == 0 \
		and mailInfo.lingshi == 0 and mailInfo.xianshi == 0 and mailInfo.bindMoney == 0:		# 该邮件没有金钱，灵石，仙石，物品
			self.statusMessage( csstatus.MAIL_HAS_NO_ITEM_EXTRACT )
			return
		if mailInfo.isTaken == 1: # 邮件正在提取
			KBEDebug.ERROR_MSG( "This has been Taken! the id is: %i " % ( mailID ) )
			return
		mailInfo.isTaken = 1
		
		if mailInfo.lingshi:
			if self.addLingShi(int(mailInfo.lingshi), csdefine.CHANGE_LINGSHI_BY_MAILL) == False:
				self.extractMailState( mailID, False )
				return
				
		if mailInfo.xianshi:
			if self.gainXianShi(int(mailInfo.xianshi), csdefine.CHANGE_XIANSHI_BY_MAILL) == False:
				self.extractMailState( mailID, False )
				return

		self.cell.extractMailCB(mailID, int(mailInfo.money),mailInfo.itemList, int(mailInfo.bindMoney))

		
		#添加日志
		itemDatas = [itemInst.getDictFromObj() for itemInst in mailInfo.itemList]
		g_logger.mailExtractLog(mailInfo.senderName, mailInfo.receiverName, mailInfo.senderType, mailInfo.title, mailInfo.money, itemDatas, mailID)

	def extractMailState( self, mailID, isSuccess ):
		"""
		玩家取得金钱物品后，到base来做确认。同时也会修改数据库。玩家的cell调用。
		"""
		if isSuccess:
			query = "update custom_MailTable set sm_item0 = '', sm_item1 = '', sm_item2='', sm_item3='', sm_money = 0, sm_lingshi = 0, sm_xianshi = 0, sm_bindMoney = 0  where id = %i"%mailID
			KBEngine.executeRawDatabaseCommand( query, self.extractMailStateCB )
			self.mail_allInfo[mailID].isTaken = 0
			self.mail_allInfo[mailID].money = 0
			self.mail_allInfo[mailID].itemList = []
			self.mail_allInfo[mailID].lingshi = 0
			self.mail_allInfo[mailID].xianshi = 0
			self.mail_allInfo[mailID].bindMoney = 0
			self.client.CLIENT_ExtractMailSuccess( str(mailID) )
			self.statusMessage(csstatus.MAIL_EXTRACT_SUCCESS)
		else:
			self.mail_allInfo[mailID].isTaken = 0

	def extractMailStateCB( self, result, rows, insertid, errstr ):
		"""
		"""
		pass

	def BASE_readedMailNotify( self, mailID ):
		"""
		exposed method
		邮件已阅读通知。此方法由客户端调用，告诉自己，某一封邮件已读过
		"""
		if not self.validateClientCall():
			return
		mailID = int(mailID)
		if mailID not in self.mail_allInfo:
			KBEDebug.ERROR_MSG( "No such mailID! the id is: %i " % ( mailID ))
			return

		mailInfo = self.mail_allInfo[mailID]
		if mailInfo.isRead == 1:
			KBEDebug.ERROR_MSG( "The mail has read! the id is: %i " % ( mailID ))
			return
		mailInfo.isRead = 1
		if mailInfo.senderType == csdefine.MAIL_SENDER_TYPE_PLAYER:
			self.addRecordReceiveName( mailInfo.senderName )
		query = "update custom_MailTable set sm_isRead = 1 where id = %i"%mailID
		KBEngine.executeRawDatabaseCommand( query,Functions.Functor(self.readedMailNotifyCb, mailID) )
		
		#添加日志
		itemDatas = [itemInst.getDictFromObj() for itemInst in mailInfo.itemList]
		g_logger.mailReadLog(mailInfo.senderName, mailInfo.receiverName, mailInfo.senderType, mailInfo.title, mailInfo.money, itemDatas, mailID)

	def readedMailNotifyCb( self, mailID,result, rows, insertid, errstr ):
		"""
		更新已阅读回调
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)

	def checkHasNoItemsMail( self, mailData ):
		"""
		检查所有邮件有没有附件的
		"""
		tempList = sorted( self.mail_allInfo.values(), key = lambda m : m.isRead, reverse = True ) #是否已读来排序
		if len(tempList) == 0:
			tempList = sorted( tempList, key = lambda m : m.receiveTime, reverse = False ) #剩余时间
		mailInfo = None
		isFind = False
		for temp in tempList:
			if (len(temp.itemList) == 0) and temp.money == 0:
				mailInfo = temp
				isFind = True
				break
		if isFind: #说明有已读未读或者时间 但是没有附件的邮件
			mail = self.mail_allInfo[mailInfo.id]
			del self.mail_allInfo[mailInfo.id]
			query = "delete from custom_MailTable where id = %i"%mailInfo.id
			KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
			# 通知客户端删除数据
			self.client.OnMailDeleted( [mailInfo.id] )
			mailData.isUpper = 0
			self.mail_allInfo[mailData.id] = mailData
			mailQuery = "update custom_MailTable set sm_isUpper = 0 where id = %i"%mailData.id
			KBEngine.executeRawDatabaseCommand( mailQuery, Functions.Functor(self.updateIsUpperValueCB,mailData.id) )
			self.client.ReceiveMail(mailData)
			
			#添加日志
			itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
			g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_BEREPLACED)
		else:
			self.statusMessage( csstatus.MAIL_FULL,"" )

	def updateIsUpperValueCB( self,result, rows, insertid, errstr  ):
		"""
		更新邮件是否上限值的回调
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)

	def BASE_timeToDelMail( self, mailID ):
		"""
		时间到达 强制删除邮件
		exposed mathod
		"""
		if not self.validateClientCall():
			return
		mailID = int(mailID)
		if mailID in self.mail_allInfo:
			mail = self.mail_allInfo[mailID]
			del self.mail_allInfo[mailID]
			# 通知客户端删除数据
			self.client.OnMailDeleted( [mailID] )
			self.sendUpperMailToClient(1)
			#添加日志
			itemDatas = [itemInst.getDictFromObj() for itemInst in mail.itemList]
			g_logger.mailRemoveLog(mail.senderName, mail.receiverName, mail.senderType, mail.title, mail.money, itemDatas, mail.id, LogDefine.LT_MAIL_DEL_TYPE_TIME_ARRIVE)
		query = "delete from custom_MailTable where id = %i"%mailID
		KBEngine.executeRawDatabaseCommand( query, self._mail_deleteCb )
		

	def sendUpperMailToClient( self, count ):
		"""
		发送达到上限的邮件到客户端
		"""
		query = "select id, sm_title, sm_content, sm_item0, sm_item1, sm_item2, sm_item3,sm_money, sm_senderName, sm_receiverName, sm_senderType,UNIX_TIMESTAMP(sm_receiveTime), sm_isRead,sm_isUpper, sm_lingshi, sm_xianshi, sm_bindMoney from custom_MailTable where sm_receiverName = '%s' and sm_isUpper = 1 and UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(sm_receiveTime) < %i order by sm_receiveTime asc limit %i" %(self.getName(),csconst.MAIL_OUTTIMED,count)
		KBEngine.executeRawDatabaseCommand( query, self._sendUpperMailToClientCB )

	def _sendUpperMailToClientCB( self, result, rows, insertid, errstr ):
		"""
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		if self.isDestroyed:
			return
		changeUpperValueIDs = []
		for m in result:
			itemDatas = []
			mailItemDatas = [ m[3].decode("utf-8"), m[4].decode("utf-8"), m[5].decode("utf-8"), m[6].decode("utf-8") ]
			for mailItemData in mailItemDatas:
				if mailItemData:
					itemDict = json.loads( mailItemData )
					itemDatas.append(itemDict)
					
			mailDict = {
				"id":int(m[0]),
				"title"			: m[1].decode("utf-8"),
				"content"		: m[2].decode("utf-8"),
				"itemList": itemDatas,
				"money"			: int( m[7] ),
				"senderName"	: m[8].decode("utf-8"),
				"receiverName"	: m[9].decode("utf-8"),
				"senderType"	: int( m[10] ),
				"receiveTime"	: int( m[11] ),
				"remainTime":int(int(m[11]) + csconst.MAIL_OUTTIMED - time.time()),
				"isRead":int(m[12]),
				"isUpper":0, 				#是否为达到邮件上限的邮件标识
				"lingshi":int(m[14]),
				"xianshi":int(m[15]),			
				"isTaken"		: 0,				# 用于临时记录当前是否正在拿取邮件
				"bindMoney"		: int(m[16])
			}
			mailData = g_mailDataInfo.createObjFromDict(mailDict)	
			changeUpperValueIDs.append(mailData.id)
			self.mail_allInfo[mailData.id] = mailData
			self.client.ReceiveMail( mailData )

		if not len(changeUpperValueIDs):
			return
		#通知数据库修改邮件值
		changValueStr = ", ".join([str(i) for i in changeUpperValueIDs])
		mailQuery = "update custom_MailTable set sm_isUpper = 0 where id IN (%s)"%changValueStr
		KBEngine.executeRawDatabaseCommand( mailQuery, self.updateIsUpperValueCB )

	def addRecordReceiveName( self, receiverName ):
		"""
		增加收信人的记录	
		"""
		if receiverName in self.recordReceiverNames:
			return
		if len(self.recordReceiverNames) >= csconst.MAIL_RECORD_RECEIVE_NAME_MAX:
			removeIndex = len(self.recordReceiverNames) - 1
			self.removeRecordReceiveName( removeIndex )

		self.recordReceiverNames.insert(0,receiverName)
		self.client.CLIENT_AddRecordReceiveName( receiverName )

	def removeRecordReceiveName( self, index ):
		"""
		删除收信人的记录
		"""
		if len(self.recordReceiverNames) > index:
			removeName = self.recordReceiverNames.pop(index)
			self.client.CLIENT_RemoveRecordReceiveName( removeName )

	