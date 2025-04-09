# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    #url( r"^$", views.views, name = "views" ),
    url( r"^RequestCrossService", views.requestCrossService, name = "requestCrossService" ),
    url( r"^RequestReturnServer", views.requestReturnServer, name = "requestReturnServer" ),
    url( r"^ReturnServerFinished", views.returnServerFinished, name = "returnServerFinished" ),
    
    #请求跨服
    url( r"^$", views.views, name = "views" ),
]
