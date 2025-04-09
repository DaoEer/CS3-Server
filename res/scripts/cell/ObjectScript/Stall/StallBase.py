# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from csdefine import *
import csstatus
import KBEMath
import Math
import Const
from ObjectScript.ObjectScriptBase.GameScript import GameScript

class StallBase( GameScript ):
	"""
	摆摊基础类
	"""
	def __init__( self ):
		GameScript.__init__( self )
		self.scriptID = ""
		self.mapping = {}			# 摆摊数据
		self.point = {}				# 服务器已摆摊 { spaceID : {number:roleID}}

	def initData( self, config ):
		"""
		配置加载
		"""
		self.scriptID = config["scriptID"]
		self.mapping = config[config["scriptID"]]

	def autoFindStallPoint( self,role ):
		"""
		自动找离玩家最近的摆摊点
		"""
		if role.spaceScriptID == self.scriptID:				# 同一个地图
			pos = role.position
		else:
			pos = Math.Vector3( Const.SPACE_TELEPORT_POSITION)
			
		spaceID = role.spaceID
		if not spaceID in self.point.keys():
			self.point[spaceID] = {}
		stallPoint = self.point[spaceID]
		
		minPoint = None
		minDist = 9999999
		for number,value in self.mapping.items():
			if number in stallPoint.keys() and stallPoint[number] > 0:
				# 摆摊位置有人
				continue
			dstPos = KBEMath.Unreal2KBEnginePosition( value["position"] )
			dist = pos.distTo( dstPos )
			if dist < minDist:
				minDist = dist
				minPoint = number
		return minPoint

	def stallPointVerify( self, role, number ):
		"""
		摊位验证
		"""
		if self.scriptID != role.spaceScriptID:
			# 不在摆摊地图中
			ERROR_MSG( "stallPointVerify::stall map error" )
			return False

		spaceID = role.spaceID
		if (not spaceID in self.point) or (not number in self.mapping):
			# 不存在这个摆摊点
			ERROR_MSG( "stallPointVerify::stall point number error" )
			return False

		if self.point[spaceID][number] != role.id:
			# 摆摊位置有人
			ERROR_MSG( "stallPointVerify::stall already someone" )
			role.statusMessage( csstatus.STALL_ALREADY_SOMEONE,"" )
			return False

		# 验证和摆摊点的距离
#		point = KBEMath.Unreal2KBEnginePosition( self.mapping[number]["position"] )
#		if role.position.distTo( point ) > 5:
#			ERROR_MSG( "stallPointVerify::stall point(%s) too far"%str(point) )
#			role.statusMessage( csstatus.STALL_OPEN_TOO_FAR,"" )
#			return False
		return True
		
	def setStallPosAndDir( self, role, number ):
		"""设置玩家位置、朝向"""
		role.position = KBEMath.Unreal2KBEnginePosition( self.mapping[number]["position"] )
		direction = KBEMath.Unreal2KBEngineDirection( self.mapping[number]["direction"] )
		role.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
		
	def setStallPoint( self, role, number ):
		"""
		记录摊位
		"""
		self.point[role.spaceID][number] = role.id
		return True

	def cancelStallPoint( self, role ):
		"""
		取消摊位记录
		"""
		if self.scriptID != role.spaceScriptID:
			# 不在摆摊地图中
			ERROR_MSG( "cancelStallPoint::stall map error" )
			return False
		
		spaceID = role.spaceID
		number = role.stallPoint
		if not spaceID in self.point.keys():
			ERROR_MSG( "cancelStallPoint::stall spaceID error" )
			return False

		if not number in self.point[spaceID]:
			ERROR_MSG( "cancelStallPoint::stall point number error" )
			return False

		stallRoleID = self.point[spaceID][number]
		if stallRoleID != role.id:
			# 玩家不正确
			ERROR_MSG( "cancelStallPoint::stall role error" )
			return False

		self.point[spaceID][number] = 0
		return True
