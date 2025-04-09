# -*- coding: utf-8 -*-
import time
import datetime


class StoreRuleBase(object):
	"""
	商店购买规则
	"""
	def __init__(self):
		pass

	def verity(self, goods, amount):
		return True

class StoreLimitTime(StoreRuleBase):
	def __init__( self ):
		pass

	def verity(self, goods, amount):
		"""
		验证购买时间限制
		"""
		if not goods.LimitTime:
			return True
		nowTime = time.time()
		stringList = goods.LimitTime.split(":")
		List1 = [int(i) for i in stringList[0].split("-")]
		List2 = [int(i) for i in stringList[1].split("-")]
		startTime = time.mktime((datetime.datetime(List1[0],List1[1],List1[2],List1[3],List1[4],List1[5])).timetuple())
		endTime = time.mktime((datetime.datetime(List2[0],List2[1],List2[2],List2[3],List2[4],List2[5])).timetuple())
		if nowTime >= startTime and nowTime <= endTime:
			return True
		return False

class StoreDiscountTime(StoreRuleBase):
	def __init__( self ):
		pass

	def verity(self, goods, amount):
		"""
		验证折扣时间限制
		"""
		if not goods.DiscountTime:
			return True
		nowTime = time.time()
		stringList = goods.DiscountTime.split(":")
		List1 = [int(i) for i in stringList[0].split("-")]
		List2 = [int(i) for i in stringList[1].split("-")]
		startTime = time.mktime(datetime.datetime(List1[0],List1[1],List1[2],List1[3],List1[4],List1[5]).timetuple())
		endTime = time.mktime(datetime.datetime(List2[0],List2[1],List2[2],List2[3],List2[4],List2[5]).timetuple())
		if nowTime >= startTime and nowTime <= endTime:
			return True
		return False