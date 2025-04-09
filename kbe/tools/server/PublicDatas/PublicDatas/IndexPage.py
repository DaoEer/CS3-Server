# -*- coding: utf-8 -*-
import json
from django.shortcuts import render

from . import Utils
from . import ModelRedis
from .Define import SUCCESS, FAIL, SERVER_KEY

class IndexPage( object ):
	@staticmethod
	def index( request ):
		r = ModelRedis.ModelRedis()
		context = {}
		context[ 'content' ] = r.version()
		return render( request,  'index.html', context )
	
	@staticmethod
	def get( request ):
		key = request.GET[ 'key' ]
		r = ModelRedis.ModelRedis()
		val = r.get( key )
		resp = {}
		resp[ key ] = val
		return Utils.HttpResponseJson(resp)
	
	@staticmethod
	def set( request ):
		key = request.GET["key"]
		value = request.GET["value"]
		r = ModelRedis.ModelRedis()
		result = r.set( key, value )
		resp = {}
		resp[ 'result' ] = result
		return Utils.HttpResponseJson(resp)
		
	@staticmethod
	def delete( request ):
		key = request.GET["key"]
		r = ModelRedis.ModelRedis()
		result = r.delete( key )
		resp = {}
		resp[ 'result' ] = result
		return Utils.HttpResponseJson(resp)
		
	@staticmethod
	def hget( request ):
		hashName = request.GET[ 'hash' ]
		key = request.GET[ 'key' ]
		r = ModelRedis.ModelRedis()
		value = r.hget( hashName, key  )
		resp = {}
		resp[key ] = value
		return Utils.HttpResponseJson(resp)
		
	@staticmethod
	def hset( request ):
		hashName = request.GET[ 'hash' ]
		key = request.GET[ 'key' ]
		val = request.GET[ 'value' ]
		r = ModelRedis.ModelRedis()
		result = r.hset( hashName,  key,  val )
		resp = {}
		resp[ 'result' ] = result
		return Utils.HttpResponseJson(resp)

	@staticmethod
	def hdel( request ):
		hashName = request.GET[ 'hash' ]
		key = request.GET[ 'key' ]
		r = ModelRedis.ModelRedis()
		result = r.hdel( hashName,  key )
		resp = {}
		resp[ 'result' ] = result
		return Utils.HttpResponseJson(resp)
	
	@staticmethod
	def hgetall( request ):
		hashName = request.GET[ 'hash' ]
		r = ModelRedis.ModelRedis()
		result = r.hgetall( hashName )
		return Utils.HttpResponseJson(resp)
	
	@staticmethod
	def clear( request ):
		r = ModelRedis.ModelRedis()
		result = r.clear()
		resp = {}
		resp[ 'result' ] = result
		return Utils.HttpResponseJson(resp)
		
	@staticmethod
	def recvLoginInfo( request ):
		"""
		"""
		result = {"return_code" : SUCCESS, "return_msg" : ""}
		GET = request.GET
		params = Utils.extractParam(**GET)
		key = params.get("key", None)
		if not key:
			result["return_code"] = FAIL
			result["return_msg"] = "Key Error"
			return Utils.HttpResponseJson(result)
			
		#签名不对
		if key != Utils.encryptSign(**params):
			result["return_code"] = FAIL
			result["return_msg"] = "Sign Key Error"
			return Utils.HttpResponseJson(result)
		
		server = params.get("server", None)
		if not server:
			result["return_code"] = FAIL
			result["return_msg"] = "not found server"
			return Utils.HttpResponseJson(result)
		
		#更新相应的数据到redis中
		r = ModelRedis.ModelRedis()
		return Utils.HttpResponseJson(result)
		
		