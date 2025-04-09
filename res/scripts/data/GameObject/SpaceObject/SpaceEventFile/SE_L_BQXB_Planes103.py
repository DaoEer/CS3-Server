# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段2完成，发通知2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20005451", 
                    "param4": "", 
                    "id": 10
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
            "title": "位面收到通知，传送玩家出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_BQXB", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102532", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "101", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005451"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家到达某地，触发喊话1，移除加速BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040763", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11004100", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "-21165 -5814 -2086", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1586|-2586"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家到达某地，触发喊话2，发通知1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040764", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20005448|20005449|20005450|20005451", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-20925 -18914 -1762", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1262|-2262"
                }
            ], 
            "id": 2
        }
    ]
}