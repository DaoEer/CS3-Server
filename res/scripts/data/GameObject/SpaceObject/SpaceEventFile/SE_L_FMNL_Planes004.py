# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "完成打败苍虬阶段，完成任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 20.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20101107", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 21.0, 
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
        }, 
        {
            "title": "阶段1完成，给Boss发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20001429", 
                    "param4": "", 
                    "id": 10
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
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "副本收到boss通知播放求饶语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020090", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020091", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 12.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020092", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20001429"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家进入区域1，刷第一波暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20000779", 
                    "param1": "1", 
                    "param4": "20001423:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "20000779", 
                    "param1": "1", 
                    "param4": "20001424:3", 
                    "id": 28
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020086", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "36353 -50845 -16985", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-11000|-21000"
                }
            ], 
            "id": 1
        }
    ]
}