# -*- coding: utf-8 -*-
import KBEngine
from CoreObject import CMonsterObject
import csdefine
import Const
import KBEDebug
from Barracks.SoldierLevelCompareMonsterLevelCfg import Datas
import ItemSystemExp


class CMonster( CMonsterObject.CMonsterObject ):
	"""
	客户端AI测试怪(跟随玩家)
	"""
	def __init__( self ):
		CMonsterObject.CMonsterObject.__init__( self )
		self.moveSpeed = 6.0

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT)
		
	def CELL_onSetControlledBy(self, srcEntityID):
		"""
		Exposed method
		设置被玩家控制
		"""
		if srcEntityID == self.id:
			return
			
		if srcEntityID != self.controlEntityID:
			return
		
		self.onControl(srcEntityID)


	def onControl(self, controllerID):
		"""
		被控制
		"""	
		controller = KBEngine.entities.get(controllerID)
		if controller is None: return
		
		self.controlledBy = controller.base
		controller.roleCmdOnControlled(self.scriptID, self.id)
		controller.client.RoleCmdOnControlled(self.scriptID, self.id)

	def unControl(self):
		"""
		解除控制
		"""
		self.destroySelf()
	
	def getControlEntity( self ):
		return KBEngine.entities.get( self.controlEntityID )
	
	def IsValidMsg( self, exposed,  *args ):
		"""
		判断客户端过来的消息是否是有效消息
		"""
		return True

	def onConctrollerLogin(self, controllerID):
		"""
		控制者上线
		"""
		self.onControl(controllerID)

	def onControllerLogoff(self):
		"""
		控制者下线
		"""
		self.unControl()

	def onEnterDead(self):
		"""
		"""
		CMonsterObject.CMonsterObject.onEnterDead(self)

		self.changeCMonsterAIState(csdefine.CMONSTER_AI_STATE_DEAD)

		controller = self.getControlEntity()
		if not controller:
			return
		controller.onSoliderDead( controller.callArmyIndex, self.soldierType, self.scriptID, self.index )

	def changePosture(self, modelID, inActionID, outActionID):
		"""
		变换姿势
		"""
		self.allClients.CLIENT_ChangeShowPosture(modelID, inActionID, outActionID)

	def RPC_ChangePosture(self, srcEntityID, modelID, inActionID, outActionID):
		"""
		exposed method
		"""
		if self.IsValidMsg(srcEntityID,  modelID, inActionID, outActionID):
			self.changePosture(modelID, inActionID, outActionID)

	def startFallLand( self ):
		"""
		从梯子开始掉落
		"""
		self.startFallingHeight = self.position.y

	def notifyMonsterEndFallLand( self, srcEntityID ):
		"""
		结束掉落
		"""
		damage = int(self.HP_Max * (self.startFallingHeight - self.position.y) / 15)
		if damage < 0:
			return
		if self.HP < damage:
			self.setHP( 0 )
		else:
			self.setHP( self.HP - damage )

	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		profession = self.profession
		attrlevel = self.attrLevel
		level = self.level
		if Datas.get( self.level ):
			level = Datas[level]
		#KBEDebug.DEBUG_MSG("Monster[%s], profession[%d], attrlevel[%d], level[%d]"%(self.scriptID, profession, attrlevel, level))
		return ItemSystemExp.g_MonsterPropertyValueCfg.getData(profession, attrlevel, level)


	def beforeDestroy(self):
		"""
		"""
		CMonsterObject.CMonsterObject.beforeDestroy(self)
		controller = self.getControlEntity()
		if controller:
			controller.beforeSoldierDestroy(self.id)

