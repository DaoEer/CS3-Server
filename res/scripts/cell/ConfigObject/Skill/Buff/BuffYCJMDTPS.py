
# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold
from ConfigObject.Skill.SkillLoader import g_skills
from ItemFactory import ItemFactoryInst as g_itemFactory



class BuffYCJMDTPS( BuffHold ):
	"""
	CST-8973 勇闯绝命岛射击Buff
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.skillID = 0 #对应释放的技能
		self._highLighID = 0 #对应高亮技能ID
		self._rClickBuffID = 0 # 鼠标右键模式的buffID
		self.equipWeaponItemID = 0 #使用的武器物品ID
		self._ModelId = ""
		self._inActionId = ""
		self._outActionId = ""
		self._weaponId = 0
		self._sockeName = ""
		self._partId = ""
		self._skillIDList = {}  # {1:{"QbType":"2",ID:"10000000"}, 2:{"QbType":"2",ID:"10000000"}...}
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_SCENE
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODEL)
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODE)
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_BAR)

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		Param1Str = dictDat["Param1"].split("|")
		self.skillID = int( Param1Str[0] )
		if len(Param1Str) > 1:
			self._highLighID = int( Param1Str[1] )
		if len(Param1Str) > 2:
			self._rClickBuffID = int( Param1Str[2] )

		self.equipWeaponItemID = int( dictDat["Param2"] )
		strList = dictDat["Param3"].split("|")
		self._ModelId = strList[0]
		if len(strList) > 1:
			self._inActionId = strList[1]
		if len(strList) > 2:
			self._outActionId = strList[2]

		Param4 = dictDat["Param4"].split("|")
		if len(Param4) > 2:
			self._weaponId = int(Param4[0])
			self._sockeName = Param4[1]
			self._partId = Param4[2]

		skillIDStrList =  dictDat["Param5"].split("|") if dictDat["Param5"] else [] #["QbType:Id","","QbType:ID"]
		if len( skillIDStrList ) > 9:
			skillIDStrList = skillIDStrList[:9]
			KBEDebug.ERROR_MSG( "buff(%i) cannot replace more skillBar(%i)!"%(self._id, len(skillIDStrList)) )
		for skillIDStr in skillIDStrList:
			if skillIDStr:
				data = {}
				index = skillIDStrList.index(skillIDStr)
				data["QbType"] = skillIDStr.split(":")[0]
				if int(data["QbType"]) == 0:
					continue
				data["ID"] = skillIDStr.split(":")[1]
				if int(data["QbType"]) == csdefine.QB_ITEM_SKILL:
					skillInstance = g_skills[int(data["ID"])]
					if not skillInstance:
						KBEDebug.ERROR_MSG( "buff (%i), SkillTable has not this skill (%s)" % (self._id, data["ID"]) )
				elif int(data["QbType"]) == csdefine.QB_ITEM_KITBAG:
					itemInstance = g_itemFactory.getItemData(int(data["ID"]))
					if not itemInstance:
						KBEDebug.ERROR_MSG( "buff (%i), ItemData has not this item (%s)" % (self._id, data["ID"]) )
				for skillData in self._skillIDList.values():
					if skillData["ID"] == data["ID"]:
						KBEDebug.ERROR_MSG("buff(%i) config cannot has the same ID(%s)"%(self._id, data["ID"]))
				self._skillIDList[index] = data
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if len(receiver.findBuffsByBuffID(self._id)):
			return False
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		# 替换快捷栏
		if receiver.getClient():
			receiver.client.OnEnterYCJMDShowSkillBar()
			receiver.client.AddYCJMDSkillBars( 10, csdefine.QB_ITEM_EQUIP, self.equipWeaponItemID )
			for k, v in self._skillIDList.items():
				receiver.client.AddYCJMDSkillBars( k, int(v["QbType"]), int(v["ID"]) )

		# 处理变换操作模式
		if receiver.getClient():
			receiver.client.EnterYCJMDModelTPS( self.skillID, self.equipWeaponItemID )
			receiver.client.ChangeYCJMDModelTPSSkillID( self.skillID )
			receiver.client.ShowSkillBarsHighLigh( self._highLighID )

		# 处理变换姿势
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowAnimAndActionPosture( self._ModelId, self._inActionId, "" )
		receiver.allClients.SetWeapontYCJMD(self._weaponId, self._sockeName, self._partId)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )	
		# 替换快捷栏
		if receiver.getClient():
			receiver.client.OnEnterYCJMDShowSkillBar()
			receiver.client.AddYCJMDSkillBars( 10, csdefine.QB_ITEM_EQUIP, self.equipWeaponItemID )
			for k, v in self._skillIDList.items():
				receiver.client.AddYCJMDSkillBars( k, int(v["QbType"]), int(v["ID"]) )
		
		# 处理变换操作模式
		if receiver.getClient():
			receiver.client.EnterYCJMDModelTPS( self.skillID, self.equipWeaponItemID )
			receiver.client.ChangeYCJMDModelTPSSkillID( self.skillID )
			receiver.client.ShowSkillBarsHighLigh( self._highLighID )

		# 处理变换姿势
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		receiver.allClients.CLIENT_ChangeShowAnimAndActionPosture( self._ModelId, self._inActionId, "" )
		receiver.allClients.SetWeapontYCJMD(self._weaponId, self._sockeName, self._partId)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		# 替换快捷栏
		if receiver.getClient():
			receiver.client.RemoveYCJMDSkillBars( list(self._skillIDList) )

		# 处理变换操作模式
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE and receiver.getClient():
			receiver.client.LeaveYCJMDModelTPS()
			receiver.client.OnReplaceSkillBarEnd()
			receiver.client.OnLeaveYCJMDHideSkillBar()

		# 处理变换姿势
		if reason != csdefine.BUFF_END_RESON_BY_REPLACE:
			receiver.allClients.CLIENT_ChangeShowAnimAndActionPosture( receiver.getActionNumber(), "", self._outActionId)
			receiver.allClients.SetWeapontYCJMD(0, "", "")

		# 移除鼠标右键的buff
		if len(receiver.findBuffsByBuffID(self._rClickBuffID)):
			receiver.removeBuffByID(self._rClickBuffID)
		BuffHold.doEnd( self, receiver, buffData,reason )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffHold.onClientActorCreate( self, receiver, buffData, srcEntityID )
		
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )
		
		# 处理变换姿势 
		clientEntity.CLIENT_ChangeShowAnimAndActionPosture( self._ModelId, "", "" )
		clientEntity.SetWeapontYCJMD(self._weaponId, self._sockeName, self._partId)

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_STATE_CHANGE, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_YCJMD_RCLICK, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_YCJMD_CARRIER, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_STATE_CHANGE, buffData.index )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_YCJMD_RCLICK, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_YCJMD_CARRIER, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_STATE_CHANGE:
			newState = pDict["newState"]
			if newState == csdefine.ENTITY_STATE_DEAD:
				pass
			elif csdefine.ENTITY_STATE_FREE:
				pass
		elif eventType == csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL:
			receiver.removeBuffByIndex( buffData.index )
			self.doInterrupt( receiver, buffData )
		elif eventType == csdefine.SKILL_EVENT_YCJMD_RCLICK:
			mode = pDict["mode"]
			if self._rClickBuffID:
				if mode:
					receiver.addBuff(receiver, self._rClickBuffID)
				else:
					receiver.removeBuffByID(self._rClickBuffID)
		elif eventType == csdefine.SKILL_EVENT_ROLE_YCJMD_CARRIER:
			isMount = pDict["isMount"]
			if not isMount:
				# 处理变换操作模式
				if receiver.getClient():
					receiver.client.EnterYCJMDModelTPS( self.skillID, self.equipWeaponItemID )
					receiver.client.ChangeYCJMDModelTPSSkillID( self.skillID )
					receiver.client.ShowSkillBarsHighLigh( self._highLighID )
				# 处理变换姿势
				receiver.allClients.CLIENT_ChangeShowAnimAndActionPosture( self._ModelId, self._inActionId, "" )
				receiver.allClients.SetWeapontYCJMD(self._weaponId, self._sockeName, self._partId)
			else:
				# 处理变换操作模式
				if receiver.getClient():
					receiver.client.LeaveYCJMDModelTPS()
				# 处理变换姿势
				receiver.allClients.CLIENT_ChangeShowAnimAndActionPosture( receiver.getActionNumber(), "", self._outActionId)
				receiver.allClients.SetWeapontYCJMD(0, "", "")

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )