from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


SRV_DB = settings.CS_GAME_SERVER_DB
class GameSeccion( models.Model ):
	"""
	这个表的定义来自“tbl_GameSeccion”
	"""
	accountName = models.CharField(max_length = 255, primary_key = True, default = "", db_column = "sm_accountName")
	password    = models.CharField(max_length = 255, default = "", db_column = "sm_password")
	
	class Meta:
		db_table = 'tbl_GameSeccion'
	
	@classmethod
	def query_account(cls, account):
		"""
		@return None or instance of GameSeccion
		"""
		try:
			m = cls.objects.using(SRV_DB).get(accountName = account)
		except ObjectDoesNotExist:
			return None
		return m
