# -*- coding: utf-8 -*-
import math
import csarithmetic
import KBEngine
import KBEDebug
import csconst
import Functions
from SrvDef import ActForbidDct
from Extra.SkillLoader import g_skills
class SkillInterface:
	"""
	"""
	def __init__( self ):
		self.attrCooldowns = {}
		self.isCasting = False
		
	def set_attrBuffsForClient(self, old):
		if len(self.attrBuffsForClient) >= 10:
			if not hasattr(self, "ai"): return
			lst = sorted(self.attrBuffsForClient, key = lambda x: x["index"])
			amount = len(self.attrBuffsForClient) - 5
			for index in range(amount):
				self.GMCommand(self, "clearBuff", "{}".format(lst[index]["buffID"]))
	
	def useSkillForTarget( self, skillID, targetID ):
		"""
		"""
		if self.isCasting:
			return
		
		self.isCasting = True
		self.cell.useSkillToEntityFC( skillID, targetID )
		KBEngine.callback(5, self.resetCast)
		self.outputMsg("useSkillForTarget:%d-%d" %(skillID, targetID))
		
	def resetCast(self):
		self.isCasting = False
		
	def useSkillToEntity( self, skillID, targetID ):
		self.outputMsg("useSkillToEntity:%s-%s"%(skillID, targetID))
		
	def useSkillToPosition( self, skillID, position=() ):
		if not position:
			position = self.position
		x,y,z = position
		clientPosition = (z*100, x*100, y*100)
		self.cell.useSkillToPositionFC( skillID, clientPosition )
		self.outputMsg("useSkillToPositionFC")
		
	def turnToPos( self, position ):
		"""
		转向一个坐标
		"""
		yaw = csarithmetic.getYawByVector3(position-self.position)
		#self.direction.z = yaw
		self.GMCommand(self, "turnToPos", "{}".format(yaw))
		
	def SetCooldown( self, CooldownIDs, EndTimes, PersistTimes ):
		"""
		设置CD
		"""
		if len(CooldownIDs) != len(EndTimes) or len(EndTimes) != len(PersistTimes):
			return
		
		if len(CooldownIDs) == 0:
			self.attrCooldowns = {}
			return
			
		currTime = Functions.getTime()
		for i in range(len(CooldownIDs)):
			endTime = int(EndTimes[i])
			if currTime >= endTime:
				continue
			
			self.attrCooldowns[int(CooldownIDs[i])] = {"endTime" : float(int(EndTimes[i])/csconst.TIME_ENLARGE_MULTIPLE), "persistTime" : float(PersistTimes[i])}
			
	def ClearCooldown( self, isClear ):
		"""
		"""
		if isClear:
			self.attrCooldowns = {}
			
	def checkUseSkill( self, skillID ):
		"""
		"""
		#判断当前是否有其他技能在释放
		if self.castingSkillID != 0:
			return False
		
		skillData = g_skills.getSkillData(skillID)
		if skillData is None:
			return False
		
		#判断禁止标志位
		actForbid = ActForbidDct.get(skillData["ActForbid"])
		actionFlagValue = 1 << actForbid
		if self.actForbid & actionFlagValue != 0:
			return False
		
		#看技能当前是否还在CD中
		currTime = float(Functions.getTime() / csconst.TIME_ENLARGE_MULTIPLE)
		cooldowns = skillData["CoolDown"]
		
		_RemainTime = -1.0
		_PersistTime = -1.0
		for cooldown in cooldowns:
			if cooldown["CooldownId"] not in self.attrCooldowns:
				continue
			
			endTime = self.attrCooldowns[cooldown["CooldownId"]]["endTime"]
			if currTime >= endTime:
				self.attrCooldowns.pop(cooldown["CooldownId"])
				continue
			
			RemainingTime = endTime - currTime
			if _RemainTime > RemainingTime or _PersistTime < self.attrCooldowns[cooldown["CooldownId"]]["persistTime"] and abs(_RemainTime - RemainingTime) < 1.0e-9:
				_RemainTime = RemainingTime
				_PersistTime = self.attrCooldowns[cooldown["CooldownId"]]["persistTime"]
			
		if _RemainTime > 0:
			return False
			
		return True
	
	def SetCastingSkill( self, p1 ):
		pass
	def RefreshReplaceSkillBar( self, p1 ):
		pass
	def OnBindBuffBulletBegin( self, p1, p2, p3 ):
		pass
	def SkillInterrupted( self, p1, p2, p3 ):
		pass
	def SkillTurnToPos( self, p1 ):
		pass
	def OnBuffBulletBegin( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def OnDisMountCarrier( self ):
		pass
	def EndDistortScene( self ):
		pass
	def SetAnimRateScale( self, p1 ):
		pass
	def intonateSpell( self, p1, p2 ):
		pass
	def StopSkillHitSlow( self ):
		pass
	def intonateSpellOver( self ):
		pass
	def OnStatBuffQTE( self, p1, p2 ):
		pass
	def CastSkillToTarget( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnEndHitBack( self, p1, p2, p3 ):
		pass
	def OnRiseEnd( self, p1 ):
		pass
	def BeCapture( self, p1, p2, p3, p4, p5 ):
		pass
	def BeReleased( self, p1 ):
		pass
	def intonateSparSpell( self, p1, p2 ):
		pass
	def OnTauntEnd( self ):
		pass
	def RemoveBuff( self, p1 ):
		pass
	def OnTauntBegin( self ):
		pass
	def CastToStone( self, p1, p2 ):
		pass
	def BuffEndPlayLinkEffect( self, p1 ):
		pass
	def OnBuffBulletMultipleBegin( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def AddShowBuffExtraTips( self, p1, p2 ):
		pass
	def OnMountCarrier( self, p1 ):
		pass
	def ReplaceSkillBar( self, p1 ):
		pass
	def DistortScene( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def ChangeToNormalModelScale( self, p1, p2 ):
		pass
	def SetCatchTargetId( self, p1 ):
		pass
	def ChangeToNormalModelVisible( self ):
		pass
	def HoldEffectPlayEffect( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def ChangeToDstModelVisible( self, p1 ):
		pass
	def OnResetBuffEndTime( self, p1, p2 ):
		pass
	def CastToNormal( self, p1 ):
		pass
	def PlayArtificeSpar( self, p1, p2 ):
		pass
	def ReceiveSkill( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def TeleportToDstPosition( self, p1):
		pass
	def OnEndBuffQTE( self ):
		pass
	def OnChargeToPosition( self, p1, p2, p3, p4 ):
		pass
	def Unfreeze( self ):
		pass
	def OnBuffLayerChange( self, p1, p2 ):
		pass
	def PlayBuffEffect( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def LXDistortScene( self, p1, p2, p3, p4, p5 ):
		pass
	def ChangeToDstModelScale( self, p1, p2, p3 ):
		pass
	def OnRage( self, p1, p2, p3, p4, p5 ):
		pass
	def EndTransparency( self, p1, p2, p3, p4 ):
		pass
	def CastSkillToPosition( self, p1, p2, p3, p4, p5, p6, p7, p8, p9 ):
		pass
	def StopArtificeSpar( self, p1 ):
		pass
	def AddBuff( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnRiseBegin( self, p1, p2, p3, p4, p5 ):
		pass
	def Frozee( self ):
		pass
	def OnBuffBulletMultipleEnd( self, p1, p2, p3 ):
		pass
	def StartTransparency( self, p1, p2, p3, p4 ):
		pass
	def FlyPatrol( self, p1, p2, p3 ):
		pass
	def HoldEffectEndEffect( self, p1, p2 ):
		pass
	def BeHitPlayEffect( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnBeHitBackNew( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnStopMoving( self ):
		pass
	def OnPull( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def EndPull( self, p1, p2 ):
		pass
	def StopCycleFlyPatrol( self, p1 ):
		pass
	def EndRage( self, p1 ):
		pass
	def OnChasePlayer( self, p1 ):
		pass
	def onDodgeSkillHit( self, p1 ):
		pass
	def PlayModleHighlight( self, p1 ):
		pass
	def RemoveBuffExtraTips( self, p1 ):
		pass
	def OnBuffBulletEnd( self, p1, p2 ):
		pass
	def StartSkillHitSlow( self, p1, p2, p3 ):
		pass
	def onEndChargeToPosition( self ):
		pass
	def intonateSparSpellOver( self ):
		pass
	def onCasterSkillEnd( self, p1, p2 ):
		pass
	def BuffPlayLinkEffect( self, p1, p2, p3 ):
		pass
	def ReviveFlyPatrol( self ):
		pass
	def OnBindBuffBulletEnd( self, p1 ):
		pass
	def PauseFlyPatrol( self ):
		pass
	def OnReplaceSkillBarEnd( self ):
		pass
	def BeHitPlayEffectLocal( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def OnShowIntonateBar( self, p1, p2, p3 ):
		pass
	def OnHideIntonateBar( self, p1 ):
		pass
	def CLIENT_StartSubmerge( self ):
		pass
	def CLIENT_EndSubmerge( self ):
		pass
	def CLIENT_ControlledOnBeHitBack( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def CLIENT_ControlledEndHitBack( self, p1, p2, p3 ):
		pass
	def CLIENT_StartFog( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_EndFog( self, p1 ):
		pass
	def OnDissolve( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def EndDissolve( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_AutoRise( self, p1 ):
		pass
	def CLIENT_StopRise( self ):
		pass
	def CLIENT_RotateCamera( self, p1, p2 ):
		pass
	def CLIENT_RoleChaseEntity( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_RoleChargePosition( self, p1, p2 ):
		pass
	def CLIENT_OnDiedDissolveStart( self, p1, p2, p3, p4, p5, p6, p7 ):
		pass
	def CLIENT_RoleChaseEntityEnd( self ):
		pass
	def CLIENT_OnMountSlide( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_OnDismountSlide( self ):
		pass
	def EndOverLookScene( self ):
		pass
	def StartOverLookScene( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_ForcedJump( self, p1 ):
		pass
	def CLIENT_HideInGame( self ):
		pass
	def CLIENT_ShowInGame( self ):
		pass
	def EnterDark( self ):
		pass
	def CLIENT_TurnOffLight( self ):
		pass
	def LeaveDark( self ):
		pass
	def CLIENT_TurnOnLight( self, p1 ):
		pass
	def CLIENT_StopFlyPatrol( self, p1 ):
		pass
	def CLIENT_OnMountStone( self, p1, p2 ):
		pass
	def CLIENT_OnDisMountStone( self ):
		pass
	def EndHideCharacter( self, p1 ):
		pass
	def StartHideCharacter( self, p1 ):
		pass
	def CastCSkillToPosition( self, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 ):
		pass
	def CastCSkillToTarget( self, p1, p2, p3, p4, p5, p6, p7, p8 ):
		pass
	def IntensifySkill( self, p1, p2, p3, p4, p5 ):
		pass
	def CancelIntensifySkill( self, p1, p2, p3, p4, p5 ):
		pass
	def AddReplaceSkillBar( self, p1 ):
		pass
	def EnterToxicosis(self, p1):
		pass
	def LeaveToxicosis(self, p1):
		pass
	def OnCreateTrace(self, p1, p2, p3, p4, p5, p6, p7):
		pass
	def OnFinishCreateTrace(self, p1):
		pass
	
