# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BatteleFormationsImp( dict ):
	"""
	轮回秘境 阵图 数据
	"""
	def __init__( self ):
		dict.__init__( self )
	
	@classmethod
	def getDictFromObj( self, obj ):
		dict = {}
		temp = []
		for playerDBID, data in obj.items():
			tDict = {}
			tDict["playerDBID"] = playerDBID
			tDict["psionic"] = data[0]
			tDict["perPsionic"] = data[1]
			tDict["isActive"] = data[2]
			
			temp.append(tDict)
		dict["dictData"] = temp
		return dict
	
	@classmethod
	def createObjFromDict( self, dict ):
		obj = BatteleFormationsImp()
		for datas in dict["dictData"]:
			obj[datas["playerDBID"]] = [datas["psionic"], datas["perPsionic"], datas["isActive"] ]
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, BatteleFormationsImp )

instance = BatteleFormationsImp()
