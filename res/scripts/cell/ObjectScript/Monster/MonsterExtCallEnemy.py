import KBEngine
import Math
import csdefine
import ObjectScript.Monster.MonsterExtCall as MonsterExtCall
class MonsterExtCallEnemy( MonsterExtCall.MonsterExtCall ):

	def __init__( self ):
		MonsterExtCall.MonsterExtCall.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MonsterExtCall.MonsterExtCall.initData( self, configData )
		self.attrSkill = []

	def chooseTargetByDistance( self, selfEntity):
		"""
		重载
		只是将召唤怪自己敌对目标也加入需要战斗的列表
		普通的召唤怪是只打主人的敌对目标
		"""
		ownerEntity = selfEntity.getOwnerEntity()
		if not ownerEntity:
			return
		enemyIDList = [e for e in ownerEntity.enemyList.keys() if selfEntity.monsterAICheckInViewRange(e)]
		for e in selfEntity.enemyList.keys():
			enemyIDList.append(e)
			
		if not len(enemyIDList):
			selfEntity.changeState(csdefine.ENTITY_STATE_RESET)
			return
			
		minDis = 100000.0
		targetID = 0
		for eID in enemyIDList:
			e = KBEngine.entities.get(eID,None)
			if not e:
				continue
			distance = e.position.flatDistTo( ownerEntity.position )
			if distance<=minDis:
				minDis = distance
				targetID = eID
		selfEntity.behControlReset(csdefine.BEHAVIOUR_TYPE_SPELL)
		selfEntity.setTargetID(targetID)