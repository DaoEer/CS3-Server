# -*- coding:utf-8 -*-
import random
from LoadModule import *



class SpaceCopyLLBZNoticeLoader:
	"""
	玲珑宝珠 通知配置
	"""
	def __init__(self):
		self.lingqiConfig = {}
		self.linghuanConfig = {}

	def loadConfig( self ):
		config = openJsonCfg("SpaceCopyLLBZNotice.json")
		for data in config:
			if data["type"] == 1:
				self.lingqiConfig[data["difficulty"]] = data
			elif data["type"] == 2:
				self.linghuanConfig[data["difficulty"]] = data

	def reloadConfig(self):
		self.lingqiConfig.clear()
		self.linghuanConfig.clear()
		self.loadConfig()

	def getLingQiDiffculty(self):
		"""
		获取难度
		"""
		maxNumber = 10000
		# for i in self.lingqiConfig:
		# 	maxNumber += i["probability"]
		number = random.randint(0, maxNumber)
		limitNumber = 0
		for i in self.lingqiConfig.values():
			limitNumber += i["probability"]
			if number <= limitNumber:
				return i["difficulty"]

	def getLingQiAmount(self, difficulty):
		"""
		获取锁的数量
		"""
		if difficulty in self.lingqiConfig:
			return self.lingqiConfig[difficulty]["amount"]
		return 0

	def getLingQiSpeed(self, difficulty):
		"""
		获取鼠标速度
		"""
		if difficulty in self.lingqiConfig:
			return self.lingqiConfig[difficulty]["speed"]
		return 0

	def getLingQiNotice(self, difficulty, time):
		"""
		获取通知
		"""
		if time <= 10:
			return self.lingqiConfig[difficulty]["tensNotice"]
		elif time <= 15:
			return self.lingqiConfig[difficulty]["fifteensNotice"]
		elif time <= 20:
			return self.lingqiConfig[difficulty]["tensNotice"]
		else:
			return self.lingqiConfig[difficulty]["undoneNotice"]

	def getLingHuanDiffculty(self):
		"""
		获取难度
		"""
		maxNumber = 10000
		# for i in self.lingqiConfig:
		# 	maxNumber += i["probability"]
		number = random.randint(0, maxNumber)
		limitNumber = 0
		for i in self.linghuanConfig.values():
			limitNumber += i["probability"]
			if number <= limitNumber:
				return i["difficulty"]

	def getLingHuanAmount(self, difficulty):
		"""
		获取数量
		"""
		if difficulty in self.linghuanConfig:
			return self.linghuanConfig[difficulty]["amount"]
		return 0

	def getLingHuanNotice(self, difficulty, time):
		"""
		获取通知
		"""
		if time <= 10:
			return self.linghuanConfig[difficulty]["tensNotice"]
		elif time <= 15:
			return self.linghuanConfig[difficulty]["fifteensNotice"]
		elif time <= 20:
			return self.linghuanConfig[difficulty]["tensNotice"]
		else:
			return self.linghuanConfig[difficulty]["undoneNotice"]


g_SpaceCopyLLBZNotice = SpaceCopyLLBZNoticeLoader()