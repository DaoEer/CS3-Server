#-*- coding: utf-8 -*-
from StateInterface.MonsterStateInterface import MonsterStateInterface
import csdefine

class CMonsterStateInterface(MonsterStateInterface):
	def __init__(self):
		MonsterStateInterface.__init__(self)
	
	def CState_change( self, exposed, oldSatee, newState ):
		"""
		exposed method
		客户端请求切换状态
		"""
		if not self.IsValidMsg( exposed, oldSatee, newState ):
			return
			
		if self.getState() != oldSatee:
			return 
		
		self.changeState( newState )