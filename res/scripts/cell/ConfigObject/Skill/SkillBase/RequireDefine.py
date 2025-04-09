# -*- coding: utf-8 -*-


"""
usage:
	技能消耗类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#common
import csdefine
#data
import csstatus


class Require:
	"""
	基类
	"""
	def __init__( self ):
		"""
		"""
		pass

	def load( self, args ):
		"""
		以字符串作为参数加载；

		@param args: 各字符串具体意义由各派生类自己定义
		@type  args: STRING
		"""
		pass

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。

		@param caster: 施法者
		@type  caster: Entity
		@param skillInstance: 使用的技能实例
		@type  skillInstance: Skill
		"""
		return csstatus.SKILL_GO_ON

	def pay( self, caster, skillInstance ):
		"""
		支付消耗物

		@param caster: 施法者
		@type  caster: Entity
		@param skillInstance: 使用的技能实例
		@type  skillInstance: Skill
		"""
		pass

class RequireMp( Require ):
	"""
	蓝量(MP)消耗
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Require.__init__( self )
		self.value = 0
		self._percent = 0.0

	def load( self, args ):
		"""
		以字符串作为参数加载；

		@param args: format: int
		@type  args: STRING
		"""
		if args["Param1"]:
			self.value = int( args["Param1"] )
		if args["Param2"]:
			self._percent = float( args["Param2"] )

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。
		"""
		if caster.MP >= self.getPay( caster, skillInstance ):
			return csstatus.SKILL_GO_ON
			
		return csstatus.SKILL_OUTOF_MP
		
	def pay( self, caster, skillInstance ):
		"""
		支付消耗物
		"""
		if not self.getPay( caster, skillInstance ): #如果消耗为0则不用去支付消耗
			return
		mp = caster.MP - self.getPay( caster, skillInstance )
		caster.setMP( mp )

	def getPay( self, caster, skillInstance ):
		"""
		获取消耗物
		"""
		_value = int(caster.MP_Max * self._percent) + self.value
		if _value < 0:			# 当计算的消耗小于0时，当作0处理
			_value = 0
		return _value

class RequireHp( Require ):
	"""
	血量(HP)消耗
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Require.__init__( self )
		self.value = 0
		self._percent = 0.0

	def load( self, args ):
		"""
		以字符串作为参数加载；

		@param args: format: int
		@type  args: STRING
		"""
		if args["Param1"]:
			self.value = int( args["Param1"] )
		if args["Param2"]:
			self._percent = float( args["Param2"] )

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。
		"""
		if caster.HP > self.getPay( caster, skillInstance ):
			return csstatus.SKILL_GO_ON

		return csstatus.SKILL_OUTOF_HP

	def pay( self, caster, skillInstance ):
		"""
		支付消耗物
		"""
		if not self.getPay( caster, skillInstance ): #如果消耗为0则不用去支付消耗
			return
		hp = caster.HP - self.getPay( caster, skillInstance )
		caster.setHP( hp )

	def getPay( self, caster, skillInstance ):
		"""
		获取消耗物
		"""
		_value = int(caster.HP_Max * self._percent) + self.value
		if _value < 0:
			_value = 0
		return _value

class RequireGangQi( Require ):
	"""
	罡气消耗
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Require.__init__( self )
		self.value = 0
		self._percent = 0.0

	def load( self, args ):
		"""
		以字符串作为参数加载；

		@param args: format: int
		@type  args: STRING
		"""
		if args["Param1"]:
			self.value = int( args["Param1"] )
		if args["Param2"]:
			self._percent = float( args["Param2"] )

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。
		"""
		if caster.gangQiValue > self.getPay( caster, skillInstance ):
			return csstatus.SKILL_GO_ON

		return csstatus.SKILL_OUTOF_GANGQI

	def pay( self, caster, skillInstance ):
		"""
		支付消耗物
		"""
		if not self.getPay( caster, skillInstance ):  #如果消耗为0则不用去支付消耗
			return
		_gangQiValue = self.getPay( caster, skillInstance )
		caster.recvGangQiDamage( _gangQiValue )

	def getPay( self, caster, skillInstance ):
		"""
		获取消耗物
		"""
		_value = int(caster.gangQiValue_Max * self._percent) + self.value
		if _value < 0:
			_value = 0
		return _value




class RequireDefine( Require ):

	def __init__( self ):
		"""
		构造函数。
		"""
		Require.__init__( self )
		self._requires = []

	def load( self, pyDat ):
		"""
		以字符串作为参数加载；

		@param dictDat: python data
		"""
		for dat in pyDat:
			instance = eval( dat[ "Type" ] )()
			instance.load( dat )
			self._requires.append( instance )

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。

		注：如果出现类似于“使用技能时，有$1%的几率‘增加’$2%的法力消耗”时，表现不一定正确，
		因为现在没有办法正确表现随机的“增加”
		"""
		for r in self._requires:
			state = r.validObject( caster, skillInstance )
			if state != csstatus.SKILL_GO_ON:
				return state
		return csstatus.SKILL_GO_ON

	def pay( self, caster, skillInstance ):
		"""
		支付消耗物
		"""
		for r in self._requires:
			r.pay( caster, skillInstance )

class RequireCostItem( Require ):
	"""
	物品消耗
	"""
	def __init__( self ):
		"""
		构造函数。
		"""
		Require.__init__( self )
		self.itemID = 0
		self.amount = 0

	def load( self, args ):
		"""
		以字符串作为参数加载；

		@param args: format: int
		@type  args: STRING
		"""
		if args["Param1"]:
			self.itemID = int( args["Param1"] )
		if args["Param2"]:
			self.amount = int( args["Param2"] )

	def validObject( self, caster, skillInstance ):
		"""
		校验对象是否满足需求。
		"""
		itemList = caster.getItemInstsByID( self.itemID )
		if not len(itemList):
			return csstatus.SKILL_OUTOF_ITEM
		totalAmount = 0
		for item in itemList:
			totalAmount += item.amount
		if not (totalAmount >= self.amount):
			return csstatus.SKILL_OUTOF_ITEM
		return csstatus.SKILL_GO_ON

	def pay( self, caster, skillInstance ):
		"""
		支付消耗物
		"""
		itemList = caster.getItemInstsByID( self.itemID )
		caster.removeItemListByAmount(itemList, self.amount, csdefine.ITEM_REMOVE_BY_SKILL)

def newInstance( dictDat ):
	"""
	获取需求实例。
		以字符串作为参数加载；

		@param dictDat: python data
	"""
	inst = RequireDefine()
	if dictDat:
		inst.load( dictDat )
	return inst