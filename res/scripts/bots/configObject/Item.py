# -*- coding: utf-8 -*-

class Item:
	"""
	"""
	def __init__(self):
		self.uid = 0
		self.id = 0
		self.amount = 0
		self.itemOrder = 0
		self.bindType = 0
		
	def init(self, data):
		self.uid = int(data["uid"])
		self.id = int(data["id"])
		self.amount = int(data["amount"])
		self.itemOrder = int(data["itemOrder"])
		self.bindType = int(data["bindType"])
		