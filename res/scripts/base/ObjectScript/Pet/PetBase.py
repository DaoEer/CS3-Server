# -*- coding: utf-8 -*-
#import KBEngine


"""
usage:
	怪物对象script类

attribute:
	objectType

member function:
	getObjectType
	getName

callback:
	pass

"""


#python
import random
#engine
import KBEngine
#script

import KBEDebug
from XiuweiLoader import g_XiuweiMgr
import ObjectScript.ObjectScriptBase.GameScript as GameScript
from ObjectScript.Pet import PetPropertyLoader

class PetBase( PetPropertyLoader.PetPropertyLoader, GameScript.GameScript ):
	"""
	怪物对象script类
	"""
	def __init__( self ):
		PetPropertyLoader.PetPropertyLoader.__init__( self )
		GameScript.GameScript.__init__( self )
		self.passiveSkills = ""
		
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

	def getSkillIDByQualityAndStep( self, quality, step ):
		"""根据品质和介次获取技能ID"""
		skillIDs = []
		if quality in self._skillIDs:
			if step in self._skillIDs[quality]:
				skillIDs.append( self._skillIDs[quality][step] )
		return skillIDs
			
	def getPassiveSkill( self, quality ):
		"""获取出生被动技能"""
		passiveSkillList = self.passiveSkills.split("|")
		if len(passiveSkillList) >= quality and passiveSkillList[quality-1]:
			return int( passiveSkillList[quality-1])
		else:
			return 0

	def getNoLearnedSkillID( self, quality, step ):
		"""根据品质和介次获取未学习技能ID"""
		noLearneskillIDs = []
		if quality in self._skillIDs:
			for i in self._skillIDs[quality]:
				if i > step:
					noLearneskillIDs.append( self._skillIDs[quality][i] )
		return noLearneskillIDs
