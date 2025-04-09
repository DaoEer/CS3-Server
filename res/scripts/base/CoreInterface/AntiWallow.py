#-*-coding:utf-8-*-

"""
防沉迷系统模块
"""
import json
import time
import KBEngine
import csdefine
import csconst
import KBEDebug
import LoadModule
from ConfigObject.AntiWallowLoader import g_antiWallow

class AntiWallow :
	"""
	未成年人防沉迷系统
	"""
	def __init__( self ):
		"""
		初始化
		"""
		self.bWallow_isAdult = False				# 是否是成年人（defined）

	# ----------------------------------------------------------------
	# callbacks
	# ----------------------------------------------------------------
	def onGetCell( self ) :
		eAccount = self.accountEntity
		if eAccount :
			# isAdult = eAccount.customData.query( "adult" )
			isAdult = self._localGetAdult()
			if isAdult == "" or not isAdult :						# 配置为空或未配置，将被认为是未成年
				isAdult = False
			else:
				isAdult = int( isAdult )
		else:
			KBEDebug.ERROR_MSG( "%s(%i:%i): I has no account entity." % ( self.getName(), self.databaseID, self.id ) )
			return	# 找不到所属帐号则不验证是否未成年，使用默认值就好
		if not isAdult:												# 如果是未成年人
			gwp = KBEngine.globalData["AntiWallowBridge"]
			gwp.onAccountLogin( eAccount.__ACCOUNT_NAME__, self.databaseID )				# 则向防沉迷后台发送登录信息

		self.bWallow_isAdult = isAdult
		self.cell.wallow_setAgeState( isAdult )					
		

	def onLoseCell( self ) :
		eAccount = self.accountEntity
		if eAccount and not self.bWallow_isAdult :						# 如果是非成年人
			gwp = KBEngine.globalData["AntiWallowBridge"]
			gwp.onAccountLogout( eAccount.__ACCOUNT_NAME__ )					# 则向防沉迷后台发送登出信息

	# -------------------------------------------------
	def wallow_onWallowNotify( self, state, olTime ) :
		"""
		defined.
		沉迷提醒
		@type			state  : MACRO DEFINATION
		@param			state  : 收益状态，在 csdefine 中定义：WALLOW_XXX
		@type			olTime : INT64
		@param			olTime : 在线时间
		"""
		self.cell.wallow_onWallowNotify( state, olTime )


	# ----------------------------------------------------------------
	# defined methods
	# ----------------------------------------------------------------
	def wallow_setAgeState( self, isAdult ) :
		"""
		defined.
		设置年龄状态
		@type			isAdult : BOOL
		@param			isAdult : 是否是成年
		"""
		eAccount = self.accountEntity
		if eAccount :
			# eAccount.customData.set( "adult", str( int( isAdult ) ) )	# 将 BOOL 型的 isAdult 转换为字符'0','1'。还原数据避免其他对方使用的时候不知道该只会被修改而出错。
			self.bWallow_isAdult = isAdult
			self.cell.wallow_setAgeState( isAdult )
			self._localSetAdult(isAdult)

		gwp = KBEngine.globalData["AntiWallowBridge"]
		if isAdult:
			gwp.onAccountLogout( eAccount.__ACCOUNT_NAME__ )
		else:
			gwp.onAccountLogin( eAccount.__ACCOUNT_NAME__, self.databaseID )

#---------------------------------------------------------------------------------------------------------
#------------------------本地服务器的处理(对接时删除)-----------------------------------------------------

	def _localGetAdult(self):
		"""
		读取本地配置查看是否成年	
		"""
		sect = g_antiWallow.getData("role")
		eAccount = self.accountEntity
	
		if sect and eAccount.__ACCOUNT_NAME__ in sect:
			isAdult = sect[eAccount.__ACCOUNT_NAME__]["isAdult"]
		else:
			isAdult = 0

		return isAdult

	def _localSetAdult(self, isAdult):
		"""
		设置成年成年
		"""
		AntiWallowMgr = KBEngine.globalData["AntiWallowMgr"]
		eAccount = self.accountEntity
		AntiWallowMgr.setRoleAdult(eAccount.__ACCOUNT_NAME__, isAdult)
		
#------------------------gm设置在线/离线时长-----------------------------------------------------
	
	def gmSetOnlineTime(self, t):
		"""
		gm设置在线时长
		"""
		AntiWallowMgr = KBEngine.globalData["AntiWallowMgr"]
		eAccount = self.accountEntity
		AntiWallowMgr.setRoleOnlineTime(eAccount.__ACCOUNT_NAME__, t)
		
	def gmSetOfflineTime(self, t):
		"""
		gm设置离线时长
		"""
		AntiWallowMgr = KBEngine.globalData["AntiWallowMgr"]
		eAccount = self.accountEntity
		AntiWallowMgr.setRoleOfflineTime(eAccount.__ACCOUNT_NAME__, t)
		