# -*- coding: utf-8 -*-
import random, time, datetime

import KBEngine
from KBEDebug import *

import csdefine
from PlayerAI.State.CStateInterface import CStateBase

#幻兽蛋ID
PET_ITEM_ID = 204010020

class CNull( CStateBase ):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
	def enter(self):
		pass
		
	def leave(self):
		pass
		
class CCleanAISys( CStateBase ):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
	def enter(self):
		#注册事件
		self.ai.owner.eventObj.registerEvent("Event_CTeamAISys_onLeaveTeam", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onLeaveTong", self)
		
		self.leaveTong()
		self.leaveTeam()
		
		#如果没有加入队伍也没有加入帮会
		if not self.ai.owner.tongDBID and not self.ai.owner.teamID:
			self.ai.think()
	
	def leave(self):
		#反注册
		self.ai.owner.eventObj.unregisterEvent("Event_CTeamAISys_onLeaveTeam", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onLeaveTong", self)
		
	def onEvent(self, name, *argv):
		if name == "Event_CTongAISys_onLeaveTong":
			self.ai.think()
		elif name == "Event_CTeamAISys_onLeaveTeam":
			self.ai.think()
	
	def leaveTong(self):
		if self.ai.owner.tongDBID <= 0:
			return
			
		if self.ai.owner.playerDBID == self.ai.owner.tongLeader:
			for member in list(self.ai.owner.tongMember.values()):
				self.ai.owner.base.tongKickMember(str(member["DBID"]))
			self.ai.owner.base.tongDismiss()
		else:
			self.ai.owner.base.tongQuit()
	
	def leaveTeam(self):
		if self.ai.owner.teamID <= 0:
			return
		
		if self.ai.owner.id == self.ai.owner.captainID:
			for member in list(self.ai.owner.teamMembers.values()):
				self.ai.owner.cell.leaveTeamFC(member["entityID"])
				self.ai.owner.outputMsg("leaveTeamFC {}".format(member["entityID"]))
			
			self.ai.owner.cell.disbandTeamFC()
			self.ai.owner.outputMsg("disbandTeamFC")
		else:
			self.ai.owner.cell.leaveTeamFC(self.ai.owner.id)
			self.ai.owner.outputMsg("leaveTeamFC")


class CPetAISys(CStateBase):
	"""
	宠物系统
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		self.hasAddPetItem = False
		
	def enter(self):
		if self.ai.owner.level < 10:
			self.ai.owner.GMCommand(self.ai.owner, "setLevel", "30")
		self.callbackID = KBEngine.callback(3, self.onFight)
		
	def leave(self):
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
		
	def onFight(self):
		"""
		"""
		if self.ai.owner.currentPetUID <= 0:
			if self.ai.owner.isInitPets:
				if len(self.ai.owner.petCages) <= 0:
					if not self.hasAddPetItem:
						self.ai.owner.GMCommand(self.ai.owner, "addItem", str(PET_ITEM_ID))
						self.hasAddPetItem = True
						self.callbackID = KBEngine.callback(3, self.onFight)
						return
					else:
						items = self.ai.owner.items
						for itemOrder, item in items.items():
							if item.id == PET_ITEM_ID:
								self.ai.owner.cell.CELL_useItem( str(item.uid), str(self.ai.owner.id) )
								self.ai.owner.outputMsg("CELL_useItem")
								break
						
						self.callbackID = KBEngine.callback(3, self.onFight)
						return
				else:
					self.ai.owner.GMCommand(self.ai.owner, "clearPetSleep")
					for k, v in self.ai.owner.petCages.items():
						#召唤宠物
						self.ai.owner.cell.conjurePet(str(k))
						self.ai.owner.outputMsg("conjurePet")
						self.callbackID = KBEngine.callback(3, self.onFight)
						return
			else:
				pass
				
		self.ai.think()
		
class CTeamAISys(CStateBase):
	"""
	组队系统
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		
	def enter(self):
		#延时一个随机时间后，开始组队
		self.callbackID = KBEngine.callback(random.randint(1, 10), self.createTeam)
		
		#注册事件
		self.ai.owner.eventObj.registerEvent("Event_CTeamAISys_onJoinTeam", self)
		self.ai.owner.eventObj.registerEvent("Event_CTeamAISys_onTeamInvite", self)
		self.ai.owner.eventObj.registerEvent("Event_CTeamAISys_onLeaveTeam", self)
		self.ai.owner.eventObj.registerEvent("Event_CTeamAISys_onInviteTeammate", self)
		
	def leave(self):
		self.clearTimer()
		
		#反注册
		self.ai.owner.eventObj.unregisterEvent("Event_CTeamAISys_onJoinTeam", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTeamAISys_onTeamInvite", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTeamAISys_onLeaveTeam", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTeamAISys_onInviteTeammate", self)
	
	def onEvent(self, name, *argv):
		if name == "Event_CTeamAISys_onJoinTeam":
			self.onJoinTeam()
		elif name == "Event_CTeamAISys_onTeamInvite":
			self.onTeamInvite(*argv)
		elif name == "Event_CTeamAISys_onInviteTeammate":
			self.onTeamInviteTeammate(*argv)
		elif name == "Event_CTeamAISys_onLeaveTeam":
			self.ai.think()
		
	def createTeam(self):
		self.callbackID = 0
		
		#自己不在队伍中
		if self.ai.owner.teamID == 0:
			self.ai.owner.GMCommand(self.ai.owner, "createTeam")
		else:
			self.teamInvite()
		
	def onJoinTeam(self):
		#邀请他人加入
		self.teamInvite()
		
		self.clearTimer()
		self.callbackID = KBEngine.callback(3, self.onWait)
		
	def teamInvite(self):
		#从还未加入队伍的玩家中随机挑出8个发送邀请
		entities = self.ai.owner.entitiesInRange( 5, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_ROLE and not entity.hasFlag(csdefine.ROLE_FLAG_TEAMMING) else False )
		entities = random.sample(entities, 8 if len(entities) >= 8 else len(entities))
		for entity in entities:
			self.ai.owner.cell.teamInviteFC(entity.id)
			self.ai.owner.outputMsg("teamInviteFC {}".format(entity.id))
		
	def onTeamInvite(self, inviteID):
		#同意邀请
		if self.ai.owner.teamID == 0:
			self.ai.owner.cell.replyTeamInviteByFC(True, inviteID)
			self.ai.owner.outputMsg("replyTeamInviteByFC")
			
	def onTeamInviteTeammate(self, targetID, targetName, inviteID):
		if self.ai.owner.teamID != 0:
			self.ai.owner.cell.replyTeammateInvite(targetID, targetName, inviteID, True)
			self.ai.owner.outputMsg("replyTeammateInvite")
	
	def clearTimer(self):
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
	
	def onWait(self):
		self.callbackID = 0
		self.ai.think()
	
class CTongAISys(CStateBase):
	"""
	公会系统
	"""
	TONGNUM = 0
	
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		self.reqTongsTimes = 0
		
	def enter(self):
		self.ai.owner.GMCommand(self.ai.owner, "setLevel", "30")
		
		if (random.randint(1, 10) % 5) == 0:
			self.createTong()
		else:
			#延时一个随机时间后，开始加入帮会
			self.callbackID = KBEngine.callback(10, self.onCallBack)
		
		#注册事件
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onReceTongInfos", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onTongJoin", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onReqJoinTong", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onLeaveTong", self)
		
	def leave(self):	
		self.clearTimer()
		self.reqTongsTimes = 0
		
		#反注册
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onReceTongInfos", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onTongJoin", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onReqJoinTong", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onLeaveTong", self)
	
	def onEvent(self, name, *argv):
		if name == "Event_CTongAISys_onTongJoin":
			self.inviteJoinTong()
		elif name == "Event_CTongAISys_onReqJoinTong":
			#有人申请加入帮会，直接同意好了
			self.ai.owner.base.replyJoinTong(str(*argv), True)
		elif name == "Event_CTongAISys_onReceTongInfos":
			self.joinTong()
		elif name == "Event_CTongAISys_onLeaveTong":
			self.ai.think()
	
	def onCallBack(self):
		self.callbackID = 0
		#请求帮会列表
		self.ai.owner.base.RequireTongInfo()
		
	def createTong(self):
		if self.ai.owner.tongDBID > 0:
			self.inviteJoinTong()
			return
		
		#创建帮会
		self.ai.owner.GMCommand(self.ai.owner, "setXiuwei", "100000000")
		self.ai.owner.GMCommand(self.ai.owner, "setMoney", "300000000")
		name = str(int(time.time()) * 100 + CTongAISys.TONGNUM)
		CTongAISys.TONGNUM += 1
		self.ai.owner.cell.tongCreate(name)
		self.ai.owner.outputMsg("tongCreate")
	
	def joinTong(self):
		if self.ai.owner.tongDBID > 0:
			self.inviteJoinTong()
			return
		
		#如果还没有创建帮会，那么就创建帮会
		if len(self.ai.owner.tongs) <= 0:
			if self.reqTongsTimes <= 3:
				self.reqTongsTimes += 1
				self.callbackID = KBEngine.callback(5, self.onCallBack)
			else:
				self.createTong()
			return
		
		#随机出5个，申请加入
		tongDBIDList = list(self.ai.owner.tongs.keys())
		amount = 5 if len(tongDBIDList) >= 5 else len(tongDBIDList)
		if amount > 0:
			temp = random.sample(tongDBIDList, amount)
			for id in temp:
				self.ai.owner.base.tongReqJoin(str(id))
		else:
			self.clearTimer()
			self.callbackID = KBEngine.callback(5, self.onCallBack)
			
	def inviteJoinTong(self):
		if self.ai.owner.tongDBID <= 0:
			self.joinTong()
			return
	
		#从玩家中随机挑出6个发送邀请
		entities = self.ai.owner.entitiesInRange( 50, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_ROLE and not self.ai.owner.isInSelfTong(entity.id) else False )
		entities = random.sample(entities, 6 if len(entities) >= 6 else len(entities))
		for entity in entities:
			self.ai.owner.cell.tongInviteJoin(entity.id)
			self.ai.owner.outputMsg("tongInviteJoin {}".format(entity.id))
		
		self.clearTimer()
		self.callbackID = KBEngine.callback(10, self.leave)

	def clearTimer(self):
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0

class CItemAISys(CStateBase):
	"""
	物品系统
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0

	def enter(self):
		self.addItem()
		self.ai.owner.eventObj.registerEvent("Event_CItemAISys_onInitKitBag", self)
		self.ai.owner.eventObj.registerEvent("Event_CItemAISys_onAddItem", self)
		self.ai.owner.eventObj.registerEvent("Event_CItemAISys_onRemoveItem", self)
		
	def leave(self):
		self.ai.owner.eventObj.unregisterEvent("Event_CItemAISys_onInitKitBag", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CItemAISys_onAddItem", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CItemAISys_onRemoveItem", self)
		
	def onEvent(self, name, *argv):
		"""
		"""
		if name == "Event_CItemAISys_onAddItem":
			pass
		elif name == "Event_CItemAISys_onRemoveItem":
			pass
		elif name == "Event_CItemAISys_onInitKitBag":
			self.addItem()
			
	def addItem(self):
		"""
		"""
		if not self.ai.owner.initKitBag:
			return
	
		amount = self.ai.owner.commonCapacity - len(self.ai.owner.items)
		if amount<=0:
			self.ai.think()
			return
		
		for i in range(amount):
			self.ai.owner.GMCommand(self.ai.owner, "addItem", "{} {}".format(str(PET_ITEM_ID), str(20)))
		if self.callbackID == 0:
			self.callbackID = KBEngine.callback(5, self.onCallBack)

	def onCallBack(self):
		self.callbackID = 0
		self.ai.think()
		
CHAT_SPACE_TIME = 5 * 60
CHAT_MESSAGE_LIST = [
"[%s]hello world",
"[%s]还能不能愉快的聊天",
"[%s]测试测试测试测试",
"[%s]想些测试的信息好艰难呀",
"[%s]算了不想了，就这些了",
"[%s]习主席说2020年消灭贫困人口，想到这里手微微颤抖，代码不自觉的又多写了两行",
"[%s]python是最可爱的语言",
]
class CChatAISys(CStateBase):
	"""
	聊天系统
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)

	def enter(self):
		pass
	
	def leave(self):
		pass
	
	def onTickCallBack(self, tick):
		self.sendMsg()
		
	def sendMsg(self):
		now = datetime.datetime.now()
		msg = random.choice(CHAT_MESSAGE_LIST)
		msg = msg %(now.strftime("%Y-%m-%d %H:%M"))
		self.ai.owner.cell.onRoleSendChatMessage( "bot", str(csdefine.CHAT_TYPE_WORLD), msg, "")
		self.ai.owner.outputMsg("chat message")
	