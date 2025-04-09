# -*- coding: utf-8 -*-


# engine

# python

# script
import csdefine
import KBEngine
import KBEDebug
import Const
import KST
import Math
import csarithmetic
import random
from SmartImport import smartImport

class Route( dict ):
	def __init__( self, routePosList ):
		dict.__init__( self )
		for k, v in routePosList.items():
			self[ k ] = v

	def getNext(self, curIdx ):
		if max( self.positions.keys() ) == curIdx: #已经最后一个
			return None

		return self.positions[ curIdx+1 ]

	def getPre(self, curIdx ):
		if 1 == curIdx:#当前是第一个
			return None

		return self.positions[curIdx - 1]

class PatrolRouteLoader:
	def __init__( self ):
		self._patrolRouteDatas = {}
		
	def initSpacePatrolRoute( self, spaceScriptID, spawnFile ):
		"""
		初始化空间内巡逻数据
		"""
		routeDatas = smartImport( "GameObject.SpaceObject.PatrolRoute." + spawnFile + ":" + "Datas" )
		self._patrolRouteDatas[spaceScriptID] = {}
		for k, v in routeDatas.items():
			self._patrolRouteDatas[spaceScriptID][ k ] = Route( v )

	def getPatrolRoute(self , spaceScriptID, route):
		"""
		通过spaceScriptID以及route得到线路内的巡逻点
		@param spaceScriptID:	空间ID
		@param type:	int
		@param route:	某一条巡逻路线
		@param type:	int
		"""
		if self._patrolRouteDatas.get(spaceScriptID):
			if self._patrolRouteDatas[spaceScriptID].get(route):
				return self._patrolRouteDatas[spaceScriptID][route]
			else:
				return {}
				KBEDebug.ERROR_MSG("spaceScriptID = %s can't find route = %s patrol route ,please check it"%(spaceScriptID,route) )
		else:
			KBEDebug.ERROR_MSG("PatrolRouteLoader::can't find spaceScriptID = %s patrol route,please check it"%(spaceScriptID))

	def getSpacePatrolRoute(self , spaceScriptID):
		"""
		通过spaceScriptID以及route得到线路内的巡逻点
		@param spaceScriptID:	空间ID
		@param type:	int
		@param route:	某一条巡逻路线
		@param type:	int
		"""
		if self._patrolRouteDatas.get(spaceScriptID):
			return self._patrolRouteDatas[spaceScriptID]
		else:
			return {}
			KBEDebug.ERROR_MSG("PatrolRouteLoader::can't find spaceScriptID = %s patrol route,please check it"%(spaceScriptID))
			
	def getNearestRoutePoint(self, spaceScriptID, route, position):
		"""
		得到指定巡逻路线上离指定点最近的巡逻点
		@param spaceScriptID:	空间ID
		@param type:	int
		@param route:	某一条巡逻路线
		@param type:	int
		"""
		routePoint = 0
		position = Math.Vector3(position)
		if self._patrolRouteDatas.get(spaceScriptID):
			if self._patrolRouteDatas[spaceScriptID].get(route):
				patrolRoute = self._patrolRouteDatas[spaceScriptID][route]
				distance = 1000
				for index,value in patrolRoute.items():
					pos = Math.Vector3(value[ "position" ])
					if pos.flatDistTo(position) < distance:
						routePoint = index
						distance = pos.flatDistTo(position)
			else:
				KBEDebug.ERROR_MSG("spaceScriptID = %s can't find route = %s patrol route ,please check it"%(spaceScriptID,route) )
		else:
			KBEDebug.ERROR_MSG("PatrolRouteLoader::can't find spaceScriptID = %s patrol route,please check it"%(spaceScriptID))

		return routePoint

	def getRoutePoints(self, routeDatas):
		"""
		获取指定route上的routePoint
		"""
		points = []
		for index in routeDatas.keys():
			points.append(index)
		return points
	# ----------------------------------------------------------------------------
	# 吃豆子玩法（怪物按照路线追击玩家）
	# ----------------------------------------------------------------------------
	def initSpaceMazeRoute( self, spaceScriptID ):
		"""
		初始化迷宫路线
		"""
		if spaceScriptID in self._patrolRouteDatas:
			for index, routeInfo in self._patrolRouteDatas[spaceScriptID].items():
				fIndex = self.getMinKey( routeInfo )
				lIndex = self.getMaxKey( routeInfo )
				
				fPos = Math.Vector3( routeInfo[fIndex]["position"] )
				lPos = Math.Vector3( routeInfo[lIndex]["position"] )
				routeInfo["formerRoute"] = {}
				routeInfo["formerRoute"]["head"] = []
				routeInfo["formerRoute"]["end"] = []
				routeInfo["lastRoute"] = {}
				routeInfo["lastRoute"]["head"] = []
				routeInfo["lastRoute"]["end"] = []
				for eIndex, eRouteInfo in self._patrolRouteDatas[spaceScriptID].items():
					if eIndex == index:continue
					formerIndex = self.getMinKey( eRouteInfo )
					lastIndex = self.getMaxKey(eRouteInfo )
					
					nfPos = eRouteInfo[formerIndex]["position"]
					nlPos = eRouteInfo[lastIndex]["position"]
					if self.isSamePos( fPos, nfPos ):
						routeInfo["formerRoute"]["head"].append( eIndex )
					elif self.isSamePos( fPos, nlPos ):
						routeInfo["formerRoute"]["end"].append( eIndex )
					elif self.isSamePos( lPos, nfPos ):
						routeInfo["lastRoute"]["head"].append( eIndex )
					elif self.isSamePos( lPos, nlPos ):
						routeInfo["lastRoute"]["end"].append( eIndex )
		else:
			KBEDebug.ERROR_MSG("InitSpaceMazeRoute fail!!Can not find space scriptID(%s)"%spaceScriptID)
			
	def getNearestRouteAndPosByEntity( self, monster ):
		"""
		获取monster最近路线 和 路点
		"""
		scriptID = monster.getCurrentSpaceScriptID()
		Datas = self._patrolRouteDatas[scriptID]
		minRoute = 1
		minDist = 99999
		minPos = (0,0,0)
		for route, routeInfo in Datas.items():
			for index, point in routeInfo.items():
				if index in ["formerRoute", "lastRoute"]:continue
				dst = monster.position.flatDistTo( point["position"] )
				if dst < minDist:
					minDist = dst
					minRoute = route
					minPos = Math.Vector3( point["position"])
		return minRoute, minPos
		
	def getNearestRouteAndPosByRouteInfo( self, target, route, pointPos ):
		"""
		根据 自身的巡逻数据
		获得与target最近的路线和路点
		"""
		scriptID = target.getCurrentSpaceScriptID()
		Datas = self._patrolRouteDatas[scriptID]
		curRouteInfo = Datas[route]
		if self.isSamePos( Math.Vector3( pointPos ), curRouteInfo[1]["position"] ):
			routeName = "formerRoute"
			minRoute = route
			minPos = curRouteInfo[self.getMaxKey(curRouteInfo)]["position"]
			minDist = target.position.flatDistTo( minPos )
		else:
			routeName = "lastRoute"
			minRoute = route
			minPos = curRouteInfo[1]["position"]
			minDist = target.position.flatDistTo( minPos )
		
		for tmpRoute in curRouteInfo[routeName]["head"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMaxKey(tmpInfo)]
			dit = target.position.flatDistTo( point["position"] )
			if dit < minDist:
				minRoute = tmpRoute
				minDist = dit
				minPos = point["position"]
				
		for tmpRoute in curRouteInfo[routeName]["end"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMinKey(tmpInfo)]
			dit = target.position.flatDistTo( point["position"] )
			if dit < minDist:
				minRoute = tmpRoute
				minDist = dit
				minPos = point["position"]
		
		return minRoute, minPos
	
	def getFarestRouteAndPosByRouteInfo( self, target, route, pointPos ):
		"""
		根据 自身的巡逻数据
		获得与target最远的路线和路点
		"""
		scriptID = target.getCurrentSpaceScriptID()
		Datas = self._patrolRouteDatas[scriptID]
		curRouteInfo = Datas[route]
		if self.isSamePos( Math.Vector3( pointPos ), curRouteInfo[1]["position"] ):
			routeName = "formerRoute"
			maxRoute = route
			maxPos = curRouteInfo[self.getMaxKey(curRouteInfo)]["position"]
			maxDist = target.position.flatDistTo( maxPos )
		else:
			routeName = "lastRoute"
			maxRoute = route
			maxPos = curRouteInfo[1]["position"]
			maxDist = target.position.flatDistTo( maxPos )
		
		for tmpRoute in curRouteInfo[routeName]["head"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMaxKey(tmpInfo)]
			dit = target.position.flatDistTo( point["position"] )
			if dit > maxDist:
				maxRoute = tmpRoute
				maxDist = dit
				maxPos = point["position"]
				
		for tmpRoute in curRouteInfo[routeName]["end"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMinKey(tmpInfo)]
			dit = target.position.flatDistTo( point["position"] )
			if dit > maxDist:
				maxRoute = tmpRoute
				maxDist = dit
				maxPos = point["position"]
		
		return maxRoute, maxPos
		
	def getYawRouteAndPosByRouteInfo( self, target, route, pointPos ):
		"""根据yaw值，预判玩家移动"""
		scriptID = target.getCurrentSpaceScriptID()
		Datas = self._patrolRouteDatas[scriptID]
		curRouteInfo = Datas[route]
		yaw = csarithmetic.getYawByVector3( target.position - pointPos )
		
		if self.isSamePos( Math.Vector3(pointPos), curRouteInfo[1]["position"] ):
			routeName = "formerRoute"
			dstPos = curRouteInfo[self.getMaxKey(curRouteInfo)]["position"]
			dstYaw = csarithmetic.getYawByVector3( Math.Vector3(dstPos) - pointPos )
			minYaw = abs( yaw - dstYaw )
			minRoute = route
			minPos = dstPos
		else:
			routeName = "lastRoute"
			dstPos = curRouteInfo[1]["position"]
			dstYaw = csarithmetic.getYawByVector3( Math.Vector3(dstPos) - pointPos )
			minYaw = abs( yaw - dstYaw )
			minRoute = route
			minPos = dstPos
			
		for tmpRoute in curRouteInfo[routeName]["head"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMaxKey(tmpInfo)]
			dstYaw = csarithmetic.getYawByVector3( Math.Vector3(point["position"]) - pointPos)
			if abs( yaw - dstYaw ) < minYaw:
				minYaw = abs( yaw - dstYaw )
				minRoute = tmpRoute
				minPos = point["position"]
		for tmpRoute in curRouteInfo[routeName]["end"]:
			tmpInfo = Datas[tmpRoute]
			point = tmpInfo[self.getMinKey(tmpInfo)]
			dstYaw = csarithmetic.getYawByVector3( Math.Vector3(point["position"]) - pointPos)
			if abs( yaw - dstYaw ) < minYaw:
				minYaw = abs( yaw - dstYaw )
				minRoute = tmpRoute
				minPos = point["position"]
		return minRoute, minPos
	
	def getRangeRouteAndPosByRouteInfo( self, scriptID, route, pointPos ):
		"""
		随机获得路点
		"""
		Datas = self._patrolRouteDatas[scriptID]
		curRouteInfo = Datas[route]
		if self.isSamePos( Math.Vector3( pointPos ), curRouteInfo[1]["position"] ):
			routeName = "formerRoute"
		else:
			routeName = "lastRoute"
			
		tmpList = []
		tmpList.extend( curRouteInfo[routeName]["head"] )
		tmpList.extend( curRouteInfo[routeName]["end"] )
		randRoute = random.choice( tmpList )
		tmpInfo = Datas[randRoute]
		if randRoute in curRouteInfo[routeName]["head"]:
			return randRoute, tmpInfo[self.getMaxKey(tmpInfo)]["position"]
		else:
			return randRoute, tmpInfo[self.getMinKey(tmpInfo)]["position"]
	
	def isSamePos( self, rPos, tPos ):
		"""
		是否 同一个点
		默认距离小于1，为同一个点
		"""
		return rPos.flatDistTo( tPos ) <= 1
		
	def getMinKey( self, dct ):
		"""获取字典最小 整数key值 """
		listKey = list( dct.keys() )
		if "lastRoute" in listKey:
			listKey.remove("lastRoute")
		if "formerRoute" in listKey:
			listKey.remove("formerRoute")
		return min( listKey )
		
	def getMaxKey( self, dct ):
		"""获取字典最大 整数key值 """
		listKey = list( dct.keys() )
		if "lastRoute" in listKey:
			listKey.remove("lastRoute")
		if "formerRoute" in listKey:
			listKey.remove("formerRoute")
		return max( listKey )

g_patrolRouteLoader = PatrolRouteLoader()