# -*- coding: utf-8 -*-
import redis
from django.conf import settings

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_PWD = settings.REDIS_PWD
REDIS_DB = settings.REDIS_DB

class ModelRedis():
	def __init__( self ):
		self.db = redis.StrictRedis(host=REDIS_SERVER, password = REDIS_PWD, port=REDIS_PORT, db=REDIS_DB, decode_responses=True )
	
	def version( self ):
		return redis.VERSION
	
	#获取key
	def get( self, key ):
		return self.db.get( key )
	
	#设置key
	def set( self, key, val ):
		return self.db.set( key, val )

	#删除key
	def delete( self, key ):
		return self.db.delete( key )
	
	#设置hash指定 key的值
	def hset( self, hashKey, key, val ):
		return self.db.hset( hashKey, key, val )
	
	#获取hash指定 key的值
	def hget( self, hashKey, key ):
		return self.db.hget( hashKey, key )

	#删除hash指定 key的值
	def hdel( self, hashKey, key ):
		return self.db.hdel( hashKey, key )
		
	#获取hash所有值
	def hgetall( self, hashKey ):
		res = self.db.hgetall( hashKey )
		return res
	
	def clear( self ):
		res = self.db.flushdb()
		return res
	