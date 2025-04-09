import KBEngine
import Const
import csstatus
import csdefine
import KBEDebug
import cschannel_msgs

class SGMZMember( dict ):

	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):
		datalist = []
		for camp, _dict in obj.items():
			datalist.append( _dict )
			
		return { "datas" : datalist }

	def createObjFromDict( self, dict ):
		obj = SGMZMember()
		for r in dict[ "datas" ]:
			camp = r["camp"]
			obj[camp] = r	
		return obj

	def add(self, camp, monsterList):
		self[camp] = {}
		self[camp]["camp"] = camp
		self[camp]["isKillBoss"] = 0
		self[camp]["isWin"] = 0
		self[camp]["extraExp"] = 0
		self[camp]["feats"] = 0
		self[camp]["score"] = 0
		self[camp]["bossKiller"] = ""
		self[camp]["bossDatas"] = []
		for stage,scriptID in enumerate(monsterList):
			bossData = {
			"name"  : "",
			"scriptID" : scriptID,
			"time"  : 0,
			"exp"   : 0,
			"level" : 0,
			"PerHP" : 1.0,
			"stage" : stage+1,
			}
			self[camp]["bossDatas"].append( bossData ) 

	def onKillBoss(self, camp, bossScriptID, bossName , time, exp, level, HPPersent=1.0, feats=0, score = 0 ): 
		self[camp]["feats"] = feats
		self[camp]["score"] = score
		for data in self[camp]["bossDatas"]:
			if data["scriptID"] == bossScriptID:
				data["name"] = bossName
				data["time"] = time
				data["exp"] = exp
				data["level"] = level 
				data["PerHP"] = HPPersent

	def onKillFinalBoss(self, winCamp, extraExp, killerCamp, killerrName = None, ):
		self[killerCamp]["isKillBoss"] = 1
		self[killerCamp]["extraExp"] = extraExp
		self[killerCamp]["bossKiller"] = killerrName
		self[winCamp]["isWin"] = 1
	
	def getMonsterStage(self, camp , scriptID):
		if camp in self:
			for data in self[camp]["bossDatas"]:
				if data["scriptID"] == scriptID:
					return data["stage"]
		return 0

	def fromMonsterGetCamp(self, scriptID):
		for camp in self:
			for data in self[camp]["bossDatas"]:
				if data["scriptID"] == scriptID:
					return camp
		return 0
		
	def isSameType( self, obj ):
		return isinstance( obj, SGMZMember )

g_SGMZMember = SGMZMember()