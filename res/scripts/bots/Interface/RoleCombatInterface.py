# -*- coding: utf-8 -*-
from Interface.CombatInterface import CombatInterface
import csdefine
from Interface.RoleStateInterface import RoleStateInterface
SKILL_ATTACK_TARGET = [] #所有攻击技能列表
class RoleCombatInterface( CombatInterface ,
	RoleStateInterface,
	):
	def __init__( self ):
		RoleStateInterface.__init__(self)
		CombatInterface.__init__( self )
		self.autoFightFlag = False				#自动战斗开关
		self.fightTargetID  = 0
		
		self.attrackSkillSpellEntity = [] #所有攻击技能
		self.attrackSkillSpellPosition = [] #所有对位置攻击的
		self.skillsList = [] #所有技能
		self.firstUseSkillID = 0	#攻击使用的技能ID
	
#------自动战斗------
	def findEnemy(self):
		"""找到适合的敌人直接设为target,无返回值"""
		entityList = self.entitiesInRange(20)		
		for e in entityList:
			if self.isEnemy(e):
				self.fightTargetID = e.id
				self.moveTo(e.position)
				self.toFight()
				return
				
	def getEnemy(self, targetID):
		target = self.monsterInRange( [targetID,] )
		if target:
			self.fightTargetID = target.id
		
	def toFight(self):
		"""打怪"""
		self.outputMsg("AUTO_FIGHT attackting %i" % self.fightTargetID )
		self.useSkillToTarget( botdefine.DEFAULT_SKILL_ID, self.fightTargetID )
		
	def autoFight(self):
		"""自动战斗本体"""
		if not self.autoFightFlag:		#自动开关
			return
		target = self.clientapp.entities.get( self.fightTargetID )
		if self.isEnemy(target):
			self.moveTo( target.position )
			self.toFight()
		else:
			self.getEnemy( botdefine.DEFAULT_MONSTER )
		KBEngine.callback( 3.0, self.autoFight )
		
	def isEnemy( self, e ):
		if e==None or e.className != "Monster":
			return False
		#if e.camp == self.camp:
		#	return False
		if e.state ==  botdefine.ENTITY_STATE_DEAD:
			self.outputMsg("AUTO_FIGHT target %i is dead." % e.id )
			return False
		return True
#------SkillInterface------
	def useSkillToTarget( self, skillID, targetID ):
		self.cell.useSkillToEntityFC( skillID, targetID )
		self.outputMsg("useSkillToEntityFC")
		
	def useSkillToPosition( self, skillID, position=() ):
		if not position:
			position = self.position
		x,y,z = position
		serPosition = (z*100, x*100, y*100)
		self.cell.useSkillToPositionFC( skillID, serPosition )
		self.outputMsg("useSkillToPositionFC")
		
	def InitSkills(self, skillIDList ):
		for skillID in skillIDList:
			if skillID not in self.skillsList:
				self.skillsList.append( skillID )
				self.attrackSkillSpellEntity.append( skillID )
		
	def OnAddSkill(self, skillID):
		if skillID not in self.skillsList:
			self.skillsList.append( skillID )
		
	def OnRemoveSkill(self, skillID):
		if skillID not in self.skillsList:
			self.skillsList.append( skillID )
		
	def ShowBuffExtraSkillBar( self, skillIDStr ):
		pass
		
	def CloseBuffExtraSkillBar(self):
		pass
	def ShowBuffExtraFaBaoSkillBar( self, p1 ):
		pass
	def CloseBuffExtraFaBaoSkillBar( self ):
		pass
	def CLIENT_requestOpenSkillLearn( self, p1 ):
		pass
	def CLIENT_ShowCombatPowerChangeTips( self, p1, p2 ):
		pass
	def CLIENT_OnDoubleHit( self, p1 ):
		pass
	def CLIENT_FirstLearnSkillNotify( self, p1 ):
		pass
	def InitPassiveSkillBar( self, p1 ):
		pass
	def updatePassiveSkillBar( self, p1 ):
		pass
		
	def CLIENT_SetForbidJumpSkillIDs(self, skillIDs):
		pass
