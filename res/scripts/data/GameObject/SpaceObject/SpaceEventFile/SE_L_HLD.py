# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段完成，播放烈瞳出场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000039", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到镜头通知39，刷出烈瞳", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "39"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到烈瞳通知2，播放玩家离开镜头/获得三昧神火", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000040", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20000138"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到陷阱通知，播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000116", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "110", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20000164"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到镜头通知，刷暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "1", 
                    "param4": "20000130:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "1", 
                    "param4": "20000131:3", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "116"
                }
            ], 
            "id": 4
        }
    ], 
    15: [
        {
            "title": "玩家进入区域2，刷新第三批暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "3", 
                    "param4": "20000135:3", 
                    "id": 28
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "3", 
                    "param4": "20000136:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "3", 
                    "param4": "20000137:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010825", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "23", 
                    "param3": "-3680 -1758 14859", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "20000|10000"
                }
            ], 
            "id": 1
        }
    ]
}