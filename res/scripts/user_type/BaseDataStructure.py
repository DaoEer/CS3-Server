# -*- coding: utf-8 -*-


class DictBase( dict ):
	#FIXED_DICT dict
	def __init__( self ):
		dict.__init__( self )
	
	def set( self, key, value ):
		self[ key ] = value
		
	def remove( self, key ):
		if self.has_key( key ):
			del self[ key ]
	
	def getLen( self ):
		return len( self )
	
	@classmethod
	def getDictFromObj( self, obj ):
		datalist = []
		for k, v in obj.items():
			tdict = {}
			tdict[ "key" ] = k
			tdict[ "value" ] = v
			datalist.append( tdict )
			
		return { "dictData" : datalist }
		
	#@classmethod
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		for r in dict[ "dictData" ]:
			obj[ r[ "key" ] ] = r[ "value" ]
			
		return obj
	
	#@classmethod
	def isSameType( self, obj ):
		return isinstance( obj, dict )

class DictStrStr( DictBase ):
	def __init__( self ):
		super( DictStrStr, self ).__init__()
		
class DictUniUni( DictBase ):
	def __init__( self ):
		super( DictUniUni, self ).__init__()
		
class DictIntInt( DictBase ):
	def __init__( self ):
		super( DictIntInt, self ).__init__()

	def add( self, key, values ):
		if not self.has_key( key ):
			self[ key ] = values
		else:
			self[ key ] += values

class DictStrInt( DictBase ):
	def __init__( self ):
		super( DictStrInt, self ).__init__()

	def add( self, key, values ):
		if not self.has_key( key ):
			self[ key ] = values
		else:
			self[ key ] += values

class DictStrIntList( DictBase ):
	def __init__( self ):
		super( DictStrIntList, self ).__init__()
	
	def addValue( self, key, value ):
		if not self.has_key( key ):
			self[ key ] = []
			
		self[ key ].append( value )
	
	def delValue( self, key, value ):
		if self.has_key( key ):
			if value in self[ key ]:
				self[ key ].remove( value )
	
	def delValues( self, key, remvoeList ):
		"""
		删除列表元素
		"""
		if self.has_key( key ):
			for v in remvoeList:
				if v in self[ key ]:
					self[ key ].remove( v )

class DictIntIntList( DictBase ):
	def __init__( self ):
		super( DictIntIntList, self ).__init__()
	
	def addValue( self, key, value ):
		if not key in self:
			self[ key ] = []
			
		self[ key ].append( value )
	
	def delValue( self, key, value ):
		if key in self:
			if value in self[ key ]:
				self[ key ].remove( value )
				if not self[key]:
					self.pop(key)
	
	def delValues( self, key, remvoeList ):
		"""
		删除列表元素
		"""
		if self.has_key( key ):
			for v in remvoeList:
				if v in self[ key ]:
					self[ key ].remove( v )
			if not self[key]:
				self.pop(key)
			
class DictIntUni( DictBase ):
	def __init__( self ):
		super( DictIntUni, self ).__init__()

class DictDbidMB( DictBase ):
	def __init__( self ):
		super( DictDbidMB, self ).__init__()
		
class DictDBIDInt( DictIntIntList ):
	def __init__( self ):
		super( DictIntIntList, self ).__init__()
		
class DictDBIDIntList( DictIntIntList ):
	def __init__( self ):
		super( DictIntIntList, self ).__init__()
	
g_dictStrStr = DictStrStr()
g_dictUniUni = DictUniUni()
g_dictIntInt = DictIntInt()
g_dictIntUni = DictIntUni()
g_dictStrInt = DictStrInt()
g_dictStrIntList = DictStrIntList()
g_dictIntIntList = DictIntIntList()
g_dictDbidMB = DictDbidMB()
g_dictDBIDInt = DictDBIDInt()
g_dictDBIDIntList = DictDBIDIntList()