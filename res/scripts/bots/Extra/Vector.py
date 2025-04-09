import math
"""
本封装的向量是针对Vector3
"""
import math
from Math import Vector3

back =    Vector3(0.0, 0.0, -1)
forward = Vector3(0.0, 0.0, 1.0)
left =    Vector3(-1.0, 0.0, 0.0)
right =   Vector3(0.0, 0.0, 1.0)
up =      Vector3(0.0, 1.0, 0.0)
down =    Vector3(0.0, -1, 0.0)
zero =    Vector3(0.0, 0.0, 0.0)
one =     Vector3(1.0, 1.0, 1.0)


def dot(a, b):
	"""
	点乘
	"""
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def cross(a, b):
	"""
	叉乘
	"""
	value = type(a)(a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
	return value
	
def distance(a, b ):
	"""
	二点之间的距离
	"""
	c = a - b
	return magnitude(c)
	
def magnitude(a):
	"""
	返回向量的长度
	"""
	return math.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])

def normalize(a):
	"""
	返回单位向量
	"""
	len = magnitude(a)
	if len == 0:
		return type(a)(0.0, 0.0, 0.0)

	value = type(a)(a[0]/len, a[1]/len, a[2]/len)
	return value

def radian(from_v, to_v):
	"""
	由from和to两者返回一个角度。形象的说，from和to的连线和它们一个指定轴向的弧度。
	"""
	cosA = dot(from_v, to_v)/( magnitude(from_v) * magnitude(to_v) )
	return math.acos(cosA)

def rotalteXZ(v, angle):
	"""
	向量按照angle度数旋转
	argle是弧度
	"""
	x = v[0]*math.cos(angle) + 0 + (-v[2]*math.sin(angle))
	y = v[1]
	z = v[0]*math.sin(angle) + 0 + v[2]*math.cos(angle)
	return Vector3(x, y, z)
	
# alias
angle = radian

