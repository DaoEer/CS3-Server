# -*- coding: utf-8 -*-

"""
write by penghuawei
自定义表格行实例
"""
import functools

import KBEngine
from KBEDebug import *
import MysqlUtility

class CustomTableField( object ):
	"""
	表字段定义
	"""
	def __init__( self, name, type, decodeType = "utf-8" ):
		"""
		@param name: field name
		@param type: field type, useful to convert str data to specify python data type.exp: int, float, ...
		"""
		self.name = name
		self.type = type
		self.decodeType = decodeType
	
	def convertToPython( self, value ):
		"""
		转换数据库数据为python类型
		"""
		if value is None:
			return self.type()  # return default value
			
		if self.type == str :
			return value.decode( self.decodeType )
		
		return self.type( value )


class CustomTable(object):
	"""
	"""
	# what name's attr is identify key
	_main_key_ = "id"
	_tbl_name_ = ""
	
	# key = attr name; value = instance of CustomTableField that include field name and field type
	# example: { "id" : CustomTableField( "id", int ), "name" : CustomTableField( "sm_name", str ), "speed" : CustomTableField( "sm_speed", float ) }
	_tbl_field_ = {
	
	}

	def __init__( self ):
		"""
		"""
		for k, v in self._tbl_field_.items():
			setattr( self, k, v.type() )

	@classmethod
	def get_field_def( SELF, attrName ):
		"""
		"""
		return SELF._tbl_field_[attrName]

	@classmethod
	def get_field_name( SELF, attrName ):
		"""
		"""
		return SELF._tbl_field_[attrName].name

	@classmethod
	def get_main_key_name( SELF ):
		"""
		"""
		return SELF._tbl_field_[SELF._main_key_].name

	def get_main_key_value( self ):
		"""
		"""
		return getattr( self, self._main_key_ )

	def deleteFromDB( self, callback = None ):
		"""
		从服务器中把与自己有关的数据删除
		"""
		self.deleteWithKey( self._main_key_, self.get_main_key_value() )

	def updateToDB( self, callback = None, **kw ):
		"""
		@param kw: key = table field name, value = value
		"""
		if self._main_key_ in kw:
			raise KeyError( "The main key '%s' value can't change!" % self._main_key_ )
		
		paramsKey = []
		paramsVal = []
		for k, v in kw.items():
			paramsKey.append( "{} = %s".format( self.get_field_name(k) ) )
			paramsVal.append( v )
		
		paramsVal.append( self.get_main_key_value() )
		cmd = "update {} set {} where {} = %s".format( self._tbl_name_, ", ".join( paramsKey ), self.get_main_key_name() )
		
		cmd = MysqlUtility.makeSafeSql( cmd, paramsVal )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( self._executeRawSqlCallback, cmd, callback ) );

	def updateAllToDB( self, callback = None ):
		"""
		把当前所有数据写入到数据库中。
		注意：如果self.databaseID是无效的值，那么将会出现异常
		@param callback:  This optional argument is a callable object that will be called when the response from the database is received. 
		It takes two arguments. The first is a boolean indicating success or failure and the second is the instance of class of HeroData
		"""
		if getattr( self, self._main_key_, 0 ) <= 0:
			raise ValueError( "identify key must big than 0; %s" % self.get_main_key_value( self._main_key_ ) )
		
		d = {}
		for k in self._tbl_field_:
			if k == self._main_key_: continue
			d[k] = self.__dict__[k]

		self.updateToDB( callback, **d )

	def _executeRawSqlCallback( self, cmd, callback, result, rows, insertid, error ):
		"""
		原生sql执行完毕后的回调
		"""
		if error is None:
			if callable( callback ):
				callback( True, self )
		else:
			ERROR_MSG( "%s::_executeRawSqlCallback(), execute raw sql '%s' fault!!!; error: %s" % ( self.__class__.__name__, cmd, error ) )
			if callable( callback ):
				callback( False, self )

	def insertToDB( self, callback = None ):
		"""
		把数据全部写入到数据库中。
		注：插入到数据库中的数据并不会自动更新dbid，这个需要上层使用者自己想办法更新。
		"""
		#if self.get_main_key_value() > 0:
		#	raise KeyError( "Can't re-insert data to db! %s = '%s'" % ( self.get_main_key_name(), self.get_main_key_value() ) )
		
		fieldNames = []
		fieldValues = []
		fieldValuesP = []
		for k in self._tbl_field_:
			fieldNames.append( self.get_field_name(k) )
			fieldValues.append( self.__dict__[k] )
			fieldValuesP.append( "%s" )
		
		cmd = "insert into {} ( {} ) values ( {} )".format( self._tbl_name_, ", ".join( fieldNames ), ", ".join( fieldValuesP ) )
		
		cmd = MysqlUtility.makeSafeSql( cmd, fieldValues )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( self._insertToDBCallback, cmd, callback ) );

	def _insertToDBCallback( self, cmd, callback, result, rows, insertid, error ):
		"""
		"""
		if error is not None:
			ERROR_MSG( "%s::_insertToDBCallback(), execute raw sql '%s' fault!!!; error: %s" % ( self.__class__.__name__, cmd, error ) )
			if callable( callback ):
				callback( False, self )
			return
		
		if callable( callback ):
			callback( True, self )

	@classmethod
	def deleteWithKey( SELF, whereKey, whereValue, callback = None ):
		"""
		使用指定的键值一次性删除多条记录
		"""
		if whereKey in SELF._tbl_field_:
			whereKey = SELF.get_field_name( whereKey )

		if isinstance( whereValue, (list, tuple) ):
			p = ", ".join(("%s",) * len(whereValue))
			cmd = "delete from {} where {} in ({})".format( SELF._tbl_name_, whereKey, p )
			cmd = MysqlUtility.makeSafeSql( cmd, whereValue )
		else:
			cmd = "delete from {} where {} = %s".format( SELF._tbl_name_, whereKey )
			cmd = MysqlUtility.makeSafeSql( cmd, (whereValue, ) )

		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( SELF._s_executeRawSqlCallback, cmd, callback ) );
	
	@classmethod
	def _s_executeRawSqlCallback( SELF, cmd, callback, result, rows, insertid, error ):
		"""
		原生sql执行完毕后的回调
		"""
		if error is None:
			if callable( callback ):
				callback( True )
		else:
			ERROR_MSG( "%s::_executeRawSqlCallback(), execute raw sql '%s' fault!!!; error: %s" % ( SELF.__name__, cmd, error ) )
			if callable( callback ):
				callback( False )

	@classmethod
	def queryAll( SELF, callback = None ):
		"""
		获得所有
		"""
		attrs = list( SELF._tbl_field_ )
		fields = [ SELF.get_field_name(e) for e in attrs ]
		queryField = ", ".join( fields )
		cmd = "select {} from {}".format( queryField, SELF._tbl_name_ )
		cmd = MysqlUtility.makeSafeSql( cmd )
		#DEBUG_MSG( "%s::queryWithKey(), %s" % (SELF.__name__, cmd) )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( SELF._queryWithKeyCallback, cmd, attrs, callback ) )

	@classmethod
	def queryWithKeys( SELF, callback = None, logicAnd = True, **kw ):
		"""
		@param logicAnd: bool, key之间是否是"and"的关系，false则表示"or"的关系
		@param kw: key = table field name, value = value
		"""
		if len( kw ) == 0:
			ERROR_MSG( "%s::queryWithKeys(), no key found! kw = {}" % ( SELF.__name__ ) )
			return
			
		logic = logicAnd and " and " or " or "
			
		fieldDict = {}
		for k, v in kw.items():
			fieldDict[SELF.get_field_name(k)] = v
		
		params = []
		values = []
		for key, value in fieldDict.items():
			params.append( "{} = %s".format( key ) )
			values.append( value )
		
		attrs = list( SELF._tbl_field_ )
		fields = [ SELF.get_field_name(e) for e in attrs ]
		queryField = ", ".join( fields )
		
		cmd = "select {} from {} where {}".format( queryField, SELF._tbl_name_, logic.join( params ) )
		cmd = MysqlUtility.makeSafeSql( cmd, values )
		#DEBUG_MSG( "%s::queryWithKeys(), %s" % (SELF.__name__, cmd) )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( SELF._queryWithKeyCallback, cmd, attrs, callback ) )


	@classmethod
	def queryWithKey( SELF, whereKey, whereValue, callback = None ):
		"""
		callback( success, instanceOfCustomTable )
		"""
		if whereKey in SELF._tbl_field_:
			whereKey = SELF.get_field_name( whereKey )
			
		attrs = list( SELF._tbl_field_ )
		fields = [ SELF.get_field_name(e) for e in attrs ]
		queryField = ", ".join( fields )
		cmd = "select {} from {} where {} = %s".format( queryField, SELF._tbl_name_, whereKey )
		cmd = MysqlUtility.makeSafeSql( cmd, (whereValue, ) )
		#DEBUG_MSG( "%s::queryWithKey(), %s" % (SELF.__name__, cmd) )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( SELF._queryWithKeyCallback, cmd, attrs, callback ) )

	@classmethod
	def queryLessThanKey( SELF, whereKey, whereValue, callback = None  ):
		"""
		callback( success, instanceOfCustomTable )
		"""			
		if whereKey in SELF._tbl_field_:
			whereKey = SELF.get_field_name( whereKey )
			
		attrs = list( SELF._tbl_field_ )
		fields = [ SELF.get_field_name(e) for e in attrs ]
		queryField = ", ".join( fields )
		cmd = "select {} from {} where {} <= %s".format( queryField, SELF._tbl_name_, whereKey )
		cmd = MysqlUtility.makeSafeSql( cmd, (whereValue, ) )
		KBEngine.executeRawDatabaseCommand( cmd, functools.partial( SELF._queryWithKeyCallback, cmd, attrs, callback ) )
	
	@classmethod
	def _queryWithKeyCallback( SELF, cmd, fields, callback, result, rows, insertid, error ):
		"""
		"""
		if error is not None:
			ERROR_MSG( "%s::_executeRawSqlCallback(), execute raw sql '%s' fault!!!; error: %s" % ( SELF.__name__, cmd, error ) )
			if callable( callback ):
				callback( False, None )
			return
		
		#DEBUG_MSG( "%s::_executeRawSqlCallback(), cmd: |%s|, result: |%s|" % ( SELF.__name__, cmd, result ) )
		tbls = []
		for row in result:
			t = SELF()
			for i, key in enumerate( fields ):
				setattr( t, key, SELF.get_field_def( key ).convertToPython(  row[i] ) )
			tbls.append( t )
		
		if callable( callback ):
			callback( True, tbls )
		






class TestTable( CustomTable ):
	"""
	测试用
	"""
	_main_key_ = "databaseID"
	_tbl_name_ = "tbl_TestTable"
	
	# key = attr name; value = instance of CustomTableField that include field name and field type
	# example: { "id" : CustomTableField( "id", int ), "name" : CustomTableField( "sm_name", str ), "speed" : CustomTableField( "sm_speed", float ) }
	_tbl_field_ = {
		"databaseID"            : CustomTableField( "id", int ),
		"i1"                    : CustomTableField( "sm_i1", int ),
		"i2"                    : CustomTableField( "sm_i2", int ),
		"s1"                    : CustomTableField( "sm_s1", str ),
		"s2"                    : CustomTableField( "sm_s2", str ),

	}

"""
CustomTable.TestTable.queryWithKeys( None, False, s1 = "abc", i1 = 100 )
"""
