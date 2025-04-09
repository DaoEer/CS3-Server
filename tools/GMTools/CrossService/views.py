# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse

from .Scripts.CrossServiceInterface import g_CSInterfaceInst

@csrf_exempt
def views(request):
	return HttpResponse("Hello, world. You're at the polls index.")
	
@csrf_exempt
def requestCrossService(request):
	return g_CSInterfaceInst.requestCrossService(request)

@csrf_exempt	
def requestReturnServer(request):
	return g_CSInterfaceInst.requestReturnServer(request)

@csrf_exempt	
def returnServerFinished(request):
	return g_CSInterfaceInst.returnServerFinished(request)