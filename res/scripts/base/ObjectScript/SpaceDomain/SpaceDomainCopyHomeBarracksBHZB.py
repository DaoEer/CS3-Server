# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyHomeBarracksBHZB( SpaceDomainCopy ):
	"""
	帮会争霸大本营 空间管理器
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )

	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		SpaceDomainCopy.createSpaceItem( self, params )

	def findSpaceItemByTongDBID( self, tongDBID, camp ):
		"""
		通过tongDBID找到spaceItem
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == str(tongDBID):
				return spaceItem
		return None

	def updataNPCPointRestEndTime( self, camp,tongDBIDs, pointIndex,restEndTime ):
		"""
		更新据点重置时间
		"""
		for tongDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tongDBID, camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataNPCPointRestEndTime( pointIndex,restEndTime )

	def updataNPCPointReadyEndTime( self, camp,tongDBIDs, pointIndex,readyEndTime ):
		"""
		更新据点准备时间
		"""
		for tongDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataNPCPointReadyEndTime( pointIndex,readyEndTime )

	def updataNPCPointDeclareWarState( self, camp,tongDBIDs, pointIndex,declareWarState ):
		"""
		更新据点状态
		"""
		for tongDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataNPCPointDeclareWarState( pointIndex,declareWarState )

	def updateNPCPointAttackGroupTeamID( self, camp,tongDBIDs, pointIndex, attackGroupTeamID,declareTongDBID ):
		"""
		更新据点进攻队伍数据
		"""
		for tongDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updateNPCPointAttackGroupTeamID( pointIndex, attackGroupTeamID,declareTongDBID )

	def updataNPCPointOccupyData( self, camp,tongDBIDs, pointIndex,playerDBID,playerName,tongDBID,tongName ):
		"""
		更新据点占领帮会
		"""
		for tDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataNPCPointOccupyData( pointIndex,playerDBID,playerName,tongDBID,tongName )

	def updataBHZBPointJoinAttackMembers( self, camp,tongDBIDs, pointIndex,joinAttackMembers ):
		"""
		更新据点攻占成员
		"""
		for tDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataBHZBPointJoinAttackMembers( pointIndex,joinAttackMembers )

	def updataBHZBPointJoinProtectMembers( self, camp,tongDBIDs, pointIndex, joinProtectMembers ):
		"""
		更新据点防守成员
		"""
		for tDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataBHZBPointJoinProtectMembers( pointIndex, joinProtectMembers )

	def updataBHZBPointJoinProtectTeamID( self, camp,tongDBIDs, pointIndex, joinProtectTeamID):
		"""
		更新参与防守的队伍编号
		"""
		for tDBID in tongDBIDs:
			spaceItem = self.findSpaceItemByTongDBID( tDBID,camp )
			if not spaceItem:
				continue
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.updataBHZBPointJoinProtectTeamID( pointIndex, joinProtectTeamID )

	# def updataHomeBarracksDataToAllMember( self, standMapSpaceKey, homeBarrackData ):
	# 	"""
	# 	更新大本营数据到所有成员
	# 	"""
	# 	tongDBIDStrs = standMapSpaceKey.split("|")
	# 	for tongDBIDStr in tongDBIDStrs:
	# 		spaceItem = self.findSpaceItemByTongDBID( int(tongDBIDStr) )
	# 		if not spaceItem:
	# 			continue
	# 		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
	# 			spaceItem.spaceMailBox.cell.updataHomeBarracksDataToAllMember( homeBarrackData )

	# def updataMemberPositionToClient( self, standMapSpaceKey, memberPosDatas ):
	# 	"""
	# 	更新成员位置信息到客户端
	# 	"""
	# 	tongDBIDStrs = standMapSpaceKey.split("|")
	# 	for tongDBIDStr in tongDBIDStrs:
	# 		spaceItem = self.findSpaceItemByTongDBID( int(tongDBIDStr) )
	# 		if not spaceItem:
	# 			continue
	# 		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
	# 			spaceItem.spaceMailBox.cell.updataMemberPositionToClient( int(tongDBIDStr), memberPosDatas )

	def onEnterBHZBPointWar( self, camp,tongDBID, spaceSciptID, pointDict, playerDBIDs ):
		"""
		通知玩家进入副本
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.onEnterBHZBPointWar( tongDBID,spaceSciptID, pointDict, playerDBIDs )

	def defenseBHZBPoint( self, camp,tongDBID, spaceSciptID, pointDict, playerDBIDs ):
		"""
		通知玩家进入布防
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.defenseBHZBPoint( tongDBID, spaceSciptID, pointDict, playerDBIDs )

	def statusMsgToAllMember( self, camp,msgID,msgArgs ):
		"""
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.statusMsgToMember( msgID, msgArgs )

	def statusMsgToTongMember( self, camp,tongDBID,msgID,msgArgs ):
		"""
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.statusMsgToMember( msgID,msgArgs )

	def updateBHZBWarDetailIntegralData( self, camp,tongDBID,integral,rank ):
		"""
		更新帮会争霸详情积分和排名数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.updateBHZBWarDetailIntegralData( tongDBID, integral, rank )

	def updateBHZBWarDetailOccupyNumber( self, camp, tongDBID, occupyPointAmount ):
		"""
		更新帮会争霸详情占领的据点数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.updateBHZBWarDetailOccupyNumber( tongDBID, occupyPointAmount )

	def updateBHZBWarDetailTeamData( self, camp,tongDBID, teamNumber, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情队伍数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.updateBHZBWarDetailTeamData( tongDBID, teamNumber, pointNumber, pointState, pointName )

	def removeBHZBWarDetailTeamData( self, camp,tongDBID, teamNumber ):
		"""
		移除帮会争霸详情队伍数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.removeBHZBWarDetailTeamData( tongDBID, teamNumber )

	def updateBHZBWarDetailOccupyPointData( self, camp, tongDBID, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情据点占领数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.updateBHZBWarDetailOccupyPointData( tongDBID, pointNumber, pointState, pointName )

	def removeBHZBWarrDetailOccupyPoint( self, camp, tongDBID, pointNumber ):
		"""
		移除帮会争霸详情占领据点
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.removeBHZBWarrDetailOccupyPoint( tongDBID, pointNumber )

	def addBHZBWarMsgData( self, camp,tongDBID, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		spaceItem = self.findSpaceItemByTongDBID( tongDBID,camp )
		if not spaceItem:
			return
		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.addBHZBWarMsgData( tongDBID, statusID, statusArgs )

	def onBHZBEnd( self ):
		"""
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.cell.closeSpace()
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			KBEDebug.INFO_MSG("SpaceDomainCopyHomeBarracksBHZB player(%d) tongDBID = %s gotoSpace exitScriptID(%s)"%(pickArgs.get("playerDBID",0),pickArgs.get( "spaceKey",""),exitScriptID))
			roleMB.cell.gotoSpace( exitScriptID, exitPosition, exitDirection )
			return
		KBEDebug.INFO_MSG("SpaceDomainCopyHomeBarracksBHZB Enter player(%d) tongDBID = %s"%( pickArgs.get("playerDBID",0),pickArgs.get( "spaceKey","") ))
		spaceItem.enter( roleMB, position, direction, pickArgs )
