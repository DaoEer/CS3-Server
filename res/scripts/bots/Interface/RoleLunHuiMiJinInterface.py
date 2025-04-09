from Interface.RoleLHMJActiveInterface import RoleLHMJActiveInterface
# -*- coding: utf-8 -*-
class RoleLunHuiMiJinInterface(
	RoleLHMJActiveInterface,
	):
	def __init__(self):
		RoleLHMJActiveInterface.__init__(self)
	def LeaveHSBZModelTPS( self ):
		pass
	def EnterHSBZModelTPS( self, p1, p2 ):
		pass
	def TongTinaDaSpaceFailure( self, p1 ):
		pass
	def TongTinaDaSpaceSuccess( self, p1, p2, p3, p4 ):
		pass
	def OnCatchOriginPetResult( self, p1 ):
		pass
	def CLIENT_onUpgradeJadeItem( self, p1 ):
		pass
	def CLIENT_OnLHMJBuildLevelChange( self, p1, p2 ):
		pass
	def CLIENT_initLHMJBuild( self, p1, p2 ):
		pass
	def CLIENT_OnSuccessBuyLHMJShopItem( self, p1, p2 ):
		pass
	def CLIENT_reflashLHMJShopTime( self, p1 ):
		pass
	def CLIENT_reflashLHMJShopData( self, p1 ):
		pass
	def CLIENT_autoReflashLHMJShopData( self, p1 ):
		pass
	def CLIENT_InitLHMJShopData( self, p1, p2 ):
		pass
	def OnNotifyBuildPos( self, p1, p2 ):
		pass
	def OccupyBuildResult( self, p1 ):
		pass
	def OnShowCompassUI( self ):
		pass
	def StartBuildCaveHouse( self, p1 ):
		pass
	def OnEnterCaveHouse( self ):
		pass
	def OpenLingQuanUI( self ):
		pass
	def StartBuildUpgrade( self, p1, p2 ):
		pass
	def CLIENT_OnActiveBatteleFormations( self, p1, p2 ):
		pass
	def OnRequestDFDatasByPage( self, p1 ):
		pass
	def OnRequestDFDatas( self, p1, p2, p3 ):
		pass
	def ShowLHMJButton( self ):
		pass
	def InitDongFuData( self, p1, p2, p3 ):
		pass
	def OpenRepairBuildUI( self, p1, p2 ):
		pass
	def OnBeginRepairDFBuild( self, p1, p2 ):
		pass
	def OnRepairDFBuildFinish( self, p1 ):
		pass
	def OnRequestPlayerDFDatas( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_OnCloseBatteleFormations( self ):
		pass
	def OnGuardReviveTime( self, p1 ):
		pass
