# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import time
import random
import csconst
import Functions
if KBEngine.component == "cellapp":
	from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

LEFT_TREE_ROOT = 0					# 左树根节点
MID_TREE_ROOT = 1					# 中间树根节点
RIGHT_TREE_ROOT = 2					# 右树根节点
RANDOM_NODE_NUM = [1,1,1,2,2,2,3]		# 节点随机数，用于刷出控制随机刷出节点数

class TongDailyQuestData( object ):
	def __init__( self ):
		self.finishQuestDailyNum = 0	# 每日完成多少个任务
		self.finishQuestIndexs = []		# 任务树中完成的任务索引
		self.acceptQuestIndex = -1
		self.treeQuestNodes = {}		# {0:[1,2],1:[3]...} 描述树节点的关系
		self.nodeMapQuestID = {}		# {0:que0stID, 1:questID, 2:questID....}
		self.taskCompleteNum = 0		# 任务目标完成数量,用于计算奖励
		
	def initQuest( self ):
		"""每日更新"""
		self.finishQuestDailyNum = 0
		self.acceptQuestIndex = -1
		if not self.treeQuestNodes:						# 如果是空树，也要生成一次
			self.genrateDailyQuest()
		else:
			localtime = time.localtime()
			if localtime.tm_wday == 0:					# 每周一生成新的任务树
				self.genrateDailyQuest()
			
	def genrateDailyQuest( self ):
		"""生成任务树"""
		self.finishQuestIndexs = []
		self.treeQuestNodes = {}
		self.nodeMapQuestID = {}
		self.taskCompleteNum = 0
		self.genrateRandomNode()
		self.balanceNode()
		self.linkNode()
		self.fillQuestDatas()
		del self.questDayIndex
		
	def genrateRandomNode( self ):
		"""生成随机节点"""
		self.questDayIndex = {}
		self.questDayIndex[0] = [[LEFT_TREE_ROOT,], [ MID_TREE_ROOT ,], [ RIGHT_TREE_ROOT, ]]
		index = RIGHT_TREE_ROOT
		random3NodeList = [0,0,0]				# 每个树，只能出现一个3任务节点，否则树会分布不均匀
		for day in range(1,7):
			self.questDayIndex[day] = [[],[],[]]
			for nodeIndex in range( 3 ):
				randIndex = random.choice( RANDOM_NODE_NUM )
				if randIndex == 3:
					if random3NodeList[nodeIndex]:
						randIndex = random.choice([1,2])
					else:
						random3NodeList[nodeIndex] = 1
				for i in range( randIndex ):
					index += 1
					self.questDayIndex[day][nodeIndex].append( index )
		
	def balanceNode( self ):
		"""平衡树节点"""
		for treeNodeList in self.questDayIndex.values():
			isThreeFirst = len( treeNodeList[0] ) >= 3
			isThreeSecond = len( treeNodeList[1] ) >= 3
			isThreeThird = len( treeNodeList[2] ) >= 3
			if isThreeFirst and not isThreeSecond:
				treeNodeList[1].insert( 0, treeNodeList[0][-1] )
			elif isThreeThird and not isThreeSecond:
				treeNodeList[1].append( treeNodeList[2][0] )
			elif isThreeSecond:
				if not isThreeFirst:
					treeNodeList[0].append( treeNodeList[1][0] )
				elif not isThreeThird:
					treeNodeList[2].insert(0, treeNodeList[1][-1])
		
	def linkNode( self ):
		"""链接生成随机数"""
		for day, NodeList in self.questDayIndex.items():
			for nodes in NodeList:
				for node in nodes:
					self.treeQuestNodes[node] = []
			if day == 6:continue
			nextDayNodeList = self.questDayIndex[day+1]
			for index, nodes in enumerate( NodeList):
				if len( nextDayNodeList[index] ) >= len( nodes ):
					for tIndex, node in enumerate( nextDayNodeList[index] ):
						baseNode = nodes[min( len( nodes ) - 1, tIndex )]
						self.treeQuestNodes[baseNode].append( node )
				else:
					for tIndex, baseNode in enumerate( nodes ):
						node = nextDayNodeList[index][min( len( nextDayNodeList[index]) - 1, tIndex )]
						self.treeQuestNodes[baseNode].append( node )
					
	def fillQuestDatas( self ):
		"""填充任务数据"""
		maxNum = max( self.treeQuestNodes ) + 1
		qList = g_QuestLoader.getRandomDailyQuest( maxNum )
		for index in range( maxNum ):
			self.nodeMapQuestID[index] = qList[index]
	
	def getAcceptQuestIndexByDay( self ):
		"""获取当天已经完成或已经接取的任务"""
		if self.acceptQuestIndex > 0:
			return self.acceptQuestIndex
		if self.finishQuestDailyNum > 0:
			return self.finishQuestIndexs[len(self.finishQuestIndexs)-1]
		return -1
	
	def getNodeMapQuestDatas( self ):
		"""获取节点 映射的任务数据"""
		datas = {}
		for index, questID in self.nodeMapQuestID.items():
			genre = 0
			if questID in g_QuestLoader._tongDailyQuestList:
				genre = g_QuestLoader._tongDailyQuestList[questID]
			datas[index] = [questID, genre]
		return datas
	
	def onFinishQuest( self, questID ):
		"""完成任务"""
		if self.acceptQuestIndex in self.nodeMapQuestID and self.nodeMapQuestID[self.acceptQuestIndex] == questID:
			self.finishQuestIndexs.append( self.acceptQuestIndex )
			self.acceptQuestIndex = -1
			self.finishQuestDailyNum += 1
		
	def onAbandonQuest( self, questID ):
		"""放弃任务"""
		if self.acceptQuestIndex is self.nodeMapQuestID and self.nodeMapQuestID[self.acceptQuestIndex] == questID:
			self.acceptQuestIndex = -1
		
	def acceptQuestNode( self, playerRole, beforeNode, acceptNode ):
		"""接受 任务节点"""
		if self.acceptQuestIndex != -1:return
		if self.finishQuestDailyNum >= 1:return
		if acceptNode in [ LEFT_TREE_ROOT, MID_TREE_ROOT, RIGHT_TREE_ROOT ]:
			questID = self.nodeMapQuestID[acceptNode]
			playerRole.acceptQuest( questID )
			self.acceptQuestIndex = acceptNode
			playerRole.onAcceptTongDailyQuest()
			return
		if beforeNode in self.finishQuestIndexs:
			if acceptNode in self.treeQuestNodes[beforeNode]:
				if acceptNode in self.nodeMapQuestID:
					questID = self.nodeMapQuestID[acceptNode]
					playerRole.acceptQuest( questID )
					self.acceptQuestIndex = acceptNode
					playerRole.onAcceptTongDailyQuest()
					return
		KBEDebug.ERROR_MSG("Accept tong daily quest err!Cannot accept questNode(%d)!"%acceptNode)
			
	def getAcceptQuestList( self ):
		"""获取任务树，可接取的任务"""
		questList = []
		if self.finishQuestIndexs:
			finishQuestIndex = max( self.finishQuestIndexs )
			nodes = self.treeQuestNodes[finishQuestIndex]
			for node in nodes:
				questList.append( self.nodeMapQuestID[node] )
			
		elif self.treeQuestNodes:
			rootQuests = [0,1,2]					# 根节点任务
			for rootNode in rootQuests:
				nodes = self.treeQuestNodes[rootNode]
				for node in nodes:
					questList.append( self.nodeMapQuestID[node] )
			
		return questList
		
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		Data = {}
		Data[ "finishQuestDailyNum" ] = obj.finishQuestDailyNum
		Data[ "acceptQuestIndex" ] = obj.acceptQuestIndex
		Data["finishQuestIndexs"] = obj.finishQuestIndexs
		Data[ "treeQuestNodes" ] = obj.treeQuestNodes
		Data["nodeMapQuestID"] = obj.nodeMapQuestID
		Data[ "taskCompleteNum" ] = obj.taskCompleteNum
		return  Data
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		obj = TongDailyQuestData()
		obj.finishQuestDailyNum = proDict["finishQuestDailyNum"]
		obj.acceptQuestIndex = proDict["acceptQuestIndex"]
		obj.finishQuestIndexs = proDict["finishQuestIndexs"]
		obj.treeQuestNodes = proDict["treeQuestNodes"]
		obj.nodeMapQuestID = proDict["nodeMapQuestID"]
		obj.taskCompleteNum = proDict["taskCompleteNum"]
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, TongDailyQuestData )

instance = TongDailyQuestData()
