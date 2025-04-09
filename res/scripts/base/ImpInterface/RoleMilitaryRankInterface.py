import datetime
import time
import KBEDebug
class RoleMilitaryRankInterface:
	"""
	玩家军衔接口
	"""
	def __init__( self ):
		pass

	def onGetCell(self):
		self.exploitReduce()

	def addExploit( self, titleID ):
		"""
		添加军功
		"""
		pass


	def changeMilitaryRank( self ):
		"""
		修改军衔
		"""
		pass

	def exploitReduce( self ):
		"""
		军功衰减
		"""
		day_time=int(time.mktime(datetime.date.today().timetuple())) 		#今天00.00的时间
		day_Week = datetime.datetime.now().weekday()						#星期几
		Monday = day_time - day_Week * 64800								#这周的周一00:00
		if self.offlineTime > 0 and self.offlineTime < Monday:
			reduceNum = int((Monday - self.offlineTime) / 64800 / 7) + 1			#过去了几周
			self.cell.exploitReduce( reduceNum )
		