#############
#移动平台脚本
#############

import ObjectScript.Scene.MovingPlatform as MovingPlatform


class MovingPlatformShade( MovingPlatform.MovingPlatform ):
	"""
	移动平台 逐渐透明至消失
	"""
	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.warnParticle = ""					# 预警光效
		self.shadeTime = 0.0					# 开始渐变时间
		self.shadeDurationTime = 0.0			# 渐变时间（显示-》透明）
		self.endShadeTime = 0.0					# 结束透明状态
		self.endShadeDurationTime = 0.0			# 渐变时间（透明-》显示）

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		if configData["Param2"]:
			time = configData["Param2"].split("|")
			self.shadeTime = float( time[0] )
			if len(time) >= 2:
				self.shadeDurationTime = float( time[1] )
			if len(time) >= 3:
				self.warnParticle = time[2]
		if configData["Param3"]:
			time = configData["Param3"].split("|")
			self.endShadeTime = float( time[0] )
			if len(time) >= 2:
				self.endShadeDurationTime = float( time[1] )



