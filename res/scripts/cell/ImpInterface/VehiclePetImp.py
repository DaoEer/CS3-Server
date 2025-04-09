# -*- coding: utf-8 -*-

# 幻兽数据使用原则：
#	以玩家身上的幻兽数据为基准，对幻兽数据的修改都必须先更新玩家的数据。然后玩家那边才分别更新到幻兽或者客户端

import KBEngine
import KBEDebug
import csconst
import Functions

from ObjectScript.Pet.PetFactory import g_petFactory

class VehiclePetImp(object):
	"""
	"""
	def __init__( self ):
		object.__init__( self )
		
	def getName( self ):
		""""""
		if self.name:
			return self.name
		petObject = g_petFactory.getObject( self.scriptID )
		if petObject:
			return petObject.getEntityProperty("uname", "")
		return ""
		
	def updateAttr( self, attrName, value ):
		"""
		更新属性
		"""
		setattr( self, attrName, value )
		
	def isSleepTime( self ):
		"""是否处于睡眠状态"""
		if self.sleepTime and self.sleepTime > Functions.getTime():
			return True
		return False
		