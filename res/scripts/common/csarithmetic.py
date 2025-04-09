# -*- coding: utf-8 -*-
import math
import Math
import random
import KBEDebug

def getYawByVector3( vec3 ):
	"""
	从Vector3中获取yaw值
	"""
	return math.atan2(vec3.x,vec3.z)

def getPitchByVector3( vec3 ):
	"""
	从Vector3中获取pitch值
	"""
	return math.atan2(vec3.y, math.sqrt(vec3.z * vec3.z + vec3.x * vec3.x))

def isInRectangle( dstPos, srcPos, yaw, width, height ):
	"""
	目标点 dstPos 是否在以 srcPos 为起点，yaw为方向,宽 width 高 height 的矩形中。
	"""
	if tuple(dstPos) == tuple(srcPos):
		return True
	transmitDir = Math.Vector3()
	transmitDir.x = math.sin( yaw )
	transmitDir.z = math.cos( yaw )
	desDir = dstPos - srcPos
	desDir.normalise()
	an = transmitDir.dot( desDir )
	if an < -1:
		an = -1

	if an == 0:	 # 刚好与施法者在同一个位置
		an = 1

	if an > 1:
		an = 1
	diffYaw = math.acos( an )
	dist = srcPos.distTo( dstPos )
	if abs( diffYaw ) <= math.pi / 2 and abs( dist * math.sin( diffYaw ) ) <= width / 2.0 and abs( dist * math.cos( diffYaw ) ) <= height:
		return True
	return False


def isInRectangleExt( dstPos, srcPos, yaw, width, length ):
	"""
	目标点 dstPos 是否在以 srcPos 为中心，yaw为方向（宽的方向）,宽 width 长 length 的矩形中。
	以坐标原点为中心，将点逆时针旋转yaw，使矩形平行于坐标轴，yaw为0 朝向的是客户端的x轴正方向，服务器的z轴正方向
	向量的变换公式为：
	x = cost*x+sint*y
	y = -sint*x+cost*y
	将坐标替换后可以得到新的srcPosNew = (cost*srcPos.x+sint*srcPos.z, srcPos.y, -sint*srcPos.x+cost*srcPos.z)
	可以简单得到变换后的矩形的四个顶点 从左上角开始为第一个 顺时针依次为1,2,3,4，坐标依次为：
	(cost*srcPos.x+sint*srcPos.z-length/2, srcPos.y, -sint*srcPos.x+cost*srcPos.z+width/2)
	(cost*srcPos.x+sint*srcPos.z+length/2, srcPos.y, -sint*srcPos.x+cost*srcPos.z+width/2)
	(cost*srcPos.x+sint*srcPos.z+length/2, srcPos.y, -sint*srcPos.x+cost*srcPos.z-width/2)
	(cost*srcPos.x+sint*srcPos.z-length/2, srcPos.y, -sint*srcPos.x+cost*srcPos.z-width/2)
	新的dstPosNew = (cost*dstPos.x+sint*dstPos.z, dstPos.y, -sint*dstPos.x+cost*dstPos.z)
	判断新的dstPos是否在新的矩形内就非常简单了 只需要判断一下大小关系 因为平行于坐标轴
	"""
	cost = math.cos(yaw)
	sint = math.sin(yaw)

	dx, dz = cost*dstPos.x+sint*dstPos.z, -sint*dstPos.x+cost*dstPos.z
	sx1, sx3 = cost*srcPos.x+sint*srcPos.z-length/2, cost*srcPos.x+sint*srcPos.z+length/2
	sz1, sz3 = -sint*srcPos.x+cost*srcPos.z+width/2, -sint*srcPos.x+cost*srcPos.z-width/2

	if dx<sx1 or dx>sx3 or dz>sz1 or dz<sz3:
		return False
	return True


def isInSector( dstPos, srcPos, yaw, radius, angle ):
	"""
	目标点 dstPos 是否在以 srcPos 为圆心，radius 为半径，角度为 angle(角度(0,360]) ，朝向为 yaw 的扇形中。
	"""
	if tuple(dstPos) == tuple(srcPos):
		return True
	dist = srcPos.distTo( dstPos )
	if dist > radius:
		return False

	halfAngle = angle / 180.0 * math.pi		#转化为弧度
	transmitDir = Math.Vector3()
	transmitDir.x = math.sin( yaw )
	transmitDir.z = math.cos( yaw )
	desDir = dstPos - srcPos
	desDir.normalise()

	an = transmitDir.dot( desDir )
	if an < -1:
		an = -1

	if an == 0:	 # 刚好与施法者在同一个位置
		an = 1

	if an > 1:
		an = 1

	angle = math.acos( an )
	if angle <= halfAngle / 2:	# 小于或等于夹角
		return True
	return False

def getPositionByLink(pos, radius):
	"""
	获取环上随机弧度位置   pos 为圆心,radius 为半径
	"""
	radian = random.uniform( 0, 2*math.pi )
	return Math.Vector3( pos.x + radius*math.sin(radian), pos.y, pos.z + radius*math.cos(radian) )

def getPositionByCircular(pos, radius):
	"""
	随机获取圆内的位置   pos 为圆心,radius 为半径
	"""
	radian = random.uniform( 0, radius )
	theta = random.uniform(0,2*math.pi)
	return Math.Vector3( pos + Math.Vector3( math.sin(theta)*radian, 0, math.cos(theta)*radian ))

def getPositionByByLinks(pos, minRadius, maxRadius):
	"""
	随机获取环内的位置, pos 为圆心,minRadius 为内径，maxRadius 为外径
	"""
	radian = random.uniform( minRadius, maxRadius )
	theta = random.uniform(0,2*math.pi)
	return Math.Vector3( pos + Math.Vector3( math.sin(theta)*radian, 0, math.cos(theta)*radian ))

def getPositionBySphere(pos, radius):
	"""
	随机获取球内的位置   pos 为球心,radius 为半径
	"""
	radian = random.uniform( 0, radius )
	theta = random.uniform(0,2*math.pi)
	height = radius * math.sin( math.acos( radian/radius ) )
	rheight = random.uniform( -height, height )
	rPos = Math.Vector3( pos + Math.Vector3( math.sin(theta)*radian, 0, math.cos(theta)*radian ))
	rPos.y += rheight
	return rPos