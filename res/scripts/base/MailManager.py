# -*- coding: utf-8 -*-


import KBEDebug
import KBEngine
from CoreObject import MgrPersistentObject
import time
import json
import Functions
import csstatus
import KST
import csconst
from MsgLogger import g_logger
import csdefine

SEND_MAIL_SQL = "insert into custom_MailTable ( sm_title, sm_content, sm_item0, sm_item1, sm_item2, sm_item3,sm_money, sm_bindMoney, sm_senderName, sm_receiverName, sm_senderType, sm_receiveTime, sm_timeFlag, sm_isRead,sm_isUpper, sm_lingshi, sm_xianshi) value ( '%s','%s','%s','%s','%s','%s', %i, %i, '%s','%s', %i, DATE_ADD(now(),INTERVAL %i SECOND), %i,%i,%i,%i,%i );"

class MailManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	邮件管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )

		# 在数据库中创建邮件表custom_MailTable
		self._createMailTable()
		self.waitToAddColumn = ["sm_lingshi","sm_xianshi", "sm_bindMoney"]
		self.alreadyAddColumn = []

	def _queryColumnToMailTable( self, columnName ):
		"""
		增加字段到 custom_MailTable
		"""
		# 存储过程
		# sql_drop = """DROP PROCEDURE IF EXISTS `CUSTOM_MAILTABLE_CHANGE`;"""

		# sql_create = """CREATE DEFINER=CURRENT_USER PROCEDURE `CUSTOM_MAILTABLE_CHANGE`()
		# 			BEGIN
		#  			SELECT @coumt1 = (select count(*) from information_schema.columns where table_name = 'custom_MailTable' and column_name = 'sm_lingshi');
		#  			IF (SELECT @coumt1 is Null) THEN
		# 				alter table custom_MailTable add column am_lingshi int(11) default 0;
		# 			END IF;
		# 			END;
		# 			"""

		query = "select count(*) from information_schema.columns where table_name = 'custom_MailTable' and column_name = '%s'"%columnName

		KBEngine.executeRawDatabaseCommand( query,  Functions.Functor(self._addFiledToMailTable, columnName) )

	def _addFiledToMailTable( self, columnName, result, rows, insertid, errstr ):
		"""
		增加某个字段
		"""
		if errstr:
			# 创建存储过程错误
			KBEDebug.ERROR_MSG("errstr++++++",errstr)
			return
		if int(result[0][0]) == 0:
			query = "alter table custom_MailTable add column %s int(11) default 0"%columnName
			KBEngine.executeRawDatabaseCommand( query,  Functions.Functor( self._addFiledIsInMailTableCb,columnName)  )
		else:
			self.alreadyAddColumn.append(columnName)
			if len( self.alreadyAddColumn ) == len(self.waitToAddColumn):
				self.onCompleteInit()

	def _addFiledIsInMailTableCb( self, columnName,result, rows, insertid, errstr ):
		"""
		增加某个字段回调
		"""
		if errstr:
			# 创建邮件数据表错误
			KBEDebug.ERROR_MSG(errstr)
			return
		self.alreadyAddColumn.append(columnName)
		if len( self.alreadyAddColumn ) == len(self.waitToAddColumn):
			self.onCompleteInit()

	def _createMailTable( self ):
		"""
		创建邮件数据表
		"""
		query = """CREATE TABLE IF NOT EXISTS `custom_MailTable` (
				  `id` bigint(20) unsigned NOT NULL auto_increment,
				  `sm_title` varchar(255) default '',
				  `sm_content` text,
				  `sm_item0` blob,
				  `sm_item1` blob,
				  `sm_item2` blob,
				  `sm_item3` blob,
				  `sm_money` bigint(20) default '0',
				  `sm_senderName` varchar(255) default '',
				  `sm_receiverName` varchar(255) default '',
				  `sm_senderType` tinyint(4) default '0',
				  `sm_receiveTime` timestamp NOT NULL default now(),
				  `sm_timeFlag` int(10) unsigned NOT NULL default '0',
				  `sm_isRead` tinyint(1) default '0',
				  `sm_isUpper` tinyint(1) default '0',
				  `sm_lingshi` int(11) default 0,
				  `sm_xianshi` int(11) default 0,
				  `sm_bindMoney` bigint(20) default '0',
				  PRIMARY KEY  (`id`),
				  KEY `index_receiverName` (`sm_receiverName`),
				  KEY `index_senderName` (`sm_senderName`)
				) ENGINE=InnoDB;"""

		KBEngine.executeRawDatabaseCommand( query, self._createMailTableCb )


	def _createMailTableCb( self, result, rows, insertid, errstr ):
		"""
		"""
		if errstr:
			# 创建邮件数据表错误
			KBEDebug.ERROR_MSG("Create custom_MailTable Fail!")
			return
		
		for columnName in self.waitToAddColumn:
			self._queryColumnToMailTable(columnName)

	def sendWithMailbox( self,senderMB, receiverBase, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi ):
		"""
		有收信者mailbox的发信（该mailbox可能为None，表示不在线），此功能主要用于可以直接找到发信者base mailbox的场合，以提高发信效率。
		过程：玩家寄出的邮件到达这里，就被直接存储到数据库中了。
		同时还会利用receiverBase来把这个信息通知收信人，让他读取新的邮件。
		senderMB: 发件人的MAILBOX，如果发信的是玩家，把玩家的mailbox写上有助于返回发信成功/失败的消息，如果是系统，可以置None
		receiverBase: 收件人的base
		receiverName: 收件人的名字
		senderType: 发送类型
		senderName: 发送者名字
		title：标题
		content：内容
		money：所携带的金钱
		bindMoney:绑定金钱
		itemDatas: 所携带的物品数据 [{},{}..]  {}:itemInst.getDictFromObj()
		lingshi: 所携带灵石
		xianshi: 所携带仙石
		"""
		#查询玩家邮件数量
		query = "select count(*) from custom_MailTable where sm_receiverName = '%s'"%receiverName
		KBEngine.executeRawDatabaseCommand( query,Functions.Functor(self._mail_queryCountForCheckCb,senderMB, receiverBase, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi) )

	def _mail_queryCountForCheckCb( self,senderMB, receiverBase, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi, resultSet, rows, insertid, errstr ):
		"""
		查询收件人邮件数目的回调函数
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			return
		isUpper = 0
		if int(resultSet[0][0]) + 1 > csconst.MAIL_UPPER_LIMIT:
			isUpper = 1
		itemDataListStr = []
		for itemData in itemDatas:
			itemDataListStr.append(json.dumps(itemData.getDictFromObj()))
		
		itemEmptyCount = 4 - len(itemDatas)
		if itemEmptyCount > 0:
			itemDataListStr.extend( [""] * itemEmptyCount )
		timeFlag = int(time.time())
		query = SEND_MAIL_SQL %(title, content, itemDataListStr[0], itemDataListStr[1], itemDataListStr[2], itemDataListStr[3], money, bindMoney, senderName, receiverName , senderType, 0, timeFlag,0,isUpper, lingshi, xianshi)
		KBEngine.executeRawDatabaseCommand( query, Functions.Functor( self._sendWithMailboxCB, senderMB, receiverBase, senderName, receiverName, senderType, title, itemDatas, money, bindMoney, timeFlag,isUpper, lingshi, xianshi ) )	# 记录到数据库

	def _sendWithMailboxCB( self, senderMB, receiverBase, senderName, receiverName, senderType, title, itemDatas, money, bindMoney, timeFlag,isUpper, lingshi, xianshi, resultSet, rows, insertid, errstr):
		"""
		玩家寄信的回调函数。
		附加的几个参数目的主要是当邮件记录到数据库失败的时候，我们可以看到是谁寄出的邮件，并且该邮件是否有物品和金钱。
		timeFlag: 用于查询过滤的标记
		"""
		if errstr:
			KBEDebug.ERROR_MSG(errstr)
			KBEDebug.ERROR_MSG("senderName %s send item an money is error"%senderName)
			return

		# 发信成功，通知在线的收件人
		if receiverBase:
			receiverBase.mail_newNotify(senderName, timeFlag)
		# 有发信人mailbox，通知发信人
		if senderMB and senderType == csdefine.MAIL_SENDER_TYPE_PLAYER:
			senderMB.addRecordReceiveName(receiverName)
			senderMB.statusMessage( csstatus.MAIL_SEND_SUCCESS, "" )
			if hasattr( senderMB, "client" ) and senderMB.client:
				senderMB.client.OnMailSendSuccess()
			
		#添加日志
		g_logger.mailSendLog(senderName, receiverName, senderType, title, money, bindMoney, itemDatas )

	def send(self, senderMB, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi):
		"""
		define method
		无目标mailbox发信。此功能一般用于不知道收信目标的base mailbox的发信功能。一般来说，使用此方法会比使用sendWithMailbox()的效率低。
		"""
		KST.g_baseAppEntity.lookupRoleBaseByName( receiverName,Functions.Functor(self._getPlayerMailboxForSendMailCb,senderMB, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi) )

	def _getPlayerMailboxForSendMailCb( self, senderMB, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi, target):
		"""
		没有目标mailbox发信模式的回调函数
		"""
		if target:
			self.sendWithMailbox( senderMB, target, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi) #目标在线
		else:
			self.sendWithMailbox( senderMB, None, receiverName, senderType, senderName, title, content, money, bindMoney, itemDatas, lingshi, xianshi)	#目标不在线

