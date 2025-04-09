# -*- coding: utf-8 -*-
import hashlib, time, sys, functools, itertools, logging
from tornado.ioloop import IOLoop, PollIOLoop, _Timeout
from tornado import stack_context

import KBEngine
from KBEDebug import *
from KBESelect import KBESelect

CALL_BACK = 0
TIMEOUT_CALL_BACK = 1

class KBEIOLoop(IOLoop):
	"""
	1、write by phw.
	这是一个使用KBEngine的timer来loop的版本，用于tornado的AsyncHTTPClient访问远程服务器。
	已知的未实现的方法：
		def set_blocking_signal_threshold(self, seconds, action)
		def add_callback_from_signal(self, callback, *args, **kwargs):
	上述方法暂时用不上，所以不考虑实现，如果将来真有需要的时候再考虑。
	
	2、modify by QRN
	这个版本主要是在狼人版本的基础上改动而来，因原来的版本是用在interface中
	interface借助的是KBEngine.addTimer来实现的IO Loop
	放在base这边的话，只能借助entity的timer机制来进行相关的操作
	"""
	def initialize(self, time_func=None, **kwargs):
		super(KBEIOLoop, self).initialize(**kwargs)
		
		self._impl = KBESelect( self )
		self.time_func = time_func or time.time
		self._callbacks = []
		self._handlers = {}
		self._timeouts = {}
		self._running = False
		self._timeout_counter = itertools.count()

	def add_handler(self, fd, handler, events):
		fd, obj = self.split_fd(fd)
		self._handlers[fd] = (obj, stack_context.wrap(handler))
		self._impl.register(fd, events | self.ERROR)

	def update_handler(self, fd, events):
		fd, obj = self.split_fd(fd)
		self._impl.modify(fd, events | self.ERROR)

	def remove_handler(self, fd):
		fd, obj = self.split_fd(fd)
		self._handlers.pop(fd, None)
		try:
			self._impl.unregister(fd)
		except Exception:
			gen_log.debug("Error deleting fd from IOLoop", exc_info=True)

	def time(self):
		return self.time_func()

	def start(self):
		"""
		以下大部份代码来自PollIOLoop.start()，
		只是为了适应kbe引擎，把其拆解成了两部分
		"""
		if self._running:
			raise RuntimeError("IOLoop is already running")
		self._setup_logging()
		IOLoop._current.instance = self
		self._running = True

	def stop(self):
		self._running = False
		
		# 清理timer
		for timeout in self._timeouts.values():
			self.parentEntity.delTimer( timeout.kbe_timer_id )
			timeout.callback = None
			timeout.kbe_io_loop = None
			timeout.kbe_timer_id = 0
		self._timeouts.clear()
		# stop时需要对logging进行清理，否则服务器会crash，原因未知。
		logging.shutdown()
		logging.getLogger().handlers.clear()

	def add_callback(self, callback, *args, **kwargs):
		if not self._running:
			raise RuntimeError("IOLoop is closing")
		list_empty = not self._callbacks
		self._callbacks.append(functools.partial(
			stack_context.wrap(callback), *args, **kwargs))
		if list_empty:
			# 使用timer来模拟下一次的IO循环
			self.parentEntity.addTimer( 0.01, 0.0, CALL_BACK )
			
	def call_at(self, deadline, callback, *args, **kwargs):
		timeout = KBE_Timeout(
			deadline,
			functools.partial(stack_context.wrap(callback), *args, **kwargs),
			self)
		
		timeout.kbe_io_loop = self
		timeout.kbe_timer_id = self.parentEntity.addTimer( deadline - self.time(), 0.0, TIMEOUT_CALL_BACK )
		self._timeouts[timeout.kbe_timer_id] = timeout # 记录起来以在释放的时候清理
		return timeout

	def remove_timeout(self, timeout):
		self._timeouts.pop( timeout.kbe_timer_id, None )
		timeout.callback = None
		timeout.kbe_io_loop = None
		self.parentEntity.delTimer( timeout.kbe_timer_id )
		timeout.kbe_timer_id = 0

	def kbe_onCallback( self, timerID ):
		"""
		"""
		callbacks = self._callbacks
		self._callbacks = []
		
		for callback in callbacks:
			self._run_callback(callback)

	def kbe_process_event( self, fd, eventType ):
		"""
		"""
		try:
			fd_obj, handler_func = self._handlers[fd]
			handler_func(fd_obj, eventType)
		except (OSError, IOError) as e:
			if errno_from_exception(e) == errno.EPIPE:
				# Happens when the client closes the connection
				pass
			else:
				self.handle_callback_exception(self._handlers.get(fd))
		except Exception:
			self.handle_callback_exception(self._handlers.get(fd))

	def kbe_onRecv( self, fd ):
		"""
		"""
		self.kbe_process_event( fd, IOLoop.READ )

	def kbe_onWrite( self, fd ):
		"""
		"""
		self.kbe_process_event( fd, IOLoop.WRITE )

	def onTimer(self, timerHandle, userData):
		"""
		"""
		if userData == CALL_BACK:
			self.kbe_onCallback(timerHandle)
		elif userData == TIMEOUT_CALL_BACK:
			if timerHandle in self._timeouts:
				self._timeouts[timerHandle].kbe_on_callback(timerHandle)
		else:
			KBEDebug.ERROR_MSG("KBEIOLoop error, error timerHandle[%d], userData[%s]" %(timerHandle, userData))


class KBE_Timeout( _Timeout ):
	"""
	"""
	__slots__ = ['kbe_timer_id', "kbe_io_loop"]
	
	def kbe_on_callback( self, timerID ):
		"""
		"""
		callback = self.callback
		io_loop = self.kbe_io_loop
		self.callback = None
		self.kbe_io_loop = None
		self.kbe_timer_id = 0
		io_loop.parentEntity.delTimer( timerID )
		
		io_loop._run_callback(callback)

