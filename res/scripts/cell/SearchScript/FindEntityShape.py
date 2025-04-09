# -*- coding: utf-8 -*-

class FindEntityShape( object ):
	def __init__(self ):
		pass

	@staticmethod
	def rectangle( absX, absY, absZ, usePosition, targetPosition ):
		#正方形
		relativePosition = targetPosition - usePosition
		if absY > 0:
			if abs( relativePosition.x ) <= absX and abs( relativePosition.y ) <= absY and abs( relativePosition.z ) <= absZ:
				return True
		else:
			if abs( relativePosition.x ) <= absX and abs( relativePosition.z ) <= absZ:
				return True

		return False

	@staticmethod
	def circle( radius, absY, usePosition, targetPosition ):
		#圆形
		if  absY > 0:
			if targetPosition.flatDistTo( usePosition ) <= radius and ( abs(targetPosition.y - usePosition.y) <= absY ):
				return True
		else:
			if targetPosition.flatDistTo(usePosition) <= radius:
				return True

		return False
