# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from Extra.KSTEvent import KSTEvent
class GameObject:
	
	def __init__(self):
		self.eventObj = KSTEvent()
		
	def hasFlag(self, flag):
		"""
		判断一个entity是否有指定的标志
		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		@return: BOOL
		"""
		flag = 1 << flag
		return ( self.flags & flag ) == flag
		
	def OnStartMoving(self):
		pass
		
	def OnStopMoving(self):
		pass
		
	def SetIntPropertyByKey(self, s, i):
		pass
		
	def SetFloatPropertyByKey(self, s, f):
		pass
		
	def SetFStringPropertyByKey(self, ss, ds):
		pass
		
	def OnPlayAction(self, arg0_string,arg1_float):
		pass
		
	def StopAction(self):
		pass
		
	def StopFrontAction(self):
		pass
		
	def ShowInvisible(self):
		pass
			
	def HideInvisible(self):
		pass
		
	def OnRelationChange(self):
		pass
		
	def OnPlayParticles(self,arg0_int32,arg1_string,arg2_string,arg3_float,arg4_vector3):
		pass
		
	def ShowTopCountDown(self, lifeTime, time):
		pass
		
	def HideTopCountDown(self):
		pass
		
	def PlayOneByOneAction( self, p1, p2 ):
		pass
	def ChangeToDstModelScale( self, p1, p2, p3 ):
		pass
	def ChangeToNormalModelScale( self, p1, p2 ):
		pass
	def CastToStone( self, p1, p2 ):
		pass
	def CastToNormal( self, p1 ):
		pass
	def BindDisplayObject( self, p1 ):
		pass
	def UnbindDisplayObject( self, p1 ):
		pass
	def ChangeShowPosture( self, p1, p2, p3 ):
		pass
	def OnStopParticles( self ):
		pass
	def CLIENT_OnPlay3DSound( self, p1 ):
		pass
	def CLIENT_OnStop3DSound( self ):
		pass
	def CLIENT_SetIntPropertyByKey( self, p1, p2 ):
		pass
	def CLIENT_SetFloatPropertyByKey( self, p1, p2 ):
		pass
	def CLIENT_SetFStringPropertyByKey( self, p1, p2 ):
		pass
	def CLIENT_OnPlayAction( self, p1, p2 ):
		pass
	def CLIENT_OnStopParticles( self ):
		pass
	def CLIENT_StopAction( self ):
		pass
	def CLIENT_StopFrontAction( self ):
		pass
	def CLIENT_ShowInvisible( self ):
		pass
	def CLIENT_HideInvisible( self ):
		pass
	def CLIENT_OnRelationChange( self ):
		pass
	def CLIENT_OnPlayParticles( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_ShowTopCountDown( self, p1, p2 ):
		pass
	def CLIENT_HideTopCountDown( self ):
		pass
	def CLIENT_PlayOneByOneAction( self, p1, p2, p3 ):
		pass
	def CLIENT_ChangeToDstModelScale( self, p1, p2, p3, p4, p5 ):
		pass
	def CLIENT_ChangeToNormalModelScale( self, p1, p2 ):
		pass
	def CLIENT_CastToStone( self, p1, p2 ):
		pass
	def CLIENT_CastToNormal( self, p1, p2 ):
		pass
	def CLIENT_BindDisplayObject( self, p1 ):
		pass
	def CLIENT_UnbindDisplayObject( self, p1 ):
		pass
	def CLIENT_ChangeShowPosture( self, p1, p2, p3 ):
		pass
	def CLIENT_SetBoolPropertyByKey( self, p1, p2 ):
		pass
	def CLIENT_SynchroLocalPos( self, p1 ):
		pass
	def UpdateRelation( self ):
		pass
	def CLIENT_ChangeShowAnimAndActionPosture( self, p1, p2, p3 ):
		pass
