# -*- coding: utf-8 -*-

"""
垃圾分析工具，用于分析收集到的垃圾数据之关的依赖关系。
"""

#from bwdebug import *

import gc
import sys
import os
import KBEngine

# bound method 也属于 types.UnboundMethodType 类型，所以不能忽略
_types_ignore = (
            bool,                   str,                            bytes,
			int,                    float,
        )

class GBProcess:
	def __init__( self, pyobj ):
		self.key = None		# 用于标识它的唯一属性名称——如果有的话。
		self.pyobj_ = pyobj
		self.links = set()		# 自身类型包函的其它类型
		self.parents = set()	# 记录指向自己的对象，用于删除自身时能快速的更新parent的指向列表

	@classmethod
	def newNode( SELF, pyobj ):
		"""
		"""
		if pyobj is None or isinstance( pyobj, _types_ignore ):
			return None

		return GBProcess( pyobj )

	def uid( self ):
		"""
		virtual method.
		获取uid
		"""
		return id( self.pyobj_ )

	def release( self ):
		self.onRelease()
		self.links.clear()
		self.parents.clear()
		self.pyobj_ = None

	def onRelease( self ):
		"""
		template method.
		"""
		pass

	def objRefCount( self ):
		"""
		返回引用的pyobj的引用计数
		"""
		# 减2的原因是self.pyobj_引用了一次，在调用sys.getrefcount()时参数又引用了一次
		return sys.getrefcount( self.pyobj_ ) - 2

	def generateSubNodes( self ):
		"""
		virtual method.
		创建当前类型引用的实例的子类型
		@return: 子类型列表
		"""
		s = [ self.newNode( pyobj ) for pyobj in gc.get_referents( self.pyobj_ ) ]
		return [ e for e in s if e is not None and e.uid() != 0 ]

	def getName( self ):
		"""
		取得pyobj的真实名称

		@return: string
		"""
		return "%s : %s" % ( id(self.pyobj_), repr(self.pyobj_) )



class Garbage:
	def __init__( self, outputFile ):
		self._outputFile = outputFile

		# key == GBProcess.uid(), value == instance of GBProcess
		self._instanceDict = {}

	def addInstance( self, instance ):
		self._instanceDict[id( instance )] = instance	# instance of class

	def collect( self, garbageList = None, recursiveTimes = 0 ):
		"""
		收集、过滤gc.garbage里的元素，并生成交叉引用数据。
		@param recursive: 递归搜索次数，极慢，正常情况下都不需要使用。
		@param recursive: int
		"""
		self._instanceDict.clear()

		# 首先，从gc.garbage收集所有的未释放元素
		if garbageList is None:
			garbageList = gc.garbage
			
		for g in garbageList:
			node = GBProcess.newNode( g )
			if node and node.uid() != 0:
				self._instanceDict[node.uid()] = node
				#print( "Node:", node.uid(), node.__class__.__name__, "-->", node.getName() )

		# 然后，从所有收集自gc.garbage的元素中收集子元素
		print( "info: collectting garbage..." )
		allNodes = self._instanceDict.values()
		searchTime = 0
		while len( allNodes ):
			validNodes = []
			for node in list( allNodes ):	# 为了避免中间插入改变状态，必须复制一份
				nodes = node.generateSubNodes()
				#print( "subNodes:", nodes, "parentNode ->", node.getName() )
				for subNode in nodes:
					#print( "subNode:", subNode.uid(), subNode.__class__.__name__, "-->", subNode.getName() )
					if subNode.uid() == 0:
						continue
					if subNode.uid() not in self._instanceDict:
						self._instanceDict[subNode.uid()] = subNode
						validNodes.append( subNode )
						#print( "subNode:", subNode.uid(), subNode.__class__.__name__, "-->", subNode.getName() )

					existedSubNode = self._instanceDict[subNode.uid()]
					node.links.add( subNode.uid() )					# 加入到链接表中
					existedSubNode.parents.add( node.uid() )		# 加入到父类列表中
					# 如果已存在的node中没有有效的key，则更新
					if subNode.key and not existedSubNode.key:
						existedSubNode.key = subNode.key
					# 如果这个异常出现了，则表示代码有bug
					assert subNode.uid() != node.uid(), "%s" % subNode.uid()

			# 检查是否要递归搜索
			if recursiveTimes > 0:
				if searchTime >= recursiveTimes:
					break
				searchTime += 1
				allNodes = validNodes
				print( "recursive ... %s" % len( allNodes ) )
			else:
				allNodes = []

		# 接着，清除所有没有下层（交叉）引用的元素
		print( "info: processing depend..." )
		self.calculateDepend()

		# 最后，把有交叉引用的数据写到日志中
		self.writeLog( self.makeNodeUIDTracks )

	def writeLog( self, collectStrategy ):
		"""
		@param collectStrategy: 一个用于生成uid轨迹的策略，当前可用的为makeNodeUIDTracks()和makeNodeUIDTracksEx（）
		"""
		f = open( self._outputFile, "wt" )

		print( "info: making log... %s" % len( self._instanceDict ) )
		for key in self._instanceDict.keys():
			print( "info: making uids track... %s" % key )
			tracks = []
			collectStrategy( key, tracks, [] )
			for track in tracks:
				print( track )
				log = self.generateLogByUIDs( track )
				f.write( log )
		f.close()

	def makeNodeUIDTracks( self, uid, tracksOut, trackTmp ):
		"""
		产生与uid相对应的实例及其子节点关联的日志
		注：为了效率的考虑，此函数只返回第1个链接的日志，
		    如果想返回所有的日志，请使用makeNodeUIDTracksEx()。
		@param tracksOut: 结果; like as [ [uid1, uid2, ...], ... ]
		@param trackTmp: 一个用于中转的临时list实例，不使用默认值“[]”，
		                 原因是参数中的trackTmp = []永远都只使用同一个实例，
		                 这样容易误使列表存在多余的内容
		"""
		uids = set( [uid,] )
		trackTmp.append( uid )
		node = self._instanceDict[uid]
		while 1:
			assert len( node.links ) > 0
			node = self._instanceDict[list( node.links )[0]]	# 只取第0个链接的node，其余的忽略
			if node.uid() in uids:
				break
			uids.add( node.uid() )
			trackTmp.append( node.uid() )
		trackTmp.append( node.uid() )
		tracksOut.append( trackTmp )

	def makeNodeUIDTracksEx( self, uid, tracksOut, trackTmp ):
		"""
		比makeNodeUIDTracks()更详细的搜索所有的轨迹，但需要更长的时间。
		@param tracksOut: 结果; like as [ [uid1, uid2, ...], ... ]
		@param trackTmp: 一个用于中转的临时list实例，不使用默认值“[]”，
		                 原因是参数中的trackTmp = []永远都只使用同一个实例，
		                 这样容易误使列表存在多余的内容
		"""
		if uid in trackTmp:
			t = list( trackTmp )
			t.append( uid )
			tracksOut.append( t )
			return
		
		trackTmp.append( uid )		# 把自己加入到轨迹表中
		for e in self._instanceDict[uid].links:
			self.makeNodeUIDTracksEx( e, tracksOut, trackTmp )
		trackTmp.pop()				# 任务已完成，把自己从轨迹表中移除


	def generateLogByUIDs( self, uids ):
		"""
		@param uids: list of uid
		"""
		logs = []
		for uid in uids:
			node = self._instanceDict[uid]
			logs.append( node.getName() )
			logs.append( "\n\t-->\t" )
		logs.pop()	# 去掉最后一个"\n\t-->\t"
		logs.append( "\n\n" )
		
		return "".join( logs )

	def calculateDepend( self ):
		"""
		检查依赖关系，把不需要的处理掉
		"""
		count = 1
		while count != 0:	# 一直循环，直到把所有不相关节点都清理干净
			count = 0
			for key in list( self._instanceDict.keys() ):	# 必须复制一份，因为下面在执行删除操作
				#if key not in self._instanceDict:
				#	continue	# 这个是可能的，因为下面在执行一些关联删除操作
				node = self._instanceDict[key]
				if len( node.links ) == 0:						# 没有下层链接
					self._instanceDict.pop( key )				# 就可以把它从列表中去除
					count += 1
					for k in node.parents:
						pnode = self._instanceDict[k]
						pnode.links.remove( node.uid() )		# 并通知链接它的父节点
					node.release()
				"""有这个也许会不利于问题的查找
				elif len( node.parents ) == 0:					# 如果没有上层链接
					print( "remove parents", node.pyobj_ )
					self._instanceDict.pop( key )				# 就可以把它从列表中去除，这样可以使生成的链接更简短，但可能会给定位问题带来麻烦
					count += 1
					for k in node.links:
						pnode = self._instanceDict[k]
						pnode.parents.remove( node.uid() )		# 并通知链接它的子节点
					node.release()
				"""


def ouputGc():
	"""
	"""
	gc.set_debug( gc.DEBUG_LEAK )
	gc.enable()
	gc.collect()
	
	fileName = "%s-%s.log"%( KBEngine.component, id(KBEngine))
	g = Garbage( fileName )
	g.collect()
	print( "path:", os.environ['KBE_ROOT'],fileName )
