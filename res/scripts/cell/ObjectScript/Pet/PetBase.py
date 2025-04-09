# -*- coding: utf-8 -*-
#import KBEngine

#python
import random
#engine
import KBEngine
#script

import KBEDebug
from XiuweiLoader import g_XiuweiMgr
import ObjectScript.ObjectScriptBase.GameScript as GameScript
from ObjectScript.Pet import PetPropertyLoader

class PetBase( GameScript.GameScript, PetPropertyLoader.PetPropertyLoader ):
	"""
	宠物对象script类
	"""
	def __init__( self ):
		GameScript.GameScript.__init__( self )
		PetPropertyLoader.PetPropertyLoader.__init__( self )
	
	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		GameScript.GameScript.initData( self, data )
		PetPropertyLoader.PetPropertyLoader.initData(self,data)
		
	def createLocalEntity( self, params ) :
		"""
		创建entity
		"""
		return GameScript.GameScript.createLocalEntity( self, params )

	def onConjurePet( self, owner ):
		"""
		virtual method
		召唤出幻兽
		"""
		pass
		
	def onMountPet( self, owner ):
		"""
		virtual method
		骑宠状态
		"""
		pass