# -*- coding- : utf-8 -*-
import KBEngine

from ConfigObject.Drop.DropBase.DropValueBase import DropValueBase

import Define
import csdefine

class DItemExp( DropValueBase ):
	"""
	经验
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )

	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			entity.addExp( self._value + extra, csdefine.EXP_ADD_REASON_KILL_MONSTER )
			
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_EXP

class DItemMoney( DropValueBase ):
	"""
	金钱
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			entity.addBindMoney( self._value + extra, csdefine.MONEY_ADD_REASON_DROP_MONSTER )
	
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_MONEY
	
class DItemXiuwei( DropValueBase ):
	"""
	修为
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			entity.addXiuwei( self._value + extra, csdefine.XIUWEI_ADD_REASON_DORP_MONSTER )
	
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_XIUWEI
	
class DItemPotential( DropValueBase ):
	"""
	潜能
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			entity.addPotential( self._value + extra, csdefine.POTENTIAL_ADD_REASON_DORP_MONSTER )
			
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_POTENTIAL

class DItemBangGong( DropValueBase ):
	"""
	帮贡
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			pass
			
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_BANGGONG			
			
class DItemTongMoney( DropValueBase ):
	"""
	帮会资金
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			pass
			
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_TONG_MONEY			
			
class DItemFeats( DropValueBase ):
	"""
	功勋
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			entity.addFeats( self._value, csdefine.FEATS_ADD_REASON_DROP)
			
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_FEATS			
			
class DItemMorale( DropValueBase ):
	"""
	战意，士气
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity and self._value > 0:
			pass				
				
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_MORALE
		
class DItemPsionic( DropValueBase ):
	"""
	战意，士气
	"""
	def __init__( self, value ):
		DropValueBase.__init__( self, value )
	
	def addValue( self, eid, extra ):
		"""
		添加数值
		"""
		entity = KBEngine.entities.get( eid, None )
		if entity:
			entity.addPsionic( self._value )
				
	def getType( self ):
		"""
		返回值类型
		"""
		return Define.DROP_VALUE_PSIONIC
						
DropValueBase.registerOjbect( Define.DROP_VALUE_EXP, DItemExp )
DropValueBase.registerOjbect( Define.DROP_VALUE_MONEY, DItemMoney )
DropValueBase.registerOjbect( Define.DROP_VALUE_XIUWEI, DItemXiuwei )
DropValueBase.registerOjbect( Define.DROP_VALUE_POTENTIAL, DItemPotential )
DropValueBase.registerOjbect( Define.DROP_VALUE_BANGGONG, DItemBangGong )
DropValueBase.registerOjbect( Define.DROP_VALUE_TONG_MONEY, DItemTongMoney )
DropValueBase.registerOjbect( Define.DROP_VALUE_FEATS, DItemFeats )
DropValueBase.registerOjbect( Define.DROP_VALUE_MORALE, DItemMorale )
DropValueBase.registerOjbect( Define.DROP_VALUE_PSIONIC, DItemPsionic )