
import KBEDebug
import KBEngine
import Math
import csdefine


def MonsterNavigateToPoint(startPos, targetPos):
	role = getRole()
	createDict = {}
	createDict[ "spawnPos" ] = Math.Vector3( startPos )
	createDict[ "spawnDir" ] = tuple(Math.Vector3((0,0,0)))
	obj = role.createMonster("29900101", tuple(Math.Vector3(startPos)), tuple(Math.Vector3((0,0,0))), createDict)
	#obj.navigateToPointTest(Math.Vector3( targetPos ), 1.0)
	obj.changeState( csdefine.ENTITY_STATE_FREE )
	obj.addTimerCallBack(1.2, "navigateToPointTest", (Math.Vector3( targetPos ), 1.0))
	#obj.addTimerRepeat(0.1, "navigateToPointTest", (Math.Vector3( targetPos ), 1.0))

def MonsterNavigatePointsToPoints(startPos, targetPos):
	role = getRole()
	navigateStartPos = Math.Vector3(startPos)
	navigateEndPos = Math.Vector3(targetPos)
	layers = role.getCurrentSpace().getScript().getNavmeshLayers()
	for i in range(layers):
		startPosList = KBEngine.collideVertical(role.spaceID, i, startPos, 20, -20)
		for j in range(layers):
			endPosList = KBEngine.collideVertical(role.spaceID, j, targetPos, 20, -20)
			if len(startPosList) > 0 and len(endPosList) > 0:
				for startTuple in startPosList:
					navigateStartPos = Math.Vector3(startTuple)
					for endTuple in endPosList:
						navigateEndPos = Math.Vector3(endTuple)
						MonsterNavigateToPoint(navigateStartPos, navigateEndPos)


def MonsterNavigateRect(startPos, lenOfX, lenOfZ, segment):
	navigateStartPos = Math.Vector3(startPos)
	navigateEndPos = Math.Vector3(startPos)
	startX = 0
	while startX <= lenOfX:
		navigateStartPos.x += startX
		startZ = 0
		while startZ <= lenOfZ:
			navigateStartPos.z += startZ
			endX = lenOfX
			while endX >= startX:
				navigateEndPos.x += endX
				endZ = lenOfZ
				while endZ >= startZ:
					if endX > startX or ( endX == startX and endZ > startZ):
						navigateEndPos.z += endZ
						#print("navigateStartPos is",navigateStartPos,"navigateEndPos is",navigateEndPos)
						#MonsterNavigateToPoint(Math.Vector3(navigateStartPos), Math.Vector3(navigateEndPos))
						MonsterNavigatePointsToPoints(Math.Vector3(navigateStartPos), Math.Vector3(navigateEndPos))
					navigateEndPos.z = startPos.z
					endZ -= lenOfZ / segment
				navigateEndPos.x = startPos.x
				endX -= lenOfX /segment
			navigateStartPos.z = startPos.z
			startZ += lenOfZ / segment
		navigateStartPos.x = startPos.x
		startX += lenOfX / segment

def getRole():
	"""
	获取服务器唯一玩家
	"""
	for entity in KBEngine.entities.values():
		if entity.__class__.__name__ == "Role":
			return entity