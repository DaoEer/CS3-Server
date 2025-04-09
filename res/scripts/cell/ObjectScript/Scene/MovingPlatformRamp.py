#############
#移动平台脚本
#############

import ObjectScript.Scene.MovingPlatform as MovingPlatform


class MovingPlatformRamp( MovingPlatform.MovingPlatform ):
	"""
	移动平台 显示——透明——销毁
	"""
	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.displayTime = 0.0				# 显示时间
		self.rampTime = 0.0					# 渐变时间
		self.endRampTime = 0.0				# 渐变结束后的销毁时间
 
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		if configData["Param2"]:
			time = [float(i) for i in configData["Param2"].split("|")]
			if len(time) >= 3:
				self.displayTime = time[0]
				self.rampTime = time[1]
				self.endRampTime = time[2]