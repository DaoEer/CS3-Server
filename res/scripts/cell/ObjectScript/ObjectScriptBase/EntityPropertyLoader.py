#coding:utf-8

# $Id: EntityPropertyLoader.py

import csdefine
import sys

class EntityPropertyLoader:
	def __init__( self ):
		self.entityCreateDict = {}

	def initData( self, configData ):
		if 'scriptID' in configData:
			self.setEntityProperty("scriptID",configData["scriptID"])

		if 'EntityScript' in configData:
			self.setEntityProperty( "entityScript", configData["EntityScript"])

		if 'ModelNumber' in configData:
			self.setEntityProperty("modelNumber",configData["ModelNumber"])

		if 'ModelScale' in configData:
			self.setEntityProperty("modelScale",float(configData["ModelScale"]))

		if 'Flags' in configData:
			flag = 0
			groupFlags = configData["Flags"]
			if type(groupFlags) == list:
				for v in groupFlags:
					flag |= 1 << v

				flag &= 0x7FFFFFFFFFFFFFFE
			else:
				flag = groupFlags
			self.setEntityProperty("flags", flag)

	def setEntityProperty( self , name, value ):
		"""
		设置entity的初始化属性
		@param name: 属性名称，该名称必须存在于相应的Entity类型的.def文件中
		@type  name: STRING
		@param value: 与name对应的值，类型为与相应的.def中定义的name的取值类型
		"""
		self.entityCreateDict[name] = value

	def getEntityProperty( self , name, defaultValue = None ):
		if name in self.entityCreateDict:
			return self.entityCreateDict[name]
		else:
			return defaultValue

	def getEntityProperties( self, argDict = {} ):
		tempDict = {}
		tempDict.update( self.entityCreateDict )
		tempDict.update( argDict )
		return tempDict
		
	def hasScriptFlag( self, flag ):
		"""是否配置了标记位"""
		return 1 << flag & self.getEntityProperty("flags")