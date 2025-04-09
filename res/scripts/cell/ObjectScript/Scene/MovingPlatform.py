#############
#移动平台脚本
#############

from ObjectScript.Scene import SceneObject
from ObjectScript.Scene import ScenePropertyLoader


class MovingPlatform( SceneObject.SceneObject,ScenePropertyLoader.ScenePropertyLoader ):
	def __init__( self ):
		SceneObject.SceneObject.__init__( self )
		ScenePropertyLoader.ScenePropertyLoader.__init__( self )
		self.navmeshPath = ""
		self.moveSpeed = 0
		self.uname = ""

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		SceneObject.SceneObject.initData( self, configData )
		ScenePropertyLoader.ScenePropertyLoader.initData( self, configData )
		self.uname = configData["Uname"]
		if configData["Param1"]:
			self.navmeshPath = "space/A_PLATFORM_NAVIMESH/%s"%configData["Param1"]
		
		if 'WalkSpeed' in configData:
			self.moveSpeed = float( configData["WalkSpeed"] )



