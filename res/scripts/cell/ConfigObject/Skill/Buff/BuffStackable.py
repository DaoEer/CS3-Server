# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import csdefine
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffLoop import BuffLoop


class BuffStackable( BuffLoop ):
	"""
	可叠加的持有buff
	通过重复添加持续效果实现效果的增强，因此要求buff配置的持续效果必须是可叠加的（递增、递减entity某属性）
	如不能通过持续效果实现叠加，可新增继承此脚本的buff脚本（buff脚本读取layer来计算数值）
	"""
	def __init__( self ):
		BuffLoop.__init__( self )
		self.maxStackLayer = 1	#最大叠加层数
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffLoop.init( self, dictDat )
		if dictDat["Param1"]:
			self.maxStackLayer = int(dictDat["Param1"])
	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		重载掉此方法，叠加buff只增加层数，而不另外加buff
		"""
		for buffData in receiver.getAttrBuffs().values():
			if buffData.buffID == self.getID():				#只叠加第一个找到的buff，理论上也只会有一个
				receiver.attrBuffs[buffData.index].casterID = caster.id
				if buffData.layer < self.maxStackLayer:		#大于叠加上限则不继续叠加，只重置持续时间
					receiver.stackBuff( buffData.index )
				receiver.resetBuffEndTime( buffData.index )
				return True
		
		return BuffLoop.receiveSuccess( self, caster, receiver )
	
	def doStack( self, receiver, buffData ):
		"""
		叠加
		"""
		#再加一遍持有效果
		caster = KBEngine.entities.get( buffData.casterID, None )
		for index, effect in enumerate( self._holdEffectList ):
			if effect.canEffect( caster, receiver ):
				effectData = effect.getNewEffectData( caster, receiver )
				effectData.index = receiver.getNewHoldEffectIndex()
				effectData.sourceType = csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF
				effectData.sourceID = self.getID()
				effectData.configIndex = index
				effectData.casterID = caster.id if caster != None else 0
				effectData.buffIndex = buffData.index
				effectData.setTempData( "isReloadBuff", False )		#记录是不是重载buff引起的加载持有效果，某些持有效果需要此信息
				
				receiver.addHoldEffectData( effectData )
				effect.onBegin( effectData, receiver )
		
		buffData.layer += 1
		receiver.allClients.OnBuffLayerChange( buffData.index, buffData.layer )
	
	def addHoldEffect( self, receiver, buffData, isReloadBuff = False ):
		"""
		virtual method
		加载持有效果
		"""
		caster = KBEngine.entities.get( buffData.casterID, None )
		for index, effect in enumerate( self._holdEffectList ):
			if isReloadBuff or effect.canEffect( caster, receiver ):	#上线加载时不检测条件
				for i in range( buffData.layer ):	#有多少层加多少遍
					effectData = effect.getNewEffectData( caster, receiver )
					effectData.index = receiver.getNewHoldEffectIndex()
					effectData.sourceType = csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF
					effectData.sourceID = self.getID()
					effectData.configIndex = index
					effectData.casterID = caster.id if caster != None else 0
					effectData.buffIndex = buffData.index
					effectData.setTempData( "isReloadBuff", isReloadBuff )		#记录是不是重载buff引起的加载持有效果，某些持有效果需要此信息
					
					receiver.addHoldEffectData( effectData )
					effect.onBegin( effectData, receiver )
	
	def removeHoldEffect( self, receiver, buffData ):
		"""
		virtual method
		移除持有效果
		"""
		for index, effect in enumerate( self._holdEffectList ):
			tempList = []
			for effectData in receiver.holdEffectData:
				if effectData.sourceType == csdefine.HOLD_EFFECT_SOURCE_TYPE_BUFF and effectData.configIndex == index and effectData.buffIndex == buffData.index:
					tempList.append( effectData )
			
			if tempList:
				tempList.reverse()	#倒序，高层的持续效果先移除
				for effectData in tempList:
					effect.onEnd( effectData, receiver )
					receiver.removeHoldEffectData( effectData.index )