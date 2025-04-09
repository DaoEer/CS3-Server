# -*- coding: utf-8 -*-
#
#
# 陷阱持有行为

import csdefine
import KBEMath
import Math

class TrapHoldActionBase:
	"""
	陷阱触发持有效果基础类
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def onBegin( selfEntity, targetEntity, args ):
		"""
		"""
		pass
		
	@staticmethod
	def onEnd( selfEntity, targetEntity, args ):
		"""
		"""
		pass
		
class TrapHoldActionUncontrollable( TrapHoldActionBase ):
	"""
	持有行为：霸体
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def onBegin( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.effectStateInc( csdefine.EFFECT_STATE_UNCONTROLLABLE )
		
	@staticmethod
	def onEnd( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.effectStateDec( csdefine.EFFECT_STATE_UNCONTROLLABLE )
		
class TrapHoldActionInvincible( TrapHoldActionBase ):
	"""
	持有行为：无敌
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def onBegin( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.effectStateInc( csdefine.EFFECT_STATE_INVINCIBLE )
		
	@staticmethod
	def onEnd( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.effectStateDec( csdefine.EFFECT_STATE_INVINCIBLE )

class TrapHoldActionSuck( TrapHoldActionBase ):
	"""
	持有行为：吸力
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def onBegin( selfEntity, targetEntity, args ):
		"""
		"""
		if not targetEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return
		suckSpeed = float( args[0] )
		suckPosition = Math.Vector3( KBEMath.KBEngine2UnrealPosition( selfEntity.position ) )
		targetEntity.client.OnBeginTrapSuck( suckPosition, suckSpeed )

	@staticmethod
	def onEnd( selfEntity, targetEntity, args ):
		"""
		"""
		if not targetEntity.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			return
		targetEntity.client.OnEndTrapSuck()

class TrapHoldActionBuff( TrapHoldActionBase ):
	"""
	持有行为：Buff...
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def onBegin( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.addBuff( selfEntity,int( args[0] ) )

	@staticmethod
	def onEnd( selfEntity, targetEntity, args ):
		"""
		"""
		targetEntity.removeBuffByID( int( args[0] ) )
