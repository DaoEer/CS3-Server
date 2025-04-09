# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
import threading, traceback, logging

import Settings
from DBConnector import DBConnector

logging.basicConfig(**Settings.logger_except_file)

"""
"""

def LOCAL_EXCEHOOK_MSG( *args ) :
	"""
	输出当前栈帧错误信息，常用于输出异常信息
	不用KBEDebug.EXCEHOOK_MSG()的原因，是因为在子线程下直接print()的消息底层捕捉不到（或者说没有去捕捉）
	"""
	exceInfo = sys.exc_info()
	if exceInfo is None or exceInfo == ( None, None, None ) :
		logging.error( "no exception in stack!" )
	else :
		logging.error( "EXCEHOOK_MSG: " )
		for arg in args :
			logging.error( str( arg ) )
		tb = traceback.format_exception(*exceInfo)
		for e in tb:
			logging.error( e )


class LogProcesserManager(object):
	"""
	"""
	_instance = None
	
	def __init__( self ):
		"""
		"""
		# 记录特定类型的日志对应特定的处理器
		self.type2processer = {}
	
	@staticmethod
	def instance():
		if not LogProcesserManager._instance:
			LogProcesserManager._instance = LogProcesserManager()
		return LogProcesserManager._instance
	
	def registerType( self, type, processer ):
		"""
		注册一个类型的日志处理器，当前一个类型仅能注册一次（即只一种类型只能有一个处理器）。
		"""
		assert type not in self.type2processer, "one type can only register once times."
		self.type2processer[type] = processer
	
	def mtOnReceiveLog( self, log ):
		"""
		see also: KST.onLogWrote()
		"""
		logSegments = log.split(b"mysql$")
		if len( logSegments ) < 2:
			return
		#因为日志中可能有多个$字符，所以需要从前面开始解析$
		firstIndex = logSegments[1].find(b"$")
		if firstIndex != -1:
			type = int(logSegments[1][:firstIndex])
			logSegment = logSegments[1][firstIndex + 1:].split(b"||")
		else:
			ERROR_MSG( "Log error '%s'" % logSegments[1] )
		#INFO_MSG( "%s" % logSegment )
		if type in self.type2processer:
			self.type2processer[type].mtOnReceiveLog( logSegment )
		else:
			ERROR_MSG( "Unknown log type '%s'" % type )

	def mtIsReadyForShutDown( self ):
		"""
		"""
		for processer in self.type2processer.values():
			if not processer.mtIsReadyForShutDown():
				return False
		return True







class LogProcesser(object):
	"""
	日志处理基类
	"""
	# 日志的类型，每一类日志管理器都需要重新设置这个值
	LOG_TYPE = b""
	
	def __init__( self, manager ):
		"""
		@param manager: 日志管理器实例
		"""
		manager.registerType( self.LOG_TYPE, self )

		# 主线日志队列，由主线程负责操作，符合规则的日志都会放到这里
		self.mtLogQueue = []
		
		# 由主线程设置并由子线程重置的队列，以去掉对线程锁的需求
		self.tmpLogQueue = None
		
		# 是否启动中
		self.thread = None

	def mtIsReadyForShutDown( self ):
		"""
		virtual method.
		判断是否能shutdown了
		"""
		# 如果没有线程运行，并且self.tmpLogQueue为None，且self.mtLogQueue也无值了，
		# 则表示所有的日志都已成功写入数据库，既然如此，自然就可以安心shutdown了
		return self.thread is None and self.tmpLogQueue is None and not self.mtLogQueue

	def mtOnReceiveLog( self, logSegment ):
		"""
		virtual method.
		see also: KST.onLogWrote()
		"""
		#assert logSegment[0] == self.LOG_TYPE
		
		self.mtLogQueue.append( logSegment )
		self.checkAndWrite()

	def checkAndWrite( self ):
		"""
		"""
		# 如果self.tmpLogQueue为None，则表示子线程已经取走了正在缓存的数据
		# 因此需要把当前的数据放到self.tmpLogQueue中，以让子线程继续处理
		if self.tmpLogQueue is None and self.mtLogQueue:
			self.tmpLogQueue = self.mtLogQueue
			self.mtLogQueue = []
			if self.thread is None:
				self.thread = threading.Thread( target = self.stRun )
				self.thread.start()
				KBEngine.addTimer( 0.1, 0.1, self.mtOnTimeToCheckSubThread )

	def mtOnTimeToCheckSubThread( self, timerID ):
		"""
		检查线程工作是否完成。
		为什么要检查：因为只有timer在不停运行，子线程才有cpu资源运行
		"""
		#print( "onTimeToCheckSubThread(), " )
		if self.thread is None:
			# 必须先把自己的timer停掉，如果还有数据要写，
			# self.checkAndWrite()会自动増加timer
			KBEngine.delTimer( timerID )
			
			# 由于多线程的原因，我们需要再次检测，以保证在没有新的日志来临时，
			# self.mtLogQueue下的日志能够得到正确的写入
			self.checkAndWrite()

	def stRun( self ):
		"""
		线程运行函数
		"""
		#print( "LogProcesser::stRun(), start" )
		while self.tmpLogQueue is not None:
			logQueue = self.tmpLogQueue
			self.tmpLogQueue = None
			
			try:
				self.onSaveLog( logQueue )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(logQueue) )
			
		# 结束的时候设置标志
		self.thread = None
		#print( "LogProcesser:stRun(), over" )

	def onSaveLog( self, logQueue ):
		"""
		template method.
		要求存储日志的接口。
		
		@param logQueue: 分割后的日志队列
		"""
		print( 'LogProcesser::onSaveLog: un-implement!!!' )




class CenterLogProcesser( LogProcesser ):
	def __init__( self, manager ):
		super(CenterLogProcesser, self).__init__(manager)
		self.dbc = DBConnector( **Settings.DB_GAME_LOG_CSOL )

class LogIconStart( CenterLogProcesser ):
	"""
	CREATE TABLE `log_icon_start` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `client_model` varchar(20) NOT NULL COMMENT '设备型号',
	  `mac` varchar(100) NOT NULL COMMENT 'MAC地址',
	  `imei` varchar(100) NOT NULL COMMENT '移动设备识别码',
	  `ifa` varchar(100) NOT NULL COMMENT 'iOS广告标识符',
	  `ifv` varchar(100) NOT NULL COMMENT 'iOS厂商标识符',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏启动日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 用户启动游戏时记录的日志 */
	"""
	LOG_TYPE = b"log_icon_start"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, client_model, mac, imei, ifa, ifv = log
			values.append( (create_time, gyyx_lf, client_model, mac, imei, ifa, ifv) )
			
		sql = "insert into `log_icon_start` (`create_time`, `gyyx_lf`, `client_model`, `mac`, `imei`, `ifa`, `ifv`) values (%s, %s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class LogAccountLogin( CenterLogProcesser ):
	"""
	CREATE TABLE `log_account_login` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `login_type` int(11) NOT NULL COMMENT '类型(1:登录, 0:登出)',
	  `online_sec` int(11) NOT NULL COMMENT '在线时长',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号登录/登出日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 用户登录/登出帐号时记录的日志 */
	"""
	LOG_TYPE = b"log_account_login"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, account_id, login_type, online_sec = log
			try:
				values.append( (create_time, gyyx_lf, account_id, int(login_type), int(online_sec)) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `log_account_login` (`create_time`, `gyyx_lf`, `account_id`, `login_type`, `online_sec`) values (%s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )












class GameLogProcesser( LogProcesser ):
	def __init__( self, manager ):
		super(GameLogProcesser, self).__init__(manager)
		
		self.dbc = DBConnector( **Settings.DB_GAME_LOG )


class EnterDistLog( GameLogProcesser ):
	"""
	CREATE TABLE `enter_dist_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `login_type` int(11) NOT NULL COMMENT '类型（1:登录, 0:登出）',
	  `online_sec` int(11) NOT NULL COMMENT '在线时长',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='区服登录/登出日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 玩家登录（选择指定区服，进入区服时）/登出区服时记录的日志 */
	"""
	LOG_TYPE = b"enter_dist_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, login_type, online_sec = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, int( login_type ), int( online_sec ), create_time) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `enter_dist_log` (`gyyx_lf`, `dist_id`, `account_id`, `login_type`, `online_sec`, `create_time`) values (%s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class EnterSceneLog( GameLogProcesser ):
	"""
	CREATE TABLE `enter_scene_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `role_id` varchar(30) NOT NULL COMMENT '角色ID',
	  `role_lv` int(11) NOT NULL COMMENT '角色等级',
	  `login_type` int(11) NOT NULL COMMENT '类型（1:登录, 0:登出）',
	  `online_sec` int(11) NOT NULL COMMENT '在线时长',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='主场景登录/登出日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 玩家登录（选择指定角色，进入游戏时）/登出主场景时记录的日志 */
	"""
	LOG_TYPE = b"enter_scene_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, login_type, online_sec, role_id, role_lv = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, int( login_type ), int( online_sec ), create_time, role_id, int( role_lv )) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `enter_scene_log` (`gyyx_lf`, `dist_id`, `account_id`, `login_type`, `online_sec`, `create_time`, `role_id`, `role_lv`) values (%s, %s, %s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class OnlineLog( GameLogProcesser ):
	"""
	CREATE TABLE `online_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号在线日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 记录当前在线的玩家账号，需每五分钟内记录一次，可由服务器统一记录，亦可针对每个玩家单独记录。 */
	"""
	LOG_TYPE = b"online_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, create_time) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `online_log` (`gyyx_lf`, `dist_id`, `account_id`, `create_time`) values (%s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class LevelLog( GameLogProcesser ):
	"""
	CREATE TABLE `level_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `role_id` varchar(30) NOT NULL COMMENT '角色ID',
	  `role_lv` int(11) NOT NULL COMMENT '角色等级',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色升级日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 玩家角色升级时记录的日志 */
	"""
	LOG_TYPE = b"level_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, role_id, role_lv = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, create_time, role_id, int( role_lv )) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `level_log` (`gyyx_lf`, `dist_id`, `account_id`, `create_time`, `role_id`, `role_lv`) values (%s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class CreditLog( GameLogProcesser ):
	"""
	CREATE TABLE `credit_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `role_id` varchar(30) NOT NULL COMMENT '角色ID',
	  `role_lv` int(11) NOT NULL COMMENT '角色等级',
	  `money` int(11) NOT NULL COMMENT '充值金额（人民币）',
	  `order_no` varchar(100) NOT NULL COMMENT '订单号',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间（订单成功时间）',
	  KEY `create_time` (`create_time`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='充值日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/* 玩家充值成功时记录的日志 */
	"""
	LOG_TYPE = b"credit_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, role_id, role_lv, money, order_no = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, create_time, role_id, int( role_lv ), int( money ), order_no) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `credit_log` (`gyyx_lf`, `dist_id`, `account_id`, `create_time`, `role_id`, `role_lv`, `money`, `order_no`) values (%s, %s, %s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class CostLog( GameLogProcesser ):
	"""
	CREATE TABLE `cost_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `role_id` varchar(30) NOT NULL COMMENT '角色ID',
	  `role_lv` int(11) NOT NULL COMMENT '角色级别',
	  `cost_type` varchar(30) NOT NULL COMMENT '消费类型（中文，例如：金币、元宝）',
	  `cost_name` varchar(100) NOT NULL COMMENT '消费名称（中文，例如：购买武器）',
	  `money` int(11) NOT NULL COMMENT '消费金额',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`),
	  KEY `cost_type` (`cost_type`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='消费日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/*
	玩家在游戏中进行消费时记录的日志。
	该表中可能出现的“消费类型（cost_type列值）”及“消费名称（cost_name列值）”，
	需要您填写至《联运日志表枚举值清单》。
	*/
	"""
	LOG_TYPE = b"cost_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, role_id, role_lv, cost_type, cost_name, money = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, create_time, role_id, int( role_lv ), cost_type, cost_name, int( money )) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `cost_log` (`gyyx_lf`, `dist_id`, `account_id`, `create_time`, `role_id`, `role_lv`, `cost_type`, `cost_name`, `money`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

class PlayLog( GameLogProcesser ):
	"""
	CREATE TABLE `play_log` (
	  `gyyx_lf` varchar(64) NOT NULL COMMENT '生命指纹',
	  `dist_id` int(11) NOT NULL COMMENT '区服ID',
	  `account_id` varchar(30) NOT NULL COMMENT '账号ID',
	  `role_id` varchar(30) NOT NULL COMMENT '角色ID',
	  `role_lv` int(11) NOT NULL COMMENT '角色等级',
	  `t_type` varchar(30) DEFAULT NULL COMMENT '玩法类型（中文，例如：任务、副本）',
	  `t_name` varchar(100) NOT NULL COMMENT '玩法名称（中文，例如：新手任务）',
	  `op_type` int(11) NOT NULL COMMENT '状态（1:进入, 2:成功, 3:失败）',
	  `use_time` int(11) NOT NULL COMMENT '完成耗时（秒）',
	  `create_time` datetime NOT NULL COMMENT '日志创建时间',
	  KEY `create_time` (`create_time`),
	  KEY `t_type` (`t_type`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='玩法日志表'
	/*!50500 PARTITION BY RANGE  COLUMNS(create_time)
	(PARTITION __max VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
	/*
	玩家在游戏中开始/结束某种玩法时记录的日志。
	该表中可能出现的“玩法类型（t_type列值）”及“玩法名称（t_name列值）”，
	需要您填写至《联运日志表枚举值清单》。
	*/
	"""
	LOG_TYPE = b"play_log"

	def onSaveLog( self, logQueue ):
		"""
		"""
		values = []
		for log in logQueue:
			_, create_time, gyyx_lf, dist_id, account_id, role_id, role_lv, t_type, t_name, op_type, use_time = log
			try:
				values.append( (gyyx_lf, int( dist_id ), account_id, create_time, role_id, int( role_lv ), t_type, t_name, int(op_type), int(use_time)) )
			except Exception:
				LOCAL_EXCEHOOK_MSG( str(log) )
				continue
			
		sql = "insert into `play_log` (`gyyx_lf`, `dist_id`, `account_id`, `create_time`, `role_id`, `role_lv`, `t_type`, `t_name`, `op_type`, `use_time`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		self.dbc.execute( sql, *values )

g_logProcesser = LogProcesserManager.instance()
