# -*- coding: utf-8 -*-

import KBEDebug
import json
from YXLMMember import YXLMMember
import csstatus
import ItemTypeEnum
import csdefine

class YCJMDMemberSkillBarData( dict ):
	"""
	勇闯绝命岛 成员快捷栏数据
	"""
	def __init__( self, index = 0, qbtype = csdefine.QB_ITEM_NONE, id = 0 ):
		self.index = index
		self.qbtype = qbtype
		self.id = id

	def getDictFromObj( self, obj ):

		itemDict = { "index":obj.index, "qbtype":obj.qbtype, "id":obj.id}
		return itemDict
	
	def createObjFromDict( self, dict ):
		obj = YCJMDMemberSkillBarData()
		obj.index = dict["index"]
		obj.qbtype = dict["qbtype"]
		obj.id = dict["id"]		
		return obj

	def isSameType( self, obj ) :
		return isinstance( obj, YCJMDMemberSkillBarData )

class YCJMDMemberInfo( dict ):
	"""
	勇闯绝命岛 成员数据
	"""
	def __init__( self, roleID = 0, roleMB = None, roleDBID = 0 ):
		self.roleID = roleID
		self.roleMB = roleMB
		self.roleDBID = roleDBID
		self.skillBarDatas = {}
		self.equipWeaponItemID = 0
		self.weaponUseSkillID = 0

	def initData( self, dict ):
		self.roleID = dict[ "roleID" ]
		self.roleMB = dict[ "roleMB" ]
		self.roleDBID = dict["roleDBID"]
		self.equipWeaponItemID= dict["equipWeaponItemID"]
		self.weaponUseSkillID = dict["weaponUseSkillID"]
		for skillBarData in dict["skillBarDatas"]:
			dict = { "index":skillBarData.index, "qbtype":skillBarData.qbtype, "id":skillBarData.id }
			skillBarDataObj = g_YCJMDMemberSkillBarData.createObjFromDict(dict)
			self.skillBarDatas[skillBarDataObj.index] = skillBarDataObj

	def equipWeapon( self, skillID, equipWeaponItemID ):
		"""
		装备武器
		"""
		if self.equipWeaponItemID == equipWeaponItemID:
			return
		lastEquipWeaponItemID = self.equipWeaponItemID
		lastWeaponUseSkillID = self.weaponUseSkillID
		self.equipWeaponItemID = equipWeaponItemID
		self.weaponUseSkillID = skillID
		self.removeLastWeaponUseSkillID( lastWeaponUseSkillID, lastEquipWeaponItemID )
		self.addNewWeaponUseSkillID( skillID, equipWeaponItemID )

	def removeLastWeaponUseSkillID( self, lastWeaponUseSkillID, lastEquipWeaponItemID ):
		"""
		移除上次武器使用的技能ID
		"""
		indexs = []
		for index,skillBarData in self.skillBarDatas.items():
			if skillBarData.id == lastWeaponUseSkillID:
				indexs.append( skillBarData.index )

		for index in indexs:
			if index in self.skillBarDatas:
				del self.skillBarDatas[index]

		skillBarData = self.skillBarDatas.get(10,None)
		if skillBarData:
			del self.skillBarDatas[10]

		indexs.append(10)
		if self.roleMB.getClient():
			self.roleMB.client.RemoveYCJMDSkillBars(indexs)

	def addNewWeaponUseSkillID( self, weaponUseSkillID, equipWeaponItemID ):
		"""
		增加武器使用的技能ID
		"""
		minIndex = 0
		for index in range(0,10):
			if index not in self.skillBarDatas.keys():
				minIndex = index
				break
		skillBarData = YCJMDMemberSkillBarData( minIndex,csdefine.QB_ITEM_SKILL,weaponUseSkillID )
		self.skillBarDatas[skillBarData.index] = skillBarData
		if self.roleMB.getClient():
			self.roleMB.client.AddYCJMDSkillBars( skillBarData.index, skillBarData.qbtype, skillBarData.id )
		skillBarData = YCJMDMemberSkillBarData( 10,csdefine.QB_ITEM_KITBAG,equipWeaponItemID )	#特殊数据  
		self.skillBarDatas[skillBarData.index] = skillBarData
		if self.roleMB.getClient():
			self.roleMB.client.AddYCJMDSkillBars( skillBarData.index, skillBarData.qbtype, skillBarData.id )

	def addSkillBarData( self, index, type, id ):
		"""
		增加技能数据
		"""
		for index1, skillBarData in self.skillBarDatas.items():
			if skillBarData.id == id and  index1 != 10:
				self.removeSkillBarData(index1)
				break

		skillBarData = YCJMDMemberSkillBarData( index, type, id )
		self.skillBarDatas[skillBarData.index] = skillBarData
		if self.roleMB.getClient():
			self.roleMB.client.AddYCJMDSkillBars( skillBarData.index, skillBarData.qbtype, skillBarData.id )

	def removeSkillBarData( self, index ):
		"""
		移除技能数据
		"""
		if index in self.skillBarDatas.keys():
			del self.skillBarDatas[index]

		if self.roleMB.getClient():
			self.roleMB.client.RemoveYCJMDSkillBars( [index] )

	def exchangeSkillBarData( self, srcIndex, dstIndex ):
		"""
		交换技能数据
		"""
		if srcIndex == dstIndex:
			return
		if srcIndex < 0 or dstIndex < 0:
			return
		if srcIndex in self.skillBarDatas.keys():
			srcItem = self.skillBarDatas.pop( srcIndex )
			if dstIndex in self.skillBarDatas.keys():
				self.skillBarDatas[srcIndex] = self.skillBarDatas[dstIndex]
				self.skillBarDatas[srcIndex].index = srcIndex
				self.removeSkillBarData(dstIndex)
				self.roleMB.client.AddYCJMDSkillBars( srcIndex, self.skillBarDatas[srcIndex].qbtype, self.skillBarDatas[srcIndex].id )
			else:
				self.roleMB.client.RemoveYCJMDSkillBars( [srcIndex] )

			self.skillBarDatas[dstIndex] = srcItem
			self.skillBarDatas[dstIndex].index = dstIndex
			self.roleMB.client.AddYCJMDSkillBars( dstIndex, srcItem.qbtype, srcItem.id )

	def updateAllSkillBarDataToClient( self ):
		"""
		发送玩家技能数据到客户端  排除穿戴的 (因为玩家进副本自动会穿戴一遍)
		"""
		for index, skillBarData in self.skillBarDatas.items():
			if self.roleMB.getClient():
				self.roleMB.client.AddYCJMDSkillBars( index, skillBarData.qbtype, skillBarData.id )

	def getDictFromObj( self, obj ):
		# skillBarDatas = []
		# for skillBarData in obj.skillBarDatas.values():
		# 	skillBarDatas.append( g_YCJMDMemberSkillBarData.getDictFromObj( skillBarData ) )
		dict = {
			"roleID" 	: obj.roleID,
			"roleMB"	: obj.roleMB,
			"roleDBID"  : obj.roleDBID,
			"skillBarDatas" : list(obj.skillBarDatas.values()),
			"equipWeaponItemID": obj.equipWeaponItemID,
			"weaponUseSkillID": obj.weaponUseSkillID,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, YCJMDMemberInfo )

class YCJMDMemberMgr( dict ):
	"""
	勇闯绝命岛 成员数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "members" ]:
			self[ m.roleDBID ] = m

	def addMember( self, roleMB,roleDBID ):
		"""
		增加勇闯绝命岛成员
		"""
		if roleDBID in self.keys():
			self[roleDBID].roleID = roleMB.id
			self[roleDBID].roleMB = roleMB
			self[roleDBID].updateAllSkillBarDataToClient()
			return
		m = YCJMDMemberInfo( roleMB.id, roleMB, roleDBID )
		self[m.roleDBID] = m
		self[m.roleDBID].updateAllSkillBarDataToClient()

	def getMemberEquipWeaponItemID( self, roleDBID ):
		"""
		获得玩家装备的武器ID
		"""
		if roleDBID in self.keys():
			return self[roleDBID].equipWeaponItemID

		return 0

	def memberEquipWeapon( self, player,skillID, equipWeaponItemID ):
		"""
		玩家装备武器
		"""
		DBID = player.playerDBID
		if DBID in self.keys():
			self[DBID].equipWeapon( skillID, equipWeaponItemID )

	def addSkillBarData( self, player, index, type, id ):
		"""
		增加玩家的技能数据
		"""
		DBID = player.playerDBID
		if DBID in self.keys():
			self[DBID].addSkillBarData( index, type, id )

	def removeSkillBarData( self, player, index ):
		"""
		移除玩家的技能数据
		"""
		DBID = player.playerDBID
		if DBID in self.keys():
			self[DBID].removeSkillBarData( index )

	def exchangeSkillBarData( self, player, srcIndex, dstIndex ):
		"""
		交换玩家的技能数据
		"""
		DBID = player.playerDBID
		if DBID in self.keys():
			self[DBID].exchangeSkillBarData( srcIndex, dstIndex )

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "members" ] = []
		
		for mObj in obj.values():
			tempDict[ "members" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = YCJMDMemberMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, YCJMDMemberMgr )

g_YCJMDMemberInfoMgr = YCJMDMemberMgr()
g_YCJMDMemberInfo = YCJMDMemberInfo()
g_YCJMDMemberSkillBarData = YCJMDMemberSkillBarData()