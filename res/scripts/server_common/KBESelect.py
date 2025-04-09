# -*- coding: utf-8 -*-

import KBEngine

from tornado.ioloop import IOLoop


class KBESelect(object):
	"""
	使用KBE的KBEngine.registerFileDescriptor()和KBEngine.registerWriteFileDescriptor()
	来代替事件的触发
	"""
	def __init__(self, kbeLoop):
		self.read_fds = set()
		self.write_fds = set()
		self.error_fds = set()
		
		self.kbeLoop = kbeLoop

	def close(self):
		pass

	def register(self, fd, events):
		if fd in self.read_fds or fd in self.write_fds or fd in self.error_fds:
			raise IOError("fd %s already registered" % fd)
		if events & IOLoop.READ:
			self.read_fds.add(fd)
			KBEngine.registerReadFileDescriptor(fd, self.onRecv)
		if events & IOLoop.WRITE:
			self.write_fds.add(fd)
			KBEngine.registerWriteFileDescriptor(fd, self.onWrite)
		if events & IOLoop.ERROR:
			# @TODO(phw): KBEngine未支持
			pass

	def modify(self, fd, events):
		self.unregister(fd)
		self.register(fd, events)

	def unregister(self, fd):
		if fd in self.read_fds:
			self.read_fds.discard(fd)
			KBEngine.deregisterReadFileDescriptor(fd)
			
		if fd in self.write_fds:
			self.write_fds.discard(fd)
			KBEngine.deregisterWriteFileDescriptor(fd)
			
		self.error_fds.discard(fd)

	def poll(self, timeout):
		# 我们会使用回调的方式触发，所以不会处理poll的请求
		return ()

	def onWrite(self, fd):
		self.kbeLoop.kbe_onWrite( fd )
		
	def onRecv(self, fd):
		self.kbeLoop.kbe_onRecv( fd )

