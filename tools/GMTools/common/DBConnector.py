# -*- coding: utf-8 -*-
import os

import mysql.connector

class MyUTF8Converter(mysql.connector.conversion.MySQLConverter):
	def row_to_python(self, row, fields):
		row = super(MyUTF8Converter, self).row_to_python(row, fields)

		def to_unicode(col):
			if type(col) == bytearray:
				return col.decode('utf-8')
			return col

		return[to_unicode(col) for col in row]


class DBConnector(object):
	"""
	数据库连接器
	"""
	def __init__( self, *args, **kwargs ):
		"""
		"""
		kwargs.update({"converter_class":MyUTF8Converter})
		self.connector = mysql.connector.connect( *args, **kwargs )
		self.connector.autocommit = True
		
	def close(self):
		"""
		"""
		self.connector.close()
		
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
					#print( "mysql was not connected! write log error:", sql_cmd )
					#print( str(args) )
					return
				continue

		if len(args)==0:
			cursor.execute(sql_cmd)
		elif len(args) == 1:
			cursor.execute( sql_cmd, args[0])
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
					#print( "mysql was not connected! write log error:", sql_cmd )
					return
				continue
				
		cursor.execute( sql_cmd )
		results=cursor.fetchall()
		self.connector.commit()
		return results

		