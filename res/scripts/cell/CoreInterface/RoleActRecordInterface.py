# -*- coding: utf-8 -*-

# 玩家各种游戏操作记录接口
# 增加一个写数据库的cell_public属性publicActRecord，需要ghost查询的数据可以用此属性保存。
# 只用于realEntity的数据请勿用此属性保存，以免数据过于庞大，有需要的话可以再定义一个cell_private属性，用于保存这部分数据。

from PublicActRecordDataType import PublicActRecordDataType

class RoleActRecordInterface:
	def __init__( self ):
		pass
	
	def addPublicActRecord( self, recordKey, param1, param2, param3 ):
		"""
		<define method>
		添加记录
		为便于管理，这里的recordKey必须是在csdefine定义的一个枚举值
		"""
		inst = PublicActRecordDataType()
		inst.init( recordKey, param1, param2, param3 )
		self.publicActRecord.append( inst )
	
	def removePublicActRecord( self, recordKey, param1, param2, param3 ):
		"""
		<define method>
		移除记录
		"""
		for i in self.publicActRecord:
			if i.recordKey != recordKey:
				continue
			elif param1 and i.param1 != param1:
				continue
			elif param2 and i.param2 != param2:
				continue
			elif param3 and i.param3 != param3:
				continue
			self.publicActRecord.remove( i )
			break
	
	def updatePublicActRecord( self, recordKey, conParams, valParams ):
		"""
		<define method>
		更新记录
		"""
		record = self.getPublicActRecord( recordKey, conParams[0],conParams[1], conParams[2] )
		if not record:
			return
		record.param1 = valParams[0]
		record.param2 = valParams[1]
		record.param3 = valParams[2]
	
	def getPublicActRecord( self, recordKey, param1, param2, param3 ):
		"""
		获取记录
		"""
		for i in self.publicActRecord:
			if i.recordKey != recordKey:
				continue
			elif param1 and i.param1 != param1:
				continue
			elif param2 and i.param2 != param2:
				continue
			elif param3 and i.param3 != param3:
				continue
			return i
		return None