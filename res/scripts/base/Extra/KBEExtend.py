# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import Functions

def CreateMgrFromDB( mgrName ):
	"""
	使用这种创建方式，必需继承于MgrPersistentObject
	"""
	mgrTableName = "tbl_%s"%mgrName
	strSql = "SELECT `id` FROM %s WHERE `sm_mgrName`='%s'"%( mgrTableName, mgrName )
	KBEngine.executeRawDatabaseCommand( strSql, Functions.Functor( OnGetMgrDBID, mgrName ) )

def OnGetMgrDBID( mgrName, result, rows, insertid, errstr ):
	if errstr != None:
		ERROR_MSG(mgrName)
		ERROR_MSG( "Create Manager Error%s"%( errstr ) )
		return

	if result and len( result ):
		mgrDBID = int( result[ 0 ][ 0 ] )
		if mgrDBID > 0:
			KBEngine.createEntityFromDBID( mgrName, mgrDBID )
	else:
		mgr = KBEngine.createEntityLocally( mgrName, { "mgrName" : mgrName } )
		mgr.writeToDB()