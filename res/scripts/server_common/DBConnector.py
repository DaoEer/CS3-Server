# -*- coding: utf-8 -*-
import os
import KBEngine
import Settings
from KBEDebug import *

import mysql.connector
import MysqlUtility


class DBConnector(object):
	"""
	数据库连接器
	"""
	def __init__( self, *args, **kwargs ):
		"""
		"""
		self.connector = mysql.connector.connect( *args, **kwargs )
		self.autocommit = True
		
	'''phw: 废弃，因为有更好的方案
	def insertInto( self, tableName, columnNames, values ):
		"""
		@param tableName: 库名.表名（例：union_game_log.enter_dist_log）
		@param columnNames: list；表字段名列表。格式：(column1, column2, ...)
		@param values: list of tuple；值，值的个数必须与columnNames匹配。例：[(value1, value2, ...), (value1, value2, ...)]
		"""
		# make value to strings like as [ "( 'v1', v2, ... )", ... ]
		mtm = b"( " + b", ".join( (b"%s",) * len( columnNames ) ) + b" )"
		ps = [ MysqlUtility.makeSafeSql( mtm, params ) for params in values ]
		
		# make column names to string like as "(`column1`, `column2`, ...)"
		clumns = "( " + ", ".join( ("`%s`",) * len( columnNames ) ) + " )"
		clumns = clumns % tuple( columnNames )
		
		# make full sql
		sql = b"insert into `%s` %s values %s" % ( clumns.encode("utf-8"), b", ".join( ps ) )
		
		cursor = self.connector.cursor()
		cursor.execute( sql )
		self.connector.commit()
	'''

	def execute( self, sql_cmd, *args ):
		"""
		"""
		tryCount = 0
		while tryCount <= 1:
			try:
				cursor = self.connector.cursor()
				break
			except mysql.connector.OperationalError:
				cursor = None
				tryCount += 1
				# 每1秒重试一次，共10次
				try:
					self.connector.reconnect(10, 1.0)
				except mysql.connector.InterfaceError:
					print( "mysql was not connected! write log error:", sql_cmd )
					print( str(args) )
					return
				continue


		if len(args) == 1:
			cursor.execute( sql_cmd, args[0] )
		else:
			cursor.executemany( sql_cmd, args )
		
		self.connector.commit()
		
	def select( self, sql_cmd ):
		"""
		查询
		"""
		tryCount = 0
		while tryCount <= 1:
			try:
				cursor = self.connector.cursor()
				break
			except mysql.connector.OperationalError:
				cursor = None
				tryCount += 1
				# 每1秒重试一次，共10次
				try:
					self.connector.reconnect(10, 1.0)
				except mysql.connector.InterfaceError:
					print( "mysql was not connected! write log error:", sql_cmd )
					return
				continue
				
		cursor.execute( sql_cmd )
		results=cursor.fetchall()
		self.connector.commit()
		return results

		