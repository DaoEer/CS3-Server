# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "设置为一阶段", 
            "describe": "设置为一阶段", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 1
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040221", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "Q040218结束，发送指令给九天玄女", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "333", 
                    "param1": "20012271", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q040218", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "副本收到通知，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040222|Q040223|Q040217|Q040218", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "444", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012272"
                }
            ], 
            "id": 1
        }
    ]
}