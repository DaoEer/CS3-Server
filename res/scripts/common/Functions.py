import KBEngine
import KBEDebug
import json
import random
import time
import csconst
import Math
import Vector
import math
import re

PI = 3.1415926535897932

def JsonEncodeBytes(obj):
	if isinstance(obj, bytes):
		return obj.decode('ascii')  
	raise TypeError(repr(obj) + " is not JSON serializable")

def toJsonString(param):
	"""
	目前仅支持字典，列表中嵌套字典（不支持一般列表如[1,2,4]）
	"""
	return json.dumps({"ROOT":param}, default=JsonEncodeBytes)

# --------------------------------------------------------------------
class Functor:
	"""
	构造任意参数的Callback函数类。
		@ivar _fn:			Callback函数
		@type _fn:			function
		@ivar _args:		参数
		@type _args:		tuple
	"""

	def __init__( self, fn, *args ):
		"""
		构造函数。
			@param fn:			Callback函数
			@type fn:			function
			@param args:		参数
			@type args:			tuple
		"""
		self._fn = fn
		self._args = list( args ) if args else []

	def __call__( self, *args ):
		"""
		调用Callback函数fn。
			@param args:		参数
			@type args:			tuple
			@return:			Callback函数的返回值
		"""
		self._args.extend(args)
		return self._fn( *self._args )


def split1(srcstr):
	"""
	解析："20121543|20123678"
	返回值：['20121543', '20123678']
	"""
	return srcstr.split("|")

def split2(srcstr):
	"""
	解析："[20121543,201215436]|[20123678,20123679]"
	返回值：[[20121543, 201215436], [20123678, 20123679]]
	"""
	return [eval(item) for item in srcstr.split("|")]

def split3(srcstr):
	"""
	解析："1:20121543|2:20123678"
	返回值：{1:20121543|2:20123678}
	"""
	templist = [eval("{"+item+"}") for item in srcstr.split("|")]
	result = {}
	for item in templist:
		result.update(item)
	return result

def split4(srcstr):
	"""
	解析："1:[20121543,201215436]|2:[20123678,20123679]"
	返回值：{1:20121543|2:20123678}
	"""
	return split3(srcstr)


#--------------实现在遍历过程中，可增删元素的字典----------------------------------------------
class MyDict( dict ):
	def __iter__( self ):
		return dict( self ).__iter__()
	
	def keys( self ):
		return dict( self ).keys()
	
	def values( self ):
		return dict( self ).values()
	
	def items( self ):
		return dict( self ).items()

#-------------------------------------------------------------------------------------------------

def isMatchProfessions(professions, item):
	"""
	检测物品是否符合职业要求
	@return： true or false
	"""
	result = set(item.reqClasses) & set(professions) 
	return (len(result) > 0)

def filterProfessions(professions, itemList):
	"""
	professions是职业的列表
	itemList是物品实例的列表
	@return: 返回符合职业要求的物品
	"""
	return list(filter(lambda item:isMatchProfessions(professions, item), itemList))

def isMatchEquipParts(modelparts, item):
	"""
	检测物品是否符合装备部位要求
	"""
	if hasattr(item, "getEquipPart"):
		return len(set(list((item.getEquipPart(),))) & set(modelparts)) > 0
	else:
		return False

def filterEquipParts(modelparts, itemList):
	"""
	modelparts：装备部位的列表 
	itemList是物品实例的列表
	@return: 返回符合此装备部位的列表
	"""
	return list(filter(lambda item:isMatchEquipParts(modelparts, item), itemList))

def isMatchLevels(levels, item):
	"""
	levels：表示等级段范围，一般一个等级段的列表为[10,11,12,13,14,15,16,17,18,19]
	检测物品等级是否符合等级段要求
	"""
	return len(set(list((item.level,))) & set(levels)) > 0

def filterLevels(levels, itemList):
	"""
	levels：表示等级段范围，
	itemList是物品实例的列表
	@return: 返回符合等级要求的物品
	"""
	return list(filter(lambda item:isMatchLevels(levels, item), itemList))

def isMatchQuality(qualities, item):
	"""
	检测物品的品质是否符合要求
	"""
	return len(set(list((item.quality,))) & set(qualities)) > 0

def filterQualities(qualities, itemList):
	"""
	qualities：表示品质列表，
	itemList是物品实例的列表
	@return: 返回符合品质要求的物品
	"""
	return list(filter(lambda item:isMatchQuality(qualities, item), itemList))


#----------------------------------time---------------------------------------------------------------
def getTime( timeVal = 0.0 ):
	return int( ( time.time() + timeVal ) * csconst.TIME_ENLARGE_MULTIPLE )

def convertTime( timeVal  ):
	return timeVal/ csconst.TIME_ENLARGE_MULTIPLE

def convertToClientTime( timeVal ):
	return str( timeVal )

def convertClientTime( timerStr ):
	return int( timerStr )


pat = re.compile(r"^\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)(\s*\,|\s+)\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)(\s*\,|\s+)\s*-?([1-9]\d*\.{0,1}\d*|0\.\d*[1-9]\d*|0?\.0+|0)\s*$")

def vector3TypeConvert( param ):
	"""
	@param param: 将字符串转换成三维坐标，三个坐标之间式必须用空格分隔
	@return:	  Math.Vector3
	"""
	try:	#判断Vector3类型数据格式是否正确
		m = pat.match( param ).group().split()
		if len( m ) != 3:
			return None
	except:
		return None

	result = Math.Vector3( float( m[0] ), float( m[1] ), float( m[2] ) )
	return result
	
def rotate( origin, point, angle ):
	"""
	返回点p以点o为圆心逆时针旋转alpha(单位：弧度)后所在的位置
	"""
	ox,oy = origin
	px,py = point
	px -= ox
	py -= oy
	qx = ox + math.cos(angle) * px - math.sin(angle) * py
	qy = oy + math.sin(angle) * px + math.cos(angle) * py
	return qx, qy
	

#-----------------取点--------------------------------------

def halfCircleCalcHoverPosition( center, position, hoverRadiusMin, hoverRadiusMax ):
	"""
	计算徘徊位置（半圆）
	主要是为了避免“NPC游荡时直接穿透目标”的表现
	
	@param center: Vector3; 以这个为中心点
	@param position: Vector3;  
	"""
	# 限制移动范围在外圈到内圈之间,且满足以中心点到当前位置的朝向作为角平分线的180度范围内的点
	dst = position - center
	dst.y = 0
	if dst.length == 0:
		dst.x = random.uniform(-hoverRadiusMin, hoverRadiusMin)
		dst.z = random.uniform(-hoverRadiusMax, hoverRadiusMax)
	
	angle = random.uniform(-math.pi, math.pi)
	vet = Vector.rotalteXZ( dst, angle)
	l =  ( hoverRadiusMax - hoverRadiusMin ) * random.random() + hoverRadiusMin

	return Vector.normalize(vet)*l + center

def getRandomMovePoint( center, position, hoverRadiusMin, hoverRadiusMax ):
	"""
	"""
	global halfCircleCalcHoverPosition
	point = halfCircleCalcHoverPosition( center, position, hoverRadiusMin, hoverRadiusMax )
	return point

def getWanderMovePoint( position, targetPosition, radiusMin, radiusMax):
	"""
	取游荡移动目标点
	使用此方法的出来的点并不能保证在导航面上，
	所以此方法目前也只是个临时方案，后续需要针对这个需求进行讨论研究

	二维坐标下向量围绕圆点的逆时针旋转公式.顺时针旋转就把角度变为负：
 	x1 = x0 * cos（-B） - y0 * sin（-B） =>  x1 = x0 * cosB + y0 * sinB
 	y1 = x0 * sin（-B） + y0 * cos（-B）=>  y1 = -x0 * sinB + y0 * cosB
	"""
	#计算出两个目标点之间的distance，根据与radiusMin、radiusMax之间的大小关系进行跟情况
	distance = position.flatDistTo(targetPosition)
	v = Vector.normalize(targetPosition - position)
	posx = position.x
	posy = position.y
	posz = position.z
	
	dst = random.uniform(radiusMin, radiusMax)
	moveDireList = ["front","back","left","right"]

	moveDire = random.choice( moveDireList )
	if moveDire == "front":
		#如果是向正前方向移动
		if dst > distance:
			dst = distance
		vector = v*dst
	elif moveDire == "back":
		vector = v * (-dst)
	elif moveDire == "left":
		vector = Math.Vector3(-v.z,v.y,v.x)*dst
	elif moveDire == "right":
		vector = Math.Vector3(v.z,v.y,v.x)*dst

	posx = position.x + vector.x
	posz = position.z + vector.z
	return Math.Vector3( posx, posy, posz), moveDire
	
def moneyToStr( money ):
	"""
	金钱转化为带图标字符串，UCS3RichTextBlock格式
	"""
	colorstr =  "@F%i"
	#copperCoin = "@I{p=A3}"
	#silverCoin = "@I{p=A4}"
	goldCoin = "@I{p=A5}"
	#gold = money / 10000
	#silver = (money % 10000) / 100
	#copper = money % 100
	return " " + colorstr%money + goldCoin

def bindMoneyToStr( money ):
	"""
	金钱转化为带图标字符串，UCS3RichTextBlock格式
	"""
	colorstr =  "@F%i"
	#copperCoin = "@I{p=A13}"
	#silverCoin = "@I{p=A14}"
	goldCoin = "@I{p=A15}"
	#gold = money / 10000
	#silver = (money % 10000) / 100
	#copper = money % 100
	return " " + colorstr%money + goldCoin
	
def moneyToRichTextStr( money ):
	"""
	金钱转化为带图标字符串，商城购买的富文本格式
	"""
	colorstr = "<text color=\"#FFFFFFFF\">%d"
	#copperCoin = "</text><img filePath=\"Texture2D'/Game/Textures/UI/Common/T_GE_ICON_tongqian_D'\" size=\"[12, 12]\"/>"
	#silverCoin = "</text><img filePath=\"Texture2D'/Game/Textures/UI/Common/T_GE_ICON_yinqian_D'\" size=\"[12, 12]\"/>"
	goldCoin = "</text><img filePath=\"Texture2D'/Game/Textures/UI/Common/T_GE_ICON_jinqian_D'\" size=\"[12, 12]\"/>"
	
	#gold = money / 10000
	#silver = (money % 10000) / 100
	#copper = money % 100
	return " " + colorstr%money + goldCoin
	

def checkPositonIsInArea(srcPos, posList):
	"""
	检查一个点是否在一个多边形范围内 原理：判断这个点发送射线与几条边相交 奇数在安全区域里，否则不在
	"""
	XList = [pos.x for pos in posList]
	ZList = [pos.z for pos in posList]
	lastIndex = len(posList) -1
	MaxX = max(XList)
	MaxZ = max(ZList)
	MinX = min(XList)
	MinZ = min(ZList)

	if srcPos.x > MaxX or srcPos.x < MinX or srcPos.z > MaxZ or srcPos.z < MinZ:
		return False

	isInSaveArea = False
	for pos in posList:
		beValue = ( posList[lastIndex].z - pos.z )
		if beValue == 0:
			value = 0
		else:
			value = (posList[lastIndex].x - pos.x) * ( srcPos.z - pos.z ) / beValue
		boolY1 = pos.z > srcPos.z
		boolY2 = posList[lastIndex].z > srcPos.z
		if srcPos.x < (pos.x + value) and (boolY1 != boolY2):
			isInSaveArea = not isInSaveArea
		lastIndex = posList.index(pos)
	return isInSaveArea

#-------------------------------------------------------------------------------
def isUnreliable( entity ):
	"""
	判断对象是否不可靠
	"""
	if entity is None or entity.isDestroyed: 
		return True
	
	if KBEngine.component == "baseapp":
		pass
	elif KBEngine.component == "cellapp":
		if entity.inDestroying():
			return True
	else:
		assert False 
	return False
	
	