# -*- coding: utf-8 -*-


#批次刷新管理接口：只管理通过SpawnPointGroup刷新点刷出的怪

import random
from GroupSpawnAmountConfig import Datas

class GroupSpawnInfo:
	"""
	一个批次的刷新点记录
	"""
	def __init__( self, group ):
		self.group = group
		self.spawnInfo = {}
	
	def addSpawnInfo( self, spawnPoint ):
		"""
		"""
		scriptID = spawnPoint.getEntityScriptID()
		if scriptID not in self.spawnInfo:
			self.spawnInfo[ scriptID ] = [ spawnPoint ]
		else:
			self.spawnInfo[ scriptID ].append( spawnPoint )
	
	def spawnEntity( self, spaceEntity, effectScriptID, delaySpawnTime ):
		"""
		"""
		for spList in self.spawnInfo.values():
			for sp in spList:
				if effectScriptID:
					sp.spawnReplaceEntity( spaceEntity, effectScriptID )
					sp.delaySpawn( spaceEntity, delaySpawnTime )
				else:
					sp.spawnCreateEntity( spaceEntity )
	
	def spawnSomeEntity( self, spaceEntity, effectScriptID, delaySpawnTime, idAndAmountDict ):
		"""
		"""
		for scriptID, spList in self.spawnInfo.items():
			if scriptID not in idAndAmountDict:
				continue
			amount = idAndAmountDict[ scriptID ]
			if len( spList ) > amount:
				spawnSpList = random.sample( spList, amount )
			else:
				spawnSpList = spList
			
			for sp in spawnSpList:
				if effectScriptID:
					sp.spawnReplaceEntity( spaceEntity, effectScriptID )
					sp.delaySpawn( spaceEntity, delaySpawnTime )
				else:
					sp.spawnCreateEntity( spaceEntity )


class GroupDieRecord:
	"""
	一个批次的entity死亡记录
	"""
	def __init__( self, group, cfg ):
		self.group = group
		self.dieRecord = {}		#死亡或销毁记录
		self.amountCfg = cfg.get( "monsterInfo", {} )	#{"monsterInfo":{ scriptID1: amount1, scriptID2: amount2, ... }}
	
	def addDieRecord( self, scriptID, entityID ):
		"""
		"""
		if scriptID not in self.dieRecord:
			self.dieRecord[ scriptID ] = [ entityID ]
		else:
			if entityID not in self.dieRecord[ scriptID ]:
				self.dieRecord[ scriptID ].append( entityID )
	
	def isSomeEntityDie( self, idAndAmountDict ):
		"""
		某些ID entity达到某些死亡数量
		"""
		for id, amount in idAndAmountDict.items():
			if id not in self.dieRecord:
				return False
			if len( self.dieRecord[ id ] ) < amount:
				return False
		return True
	
	def isAllEntityDie( self ):
		"""
		所有entity全部死亡
		每个id的怪物的死亡数量都已达到配置的数量，则认为已经全部死亡，而不是判断所有怪物的死亡总数
		"""
		return self.isSomeEntityDie( self.amountCfg )
	
	def getDieAmount( self ):
		"""
		"""
		amount = 0
		for dieList in self.dieRecord.values():
			amount += len( dieList )
		return amount


class GroupSpawnInterface:
	def __init__( self ):
		self.groupSpawnInfo = {}	# 刷新点记录
		self.groupDieRecord = {}	# entity死亡或销毁记录
		self.groupSpawnAmountCfg = Datas.get( self.scriptID, {} )	# 各个批次各个ID的怪物的刷新数量，用于判断某批次怪物是否全部死亡
		self.allGroup = self.groupSpawnAmountCfg.keys()
	
	def addGroupSpawnPoint( self, spawnPoint ):
		"""
		记录批次刷新点
		"""
		if spawnPoint.group not in self.groupSpawnInfo:
			self.groupSpawnInfo[ spawnPoint.group ] = GroupSpawnInfo( spawnPoint.group )
		self.groupSpawnInfo[ spawnPoint.group ].addSpawnInfo( spawnPoint )
	
	def onGroupMonsterDie( self, group, scriptID, entityID ):
		"""
		批次怪死亡
		"""
		if group not in self.groupDieRecord:
			cfg = self.groupSpawnAmountCfg.get( group, {} )
			self.groupDieRecord[ group ] = GroupDieRecord( group, cfg )
		self.groupDieRecord[ group ].addDieRecord( scriptID, entityID )
	
	def onGroupNPCObjectDestroy( self, group, scriptID, entityID ):
		"""
		批次怪销毁
		"""
		if group not in self.groupDieRecord:
			cfg = self.groupSpawnAmountCfg.get( group, {} )
			self.groupDieRecord[ group ] = GroupDieRecord( group, cfg )
		self.groupDieRecord[ group ].addDieRecord( scriptID, entityID )
	
	def isGroupSomeEntityDie( self, group, idAndAmountDict ):
		"""
		某一批怪物中的某些怪物的死亡或销毁数量达到某值
		"""
		if group not in self.groupDieRecord:	# 没有此批次怪物的死亡记录
			return False
		return self.groupDieRecord[ group ].isSomeEntityDie( idAndAmountDict )
	
	def isGroupEntityAllDie( self, groups ):
		"""
		某些批次怪全部死亡或销毁
		"""
		for group in groups:
			if group not in self.groupDieRecord:	# 没有此批次怪物的死亡记录
				return False
			if not self.groupDieRecord[ group ].isAllEntityDie():
				return False
		return True
	
	def isAllGroupEntityDie( self ):
		"""
		所有批次怪物全部死亡或销毁
		"""
		if len( self.allGroup ) == 0:
			return False
		
		for group in self.allGroup:
			if group not in self.groupDieRecord:	# 没有此批次怪物的死亡记录
				return False
			if not self.groupDieRecord[ group ].isAllEntityDie():
				return False
		return True
	
	def isSomeGroupEntityDie( self, groups, requireAmount ):
		"""
		某几批怪物死亡或销毁总数量不少于某值
		"""
		amount = 0
		for group in groups:
			if group not in self.groupDieRecord:	# 没有此批次怪物的死亡记录
				continue
			amount += self.groupDieRecord[ group ].getDieAmount()
		return amount >= requireAmount
	
	def spawnGroupEntity( self, group, effectScriptID, delaySpawnTime ):
		"""
		刷新一批怪（刷了光效怪则先刷光效怪）
		@param effectScriptID:光效怪ID
		@param delaySpawnTime:光效怪刷出后延时多少秒刷配置的怪
		"""
		if group not in self.groupSpawnInfo:
			return
		self.groupSpawnInfo[ group ].spawnEntity( self, effectScriptID, delaySpawnTime )
	
	def spawnGroupSomeEntity( self, group, effectScriptID, delaySpawnTime, idAndAmountDict ):
		"""
		刷新一批怪物中的某一些怪物（刷了光效怪则先刷光效怪）
		"""
		if group not in self.groupSpawnInfo:
			return
		self.groupSpawnInfo[ group ].spawnSomeEntity( self, effectScriptID, delaySpawnTime, idAndAmountDict )
