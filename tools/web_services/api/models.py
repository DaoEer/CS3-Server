from django.db import models

# Create your models here.

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import time

import logging
logger = logging.getLogger("default")

SRV_DB = settings.CS_GAME_SERVER_DB

class ChargeOrders(models.Model):
	"""
	这个表的定义来自“tbl_ChargeOrders”
	"""
	orderID = models.CharField(max_length = 128, primary_key = True, default = "", db_column = "sm_gy_orderId")
	accountName = models.CharField(max_length = 255, default = "", db_column = "sm_account")
	goodType = models.CharField(max_length = 128, default = "", db_column = "sm_goodType")
	amount = models.IntegerField(db_column = "sm_amount")
	ordersTime = models.FloatField(db_column = "sm_orders_time")
	
	class Meta:
		db_table = 'tbl_ChargeOrders'
	
	@classmethod
	def query_orderid(cls, orderid):
		"""
		@return None or instance of GameSeccion
		"""
		try:
			m = cls.objects.using(SRV_DB).get(orderID = orderid)
		except ObjectDoesNotExist:
			return None
		return m

	@classmethod
	def charge(cls, orderid, account, goodtype, amountValue):
		try:
			m = cls.objects.using(SRV_DB).create(
				orderID = orderid,
				accountName = account,
				goodType = goodtype,
				amount = amountValue,
				ordersTime = int(time.time())
				)
		except Exception as err:
			logger.error("ChargeOrders charge error: %s" % err)
			return None
		return m
