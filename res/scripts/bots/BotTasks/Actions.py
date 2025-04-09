# -*- coding: utf-8 -*-
import Math
import re
import KBEngine
import time
import Functions
import csarithmetic

from BotTasks.BehaviorBase import ActionBase

PET_EGG = "204010001"
#----------------------------------
# public methods
#----------------------------------
pat = re.compile(r"^\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)(\s*\,|\s+)\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)(\s*\,|\s+)\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)\s*$")

def vector3TypeConvert( param ):
	"""
	@param param: 将字符串转换成三维坐标，三个坐标之间式必须用空格分隔
	@return:	  Math.Vector3
	"""
	try:	#判断Vector3类型数据格式是否正确
		m = pat.match( param ).group().split()
		if len( m ) != 3:
			return None
	except:
		return None

	result = Math.Vector3( float( m[0] ), float( m[1] ), float( m[2] ) )
	return result


#----------------------------------
# extends class 
#----------------------------------
#doNothing
class Action0( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction0"%self.keyID)
		roleEntity.behOver()
		
# killMonster
class Action1( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.killMonsterScriptIDs = config[ "param1" ].split( "|" )
		self.amount = config["goal"]

	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction1"%self.keyID)
		if not roleEntity.monsterInRange(self.killMonsterScriptIDs):
			roleEntity.outputMsg("clone %s "% self.killMonsterScriptIDs[0] )
			roleEntity.GMCommand( roleEntity, "clone", self.killMonsterScriptIDs[0] )
		roleEntity.killMonster( self.killMonsterScriptIDs, self.amount )
		
	def checkIsCompleted( self, roleEntity ):
		roleEntity.outputMsg("quest %s  %s killed %s monster!"% (self.keyID, self.__class__ , roleEntity.getKillMonstersCounter( self.killMonsterScriptIDs )))
		return roleEntity.getKillMonstersCounter( self.killMonsterScriptIDs ) >= self.amount

#moveto position
class Action2( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.position = vector3TypeConvert( config[ "param1" ] )
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction2"%self.keyID)
		needTime = roleEntity.moveTo( self.position )
		roleEntity.behOver( needTime )
		
	def checkIsCompleted(self, roleEntity):
		return roleEntity.position.distTo( self.position )<=5.0

#teleport space
class Action3( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.spaceScriptID = config[ "param1" ]
		self.position = vector3TypeConvert( config[ "param2" ] )
		self.taskID = str(config[ "taskID" ])

	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction3"%self.keyID)
		roleEntity.teleportTo( self.spaceScriptID, self.position )
		roleEntity.cell.broadcastQuestEvent( self.keyID, self.taskID)
		roleEntity.behOver()
		

#study skill
class Action4( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.skillID = config[ "param1" ]
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction4"%self.keyID)
		roleEntity.GMCommand( roleEntity, "addSkill", self.skillID )
		roleEntity.behOver()
		
#EventTrigger
class Action5( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.taskID = str(config[ "taskID" ])
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction5"%self.keyID)
		roleEntity.cell.broadcastQuestEvent( self.keyID, self.taskID)
		roleEntity.behOver()

#getItem
class Action6( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.itemID = config[ "param1" ]
		self.amount = config[ "goal" ]
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction6"%self.keyID)
		roleEntity.GMCommand( roleEntity, "addItem", self.itemID, str(self.amount ))
		roleEntity.behOver()
		
#DaohengLevel
class Action7( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.amount = config[ "param1" ]
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction7"%self.keyID)
		roleEntity.GMCommand( roleEntity, "add_daoheng", self.skillID )
		roleEntity.behOver()
		
#QuestTaskCommitItem
class Action8( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction8"%self.keyID)
		roleEntity.behOver()
		
#acceptQuest
class Action9( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.startNPC = config["param1"]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction9"%self.keyID)
		spaceID, position = roleEntity.findNPC(self.startNPC)
		needTime=0
		if spaceID and position:
			needTime = roleEntity.goto( spaceID,position )
		KBEngine.callback( needTime+2, Functions.Functor(roleEntity.acceptQuest,self.keyID))
		roleEntity.behOver( needTime+3 )
		
#commitQuest
class Action10( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.finishNPC = config["param1"]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction10"%self.keyID)
		roleEntity.GMCommand( roleEntity, "complete_quest", self.keyID )
		spaceID, position = roleEntity.findNPC(self.finishNPC)
		needTime=0
		if spaceID and position:
			needTime = roleEntity.goto( spaceID,position )
		KBEngine.callback( needTime+3, Functions.Functor(roleEntity.commitQuest,self.keyID))
		
#find and  goto NPC
class Action11( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.navigateData = config["navigateData"]
		self.killMonsterScriptIDs = []
		self.killMonsterScriptIDs = config[ "param1" ].split( "|" )
		self.amount = config["goal"]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction11"%self.keyID)
		if self.navigateData:
			naviData = self.navigateData.split("#")
			if "(" in naviData[0]:
				position, spaceScriptID = naviData[0].replace("(","").replace(")","").split(" "), naviData[1]
				monsterScriptIDs = self.killMonsterScriptIDs
			else:
				monsterScriptIDs, spaceScriptID = naviData[0].split( "|" ),naviData[1]
				spaceScriptID, position = roleEntity.findNPC( monsterScriptIDs, spaceScriptID )
		else:
			roleEntity.behOver()
			return
		if spaceScriptID and position:
			needTime = roleEntity.goto( spaceScriptID, position )
			roleEntity.behOver( needTime )
			roleEntity.onRoleSendChatMessage( "2", "quest:%s goto position: %s %s find: %s;"%(self.keyID,spaceScriptID,position, monsterScriptIDs) , "" )
		else:
			roleEntity.GMCommand( roleEntity, "clone", self.killMonsterScriptIDs[0],str(self.amount ))
			roleEntity.outputMsg("clone %s "%self.killMonsterScriptIDs[0] )
			roleEntity.behOver()
			
	def checkIsCompleted(self, roleEntity):
		return roleEntity.position.distTo( self.position )<=5.0

#useSkill
class Action12( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.skillID = config[ "param1" ]
	
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction12"%self.keyID)
		roleEntity.useSkillToTarget(self.skillID,roleEntity.id)
		roleEntity.behOver()
		
#talkWithNPC
class Action13( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.NPCID = config[ "param1" ]
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction13"%self.keyID)
		npc = None
		for e in roleEntity.entitiesInRange(20):
			if e.entityFlag in [4,5,12] and e.scriptID == self.NPCID:
				npc = e
				break
		if not npc:
			roleEntity.outputMsg( "can not find NPC %s"% self.NPCID )
		else:
			npc.cell.talkWith("","")
			npc.cell.talkWith("talks","")
		roleEntity.behOver()
	
#ConjurePet 召唤
class Action14( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.scriptID = config[ "param1" ]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction14"%self.keyID)
		uid = roleEntity.getPetbySID( self.scriptID )
		roleEntity.cell.conjurePet( uid )
		roleEntity.behOver()
		
#MountPet 骑乘
class Action15( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.scriptID = config[ "param1" ]
				
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction15"%self.keyID)
		roleEntity.cell.transformPet()
		roleEntity.behOver()
	
#useItem 使用物品
class Action16( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.itemID = config[ "param1" ]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction16"%self.keyID)
		items = self.ai.owner.items
		for itemOrder, item in items.items():
			if item.id == self.itemID:
				self.roleEntity.cell.CELL_useItem( str(item.uid),  str(roleEntity.id))
		roleEntity.behOver()
		
#upLevel 升级
class Action17( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.level= config["param1"]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction17"%self.keyID)
		roleEntity.GMCommand( roleEntity, "setLevel", self.level)
		roleEntity.behOver()
		
# 修为升级
class Action18( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.xiuwei= config["param1"]
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction18"%self.keyID)
		roleEntity.GMCommand( roleEntity, "setXiuwei", self.xiuwei)
		roleEntity.behOver()
		
#moveto area
class Action19( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.param1 = config[ "param1" ]	#区域类型:		1圆形，2多边形
		self.param2 = config[ "param2" ]        #区域z值范围:	最大z值|最小z值
		self.param3 = config[ "param3" ]        #区域参数:		圆形“x y z：半径”，多边形“x1 y1|x2 y2|...
		
	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction19"%self.keyID)
		if param1=="1":
			pos = self.param3.split(":")[0].split(" ")
			radius = self.param3.split(":")[1]
			position = csarithmetic.getPositionByCircular( pos , radius )
		elif param2 =="2":
			pos = self.param3.split("|")[0].split(" ")
		needTime = roleEntity.moveTo( position )
		roleEntity.behOver( needTime )
		
#doSpaceStage
class Action20( ActionBase.ActionBase ):
	def __init__( self, config ):
		ActionBase.ActionBase.__init__( self, config )
		self.taskID = str(config[ "taskID" ])
		self.stageID = str(config[ "stageID" ])
		self.goal = config["goal"]

	def doAction( self, roleEntity ):
		roleEntity.outputMsg("quest %s doAction20"%self.keyID)
		import time
		for i in range(self.goal):
			roleEntity.GMCommand(roleEntity, "completeStageTask",self.stageID, self.taskID)
			time.sleep(3)
		roleEntity.behOver( 20 )
	
ActionBase.ActionBase.setClass( "Action0", Action0 )
ActionBase.ActionBase.setClass( "Action1", Action1 )
ActionBase.ActionBase.setClass( "Action2", Action2 )
ActionBase.ActionBase.setClass( "Action3", Action3 )
ActionBase.ActionBase.setClass( "Action4", Action4 )
ActionBase.ActionBase.setClass( "Action5", Action5 )
ActionBase.ActionBase.setClass( "Action6", Action6 )
ActionBase.ActionBase.setClass( "Action7", Action7 )
ActionBase.ActionBase.setClass( "Action8", Action8 )
ActionBase.ActionBase.setClass( "Action9", Action9 )
ActionBase.ActionBase.setClass( "Action10", Action10 )
ActionBase.ActionBase.setClass( "Action11", Action11 )
ActionBase.ActionBase.setClass( "Action12", Action12 )
ActionBase.ActionBase.setClass( "Action13", Action13 )
ActionBase.ActionBase.setClass( "Action14", Action14 )
ActionBase.ActionBase.setClass( "Action15", Action15 )
ActionBase.ActionBase.setClass( "Action16", Action16 )
ActionBase.ActionBase.setClass( "Action17", Action17 )
ActionBase.ActionBase.setClass( "Action18", Action18 )
ActionBase.ActionBase.setClass( "Action19", Action19 )
ActionBase.ActionBase.setClass( "Action20", Action20 )