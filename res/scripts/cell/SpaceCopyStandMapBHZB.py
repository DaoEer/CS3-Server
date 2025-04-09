# -*- coding: utf-8 -*-

from SpaceCopyHomeBarracksBHZB import SpaceCopyHomeBarracksBHZB
import Const
import KBEDebug
import csdefine
import KBEngine

class SpaceCopyStandMapBHZB( SpaceCopyHomeBarracksBHZB ):
	"""
	帮会争霸沙盘大地图
	"""
	def __init__( self ):
		SpaceCopyHomeBarracksBHZB.__init__( self )
		self.addTimerRepeat( 2.0,"updataMemberPosition",() )
		
	def addNPCPointData( self,index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,declareWarState,fightEndTime,restEndTime,readyEndTime,joinPlayerDBIDs,joinProtectPlayerDBIDs ):
		"""
		增加帮会争霸沙盘大地图 据点数据
		"""
		self.pointDataMgr.addNPCPointData( index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,declareWarState,fightEndTime,restEndTime,readyEndTime,joinPlayerDBIDs,joinProtectPlayerDBIDs )	

	def onRequestBHZBPointDatasCB( self, pointDatas ):
		"""
		请求该分线据点的数据
		"""
		self.getScript().onRequestBHZBPointDatasCB( self, pointDatas )

	def getAllNPCPointData( self ):
		"""
		获得所有NPC据点信息
		"""
		return list(self.pointDataMgr.values())

	def addNpcHomeBarracksEntitys( self, npcEntityMB ):
		"""
		增加NPC大本营entity
		"""
		self.npcHomeBarracksEntitys.append(npcEntityMB)

	def removeNpcHomeBarracksEntitys( self, npcEntityMB ):
		"""
		移除NPC大本营entity
		"""
		if npcEntityMB in self.npcHomeBarracksEntitys:
			self.npcHomeBarracksEntitys.remove( npcEntityMB )

	def distributHomeBarracks( self ):
		"""
		分配大本营的归属帮会
		"""
		distributHomeBarracks = self.createArgs["distributHomeBarracks"]
		if distributHomeBarracks:
			for npcHomeBarracksEntity in self.npcHomeBarracksEntitys:
				scriptID = npcHomeBarracksEntity.scriptID
				if scriptID not in distributHomeBarracks:
					continue
				tongDBID = distributHomeBarracks.get( scriptID,0 )
				npcHomeBarracksEntity.setBelongTongDBID( tongDBID )
				npcHomeBarracksEntity.setUname( self.createArgs["tongNameDict"].get(tongDBID,"") )
		else:
			tongDBIDs = [int(i) for i in self.spaceKey.split("|")]
			if len(tongDBIDs) > len( self.npcHomeBarracksEntitys ):
				KBEDebug.ERROR_MSG("SignUpTongs(Len = %i) > homeBarracksEntitys (Len =%i)"%( len(tongDBIDs),len(self.npcHomeBarracksEntitys) ))
				return
			tempDistributHomeBarracks = {}
			for index in range(0,len(tongDBIDs)):
				tongDBID = tongDBIDs[index]
				self.npcHomeBarracksEntitys[index].setBelongTongDBID( tongDBID )
				self.npcHomeBarracksEntitys[index].setUname( self.createArgs["tongNameDict"].get(tongDBID,"") )
				scriptID = self.npcHomeBarracksEntitys[index].scriptID
				tempDistributHomeBarracks[scriptID] = tongDBID

		self.updataHomeBarracksData()

	def updataHomeBarracksData( self ):
		"""
		"""
		tempDatas = []
		for npcHomeBarracksEntity in self.npcHomeBarracksEntitys:
			tempData = {}
			tempData["scriptID"] = npcHomeBarracksEntity.scriptID
			tempData["position"] = npcHomeBarracksEntity.position
			tempData["belongTongDBID"] = npcHomeBarracksEntity.getBelongTongDBID()
			tempData["name"] = npcHomeBarracksEntity.getUname()
			tempDatas.append( tempData )

		self.updataHomeBarracksDataToAllMember( tempDatas )

	def updataMemberPosition( self ):
		"""
		广播成员数据到客户端
		"""
		for tongDBID,tongObj in self.spaceMemberMgr.items():
			tempDatas = []
			for member in tongObj.getAllMembers():
				tempDict = {}
				tempDict["groupID"] = member.getGroupID()
				tempDict["position"] = member.roleMB.position
				tempDatas.append( tempDict )
			
			self.updataMemberPositionToClient( tongDBID, tempDatas )

			KBEngine.globalData["BHZBManager"].updataMemberPositionToClient( self.spaceKey, self.createArgs["camp"],tempDatas )

