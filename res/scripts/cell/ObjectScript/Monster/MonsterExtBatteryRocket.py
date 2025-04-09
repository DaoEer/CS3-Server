# -*- coding: utf-8 -*-
import ObjectScript.Monster.MonsterExtBattery as MonsterExtBattery
import KBEDebug
import time


class MonsterExtBatteryRocket( MonsterExtBattery.MonsterExtBattery ):
	def __init__( self ):
		MonsterExtBattery.MonsterExtBattery.__init__( self )
#		self.batteryType = 1				# 弹药类型
#		self.ammo = 0						# 弹药
#		self.guidInterval = 0.0				# 引导间隔
		self.guidTimer = 0					# 引导次数
#		self.inputYawScale = 1.0			# 摄像机灵敏度
		self.loadCD = 0.0					# 装弹时间
#		self.flySpeed = 1.0					# 炮弹飞行速度
#		self.gravityScale = 1.0				# 重力倍率影响
#		self.projectSkillID = 0				# 炮弹爆炸释放技能

	def initData( self, configData ):
		MonsterExtBattery.MonsterExtBattery.initData( self, configData )
		projectData = configData["Param1"].split("|")
		if len(projectData) >= 2:
			self.setEntityProperty("ammo",int(projectData[1]))
		if len(projectData) >= 4:
			self.guidTimer = int(projectData[3])
		
#		if configData[ "Param2" ]:
#			self.inputYawScale = float(configData[ "Param2" ])
		if configData[ "Param3" ]:
			self.loadCD = float(configData[ "Param3" ])
#		projectData = configData["Param4"].split("|")
#		if len(projectData) >= 3:
#			self.flySpeed = float(projectData[0])
#			self.gravity = float(projectData[1])
#		if configData[ "Param5" ]:
#			self.projectSkillID = int(configData[ "Param5" ])

			
