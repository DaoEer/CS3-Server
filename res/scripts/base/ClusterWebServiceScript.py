# -*- coding: utf-8 -*-
"""
ClusterWebServiceScript 模块是提供给webservice向游戏服务器（baseapp）发送消息的中间接口，
WebService通过.sh文件执行ClusterWebServiceScript.py 脚本，然后调用ClusterWebServiceScript
的某个方法，最终通过TelnetConsole使用Telnet的方式向游戏服务器（baseapp）发送指令，本模块
相当于是一个Telnet的客户端

.sh文件格式： python (配置路径) + “res/scripts/base/ClusterWebServiceScript.py” 函数名 要传给baseapp的参数列表（多个参数以空格隔开）
例如充值：
	python D:/CS3-Sever/res/base/ClusterWebServiceScript.py charge_script acountName
"""

import time
import sys
import time
import os
import telnetlib


def initRootPath():
	"""
	初始化root目录，以加载其它的脚本
	"""
	appdir = os.path.dirname( os.path.abspath( __file__ ) )
	parentDir = os.path.dirname( appdir )
	parentDir = os.path.dirname( parentDir )
	parentDir = os.path.dirname( parentDir )
	if parentDir not in sys.path:
		sys.path.append(parentDir + r"/kbe/tools/server")

initRootPath()
from pycommon import Define
from pycommon import Cluster_WebService_Define
from pycommon.Machines import Machines

def _pre_process_cmd(cmd):
	cmd = cmd.encode("utf-8")
	if cmd.endswith( b"\r\n" ):
		return cmd
	elif cmd[-1] == b"\r":
		cmd += b"\n"
	elif cmd[-1] == b"\n":
		cmd = cmd[:-1] + b"\r\n"
	else:
		cmd += b"\r\n"
	return cmd


class TelnetConsole(object):
	def __init__( self, host_ip, host_port ):
		"""
		"""
		self.host_ip = host_ip
		self.host_port = host_port
		self.consoleInst = None

	def close( self ):
		"""
		"""
		if self.consoleInst:
			self.consoleInst.close()
		self.consoleInst = None
		self.host_ip = ""
		self.host_port = 0

	def run(self, cmdList):
		"""
		"""
		try:
			self.consoleInst = telnetlib.Telnet(self.host_ip, self.host_port)
		except Exception as err:
			print("TelnetConsole.run: 服务器连接失败！, error: %s\n" % err)
			self.close()
			return
		tempCmdList = cmdList[:]
		self.consoleInst.read_until(b'password:')
		self.consoleInst.write(b'kbe\r\n')
		self.consoleInst.read_until(b'>>>')
		for cmd in tempCmdList:
			self.consoleInst.write(_pre_process_cmd(cmd))
			self.consoleInst.read_until(b'>>>')
		time.sleep(2)
		self.close()


class WebServiceRunScript(object):
	"""
	"""
	def __init__(self, ip, host_port):
		self.host_ip = ip
		self.host_port = host_port
		self.telnet_client = TelnetConsole(self.host_ip, self.host_port)
		
	def charge_script(self, *args, **kwargs):
		"""
		充值
		"""
		if len(args) == 0:
			print("error: method charge_script arguments error")
			return
		accountName = args[0]
		cmdList = ["import KST", "KST.g_baseAppEntity.pickUpChargeOrder('%s')" % accountName]
		if self.telnet_client:
			self.telnet_client.run(cmdList)


class ClusterWebServiceHandler(Machines):
	def __init__(self, uid, types):
		Machines.__init__(self, uid)
		
	def getComponentHost(self, componentType = Define.BASEAPP_TYPE):
		self.interfaces_groups = {}
		self.queryAllInterfaces(Cluster_WebService_Define.MACHINES_ADDRESS, Cluster_WebService_Define.MACHINES_QUERY_ATTEMPT_COUNT, 
			Cluster_WebService_Define.MACHINES_QUERY_WAIT_TIME)
		
		host_ip = ""
		host_port = 0
		for mID, comps in self.interfaces_groups.items():
			for comp in comps:
				#print( comp.intaddr, comp.consolePort, comp.fullname, comp.intaddr, comp.consolePort)
				if comp.componentType == componentType:
					host_ip = comp.intaddr
					host_port = comp.consolePort
					break
		if not host_ip or not host_port:
			print("error: can't find component of the componentType: %s" % componentType)
			
		return (host_ip, host_port)
		
	def do(self, func, *args):
		host_ip, host_port = self.getComponentHost()
		if host_ip and host_port:
			runScriptInst = WebServiceRunScript(host_ip, host_port)
			try:
				getattr(runScriptInst, func)(*args)
			except Exception as err:
				print("ClusterWebServiceHandler do error of %s, error: %s" % (func, err))
		


if __name__ == "__main__":
	if len(sys.argv)  >= 2:
		runscript = sys.argv[1]
		argv = sys.argv[2:]
		uid = -1
		if uid < 0:
			uid = Define.getDefaultUID()
		templatestr = ""
		clusterHandler = ClusterWebServiceHandler(uid, templatestr)
		clusterHandler.do(runscript, *argv)
	else:
		print("runscript error: arguments less")
