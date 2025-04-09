# -*- coding: utf-8 -*-


import KBEngine
import csdefine
import random
import Math


class RoleCommanderInterface:
	"""
	"""
	def __init__(self):
		self.armsData = {}	#{scriptID, amount} 携带兵力数据
		self.controlledData = {} #{scriptID, [id1,id2]}玩家控制的controlledBy数据 
		self.armyModelList = []

	def beforeDestroy(self):
		"""
		"""
		self.destroyArms()
		
	def onEnterDead(self):
		"""
		"""
		self.destroyArms()
		self.resetArmyModelList()


	def callGCZDefultArmy( self, armyData, id ):
		"""
		召唤攻城战默认部队数据
		"""
		if not armyData:
			return
		self.setCallArmyIndex( id )
		if self.getClient():
			self.client.InitRoleCmdArmsScriptID(armyData.firstGuardScriptID, armyData.secondGuardScriptID, armyData.soldierScriptID)

		self.createEntityByScriptID(armyData.firstGuardScriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.LEFT_GUARD,"belongSide":self.getBelongSide(),"soldierType":csdefine.BARRACKS_SOLDIER_GUARD_TYPE})
		self.createEntityByScriptID(armyData.secondGuardScriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.RIGHT_GUARD,"belongSide":self.getBelongSide(),"soldierType":csdefine.BARRACKS_SOLDIER_GUARD_TYPE})
		for soldierID in armyData.soldierIDs:
			self.createEntityByScriptID(armyData.soldierScriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.SOLDIER,"index":soldierID,"belongSide":self.getBelongSide(),"soldierType":csdefine.BARRACKS_SOLDIER_COMMON_TYPE})

		self.showRoleCmdUI(1)

	def callRoleArmySoldier( self, id ):
		"""
		召出自己部队的兵数据
		"""
		roleArmyDatas = self.roleArmyDatas.get( id,None )
		if not roleArmyDatas:
			return
		self.setCallArmyIndex( id )
		if self.getClient():
			self.client.InitRoleCmdArmsScriptID(roleArmyDatas.firstGuardScriptID, roleArmyDatas.secondGuardScriptID, roleArmyDatas.soldierScriptID)

		firstGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, roleArmyDatas.firstGuardScriptID )
		if len( firstGudSoldiers ) and firstGudSoldiers[0].isActive:
			self.createEntityByScriptID(roleArmyDatas.firstGuardScriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.LEFT_GUARD,"index":firstGudSoldiers[0].id,"belongSide":self.getBelongSide(),"level":firstGudSoldiers[0].level,"soldierType":csdefine.BARRACKS_SOLDIER_GUARD_TYPE})
		secondGudSoldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, roleArmyDatas.secondGuardScriptID )
		if len( secondGudSoldiers ) and secondGudSoldiers[0].isActive:
			self.createEntityByScriptID(roleArmyDatas.secondGuardScriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.RIGHT_GUARD,"index":secondGudSoldiers[0].id,"belongSide":self.getBelongSide(),"level":secondGudSoldiers[0].level,"soldierType":csdefine.BARRACKS_SOLDIER_GUARD_TYPE})
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, roleArmyDatas.soldierScriptID )
		for soldier in soldiers:
			if soldier.id not in roleArmyDatas.soldierIDs:
				continue
			randPos = Math.Vector3(random.uniform(1,5), random.uniform(1,5), 0)
			self.createEntityByScriptID(roleArmyDatas.soldierScriptID, self.position+randPos, self.direction, {"controlEntityID":self.id,"category":csdefine.SOLDIER,"index":soldier.id,"belongSide":self.getBelongSide(),"level":soldier.level,"soldierType":csdefine.BARRACKS_SOLDIER_COMMON_TYPE})

		self.showRoleCmdUI(1)

	def showRoleCmdUI(self, isShow):
		"""
		打开关闭RoleCommanderInterfaceUI
		"""
		if self.getClient():
			self.client.ShowRoleCmdUI(isShow)

	def equipArms(self, soldierScriptID, soldierAmount, leftGuardScriptID, rightGuardScriptID):
		"""
		配备兵力
		"""
		self.armsData["soldierScriptID"] = soldierScriptID
		self.armsData["soldierAmount"] =  soldierAmount
		self.armsData["leftGuardScriptID"] = leftGuardScriptID
		self.armsData["rightGuardScriptID"] = rightGuardScriptID

		self.client.InitRoleCmdArmsScriptID(leftGuardScriptID, rightGuardScriptID, soldierScriptID)

	def createArms(self):
		"""
		创建部队单位
		"""
		self.createEntityByScriptID(self.armsData["leftGuardScriptID"], self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.LEFT_GUARD})
		self.createEntityByScriptID(self.armsData["rightGuardScriptID"], self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.RIGHT_GUARD})

		scriptID = self.armsData["soldierScriptID"]
		amount = self.armsData["soldierAmount"]
		for index in range(amount):
			self.createEntityByScriptID(scriptID, self.position, self.direction, {"controlEntityID":self.id,"category":csdefine.SOLDIER})

		self.showRoleCmdUI(1)

	def destroyArms(self):
		"""
		销毁部队单位
		"""
		self.showRoleCmdUI(0)
		
		for idList in self.controlledData.values():
			for entityID in idList:
				entity = KBEngine.entities.get(entityID, None)
				if entity:
					entity.destroySelf()

	def roleCmdOnControlled(self, scriptID, entityID):
		"""
		"""
		if not scriptID in self.controlledData.keys():
			self.controlledData[scriptID] = []

		if not entityID in self.controlledData[scriptID]:
			self.controlledData[scriptID].append(entityID)

	def roleCmdUseSkillToPosition(self, skillID, targetPos):
		"""
		技能指令 对位置施法
		"""
		if not self.getClient():
			return	
		self.client.RoleCmdUseSkillToPosition(skillID, targetPos)

	def roleCmdUseSkillToEntity(self, skillID, entityID):
		"""
		技能指令 对目标施法
		"""
		if not self.getClient():
			return	
		self.client.RoleCmdUseSkillToEntity(skillID, entityID)

	def roleCmdUseSkillToSelf(self, skillID):
		"""
		技能指令 对目标施法
		"""
		if not self.getClient():
			return	
		self.client.RoleCmdUseSkillToSelf(skillID)


	def roleCmdClimb(self):
		"""
		攀爬指令，爬云梯
		"""
		if not self.getClient():
			return	
		self.client.RoleCmdClimb()

	def roleDestroyArms(self):
		"""
		销毁部队
		"""
		self.destroyArms()
		if not self.getClient():
			return
		#self.client.RoleDestroyArms()

	def beforeSoldierDestroy(self, soldierID):
		"""
		士兵销毁前 通知清掉客户端的数据
		"""
		if not self.getClient():
			return
		self.client.RoleRemoveSoldier(soldierID)





