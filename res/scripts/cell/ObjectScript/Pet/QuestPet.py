# -*- coding: utf-8 -*-

import csdefine
import Math
import QuestEventDefine
from ObjectScript.Pet import PetBase
import KBEDebug


class QuestPet( PetBase.PetBase ):
	"""任务幻兽"""
	def __init__( self ):
		PetBase.PetBase.__init__( self )
		
	def onConjurePet( self, owner ):
		"""
		virtual method
		召唤出幻兽
		"""
		owner.triggerQuestEvent( QuestEventDefine.EVENT_CONJURE_PET, (self.scriptID,) )
		
	def onMountPet( self, owner ):
		"""
		virtual method
		骑宠状态
		"""
		owner.triggerQuestEvent( QuestEventDefine.EVENT_MOUNT_PET, (self.scriptID,) )
