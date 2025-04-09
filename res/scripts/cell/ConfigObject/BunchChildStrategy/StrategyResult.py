# -*- coding: utf-8 -*-
"""
策划结果脚本
"""
import random
import Const

class ResultBase:
	"""
	基类
	"""
	def __init__( self ):
		pass
	
	def init( self, dict ):
		pass
	
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		return ""

class ResultRandomBig( ResultBase ):
	"""
	随机取一大副本
	"""
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		if spaceEntity:
			completeList = list( spaceEntity.createArgs[ "completeList" ] )
			completeList.append( spaceEntity.bunchChildSpaceIndex )
		else:
			completeList = []
		bigList = bunchObj.getAllBigChildSpace()
		
		remainList = []
		for i in bigList:
			if i not in completeList:
				remainList.append(i)
		if remainList:
			index = random.choice( remainList )
			return bunchObj.getChildSpaceScriptIDByIndex(index)
		return ""

class ResultRandomSmall( ResultBase ):
	"""
	随机取一小副本
	"""
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		if spaceEntity:
			completeList = list( spaceEntity.createArgs[ "completeList" ] )
			completeList.append( spaceEntity.bunchChildSpaceIndex )
		else:
			completeList = []
		smallList = bunchObj.getAllSmallChildSpace()
		
		remainList = []
		for i in smallList:
			if i not in completeList:
				remainList.append(i)
		if remainList:
			index = random.choice( remainList )
			return bunchObj.getChildSpaceScriptIDByIndex(index)
		return ""

class ResultBigOrOut( ResultBase ):
	"""
	按几率取大副本或传出去
	只能配在非第一层
	"""
	def __init__( self ):
		self.bigRate = 0.0
	
	def init( self, dict ):
		self.bigRate = float(dict["Param1"])
	
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		if random.random() < self.bigRate:
			completeList = list( spaceEntity.createArgs[ "completeList" ] )
			completeList.append( spaceEntity.bunchChildSpaceIndex )
			bigList = bunchObj.getAllBigChildSpace()
			
			remainList = []
			for i in bigList:
				if i not in completeList:
					remainList.append(i)
			if remainList:
				index = random.choice( remainList )
				return bunchObj.getChildSpaceScriptIDByIndex(index)
		
		return Const.BUNCH_RECORD_SPACE_STR

class ResultSmallOrOut( ResultBase ):
	"""
	按几率取小副本或传出去
	只能配在非第一层
	"""
	def __init__( self ):
		self.smallRate = 0.0
	
	def init( self, dict ):
		self.smallRate = float(dict["Param1"])
	
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		if random.random() < self.smallRate:
			completeList = list( spaceEntity.createArgs[ "completeList" ] )
			completeList.append( spaceEntity.bunchChildSpaceIndex )
			smallList = bunchObj.getAllSmallChildSpace()
			
			remainList = []
			for i in smallList:
				if i not in completeList:
					remainList.append(i)
			if remainList:
				index = random.choice( remainList )
				return bunchObj.getChildSpaceScriptIDByIndex(index)
		
		return Const.BUNCH_RECORD_SPACE_STR

class ResultBigOrSmall( ResultBase ):
	"""
	按几率取大副本或小副本
	"""
	def __init__( self ):
		self.bigRate = 0.0
	
	def init( self, dict ):
		self.bigRate = float(dict["Param1"])
	
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		if spaceEntity:
			completeList = list( spaceEntity.createArgs[ "completeList" ] )
			completeList.append( spaceEntity.bunchChildSpaceIndex )
		else:
			completeList = []
		
		if random.random() < self.bigRate:
			bigList = bunchObj.getAllBigChildSpace()
			remainList = []
			for i in bigList:
				if i not in completeList:
					remainList.append(i)
			if remainList:
				index = random.choice( remainList )
				return bunchObj.getChildSpaceScriptIDByIndex(index)
		else:
			smallList = bunchObj.getAllSmallChildSpace()
			remainList = []
			for i in smallList:
				if i not in completeList:
					remainList.append(i)
			if remainList:
				index = random.choice( remainList )
				return bunchObj.getChildSpaceScriptIDByIndex(index)
		
		return ""

class ResultOut( ResultBase ):
	"""
	传出去
	只能配在非第一层
	"""
	def getResult( self, bunchObj, spaceEntity, playerEntity ):
		return Const.BUNCH_RECORD_SPACE_STR