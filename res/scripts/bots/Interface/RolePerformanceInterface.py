# -*- coding: utf-8 -*-
class RolePerformanceInterface( object ):
	def __init__( self ):
		pass
	
	def ShowMessagePlaySound(self, params):
		pass
		
	def HideSpaceLife( self ):
		pass
	
	def ShowSpaceLife( self, p1, p2 ):
		pass
	
	def ShowStopSpaceLife( self, p1 ):
		pass
	def Intonate( self, float1, int1, int2 ):
		pass
	def InteruptIntonate( self ):
		pass
	
	def OnChangeBodyStart(self):
		pass
		
	def OnChangeBodyEnd(self):
		pass
		
	def onXinMoCtrlStart(self):
		pass
		
	def onXinMoCtrlEnd(self):
		pass
		
	def OnBeginTrapSuck(self, suckPosition, suckSpeed):
		pass
		
	def OnEndTrapSuck(self):
		pass
		
	def onBeginConfusion(self):
		pass
		
	def onEndConfusion(self):
		pass
		
	def ShowSpellBoxResultMessage( self, result, exp ):
		pass
		
	def ShowPrompetOper( self, prompetID, particleID, p3 ):
		pass
		
	def HidePrompetOper(self):
		pass
		
	def StartGuessGame(self, roll, finishMsg ):
		pass
		
	def RightGuess(self, roll, finishMsg ):
		pass
		
	def  WrongGuess(self, roll, finishMsg ):
		pass
		
	def FinishGuess(self, roll, finishMsg ):
		pass
		
	def CreateLightWallBP(self, str1, int1):
		pass
		
	def RemoveLightWallBP(self, str1):
		pass
			
	def ShowEquipHardiness(self, str1):
		pass
		
	def ShowSwordAmount(self, int1):
		pass
		
	def HLDCanStart(self):
		pass
		
	def HoldPet(self, str1):
		pass
		
	def DownPet(self, p1):
		pass
	
	def HLDEnd(self):
		pass
		
	def EnterFishState(self,int1, int2, int3 ):
		pass
		
	def StartFish(self):
		pass
		
	def ChangeWrestlingWidget(self):
		pass
		
	def ShowFishScore(self, int1):
		pass
		
	def ZhenLongQiJu_OnBossHPChange( self,HP_Max, newValue ):
		pass
		
	def ZhenLongQiJu_OnBossStateChange(self, pieceState,id):
		pass
		
	def ZhenLongQiJu_StopBossStateChange(self, pieceState,id):
		pass
		
	def ZhenLongQiju_ClearData(self):
		pass
		
	def UpdateMoneyDataToOtherPlayer(self, int1,int2 ):
		pass
		
	def ReceiveOtherMoneyData(self, int1,int2 ):
		pass
		
	def UpdateIntegralDataToOtherClient(self, int1,int2 ):
		pass
		
	def ReceiveOtherIntegralData(self, int1,int2 ):
		pass
		
	def UpdateBeKillDataToOtherClient(self,int1,int2):
		pass
		
	def ReceiveOtherBeKillData(self, int1,int2):
		pass
		
	def UpdateKillDataToOtherClient(self, int1,int2):
		pass
		
	def ReceiveOtherKillData(self,int1,int2):
		pass
		
	def SetIntegralMax(self):
		pass
		
	def PlayBindEffect(self, int1, str1):
		pass
		
	def EndPlayBindEffect(self, int1):
		pass
		
	def EnterAimStatus(self):
		pass
		
	def LeaveAimStatus(self):
		pass
		
	def HoldJinDan( self, petMeshTableId, buffRemainTime, timerInterval):
		pass
		
	def DownJinDan(self):
		pass
		
	def ShowPutDownJinDanBtn(self):
		pass
		
	def HidePutDownJinDanBtn(self):
		pass
		
	def OnStartThroughCanyon(self, mountModelId, forwardSpeed, downSpeed):
		pass
		
	def OnEndThroughCanyon(self):
		pass
		
	def AddFlyForce( self, dire, forceSpeed, forceTime ):
		pass
		
	
	def onStartMoveByMoveTrap(self, id, moveSpeed):
		pass
		
	def onStopMoveByMoveTrap(self):
		pass
		
	def OnAddShield(self,int1,int2):
		pass
		
	def OnRemoveShield(self):
		pass
		
	def OnShieldChanged(self,int1,int2):
		pass
		
	def RoleCameraMoveToEntity(self):
		pass
		
	def GetMovingPlatFormControl(self):
		pass
		
	def LoseMovingPlatFormControl(self):
		pass
		
	def OnMountHeHua(self):
		pass
		
	def MoveToTargetPosition(self,pos):
		pass
		
	def RoleCameraMoveToEntityCB( self, p1 ):
		pass
	def CopyRemainTime( self, p1 ):
		pass
	def UpdateScoreForLHSL( self, p1, p2 ):
		pass
	def SendRandomList( self, p1 ):
		pass
	def ExpelTheSoul( self, p1, p2, p3, p4 ):
		pass
	def AlchemyStart( self, p1, p2 ):
		pass
	def OpenAreaWall( self, p1 ):
		pass
	def LeaveModelTPS( self ):
		pass
	def EnterModelTPS( self ):
		pass
	def FabaoPlayEffectEnd( self ):
		pass
	def WrongGuess( self, p1 ):
		pass
	def FabaoPlayEffect( self, p1, p2 ):
		pass
	def CloseAreaWall( self, p1 ):
		pass
	def ShowMessageUpPlayerHead( self, p1 ):
		pass
	def CreateFaBao( self, p1, p2 ):
		pass
	def AbsorbTheSoul( self, p1 ):
		pass
	def RemoveFaBao( self ):
		pass
	def CreateAircraft( self, p1, p2 ):
		pass
	def RemoveAircraft( self, p1 ):
		pass
	def AircraftUseSkill( self, p1 ):
		pass
	def RoleCameraShake( self, p1, p2, p3 ):
		pass
	def SendGameCopyTime( self, p1, p2 ):
		pass
	def OnTauntBegin( self ):
		pass
	def OnTauntEnd( self ):
		pass
	def EnterShootModel( self ):
		pass
	def LeaveShootModel( self ):
		pass
	def EnterFlyModel( self ):
		pass
	def LeaveFlyModel( self ):
		pass
	def ResetJump( self ):
		pass
	def OnSetViewTarget( self, p1, p2, p3, p4, p5, p6 ):
		pass
	def CLIENT_CreateAircraft( self, p1, p2 ):
		pass
	def CLIENT_RemoveAircraft( self, p1 ):
		pass
	def CLIENT_AircraftUseSkill( self, p1, p2 ):
		pass
	def CLIENT_ResetJump( self ):
		pass
	def CLIENT_ThrowJinDan( self, p1, p2, p3 ):
		pass
	def CLIENT_OnThrowJinDan( self, p1 ):
		pass
	def OnDialogWithNPCTaskScriptID( self, p1 ):
		pass
	def CLIENT_EnterModelTPSParam( self, p1 ):
		pass
	def CLIENT_LeaveModelTPSParam( self ):
		pass
	def CLIENT_AddTrapVortex( self, p1, p2 ):
		pass
	def CLIENT_RemoveTrapVortex( self, p1 ):
		pass
	def CLIENT_ShowSpaceSettlementWin( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_showSurvivalTime( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_startSurvivalTime( self ):
		pass
	def CLIENT_endSurvivalTime( self, p1 ):
		pass
	def CLIENT_ClearChasePosInfo( self ):
		pass
	def CLIENT_AddPerspectiveTarget( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_RemovePerspectiveTarget( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_ShowHPPercentAboveQuestBar( self, p1 ):
		pass
	def CLIENT_CloseHPPercentAboveQuestBar( self ):
		pass
	def CLIENT_SetMiniMapViewDefaultScale( self, p1 ):
		pass
	def CameraLookAtTarget( self, p1, p2, p3, p4 ):
		pass
	def EnterYCJMDModelTPS( self, p1 ):
		pass
	def LeaveYCJMDModelTPS( self ):
		pass
	def OnWinGameSGMZ( self, p1 ):
		pass
	def SGMZMonsterHPChange( self, p1, p2, p3 ):
		pass
	def leadTeamChange( self, p1, p2, p3 ):
		pass
	def CLIENT_OnRequestCrossServiceResult( self, p1 ):
		pass
	def sendSGMZMonsterHp( self, p1, p2 ):
		pass
	def CLIENT_OnRequestReturnServerResult( self, p1 ):
		pass
	def ChangeYCJMDModelTPSSkillID( self, p1 ):
		pass
	def ShowSkillBarsHighLigh( self, p1 ):
		pass
	def CLIENT_SGMZBossKilled( self, p1, p2 ):
		pass
	def SGMZSendScore( self, p1, p2, p3 ):
		pass
	def SGMZSendScoreChange( self, p1, p2 ):
		pass
	def SGMZSendMonsterHp( self, p1, p2, p3 ):
		pass
	def SGMZOnWinGame( self, p1 ):
		pass
	def SGMZLeadTeamChange( self, p1 ):
		pass

	def SetSkillBarEnabled( self, p1 ):
		pass