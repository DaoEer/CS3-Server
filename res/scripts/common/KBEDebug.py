# -*- coding: utf-8 -*-
import sys, csv
import KBEngine
import traceback
import csdefine
import os
import time
import Settings
from pathlib import Path
from SrvDef import LogLevel, EntityTypeDct

# 是否打印调用者的程序信息(Source FileName + LineNo)
printPath = True


def _printErrorInfo():
	print( str( sys.exc_info()[1] ) )

def _getClassName( f, funcName ):
	"""
	取得对应堆栈帧(Frame)的类名字。
	@param 			f : 调用者的堆栈帧(Frame)
	@type 			f : Frame
	@return			  : 对应的类名字
	@rtype			  : string
	"""
	try:
		selfClass = f.f_locals[ 'self' ].__class__					# Note: This only works if self argument is self.
		mro = getattr( selfClass, "__mro__", [] )					# Only new style classes have __mro__ ( inherit object class )
		if mro == []:												# get all grandsire classes
			stack = [selfClass]
			while stack:
				curr = stack.pop( 0 )
				mro.append(curr)									# get all grandsire classes and my self
				stack += curr.__bases__								# base classes
		for bases in mro:
			method = bases.__dict__.get( funcName, None )
			if method is None :										# private method
				prvFunc = "_%s%s" % ( bases.__name__, funcName )	# private method name
				method = bases.__dict__.get( prvFunc, None )		# get private method
			if ( method is not None ) and \
				method.__code__ == f.f_code :						# if find out the method, in class
					return bases.__name__ + "."						# return the class name
	except : pass
	return ""

def _printMessage( args ):
	"""
	按照输出信息。
	@param 			args		: 输出的信息
	@type 			args		: tuple
	@return						: None
	"""
	f = sys._getframe(2)
	if printPath:
		print( f.f_code.co_filename + "(" + str( f.f_lineno ) + ") :" )
	funcName = f.f_code.co_name
	className = _getClassName( f, funcName )
	print( "%s%s: " % ( className, funcName ), end = "" )
	print( *args, sep = "" )

def STREAM_MSG( stream, *args ):
	"""
	输出Hack信息。
	@param 			stream	: 输出的二进制流
	@type 			stream	: String
	@param 			args	: 输出的信息
	@type 			args	: 可变参数列表
	@return					: 无
	@rtype					: None
	"""
	dumpStream = "0x"
	for char in stream:
		hexString = hex( ord( char ) )[2:]
		pad = "0" * ( 2 - len( hexString ) )
		dumpStream = dumpStream + pad + hexString
	sargs = list( args )
	sargs.append( dumpStream )
	_printMessage( sargs )

def TRACE_MSG( *args ):
	"""
	输出Trace信息。
	@param 				args : 输出的信息
	@type 				args : 可变参数列表
	@return					 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_NORMAL)
	_printMessage( args )

def DEBUG_MSG( *args ):
	"""
	输出Debug信息。
	@param 				args : 输出的信息
	@type 				args : 可变参数列表
	@return					 : None
	"""
	if Settings.log_level > LogLevel.DEBUG_LOG: return
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_DBG)
	_printMessage( args )

def INFO_MSG( *args ):
	"""
	输出Info信息。
	@param 				args : 输出的信息
	@type 				args : 可变参数列表
	@return					 : 无
	@rtype					 : None
	"""
	if Settings.log_level > LogLevel.INFO_LOG: return
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_INFO)
	_printMessage( args )

def NOTICE_MSG( *args ):
	"""
	输出Notice信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	_printMessage( args )

def WARNING_MSG( *args ):
	"""
	输出Warning信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	if Settings.log_level > LogLevel.WARNING_LOG: return
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_WAR)
	_printMessage( args )

def ERROR_MSG( *args ):
	"""
	输出Error信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : 无
	@rtype				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	_printMessage( args )
	_printErrorInfo()

def CRITICAL_MSG( *args ):
	"""
	输出Critical信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	_printMessage( args )

def HACK_MSG( *args ):
	"""
	输出Hack信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	_printMessage( args )

def HOOK_MSG( *args ) :
	"""
	输出Hook信息。
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	excStr = "Hook: "
	for i in range( len( args ) ) :
		excStr += "%s, "
	try :
		raise excStr % args
	except:
		sys.excepthook( *sys.exc_info() )

def EXCEHOOK_MSG( *args ) :
	"""
	输出当前栈帧错误信息，常用于输出异常信息
	
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	exceInfo = sys.exc_info()
	if exceInfo is None or exceInfo == ( None, None, None ) :
		ERROR_MSG( "no exception in stack!" )
	else :
		print( "EXCEHOOK_MSG: " )
		for arg in args :
			print( str( arg ) )
		sys.excepthook( *exceInfo )


PRINT_AI_DEBUG_SCRIPTID = []
def DEBUG_MSG_FOR_AI( entity, *args ):
	"""
	输出Debug信息。
	@param 				args : 输出的信息
	@type 				args : 可变参数列表
	@return					 : None
	"""
	if Settings.log_level > LogLevel.DEBUG_LOG: return
	if entity.hasDebugFlag(csdefine.ENTITY_DEBUG_FLAG_FOR_AI) or entity.getScriptID()  in PRINT_AI_DEBUG_SCRIPTID:
		KBEngine.scriptLogType(KBEngine.LOG_TYPE_DBG)
		aiArgs = "AI_DEBUG_MSG:"
		for arg in args:
			aiArgs += arg
		printForAI( aiArgs )



def print_stack():
	"""打印当前堆栈调用信息"""
	frame = sys._getframe().f_back
	print("<Debug> Stack trace:")
	print( "(From file %s, line %s, in %s)" % traceback.extract_stack(frame, 1)[0][:3])
	traceback.print_stack( frame )


def printForAI( args ):
	"""
	输出AI日志
	@param 			args		: 输出的信息
	@type 			args		: tuple
	@return						: None
	"""
	path = Path( os.environ["KBE_ROOT"] ) / "logs/AIDebugInfo.log"
	try:
		f = path.open("a")
		args = "time:"+str(time.ctime())+"  "+str(time.time())+"=====>"+args
		f.write(args+"\n")
	except:
		print("printForAI failed!")
	finally:
		f.close()
		
def DATABASE_LOG_MSG( table, *args ):
	"""
	输出日志数据
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_NORMAL)
	t = getLogTime()
	message = "mysql$"+ str( table ) + "$" + t + "||"
	for i in range( len( args ) ):
		message += "%s||"
	message = message[ : len( message ) - 2 ]
	print( message % args ) 
	
def getLogTime():
	"""
	获取当前的时间，格式为"2017-06-01 12:00:00"
	"""
	return time.strftime("%Y-%m-%d %H:%M:%S")

def OUTPUT_FILE_LOG_MSG( fileUrl, msg ):
	absUrl = Path( os.environ["KBE_ROOT"] ) / fileUrl
	try:
		f = absUrl.open("a")
		writeStr = getLogTime()+" [ "+ KBEngine.component + os.getenv("KBE_COMPONENTID") +" ] : "+msg
		f.write(writeStr+"\n")
	except:
		print("output error!! file:%s, msg:%s"%( fileUrl, msg ))
	finally:
		f.close()

def OUTPUT_PROCESS_INFOS( msg ):
	cid = os.getenv("KBE_COMPONENTID")
	fileUrl = "logs/log_count_" + str(cid) + "_" + time.strftime("%Y-%m-%d") + ".log"
	OUTPUT_FILE_LOG_MSG( fileUrl, msg)
	

def DEBUG_MSG_FOR_SPACECOPY_PLOT( entity, triggerID, *args ):
	"""
	输出Debug信息。
	@param 				args : 输出的信息
	@type 				args : 可变参数列表
	@return					 : None
	"""
	if Settings.log_level > LogLevel.DEBUG_LOG: return
	space = entity if entity.getEntityFlag() == csdefine.ENTITY_FLAG_SPACE else entity.getCurrentSpace()
	key = "SPACE_DEBUG_FLAG_{}".format(space.scriptID)
	flag = KBEngine.cellAppData.get(key, False)
	if space and flag:
		KBEngine.scriptLogType(KBEngine.LOG_TYPE_DBG)
		entity = KBEngine.entities.get(triggerID, None)
		entityFlag = 0 if entity is None else entity.getEntityFlag()
		spaceArgs = "(space:{}, spaceID:{}, triggerEntity:{}, id:{})".format(space.scriptID, space.spaceID, EntityTypeDct.get(entityFlag, "无"), triggerID)
		for arg in args: spaceArgs += arg
		printForSpaceCopyPlot( spaceArgs )

def printForSpaceCopyPlot( args ):
	"""
	输出副本/位面剧情日记
	@param 			args		: 输出的信息
	@type 			args		: tuple
	@return						: None
	"""
	path = Path( os.environ["KBE_ROOT"] ) / "logs/SpaceCopyPlotDebugInfo.log"
	try:
		f = path.open("a")
		args = "time:"+str(time.ctime())+"=====>"+args
		f.write(args+"\n")
	except:
		print("printForSpaceCopyPlot failed!")
	finally:
		f.close()

def DEBUG_MSG_FOR_REWARD(*args):
	#rewardArgs = "" if entity == None else "PlayerID:{} ".format(entity.id)
	rewardArgs = ""
	for arg in args:
		rewardArgs += arg
	writeRewardInfosToLogFile(rewardArgs)

def writeRewardInfosToLogFile(args):
	"""
	输出奖励日志
	@param 			args		: 输出的信息
	@type 			args		: tuple
	@return						: None
	"""
	path = Path(os.environ["KBE_ROOT"]) / "logs/RewardDebugInfo.log"
	try:
		f = path.open("a")
		args = "time:" + str(time.ctime()) + "=====>" + args
		f.write(args + "\n")
	except:
		print("writeRewardInfosToLogFile failed!")
	finally:
		f.close()


def DEBUG_BOT_MSG( msg ):
	cid = os.getenv("KBE_COMPONENTID")
	fileUrl = "/logs/log_count_" + str(cid) + "_" + time.strftime("%Y-%m-%d") + ".log"
	
	absUrl = os.environ["KBE_ROOT"]+fileUrl
	try:
		f = open(absUrl,"a")
		writeStr = getLogTime()+" [ "+ KBEngine.component + os.getenv("KBE_COMPONENTID") +" ] : "+msg
		f.write(writeStr+"\n")
	except:
		print("output error!! file:%s, msg:%s"%( fileUrl, msg ))
	finally:
		f.close()
	
def DEBUG_TO_CSV( msg_lists ):
	cid = os.getenv("KBE_COMPONENTID")
	fileUrl = "logs/" + str(cid) + ".csv"
	absUrl = Path( os.environ["KBE_ROOT"] ) / fileUrl
	
	try:
		f = absUrl.open("a", encoding='utf-8', newline='')
		csv_writer = csv.writer(f)
		for msg_list in msg_lists: csv_writer.writerow(msg_list)
	except:
		print("output error!! file:%s, msg:%s"%( fileUrl, msg_lists ))
	finally:
		f.close()
	