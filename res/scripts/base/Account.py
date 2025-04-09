# -*- coding: utf-8 -*-

"""
usage:
	玩家账号模块
	
global function:
	queryRoles

attribute:
	avatar
	_login
	lastClientIpAddr
	_playerList			# 临时记录当前的角色数量
	_destroySelf		# 如果是选择角色进入世界，则该变量被置为 False
	_isInitPlayerList	# 服务器角色列表是否已初始化
	deleteDBID			# 用于避免同一时间处理多条删除角色的请求，从而引发不必要的问题


KBEngine method:
	onEntitiesEnabled
	onLogOnAttempt
	onClientDeath

member function:
	requestInitRoles
	createRole
	logoff
	login
	onAvatarDeath


	
callback:
	onQueryRoles
	onWriteRoleToDBCollback
	onWriteDB
	onTimer
	onLoadedAvatar
	__onAvatarReady

"""

import KBEngine
import time
from urllib.request import urlopen
import KST
import Const
import csconst
import json
import KBEDebug
import csstatus
import LoadModule
import Functions
import csdefine
import RoleBornPropertyConfig
from FaceStyle import FaceStyle
from MsgLogger import g_logger
import BackgroundTask
import ItemTypeEnum
import ItemFactory
import TimerExt
import Settings
import MysqlUtility

from ChargeOrders import RefreshCharge
from CoreObject.EntityObject import EntityObject
import CoreInterface.EntityDataValidateInterface as EntityDataValidateInterface
from RemainItemMailInfo import Datas as MailInfos

# --------------------------------------------------------------------
# inner global methods
# --------------------------------------------------------------------
def queryRoles( parentID, callback ):
	"""
	query all roles which parent account is  parentID
	"""
	query = "select r.id, r.sm_playerName,r.sm_level, r.sm_profession, r.sm_camp, r.sm_gender, r.sm_modelNumber,\
			r.sm_bodyModel, r.sm_headModel, r.sm_suitsModel, r.sm_hairModel, r.sm_adornModel, r.sm_coatModel,\
			r.sm_pantsModel, r.sm_shoesModel, r.sm_cloakModel, r.sm_hatModel,r.sm_wristModel, r.sm_handModel,\
			r.sm_waistModel, r.sm_necklaceModel, r.sm_lringModel, r.sm_rringModel, r.sm_weaponModel, r.sm_fabaoModel,\
			r.sm_offlineTime, r.sm_actionNumber,r.sm_faceModel,r.sm_faceStyle, r.sm_tongDBID,e.sm_id,\
			r.sm_headAdornModel,r.sm_faceAdornModel,r.sm_backAdornModel,r.sm_waistAdornModel,r.sm_roleState, r.sm_unFreezeTime\
			from tbl_Role r left join tbl_Role_itemsBag_items e on r.id = e.parentID and e.sm_order = %i where \
			r.sm_parentDBID = %i and r.sm_roleState != %i" % (ItemTypeEnum.EQUIP_COAT, parentID, csdefine.ROLE_STATE_DELETE)
	KBEDebug.DEBUG_MSG(query)
	KBEngine.executeRawDatabaseCommand( query, callback )

def deleteRole( roleID, callback ):
	"""
	删除角色
	"""
	deleteTime = int(time.time())
	sql_sentence = "UPDATE tbl_Role SET sm_roleState = %i,sm_deleteTime = %s where id = %i" %(csdefine.ROLE_STATE_DELETE ,deleteTime,roleID)
	KBEDebug.DEBUG_MSG(sql_sentence)
	KBEngine.executeRawDatabaseCommand( sql_sentence, callback )

def clearRoleFrozenState(roleID):
	"""
	清除角色冻结状态
	"""
	sql_sentence = "UPDATE tbl_Role SET sm_roleState = %i,sm_unFreezeTime = %s where id = %i" %(csdefine.ROLE_STATE_ACTIVE , 0 ,roleID)
	KBEDebug.DEBUG_MSG(sql_sentence)
	KBEngine.executeRawDatabaseCommand( sql_sentence )

def queryAdultInfo( account ):
	"""
	查询是否成年
	"""
	#示例接口: "http://verify.gyyx.cn:81/User/GameAdultService.ashx?"

	try:
		interfacePath = KBEngine.globalData["adultQueryAddr"]
	except:
		ERROR_MSG("adultQueryAddr has not be configed!" )
		return -1
	params = "account=%s"
	addrPath = interfacePath + params%( account )
	INFO_MSG( "Adult check path: %s"%addrPath )
	try:
		ht = urlopen( addrPath ).read()
	except Exception as errstr:
		ERROR_MSG("Open the adult check address fault! error: %s"%errstr )
		return -1
	if ht not in ["false", "true"]:
		ERROR_MSG("Check adult return answer is not Know!! %s"%ht)
		return -1
	return ht == "true"

class QueryAdultInfoThread( BackgroundTask.BackgroundTask ):
	"""
	查询是否成年人线程
	"""
	def __init__( self, accountEntityID ):
		"""
		"""
		self.accountEntityID = accountEntityID
		BackgroundTask.BackgroundTask.__init__( self )


	def doBackgroundTask( self, mgr ):
		#读取网页字符
		#有效->关闭网页字符
		accountEntity = KBEngine.entities.get( self.accountEntityID )
		if accountEntity:
			self.result = int( queryAdultInfo( accountEntity.__ACCOUNT_NAME__ ) )
			if self.result == -1:
				ERROR_MSG( "account %s query, but overtime!"%(accountEntity.__ACCOUNT_NAME__) )
				return
			INFO_MSG("account %s is adult: %i"%(accountEntity.__ACCOUNT_NAME__, self.result) )
			mgr.addMainThreadTask( self )


	def doMainThreadTask( self, mgr ):
		accountEntity = KBEngine.entities.get( self.accountEntityID )
		if accountEntity:
			if accountEntity.avatar:
				accountEntity.avatar.wallow_setAgeState( self.result )
			else:
				accountEntity.customData.set( "adult", str( self.result ) )

# g_threadMgr = BackgroundTask.Manager()				#线程管理器
# g_threadMgr.startThreads( 5 )						#同时开5条线程，只是避免玩家同时上线的问题

#查询礼包码SQL
SELECT_ACTIVATION_KEY_SQL = "SELECT COUNT(*), sm_item FROM tbl_ActivationKey WHERE sm_keyWord = %s;"
#礼包码更新SQL
UPDATE_ACTIVATION_KEY_SQL = "UPDATE tbl_ActivationKey SET sm_accountDBID = {}, sm_roleName = %s, sm_status = 1 WHERE sm_keyWord = %s AND sm_status = 0;"


class Account(KBEngine.Proxy, EntityObject, EntityDataValidateInterface.EntityDataValidateInterface ):
	def __init__( self ):
		KBEngine.Proxy.__init__( self )
		EntityObject.__init__( self )
		EntityDataValidateInterface.EntityDataValidateInterface.__init__( self )
		KBEDebug.INFO_MSG( "Account[%d:%d] init" %(self.databaseID, self.id) )
		
		self.avatar = None
		self.__isLogin = False
		self.lastClientIpAddr = 0
		self._playerList = []			# 临时记录当前的角色数量
		self._destroySelf = True		# 如果是选择角色进入世界，则该变量被置为 False
		self._isInitPlayerList = False	# 服务器角色列表是否已初始化
		self.deleteDBID = None			# 用于避免同一时间处理多条删除角色的请求，从而引发不必要的问题
		self.isAccountLogin = True		#用于区分账号登录和返回角色选择
		self.playerName = self.__ACCOUNT_NAME__
		self.faceModel = []				#角色脸部骨骼数据
		self.faceStyle = {}				#角色脸部样式数据
		self.modelList = []				#捏脸时需要自定义的模型编号列表，例如发型，发饰
		self._tempLoginDBID = 0							# 临时记录登录的角色的DBID
		self.loginState = Const.ACCOUNT_INITIAL_STATE	# 登录状态
		self.chargeRefresher = RefreshCharge( self )
		
		if self.loginTime == 0:
			self.loginTime = int(time.time())
		self.lastLoginTime = self.loginTime #上次登录时间
	
		if Settings.open_game_time_activation:
			if not self.isGetDefaultTime:
				self.defaultTimeBalance = Settings.default_game_time
				self.isGetDefaultTime = True
	
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_ACCOUNT
		
	# ----------------------------------------------------------------
	# public
	# ----------------------------------------------------------------
	
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		KBEDebug.INFO_MSG( "Account[%d:%d] onEntitiesEnabled" %(self.databaseID, self.id) )
		#KBEDebug.INFO_MSG("Account[%i]::onEntitiesEnabled:entities enable. mailbox:%s, clientType(%i), accountName=%s" % \
		#	(self.id, self.client, self.getClientType(), self.__ACCOUNT_NAME__))

		self.lastClientIpAddr = self.clientAddr[0];												# 记录最后登进来的IP地址，用于帐号重登录判断
		self.client.AccountCreateCB()

		#添加日志
		if self.isAccountLogin:
			g_logger.accountLogonLog( self.databaseID, self.__ACCOUNT_NAME__, self.lastClientIpAddr, "" )
			self.isAccountLogin = False
			self.loginTime = int(time.time())
			if not self.fastLoginTime:
				self.fastLoginTime = self.loginTime
			self.pickUpChargeOrder()	#登陆上来的时候，主动提取一下
		
		self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)
		
	def onDestroy(self):
		"""
		KBEngine method
		"""
		KBEDebug.INFO_MSG( "[%d:%d]%s: Account onDestroy" %(self.databaseID, self.id, self.playerName) )
		# 释放引用，以避免内存泄漏
		self.chargeRefresher.parentEntity = None
		self.chargeRefresher = None
		g_logger.accountLogoutLog( self.databaseID, self.__ACCOUNT_NAME__, self.lastClientIpAddr, "" ) #添加日志
		self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)

	def requestInitRoles(self):
		"""
		<Exposed method>
		客户端请求角色列表
		"""
		if not self.validateClientCall():
			return 

		if not self.isLoginState(Const.ACCOUNT_WAITTING_STATE):
			KBEDebug.ERROR_MSG("Account[%d:%d] init roles, state[%d] error" %(self.databaseID, self.id, self.loginState))
			return
		
		queryRoles( self.databaseID, self.onQueryRoles )
		
	def onQueryRoles( self, resultSet, rows, insertid, errstr ):
		"""
		The object to call back (e.g. a function) with the result of the command execution.
		The callback will be called with 3 parameters: result set, number of affected rows and error string.

		@param resultSet:	list of list of string like as [ [ field1, field2, ... ], ... ];
						The result set parameter is a list of rows.
						Each row is a list of strings containing field values.
						The XML database will always return a result set with 1 row and 1 column containing the return code of the command.
						The result set will be None for commands to do not return a result set e.g. DELETE,
						or if there was an error in executing the command.
		@param rows:	The number of a affected rows parameter is a number indicating the number of rows affected by the command.
						This parameter is only relevant for commands to do not return a result set e.g. DELETE.
						This parameter is None for commands that do return a result set or if there was and error in executing the command.
		@param errstr:	The error string parameter is a string describing the error that occurred if there was an error in executing the command.
						This parameter is None if there was no error in executing the command.
		"""
		if errstr is not None:
			KBEDebug.ERROR_MSG( errstr )
			return
			
		if self.isDestroyed:
			return

		KBEDebug.DEBUG_MSG( "resultSet--Begin>>>", resultSet )
		for k in resultSet:
			for index, value in enumerate( k ):
				if value == None:
					k[index] = 0
		KBEDebug.DEBUG_MSG( "resultSet--end>>>", resultSet )

		roles = resultSet									# [ [ id, playerName, level, raceclass, lifetime, hairNumber ], ... ]
		self._playerList = [[int(e[0]), int(e[29]), int(e[2]), int(e[35]), int(e[36]), e[1].decode( "utf-8" )] for e in roles]		# 汇总所有角色用于登录、删除操作时认证
		tmpPlayers = []
		for role in roles:
			# id
			if not isinstance(role[27], bytes):  #对旧账号的容错处理，目前使用BLOB类型进行存储，等捏脸功能完成后修改为字符串类型，见CST-6697
				role[27] = b'[]'
			if not bytes(role[27]):
				role[27] = b'[]'

			loginPlayer = {				
				"dbid"			: int( role[0] ),
				"playerName"	: role[1].decode( "utf-8" ),
				"level"			: int( role[2] ),
				"profession"	: int(role[3]),
				"camp"			: int(role[4]),
				"gender"		: int(role[5]),
				"modelNumber"	: bytes.decode( role[6] ),
				"bodyModel"		: bytes.decode( role[7] ),
				"headModel"		: bytes.decode( role[8] ),
				"suitsModel"	: bytes.decode( role[9] ),
				"hairModel"		: bytes.decode( role[10]),
				"adornModel"	: bytes.decode( role[11] ),
				"coatModel"		: bytes.decode( role[12] ),
				"pantsModel"	: bytes.decode( role[13] ),
				"shoesModel"	: bytes.decode( role[14] ),
				"cloakModel"	: bytes.decode( role[15] ),
				"hatModel"		: bytes.decode( role[16] ),
				"wristModel"	: bytes.decode( role[17] ),
				"handModel"		: bytes.decode( role[18] ),
				"waistModel"	: bytes.decode( role[19] ),
				"necklaceModel"	: bytes.decode( role[20] ),
				"lringModel"	: bytes.decode( role[21] ),
				"rringModel"	: bytes.decode( role[22] ),
				"weaponModel"	: bytes.decode( role[23] ),
				"fabaoModel"	: bytes.decode( role[24] ),
				"offlineTime"	: int( role[25] ),
				"actionNumber"	: bytes.decode( role[26] ),
				"faceModel"		: {"infos": json.loads(bytes.decode(role[27]))},
				"faceStyle"		: FaceStyle().createObjFromDict(json.loads(bytes.decode(role[28]))),
				"headAdornModel": bytes.decode( role[31] ),
				"faceAdornModel": bytes.decode( role[32] ),
				"backAdornModel": bytes.decode( role[33] ),
				"waistAdornModel": bytes.decode( role[34] ),
			}
			if loginPlayer["coatModel"]== "":
				if role[30]:
					coatItemID = int(role[30])
					modelParam = self.getWieldModelParam(coatItemID, loginPlayer["gender"])
					if modelParam.strip() != loginPlayer["coatModel"].strip():
						loginPlayer["coatModel"] = modelParam.strip()
				else:
					loginPlayer["coatModel"] = self.initModelCfg(loginPlayer["profession"], loginPlayer["gender"])["coatModel"]
			KBEDebug.DEBUG_MSG( "login info for %s" % ( loginPlayer ) )
			tmpPlayers.append( loginPlayer )

		self._isInitPlayerList = True
		if hasattr(self, "client") and  self.client:
			self.setAccountInfoToClient()

			if self.isCrossService:
				self.client.OnCrossServiceEnter(str(tmpPlayers[0]["dbid"]))
				self.isCrossService = 0
			self.client.RequestInitRolesCB( {"infos":tmpPlayers} )

	def getWieldModelParam(self, itemID, gender):
		"""获取玩家已装备物品的模型ID"""
		modelSources = {}
		Param1 = ItemFactory.ItemFactoryInst.getItemData(itemID)["Param1"].split(";")
		modelSources[1] = Param1[0]
		if len(Param1) == 1:
			modelSources[2] = Param1[0]
		elif len(Param1) > 1:
			modelSources[2] = Param1[1]
		return modelSources[gender]

	def modifyFace(self, faceInfoList, faceStyle, modelList):
		"""
		<Exposed method>
		设置玩家捏脸数据
		"""
		if not faceInfoList:
			KBEDebug.ERROR_MSG("modifyFace:boneData is empty!")
			return
		if not faceStyle:
			KBEDebug.ERROR_MSG("modifyFace:StyleData is empty!")
			return

		self.faceModel = faceInfoList["infos"]
		self.faceStyle = faceStyle
		self.modelList = modelList["modelList"]

	def createRole( self, playerName, profession, camp, gender ):
		"""
		<Exposed method>
		创建角色
		"""
		KBEDebug.INFO_MSG("Account[%i]::createRole: playerName=%s, camp=%i, gender=%i" %(self.id, playerName, camp, gender ))
		if not self.validateClientCall():
			return 
		
		if not self.isLoginState(Const.ACCOUNT_WAITTING_STATE):
			KBEDebug.ERROR_MSG("Account[%d:%d] create roles, state[%d] error" %(self.databaseID, self.id, self.loginState))
			return
		
		if (self.avatar is not None) and (not self.avatar.isDestroyed):
			#进入销毁队列了,那就提示下“服务器繁忙”
			if self.avatar.hasJoinDestroyQueue:
				self.statusMessage(csstatus.ACCOUNT_STATE_SERVER_BUSY)
				KBEDebug.INFO_MSG("Account[%d:%d] createRole busy, role[%d:%d] hasJoinDestroyQueue" %(self.databaseID, self.id, self.avatar.databaseID, self.avatar.id))
				return
		
			#提示客户端账号已经登陆
			self.statusMessage(csstatus.ACCOUNT_STATE_SERVER_FREQUENTLY)
			KBEDebug.ERROR_MSG("Account[%d:%d] createRole error, role[%d:%d] not destroy" %(self.databaseID, self.id, self.avatar.databaseID, self.avatar.id))
			return
			
		if not self._isInitPlayerList:
			#提示客户端账号列表还没有初始化完毕
			self.statusMessage( csstatus.ACCOUNT_STATE_ROLE_LIST_NOT_READY )
			self.client.CreateRoleCallback()
			return
			
		
		if len( self._playerList ) >= csconst.LOGIN_ROLE_UPPER_LIMIT:
			#提示客户端创建角色数量已经达到上限
			self.statusMessage( csstatus.ACCOUNT_STATE_CREATE_FULL )
			self.client.CreateRoleCallback()
			return

		#KBEDebug.INFO_MSG( "Account[%i]: create new player: playername = '%s', eMetaClass = %s" % (self.id, playerName, eMetaClass ) )

		if playerName == "" :
			#提示客户端角色名不能为空
			self.statusMessage(csstatus.ACCOUNT_STATE_NAME_NONE)
			self.client.CreateRoleCallback()
			return

		if len( playerName.encode("gbk") ) > csconst.ROLE_NAME_LENGTH_UPPER_LIMIT:
			#提示角色名字长度超出上限
			self.statusMessage(csstatus.ACCOUNT_STATE_NAME_TOOFAR)
			self.client.CreateRoleCallback()
			return
			
		isFirstRole = 0
		if len( self._playerList ) <= 0:
			isFirstRole = 1
		Data = RoleBornPropertyConfig.Datas
		strcamp = str(camp)
		strgender = str(gender)
		strprofession = str(profession)
		position = Data[strcamp][strgender][strprofession]["position"]
		direction = Data[strcamp][strgender][strprofession]["direction"]
		spaceScriptID = Data[strcamp][strgender][strprofession]["spaceScriptID"]
		faceData=json.dumps(self.faceModel)
		faceModel = bytes(faceData, encoding='utf-8')
		faceStyle = json.dumps(self.faceStyle)

		paramDict = { 
				"playerName"		:	playerName,
				"profession"		:	profession,
				"camp"				:	camp,
				"gender"			:	gender,
				"parentDBID"		:	self.databaseID,
				"position"			:	position,
				"direction"			:	direction,
				"spaceScriptID"		:	spaceScriptID,
				"isFirstRole"		:	isFirstRole,
				"reviveSpaceScriptID":  spaceScriptID,
				"revivePosition"	:   position,
				"reviveDirection"	:	direction,
				"createTime"		:	int(time.time()),
				"faceModel"			:	faceModel,
				"faceStyle"			:	faceStyle

			}

		otherparams = self.bornInit(profession, gender)
		if self.modelList:
			for m in self.modelList:
				if m["modelName"] in otherparams:
					otherparams.update({m["modelName"]: m["modelNumber"]})
		paramDict.update(otherparams)
		avatar = KBEngine.createEntityLocally( "Role", paramDict )
		self.avatar = avatar
		avatar.accountEntity = self
		self.__isLogin = True
		avatar.writeToDB( Functions.Functor(self.onWriteRoleToDBCollback, self.databaseID, self.__ACCOUNT_NAME__) )
	
	def bornInit(self, profession, gender):
		"""
		处理新建角色默认值设置
		"""
		params = {}
		params.update(self.initModelCfg(profession, gender))		#加载模型默认配置
		return params

	def initModelCfg(self, profession, gender):
		"""
		处理新建角色的模型配置
		"""
		return self.getDefaultBornModelCfg(profession, gender)

	def getDefaultBornModelCfg(self, profession, gender):
		"""
		根据角色信息获取角色的默认模型配置
		"""
		datas = LoadModule.openJsonCfg("InitModelTable.json")
		modelStr = csconst.ROLE_INIT_MODULE[gender].get(profession,"Default")
		return datas[modelStr]

			
	def onWriteRoleToDBCollback( self, databaseID, name, success, avatar ):
		if self.isDestroyed:
			if success:
				#添加日志
				g_logger.accountRoleAddLog( databaseID, name, avatar.databaseID, avatar.cellData["playerName"] )
		else:
			if success:
				self._playerList.append( [avatar.databaseID, avatar.tongDBID, int(avatar.cellData["level"]), 1, 0, avatar.cellData["playerName"]] )

				if not isinstance(avatar.cellData["faceModel"], bytes):
					avatar.cellData["faceModel"] = b'[]'
				if not bytes(avatar.cellData["faceModel"]):
					avatar.cellData["faceModel"] = b'[]'

				loginPlayer = {
					"dbid"			: avatar.databaseID,
					"playerName"	: avatar.cellData["playerName"],
					"level"			: avatar.cellData["level"],
					"profession"	: avatar.cellData["profession"],
					"camp"			: avatar.cellData["camp"],
					"gender"		: avatar.cellData["gender"],
					"modelNumber"	: avatar.cellData["modelNumber"],
					"actionNumber"	: avatar.cellData["actionNumber"],
					"bodyModel"		: avatar.cellData["bodyModel"],
					"headModel"		: avatar.cellData["headModel"],
					"suitsModel"	: avatar.cellData["suitsModel"],
					"hairModel"		: avatar.cellData["hairModel"],
					"adornModel"	: avatar.cellData["adornModel"],
					"coatModel"		: avatar.cellData["coatModel"],
					"pantsModel"	: avatar.cellData["pantsModel"],
					"shoesModel"	: avatar.cellData["shoesModel"],
					"cloakModel"	: avatar.cellData["cloakModel"],
					"hatModel"		: avatar.cellData["hatModel"],
					"wristModel"	: avatar.cellData["wristModel"],
					"handModel"		: avatar.cellData["handModel"],
					"waistModel"	: avatar.cellData["waistModel"],
					"necklaceModel"	: avatar.cellData["necklaceModel"],
					"lringModel"	: avatar.cellData["lringModel"],
					"rringModel"	: avatar.cellData["rringModel"],
					"weaponModel"	: avatar.cellData["weaponModel"],
					"fabaoModel"	: avatar.cellData["fabaoModel"],
					"offlineTime"	: 0,
					"faceModel"		: {"infos": json.loads(bytes.decode(avatar.cellData["faceModel"]))},
					"faceStyle"		: FaceStyle().createObjFromDict(json.loads(avatar.cellData["faceStyle"])),
					"headAdornModel"	: avatar.cellData["headAdornModel"],
					"faceAdornModel"	: avatar.cellData["faceAdornModel"],
					"backAdornModel"	: avatar.cellData["backAdornModel"],
					"waistAdornModel"	: avatar.cellData["waistAdornModel"]
				}
				
				if self.client:
					self.client.AddRoleCB( loginPlayer )							# notify client
					#提示客户端账号创建成功
				#添加日志
				g_logger.accountRoleAddLog( self.databaseID, self.__ACCOUNT_NAME__, avatar.databaseID, avatar.cellData["playerName"] )
			else:
				#提示客户端账号名字已经存在
				self.statusMessage( csstatus.ACCOUNT_STATE_NAME_EXIST )

			if self.client:
				self.client.CreateRoleCallback()
				self.faceModel = []
				self.faceStyle = {}
		# destroy entity
		avatar.destroy( writeToDB = False )
		self.__isLogin = False

	def deleteRole( self, databaseID ):
		"""
		<define method>
		删除一个角色
		
		@type  databaseID: INT64
		"""
		KBEDebug.INFO_MSG("Ready to delete Role[%s], self.deleteDBID[%s], playerList[%s]"%(str(databaseID), str(self.deleteDBID), str(self._playerList)))
		if not self.validateClientCall():
			return 
			
		if not self.isLoginState(Const.ACCOUNT_WAITTING_STATE):
			KBEDebug.ERROR_MSG("Account[%d:%d] delete roles, state[%d] error" %(self.databaseID, self.id, self.loginState))
			return
			
		if self.deleteDBID is not None:
			self.statusMessage( csstatus.ACCOUNT_STATE_SERVER_BUSY )
			return
		
		isExists = False
		for e in self._playerList:
			if e[0] == databaseID:
				isExists = True
				break
				
		if not isExists:
			self.statusMessage( csstatus.ACCOUNT_STATE_ROLE_NOT_EXIST )
			return

		def deleteResult( result, rows, insertid, errstr ):
			if errstr is None :
				self.client.DeleteRoleCB( self.deleteDBID )
				player  = None
				for e in self._playerList:
					if e[0] == self.deleteDBID:
						self._playerList.remove(e)
						KBEngine.globalData["TongMgr"].deleteRole(e[0], e[1])
						break
				
				if self.lastLogonDBID == self.deleteDBID:
					if len(self._playerList) > 0:
						self.lastLogonDBID = self._playerList[0][0]
					else:
						self.lastLogonDBID = 0
			else:
				KBEDebug.ERROR_MSG( "--------->deleteRole:delete role fail!" )
			self.deleteDBID = None
			
		self.deleteDBID = databaseID
		deleteRole( databaseID, deleteResult )
		
		#添加日志
		g_logger.accountRoleDelLog( self.databaseID, self.__ACCOUNT_NAME__, databaseID )


	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		KBEDebug.INFO_MSG("Account[%i]::onLogOnAttempt: ip=%s, port=%i, selfclient=%s" % (self.id, ip, port, self.client))
		
		lastIP = "%i.%i.%i.%i" % ( self.lastClientIpAddr & 0xff, ( self.lastClientIpAddr >> 8 ) & 0xff, ( self.lastClientIpAddr >> 16 ) & 0xff, ( self.lastClientIpAddr >> 24 ) & 0xff )
		if ip == lastIP or self.lastClientIpAddr == 0:	# 如果登录的IP与最后一次登录的IP相同则允许登录
			#只有在允许登录这一前提下，才能将相应的角色踢下线
			if self.avatar:
				try:
					self.avatar.kickFromAccount()
				except:
					KBEDebug.ERROR_MSG("Account[%i]::onLogOnAttempt: kickFromAccount error")
			return KBEngine.LOG_ON_ACCEPT
			
		return KBEngine.LOG_ON_REJECT
		
	def kickAction( self, kickerMB ):
		"""
		define method
		Account踢下线
		"""
		self.logoff()
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		KBEDebug.DEBUG_MSG("Account[%d:%d]%s.onClientDeath:" % (self.databaseID, self.id, self.playerName))
		self.logoff()
			
	def logoff(self):
		"""
		<Exposed method>
		玩家下线
		"""
		if not self.validateClientCall():
			return 
			
		# 这里返回不往后走了，防止短时间内再次上线，但是Role还未销毁而出现其他异常
		# CST-5446
		# 这里实际测试中发现，新创的账号在写入数据库的过程中踢下线，可能会有一些问题
		# 写入数据库成功后的回调函数中，可能avatar已经销毁，导致一些其他错误（比如下线排队管理器中，记录的是该entity的DBID（但其在写入成功前为0））
		if self.avatar and not self.avatar.isDestroyed and self.avatar.databaseID:
			self.avatar.kickFromAccount()
			return
		
		KBEDebug.INFO_MSG( "(%d:%d): logoff." %(self.databaseID, self.id) )
		self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)
		self.destroy()

	def onTimer( self, timerID, userData ): 
		"""
		定时器回调
		"""
		pass

	def login(self, databaseID, clientMacAddr):
		"""
		<Exposed method>
		player login by databaseID

		@param databaseID: indicate which role exist in Role table want to login
		@type  databaseID: INT64
		@return: none
		"""
		if not self.validateClientCall():
			return
		
		self.currLoginMacAddr = clientMacAddr
		
		if not self.fastLoginMacAddr:
			self.fastLoginMacAddr = self.currLoginMacAddr
		
		if Settings.open_game_time_activation:
			for playInfo in self._playerList:
				if playInfo[0] == databaseID and playInfo[2] >= Settings.start_billing_level:
					if self.payTimeBalance + self.defaultTimeBalance <= 0:
						self.client.GameTimeHasUsedUp()
						return
		
		if (self.avatar is not None) and (not self.avatar.isDestroyed):
			#进入销毁队列了,那就提示下“服务器繁忙”
			if self.avatar.hasJoinDestroyQueue:
				self.statusMessage(csstatus.ACCOUNT_STATE_SERVER_BUSY)
				KBEDebug.INFO_MSG("Account[%d:%d] loginRole busy, role[%d:%d] hasJoinDestroyQueue" %(self.databaseID, self.id, self.avatar.databaseID, self.avatar.id))
				return
		
			#提示客户端账号已经登陆
			self.statusMessage(csstatus.ACCOUNT_STATE_ROLE_ALREADY_LOGIN)
			KBEDebug.ERROR_MSG("Account[%d:%d] loginRole error, role[%d:%d] not destroy" %(self.databaseID, self.id, self.avatar.databaseID, self.avatar.id))
			return
		
		isExists = False
		for e in self._playerList:
			if e[0] == databaseID:
				if e[3] == csdefine.ROLE_STATE_FROZEN:
					if e[4] > time.time():
						endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e[4]))
						self.client.RoleFrozenNotification(str(endTime))
						return
					else:
						clearRoleFrozenState(e[0])
				isExists = True
				break
		
		if not isExists:
			#提示客户端账号不存在当前选择角色
			self.statusMessage(csstatus.ACCOUNT_STATE_ROLE_NOT_EXIST)
			return
		
		#状态不对
		if not self.isLoginState(Const.ACCOUNT_WAITTING_STATE):
			if self.isLoginState(Const.ACCOUNT_LOGIN_STATE):
				self.statusMessage(csstatus.ACCOUNT_STATE_ID_ALREADY_LOGIN) #提示客户端账号已经登陆
			KBEDebug.ERROR_MSG("Account[%s:%d:%d] LoginState[%d] error" %(self.__ACCOUNT_NAME__, self.databaseID, self.id, self.loginState))
			return
		
		self._tempLoginDBID = databaseID
		self.changeLoginState(Const.ACCOUNT_LOGIN_STATE)
		
	def loginRole(self):
		"""
		define method
		登录排队通知登录
		"""
		if (self.avatar is not None) and (not self.avatar.isDestroyed):
			#进入销毁队列了,那就提示下“服务器繁忙”
			if self.avatar.hasJoinDestroyQueue:
				self.statusMessage(csstatus.ACCOUNT_STATE_SERVER_BUSY)
				return
			
			#提示客户端账号已经登陆
			self.statusMessage(csstatus.ACCOUNT_STATE_ROLE_ALREADY_LOGIN)
			return
		
		if not self.isLoginState(Const.ACCOUNT_LOGIN_STATE):
			KBEDebug.ERROR_MSG("Account[%d:%d] login role, state[%d] error" %(self.databaseID, self.id, self.loginState))
			return
			
		#当前正在加载角色
		if self.__isLogin:
			self.statusMessage( csstatus.ACCOUNT_STATE_ROLE_ALREADY_LOGIN )
			return
		
		isExists = False
		for e in self._playerList:
			if e[0] == self._tempLoginDBID:
				isExists = True
				break
		
		if not isExists:
			KBEDebug.ERROR_MSG("not found role[%d]" %(self._tempLoginDBID))
			#提示客户端账号不存在当前选择角色
			self.statusMessage(csstatus.ACCOUNT_STATE_ROLE_NOT_EXIST)
			return
		
		KBEDebug.INFO_MSG( " create player by databaseID %i" %self._tempLoginDBID )
		if hasattr(self, "client") and self.client:
			self.client.TimeSynchronization( Functions.convertToClientTime( Functions.getTime()) )		# 客户端时间同步
		
		self.__isLogin = True
		KBEngine.createEntityFromDBID( "Role", self._tempLoginDBID, self.onLoadedAvatar )

	def onLoadedAvatar( self, baseRef, databaseID, wasActive ):
		"""
		This is an optional callable object that will be called when the function createEntityFromDBID operation completes.
		The callable object will be called with three arguments: baseRef, databaseID and wasActive.
		If the operation was successful then baseRef will be a reference to the newly created Base entity,
		databaseID will be the database ID of the entity and wasActive will indicate whether the entity was already active.
		If wasActive is true,
		then baseRef is referring to a pre-existing Base entity and may be a mailbox rather than a direct reference to a base entity.
		If the operation failed, then baseRef will be None,
		databaseID will be 0 and wasActive will be false.
		The most common reason for failure is the that entity does not exist in the database but intermittent failures like timeouts or unable to allocate IDs may also occur.
		"""
		#print( "Account::onLoadedAvatar(), wasActive = ", type(wasActive), " -> ", wasActive )
		# 理论上，下面这行永远不会触发
		assert not wasActive, "(%i): the target entity was active, I can't do it." % self.id
		
		self.__isLogin = False
		if self.isDestroyed:
			# 经测试，在某些情况下确实会发生此问题。
			KBEDebug.ERROR_MSG( "%s(%i): Failed to load Avatar for player, because account entity is destroyed." % (self.playerName, self.id), baseRef )
			if baseRef is not None:
				baseRef.destroySelf()
			return
			
		if baseRef != None:
			KBEDebug.INFO_MSG( "Account::onLoadedAvatar(), '%s' - '%s'" % ( self.playerName, baseRef.cellData["playerName"] ) )
			self.__onAvatarReady( baseRef )
		else:
			KBEDebug.INFO_MSG( "%s(%i): Failed to load Avatar for player." % (self.playerName, self.id) )
			self.__onAvatarReady( None )

	def __onAvatarReady( self, avatar ):
		if avatar != None:
			self.lastLogonDBID = avatar.databaseID
			self.avatar = avatar
			avatar.accountEntity = self
			avatar.accountName = self.playerName
			#初始化role的相关属性(仙石、灵石、玄石)
			avatar.initRoleAttribute( self )
			self.giveClientTo( avatar )
			self._destroySelf = False
			self.changeLoginState(Const.ACCOUNT_GAMMING_STATE)
		else:
			#创建角色失败
			self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)

	def onAvatarDeath( self ):
		"""
		<<Define method>
		"""
		if self.isDestroyed:
			return
		
		self.avatar = None
		self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)
		
		if not self.hasClient:
			KBEDebug.INFO_MSG( "[%d:%d]%s: Avatar is destroyed, I will destroy self also." %(self.databaseID, self.id, self.playerName) )
			self.destroy()
			
	def statusMessage( self,statusID, *args ):
		"""
		<Define method>
		发送提示信息
		@type			statusID : UINT32
		@param			statusID : 状态消息,defined in data/csstatus.py
		@type			args	 : UNICODE
		@param			args	 : 消息附加参数
		@return					 : None
		"""
		tempArgs = ""
		if args == ():
			pass
		else:
			index = 0
			for arg in args:
				if index != 0:
					tempArgs += ","
				index +=1
				tempArgs += str(arg)
		self.client.OnStatusMessageCB(statusID, tempArgs)

	def testAddXianShi( self, value ):
		"""
		尝试增加仙石，判断是否超出上限

		@param value : 仙石的变化值
		@type value : INT64
		"""
		return self.xianshi + value < csconst.ROLE_XIANSHI_UPPER_LIMIT

	def addXianShi( self, value, reason, order = "" ):
		"""
		增减玩家仙石
		"""
		if self.xianshi + value > csconst.ROLE_XIANSHI_UPPER_LIMIT:
			return
		old = self.xianshi
		self.xianshi += value
		playerDBID = 0
		name = ""
		if self.avatar is not None:
			playerDBID = self.avatar.databaseID
			name = self.avatar.playerName
			self.avatar.updateXianShi( self.xianshi )
		g_logger.xianshiChangeLog( self.databaseID, playerDBID, name, old, self.xianshi, reason, order )
		
	def testAddXuanShi( self, value ):
		"""
		尝试增加玄石，判断是否超出上限

		@param value : 玄石的变化值
		@type value : INT64
		"""
		return self.xuanshi + value < csconst.ROLE_XUANSHI_UPPER_LIMIT

	def addXuanShi( self, value, reason, order = ""):
		"""
		增减玩家玄石
		"""
		if self.xuanshi + value > csconst.ROLE_XUANSHI_UPPER_LIMIT:
			return
		old = self.xuanshi
		self.xuanshi += value
		playerDBID = 0
		name = ""
		if self.avatar is not None:
			playerDBID = self.avatar.databaseID
			name = self.avatar.playerName
			self.avatar.updateXuanShi( self.xuanshi )
			
		g_logger.xuanshiChangeLog( self.databaseID, playerDBID, name, old, self.xuanshi, reason, order )
		
	def pickUpChargeOrder( self ):
		"""
		define method
		提取充值订单
		"""
		if self.isDestroyed: return
		self.chargeRefresher.refresh()
		
	def changeLoginState( self, state ):
		"""
		define method
		改变登录状态
		"""
		if self.loginState == state:
			return
		
		oldState = self.loginState
		self.loginState = state
		
		if self.loginState == Const.ACCOUNT_WAITTING_STATE:
			if oldState == Const.ACCOUNT_GAMMING_STATE:
				KBEngine.globalData["LoginAttemperMgr"].removeLoginAcc(self)
			else:
				KBEngine.globalData["LoginAttemperMgr"].removeLoginQueue(self)
		elif self.loginState == Const.ACCOUNT_LOGIN_STATE:
			KBEngine.globalData["LoginAttemperMgr"].requestLoginRole(self.isVIP, self)
	
	def isLoginState( self, state ):
		"""
		是否在state状态
		"""
		return self.loginState == state
		
	def reqCancelLoginQueue( self ):
		"""
		Exposed method
		取消登陆排队
		"""
		#角色已经创建出来了,这里是有可能出现的
		if (self.avatar is not None) and (not self.avatar.isDestroyed):
			self.client.OnCancelLoginQueue(False)
			return
		
		#不在登陆排队状态，理论上这里不应该出现
		if not self.isLoginState(Const.ACCOUNT_LOGIN_STATE):
			self.client.OnCancelLoginQueue(False)
			ERROR_MSG("Account[%d:%d] error state[%d], cancel login queue fail" %(self.databaseID, self.id, self.loginState))
			return
		
		#这里也是有可能出现的，正在加载角色的过程中取消排队，这里就不给取消排队了
		if self.__isLogin:
			self.client.OnCancelLoginQueue(True)
			return
		
		self.changeLoginState(Const.ACCOUNT_WAITTING_STATE)
		
	def tongOnJoin( self, roleDBID, tongDBID ):
		"""
		"""
		for i in range(len(self._playerList)):
			if self._playerList[i][0] == roleDBID:
				self._playerList[i][1] = tongDBID
				break

	def setAccountInfoToClient(self):
		"""
		设置账户信息到客户端
		"""
		accountInfo = {
			"gameTimeBalance": int(self.payTimeBalance + self.defaultTimeBalance), #充值付费时间 + 系统默认赠送时间
			"lastLoginTime": str(self.lastLoginTime * csconst.TIME_ENLARGE_MULTIPLE),
			"loginTime": str(self.loginTime * csconst.TIME_ENLARGE_MULTIPLE),
			}

		self.client.SetAccountInfo(accountInfo)
		
	def getGameTimeBalance(self):
		"""
		"""
		return self.payTimeBalance + self.defaultTimeBalance

	def addGameTimeBalance(self, value):
		"""
		添加游戏时间
		"""
		#只在付费时间上添加
		self.payTimeBalance += int(value)
		
		if self.avatar:
			self.avatar.onGameTimeRecharge(value)

	def subGameTimeBalance(self, value):
		"""
		减少游戏时间
		"""
		value = int(value)
		#先在系统赠送时间中扣除
		if self.defaultTimeBalance >= value:
			self.defaultTimeBalance -= value
			return

		tempValue = value
		if self.defaultTimeBalance > 0:
			tempValue = value - self.defaultTimeBalance
			self.defaultTimeBalance = 0

		self.payTimeBalance -= tempValue
		if self.payTimeBalance < 0:
			self.payTimeBalance = 0
			
	def GMSetPayGameTime(self, amount):
		"""
		GM指令设置付费时间
		"""
		self.avatar.beforeGMSetGameTime()
		self.payTimeBalance = int(amount)
		self.avatar.onGameTimeRecharge(amount)
		
	def GMSetDefaultGameTime(self, amount):
		"""
		GM指令设置付费默认时间
		"""
		self.avatar.beforeGMSetGameTime()
		self.defaultTimeBalance = int(amount)
		self.avatar.onGameTimeRecharge(amount)
		
	def onWriteToDB(self, cellData):
		"""
		KBEngine method，调用writeToDB的回调(在存入数据库之前调用)
		"""
		self.recordTime = int(time.time())
		
	def requestActivationKey(self, key, playerName):
		"""
		Exposed method
		输入礼包码
		"""
		if not key or not playerName:
			self.client.onActivationKeyResult(False)
			return
			
		if self.hasActivation:
			self.statusMessage(csstatus.ACTIVATION_KEY_ACCOUNT_HAS_USED)
			self.client.onActivationKeyResult(False)
			return
			
		if len(key) != 16:
			self.statusMessage(csstatus.ACTIVATION_KEY_ERROR)
			self.client.onActivationKeyResult(False)
			return
		
		if len(self._playerList) <= 0:
			self.statusMessage(csstatus.ACTIVATION_KEY_NO_ROLE)
			self.client.onActivationKeyResult(False)
			return
		
		for playInfo in self._playerList:
			if playInfo[5] == playerName:
				sql_cmd = MysqlUtility.makeSafeSql(SELECT_ACTIVATION_KEY_SQL, (key,))
				KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onSelectCallBack, key, playerName, sql_cmd))
				return
				
		self.client.onActivationKeyResult(False)
			
	def onSelectCallBack( self, key, playerName, sql_cmd, results, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return	
		
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return	
		
		if int(results[0][0]) <= 0:
			self.statusMessage(csstatus.ACTIVATION_KEY_ERROR)
			if hasattr(self, "client") and self.client:
				self.client.onActivationKeyResult(False)
			return
		
		itemStr = (results[0][1]).decode( "utf-8" )
		sql_cmd = UPDATE_ACTIVATION_KEY_SQL.format(self.databaseID)
		sql_cmd = MysqlUtility.makeSafeSql(sql_cmd, (playerName, key,))
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onUpdateCallBack, playerName, itemStr, sql_cmd))
		
	def onUpdateCallBack( self, playerName, itemStr, sql_cmd, results, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			if hasattr(self, "client") and self.client:
				self.client.onActivationKeyResult(False)
			return
		
		#不等于1的话，可能该礼包码已经失效
		if rows == 1:
			items = []
			self.hasActivation = True
			self.statusMessage(csstatus.ACTIVATION_KEY_USE_SUCCESS, playerName)
			sender, title, content = self.getMailInfo(csdefine.REMAIN_ITEM_FENGCE_GIFT, "")
			
			if itemStr:
				itemList = itemStr.split("|")
				for data in itemList:
					itemData = data.split(":")
					if len(itemData) != 2:
						KBEDebug.ERROR_MSG("ACTIVATION_KEY item config error. %s" %(itemStr))
						return
					
					itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(int(itemData[0]), int(itemData[1]), {})
					if not itemInst:
						KBEDebug.ERROR_MSG("MailContentData.json has not item=%i"%(itemID))
						return
					
					items.append(itemInst)
			
			KBEngine.globalData["MailManager"].send( None, playerName, csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0, 0, items, 0, 0 )
			if hasattr(self, "client") and self.client: self.client.onActivationKeyResult(True)
			return
		
		self.statusMessage(csstatus.ACTIVATION_KEY_HAS_USED)
		if hasattr(self, "client") and self.client:
			self.client.onActivationKeyResult(False)
		
	def getMailInfo(self, remianType, titleKey):
		"""
		根据不同类型的奖励获取方式和内容关键字获取邮件的信息
		"""
		sender = MailInfos[remianType]["sender"]
		if remianType == csdefine.REMAIN_ITEM_GIFT or remianType == csdefine.REMAIN_ITEM_DROPBOX:
			title = MailInfos[remianType]["title"]
			content = MailInfos[remianType]["content"]
		else:
			title = MailInfos[remianType]["title"].replace("{0}", titleKey)
			content = MailInfos[remianType]["content"].replace("{0}", titleKey)
		return sender, title, content
		
		