# -*- coding: utf-8 -*-

from SpaceCopyCangGongDian import SpaceCopyCangGongDian
import KBEngine
import Functions
import csdefine
from AnswerConfig.CangShuGeAnswer import Datas as answerDatas1

class SpaceCopyCangGongDian1( SpaceCopyCangGongDian ):
	"""
	藏功殿（魔道）
	"""
	def __init__( self ):
		SpaceCopyCangGongDian.__init__( self )

	def getAnswerDatas( self, questionID ):
		"""
		获取答案字典
		"""
		answerDict = {}
		if answerDatas1.get(questionID).get( "answer" ):
			answerData = answerDatas1.get(questionID).get("answer").split("|")
			for data in answerData:
				answer = data.split(":")
				answerDict[answer[0]] = answer[1]

		return answerDict

	def getAnswerCfg( self, questionID ):
		"""
		获取答案
		"""
		answerList = []
		if answerDatas1.get(questionID).get( "answer" ):
			answerBuff = answerDatas1.get(questionID).get("answer").split("|")
			for data in answerBuff:
				answer = data.split(":")
				answerList.append(answer[1])
		return answerList

	def getDescriptionCfg( self, questionID ):
		"""
		获取问题描述的语音ID
		"""
		return answerDatas1.get( questionID ).get( "questionDes", "" )
