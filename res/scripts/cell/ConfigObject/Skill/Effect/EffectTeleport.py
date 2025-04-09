# -*- coding: utf-8 -*-


"""
usage:
	效果

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#engine
import Math
#cell
import Functions
from ConfigObject.Skill.Effect.EffectSkillBase import EffectSkillBase
#common
import KBEDebug
#server_common
import KBEMath
import csdefine
import random

class EffectTeleport( EffectSkillBase ):
	"""
	闪现效果
	"""
	def __init__( self ):
		EffectSkillBase.__init__( self )
		self._positionList = []
		self._direction = (0.0, 0.0, 0.0)
	
	def init( self, dictDat, skill ):
		"""
		virtual method;
		读取技能配置
		@param dictDat: 配置数据 { "Param1":"", "Param2":"", "Param3":"" }
		@type  dictDat: python dict
		"""
		EffectSkillBase.init( self, dictDat, skill )
		if dictDat["Param1"]:
			tempPosList = dictDat["Param1"].split("|")
			for strPos in tempPosList:
				convertPos = Functions.vector3TypeConvert( strPos)
				if convertPos is None:
					KBEDebug.ERROR_MSG("Vector3 Type Error: param1(%s)" % dictDat["Param1"] )
				else:
					convertPos = KBEMath.Unreal2KBEnginePosition( convertPos )
					self._positionList.append( convertPos )
		
		if dictDat["Param2"]:
			self._direction = KBEMath.Unreal2KBEngineDirection( Functions.vector3TypeConvert( dictDat["Param2"] ) )

	def onReceive( self, skill, caster, receiver ):
		"""
		效果开始
		"""
		if len( self._positionList ) == 0:
			KBEDebug.ERROR_MSG("please check param1 ")
			return
			
		if not receiver.stopMovingForType( csdefine.NORMAL_MOVE ):
			return
			
		random.shuffle( self._positionList ) #打乱一次位置
		dstPos = Math.Vector3(self._positionList[0])
		for position in self._positionList:
			#如果有多个坐标，随机到脚下的坐标则重新随机一次
			pos = Math.Vector3(position)
			if pos.flatDistTo(receiver.position) > 0.5:
				dstPos = pos
				break
		
		#客户端位置过滤器同步时机不对，需要改编为之前通知
		receiver.allClients.TeleportToDstPosition(KBEMath.KBEngine2UnrealPosition(dstPos))
		 #更新位置
		receiver.position = dstPos
		if self._direction != (0.0, 0.0, 0.0):
			receiver.changeDirection(self._direction, csdefine.REASON_CHANGE_DIR_FORCE)
		
		

