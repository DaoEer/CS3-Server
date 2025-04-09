# -*- coding: utf-8 -*-

# 副本事件行为  九字真言
import csdefine
import KBEDebug
import KBEngine
from ConfigObject.SpaceCopyYXLMMonsterDataLoader import g_spaceCopyYXLMMonsterDataLoader
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import Functions
from ConfigObject import PatrolRouteLoader
import Math
import csstatus
import ItemTypeEnum
import random
import KBEMath

class SEAction414( SEActionBase ):
	"""
	英雄王座  (小兵)怪物被击杀 奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardExpRangeByRoleKill = float( section["param1"] ) 		#玩家击杀怪 周围友方怪奖励经验的范围
		self.rewardJadeRangeByMonsterKill = float( section["param2"] ) 	#怪物击杀怪 周围友方玩家获得奖励的魂玉
		#self.rewardExp = int( section["param3"] ) # 增加经验

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if not dieEntity and not killEntity:
			KBEDebug.ERROR_MSG("trigger(%i) or killer(%i) is exit"%( triggerID,  eventParams["killerID"] ))
			return
		if dieEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			KBEDebug.ERROR_MSG("trigger(%i) is not Monster"%( triggerID ))
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if not killEntity:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			jadeValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterRewardJadeToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			number = spaceEntity.hasSpecialMonsterNumber( killEntity )
			killEntity.addJade( int(jadeValue * (1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple)) )
			killRewardExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			spaceEntity.addMemberRewardExp( killEntity, killRewardExp )
			expValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToAssistMonster( dieEntity.scriptID, dieEntity.levelYXLM )
			entitylist = [e for e in dieEntity.entitiesInRangeExt( self.rewardExpRangeByRoleKill, "MonsterExtYXLMSoldier") if e.getBelongSide() == killEntity.getBelongSide()]
			for e in entitylist:
				e.addExp(expValue)
			entitylist = [e for e in dieEntity.entitiesInRangeExt( self.rewardJadeRangeByMonsterKill, "Role") if e.getBelongSide() == killEntity.getBelongSide() and e.id != killEntity.id]
			if len(entitylist) <= 0:
				return
			assistExpValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToAssistPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			assistJade = g_spaceCopyYXLMMonsterDataLoader.getMonsterRewardJadeToAssistPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			for e in entitylist:
				spaceEntity.addMemberRewardExp( e,assistExpValue )
				e.addJade( assistJade )
			#spaceEntity.addKillRewardExp( killEntity.getBelongSide(), self.rewardExp )
		elif killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			expValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToKillerMonster( dieEntity.scriptID, dieEntity.levelYXLM )
			killEntity.addExp(expValue)
			#spaceEntity.addKillRewardExp( killEntity.getBelongSide(), self.rewardExp )
			entitylist = [e for e in dieEntity.entitiesInRangeExt( self.rewardJadeRangeByMonsterKill, "Role") if e.getBelongSide() == killEntity.getBelongSide()]
			if len(entitylist) <= 0:
				return
			jadeValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterRewardJadeToAssistPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			assistExpValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToAssistPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			value = int(jadeValue/len( entitylist ))
			for e in entitylist:
				number = spaceEntity.hasSpecialMonsterNumber( killEntity )
				e.addJade( int(value * (1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple))  )
				spaceEntity.addMemberRewardExp( e, assistExpValue )

class SEAction415( SEActionBase ):
	"""
	英雄王座  玩家被击杀 奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.firstKillReward = 0
		self.otherKillReward = 0
		if section["param1"]:
			self.firstKillReward = int( section["param1"].split("|")[0] )  #首杀的奖励
			if len(section["param1"].split("|")) > 1:
				self.otherKillReward = int( section["param1"].split("|")[1] )  #其他情况击杀奖励

		self.rewardExp = 0
		self.rewardFeats = 0
		if section["param2"]:
			self.rewardExp = int(section["param1"].split("|")[0]) # 击杀奖励经验值
			if len( section["param2"].split("|") ) > 1:
				self.rewardFeats = int( section["param2"].split("|")[1] ) #击杀奖励的功勋

		self.creepScriptIDs = section["param3"].split("|") #野怪scriptID
		#self.rewardExp = int( section["param4"] )
		self.assistRange = 0.0
		self.assistJade = 0
		if section["param4"]:
			self.assistRange = float( section["param4"].split("|")[0] ) # 助攻范围
			if len(section["param4"].split("|")) > 1:
				self.assistJade = int( section["param4"].split("|")[1] ) # 助攻奖励魂玉

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if not dieEntity and not killEntity:
			KBEDebug.ERROR_MSG("trigger(%i) or killer(%i) is exit"%( triggerID,  eventParams["killerID"] ))
			return
		if dieEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			KBEDebug.ERROR_MSG("trigger(%i) is not Role"%( triggerID ))
			return
		campStr = ""
		killStr = ""
		if dieEntity.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
			campStr = "进攻方"
			killStr = "防守方"
		elif dieEntity.getBelongSide() == csdefine.BELONG_SIDE_PROTECT:
			campStr = "防守方"
			killStr = "进攻方"
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if not killEntity:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			for member in spaceEntity.memberDatas.getAllMembers():
				if member.roleMB:
					member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_ROLE, campStr, dieEntity.getName(),killStr,killEntity.getName())
			spaceEntity.memberDatas.kill( dieEntity.id, killEntity.id )
			#spaceEntity.addKillRewardExp( killEntity.getBelongSide(), self.rewardExp )
			member = spaceEntity.memberDatas.getMemberByPlayerDBID( killEntity.playerDBID )
			if not member:
				KBEDebug.ERROR_MSG(" space has not this member(%i) "%killEntity.id)
				return
			if spaceEntity.memberDatas.checkFirstKill(member):
				number = spaceEntity.hasSpecialMonsterNumber( killEntity )
				killEntity.addJade( int(self.firstKillReward * (1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple)) )
			else:
				number = spaceEntity.hasSpecialMonsterNumber( killEntity )
				killEntity.addJade( int(self.otherKillReward * (1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple)) )

			spaceEntity.addMemberRewardExp( killEntity, self.rewardExp )
			killEntity.addFeats( self.rewardFeats, csdefine.FEATS_ADD_REASON_YXWZ )
			entitylist = [e for e in dieEntity.entitiesInRangeExt( self.assistRange, "Role") if e.getBelongSide() == killEntity.getBelongSide() and e.id != killEntity.id]
			if len(entitylist) <= 0:
				return
			for e in entitylist:
				e.addJade( self.assistJade )
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			spaceEntity.memberDatas.die(dieEntity.id)
			if killEntity.scriptID in self.creepScriptIDs:
				for member in spaceEntity.memberDatas.getAllMembers():
					if member.roleMB:
						member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_CREEPS, campStr, dieEntity.getName())
			else:
				#spaceEntity.addKillRewardExp( killEntity.getBelongSide(), self.rewardExp )
				for member in spaceEntity.memberDatas.getAllMembers():
					if member.roleMB:
						member.roleMB.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_ROLE_BEKILL_BY_BUILIDING, campStr, dieEntity.getName(), killStr)
		


class SEAction416( SEActionBase ):
	"""
	英雄王座  (Boss)怪物被击杀 奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if not dieEntity and not killEntity:
			KBEDebug.ERROR_MSG("trigger(%i) or killer(%i) is exit"%( triggerID,  eventParams["killerID"] ))
			return
		if dieEntity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER:
			KBEDebug.ERROR_MSG("trigger(%i) is not Monster"%( triggerID ))
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if not killEntity:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			killRewardExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			spaceEntity.addKillRewardExp( killEntity.getBelongSide(), killRewardExp )
			jadeValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterRewardJadeToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
			for playerMB in killEntity.getAllTeamMemberMB():
				entity = KBEngine.entities.get( playerMB.id, None )
				if entity:
					number = spaceEntity.hasSpecialMonsterNumber( entity )
					entity.addJade( int(jadeValue * (1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple)) )

class SEAction417( SEActionBase ):
	"""
	英雄王座  (防御塔)怪物被击杀 奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		if not dieEntity:
			KBEDebug.ERROR_MSG("trigger(%i) or killer(%i) is exit"%( triggerID,  eventParams["killerID"] ))
			return
		camp = csdefine.BELONG_SIDE_ATTACK
		if dieEntity.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
			camp = csdefine.BELONG_SIDE_PROTECT	
		memberList = spaceEntity.memberDatas.getMembersByCamp( camp )
		killRewardExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterExpRewardToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
		spaceEntity.addKillRewardExp( camp, killRewardExp )
		jadeValue = g_spaceCopyYXLMMonsterDataLoader.getMonsterRewardJadeToKillerPlayer( dieEntity.scriptID, dieEntity.levelYXLM )
		for member in memberList:
			number = spaceEntity.hasSpecialMonsterNumber( member.roleMB )
			member.roleMB.addJade( int(jadeValue *(1 + number * spaceEntity.getScript().jadeScriptIDRewardJadeMultiple)) )
			member.roleMB.statusMessage(csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_KILL,"")
		dieMemberList = spaceEntity.memberDatas.getMembersByCamp( dieEntity.getBelongSide() )
		for member in dieMemberList:
			member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_BUILIDING_KILL )

class SEAction418( SEActionBase ):
	"""
	英雄王座  收到小兵升级的通知
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.xianScriptID = section["param1"] #仙道小兵scriptID
		self.moScriptID = section["param2"] #魔道小兵sciptID
		self.xianSpecialScriptIDData = section["param3"].split("|") #超过数量|召唤仙道特殊小兵
		self.moSpecialScriptIDData = section["param4"].split("|") #超过数量|召唤仙道特殊小兵

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		way = int(eventParams["extraValue"].split("|")[0])
		camp = int(eventParams["extraValue"].split("|")[1])
		scriptID = ""
		routeList = []
		if camp == csdefine.BELONG_SIDE_ATTACK: #仙道
			routeList = spaceEntity.getScript().getSpecialXianRouteList()
			idList = spaceEntity.getEntityRecord( self.xianScriptID )
			amount = 0
			for id in idList:
				entity = KBEngine.entities.get(id,None)
				if not entity:
					continue
				if entity.levelYXLM == csconst.MONSTERYXLM_MAX_LEVEL:
					amount += 1
			if amount >= int(self.xianSpecialScriptIDData[0]):
				scriptID = self.xianSpecialScriptIDData[1]
		elif camp == csdefine.BELONG_SIDE_PROTECT:
			routeList = spaceEntity.getScript().getSpecialMoRouteList()
			idList = spaceEntity.getEntityRecord( self.moScriptID )
			amount = 0
			for id in idList:
				entity = KBEngine.entities.get(id,None)
				if not entity:
					continue
				if entity.levelYXLM == csconst.MONSTERYXLM_MAX_LEVEL:
					amount += 1
			if amount >= int(self.moSpecialScriptIDData[0]):
				scriptID = self.moSpecialScriptIDData[1]
		if scriptID:
			patrolList = routeList[way - 1]
			routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( spaceEntity.scriptID, patrolList )
			if len(routeInfo):
				spawnDir = Math.Vector3(routeInfo[2]["position"]) - Math.Vector3(routeInfo[1]["position"])
				spawnDir = spawnDir.normalise()
				entity = spaceEntity.createEntityByScriptID( scriptID, Math.Vector3(routeInfo[1]["position"]), spawnDir,  { "spawnPos": Math.Vector3(routeInfo[1]["position"]), "patrolList":patrolList,"spawnDir":spawnDir,"way":way } )
				if entity:
					wayStr = ""
					if way == csdefine.YXLM_SOLDIER_UP:
						wayStr = "上"
					elif way == csdefine.YXLM_SOLDIER_CENTER:
						wayStr = "中"
					elif way == csdefine.YXLM_SOLDIER_DOWN:
						wayStr = "下"
					memberList = spaceEntity.memberDatas.getMembersByCamp(camp)
					for member in memberList:
						member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_SOLDIERS_CREATE,entity.getName(),wayStr )

						
SEActionBase.setActionClass("SEAction414", SEAction414)
SEActionBase.setActionClass("SEAction415", SEAction415)
SEActionBase.setActionClass("SEAction416", SEAction416)
SEActionBase.setActionClass("SEAction417", SEAction417)
SEActionBase.setActionClass("SEAction418", SEAction418)
