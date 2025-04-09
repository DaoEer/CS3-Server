# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
import time
import Define
import csdefine
import KBEMath
import Const

#script
import CoreObject.NPCBaseObject as NPCBaseObject
import CoreInterface.DropBoxPickUpInterface as DropBoxPickUpInterface

class DropBox( NPCBaseObject.NPCBaseObject, DropBoxPickUpInterface.DropBoxPickUpInterface ):
	"""
	掉落物品Entity
	"""
	def __init__( self ):
		"""
		"""
		NPCBaseObject.NPCBaseObject.__init__( self )
		DropBoxPickUpInterface.DropBoxPickUpInterface.__init__( self )
		self.rollRemainTime = Define.ROLL_RANDOM_TIME
		
		self.rollTimerID = 0
		self.dropTimerID = self.addTimerRepeat( 1.0, "timerCallBack", () )
		#杀怪掉落需要有掉落效果,副本结束刷出的箱子不需要有这样的效果
		if self.isDropReward(): self.addTimerCallBack( 0.5, "onMovePoint", () )
		
	def isDropReward(self):
		"""
		是否是杀怪掉落
		"""
		return self.params.get("dropRewardOrSpaceReward", 1) == 0
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_DROP_BOX )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_DROP_BOX)

	def timerCallBack(self):
		"""
		掉落品自动销毁的回调
		"""
		self.dropRemainTime -= 1
		if self.dropRemainTime <=0:
			if self.dropTimerID != 0:
				self.popTimer( self.dropTimerID )
				self.dropTimerID = 0
			self.destroySelf()
		
	def onMovePoint(self):
		"""
		"""
		scale = Const.DROPBOX_END_SCALE
		dragActionID = ""
		levitateActionID = ""
		position = self.position
		positionList = self.getRandomPoints( self.position, 6, 1, self.layer, 0xFFFF )								#在死亡怪物周边6米的范围内
		if len(positionList): 
			position = positionList[0]
			if self.params.get("isGreen", False): 
				position.y += Const.GREEN_DROPBOX_XUANFU_HIGHT	#绿色品质道具的宝箱需浮空
				dragActionID = Const.GREEN_DROPBOX_DRAG_ACTION
				levitateActionID = Const.GREEN_DROPBOX_LEVITATE_ACTION
				scale = Const.GREEN_DROPBOX_END_SCALE
		
		#只给拥有者发送通知
		StartPosition = KBEMath.KBEngine2UnrealPosition(self.position)
		EndPosition = KBEMath.KBEngine2UnrealPosition(position)
		roleList = self.getEntityByNearby(self.ownershipIDs)
		for role in roleList:
			if role.getClient():
				role.client.CLIENT_dropBoxMoveToPoint(self.id, StartPosition, EndPosition, Const.DROPBOX_MOVE_SPEED, scale, Const.DROPBOX_GRAVITY, dragActionID, levitateActionID)
		
		#延时一定的时间，让客户端有做飞行表现的时间
		distance = abs(self.position.flatDistTo(position))
		timeValue = distance * 100 / Const.DROPBOX_MOVE_SPEED if distance * 100 / Const.DROPBOX_MOVE_SPEED > 0.5 else 0.5
		self.addTimerCallBack( timeValue, "onSetPosAndScale", (position, scale, ) )
		
	def onSetPosAndScale(self, position, scale):
		"""
		"""
		self.position = position
		self.modelScale = scale
		
		#没有地阶以上物品掉落
		if not self.params.get("isGreen", False): return
		#浮空效果
		self.levitateActionID = Const.GREEN_DROPBOX_LEVITATE_ACTION

		


