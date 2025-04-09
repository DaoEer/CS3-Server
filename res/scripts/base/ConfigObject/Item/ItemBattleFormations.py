# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemBase as ItemBase
import Functions
import csstatus
import Math
import KBEMath

class ItemBattleFormations( ItemBase.ItemBase ):
	"""
	阵图
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
		self.actCosume = 0							# 激活消耗
		self.perCosume = 0							# 持续消耗（每分钟）
		self.insScriptID  = ""						# 在洞府召唤的scriptID
		self.outScriptID = ""						# 在洞府外召唤的护罩scriptID
		self.outObjectHP = 0						# 护罩的血量
		self.useSpace = ""							# 在固定地图使用
		self.outSpace = ""							# 洞府外的spaceScriptID
		self.insPos = (0,0,0)						# 洞府创建entity的Pos
		self.insDir = (0,0,0)						# 洞府创建entity的朝向
		
		cosumes = srcData["Param1"].split("|")
		self.actCosume = int(cosumes[0]) if cosumes else 0
		self.perCosume = int(cosumes[1]) if len(cosumes) >= 2 else 0
		
		scriptIDs = srcData["Param2"].split("|")
		self.insScriptID = scriptIDs[0] if scriptIDs else ""
		self.outScriptID = scriptIDs[1] if len(scriptIDs) >= 2 else ""
		self.outObjectHP = int(scriptIDs[2]) if len(scriptIDs) >= 3 else 0
		
		spaces = srcData["Param3"].split("|")
		self.useSpace = spaces[0].split(":")
		self.outSpace = spaces[1] if len(spaces) >= 2 else ""
		
		tranStr = srcData["Param4"].split("|")
		if len(tranStr) >= 1:
			self.insPos = Math.Vector3( KBEMath.Unreal2KBEnginePosition(tuple(Functions.vector3TypeConvert(tranStr[0]))) )
		if len(tranStr) >= 2:
			self.insDir = Math.Vector3( KBEMath.KBEngine2UnrealDirection(tuple(Functions.vector3TypeConvert(tranStr[1]))) )
		
	def getActiveCosume( self ):
		""""""
		return self.actCosume
		
	def getPerCosume( self ):
		""""""
		return self.perCosume

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if self.useSpace:
			if owner.getCurrentSpaceScriptID() != self.useSpace:
				return csstatus.ITEM_FORBID_BY_SPACE
		return csstatus.ITEM_FORBID_BY_SPACE