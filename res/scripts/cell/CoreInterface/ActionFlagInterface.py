#-*- coding: utf-8 -*-

import KBEDebug
import csdefine


class ActionFlagInterface:
	"""
	行为开关类
	"""
	def __init__(self):
		self.hasActFlag = True
		self.actForbid = 0
		self.actCounter = [0] * len( csdefine.ACTION_FLAG_LIST )

	def getActWord( self ):
		"""
		获取动作限制。应该很少用，一般会使用actionForbidSign()来测试是否动作可用
			@return	:	当前动作限制
			@rtype	:	integer
		"""
		return self.actForbid

	def actionForbidSign( self, signWord ):
		"""
		是否存在标记。
			@return	:	标记字
			@rtype	:	bool
		"""
		try:
			return self.actCounter[signWord]
		except:
			return False


	def actCounterInc( self, act ):
		"""
		<Define method>
		动作计数器加一，并维护动作限制。
		
		@param act	:	行为开关
		@type act		:	int
		"""
		try:
			self.actCounter[act] += 1  # Counter不得大于255
			if self.actCounter[act] == 1:
				self.actForbid |= 1<<act
				self.onActionForbid(act)
				self.onActWordChangedTrigger((act, True))
		except Exception as e:
			KBEDebug.ERROR_MSG("act = %d, error:%s"%(act,e))


	def actCounterIncList( self, acts ):
		"""
		<Define method>
		动作计数器加一，并维护动作限制。
		
		@param acts	:	行为开关列表
		@type acts		:	list
		"""
		for act in acts:
			self.actCounterInc(act)

	def actCounterDec( self, act ):
		"""
		<Define method>
		动作计数器减一，并维护动作限制。
		
		@param act	:	行为开关
		@type act		:	int
		"""
		try:
			if self.actCounter[act]>=1:
				self.actCounter[act] -= 1
				if self.actCounter[act] == 0:
					self.actForbid &= ~(1<<act)
					self.onActWordChangedTrigger((act, False))
		except Exception as e:
			KBEDebug.ERROR_MSG("act = %d, error:%s"%(act,e))


	def actCounterDecList( self, acts ):
		"""
		<Define method>
		动作计数器减一，并维护动作限制。
		
		@param acts	:	行为开关列表
		@type acts		:	list
		"""
		for act in acts:
			self.actCounterDec(act)
			
	def onActionForbid( self, actForbid ):
		"""
		行为禁止时
		"""
		pass


	def onActWordChangedTrigger(self, params):
		"""
		"""
		pass


