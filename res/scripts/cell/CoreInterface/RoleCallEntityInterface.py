# -*- coding: utf-8 -*-

import json, math, time
import KBEngine
import KBEDebug
import Math
import csdefine
import CalcProperties


class RoleCallEntityInterface():
	"""
	玩家召唤entity接口
	"""

	def __init__( self ):
		#有时候在A地图给玩家加的buff，创建MonsterExtCall，但心魔不满足在A地图存在的条件，所以把属性先保存起来，在符合条件的地图再创建出来
		self.monsterExtCallParams=[]
		self.disposableMonsterList = []
	
	def createMonsterExtCallExt(self):
		"""
		创建等待中的monsterExtCall
		"""
		if not len(self.monsterExtCallParams):
			return

		spaceScriptID = self.getCurrentSpace().scriptID
		for _params in list(self.monsterExtCallParams):
			if spaceScriptID not in _params["enableSpace"] and  len(_params["enableSpace"]):
				continue
			params = {}
			params["owner"] = self.base
			params["enableSpace"] = _params["enableSpace"]
			params["spawnPos"] = Math.Vector3(self.position)
			params["spawnDir"] = Math.Vector3(self.direction)
			params["level"] = self.level
			self.createMonsterExtCall(_params["monsterScriptID"], self.getCurrentSpace(), self.position, self.direction, params)
			self.monsterExtCallParams.remove(_params)

	def callEntity( self, entityID ):
		pass

	def createMonsterExtCall( self, scriptID, spaceCell, position, direction, params ):
		"""
		创建召唤类型怪
		"""
		KBEDebug.DEBUG_MSG("Role(%d:%s) createMonsterExtCall:%s, %s [%s]" %(self.id, self.playerName, scriptID, self.spaceScriptID, params["enableSpace"]))
		self.base.createBaseMonster( scriptID, spaceCell, position, direction, params )

	def onCreateMonsterExtCall( self, baseMB ):
		"""
		创建成功的回调
		"""
		return

	def destroyCallEntity( self, baseMB ):
		"""
		销毁召唤的entity
		"""
		baseMB.cell.destroySelf()

	def registerCallMonster( self, scriptID, baseMB ):
		"""
		<Define method>
		将召唤怪注册到召唤怪物列表中
		"""
		if not scriptID in self.callMonsterMBList.keys():
			self.callMonsterMBList[ scriptID ] = []

		self.callMonsterMBList[ scriptID ].append(baseMB)

	def removeCallMonsterByScriptID( self, scriptID ):
		"""
		"""
		if not scriptID in self.callMonsterMBList:
			return
		for mb in self.callMonsterMBList[scriptID]:
			mb.cell.destroyCellByBase()
		self.callMonsterMBList.pop(scriptID)
	
	def callMonsterFollw( self ):
		"""
		让随从怪物跟随玩家
		"""
		spaceScriptID = self.getCurrentSpace().scriptID
		for value in self.callMonsterMBList.values():
			for baseMB in value:
				baseMB.cell.followOwner( spaceScriptID, self, Math.Vector3(self.position),  Math.Vector3(self.direction) )
		self.createMonsterExtCallExt()
		

	def onAddEnemy( self, enemyID ):
		"""
		玩家添加敌人，则随从怪也移除怪物
		"""
		for value in self.callMonsterMBList.values():
			for baseMB in value:
				baseMB.cell.addEnemy( enemyID )
		for id in list(self.monsterFenShen.keys()):
			entity = KBEngine.entities.get(id)
			if entity:
				entity.addEnemy( enemyID )
			
	def onRemoveEnemy( self, enemyID ):
		"""
		玩家移除敌人，则随从怪物也移除怪物
		"""
		for value in self.callMonsterMBList.values():
			for baseMB in value:
				baseMB.cell.removeEnemy( enemyID )
		for id in list(self.monsterFenShen.keys()):
			entity = KBEngine.entities.get(id)
			if entity:
				entity.removeEnemy( enemyID )

	def addRolecallMonsterProtect( self ):
		"""
		添加保护,切换至未决状态（CST-2315）
		"""
		for value in self.callMonsterMBList.values():
			for baseMB in value:
				baseMB.cell.addMonsterExtCallProtect()
		for id in list(self.monsterFenShen.keys()):
			entity = KBEngine.entities.get(id)
			if entity:
				entity.addMonsterExtCallProtect()

	def removeRoleCallMonsterProtect( self ):
		"""
		移除保护,退出未决状态（CST-2315）
		"""
		for value in self.callMonsterMBList.values():
			for baseMB in value:
				baseMB.cell.removeMonsterExtCallProtect()
		for id in list(self.monsterFenShen.keys()):
			entity = KBEngine.entities.get(id)
			if entity:
				entity.removeMonsterExtCallProtect()
	
	def onTeleportCompleted(self):
		"""
		进入新地图
		"""
		self.callMonsterFollw()
		self.callFenShenMonster()

	def onLeaveSpaceNotify(self):
		"""
		离开当前地图
		"""
		for id in list(self.monsterFenShen.keys()):
			entity = KBEngine.entities.get(id)
			if entity:
				entity.destroySelf()
		for id in self.disposableMonsterList:
			entity = KBEngine.entities.get(id)
			if entity:
				entity.destroySelf()			
	
	#--------------------------------------分身怪物相关---------------------------------------------------------------
	def callFenShenMonster(self):
		"""
		"""
		removeList = []
		t = time.time()
		curSpace = self.getCurrentSpace().scriptID
		for params in self.monsterFenShenData:
			#时间到了
			lifeTime = float(params.get("lifeTime", 0))
			if lifeTime <= time.time():
				removeList.append(params)
				continue
				
			#不能在当前的地图创建
			enableSpace = params.get("enableSpace", "")
			if enableSpace:
				lst = enableSpace.strip().split("|")
				if curSpace in lst:
					continue
			
			offsetFront = float(params.get("offsetFront", 0.0))
			offsetLeft = float(params.get("offsetLeft", 0.0))
			yaw = self.direction.z
			position = Math.Vector3( self.position )
			if offsetFront:
				position.x += offsetFront * math.sin( yaw )
				position.z += offsetFront * math.cos( yaw )
			if offsetLeft:
				position.x += offsetLeft * math.sin( yaw - math.pi/2 )
				position.z += offsetLeft * math.cos( yaw - math.pi/2 )
			
			args = {}
			args.update( {"ownerID": self.id} )
			args.update( {"level": self.level} )
			args.update( {"HP_Max": self.HP_Max} )
			args.update( {"MP_Max": self.MP_Max} )
			args.update( {"gangQiValue": self.gangQiValue} )
			args.update( {"jingjieLevel":self.jingjieLevel} )
			args.update( {"gangQiState": self.gangQiState} )
			args.update( {"spawnPos":tuple(Math.Vector3(position))} )
			args.update( {"spawnDir":tuple(Math.Vector3(self.direction))} )
			args.update( {"attrSkills":json.loads(params.get("attrSkills","{}"))} )
			args.update( {"uname": "{}(分身)".format(self.playerName)} )
			args.update( CalcProperties.getEffectProperty(self) )
			entity = self.createEntityByScriptID( params.get("scriptID"), position, Math.Vector3( self.direction ), args )
			if entity:
				entity.HP = int(float(params.get("HP", 1)) * self.HP_Max)
				entity.MP = int(float(params.get("MP", 1)) * self.MP_Max)
				
				removeList.append(params)
				entity.delayDestroy(int(lifeTime - t))
				self.monsterFenShen[entity.id] = params
				
		for data in removeList:
			self.monsterFenShenData.remove(data)
			
	def updateFenShenData(self, id, HP, HP_Max, MP, MP_Max):
		"""
		销毁之前更新一下数据
		"""
		data = self.monsterFenShen.pop(id, None)
		if data is None:
			KBEDebug.ERROR_MSG("not found monsterData")
			return
		
		if float(data.get("lifeTime", 0)) <= time.time():
			return
		
		if HP <= 0:
			return
		
		data["HP"] = str(float(HP/HP_Max))
		data["MP"] = str(float(MP/MP_Max))
		self.monsterFenShenData.append(data)

	#--------------------------------------一次性的随从怪物相关---------------------------------------------------------------
	def callDisposableMonster(self, params, lifeTime):
		"""
		"""
		entity = self.createEntityByScriptID( params["scriptID"], params["spawnPos"], params["spawnDir"], params )
		if entity:		
			self.disposableMonsterList.append(entity.id)
			entity.delayDestroy(lifeTime)