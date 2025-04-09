# -*- coding: utf-8 -*-
import weakref

import KBEDebug
import KBEngine

import csdefine
import CoreObject.VehiclePetObject as VehiclePetObject

class VehiclePet( VehiclePetObject.VehiclePetObject ):
	def __init__( self ):
		VehiclePetObject.VehiclePetObject.__init__( self )
		self.baseOwner = None
		self.withdrawReason = csdefine.PET_WITHDRAW_COMMON
		self.uid = self.cellData["uid"]
		self.creatingCell = False
		self.waitDestroyTimerID = 0

	def initialization( self, owner ):
		"""
		"""
		self.baseOwner = weakref.proxy( owner )
		self.cellData["baseOwner"] = owner
		self.cellData["baseOwnerID"] = owner.id
		self.cellData["isDestroySelf"] = False
		self.cellData["chaseEntityID"] = 0
		self.cellData["chaseTimerID"] = 0
		self.cellData["movingType"] = 0
		
		self.cellData["AICurrentState"] = 1
		self.cellData["AIAttackTargetID"] = 0
		self.cellData["AITickCBID"] = 0
		
		self.creatingCell = True
		self.waitRepeatNum = 0
		self.createCellEntity( owner.cell )
		
	def statusMessage(self, statusMessageType, *statusMessageArg):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 元组
		"""
		if self.baseOwner:
			self.baseOwner.statusMessage(statusMessageType, statusMessageArg)
		
	def withdraw( self, reason ):
		"""
		回收幻兽
		"""
		self.withdrawReason = reason
		if self.cell :													# 如果有 cell entity
			self.cell.destroyCellByBase()								# 则，删除 cell entity
		else:
			if  self.withdrawReason == csdefine.PET_WITHDRAW_MOUNT_PET:		# 骑上坐骑，幻兽的Base部分不销毁
				if self.baseOwner:
					self.baseOwner.onMountPet( self.uid, self._getWriteToDBDatas() )
				self.withdrawReason = csdefine.PET_WITHDRAW_COMMON
				return
				
			if self.withdrawReason != csdefine.PET_WITHDRAW_OFFLINE:
				if self.baseOwner:
					self.baseOwner.onWithdrawPet( self.uid, self.withdrawReason, self._getWriteToDBDatas() )
			
			self.baseOwner = None
			if self.creatingCell:
				if self.waitDestroyTimerID == 0:
					#延时进行销毁的操作
					self.waitDestroyTimerID = self.addTimerRepeat(1, "onDelayDestroy", ())
			else:
				self.destroy()
			
	def _getWriteToDBDatas( self ):
		"""
		回收幻兽 获取保存数据
		"""
		datas = {}
		if self.withdrawReason == csdefine.PET_WITHDRAW_DEATH:
			datas["HP"] = self.cellData["HP_Max"]
			datas["MP"] = self.cellData["MP_Max"]
		else:
			datas["HP"] = self.cellData["HP"]
			datas["MP"] = self.cellData["MP"]
		datas["exp"] = self.cellData["exp"]
		return datas
	# ----------------------------------------------------------------
	# callbacks of engine
	# ----------------------------------------------------------------
	def onGetCell( self ) :
		"""
		when my cell is created it will be called
		"""
		self.creatingCell = False
		VehiclePetObject.VehiclePetObject.onGetCell( self )
		
	def onCreateCellFailure( self ):
		"""
		cell创建失败
		"""
		self.creatingCell = False
		
	def onLoseCell( self ) :
		"""
		when my cell is lost, it will be called
		"""
		if self.withdrawReason == csdefine.PET_WITHDRAW_MOUNT_PET:						# 骑上坐骑，幻兽的Base部分不销毁
			if self.baseOwner:
				self.baseOwner.onMountPet( self.uid, self._getWriteToDBDatas() )
			self.withdrawReason = csdefine.PET_WITHDRAW_COMMON
			return
		if self.withdrawReason != csdefine.PET_WITHDRAW_OFFLINE:
			if self.baseOwner:
				self.baseOwner.onWithdrawPet( self.uid, self.withdrawReason, self._getWriteToDBDatas() )
		self.destroy()
		
	def doDestroyClean( self ):
		"""
		做销毁前的清理
		"""
		super().doDestroyClean()
		#之所以在这里清理，是因为实际测试中发现幻兽销毁时，可能幻兽的cell并没创建出来
		#cellData中记录的对象会造成交叉引用导致内存泄漏
		self.cellData["baseOwner"] = None
		
	def onDelayDestroy( self ):
		"""
		"""
		if not self.creatingCell:
			self.popTimer(self.waitDestroyTimerID)
			self.waitDestroyTimerID = 0
			
			if self.cell:
				self.cell.destroyCellByBase()
			else:
				self.destroy()
			return
		
		self.waitRepeatNum += 1
		if self.waitRepeatNum < 5:
			return
			
		KBEDebug.ERROR_MSG("VehiclePet[%d]:onDelayDestroy, wait times over 5s" %(self.id))
		
			