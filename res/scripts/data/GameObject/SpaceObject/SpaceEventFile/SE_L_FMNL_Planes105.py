# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段2完成，设置玩家完成任务“千妖万魔林”", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101624", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FMNL", 
                    "param4": "", 
                    "id": 20
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
    15: [
        {
            "title": "玩家进入范围1，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020589", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020590", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "94822 14197 -15283", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-14283|-16283"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围2，刷跳出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "99759 20845 -12886", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-10886|-13886"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入范围3，刷四波怪物（跳出暗怪）", 
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
                    "param4": "40", 
                    "param3": "94406.953125 35157.089844 -8892.191406", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家进入范围4，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020592", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "86816.539063 32794.902344 -8406.205078", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-7406|-9406"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "进入范围5，播放祝融出场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000090", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "75050.156250 43370.144531 -5350.511230", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-4000|-16000"
                }
            ], 
            "id": 5
        }
    ]
}