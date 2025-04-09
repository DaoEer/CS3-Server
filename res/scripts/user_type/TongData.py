# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import ItemFactory
if KBEngine.component == "baseapp":
	import TongMember

class TongMemberData( object ):
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict[ "DBID" ] = obj.DBID
		tempDict[ "name" ] = obj.name
		tempDict[ "profession" ] = obj.profession
		tempDict[ "level" ] = obj.level
		tempDict[ "title" ] = obj.title
		tempDict[ "localSpace" ] = obj.localSpace
		tempDict[ "offLineTime" ] = obj.offLineTime
		tempDict[ "exp" ] = obj.exp
		tempDict["contribution"] = obj.contribution
		tempDict["weekContribution"] = obj.weekContribution
		tempDict["totalContribution"] = obj.totalContribution
		tempDict[ "isGag" ] = obj.isGag
		tempDict[ "signTime" ] = obj.signTime
		tempDict[ "dMoney" ] = obj.dMoney
		tempDict["soldierAmount"] = obj.soldierAmount
		tempDict["militaryRank"] = obj.militaryRank
		tempDict["tongBlocklist"] = obj.tongBlocklist
		tempDict["isSign"] = obj.isSign
		tempDict["isGetSalary"] = obj.isGetSalary
		tempDict["personTitle"] = obj.personTitle
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		return TongMember.TongMember( None, proDict["DBID"],  proDict["name"],\
		proDict["level"], proDict["profession"],proDict["title"], proDict["localSpace"],\
		proDict["weekContribution"], proDict["offLineTime"], proDict["exp"],proDict["contribution"], \
		proDict["totalContribution"], proDict["isGag"], proDict["signTime"], \
		proDict["dMoney"] ,proDict["soldierAmount"],proDict["militaryRank"], proDict["isSign"], proDict["isGetSalary"], proDict["personTitle"])
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongMember.TongMember )

g_tongMemberData = TongMemberData()

class TongMemberDict( dict ):
	def __init__( self ):
		dict.__init__( self )
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict[ "members" ] = []
		
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		obj = TongMemberDict()
		for mObj in proDict[ "members" ]:
			obj[ mObj.DBID ] = mObj
			
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongMemberDict )

g_tongMemberDict = TongMemberDict()

class TongResearchSkill( dict ):
	def __init__( self ):
		self.reaSkillID = 0
		self.reaProgress = 0
	
	def setResearchSkill( self, skillID, progress ):
		self.reaSkillID = skillID
		self.reaProgress = progress
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict["reaSkillID"]= obj.reaSkillID
		tempDict["reaProgress"] = obj.reaProgress
		return tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		reaSkillInst = TongResearchSkill()
		reaSkillInst.reaSkillID = proDict["reaSkillID"]
		reaSkillInst.reaProgress = proDict["reaProgress"]
		return reaSkillInst
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongResearchSkill )

g_tongResearchSkill = TongResearchSkill()


class tongSkillData( dict ):
	def __init__( self ):
		dict.__init__(self)

	def getDictFromObj( self, obj ):

		data = {}
		data["ResearchSkill"] = {}
		data["ResearchSkill"]["skillID"] = obj["ResearchSkill"]["skillID"]
		data["ResearchSkill"]["progress"] = obj["ResearchSkill"]["progress"]

		data["PauseSkill"] = []
		for skill in obj["PauseSkill"]:
			data["PauseSkill"].append( skill )
		data["SkillList"] = []
		for skill in obj["SkillList"]:
			data["SkillList"].append( skill )
		data["SkillLevelList"] = []
		for skill in obj["SkillLevelList"]:
			data["SkillLevelList"].append( skill )

		return data
		
	def createObjFromDict( self, data ):

		obj = tongSkillData()
		obj["ResearchSkill"] = {}

		obj["ResearchSkill"]["skillID"] = data["ResearchSkill"]["skillID"]
		obj["ResearchSkill"]["progress"] = data["ResearchSkill"]["progress"]

		obj["PauseSkill"] = []
		for skill in data["PauseSkill"]:
			obj["PauseSkill"].append( skill )

		obj["SkillList"] = []
		for skill in data["SkillList"]:
			obj["SkillList"].append( skill )

		obj["SkillLevelList"] = []
		for skill in data["SkillLevelList"]:
			obj["SkillLevelList"].append( skill )

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, tongSkillData )

g_tongSkillData = tongSkillData()

class clineTongData( dict ):
	def __init__( self ):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict["TongDBID"]= obj["TongDBID"]
		tempDict["TongLeader"] = obj["TongLeader"]
		tempDict["TongName"]= obj["TongName"]
		tempDict["level"]= obj["level"]
		tempDict["TongMoney"]= obj["TongMoney"]
		tempDict["TongAffiche"]= obj["TongAffiche"]
		tempDict["TongActivity"]= obj["TongActivity"]
		tempDict["TongGrow"]= obj["TongGrow"]
		tempDict["TotalNum"]= obj["TotalNum"]
		tempDict["League"]= obj["League"]
		tempDict["City"]= obj["City"]
		tempDict["ShenShou"]= obj["ShenShou"]
		tempDict["Sign"]= obj["Sign"]
		tempDict["signTime"]= obj["signTime"]
		tempDict["donateMoney"]= obj["donateMoney"]
		tempDict["Salary"]= obj["Salary"]
		tempDict["recruitAffiche"]= obj["recruitAffiche"]
		tempDict["minActivity"]= obj["minActivity"]
		tempDict["Allocation"] = obj["Allocation"]
		tempDict["BHLDAllocation"] = obj["BHLDAllocation"]

		tempDict["TitleNames"] = []
		for name in obj["TitleNames"]:
			tempDict["TitleNames"].append( name )

		tempDict["TongGrades"] = []
		for grads in obj["TongGrades"]:
			tempDict["TongGrades"].append( grads )

		tempDict["TongBuild"] = []
		for build in obj["TongBuild"]:
			tempDict["TongBuild"].append( build )

		tempDict["UpGradeActivity"]= obj["UpGradeActivity"]
		tempDict["minActivity"]= obj["minActivity"]
		tempDict["TongSkill"]= tongSkillData().getDictFromObj( obj["TongSkill"] )
		return tempDict

	def createObjFromDict( self, data ):

		obj = clineTongData()

		obj["TongDBID"]= data["TongDBID"]
		obj["TongLeader"] = data["TongLeader"]
		obj["TongName"]= data["TongName"]
		obj["level"]= data["level"]
		obj["TongMoney"]= data["TongMoney"]
		obj["TongAffiche"]= data["TongAffiche"]
		obj["TongActivity"]= data["TongActivity"]
		obj["TongGrow"]= data["TongGrow"]
		obj["TotalNum"]= data["TotalNum"]
		obj["League"]= data["League"]
		obj["City"]= data["City"]
		obj["ShenShou"]= data["ShenShou"]
		obj["Sign"]= data["Sign"]
		obj["signTime"]= data["signTime"]
		obj["donateMoney"]= data["donateMoney"]
		obj["Salary"]= data["Salary"]
		obj["recruitAffiche"]= data["recruitAffiche"]
		obj["minActivity"]= data["minActivity"]
		obj["Allocation"] = data["Allocation"]
		obj["BHLDAllocation"] = data["BHLDAllocation"]

		obj["TitleNames"] = []
		for name in data["TitleNames"]:
			obj["TitleNames"].append( name )

		obj["TongGrades"] = []
		for grads in data["TongGrades"]:
			obj["TongGrades"].append( grads )

		obj["TongBuild"] = []
		for build in data["TongBuild"]:
			obj["TongBuild"].append( build )

		obj["UpGradeActivity"]= data["UpGradeActivity"]
		obj["TongSkill"]= tongSkillData().createObjFromDict( data["TongSkill"] )

		return obj 
	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, clineTongData )

g_clineTongData = clineTongData()

